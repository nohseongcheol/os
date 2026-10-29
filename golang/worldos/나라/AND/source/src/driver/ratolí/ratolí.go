/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package teclat

import . "unsafe"

import . "port"
import . "interrupció"
import . "consola"

type IRatolíEsdevenimenthandler interface {
	EngegatRatolíAvall(botó int8)
	EngegatRatolíAmunt(botó int8)
	EngegatRatolíMou(x int8, y int8)
}

var iRatolíEsdevenimenthandler IRatolíEsdevenimenthandler

type TPerdefecteRatolíEsdevenimenthandler struct {
}

var consola_2 TConsola = TConsola{}
var previousx int16 = 0
var previousy int16 = 0
var xPosició int16 = 0
var yPosició int16 = 0

func (unmateix TPerdefecteRatolíEsdevenimenthandler) EngegatRatolíAvall(botó int8) {
	buffer := []byte("+")
	consola_2.MImprimeixxy(buffer, uint16(previousx), uint16(previousy))
}
func (unmateix TPerdefecteRatolíEsdevenimenthandler) EngegatRatolíAmunt(botó int8)	{}
func (unmateix TPerdefecteRatolíEsdevenimenthandler) EngegatRatolíMou(x int8, y int8) {

	xPosició += int16(x)
	if xPosició < 0 {
		xPosició = 0
	}
	if xPosició >= 80 {
		xPosició = 79
	}

	yPosició -= int16(y)

	if yPosició < 0 {
		yPosició = 0
	}
	if yPosició >= 25 {
		yPosició = 24
	}

	buffer := []byte(" ")
	consola_2.MImprimeixxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	consola_2.MImprimeixxy(buffer, uint16(xPosició), uint16(yPosició))

	previousx = xPosició
	previousy = yPosició
}

type TRatolídriver struct {
	TInterrupcióhandler
}

var actiuRatolídriver *TRatolídriver
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

func enviaRatolíOrdre(valor uint8) bool {
	if !escripturaps2Ordre(0xD4) || !escripturaps2data(valor) {
		return false
	}
	ack, dacord := lecturaps2data()
	return dacord && ack == 0xFA
}

func (unmateix *TRatolídriver) Initdriver(manager *TInterrupciómanager, ratolíEsdevenimenthandler IRatolíEsdevenimenthandler) {

	iRatolíEsdevenimenthandler = TPerdefecteRatolíEsdevenimenthandler{}

	if ratolíEsdevenimenthandler != nil {
		iRatolíEsdevenimenthandler = ratolíEsdevenimenthandler
	}

	actiuRatolídriver = unmateix
	interrupcióhandler = gestorRatolíInterrupció
	var adreça uintptr
	adreça = uintptr(Pointer(&interrupcióhandler))
	unmateix.Init(0x2C, uintptr(Pointer(manager)), adreça)

	for i := 0; i < 32 && (PortLecturabyte(ordreport_2)&0x01) != 0; i++ {
		PortLecturabyte(dataport_2)
	}

	if !escripturaps2Ordre(0xA8) || !escripturaps2Ordre(0x20) {
		return
	}
	estat, dacord := lecturaps2data()
	if !dacord {
		return
	}
	estat |= 0x02
	estat &^= 0x20
	if !escripturaps2Ordre(0x60) || !escripturaps2data(estat) {
		return
	}

	if !enviaRatolíOrdre(0xF6) || !enviaRatolíOrdre(0xF4) {
		return
	}
	offset = 0

}

func gestorRatolíInterrupció(esp uint32) uint32 {
	if actiuRatolídriver == nil {
		PortLecturabyte(dataport_2)
		return esp
	}
	return actiuRatolídriver.GestorInterrupció(esp)
}

var recompte uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var botó_2 int8
var pendingx int16
var pendingy int16
var pendingBotó int8
var pendingRatolíEsdeveniment bool

func (unmateix *TRatolídriver) GestorInterrupció(esp uint32) uint32 {
	estat := PortLecturabyte(ordreport_2)
	if (estat&0x01) == 0 || (estat&0x20) == 0 {
		return esp
	}

	data := PortLecturabyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		pAQUETEstat := uint8(buffer_2[0])

		if (pAQUETEstat & 0xC0) == 0 {
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
		pendingBotó = int8(pAQUETEstat & 0x07)
		pendingRatolíEsdeveniment = true
	}

	return esp

}

func ProcéspendingRatolíEsdeveniments() {
	if iRatolíEsdevenimenthandler == nil {
		return
	}

	Interrupciódeactive()
	if !pendingRatolíEsdeveniment {
		InterrupcióActiu()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	nouBotó := pendingBotó
	oldBotó := botó_2

	pendingx = 0
	pendingy = 0
	pendingRatolíEsdeveniment = false
	InterrupcióActiu()

	if x != 0 || y != 0 {
		iRatolíEsdevenimenthandler.EngegatRatolíMou(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		màscara := int8(0x1 << i)
		if (nouBotó & màscara) != (oldBotó & màscara) {
			if (nouBotó & màscara) != 0 {
				iRatolíEsdevenimenthandler.EngegatRatolíAvall(int8(i + 1))
			} else {
				iRatolíEsdevenimenthandler.EngegatRatolíAmunt(int8(i + 1))
			}
		}
	}
	botó_2 = nouBotó
}
