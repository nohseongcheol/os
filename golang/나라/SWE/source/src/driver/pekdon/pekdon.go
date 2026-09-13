package tangentbord

import . "unsafe"

import . "port"
import . "avbrott"
import . "konsol"

type IMusHändelsehandler interface {
	PåMusNer(knapp int8)
	PåMusUpp(knapp int8)
	PåMusFlytta(x int8, y int8)
}

var iMusHändelsehandler IMusHändelsehandler

type TStandardMusHändelsehandler struct {
}

var konsol_2 TKonsol = TKonsol{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (själv TStandardMusHändelsehandler) PåMusNer(knapp int8) {
	buffer := []byte("+")
	konsol_2.MSkrivutxy(buffer, uint16(previousx), uint16(previousy))
}
func (själv TStandardMusHändelsehandler) PåMusUpp(knapp int8)	{}
func (själv TStandardMusHändelsehandler) PåMusFlytta(x int8, y int8) {

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
	konsol_2.MSkrivutxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konsol_2.MSkrivutxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type TMusdriver struct {
	TAvbrotthandler
}

var aktivMusdriver *TMusdriver
var avbrotthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var kommandoport_2 uint16 = 0x64

const ps2VäntaGräns = 100000

func väntaps2InmatningTom() bool {
	for i := 0; i < ps2VäntaGräns; i++ {
		if (PortLäsbyte(kommandoport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func väntaps2UtmatningFullständig() bool {
	for i := 0; i < ps2VäntaGräns; i++ {
		if (PortLäsbyte(kommandoport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skrivps2Kommando(värde uint8) bool {
	if !väntaps2InmatningTom() {
		return false
	}
	PortSkrivbyte(kommandoport_2, värde)
	return true
}

func skrivps2data(värde uint8) bool {
	if !väntaps2InmatningTom() {
		return false
	}
	PortSkrivbyte(dataport_2, värde)
	return true
}

func läsps2data() (uint8, bool) {
	if !väntaps2UtmatningFullständig() {
		return 0, false
	}
	return PortLäsbyte(dataport_2), true
}

func skickaMusKommando(värde uint8) bool {
	if !skrivps2Kommando(0xD4) || !skrivps2data(värde) {
		return false
	}
	ack, ok := läsps2data()
	return ok && ack == 0xFA
}

func (själv *TMusdriver) Initdriver(manager *TAvbrottmanager, musHändelsehandler IMusHändelsehandler) {

	iMusHändelsehandler = TStandardMusHändelsehandler{}

	if musHändelsehandler != nil {
		iMusHändelsehandler = musHändelsehandler
	}

	aktivMusdriver = själv
	avbrotthandler = handtagMusAvbrott
	var adress uintptr
	adress = uintptr(Pointer(&avbrotthandler))
	själv.Init(0x2C, uintptr(Pointer(manager)), adress)

	for i := 0; i < 32 && (PortLäsbyte(kommandoport_2)&0x01) != 0; i++ {
		PortLäsbyte(dataport_2)
	}

	if !skrivps2Kommando(0xA8) || !skrivps2Kommando(0x20) {
		return
	}
	status, ok := läsps2data()
	if !ok {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !skrivps2Kommando(0x60) || !skrivps2data(status) {
		return
	}

	if !skickaMusKommando(0xF6) || !skickaMusKommando(0xF4) {
		return
	}
	förskjutning = 0

}

func handtagMusAvbrott(esp uint32) uint32 {
	if aktivMusdriver == nil {
		PortLäsbyte(dataport_2)
		return esp
	}
	return aktivMusdriver.HandtagAvbrott(esp)
}

var antal uint8 = 0
var buffer_2 [3]int8
var förskjutning uint8 = 0

var knapp_2 int8
var pendingx int16
var pendingy int16
var pendingKnapp int8
var pendingMusHändelse bool

func (själv *TMusdriver) HandtagAvbrott(esp uint32) uint32 {
	status := PortLäsbyte(kommandoport_2)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	data := PortLäsbyte(dataport_2)

	if förskjutning == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[förskjutning] = int8(data)
	förskjutning = (förskjutning + 1) % 3
	if förskjutning == 0 {
		pAKETstatus := uint8(buffer_2[0])

		if (pAKETstatus & 0xC0) == 0 {
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
		pendingKnapp = int8(pAKETstatus & 0x07)
		pendingMusHändelse = true
	}

	return esp

}

func ProcesspendingMusHändelser() {
	if iMusHändelsehandler == nil {
		return
	}

	Avbrottdeactive()
	if !pendingMusHändelse {
		AvbrottAktiv()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	nyKnapp := pendingKnapp
	oldKnapp := knapp_2

	pendingx = 0
	pendingy = 0
	pendingMusHändelse = false
	AvbrottAktiv()

	if x != 0 || y != 0 {
		iMusHändelsehandler.PåMusFlytta(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (nyKnapp & mask) != (oldKnapp & mask) {
			if (nyKnapp & mask) != 0 {
				iMusHändelsehandler.PåMusNer(int8(i + 1))
			} else {
				iMusHändelsehandler.PåMusUpp(int8(i + 1))
			}
		}
	}
	knapp_2 = nyKnapp
}
