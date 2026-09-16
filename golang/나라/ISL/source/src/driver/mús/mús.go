/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package lyklaborð

import . "unsafe"

import . "port"
import . "interrupt"
import . "console"

type IMúseventhandler interface {
	NotaMúsNiður(hnappur int8)
	NotaMúsUpp(hnappur int8)
	NotaMúsFæra(x int8, y int8)
}

var iMúseventhandler IMúseventhandler

type TSjálfgefiðMúseventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xStaða int16 = 0
var yStaða int16 = 0

func (sjálft TSjálfgefiðMúseventhandler) NotaMúsNiður(hnappur int8) {
	buffer := []byte("+")
	console_2.MPrentaxy(buffer, uint16(previousx), uint16(previousy))
}
func (sjálft TSjálfgefiðMúseventhandler) NotaMúsUpp(hnappur int8)	{}
func (sjálft TSjálfgefiðMúseventhandler) NotaMúsFæra(x int8, y int8) {

	xStaða += int16(x)
	if xStaða < 0 {
		xStaða = 0
	}
	if xStaða >= 80 {
		xStaða = 79
	}

	yStaða -= int16(y)

	if yStaða < 0 {
		yStaða = 0
	}
	if yStaða >= 25 {
		yStaða = 24
	}

	buffer := []byte(" ")
	console_2.MPrentaxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MPrentaxy(buffer, uint16(xStaða), uint16(yStaða))

	previousx = xStaða
	previousy = yStaða
}

type TMúsdriver struct {
	TInterrupthandler
}

var virktMúsdriver *TMúsdriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var skipunport_2 uint16 = 0x64

const ps2Bíðalimit = 100000

func bíðaps2InntakTómt() bool {
	for i := 0; i < ps2Bíðalimit; i++ {
		if (PortLesturbyte(skipunport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func bíðaps2outputMikið() bool {
	for i := 0; i < ps2Bíðalimit; i++ {
		if (PortLesturbyte(skipunport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func skriftps2Skipun(gildi uint8) bool {
	if !bíðaps2InntakTómt() {
		return false
	}
	PortSkriftbyte(skipunport_2, gildi)
	return true
}

func skriftps2data(gildi uint8) bool {
	if !bíðaps2InntakTómt() {
		return false
	}
	PortSkriftbyte(dataport_2, gildi)
	return true
}

func lesturps2data() (uint8, bool) {
	if !bíðaps2outputMikið() {
		return 0, false
	}
	return PortLesturbyte(dataport_2), true
}

func sendaMúsSkipun(gildi uint8) bool {
	if !skriftps2Skipun(0xD4) || !skriftps2data(gildi) {
		return false
	}
	ack, ílagi := lesturps2data()
	return ílagi && ack == 0xFA
}

func (sjálft *TMúsdriver) Initdriver(manager *TInterruptmanager, múseventhandler IMúseventhandler) {

	iMúseventhandler = TSjálfgefiðMúseventhandler{}

	if múseventhandler != nil {
		iMúseventhandler = múseventhandler
	}

	virktMúsdriver = sjálft
	interrupthandler = haldfangMúsinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	sjálft.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortLesturbyte(skipunport_2)&0x01) != 0; i++ {
		PortLesturbyte(dataport_2)
	}

	if !skriftps2Skipun(0xA8) || !skriftps2Skipun(0x20) {
		return
	}
	staða_3, ílagi := lesturps2data()
	if !ílagi {
		return
	}
	staða_3 |= 0x02
	staða_3 &^= 0x20
	if !skriftps2Skipun(0x60) || !skriftps2data(staða_3) {
		return
	}

	if !sendaMúsSkipun(0xF6) || !sendaMúsSkipun(0xF4) {
		return
	}
	offset = 0

}

func haldfangMúsinterrupt(esp uint32) uint32 {
	if virktMúsdriver == nil {
		PortLesturbyte(dataport_2)
		return esp
	}
	return virktMúsdriver.Haldfanginterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var hnappur_2 int8
var pendingx int16
var pendingy int16
var pendingHnappur int8
var pendingMúsevent bool

func (sjálft *TMúsdriver) Haldfanginterrupt(esp uint32) uint32 {
	staða_3 := PortLesturbyte(skipunport_2)
	if (staða_3&0x01) == 0 || (staða_3&0x20) == 0 {
		return esp
	}

	data := PortLesturbyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetStaða := uint8(buffer_2[0])

		if (packetStaða & 0xC0) == 0 {
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
		pendingHnappur = int8(packetStaða & 0x07)
		pendingMúsevent = true
	}

	return esp

}

func ProcesspendingMúsevents() {
	if iMúseventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingMúsevent {
		InterruptVirkt()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	nýttHnappur := pendingHnappur
	oldHnappur := hnappur_2

	pendingx = 0
	pendingy = 0
	pendingMúsevent = false
	InterruptVirkt()

	if x != 0 || y != 0 {
		iMúseventhandler.NotaMúsFæra(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		möskvi := int8(0x1 << i)
		if (nýttHnappur & möskvi) != (oldHnappur & möskvi) {
			if (nýttHnappur & möskvi) != 0 {
				iMúseventhandler.NotaMúsNiður(int8(i + 1))
			} else {
				iMúseventhandler.NotaMúsUpp(int8(i + 1))
			}
		}
	}
	hnappur_2 = nýttHnappur
}
