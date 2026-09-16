/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package clavier

import . "unsafe"

import . "port"
import . "interruption"

import . "console"
import . "systèmeappel"

type IClavierévénementhandler interface {
	SurCléVerslebas(clé byte)
	SurCléHaut(clé byte)
}

var iclavierévénementhandler IClavierévénementhandler
var pardéfautclavierévénementhandler TPardéfautclavierévénementhandler

type TPardéfautclavierévénementhandler struct {
}

func (self *TPardéfautclavierévénementhandler) SurCléVerslebas(clé byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((clé >> 4) & 0xF)]
	buffer[18] = hex[clé&0xF]

	console_2 := TConsole{}
	console_2.MImprimer(buffer)

}
func (self *TPardéfautclavierévénementhandler) SurCléHaut(clé byte) {
}

type TClavierpilote struct {
	TInterruptionhandler
}

var actifclavierpilote *TClavierpilote
var interruptionhandler func(uint32) uint32

var donnéesport_2 uint16 = 0x60
var commandeport_2 uint16 = 0x64

const ps2AttendreLimite = 100000

func attendreps2EntréeVide() bool {
	for i := 0; i < ps2AttendreLimite; i++ {
		if (Portlireoctet(commandeport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func attendreps2SortieImportant() bool {
	for i := 0; i < ps2AttendreLimite; i++ {
		if (Portlireoctet(commandeport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func écrireps2Commande(valeur uint8) bool {
	if !attendreps2EntréeVide() {
		return false
	}
	Portécrireoctet(commandeport_2, valeur)
	return true
}

func écrireps2données(valeur uint8) bool {
	if !attendreps2EntréeVide() {
		return false
	}
	Portécrireoctet(donnéesport_2, valeur)
	return true
}

func lireps2données() (uint8, bool) {
	if !attendreps2SortieImportant() {
		return 0, false
	}
	return Portlireoctet(donnéesport_2), true
}

func (self *TClavierpilote) Initpilote(gestionnaire *TInterruptiongestionnaire, clavierévénementhandler IClavierévénementhandler) {

	iclavierévénementhandler = &pardéfautclavierévénementhandler
	if clavierévénementhandler != nil {
		iclavierévénementhandler = clavierévénementhandler
	}

	actifclavierpilote = self
	interruptionhandler = poignéeclavierinterruption
	var address uintptr
	address = uintptr(Pointer(&interruptionhandler))

	self.Init(0x21, uintptr(Pointer(gestionnaire)), address)

	for i := 0; i < 32 && (Portlireoctet(commandeport_2)&0x01) != 0; i++ {
		Portlireoctet(donnéesport_2)
	}

	if !écrireps2Commande(0xAE) || !écrireps2Commande(0x20) {
		return
	}
	état, valider := lireps2données()
	if !valider {
		return
	}
	état |= 0x01
	état &^= 0x10
	if !écrireps2Commande(0x60) || !écrireps2données(état) {
		return
	}

	if !écrireps2données(0xF4) {
		return
	}
	ack, valider := lireps2données()
	if !valider || ack != 0xFA {
		return
	}

}

func poignéeclavierinterruption(esp uint32) uint32 {
	if actifclavierpilote == nil {
		Portlireoctet(donnéesport_2)
		return esp
	}
	return actifclavierpilote.Poignéeinterruption(esp)
}

const clavierfileAttenteTaille = 64

var clavierfileAttente [clavierfileAttenteTaille]byte
var clavierfileAttentelire uint8
var clavierfileAttenteécrire uint8
var gaucheMaj bool
var droiteMaj bool
var extendedAnalysercode bool

func fileAttenteclavieroctet(clé byte) {
	suivant := (clavierfileAttenteécrire + 1) % clavierfileAttenteTaille
	if suivant == clavierfileAttentelire {
		return
	}
	clavierfileAttente[clavierfileAttenteécrire] = clé
	clavierfileAttenteécrire = suivant
}

func Processusattenteclavierévénements() {
	for clavierfileAttentelire != clavierfileAttenteécrire {
		clé := clavierfileAttente[clavierfileAttentelire]
		clavierfileAttentelire = (clavierfileAttentelire + 1) % clavierfileAttenteTaille
		Stdinputoctet(clé)
		if iclavierévénementhandler != nil {
			iclavierévénementhandler.SurCléVerslebas(clé)
		}
	}
}

func analysercodetooctet(analysercode uint8) (byte, bool) {
	maj := gaucheMaj || droiteMaj

	if analysercode >= 0x02 && analysercode <= 0x0B {
		if maj {
			return "!@#$%^&*()"[analysercode-0x02], true
		}
		return "1234567890"[analysercode-0x02], true
	}
	if analysercode >= 0x10 && analysercode <= 0x19 {
		clé := "qwertyuiop"[analysercode-0x10]
		if maj {
			clé -= 'a' - 'A'
		}
		return clé, true
	}
	if analysercode >= 0x1E && analysercode <= 0x26 {
		clé := "asdfghjkl"[analysercode-0x1E]
		if maj {
			clé -= 'a' - 'A'
		}
		return clé, true
	}
	if analysercode >= 0x2C && analysercode <= 0x32 {
		clé := "zxcvbnm"[analysercode-0x2C]
		if maj {
			clé -= 'a' - 'A'
		}
		return clé, true
	}

	switch analysercode {
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

func (self *TClavierpilote) Poignéeinterruption(esp uint32) uint32 {
	état := Portlireoctet(commandeport_2)
	if (état&0x01) == 0 || (état&0x20) != 0 {
		return esp
	}

	analysercode := Portlireoctet(donnéesport_2)
	if analysercode == 0xE0 {
		extendedAnalysercode = true
		return esp
	}
	if extendedAnalysercode {
		extendedAnalysercode = false
		return esp
	}

	released := (analysercode & 0x80) != 0
	basecode := analysercode & 0x7F
	if basecode == 0x2A {
		gaucheMaj = !released
		return esp
	}
	if basecode == 0x36 {
		droiteMaj = !released
		return esp
	}
	if released {
		return esp
	}

	if clé, valider := analysercodetooctet(basecode); valider {
		fileAttenteclavieroctet(clé)
	}

	return esp
}
