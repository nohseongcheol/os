package papanketik

import . "unsafe"

import . "port"
import . "interupsi"
import . "console"

type ITetikusEvenhandler interface {
	HidupTetikusBawah(tombol int8)
	HidupTetikusNaik(tombol int8)
	HidupTetikusPindah(x int8, y int8)
}

var iTetikusEvenhandler ITetikusEvenhandler

type TBakuTetikusEvenhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPosisi int16 = 0
var yPosisi int16 = 0

func (dirisendiri TBakuTetikusEvenhandler) HidupTetikusBawah(tombol int8) {
	buffer := []byte("+")
	console_2.MCetakxy(buffer, uint16(previousx), uint16(previousy))
}
func (dirisendiri TBakuTetikusEvenhandler) HidupTetikusNaik(tombol int8)	{}
func (dirisendiri TBakuTetikusEvenhandler) HidupTetikusPindah(x int8, y int8) {

	xPosisi += int16(x)
	if xPosisi < 0 {
		xPosisi = 0
	}
	if xPosisi >= 80 {
		xPosisi = 79
	}

	yPosisi -= int16(y)

	if yPosisi < 0 {
		yPosisi = 0
	}
	if yPosisi >= 25 {
		yPosisi = 24
	}

	buffer := []byte(" ")
	console_2.MCetakxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MCetakxy(buffer, uint16(xPosisi), uint16(yPosisi))

	previousx = xPosisi
	previousy = yPosisi
}

type TTetikusdriver struct {
	TInterupsihandler
}

var aktifTetikusdriver *TTetikusdriver
var interupsihandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var perintahport_2 uint16 = 0x64

const ps2TungguBatas = 100000

func tunggups2MasukanKosong() bool {
	for i := 0; i < ps2TungguBatas; i++ {
		if (PortBacabyte(perintahport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func tunggups2KeluaranPenuh() bool {
	for i := 0; i < ps2TungguBatas; i++ {
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
	if !tunggups2KeluaranPenuh() {
		return 0, false
	}
	return PortBacabyte(dataport_2), true
}

func kirimTetikusPerintah(nilai uint8) bool {
	if !tulisps2Perintah(0xD4) || !tulisps2data(nilai) {
		return false
	}
	ack, oke := bacaps2data()
	return oke && ack == 0xFA
}

func (dirisendiri *TTetikusdriver) Initdriver(manager *TInterupsimanager, tetikusEvenhandler ITetikusEvenhandler) {

	iTetikusEvenhandler = TBakuTetikusEvenhandler{}

	if tetikusEvenhandler != nil {
		iTetikusEvenhandler = tetikusEvenhandler
	}

	aktifTetikusdriver = dirisendiri
	interupsihandler = penangananTetikusInterupsi
	var address uintptr
	address = uintptr(Pointer(&interupsihandler))
	dirisendiri.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortBacabyte(perintahport_2)&0x01) != 0; i++ {
		PortBacabyte(dataport_2)
	}

	if !tulisps2Perintah(0xA8) || !tulisps2Perintah(0x20) {
		return
	}
	status, oke := bacaps2data()
	if !oke {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !tulisps2Perintah(0x60) || !tulisps2data(status) {
		return
	}

	if !kirimTetikusPerintah(0xF6) || !kirimTetikusPerintah(0xF4) {
		return
	}
	offset = 0

}

func penangananTetikusInterupsi(esp uint32) uint32 {
	if aktifTetikusdriver == nil {
		PortBacabyte(dataport_2)
		return esp
	}
	return aktifTetikusdriver.PenangananInterupsi(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var tombol_2 int8
var pendingx int16
var pendingy int16
var pendingTombol int8
var pendingTetikusEven bool

func (dirisendiri *TTetikusdriver) PenangananInterupsi(esp uint32) uint32 {
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
		pendingTombol = int8(packetstatus & 0x07)
		pendingTetikusEven = true
	}

	return esp

}

func ProsespendingTetikusKejadian() {
	if iTetikusEvenhandler == nil {
		return
	}

	Interupsideactive()
	if !pendingTetikusEven {
		InterupsiAktif()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	baruTombol := pendingTombol
	oldTombol := tombol_2

	pendingx = 0
	pendingy = 0
	pendingTetikusEven = false
	InterupsiAktif()

	if x != 0 || y != 0 {
		iTetikusEvenhandler.HidupTetikusPindah(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		topeng := int8(0x1 << i)
		if (baruTombol & topeng) != (oldTombol & topeng) {
			if (baruTombol & topeng) != 0 {
				iTetikusEvenhandler.HidupTetikusBawah(int8(i + 1))
			} else {
				iTetikusEvenhandler.HidupTetikusNaik(int8(i + 1))
			}
		}
	}
	tombol_2 = baruTombol
}
