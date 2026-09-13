package klávesnica

import . "unsafe"

import . "port"
import . "prerušenie"
import . "konzola"

type IMyšUdalosťhandler interface {
	ZapnutéMyšDole(tlačidlo int8)
	ZapnutéMyšHore(tlačidlo int8)
	ZapnutéMyšPresunúť(x int8, y int8)
}

var iMyšUdalosťhandler IMyšUdalosťhandler

type TPredvolenéMyšUdalosťhandler struct {
}

var konzola_2 TKonzola = TKonzola{}
var previousx int16 = 0
var previousy int16 = 0
var xPozícia int16 = 0
var yPozícia int16 = 0

func (vlastný TPredvolenéMyšUdalosťhandler) ZapnutéMyšDole(tlačidlo int8) {
	buffer := []byte("+")
	konzola_2.MTlačiťxy(buffer, uint16(previousx), uint16(previousy))
}
func (vlastný TPredvolenéMyšUdalosťhandler) ZapnutéMyšHore(tlačidlo int8)	{}
func (vlastný TPredvolenéMyšUdalosťhandler) ZapnutéMyšPresunúť(x int8, y int8) {

	xPozícia += int16(x)
	if xPozícia < 0 {
		xPozícia = 0
	}
	if xPozícia >= 80 {
		xPozícia = 79
	}

	yPozícia -= int16(y)

	if yPozícia < 0 {
		yPozícia = 0
	}
	if yPozícia >= 25 {
		yPozícia = 24
	}

	buffer := []byte(" ")
	konzola_2.MTlačiťxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konzola_2.MTlačiťxy(buffer, uint16(xPozícia), uint16(yPozícia))

	previousx = xPozícia
	previousy = yPozícia
}

type TMyšdriver struct {
	TPrerušeniehandler
}

var aktívnyMyšdriver *TMyšdriver
var prerušeniehandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var príkazport_2 uint16 = 0x64

const ps2PočkaťObmedzenie = 100000

func počkaťps2VstupPrázdne() bool {
	for i := 0; i < ps2PočkaťObmedzenie; i++ {
		if (PortČítaniebyte(príkazport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func počkaťps2VýstupPlné() bool {
	for i := 0; i < ps2PočkaťObmedzenie; i++ {
		if (PortČítaniebyte(príkazport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func zápisps2Príkaz(hodnota uint8) bool {
	if !počkaťps2VstupPrázdne() {
		return false
	}
	PortZápisbyte(príkazport_2, hodnota)
	return true
}

func zápisps2data(hodnota uint8) bool {
	if !počkaťps2VstupPrázdne() {
		return false
	}
	PortZápisbyte(dataport_2, hodnota)
	return true
}

func čítanieps2data() (uint8, bool) {
	if !počkaťps2VýstupPlné() {
		return 0, false
	}
	return PortČítaniebyte(dataport_2), true
}

func poslaťMyšPríkaz(hodnota uint8) bool {
	if !zápisps2Príkaz(0xD4) || !zápisps2data(hodnota) {
		return false
	}
	ack, ok := čítanieps2data()
	return ok && ack == 0xFA
}

func (vlastný *TMyšdriver) Initdriver(manager *TPrerušeniemanager, myšUdalosťhandler IMyšUdalosťhandler) {

	iMyšUdalosťhandler = TPredvolenéMyšUdalosťhandler{}

	if myšUdalosťhandler != nil {
		iMyšUdalosťhandler = myšUdalosťhandler
	}

	aktívnyMyšdriver = vlastný
	prerušeniehandler = uškoMyšPrerušenie
	var address uintptr
	address = uintptr(Pointer(&prerušeniehandler))
	vlastný.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortČítaniebyte(príkazport_2)&0x01) != 0; i++ {
		PortČítaniebyte(dataport_2)
	}

	if !zápisps2Príkaz(0xA8) || !zápisps2Príkaz(0x20) {
		return
	}
	stav, ok := čítanieps2data()
	if !ok {
		return
	}
	stav |= 0x02
	stav &^= 0x20
	if !zápisps2Príkaz(0x60) || !zápisps2data(stav) {
		return
	}

	if !poslaťMyšPríkaz(0xF6) || !poslaťMyšPríkaz(0xF4) {
		return
	}
	posunutie = 0

}

func uškoMyšPrerušenie(esp uint32) uint32 {
	if aktívnyMyšdriver == nil {
		PortČítaniebyte(dataport_2)
		return esp
	}
	return aktívnyMyšdriver.UškoPrerušenie(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var posunutie uint8 = 0

var tlačidlo_2 int8
var pendingx int16
var pendingy int16
var pendingTlačidlo int8
var pendingMyšUdalosť bool

func (vlastný *TMyšdriver) UškoPrerušenie(esp uint32) uint32 {
	stav := PortČítaniebyte(príkazport_2)
	if (stav&0x01) == 0 || (stav&0x20) == 0 {
		return esp
	}

	data := PortČítaniebyte(dataport_2)

	if posunutie == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[posunutie] = int8(data)
	posunutie = (posunutie + 1) % 3
	if posunutie == 0 {
		packetStav := uint8(buffer_2[0])

		if (packetStav & 0xC0) == 0 {
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
		pendingTlačidlo = int8(packetStav & 0x07)
		pendingMyšUdalosť = true
	}

	return esp

}

func ProcespendingMyšUdalosti() {
	if iMyšUdalosťhandler == nil {
		return
	}

	Prerušeniedeactive()
	if !pendingMyšUdalosť {
		PrerušenieAktívny()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	novýTlačidlo := pendingTlačidlo
	oldTlačidlo := tlačidlo_2

	pendingx = 0
	pendingy = 0
	pendingMyšUdalosť = false
	PrerušenieAktívny()

	if x != 0 || y != 0 {
		iMyšUdalosťhandler.ZapnutéMyšPresunúť(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maska := int8(0x1 << i)
		if (novýTlačidlo & maska) != (oldTlačidlo & maska) {
			if (novýTlačidlo & maska) != 0 {
				iMyšUdalosťhandler.ZapnutéMyšDole(int8(i + 1))
			} else {
				iMyšUdalosťhandler.ZapnutéMyšHore(int8(i + 1))
			}
		}
	}
	tlačidlo_2 = novýTlačidlo
}
