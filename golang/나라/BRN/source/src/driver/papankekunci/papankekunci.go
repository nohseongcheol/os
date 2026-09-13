package papankekunci

import . "unsafe"

import . "port"
import . "sampuk"

import . "console"
import . "sistemcall"

type IPapankekunciPeristiwahandler interface {
	BukaKunciTurun(kunci byte)
	BukaKunciNaik(kunci byte)
}

var iPapankekunciPeristiwahandler IPapankekunciPeristiwahandler
var lalaiPapankekunciPeristiwahandler TLalaiPapankekunciPeristiwahandler

type TLalaiPapankekunciPeristiwahandler struct {
}

func (diri *TLalaiPapankekunciPeristiwahandler) BukaKunciTurun(kunci byte) {
	heks := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = heks[((kunci >> 4) & 0xF)]
	buffer[18] = heks[kunci&0xF]

	console_2 := TConsole{}
	console_2.MCetak(buffer)

}
func (diri *TLalaiPapankekunciPeristiwahandler) BukaKunciNaik(kunci byte) {
}

type TPapankekuncidriver struct {
	TSampukhandler
}

var aktifPapankekuncidriver *TPapankekuncidriver
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

func (diri *TPapankekuncidriver) Initdriver(manager *TSampukmanager, papankekunciPeristiwahandler IPapankekunciPeristiwahandler) {

	iPapankekunciPeristiwahandler = &lalaiPapankekunciPeristiwahandler
	if papankekunciPeristiwahandler != nil {
		iPapankekunciPeristiwahandler = papankekunciPeristiwahandler
	}

	aktifPapankekuncidriver = diri
	sampukhandler = kendaliPapankekunciSampuk
	var address uintptr
	address = uintptr(Pointer(&sampukhandler))

	diri.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortBacabyte(perintahport_2)&0x01) != 0; i++ {
		PortBacabyte(dataport_2)
	}

	if !tulisps2Perintah(0xAE) || !tulisps2Perintah(0x20) {
		return
	}
	status, ok := bacaps2data()
	if !ok {
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
	ack, ok := bacaps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func kendaliPapankekunciSampuk(esp uint32) uint32 {
	if aktifPapankekuncidriver == nil {
		PortBacabyte(dataport_2)
		return esp
	}
	return aktifPapankekuncidriver.KendaliSampuk(esp)
}

const papankekunciqueueSaiz = 64

var papankekunciqueue [papankekunciqueueSaiz]byte
var papankekunciqueueBaca uint8
var papankekunciqueueTulis uint8
var kiriShif bool
var kananShif bool
var extendedImbascode bool

func queuePapankekuncibyte(kunci byte) {
	berikutnya := (papankekunciqueueTulis + 1) % papankekunciqueueSaiz
	if berikutnya == papankekunciqueueBaca {
		return
	}
	papankekunciqueue[papankekunciqueueTulis] = kunci
	papankekunciqueueTulis = berikutnya
}

func ProsespendingPapankekuncievents() {
	for papankekunciqueueBaca != papankekunciqueueTulis {
		kunci := papankekunciqueue[papankekunciqueueBaca]
		papankekunciqueueBaca = (papankekunciqueueBaca + 1) % papankekunciqueueSaiz
		Stdinputbyte(kunci)
		if iPapankekunciPeristiwahandler != nil {
			iPapankekunciPeristiwahandler.BukaKunciTurun(kunci)
		}
	}
}

func imbascodetobyte(imbascode uint8) (byte, bool) {
	shif := kiriShif || kananShif

	if imbascode >= 0x02 && imbascode <= 0x0B {
		if shif {
			return "!@#$%^&*()"[imbascode-0x02], true
		}
		return "1234567890"[imbascode-0x02], true
	}
	if imbascode >= 0x10 && imbascode <= 0x19 {
		kunci := "qwertyuiop"[imbascode-0x10]
		if shif {
			kunci -= 'a' - 'A'
		}
		return kunci, true
	}
	if imbascode >= 0x1E && imbascode <= 0x26 {
		kunci := "asdfghjkl"[imbascode-0x1E]
		if shif {
			kunci -= 'a' - 'A'
		}
		return kunci, true
	}
	if imbascode >= 0x2C && imbascode <= 0x32 {
		kunci := "zxcvbnm"[imbascode-0x2C]
		if shif {
			kunci -= 'a' - 'A'
		}
		return kunci, true
	}

	switch imbascode {
	case 0x0C:
		if shif {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shif {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shif {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shif {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shif {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shif {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shif {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shif {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shif {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shif {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shif {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (diri *TPapankekuncidriver) KendaliSampuk(esp uint32) uint32 {
	status := PortBacabyte(perintahport_2)
	if (status&0x01) == 0 || (status&0x20) != 0 {
		return esp
	}

	imbascode := PortBacabyte(dataport_2)
	if imbascode == 0xE0 {
		extendedImbascode = true
		return esp
	}
	if extendedImbascode {
		extendedImbascode = false
		return esp
	}

	released := (imbascode & 0x80) != 0
	basecode := imbascode & 0x7F
	if basecode == 0x2A {
		kiriShif = !released
		return esp
	}
	if basecode == 0x36 {
		kananShif = !released
		return esp
	}
	if released {
		return esp
	}

	if kunci, ok := imbascodetobyte(basecode); ok {
		queuePapankekuncibyte(kunci)
	}

	return esp
}
