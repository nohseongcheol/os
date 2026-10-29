/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package billentyűzet

import . "unsafe"

import . "port"
import . "megszakítás"
import . "konzol"

type IEgérEseményhandler interface {
	BeEgérLe(gomb int8)
	BeEgérFel(gomb int8)
	BeEgérÁthelyezés(x int8, y int8)
}

var iEgérEseményhandler IEgérEseményhandler

type TAlapértelmezettEgérEseményhandler struct {
}

var konzol_2 TKonzol = TKonzol{}
var previousx int16 = 0
var previousy int16 = 0
var xPozíció int16 = 0
var yPozíció int16 = 0

func (self TAlapértelmezettEgérEseményhandler) BeEgérLe(gomb int8) {
	buffer := []byte("+")
	konzol_2.MNyomtatásxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TAlapértelmezettEgérEseményhandler) BeEgérFel(gomb int8)	{}
func (self TAlapértelmezettEgérEseményhandler) BeEgérÁthelyezés(x int8, y int8) {

	xPozíció += int16(x)
	if xPozíció < 0 {
		xPozíció = 0
	}
	if xPozíció >= 80 {
		xPozíció = 79
	}

	yPozíció -= int16(y)

	if yPozíció < 0 {
		yPozíció = 0
	}
	if yPozíció >= 25 {
		yPozíció = 24
	}

	buffer := []byte(" ")
	konzol_2.MNyomtatásxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konzol_2.MNyomtatásxy(buffer, uint16(xPozíció), uint16(yPozíció))

	previousx = xPozíció
	previousy = yPozíció
}

type TEgérdriver struct {
	TMegszakításhandler
}

var aktívEgérdriver *TEgérdriver
var megszakításhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var parancsport_2 uint16 = 0x64

const ps2VárakozásKorlátozás = 100000

func várakozásps2BemenetÜres() bool {
	for i := 0; i < ps2VárakozásKorlátozás; i++ {
		if (PortOlvasásbyte(parancsport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func várakozásps2KimenetTeljes() bool {
	for i := 0; i < ps2VárakozásKorlátozás; i++ {
		if (PortOlvasásbyte(parancsport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func írásps2Parancs(érték uint8) bool {
	if !várakozásps2BemenetÜres() {
		return false
	}
	PortÍrásbyte(parancsport_2, érték)
	return true
}

func írásps2data(érték uint8) bool {
	if !várakozásps2BemenetÜres() {
		return false
	}
	PortÍrásbyte(dataport_2, érték)
	return true
}

func olvasásps2data() (uint8, bool) {
	if !várakozásps2KimenetTeljes() {
		return 0, false
	}
	return PortOlvasásbyte(dataport_2), true
}

func küldésEgérParancs(érték uint8) bool {
	if !írásps2Parancs(0xD4) || !írásps2data(érték) {
		return false
	}
	ack, ok := olvasásps2data()
	return ok && ack == 0xFA
}

func (self *TEgérdriver) Initdriver(manager *TMegszakításmanager, egérEseményhandler IEgérEseményhandler) {

	iEgérEseményhandler = TAlapértelmezettEgérEseményhandler{}

	if egérEseményhandler != nil {
		iEgérEseményhandler = egérEseményhandler
	}

	aktívEgérdriver = self
	megszakításhandler = fogantyúEgérMegszakítás
	var address uintptr
	address = uintptr(Pointer(&megszakításhandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortOlvasásbyte(parancsport_2)&0x01) != 0; i++ {
		PortOlvasásbyte(dataport_2)
	}

	if !írásps2Parancs(0xA8) || !írásps2Parancs(0x20) {
		return
	}
	állapot, ok := olvasásps2data()
	if !ok {
		return
	}
	állapot |= 0x02
	állapot &^= 0x20
	if !írásps2Parancs(0x60) || !írásps2data(állapot) {
		return
	}

	if !küldésEgérParancs(0xF6) || !küldésEgérParancs(0xF4) {
		return
	}
	eltolás = 0

}

func fogantyúEgérMegszakítás(esp uint32) uint32 {
	if aktívEgérdriver == nil {
		PortOlvasásbyte(dataport_2)
		return esp
	}
	return aktívEgérdriver.FogantyúMegszakítás(esp)
}

var számláló uint8 = 0
var buffer_2 [3]int8
var eltolás uint8 = 0

var gomb_2 int8
var pendingx int16
var pendingy int16
var pendingGomb int8
var pendingEgérEsemény bool

func (self *TEgérdriver) FogantyúMegszakítás(esp uint32) uint32 {
	állapot := PortOlvasásbyte(parancsport_2)
	if (állapot&0x01) == 0 || (állapot&0x20) == 0 {
		return esp
	}

	data := PortOlvasásbyte(dataport_2)

	if eltolás == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[eltolás] = int8(data)
	eltolás = (eltolás + 1) % 3
	if eltolás == 0 {
		packetÁllapot := uint8(buffer_2[0])

		if (packetÁllapot & 0xC0) == 0 {
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
		pendingGomb = int8(packetÁllapot & 0x07)
		pendingEgérEsemény = true
	}

	return esp

}

func FolyamatpendingEgérEsemények() {
	if iEgérEseményhandler == nil {
		return
	}

	Megszakításdeactive()
	if !pendingEgérEsemény {
		MegszakításAktív()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	újGomb := pendingGomb
	öregGomb := gomb_2

	pendingx = 0
	pendingy = 0
	pendingEgérEsemény = false
	MegszakításAktív()

	if x != 0 || y != 0 {
		iEgérEseményhandler.BeEgérÁthelyezés(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maszk := int8(0x1 << i)
		if (újGomb & maszk) != (öregGomb & maszk) {
			if (újGomb & maszk) != 0 {
				iEgérEseményhandler.BeEgérLe(int8(i + 1))
			} else {
				iEgérEseményhandler.BeEgérFel(int8(i + 1))
			}
		}
	}
	gomb_2 = újGomb
}
