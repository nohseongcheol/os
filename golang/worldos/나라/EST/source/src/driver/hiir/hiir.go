/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package klaviatuur

import . "unsafe"

import . "port"
import . "katkestus"
import . "console"

type IHiirSündmushandler interface {
	SeesHiirNoolalla(nupp int8)
	SeesHiirÜles(nupp int8)
	SeesHiirLiiguta(x int8, y int8)
}

var iHiirSündmushandler IHiirSündmushandler

type TVaikimisiHiirSündmushandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xAsukoht int16 = 0
var yAsukoht int16 = 0

func (ise TVaikimisiHiirSündmushandler) SeesHiirNoolalla(nupp int8) {
	buffer := []byte("+")
	console_2.MPrindixy(buffer, uint16(previousx), uint16(previousy))
}
func (ise TVaikimisiHiirSündmushandler) SeesHiirÜles(nupp int8)	{}
func (ise TVaikimisiHiirSündmushandler) SeesHiirLiiguta(x int8, y int8) {

	xAsukoht += int16(x)
	if xAsukoht < 0 {
		xAsukoht = 0
	}
	if xAsukoht >= 80 {
		xAsukoht = 79
	}

	yAsukoht -= int16(y)

	if yAsukoht < 0 {
		yAsukoht = 0
	}
	if yAsukoht >= 25 {
		yAsukoht = 24
	}

	buffer := []byte(" ")
	console_2.MPrindixy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MPrindixy(buffer, uint16(xAsukoht), uint16(yAsukoht))

	previousx = xAsukoht
	previousy = yAsukoht
}

type THiirdriver struct {
	TKatkestushandler
}

var aktiivneHiirdriver *THiirdriver
var katkestushandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var käskport_2 uint16 = 0x64

const ps2OotaPiir = 100000

func ootaps2SisendTühi() bool {
	for i := 0; i < ps2OotaPiir; i++ {
		if (PortLugeminebyte(käskport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ootaps2VäljundTäielik() bool {
	for i := 0; i < ps2OotaPiir; i++ {
		if (PortLugeminebyte(käskport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func kirjutamineps2Käsk(väärtus uint8) bool {
	if !ootaps2SisendTühi() {
		return false
	}
	PortKirjutaminebyte(käskport_2, väärtus)
	return true
}

func kirjutamineps2data(väärtus uint8) bool {
	if !ootaps2SisendTühi() {
		return false
	}
	PortKirjutaminebyte(dataport_2, väärtus)
	return true
}

func lugemineps2data() (uint8, bool) {
	if !ootaps2VäljundTäielik() {
		return 0, false
	}
	return PortLugeminebyte(dataport_2), true
}

func saadaHiirKäsk(väärtus uint8) bool {
	if !kirjutamineps2Käsk(0xD4) || !kirjutamineps2data(väärtus) {
		return false
	}
	ack, olgu := lugemineps2data()
	return olgu && ack == 0xFA
}

func (ise *THiirdriver) Initdriver(manager *TKatkestusmanager, hiirSündmushandler IHiirSündmushandler) {

	iHiirSündmushandler = TVaikimisiHiirSündmushandler{}

	if hiirSündmushandler != nil {
		iHiirSündmushandler = hiirSündmushandler
	}

	aktiivneHiirdriver = ise
	katkestushandler = handleHiirKatkestus
	var address uintptr
	address = uintptr(Pointer(&katkestushandler))
	ise.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortLugeminebyte(käskport_2)&0x01) != 0; i++ {
		PortLugeminebyte(dataport_2)
	}

	if !kirjutamineps2Käsk(0xA8) || !kirjutamineps2Käsk(0x20) {
		return
	}
	olek, olgu := lugemineps2data()
	if !olgu {
		return
	}
	olek |= 0x02
	olek &^= 0x20
	if !kirjutamineps2Käsk(0x60) || !kirjutamineps2data(olek) {
		return
	}

	if !saadaHiirKäsk(0xF6) || !saadaHiirKäsk(0xF4) {
		return
	}
	offset = 0

}

func handleHiirKatkestus(esp uint32) uint32 {
	if aktiivneHiirdriver == nil {
		PortLugeminebyte(dataport_2)
		return esp
	}
	return aktiivneHiirdriver.HandleKatkestus(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var nupp_2 int8
var pendingx int16
var pendingy int16
var pendingnupp int8
var pendingHiirSündmus bool

func (ise *THiirdriver) HandleKatkestus(esp uint32) uint32 {
	olek := PortLugeminebyte(käskport_2)
	if (olek&0x01) == 0 || (olek&0x20) == 0 {
		return esp
	}

	data := PortLugeminebyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetOlek := uint8(buffer_2[0])

		if (packetOlek & 0xC0) == 0 {
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
		pendingnupp = int8(packetOlek & 0x07)
		pendingHiirSündmus = true
	}

	return esp

}

func ProtsesspendingHiirSündmused() {
	if iHiirSündmushandler == nil {
		return
	}

	Katkestusdeactive()
	if !pendingHiirSündmus {
		KatkestusAktiivne()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	uusnupp := pendingnupp
	oldnupp := nupp_2

	pendingx = 0
	pendingy = 0
	pendingHiirSündmus = false
	KatkestusAktiivne()

	if x != 0 || y != 0 {
		iHiirSündmushandler.SeesHiirLiiguta(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (uusnupp & mask) != (oldnupp & mask) {
			if (uusnupp & mask) != 0 {
				iHiirSündmushandler.SeesHiirNoolalla(int8(i + 1))
			} else {
				iHiirSündmushandler.SeesHiirÜles(int8(i + 1))
			}
		}
	}
	nupp_2 = uusnupp
}
