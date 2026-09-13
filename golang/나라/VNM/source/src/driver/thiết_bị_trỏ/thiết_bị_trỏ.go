package bànphím

import . "unsafe"

import . "cổng"
import . "giánđoạn"
import . "console"

type IChuộtSựkiệnhandler interface {
	BậtChuộtdown(nút int8)
	BậtChuộtLên(nút int8)
	BậtChuộtDichuyển(x int8, y int8)
}

var iChuộtSựkiệnhandler IChuộtSựkiệnhandler

type TMặcđịnhChuộtSựkiệnhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xVịtrí int16 = 0
var yVịtrí int16 = 0

func (mình TMặcđịnhChuộtSựkiệnhandler) BậtChuộtdown(nút int8) {
	buffer := []byte("+")
	console_2.MInxy(buffer, uint16(previousx), uint16(previousy))
}
func (mình TMặcđịnhChuộtSựkiệnhandler) BậtChuộtLên(nút int8)	{}
func (mình TMặcđịnhChuộtSựkiệnhandler) BậtChuộtDichuyển(x int8, y int8) {

	xVịtrí += int16(x)
	if xVịtrí < 0 {
		xVịtrí = 0
	}
	if xVịtrí >= 80 {
		xVịtrí = 79
	}

	yVịtrí -= int16(y)

	if yVịtrí < 0 {
		yVịtrí = 0
	}
	if yVịtrí >= 25 {
		yVịtrí = 24
	}

	buffer := []byte(" ")
	console_2.MInxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MInxy(buffer, uint16(xVịtrí), uint16(yVịtrí))

	previousx = xVịtrí
	previousy = yVịtrí
}

type TChuộtdriver struct {
	TGiánđoạnhandler
}

var hoạtđộngChuộtdriver *TChuộtdriver
var giánđoạnhandler func(uint32) uint32

var dataCổng_2 uint16 = 0x60
var lệnhCổng_2 uint16 = 0x64

const ps2ChờGiớihạn = 100000

func chờps2GõRỗng() bool {
	for i := 0; i < ps2ChờGiớihạn; i++ {
		if (CổngĐọcbyte(lệnhCổng_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func chờps2KếtxuấtĐầy() bool {
	for i := 0; i < ps2ChờGiớihạn; i++ {
		if (CổngĐọcbyte(lệnhCổng_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func ghips2Lệnh(giátrị uint8) bool {
	if !chờps2GõRỗng() {
		return false
	}
	CổngGhibyte(lệnhCổng_2, giátrị)
	return true
}

func ghips2data(giátrị uint8) bool {
	if !chờps2GõRỗng() {
		return false
	}
	CổngGhibyte(dataCổng_2, giátrị)
	return true
}

func đọcps2data() (uint8, bool) {
	if !chờps2KếtxuấtĐầy() {
		return 0, false
	}
	return CổngĐọcbyte(dataCổng_2), true
}

func gởiChuộtLệnh(giátrị uint8) bool {
	if !ghips2Lệnh(0xD4) || !ghips2data(giátrị) {
		return false
	}
	ack, đồngý := đọcps2data()
	return đồngý && ack == 0xFA
}

func (mình *TChuộtdriver) Initdriver(manager *TGiánđoạnmanager, chuộtSựkiệnhandler IChuộtSựkiệnhandler) {

	iChuộtSựkiệnhandler = TMặcđịnhChuộtSựkiệnhandler{}

	if chuộtSựkiệnhandler != nil {
		iChuộtSựkiệnhandler = chuộtSựkiệnhandler
	}

	hoạtđộngChuộtdriver = mình
	giánđoạnhandler = handleChuộtGiánđoạn
	var address uintptr
	address = uintptr(Pointer(&giánđoạnhandler))
	mình.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (CổngĐọcbyte(lệnhCổng_2)&0x01) != 0; i++ {
		CổngĐọcbyte(dataCổng_2)
	}

	if !ghips2Lệnh(0xA8) || !ghips2Lệnh(0x20) {
		return
	}
	trạngthái, đồngý := đọcps2data()
	if !đồngý {
		return
	}
	trạngthái |= 0x02
	trạngthái &^= 0x20
	if !ghips2Lệnh(0x60) || !ghips2data(trạngthái) {
		return
	}

	if !gởiChuộtLệnh(0xF6) || !gởiChuộtLệnh(0xF4) {
		return
	}
	offset = 0

}

func handleChuộtGiánđoạn(esp uint32) uint32 {
	if hoạtđộngChuộtdriver == nil {
		CổngĐọcbyte(dataCổng_2)
		return esp
	}
	return hoạtđộngChuộtdriver.HandleGiánđoạn(esp)
}

var sốlượng uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var nút_2 int8
var pendingx int16
var pendingy int16
var pendingNút int8
var pendingChuộtSựkiện bool

func (mình *TChuộtdriver) HandleGiánđoạn(esp uint32) uint32 {
	trạngthái := CổngĐọcbyte(lệnhCổng_2)
	if (trạngthái&0x01) == 0 || (trạngthái&0x20) == 0 {
		return esp
	}

	data := CổngĐọcbyte(dataCổng_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetTrạngthái := uint8(buffer_2[0])

		if (packetTrạngthái & 0xC0) == 0 {
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
		pendingNút = int8(packetTrạngthái & 0x07)
		pendingChuộtSựkiện = true
	}

	return esp

}

func TiếntrìnhpendingChuộtevents() {
	if iChuộtSựkiệnhandler == nil {
		return
	}

	Giánđoạndeactive()
	if !pendingChuộtSựkiện {
		GiánđoạnHoạtđộng()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	mớiNút := pendingNút
	oldNút := nút_2

	pendingx = 0
	pendingy = 0
	pendingChuộtSựkiện = false
	GiánđoạnHoạtđộng()

	if x != 0 || y != 0 {
		iChuộtSựkiệnhandler.BậtChuộtDichuyển(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		lọc := int8(0x1 << i)
		if (mớiNút & lọc) != (oldNút & lọc) {
			if (mớiNút & lọc) != 0 {
				iChuộtSựkiệnhandler.BậtChuộtdown(int8(i + 1))
			} else {
				iChuộtSựkiệnhandler.BậtChuộtLên(int8(i + 1))
			}
		}
	}
	nút_2 = mớiNút
}
