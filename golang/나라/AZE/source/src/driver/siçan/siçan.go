/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package klaviatura

import . "unsafe"

import . "qapı"
import . "interrupt"
import . "console"

type ISiçaneventhandler interface {
	OnSiçandown(button int8)
	OnSiçanYuxarı(button int8)
	OnSiçanDaşı(x int8, y int8)
}

var iSiçaneventhandler ISiçaneventhandler

type TÖnQurğuluSiçaneventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self TÖnQurğuluSiçaneventhandler) OnSiçandown(button int8) {
	buffer := []byte("+")
	console_2.MÇapEtxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TÖnQurğuluSiçaneventhandler) OnSiçanYuxarı(button int8)	{}
func (self TÖnQurğuluSiçaneventhandler) OnSiçanDaşı(x int8, y int8) {

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
	console_2.MÇapEtxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MÇapEtxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type TSiçandriver struct {
	TInterrupthandler
}

var fəalSiçandriver *TSiçandriver
var interrupthandler func(uint32) uint32

var dataQapı_2 uint16 = 0x60
var əmrQapı_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (QapıOxumabyte(əmrQapı_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputTam() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (QapıOxumabyte(əmrQapı_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func yazmaps2Əmr(qiymət uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	QapıYazmabyte(əmrQapı_2, qiymət)
	return true
}

func yazmaps2data(qiymət uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	QapıYazmabyte(dataQapı_2, qiymət)
	return true
}

func oxumaps2data() (uint8, bool) {
	if !waitps2outputTam() {
		return 0, false
	}
	return QapıOxumabyte(dataQapı_2), true
}

func sendSiçanƏmr(qiymət uint8) bool {
	if !yazmaps2Əmr(0xD4) || !yazmaps2data(qiymət) {
		return false
	}
	ack, oldu := oxumaps2data()
	return oldu && ack == 0xFA
}

func (self *TSiçandriver) Initdriver(manager *TInterruptmanager, siçaneventhandler ISiçaneventhandler) {

	iSiçaneventhandler = TÖnQurğuluSiçaneventhandler{}

	if siçaneventhandler != nil {
		iSiçaneventhandler = siçaneventhandler
	}

	fəalSiçandriver = self
	interrupthandler = handleSiçaninterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (QapıOxumabyte(əmrQapı_2)&0x01) != 0; i++ {
		QapıOxumabyte(dataQapı_2)
	}

	if !yazmaps2Əmr(0xA8) || !yazmaps2Əmr(0x20) {
		return
	}
	vəziyyət, oldu := oxumaps2data()
	if !oldu {
		return
	}
	vəziyyət |= 0x02
	vəziyyət &^= 0x20
	if !yazmaps2Əmr(0x60) || !yazmaps2data(vəziyyət) {
		return
	}

	if !sendSiçanƏmr(0xF6) || !sendSiçanƏmr(0xF4) {
		return
	}
	offset = 0

}

func handleSiçaninterrupt(esp uint32) uint32 {
	if fəalSiçandriver == nil {
		QapıOxumabyte(dataQapı_2)
		return esp
	}
	return fəalSiçandriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingSiçanevent bool

func (self *TSiçandriver) Handleinterrupt(esp uint32) uint32 {
	vəziyyət := QapıOxumabyte(əmrQapı_2)
	if (vəziyyət&0x01) == 0 || (vəziyyət&0x20) == 0 {
		return esp
	}

	data := QapıOxumabyte(dataQapı_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetVəziyyət := uint8(buffer_2[0])

		if (packetVəziyyət & 0xC0) == 0 {
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
		pendingbutton = int8(packetVəziyyət & 0x07)
		pendingSiçanevent = true
	}

	return esp

}

func ProcesspendingSiçanevents() {
	if iSiçaneventhandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingSiçanevent {
		InterruptFəal()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	yenibutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingSiçanevent = false
	InterruptFəal()

	if x != 0 || y != 0 {
		iSiçaneventhandler.OnSiçanDaşı(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (yenibutton & mask) != (oldbutton & mask) {
			if (yenibutton & mask) != 0 {
				iSiçaneventhandler.OnSiçandown(int8(i + 1))
			} else {
				iSiçaneventhandler.OnSiçanYuxarı(int8(i + 1))
			}
		}
	}
	button_2 = yenibutton
}
