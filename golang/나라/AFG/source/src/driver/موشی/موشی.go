/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package صفحهکلید

import . "unsafe"

import . "درگاه"
import . "interrupt"
import . "console"

type Iموشیeventhandler interface {
	Oروشنموشیپایین(دکمه int8)
	Oروشنموشیبالا(دکمه int8)
	Oروشنموشیانتقال(x int8, y int8)
}

var iموشیeventhandler Iموشیeventhandler

type TDefaultموشیeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (خود TDefaultموشیeventhandler) Oروشنموشیپایین(دکمه int8) {
	buffer := []byte("+")
	console_2.Mچاپxy(buffer, uint16(previousx), uint16(previousy))
}
func (خود TDefaultموشیeventhandler) Oروشنموشیبالا(دکمه int8)	{}
func (خود TDefaultموشیeventhandler) Oروشنموشیانتقال(x int8, y int8) {

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
	console_2.Mچاپxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.Mچاپxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type Tموشیdriver struct {
	TInterrupthandler
}

var فعالموشیdriver *Tموشیdriver
var interrupthandler func(uint32) uint32

var dataدرگاه_2 uint16 = 0x60
var فرماندرگاه_2 uint16 = 0x64

const ps2انتظارlimit = 100000

func انتظارps2ورودیempty() bool {
	for i := 0; i < ps2انتظارlimit; i++ {
		if (Pدرگاهخواندنbyte(فرماندرگاه_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func انتظارps2خروجیfull() bool {
	for i := 0; i < ps2انتظارlimit; i++ {
		if (Pدرگاهخواندنbyte(فرماندرگاه_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func نوشتنps2فرمان(مقدار uint8) bool {
	if !انتظارps2ورودیempty() {
		return false
	}
	Pدرگاهنوشتنbyte(فرماندرگاه_2, مقدار)
	return true
}

func نوشتنps2data(مقدار uint8) bool {
	if !انتظارps2ورودیempty() {
		return false
	}
	Pدرگاهنوشتنbyte(dataدرگاه_2, مقدار)
	return true
}

func خواندنps2data() (uint8, bool) {
	if !انتظارps2خروجیfull() {
		return 0, false
	}
	return Pدرگاهخواندنbyte(dataدرگاه_2), true
}

func sendموشیفرمان(مقدار uint8) bool {
	if !نوشتنps2فرمان(0xD4) || !نوشتنps2data(مقدار) {
		return false
	}
	ack, تأیید := خواندنps2data()
	return تأیید && ack == 0xFA
}

func (خود *Tموشیdriver) Initdriver(manager *TInterruptmanager, موشیeventhandler Iموشیeventhandler) {

	iموشیeventhandler = TDefaultموشیeventhandler{}

	if موشیeventhandler != nil {
		iموشیeventhandler = موشیeventhandler
	}

	فعالموشیdriver = خود
	interrupthandler = handleموشیinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	خود.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Pدرگاهخواندنbyte(فرماندرگاه_2)&0x01) != 0; i++ {
		Pدرگاهخواندنbyte(dataدرگاه_2)
	}

	if !نوشتنps2فرمان(0xA8) || !نوشتنps2فرمان(0x20) {
		return
	}
	وضعیت, تأیید := خواندنps2data()
	if !تأیید {
		return
	}
	وضعیت |= 0x02
	وضعیت &^= 0x20
	if !نوشتنps2فرمان(0x60) || !نوشتنps2data(وضعیت) {
		return
	}

	if !sendموشیفرمان(0xF6) || !sendموشیفرمان(0xF4) {
		return
	}
	offset = 0

}

func handleموشیinterrupt(esp uint32) uint32 {
	if فعالموشیdriver == nil {
		Pدرگاهخواندنbyte(dataدرگاه_2)
		return esp
	}
	return فعالموشیdriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var دکمه_2 int8
var pendingx int16
var pendingy int16
var pendingدکمه int8
var pendingموشیevent bool

func (خود *Tموشیdriver) Handleinterrupt(esp uint32) uint32 {
	وضعیت := Pدرگاهخواندنbyte(فرماندرگاه_2)
	if (وضعیت&0x01) == 0 || (وضعیت&0x20) == 0 {
		return esp
	}

	data := Pدرگاهخواندنbyte(dataدرگاه_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetوضعیت := uint8(buffer_2[0])

		if (packetوضعیت & 0xC0) == 0 {
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
		pendingدکمه = int8(packetوضعیت & 0x07)
		pendingموشیevent = true
	}

	return esp

}

func Processpendingموشیevents() {
	if iموشیeventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingموشیevent {
		Interruptفعال()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	جدیددکمه := pendingدکمه
	oldدکمه := دکمه_2

	pendingx = 0
	pendingy = 0
	pendingموشیevent = false
	Interruptفعال()

	if x != 0 || y != 0 {
		iموشیeventhandler.Oروشنموشیانتقال(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		نقاب := int8(0x1 << i)
		if (جدیددکمه & نقاب) != (oldدکمه & نقاب) {
			if (جدیددکمه & نقاب) != 0 {
				iموشیeventhandler.Oروشنموشیپایین(int8(i + 1))
			} else {
				iموشیeventhandler.Oروشنموشیبالا(int8(i + 1))
			}
		}
	}
	دکمه_2 = جدیددکمه
}
