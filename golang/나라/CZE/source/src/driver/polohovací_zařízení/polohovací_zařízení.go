package klávesnice

import . "unsafe"

import . "port"
import . "přerušení"
import . "konzole"

type IMyšUdálostihandler interface {
	ZapnutoMyšDolů(tlačítko int8)
	ZapnutoMyšNahoru(tlačítko int8)
	ZapnutoMyšPřesunout(x int8, y int8)
}

var iMyšUdálostihandler IMyšUdálostihandler

type TVýchozíMyšUdálostihandler struct {
}

var konzole_2 TKonzole = TKonzole{}
var previousx int16 = 0
var previousy int16 = 0
var xUmístění int16 = 0
var yUmístění int16 = 0

func (self TVýchozíMyšUdálostihandler) ZapnutoMyšDolů(tlačítko int8) {
	buffer := []byte("+")
	konzole_2.MTisknoutxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TVýchozíMyšUdálostihandler) ZapnutoMyšNahoru(tlačítko int8)	{}
func (self TVýchozíMyšUdálostihandler) ZapnutoMyšPřesunout(x int8, y int8) {

	xUmístění += int16(x)
	if xUmístění < 0 {
		xUmístění = 0
	}
	if xUmístění >= 80 {
		xUmístění = 79
	}

	yUmístění -= int16(y)

	if yUmístění < 0 {
		yUmístění = 0
	}
	if yUmístění >= 25 {
		yUmístění = 24
	}

	buffer := []byte(" ")
	konzole_2.MTisknoutxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konzole_2.MTisknoutxy(buffer, uint16(xUmístění), uint16(yUmístění))

	previousx = xUmístění
	previousy = yUmístění
}

type TMyšdriver struct {
	TPřerušeníhandler
}

var aktivníMyšdriver *TMyšdriver
var přerušeníhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var příkazport_2 uint16 = 0x64

const ps2PočkatOmezení = 100000

func počkatps2VstupPrázdné() bool {
	for i := 0; i < ps2PočkatOmezení; i++ {
		if (PortČteníbyte(příkazport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func počkatps2VýstupÚplný() bool {
	for i := 0; i < ps2PočkatOmezení; i++ {
		if (PortČteníbyte(příkazport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func zápisps2Příkaz(hodnota uint8) bool {
	if !počkatps2VstupPrázdné() {
		return false
	}
	PortZápisbyte(příkazport_2, hodnota)
	return true
}

func zápisps2data(hodnota uint8) bool {
	if !počkatps2VstupPrázdné() {
		return false
	}
	PortZápisbyte(dataport_2, hodnota)
	return true
}

func čteníps2data() (uint8, bool) {
	if !počkatps2VýstupÚplný() {
		return 0, false
	}
	return PortČteníbyte(dataport_2), true
}

func poslatMyšPříkaz(hodnota uint8) bool {
	if !zápisps2Příkaz(0xD4) || !zápisps2data(hodnota) {
		return false
	}
	ack, budiž := čteníps2data()
	return budiž && ack == 0xFA
}

func (self *TMyšdriver) Initdriver(manager *TPřerušenímanager, myšUdálostihandler IMyšUdálostihandler) {

	iMyšUdálostihandler = TVýchozíMyšUdálostihandler{}

	if myšUdálostihandler != nil {
		iMyšUdálostihandler = myšUdálostihandler
	}

	aktivníMyšdriver = self
	přerušeníhandler = úchytkaMyšPřerušení
	var adresa uintptr
	adresa = uintptr(Pointer(&přerušeníhandler))
	self.Init(0x2C, uintptr(Pointer(manager)), adresa)

	for i := 0; i < 32 && (PortČteníbyte(příkazport_2)&0x01) != 0; i++ {
		PortČteníbyte(dataport_2)
	}

	if !zápisps2Příkaz(0xA8) || !zápisps2Příkaz(0x20) {
		return
	}
	stav, budiž := čteníps2data()
	if !budiž {
		return
	}
	stav |= 0x02
	stav &^= 0x20
	if !zápisps2Příkaz(0x60) || !zápisps2data(stav) {
		return
	}

	if !poslatMyšPříkaz(0xF6) || !poslatMyšPříkaz(0xF4) {
		return
	}
	offset = 0

}

func úchytkaMyšPřerušení(esp uint32) uint32 {
	if aktivníMyšdriver == nil {
		PortČteníbyte(dataport_2)
		return esp
	}
	return aktivníMyšdriver.ÚchytkaPřerušení(esp)
}

var počet uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var tlačítko_2 int8
var pendingx int16
var pendingy int16
var pendingTlačítko int8
var pendingMyšUdálosti bool

func (self *TMyšdriver) ÚchytkaPřerušení(esp uint32) uint32 {
	stav := PortČteníbyte(příkazport_2)
	if (stav&0x01) == 0 || (stav&0x20) == 0 {
		return esp
	}

	data := PortČteníbyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		pAKETStav := uint8(buffer_2[0])

		if (pAKETStav & 0xC0) == 0 {
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
		pendingTlačítko = int8(pAKETStav & 0x07)
		pendingMyšUdálosti = true
	}

	return esp

}

func ProcespendingMyšUdálosti() {
	if iMyšUdálostihandler == nil {
		return
	}

	Přerušenídeactive()
	if !pendingMyšUdálosti {
		PřerušeníAktivní()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	novýTlačítko := pendingTlačítko
	oldTlačítko := tlačítko_2

	pendingx = 0
	pendingy = 0
	pendingMyšUdálosti = false
	PřerušeníAktivní()

	if x != 0 || y != 0 {
		iMyšUdálostihandler.ZapnutoMyšPřesunout(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maska := int8(0x1 << i)
		if (novýTlačítko & maska) != (oldTlačítko & maska) {
			if (novýTlačítko & maska) != 0 {
				iMyšUdálostihandler.ZapnutoMyšDolů(int8(i + 1))
			} else {
				iMyšUdálostihandler.ZapnutoMyšNahoru(int8(i + 1))
			}
		}
	}
	tlačítko_2 = novýTlačítko
}
