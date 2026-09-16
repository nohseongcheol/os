/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package klaviatura

import . "unsafe"

import . "port"
import . "interrupt"
import . "console"

type ISichqonchaeventhandler interface {
	YoqishSichqonchaPastga(tugma int8)
	YoqishSichqonchaYuqoriga(tugma int8)
	YoqishSichqonchaKoʻchirish(x int8, y int8)
}

var iSichqonchaeventhandler ISichqonchaeventhandler

type TAndozaSichqonchaeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xHolati int16 = 0
var yHolati int16 = 0

func (self TAndozaSichqonchaeventhandler) YoqishSichqonchaPastga(tugma int8) {
	buffer := []byte("+")
	console_2.MChopetishxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TAndozaSichqonchaeventhandler) YoqishSichqonchaYuqoriga(tugma int8)	{}
func (self TAndozaSichqonchaeventhandler) YoqishSichqonchaKoʻchirish(x int8, y int8) {

	xHolati += int16(x)
	if xHolati < 0 {
		xHolati = 0
	}
	if xHolati >= 80 {
		xHolati = 79
	}

	yHolati -= int16(y)

	if yHolati < 0 {
		yHolati = 0
	}
	if yHolati >= 25 {
		yHolati = 24
	}

	buffer := []byte(" ")
	console_2.MChopetishxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MChopetishxy(buffer, uint16(xHolati), uint16(yHolati))

	previousx = xHolati
	previousy = yHolati
}

type TSichqonchadriver struct {
	TInterrupthandler
}

var faolSichqonchadriver *TSichqonchadriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var buyruqport_2 uint16 = 0x64

const ps2Kutishlimit = 100000

func kutishps2inputBosh() bool {
	for i := 0; i < ps2Kutishlimit; i++ {
		if (PortOʻqishbyte(buyruqport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func kutishps2outputTola() bool {
	for i := 0; i < ps2Kutishlimit; i++ {
		if (PortOʻqishbyte(buyruqport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func yozishps2Buyruq(qiymat uint8) bool {
	if !kutishps2inputBosh() {
		return false
	}
	PortYozishbyte(buyruqport_2, qiymat)
	return true
}

func yozishps2data(qiymat uint8) bool {
	if !kutishps2inputBosh() {
		return false
	}
	PortYozishbyte(dataport_2, qiymat)
	return true
}

func oʻqishps2data() (uint8, bool) {
	if !kutishps2outputTola() {
		return 0, false
	}
	return PortOʻqishbyte(dataport_2), true
}

func joʻnatishSichqonchaBuyruq(qiymat uint8) bool {
	if !yozishps2Buyruq(0xD4) || !yozishps2data(qiymat) {
		return false
	}
	ack, ok := oʻqishps2data()
	return ok && ack == 0xFA
}

func (self *TSichqonchadriver) Initdriver(manager *TInterruptmanager, sichqonchaeventhandler ISichqonchaeventhandler) {

	iSichqonchaeventhandler = TAndozaSichqonchaeventhandler{}

	if sichqonchaeventhandler != nil {
		iSichqonchaeventhandler = sichqonchaeventhandler
	}

	faolSichqonchadriver = self
	interrupthandler = handleSichqonchainterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortOʻqishbyte(buyruqport_2)&0x01) != 0; i++ {
		PortOʻqishbyte(dataport_2)
	}

	if !yozishps2Buyruq(0xA8) || !yozishps2Buyruq(0x20) {
		return
	}
	holat, ok := oʻqishps2data()
	if !ok {
		return
	}
	holat |= 0x02
	holat &^= 0x20
	if !yozishps2Buyruq(0x60) || !yozishps2data(holat) {
		return
	}

	if !joʻnatishSichqonchaBuyruq(0xF6) || !joʻnatishSichqonchaBuyruq(0xF4) {
		return
	}
	offset = 0

}

func handleSichqonchainterrupt(esp uint32) uint32 {
	if faolSichqonchadriver == nil {
		PortOʻqishbyte(dataport_2)
		return esp
	}
	return faolSichqonchadriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var tugma_2 int8
var pendingx int16
var pendingy int16
var pendingTugma int8
var pendingSichqonchaevent bool

func (self *TSichqonchadriver) Handleinterrupt(esp uint32) uint32 {
	holat := PortOʻqishbyte(buyruqport_2)
	if (holat&0x01) == 0 || (holat&0x20) == 0 {
		return esp
	}

	data := PortOʻqishbyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetHolat := uint8(buffer_2[0])

		if (packetHolat & 0xC0) == 0 {
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
		pendingTugma = int8(packetHolat & 0x07)
		pendingSichqonchaevent = true
	}

	return esp

}

func JarayonpendingSichqonchaevents() {
	if iSichqonchaeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingSichqonchaevent {
		Interruptfaol()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	yangiTugma := pendingTugma
	oldTugma := tugma_2

	pendingx = 0
	pendingy = 0
	pendingSichqonchaevent = false
	Interruptfaol()

	if x != 0 || y != 0 {
		iSichqonchaeventhandler.YoqishSichqonchaKoʻchirish(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (yangiTugma & mask) != (oldTugma & mask) {
			if (yangiTugma & mask) != 0 {
				iSichqonchaeventhandler.YoqishSichqonchaPastga(int8(i + 1))
			} else {
				iSichqonchaeventhandler.YoqishSichqonchaYuqoriga(int8(i + 1))
			}
		}
	}
	tugma_2 = yangiTugma
}
