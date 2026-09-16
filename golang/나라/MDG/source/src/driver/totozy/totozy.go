/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fafanteny

import . "unsafe"

import . "irika"
import . "interrupt"
import . "konsoly"

type ITotozyeventhandler interface {
	OnTotozydown(button int8)
	OnTotozyAmbony(button int8)
	OnTotozyAfindrao(x int8, y int8)
}

var iTotozyeventhandler ITotozyeventhandler

type TTsotraTotozyeventhandler struct {
}

var konsoly_2 TKonsoly = TKonsoly{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (nytena TTsotraTotozyeventhandler) OnTotozydown(button int8) {
	buffer := []byte("+")
	konsoly_2.MAtontayxy(buffer, uint16(previousx), uint16(previousy))
}
func (nytena TTsotraTotozyeventhandler) OnTotozyAmbony(button int8)	{}
func (nytena TTsotraTotozyeventhandler) OnTotozyAfindrao(x int8, y int8) {

	xposition += int16(x)
	if xposition < 0 {
		xposition = 0
	}
	if xposition >= 80 {
		xposition = 79
	}

	yposition -= int16(y)

	if yposition < 0 {
		yposition = 0
	}
	if yposition >= 25 {
		yposition = 24
	}

	buffer := []byte(" ")
	konsoly_2.MAtontayxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konsoly_2.MAtontayxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type TTotozydriver struct {
	TInterrupthandler
}

var miasaTotozydriver *TTotozydriver
var interrupthandler func(uint32) uint32

var dataIrika_2 uint16 = 0x60
var baikoIrika_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputFoana() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (IrikaMamakybyte(baikoIrika_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputFeno() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (IrikaMamakybyte(baikoIrika_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func manoratraps2Baiko(sanda uint8) bool {
	if !waitps2inputFoana() {
		return false
	}
	IrikaManoratrabyte(baikoIrika_2, sanda)
	return true
}

func manoratraps2data(sanda uint8) bool {
	if !waitps2inputFoana() {
		return false
	}
	IrikaManoratrabyte(dataIrika_2, sanda)
	return true
}

func mamakyps2data() (uint8, bool) {
	if !waitps2outputFeno() {
		return 0, false
	}
	return IrikaMamakybyte(dataIrika_2), true
}

func sendTotozyBaiko(sanda uint8) bool {
	if !manoratraps2Baiko(0xD4) || !manoratraps2data(sanda) {
		return false
	}
	ack, ok := mamakyps2data()
	return ok && ack == 0xFA
}

func (nytena *TTotozydriver) Initdriver(mpandrindra *TInterruptMpandrindra, totozyeventhandler ITotozyeventhandler) {

	iTotozyeventhandler = TTsotraTotozyeventhandler{}

	if totozyeventhandler != nil {
		iTotozyeventhandler = totozyeventhandler
	}

	miasaTotozydriver = nytena
	interrupthandler = handleTotozyinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	nytena.Init(0x2C, uintptr(Pointer(mpandrindra)), address)

	for i := 0; i < 32 && (IrikaMamakybyte(baikoIrika_2)&0x01) != 0; i++ {
		IrikaMamakybyte(dataIrika_2)
	}

	if !manoratraps2Baiko(0xA8) || !manoratraps2Baiko(0x20) {
		return
	}
	fivoarana, ok := mamakyps2data()
	if !ok {
		return
	}
	fivoarana |= 0x02
	fivoarana &^= 0x20
	if !manoratraps2Baiko(0x60) || !manoratraps2data(fivoarana) {
		return
	}

	if !sendTotozyBaiko(0xF6) || !sendTotozyBaiko(0xF4) {
		return
	}
	offset = 0

}

func handleTotozyinterrupt(esp uint32) uint32 {
	if miasaTotozydriver == nil {
		IrikaMamakybyte(dataIrika_2)
		return esp
	}
	return miasaTotozydriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingTotozyevent bool

func (nytena *TTotozydriver) Handleinterrupt(esp uint32) uint32 {
	fivoarana := IrikaMamakybyte(baikoIrika_2)
	if (fivoarana&0x01) == 0 || (fivoarana&0x20) == 0 {
		return esp
	}

	data := IrikaMamakybyte(dataIrika_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetFivoarana := uint8(buffer_2[0])

		if (packetFivoarana & 0xC0) == 0 {
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
		pendingbutton = int8(packetFivoarana & 0x07)
		pendingTotozyevent = true
	}

	return esp

}

func ProcesspendingTotozyevents() {
	if iTotozyeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingTotozyevent {
		Interruptmiasa()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	vaovaobutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingTotozyevent = false
	Interruptmiasa()

	if x != 0 || y != 0 {
		iTotozyeventhandler.OnTotozyAfindrao(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (vaovaobutton & mask) != (oldbutton & mask) {
			if (vaovaobutton & mask) != 0 {
				iTotozyeventhandler.OnTotozydown(int8(i + 1))
			} else {
				iTotozyeventhandler.OnTotozyAmbony(int8(i + 1))
			}
		}
	}
	button_2 = vaovaobutton
}
