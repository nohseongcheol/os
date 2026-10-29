/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tastatur

import . "unsafe"

import . "port"
import . "interrupt"
import . "console"

type IMuseventhandler interface {
	TændtMusNed(knap int8)
	TændtMusOp(knap int8)
	TændtMusFlyt(x int8, y int8)
}

var iMuseventhandler IMuseventhandler

type TStandardMuseventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPlacering int16 = 0
var yPlacering int16 = 0

func (selv TStandardMuseventhandler) TændtMusNed(knap int8) {
	buffer := []byte("+")
	console_2.MUdskrivxy(buffer, uint16(previousx), uint16(previousy))
}
func (selv TStandardMuseventhandler) TændtMusOp(knap int8)	{}
func (selv TStandardMuseventhandler) TændtMusFlyt(x int8, y int8) {

	xPlacering += int16(x)
	if xPlacering < 0 {
		xPlacering = 0
	}
	if xPlacering >= 80 {
		xPlacering = 79
	}

	yPlacering -= int16(y)

	if yPlacering < 0 {
		yPlacering = 0
	}
	if yPlacering >= 25 {
		yPlacering = 24
	}

	buffer := []byte(" ")
	console_2.MUdskrivxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MUdskrivxy(buffer, uint16(xPlacering), uint16(yPlacering))

	previousx = xPlacering
	previousy = yPlacering
}

type TMusdriver struct {
	TInterrupthandler
}

var aktivMusdriver *TMusdriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var kommandoport_2 uint16 = 0x64

const ps2Ventlimit = 100000

func ventps2IndgangTom() bool {
	for i := 0; i < ps2Ventlimit; i++ {
		if (PortLæsebyte(kommandoport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ventps2UdgangFuldt() bool {
	for i := 0; i < ps2Ventlimit; i++ {
		if (PortLæsebyte(kommandoport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skriveps2Kommando(værdi uint8) bool {
	if !ventps2IndgangTom() {
		return false
	}
	PortSkrivebyte(kommandoport_2, værdi)
	return true
}

func skriveps2data(værdi uint8) bool {
	if !ventps2IndgangTom() {
		return false
	}
	PortSkrivebyte(dataport_2, værdi)
	return true
}

func læseps2data() (uint8, bool) {
	if !ventps2UdgangFuldt() {
		return 0, false
	}
	return PortLæsebyte(dataport_2), true
}

func sendMusKommando(værdi uint8) bool {
	if !skriveps2Kommando(0xD4) || !skriveps2data(værdi) {
		return false
	}
	ack, ok := læseps2data()
	return ok && ack == 0xFA
}

func (selv *TMusdriver) Initdriver(manager *TInterruptmanager, museventhandler IMuseventhandler) {

	iMuseventhandler = TStandardMuseventhandler{}

	if museventhandler != nil {
		iMuseventhandler = museventhandler
	}

	aktivMusdriver = selv
	interrupthandler = håndtagMusinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	selv.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortLæsebyte(kommandoport_2)&0x01) != 0; i++ {
		PortLæsebyte(dataport_2)
	}

	if !skriveps2Kommando(0xA8) || !skriveps2Kommando(0x20) {
		return
	}
	status, ok := læseps2data()
	if !ok {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !skriveps2Kommando(0x60) || !skriveps2data(status) {
		return
	}

	if !sendMusKommando(0xF6) || !sendMusKommando(0xF4) {
		return
	}
	forskydning = 0

}

func håndtagMusinterrupt(esp uint32) uint32 {
	if aktivMusdriver == nil {
		PortLæsebyte(dataport_2)
		return esp
	}
	return aktivMusdriver.Håndtaginterrupt(esp)
}

var antal uint8 = 0
var buffer_2 [3]int8
var forskydning uint8 = 0

var knap_2 int8
var pendingx int16
var pendingy int16
var pendingKnap int8
var pendingMusevent bool

func (selv *TMusdriver) Håndtaginterrupt(esp uint32) uint32 {
	status := PortLæsebyte(kommandoport_2)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	data := PortLæsebyte(dataport_2)

	if forskydning == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[forskydning] = int8(data)
	forskydning = (forskydning + 1) % 3
	if forskydning == 0 {
		packetstatus := uint8(buffer_2[0])

		if (packetstatus & 0xC0) == 0 {
			pendingx += int16(buffer_2[1])
			pendingy += int16(buffer_2[2])
			if pendingx > 127 {
				pendingx = 127
			} else if pendingx < -127 {
				pendingx = -127
			}
			if pendingy > 127 {
				pendingy = 127
			} else if pendingy < -127 {
				pendingy = -127
			}
		}
		pendingKnap = int8(packetstatus & 0x07)
		pendingMusevent = true
	}

	return esp

}

func ProcespendingMusBegivenheder() {
	if iMuseventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingMusevent {
		InterruptAktiv()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	nyKnap := pendingKnap
	gammelKnap := knap_2

	pendingx = 0
	pendingy = 0
	pendingMusevent = false
	InterruptAktiv()

	if x != 0 || y != 0 {
		iMuseventhandler.TændtMusFlyt(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maske := int8(0x1 << i)
		if (nyKnap & maske) != (gammelKnap & maske) {
			if (nyKnap & maske) != 0 {
				iMuseventhandler.TændtMusNed(int8(i + 1))
			} else {
				iMuseventhandler.TændtMusOp(int8(i + 1))
			}
		}
	}
	knap_2 = nyKnap
}
