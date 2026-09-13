package näppäimistö

import . "unsafe"

import . "portti"
import . "keskeytys"

import . "konsoli"
import . "järjestelmäcall"

type INäppäimistöTapahtumahandler interface {
	PäälläAvainAlas(avain byte)
	PäälläAvainYlös(avain byte)
}

var iNäppäimistöTapahtumahandler INäppäimistöTapahtumahandler
var oletusNäppäimistöTapahtumahandler TOletusNäppäimistöTapahtumahandler

type TOletusNäppäimistöTapahtumahandler struct {
}

func (itse *TOletusNäppäimistöTapahtumahandler) PäälläAvainAlas(avain byte) {
	heksa := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = heksa[((avain >> 4) & 0xF)]
	buffer[18] = heksa[avain&0xF]

	konsoli_2 := TKonsoli{}
	konsoli_2.MTulosta(buffer)

}
func (itse *TOletusNäppäimistöTapahtumahandler) PäälläAvainYlös(avain byte) {
}

type TNäppäimistödriver struct {
	TKeskeytyshandler
}

var aktiivinenNäppäimistödriver *TNäppäimistödriver
var keskeytyshandler func(uint32) uint32

var dataPortti_2 uint16 = 0x60
var komentoPortti_2 uint16 = 0x64

const ps2OdotaRajoitus = 100000

func odotaps2SyöteTyhjä() bool {
	for i := 0; i < ps2OdotaRajoitus; i++ {
		if (PorttiLukubyte(komentoPortti_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func odotaps2TulosteTäysi() bool {
	for i := 0; i < ps2OdotaRajoitus; i++ {
		if (PorttiLukubyte(komentoPortti_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func kirjoitusps2Komento(arvo uint8) bool {
	if !odotaps2SyöteTyhjä() {
		return false
	}
	PorttiKirjoitusbyte(komentoPortti_2, arvo)
	return true
}

func kirjoitusps2data(arvo uint8) bool {
	if !odotaps2SyöteTyhjä() {
		return false
	}
	PorttiKirjoitusbyte(dataPortti_2, arvo)
	return true
}

func lukups2data() (uint8, bool) {
	if !odotaps2TulosteTäysi() {
		return 0, false
	}
	return PorttiLukubyte(dataPortti_2), true
}

func (itse *TNäppäimistödriver) Initdriver(manager *TKeskeytysmanager, näppäimistöTapahtumahandler INäppäimistöTapahtumahandler) {

	iNäppäimistöTapahtumahandler = &oletusNäppäimistöTapahtumahandler
	if näppäimistöTapahtumahandler != nil {
		iNäppäimistöTapahtumahandler = näppäimistöTapahtumahandler
	}

	aktiivinenNäppäimistödriver = itse
	keskeytyshandler = kahvaNäppäimistöKeskeytys
	var address uintptr
	address = uintptr(Pointer(&keskeytyshandler))

	itse.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PorttiLukubyte(komentoPortti_2)&0x01) != 0; i++ {
		PorttiLukubyte(dataPortti_2)
	}

	if !kirjoitusps2Komento(0xAE) || !kirjoitusps2Komento(0x20) {
		return
	}
	tila, ok := lukups2data()
	if !ok {
		return
	}
	tila |= 0x01
	tila &^= 0x10
	if !kirjoitusps2Komento(0x60) || !kirjoitusps2data(tila) {
		return
	}

	if !kirjoitusps2data(0xF4) {
		return
	}
	ack, ok := lukups2data()
	if !ok || ack != 0xFA {
		return
	}

}

func kahvaNäppäimistöKeskeytys(esp uint32) uint32 {
	if aktiivinenNäppäimistödriver == nil {
		PorttiLukubyte(dataPortti_2)
		return esp
	}
	return aktiivinenNäppäimistödriver.KahvaKeskeytys(esp)
}

const näppäimistöqueueKoko = 64

var näppäimistöqueue [näppäimistöqueueKoko]byte
var näppäimistöqueueLuku uint8
var näppäimistöqueueKirjoitus uint8
var vasemmallaVaihto bool
var oikeallaVaihto bool
var extendedKartoitacode bool

func queueNäppäimistöbyte(avain byte) {
	seuraava := (näppäimistöqueueKirjoitus + 1) % näppäimistöqueueKoko
	if seuraava == näppäimistöqueueLuku {
		return
	}
	näppäimistöqueue[näppäimistöqueueKirjoitus] = avain
	näppäimistöqueueKirjoitus = seuraava
}

func ProsessipendingNäppäimistöTapahtumat() {
	for näppäimistöqueueLuku != näppäimistöqueueKirjoitus {
		avain := näppäimistöqueue[näppäimistöqueueLuku]
		näppäimistöqueueLuku = (näppäimistöqueueLuku + 1) % näppäimistöqueueKoko
		Stdinputbyte(avain)
		if iNäppäimistöTapahtumahandler != nil {
			iNäppäimistöTapahtumahandler.PäälläAvainAlas(avain)
		}
	}
}

func kartoitacodetobyte(kartoitacode uint8) (byte, bool) {
	vaihto := vasemmallaVaihto || oikeallaVaihto

	if kartoitacode >= 0x02 && kartoitacode <= 0x0B {
		if vaihto {
			return "!@#$%^&*()"[kartoitacode-0x02], true
		}
		return "1234567890"[kartoitacode-0x02], true
	}
	if kartoitacode >= 0x10 && kartoitacode <= 0x19 {
		avain := "qwertyuiop"[kartoitacode-0x10]
		if vaihto {
			avain -= 'a' - 'A'
		}
		return avain, true
	}
	if kartoitacode >= 0x1E && kartoitacode <= 0x26 {
		avain := "asdfghjkl"[kartoitacode-0x1E]
		if vaihto {
			avain -= 'a' - 'A'
		}
		return avain, true
	}
	if kartoitacode >= 0x2C && kartoitacode <= 0x32 {
		avain := "zxcvbnm"[kartoitacode-0x2C]
		if vaihto {
			avain -= 'a' - 'A'
		}
		return avain, true
	}

	switch kartoitacode {
	case 0x0C:
		if vaihto {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if vaihto {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if vaihto {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if vaihto {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if vaihto {
			return ':', true
		}
		return ';', true
	case 0x28:
		if vaihto {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if vaihto {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if vaihto {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if vaihto {
			return '<', true
		}
		return ',', true
	case 0x34:
		if vaihto {
			return '>', true
		}
		return '.', true
	case 0x35:
		if vaihto {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (itse *TNäppäimistödriver) KahvaKeskeytys(esp uint32) uint32 {
	tila := PorttiLukubyte(komentoPortti_2)
	if (tila&0x01) == 0 || (tila&0x20) != 0 {
		return esp
	}

	kartoitacode := PorttiLukubyte(dataPortti_2)
	if kartoitacode == 0xE0 {
		extendedKartoitacode = true
		return esp
	}
	if extendedKartoitacode {
		extendedKartoitacode = false
		return esp
	}

	released := (kartoitacode & 0x80) != 0
	basecode := kartoitacode & 0x7F
	if basecode == 0x2A {
		vasemmallaVaihto = !released
		return esp
	}
	if basecode == 0x36 {
		oikeallaVaihto = !released
		return esp
	}
	if released {
		return esp
	}

	if avain, ok := kartoitacodetobyte(basecode); ok {
		queueNäppäimistöbyte(avain)
	}

	return esp
}
