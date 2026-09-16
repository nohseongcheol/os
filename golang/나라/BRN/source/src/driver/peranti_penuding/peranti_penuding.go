/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package papankekunci

import . "unsafe"

import . "port"
import . "sampuk"
import . "console"

type ITetikusPeristiwahandler interface {
	BukaTetikusTurun(butang int8)
	BukaTetikusNaik(butang int8)
	BukaTetikusAlih(x int8, y int8)
}

var iTetikusPeristiwahandler ITetikusPeristiwahandler

type TLalaiTetikusPeristiwahandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xKedudukan int16 = 0
var yKedudukan int16 = 0

func (diri TLalaiTetikusPeristiwahandler) BukaTetikusTurun(butang int8) {
	buffer := []byte("+")
	console_2.MCetakxy(buffer, uint16(previousx), uint16(previousy))
}
func (diri TLalaiTetikusPeristiwahandler) BukaTetikusNaik(butang int8)	{}
func (diri TLalaiTetikusPeristiwahandler) BukaTetikusAlih(x int8, y int8) {

	xKedudukan += int16(x)
	if xKedudukan < 0 {
		xKedudukan = 0
	}
	if xKedudukan >= 80 {
		xKedudukan = 79
	}

	yKedudukan -= int16(y)

	if yKedudukan < 0 {
		yKedudukan = 0
	}
	if yKedudukan >= 25 {
		yKedudukan = 24
	}

	buffer := []byte(" ")
	console_2.MCetakxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MCetakxy(buffer, uint16(xKedudukan), uint16(yKedudukan))

	previousx = xKedudukan
	previousy = yKedudukan
}

type TTetikusdriver struct {
	TSampukhandler
}

var aktifTetikusdriver *TTetikusdriver
var sampukhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var perintahport_2 uint16 = 0x64

const ps2TungguHad = 100000

func tunggups2MasukanKosong() bool {
	for i := 0; i < ps2TungguHad; i++ {
		if (PortBacabyte(perintahport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func tunggups2outputPenuh() bool {
	for i := 0; i < ps2TungguHad; i++ {
		if (PortBacabyte(perintahport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func tulisps2Perintah(nilai uint8) bool {
	if !tunggups2MasukanKosong() {
		return false
	}
	PortTulisbyte(perintahport_2, nilai)
	return true
}

func tulisps2data(nilai uint8) bool {
	if !tunggups2MasukanKosong() {
		return false
	}
	PortTulisbyte(dataport_2, nilai)
	return true
}

func bacaps2data() (uint8, bool) {
	if !tunggups2outputPenuh() {
		return 0, false
	}
	return PortBacabyte(dataport_2), true
}

func hantarTetikusPerintah(nilai uint8) bool {
	if !tulisps2Perintah(0xD4) || !tulisps2data(nilai) {
		return false
	}
	ack, ok := bacaps2data()
	return ok && ack == 0xFA
}

func (diri *TTetikusdriver) Initdriver(manager *TSampukmanager, tetikusPeristiwahandler ITetikusPeristiwahandler) {

	iTetikusPeristiwahandler = TLalaiTetikusPeristiwahandler{}

	if tetikusPeristiwahandler != nil {
		iTetikusPeristiwahandler = tetikusPeristiwahandler
	}

	aktifTetikusdriver = diri
	sampukhandler = kendaliTetikusSampuk
	var address uintptr
	address = uintptr(Pointer(&sampukhandler))
	diri.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortBacabyte(perintahport_2)&0x01) != 0; i++ {
		PortBacabyte(dataport_2)
	}

	if !tulisps2Perintah(0xA8) || !tulisps2Perintah(0x20) {
		return
	}
	status, ok := bacaps2data()
	if !ok {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !tulisps2Perintah(0x60) || !tulisps2data(status) {
		return
	}

	if !hantarTetikusPerintah(0xF6) || !hantarTetikusPerintah(0xF4) {
		return
	}
	offset = 0

}

func kendaliTetikusSampuk(esp uint32) uint32 {
	if aktifTetikusdriver == nil {
		PortBacabyte(dataport_2)
		return esp
	}
	return aktifTetikusdriver.KendaliSampuk(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var butang_2 int8
var pendingx int16
var pendingy int16
var pendingButang int8
var pendingTetikusPeristiwa bool

func (diri *TTetikusdriver) KendaliSampuk(esp uint32) uint32 {
	status := PortBacabyte(perintahport_2)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	data := PortBacabyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
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
		pendingButang = int8(packetstatus & 0x07)
		pendingTetikusPeristiwa = true
	}

	return esp

}

func ProsespendingTetikusevents() {
	if iTetikusPeristiwahandler == nil {
		return
	}

	Sampukdeactive()
	if !pendingTetikusPeristiwa {
		SampukAktif()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	baharuButang := pendingButang
	oldButang := butang_2

	pendingx = 0
	pendingy = 0
	pendingTetikusPeristiwa = false
	SampukAktif()

	if x != 0 || y != 0 {
		iTetikusPeristiwahandler.BukaTetikusAlih(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (baharuButang & mask) != (oldButang & mask) {
			if (baharuButang & mask) != 0 {
				iTetikusPeristiwahandler.BukaTetikusTurun(int8(i + 1))
			} else {
				iTetikusPeristiwahandler.BukaTetikusNaik(int8(i + 1))
			}
		}
	}
	butang_2 = baharuButang
}
