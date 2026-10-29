/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package papanketik

import . "unsafe"

import . "port"
import . "interupsi"

import . "console"
import . "sistemcall"

type IPapanketikEvenhandler interface {
	HidupKunciBawah(kunci byte)
	HidupKunciNaik(kunci byte)
}

var iPapanketikEvenhandler IPapanketikEvenhandler
var bakuPapanketikEvenhandler TBakuPapanketikEvenhandler

type TBakuPapanketikEvenhandler struct {
}

func (dirisendiri *TBakuPapanketikEvenhandler) HidupKunciBawah(kunci byte) {
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = heksa[((kunci >> 4) & 0xF)]
	buffer[18] = heksa[kunci&0xF]

	console_2 := TConsole{}
	console_2.MCetak(buffer)

}
func (dirisendiri *TBakuPapanketikEvenhandler) HidupKunciNaik(kunci byte) {
}

type TPapanketikdriver struct {
	TInterupsihandler
}

var aktifPapanketikdriver *TPapanketikdriver
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

func (dirisendiri *TPapanketikdriver) Initdriver(manager *TInterupsimanager, papanketikEvenhandler IPapanketikEvenhandler) {

	iPapanketikEvenhandler = &bakuPapanketikEvenhandler
	if papanketikEvenhandler != nil {
		iPapanketikEvenhandler = papanketikEvenhandler
	}

	aktifPapanketikdriver = dirisendiri
	interupsihandler = penangananPapanketikInterupsi
	var address uintptr
	address = uintptr(Pointer(&interupsihandler))

	dirisendiri.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortBacabyte(perintahport_2)&0x01) != 0; i++ {
		PortBacabyte(dataport_2)
	}

	if !tulisps2Perintah(0xAE) || !tulisps2Perintah(0x20) {
		return
	}
	status, oke := bacaps2data()
	if !oke {
		return
	}
	status |= 0x01
	status &^= 0x10
	if !tulisps2Perintah(0x60) || !tulisps2data(status) {
		return
	}

	if !tulisps2data(0xF4) {
		return
	}
	ack, oke := bacaps2data()
	if !oke || ack != 0xFA {
		return
	}

}

func penangananPapanketikInterupsi(esp uint32) uint32 {
	if aktifPapanketikdriver == nil {
		PortBacabyte(dataport_2)
		return esp
	}
	return aktifPapanketikdriver.PenangananInterupsi(esp)
}

const papanketikqueueUkuran = 64

var papanketikqueue [papanketikqueueUkuran]byte
var papanketikqueueBaca uint8
var papanketikqueueTulis uint8
var kirishift bool
var kananshift bool
var extendedPindaicode bool

func queuePapanketikbyte(kunci byte) {
	berikutnya := (papanketikqueueTulis + 1) % papanketikqueueUkuran
	if berikutnya == papanketikqueueBaca {
		return
	}
	papanketikqueue[papanketikqueueTulis] = kunci
	papanketikqueueTulis = berikutnya
}

func ProsespendingPapanketikKejadian() {
	for papanketikqueueBaca != papanketikqueueTulis {
		kunci := papanketikqueue[papanketikqueueBaca]
		papanketikqueueBaca = (papanketikqueueBaca + 1) % papanketikqueueUkuran
		Stdinputbyte(kunci)
		if iPapanketikEvenhandler != nil {
			iPapanketikEvenhandler.HidupKunciBawah(kunci)
		}
	}
}

func pindaicodetobyte(pindaicode uint8) (byte, bool) {
	shift := kirishift || kananshift

	if pindaicode >= 0x02 && pindaicode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[pindaicode-0x02], true
		}
		return "1234567890"[pindaicode-0x02], true
	}
	if pindaicode >= 0x10 && pindaicode <= 0x19 {
		kunci := "qwertyuiop"[pindaicode-0x10]
		if shift {
			kunci -= 'a' - 'A'
		}
		return kunci, true
	}
	if pindaicode >= 0x1E && pindaicode <= 0x26 {
		kunci := "asdfghjkl"[pindaicode-0x1E]
		if shift {
			kunci -= 'a' - 'A'
		}
		return kunci, true
	}
	if pindaicode >= 0x2C && pindaicode <= 0x32 {
		kunci := "zxcvbnm"[pindaicode-0x2C]
		if shift {
			kunci -= 'a' - 'A'
		}
		return kunci, true
	}

	switch pindaicode {
	case 0x0C:
		if shift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (dirisendiri *TPapanketikdriver) PenangananInterupsi(esp uint32) uint32 {
	status := PortBacabyte(perintahport_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	pindaicode := PortBacabyte(dataport_2)
	if pindaicode == 0xE0 {
		extendedPindaicode = true
		return esp
	}
	if extendedPindaicode {
		extendedPindaicode = false
		return esp
	}

	released := (pindaicode & 0x80) != 0
	basecode := pindaicode & 0x7F
	if basecode == 0x2A {
		kirishift = !released
		return esp
	}
	if basecode == 0x36 {
		kananshift = !released
		return esp
	}
	if released {
		return esp
	}

	if kunci, oke := pindaicodetobyte(basecode); oke {
		queuePapanketikbyte(kunci)
	}

	return esp
}
