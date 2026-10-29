/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package კლავიატურა

import . "unsafe"

import . "პორტი"
import . "interrupt"
import . "console"

type Iთაგვიeventhandler interface {
	Onთაგვიdown(button int8)
	Onთაგვიზემოთ(button int8)
	Onთაგვიგადაადგილება(x int8, y int8)
}

var iთაგვიeventhandler Iთაგვიeventhandler

type Tნაგულისხმევითაგვიeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self Tნაგულისხმევითაგვიeventhandler) Onთაგვიdown(button int8) {
	buffer := []byte("+")
	console_2.Mბეჭდვაxy(buffer, uint16(previousx), uint16(previousy))
}
func (self Tნაგულისხმევითაგვიeventhandler) Onთაგვიზემოთ(button int8)	{}
func (self Tნაგულისხმევითაგვიeventhandler) Onთაგვიგადაადგილება(x int8, y int8) {

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
	console_2.Mბეჭდვაxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.Mბეჭდვაxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type Tთაგვიdriver struct {
	TInterrupthandler
}

var აქტიურითაგვიdriver *Tთაგვიdriver
var interrupthandler func(uint32) uint32

var dataპორტი_2 uint16 = 0x60
var ბრძანებაპორტი_2 uint16 = 0x64

const ps2ლოდინიlimit = 100000

func ლოდინიps2inputცარიელი() bool {
	for i := 0; i < ps2ლოდინიlimit; i++ {
		if (Pპორტიკითხვაbyte(ბრძანებაპორტი_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ლოდინიps2outputსრული() bool {
	for i := 0; i < ps2ლოდინიlimit; i++ {
		if (Pპორტიკითხვაbyte(ბრძანებაპორტი_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func ჩაწერაps2ბრძანება(მნიშვნელობა uint8) bool {
	if !ლოდინიps2inputცარიელი() {
		return false
	}
	Pპორტიჩაწერაbyte(ბრძანებაპორტი_2, მნიშვნელობა)
	return true
}

func ჩაწერაps2data(მნიშვნელობა uint8) bool {
	if !ლოდინიps2inputცარიელი() {
		return false
	}
	Pპორტიჩაწერაbyte(dataპორტი_2, მნიშვნელობა)
	return true
}

func კითხვაps2data() (uint8, bool) {
	if !ლოდინიps2outputსრული() {
		return 0, false
	}
	return Pპორტიკითხვაbyte(dataპორტი_2), true
}

func გაგზავნათაგვიბრძანება(მნიშვნელობა uint8) bool {
	if !ჩაწერაps2ბრძანება(0xD4) || !ჩაწერაps2data(მნიშვნელობა) {
		return false
	}
	ack, ok := კითხვაps2data()
	return ok && ack == 0xFA
}

func (self *Tთაგვიdriver) Initdriver(manager *TInterruptmanager, თაგვიeventhandler Iთაგვიeventhandler) {

	iთაგვიeventhandler = Tნაგულისხმევითაგვიeventhandler{}

	if თაგვიeventhandler != nil {
		iთაგვიeventhandler = თაგვიeventhandler
	}

	აქტიურითაგვიdriver = self
	interrupthandler = handleთაგვიinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Pპორტიკითხვაbyte(ბრძანებაპორტი_2)&0x01) != 0; i++ {
		Pპორტიკითხვაbyte(dataპორტი_2)
	}

	if !ჩაწერაps2ბრძანება(0xA8) || !ჩაწერაps2ბრძანება(0x20) {
		return
	}
	სტატუსი, ok := კითხვაps2data()
	if !ok {
		return
	}
	სტატუსი |= 0x02
	სტატუსი &^= 0x20
	if !ჩაწერაps2ბრძანება(0x60) || !ჩაწერაps2data(სტატუსი) {
		return
	}

	if !გაგზავნათაგვიბრძანება(0xF6) || !გაგზავნათაგვიბრძანება(0xF4) {
		return
	}
	offset = 0

}

func handleთაგვიinterrupt(esp uint32) uint32 {
	if აქტიურითაგვიdriver == nil {
		Pპორტიკითხვაbyte(dataპორტი_2)
		return esp
	}
	return აქტიურითაგვიdriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingთაგვიevent bool

func (self *Tთაგვიdriver) Handleinterrupt(esp uint32) uint32 {
	სტატუსი := Pპორტიკითხვაbyte(ბრძანებაპორტი_2)
	if (სტატუსი&0x01) == 0 || (სტატუსი&0x20) == 0 {
		return esp
	}

	data := Pპორტიკითხვაbyte(dataპორტი_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetსტატუსი := uint8(buffer_2[0])

		if (packetსტატუსი & 0xC0) == 0 {
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
		pendingbutton = int8(packetსტატუსი & 0x07)
		pendingთაგვიevent = true
	}

	return esp

}

func Pპროცესიpendingთაგვიevents() {
	if iთაგვიeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingთაგვიevent {
		Interruptაქტიური()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	ახალიbutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingთაგვიevent = false
	Interruptაქტიური()

	if x != 0 || y != 0 {
		iთაგვიeventhandler.Onთაგვიგადაადგილება(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (ახალიbutton & mask) != (oldbutton & mask) {
			if (ახალიbutton & mask) != 0 {
				iთაგვიeventhandler.Onთაგვიdown(int8(i + 1))
			} else {
				iთაგვიeventhandler.Onთაგვიზემოთ(int8(i + 1))
			}
		}
	}
	button_2 = ახალიbutton
}
