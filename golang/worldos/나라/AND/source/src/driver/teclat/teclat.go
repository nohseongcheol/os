/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package teclat

import . "unsafe"

import . "port"
import . "interrupció"

import . "consola"
import . "sistemacall"

type ITeclatEsdevenimenthandler interface {
	EngegatClauAvall(clau byte)
	EngegatClauAmunt(clau byte)
}

var iTeclatEsdevenimenthandler ITeclatEsdevenimenthandler
var perdefecteTeclatEsdevenimenthandler TPerdefecteTeclatEsdevenimenthandler

type TPerdefecteTeclatEsdevenimenthandler struct {
}

func (unmateix *TPerdefecteTeclatEsdevenimenthandler) EngegatClauAvall(clau byte) {
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hexadecimal[((clau >> 4) & 0xF)]
	buffer[18] = hexadecimal[clau&0xF]

	consola_2 := TConsola{}
	consola_2.MImprimeix(buffer)

}
func (unmateix *TPerdefecteTeclatEsdevenimenthandler) EngegatClauAmunt(clau byte) {
}

type TTeclatdriver struct {
	TInterrupcióhandler
}

var actiuTeclatdriver *TTeclatdriver
var interrupcióhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var ordreport_2 uint16 = 0x64

const ps2EsperaLímit = 100000

func esperaps2EntradaBuit() bool {
	for i := 0; i < ps2EsperaLímit; i++ {
		if (PortLecturabyte(ordreport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func esperaps2SortidaComplet() bool {
	for i := 0; i < ps2EsperaLímit; i++ {
		if (PortLecturabyte(ordreport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func escripturaps2Ordre(valor uint8) bool {
	if !esperaps2EntradaBuit() {
		return false
	}
	PortEscripturabyte(ordreport_2, valor)
	return true
}

func escripturaps2data(valor uint8) bool {
	if !esperaps2EntradaBuit() {
		return false
	}
	PortEscripturabyte(dataport_2, valor)
	return true
}

func lecturaps2data() (uint8, bool) {
	if !esperaps2SortidaComplet() {
		return 0, false
	}
	return PortLecturabyte(dataport_2), true
}

func (unmateix *TTeclatdriver) Initdriver(manager *TInterrupciómanager, teclatEsdevenimenthandler ITeclatEsdevenimenthandler) {

	iTeclatEsdevenimenthandler = &perdefecteTeclatEsdevenimenthandler
	if teclatEsdevenimenthandler != nil {
		iTeclatEsdevenimenthandler = teclatEsdevenimenthandler
	}

	actiuTeclatdriver = unmateix
	interrupcióhandler = gestorTeclatInterrupció
	var adreça uintptr
	adreça = uintptr(Pointer(&interrupcióhandler))

	unmateix.Init(0x21, uintptr(Pointer(manager)), adreça)

	for i := 0; i < 32 && (PortLecturabyte(ordreport_2)&0x01) != 0; i++ {
		PortLecturabyte(dataport_2)
	}

	if !escripturaps2Ordre(0xAE) || !escripturaps2Ordre(0x20) {
		return
	}
	estat, dacord := lecturaps2data()
	if !dacord {
		return
	}
	estat |= 0x01
	estat &^= 0x10
	if !escripturaps2Ordre(0x60) || !escripturaps2data(estat) {
		return
	}

	if !escripturaps2data(0xF4) {
		return
	}
	ack, dacord := lecturaps2data()
	if !dacord || ack != 0xFA {
		return
	}

}

func gestorTeclatInterrupció(esp uint32) uint32 {
	if actiuTeclatdriver == nil {
		PortLecturabyte(dataport_2)
		return esp
	}
	return actiuTeclatdriver.GestorInterrupció(esp)
}

const teclatqueueMida = 64

var teclatqueue [teclatqueueMida]byte
var teclatqueueLectura uint8
var teclatqueueEscriptura uint8
var esquerraMaj bool
var dretaMaj bool
var extendedExploracode bool

func queueTeclatbyte(clau byte) {
	següent := (teclatqueueEscriptura + 1) % teclatqueueMida
	if següent == teclatqueueLectura {
		return
	}
	teclatqueue[teclatqueueEscriptura] = clau
	teclatqueueEscriptura = següent
}

func ProcéspendingTeclatEsdeveniments() {
	for teclatqueueLectura != teclatqueueEscriptura {
		clau := teclatqueue[teclatqueueLectura]
		teclatqueueLectura = (teclatqueueLectura + 1) % teclatqueueMida
		Stdinputbyte(clau)
		if iTeclatEsdevenimenthandler != nil {
			iTeclatEsdevenimenthandler.EngegatClauAvall(clau)
		}
	}
}

func exploracodetobyte(exploracode uint8) (byte, bool) {
	maj := esquerraMaj || dretaMaj

	if exploracode >= 0x02 && exploracode <= 0x0B {
		if maj {
			return "!@#$%^&*()"[exploracode-0x02], true
		}
		return "1234567890"[exploracode-0x02], true
	}
	if exploracode >= 0x10 && exploracode <= 0x19 {
		clau := "qwertyuiop"[exploracode-0x10]
		if maj {
			clau -= 'a' - 'A'
		}
		return clau, true
	}
	if exploracode >= 0x1E && exploracode <= 0x26 {
		clau := "asdfghjkl"[exploracode-0x1E]
		if maj {
			clau -= 'a' - 'A'
		}
		return clau, true
	}
	if exploracode >= 0x2C && exploracode <= 0x32 {
		clau := "zxcvbnm"[exploracode-0x2C]
		if maj {
			clau -= 'a' - 'A'
		}
		return clau, true
	}

	switch exploracode {
	case 0x0C:
		if maj {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if maj {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if maj {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if maj {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if maj {
			return ':', true
		}
		return ';', true
	case 0x28:
		if maj {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if maj {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if maj {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if maj {
			return '<', true
		}
		return ',', true
	case 0x34:
		if maj {
			return '>', true
		}
		return '.', true
	case 0x35:
		if maj {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (unmateix *TTeclatdriver) GestorInterrupció(esp uint32) uint32 {
	estat := PortLecturabyte(ordreport_2)
	if (estat&0x01) == 0 || (estat&0x20) != 0 {
		return esp
	}

	exploracode := PortLecturabyte(dataport_2)
	if exploracode == 0xE0 {
		extendedExploracode = true
		return esp
	}
	if extendedExploracode {
		extendedExploracode = false
		return esp
	}

	released := (exploracode & 0x80) != 0
	basecode := exploracode & 0x7F
	if basecode == 0x2A {
		esquerraMaj = !released
		return esp
	}
	if basecode == 0x36 {
		dretaMaj = !released
		return esp
	}
	if released {
		return esp
	}

	if clau, dacord := exploracodetobyte(basecode); dacord {
		queueTeclatbyte(clau)
	}

	return esp
}
