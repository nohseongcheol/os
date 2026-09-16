/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tastiera

import . "unsafe"

import . "porta"
import . "interrupt"
import . "console"

type IMouseEventohandler interface {
	AccesomouseGiù(pulsante int8)
	AccesomouseSu(pulsante int8)
	AccesomouseSposta(x int8, y int8)
}

var imouseEventohandler IMouseEventohandler

type TPredefinitomouseEventohandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPosizione int16 = 0
var yPosizione int16 = 0

func (séstesso TPredefinitomouseEventohandler) AccesomouseGiù(pulsante int8) {
	buffer := []byte("+")
	console_2.MStampaxy(buffer, uint16(previousx), uint16(previousy))
}
func (séstesso TPredefinitomouseEventohandler) AccesomouseSu(pulsante int8)	{}
func (séstesso TPredefinitomouseEventohandler) AccesomouseSposta(x int8, y int8) {

	xPosizione += int16(x)
	if xPosizione < 0 {
		xPosizione = 0
	}
	if xPosizione >= 80 {
		xPosizione = 79
	}

	yPosizione -= int16(y)

	if yPosizione < 0 {
		yPosizione = 0
	}
	if yPosizione >= 25 {
		yPosizione = 24
	}

	buffer := []byte(" ")
	console_2.MStampaxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MStampaxy(buffer, uint16(xPosizione), uint16(yPosizione))

	previousx = xPosizione
	previousy = yPosizione
}

type TMousedriver struct {
	TInterrupthandler
}

var attivomousedriver *TMousedriver
var interrupthandler func(uint32) uint32

var dataPorta_2 uint16 = 0x60
var comandoPorta_2 uint16 = 0x64

const ps2AttendiLimite = 100000

func attendips2IngressoVuoto() bool {
	for i := 0; i < ps2AttendiLimite; i++ {
		if (PortaLetturabyte(comandoPorta_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func attendips2UscitaCompleto() bool {
	for i := 0; i < ps2AttendiLimite; i++ {
		if (PortaLetturabyte(comandoPorta_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func scritturaps2Comando(valore uint8) bool {
	if !attendips2IngressoVuoto() {
		return false
	}
	PortaScritturabyte(comandoPorta_2, valore)
	return true
}

func scritturaps2data(valore uint8) bool {
	if !attendips2IngressoVuoto() {
		return false
	}
	PortaScritturabyte(dataPorta_2, valore)
	return true
}

func letturaps2data() (uint8, bool) {
	if !attendips2UscitaCompleto() {
		return 0, false
	}
	return PortaLetturabyte(dataPorta_2), true
}

func spediscimouseComando(valore uint8) bool {
	if !scritturaps2Comando(0xD4) || !scritturaps2data(valore) {
		return false
	}
	ack, fatto := letturaps2data()
	return fatto && ack == 0xFA
}

func (séstesso *TMousedriver) Initdriver(manager *TInterruptmanager, mouseEventohandler IMouseEventohandler) {

	imouseEventohandler = TPredefinitomouseEventohandler{}

	if mouseEventohandler != nil {
		imouseEventohandler = mouseEventohandler
	}

	attivomousedriver = séstesso
	interrupthandler = manigliamouseinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	séstesso.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortaLetturabyte(comandoPorta_2)&0x01) != 0; i++ {
		PortaLetturabyte(dataPorta_2)
	}

	if !scritturaps2Comando(0xA8) || !scritturaps2Comando(0x20) {
		return
	}
	stato, fatto := letturaps2data()
	if !fatto {
		return
	}
	stato |= 0x02
	stato &^= 0x20
	if !scritturaps2Comando(0x60) || !scritturaps2data(stato) {
		return
	}

	if !spediscimouseComando(0xF6) || !spediscimouseComando(0xF4) {
		return
	}
	offset = 0

}

func manigliamouseinterrupt(esp uint32) uint32 {
	if attivomousedriver == nil {
		PortaLetturabyte(dataPorta_2)
		return esp
	}
	return attivomousedriver.Manigliainterrupt(esp)
}

var conteggio uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var pulsante_2 int8
var pendingx int16
var pendingy int16
var pendingPulsante int8
var pendingmouseEvento bool

func (séstesso *TMousedriver) Manigliainterrupt(esp uint32) uint32 {
	stato := PortaLetturabyte(comandoPorta_2)
	if (stato&0x01) == 0 || (stato&0x20) == 0 {
		return esp
	}

	data := PortaLetturabyte(dataPorta_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		pACCHETTOStato := uint8(buffer_2[0])

		if (pACCHETTOStato & 0xC0) == 0 {
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
		pendingPulsante = int8(pACCHETTOStato & 0x07)
		pendingmouseEvento = true
	}

	return esp

}

func ProcessipendingmouseEventi() {
	if imouseEventohandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingmouseEvento {
		InterruptAttivo()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	nuovoPulsante := pendingPulsante
	oldPulsante := pulsante_2

	pendingx = 0
	pendingy = 0
	pendingmouseEvento = false
	InterruptAttivo()

	if x != 0 || y != 0 {
		imouseEventohandler.AccesomouseSposta(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maschera := int8(0x1 << i)
		if (nuovoPulsante & maschera) != (oldPulsante & maschera) {
			if (nuovoPulsante & maschera) != 0 {
				imouseEventohandler.AccesomouseGiù(int8(i + 1))
			} else {
				imouseEventohandler.AccesomouseSu(int8(i + 1))
			}
		}
	}
	pulsante_2 = nuovoPulsante
}
