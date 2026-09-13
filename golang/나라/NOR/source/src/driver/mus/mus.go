package tastatur

import . "unsafe"

import . "port"
import . "avbrudd"
import . "console"

type IMusHendelsehandler interface {
	PåMusNed(knapp int8)
	PåMusOpp(knapp int8)
	PåMusFlytt(x int8, y int8)
}

var iMusHendelsehandler IMusHendelsehandler

type TStandardMusHendelsehandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPosisjon int16 = 0
var yPosisjon int16 = 0

func (selv TStandardMusHendelsehandler) PåMusNed(knapp int8) {
	buffer := []byte("+")
	console_2.MSkrivutxy(buffer, uint16(previousx), uint16(previousy))
}
func (selv TStandardMusHendelsehandler) PåMusOpp(knapp int8)	{}
func (selv TStandardMusHendelsehandler) PåMusFlytt(x int8, y int8) {

	xPosisjon += int16(x)
	if xPosisjon < 0 {
		xPosisjon = 0
	}
	if xPosisjon >= 80 {
		xPosisjon = 79
	}

	yPosisjon -= int16(y)

	if yPosisjon < 0 {
		yPosisjon = 0
	}
	if yPosisjon >= 25 {
		yPosisjon = 24
	}

	buffer := []byte(" ")
	console_2.MSkrivutxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MSkrivutxy(buffer, uint16(xPosisjon), uint16(yPosisjon))

	previousx = xPosisjon
	previousy = yPosisjon
}

type TMusdriver struct {
	TAvbruddhandler
}

var aktivMusdriver *TMusdriver
var avbruddhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var kommandoport_2 uint16 = 0x64

const ps2VentGrense = 100000

func ventps2InndataTom() bool {
	for i := 0; i < ps2VentGrense; i++ {
		if (PortLesbyte(kommandoport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ventps2Utdatafull() bool {
	for i := 0; i < ps2VentGrense; i++ {
		if (PortLesbyte(kommandoport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skrivps2Kommando(verdi uint8) bool {
	if !ventps2InndataTom() {
		return false
	}
	PortSkrivbyte(kommandoport_2, verdi)
	return true
}

func skrivps2data(verdi uint8) bool {
	if !ventps2InndataTom() {
		return false
	}
	PortSkrivbyte(dataport_2, verdi)
	return true
}

func lesps2data() (uint8, bool) {
	if !ventps2Utdatafull() {
		return 0, false
	}
	return PortLesbyte(dataport_2), true
}

func sendMusKommando(verdi uint8) bool {
	if !skrivps2Kommando(0xD4) || !skrivps2data(verdi) {
		return false
	}
	ack, ok := lesps2data()
	return ok && ack == 0xFA
}

func (selv *TMusdriver) Initdriver(manager *TAvbruddmanager, musHendelsehandler IMusHendelsehandler) {

	iMusHendelsehandler = TStandardMusHendelsehandler{}

	if musHendelsehandler != nil {
		iMusHendelsehandler = musHendelsehandler
	}

	aktivMusdriver = selv
	avbruddhandler = håndtakMusAvbrudd
	var address uintptr
	address = uintptr(Pointer(&avbruddhandler))
	selv.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortLesbyte(kommandoport_2)&0x01) != 0; i++ {
		PortLesbyte(dataport_2)
	}

	if !skrivps2Kommando(0xA8) || !skrivps2Kommando(0x20) {
		return
	}
	status, ok := lesps2data()
	if !ok {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !skrivps2Kommando(0x60) || !skrivps2data(status) {
		return
	}

	if !sendMusKommando(0xF6) || !sendMusKommando(0xF4) {
		return
	}
	avstand = 0

}

func håndtakMusAvbrudd(esp uint32) uint32 {
	if aktivMusdriver == nil {
		PortLesbyte(dataport_2)
		return esp
	}
	return aktivMusdriver.HåndtakAvbrudd(esp)
}

var antall uint8 = 0
var buffer_2 [3]int8
var avstand uint8 = 0

var knapp_2 int8
var pendingx int16
var pendingy int16
var pendingKnapp int8
var pendingMusHendelse bool

func (selv *TMusdriver) HåndtakAvbrudd(esp uint32) uint32 {
	status := PortLesbyte(kommandoport_2)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	data := PortLesbyte(dataport_2)

	if avstand == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[avstand] = int8(data)
	avstand = (avstand + 1) % 3
	if avstand == 0 {
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
		pendingKnapp = int8(packetstatus & 0x07)
		pendingMusHendelse = true
	}

	return esp

}

func ProsesspendingMusevents() {
	if iMusHendelsehandler == nil {
		return
	}

	Avbrudddeactive()
	if !pendingMusHendelse {
		AvbruddAktiv()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	nyKnapp := pendingKnapp
	gammelKnapp := knapp_2

	pendingx = 0
	pendingy = 0
	pendingMusHendelse = false
	AvbruddAktiv()

	if x != 0 || y != 0 {
		iMusHendelsehandler.PåMusFlytt(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maske := int8(0x1 << i)
		if (nyKnapp & maske) != (gammelKnapp & maske) {
			if (nyKnapp & maske) != 0 {
				iMusHendelsehandler.PåMusNed(int8(i + 1))
			} else {
				iMusHendelsehandler.PåMusOpp(int8(i + 1))
			}
		}
	}
	knapp_2 = nyKnapp
}
