/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package clavier

import . "unsafe"

import . "port"
import . "interruption"
import . "console"

type ISourisévénementhandler interface {
	SursourisVerslebas(bouton int8)
	SursourisHaut(bouton int8)
	SursourisDéplacer(x int8, y int8)
}

var isourisévénementhandler ISourisévénementhandler

type TPardéfautsourisévénementhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self TPardéfautsourisévénementhandler) SursourisVerslebas(bouton int8) {
	buffer := []byte("+")
	console_2.MImprimerxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TPardéfautsourisévénementhandler) SursourisHaut(bouton int8)	{}
func (self TPardéfautsourisévénementhandler) SursourisDéplacer(x int8, y int8) {

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
	console_2.MImprimerxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MImprimerxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type TSourispilote struct {
	TInterruptionhandler
}

var actifsourispilote *TSourispilote
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

func envoyersourisCommande(valeur uint8) bool {
	if !écrireps2Commande(0xD4) || !écrireps2données(valeur) {
		return false
	}
	ack, valider := lireps2données()
	return valider && ack == 0xFA
}

func (self *TSourispilote) Initpilote(gestionnaire *TInterruptiongestionnaire, sourisévénementhandler ISourisévénementhandler) {

	isourisévénementhandler = TPardéfautsourisévénementhandler{}

	if sourisévénementhandler != nil {
		isourisévénementhandler = sourisévénementhandler
	}

	actifsourispilote = self
	interruptionhandler = poignéesourisinterruption
	var address uintptr
	address = uintptr(Pointer(&interruptionhandler))
	self.Init(0x2C, uintptr(Pointer(gestionnaire)), address)

	for i := 0; i < 32 && (Portlireoctet(commandeport_2)&0x01) != 0; i++ {
		Portlireoctet(donnéesport_2)
	}

	if !écrireps2Commande(0xA8) || !écrireps2Commande(0x20) {
		return
	}
	état, valider := lireps2données()
	if !valider {
		return
	}
	état |= 0x02
	état &^= 0x20
	if !écrireps2Commande(0x60) || !écrireps2données(état) {
		return
	}

	if !envoyersourisCommande(0xF6) || !envoyersourisCommande(0xF4) {
		return
	}
	décalage = 0

}

func poignéesourisinterruption(esp uint32) uint32 {
	if actifsourispilote == nil {
		Portlireoctet(donnéesport_2)
		return esp
	}
	return actifsourispilote.Poignéeinterruption(esp)
}

var nombre uint8 = 0
var buffer_2 [3]int8
var décalage uint8 = 0

var bouton_2 int8
var attentex int16
var attentey int16
var attenteBouton int8
var attentesourisévénement bool

func (self *TSourispilote) Poignéeinterruption(esp uint32) uint32 {
	état := Portlireoctet(commandeport_2)
	if (état&0x01) == 0 || (état&0x20) == 0 {
		return esp
	}

	données := Portlireoctet(donnéesport_2)

	if décalage == 0 && (données&0x08) == 0 {
		return esp
	}
	buffer_2[décalage] = int8(données)
	décalage = (décalage + 1) % 3
	if décalage == 0 {
		packetÉtat := uint8(buffer_2[0])

		if (packetÉtat & 0xC0) == 0 {
			attentex += int16(buffer_2[1])
			attentey += int16(buffer_2[2])
			if attentex > 127 {
				attentex = 127
			} else if attentex < -127 {
				attentex = -127
			}
			if attentey > 127 {
				attentey = 127
			} else if attentey < -127 {
				attentey = -127
			}
		}
		attenteBouton = int8(packetÉtat & 0x07)
		attentesourisévénement = true
	}

	return esp

}

func Processusattentesourisévénements() {
	if isourisévénementhandler == nil {
		return
	}

	Interruptiondeactive()
	if !attentesourisévénement {
		InterruptionActif()
		return
	}
	x := int8(attentex)
	y := int8(attentey)
	nouveauBouton := attenteBouton
	vieuxBouton := bouton_2

	attentex = 0
	attentey = 0
	attentesourisévénement = false
	InterruptionActif()

	if x != 0 || y != 0 {
		isourisévénementhandler.SursourisDéplacer(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		masque := int8(0x1 << i)
		if (nouveauBouton & masque) != (vieuxBouton & masque) {
			if (nouveauBouton & masque) != 0 {
				isourisévénementhandler.SursourisVerslebas(int8(i + 1))
			} else {
				isourisévénementhandler.SursourisHaut(int8(i + 1))
			}
		}
	}
	bouton_2 = nouveauBouton
}
