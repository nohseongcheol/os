package mwandikisho

import . "unsafe"

import . "umuyoboro"
import . "interrupt"
import . "console"

type IImbebaeventhandler interface {
	KuriImbebadown(button int8)
	KuriImbebaup(button int8)
	KuriImbebamove(x int8, y int8)
}

var iImbebaeventhandler IImbebaeventhandler

type TMburabuziImbebaeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self TMburabuziImbebaeventhandler) KuriImbebadown(button int8) {
	buffer := []byte("+")
	console_2.MGucapaxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TMburabuziImbebaeventhandler) KuriImbebaup(button int8)	{}
func (self TMburabuziImbebaeventhandler) KuriImbebamove(x int8, y int8) {

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
	console_2.MGucapaxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MGucapaxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type TImbebadriver struct {
	TInterrupthandler
}

var gikoraImbebadriver *TImbebadriver
var interrupthandler func(uint32) uint32

var dataUmuyoboro_2 uint16 = 0x60
var icyowifuzaUmuyoboro_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Umuyoborogusomabyte(icyowifuzaUmuyoboro_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputfull() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (Umuyoborogusomabyte(icyowifuzaUmuyoboro_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func kwandikaps2Icyowifuza(agaciro uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Umuyoborokwandikabyte(icyowifuzaUmuyoboro_2, agaciro)
	return true
}

func kwandikaps2data(agaciro uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	Umuyoborokwandikabyte(dataUmuyoboro_2, agaciro)
	return true
}

func gusomaps2data() (uint8, bool) {
	if !waitps2outputfull() {
		return 0, false
	}
	return Umuyoborogusomabyte(dataUmuyoboro_2), true
}

func sendImbebaIcyowifuza(agaciro uint8) bool {
	if !kwandikaps2Icyowifuza(0xD4) || !kwandikaps2data(agaciro) {
		return false
	}
	ack, yEGO := gusomaps2data()
	return yEGO && ack == 0xFA
}

func (self *TImbebadriver) Initdriver(manager *TInterruptmanager, imbebaeventhandler IImbebaeventhandler) {

	iImbebaeventhandler = TMburabuziImbebaeventhandler{}

	if imbebaeventhandler != nil {
		iImbebaeventhandler = imbebaeventhandler
	}

	gikoraImbebadriver = self
	interrupthandler = handleImbebainterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Umuyoborogusomabyte(icyowifuzaUmuyoboro_2)&0x01) != 0; i++ {
		Umuyoborogusomabyte(dataUmuyoboro_2)
	}

	if !kwandikaps2Icyowifuza(0xA8) || !kwandikaps2Icyowifuza(0x20) {
		return
	}
	imimerere, yEGO := gusomaps2data()
	if !yEGO {
		return
	}
	imimerere |= 0x02
	imimerere &^= 0x20
	if !kwandikaps2Icyowifuza(0x60) || !kwandikaps2data(imimerere) {
		return
	}

	if !sendImbebaIcyowifuza(0xF6) || !sendImbebaIcyowifuza(0xF4) {
		return
	}
	offset = 0

}

func handleImbebainterrupt(esp uint32) uint32 {
	if gikoraImbebadriver == nil {
		Umuyoborogusomabyte(dataUmuyoboro_2)
		return esp
	}
	return gikoraImbebadriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingImbebaevent bool

func (self *TImbebadriver) Handleinterrupt(esp uint32) uint32 {
	imimerere := Umuyoborogusomabyte(icyowifuzaUmuyoboro_2)
	if (imimerere&0x01) == 0 || (imimerere&0x20) == 0 {
		return esp
	}

	data := Umuyoborogusomabyte(dataUmuyoboro_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetImimerere := uint8(buffer_2[0])

		if (packetImimerere & 0xC0) == 0 {
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
		pendingbutton = int8(packetImimerere & 0x07)
		pendingImbebaevent = true
	}

	return esp

}

func ProcesspendingImbebaevents() {
	if iImbebaeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingImbebaevent {
		InterruptGikora()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	newbutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingImbebaevent = false
	InterruptGikora()

	if x != 0 || y != 0 {
		iImbebaeventhandler.KuriImbebamove(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (newbutton & mask) != (oldbutton & mask) {
			if (newbutton & mask) != 0 {
				iImbebaeventhandler.KuriImbebadown(int8(i + 1))
			} else {
				iImbebaeventhandler.KuriImbebaup(int8(i + 1))
			}
		}
	}
	button_2 = newbutton
}
