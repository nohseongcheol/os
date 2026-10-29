/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tastatura

import . "unsafe"

import . "port"
import . "ometanje"
import . "konzola"

type IMišDogađajhandler interface {
	NaMišNiže(dugme int8)
	NaMišGore(dugme int8)
	NaMišPremesti(x int8, y int8)
}

var iMišDogađajhandler IMišDogađajhandler

type TPodrazumevanoMišDogađajhandler struct {
}

var konzola_2 TKonzola = TKonzola{}
var previousx int16 = 0
var previousy int16 = 0
var xPoložaj int16 = 0
var yPoložaj int16 = 0

func (isti TPodrazumevanoMišDogađajhandler) NaMišNiže(dugme int8) {
	buffer := []byte("+")
	konzola_2.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))
}
func (isti TPodrazumevanoMišDogađajhandler) NaMišGore(dugme int8)	{}
func (isti TPodrazumevanoMišDogađajhandler) NaMišPremesti(x int8, y int8) {

	xPoložaj += int16(x)
	if xPoložaj < 0 {
		xPoložaj = 0
	}
	if xPoložaj >= 80 {
		xPoložaj = 79
	}

	yPoložaj -= int16(y)

	if yPoložaj < 0 {
		yPoložaj = 0
	}
	if yPoložaj >= 25 {
		yPoložaj = 24
	}

	buffer := []byte(" ")
	konzola_2.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konzola_2.MŠtampajxy(buffer, uint16(xPoložaj), uint16(yPoložaj))

	previousx = xPoložaj
	previousy = yPoložaj
}

type TMišdriver struct {
	TOmetanjehandler
}

var aktivnaMišdriver *TMišdriver
var ometanjehandler func(uint32) uint32

var dataPort_2 uint16 = 0x60
var naredbaPort_2 uint16 = 0x64

const ps2SačekajOgraniči = 100000

func sačekajps2UlazPrazno() bool {
	for i := 0; i < ps2SačekajOgraniči; i++ {
		if (Portčitanjebyte(naredbaPort_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func sačekajps2Izlazpotpuno() bool {
	for i := 0; i < ps2SačekajOgraniči; i++ {
		if (Portčitanjebyte(naredbaPort_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func pišeps2Naredba(vrednost uint8) bool {
	if !sačekajps2UlazPrazno() {
		return false
	}
	PortPišebyte(naredbaPort_2, vrednost)
	return true
}

func pišeps2data(vrednost uint8) bool {
	if !sačekajps2UlazPrazno() {
		return false
	}
	PortPišebyte(dataPort_2, vrednost)
	return true
}

func čitanjeps2data() (uint8, bool) {
	if !sačekajps2Izlazpotpuno() {
		return 0, false
	}
	return Portčitanjebyte(dataPort_2), true
}

func pošaljiMišNaredba(vrednost uint8) bool {
	if !pišeps2Naredba(0xD4) || !pišeps2data(vrednost) {
		return false
	}
	ack, uredu := čitanjeps2data()
	return uredu && ack == 0xFA
}

func (isti *TMišdriver) Initdriver(manager *TOmetanjemanager, mišDogađajhandler IMišDogađajhandler) {

	iMišDogađajhandler = TPodrazumevanoMišDogađajhandler{}

	if mišDogađajhandler != nil {
		iMišDogađajhandler = mišDogađajhandler
	}

	aktivnaMišdriver = isti
	ometanjehandler = ručkaMišOmetanje
	var address uintptr
	address = uintptr(Pointer(&ometanjehandler))
	isti.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portčitanjebyte(naredbaPort_2)&0x01) != 0; i++ {
		Portčitanjebyte(dataPort_2)
	}

	if !pišeps2Naredba(0xA8) || !pišeps2Naredba(0x20) {
		return
	}
	stanje, uredu := čitanjeps2data()
	if !uredu {
		return
	}
	stanje |= 0x02
	stanje &^= 0x20
	if !pišeps2Naredba(0x60) || !pišeps2data(stanje) {
		return
	}

	if !pošaljiMišNaredba(0xF6) || !pošaljiMišNaredba(0xF4) {
		return
	}
	offset = 0

}

func ručkaMišOmetanje(esp uint32) uint32 {
	if aktivnaMišdriver == nil {
		Portčitanjebyte(dataPort_2)
		return esp
	}
	return aktivnaMišdriver.RučkaOmetanje(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var dugme_2 int8
var pendingx int16
var pendingy int16
var pendingDugme int8
var pendingMišDogađaj bool

func (isti *TMišdriver) RučkaOmetanje(esp uint32) uint32 {
	stanje := Portčitanjebyte(naredbaPort_2)
	if (stanje&0x01) == 0 || (stanje&0x20) == 0 {
		return esp
	}

	data := Portčitanjebyte(dataPort_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetStanje := uint8(buffer_2[0])

		if (packetStanje & 0xC0) == 0 {
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
		pendingDugme = int8(packetStanje & 0x07)
		pendingMišDogađaj = true
	}

	return esp

}

func ProcespendingMišDogađaji() {
	if iMišDogađajhandler == nil {
		return
	}

	Ometanjedeactive()
	if !pendingMišDogađaj {
		OmetanjeAktivna()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	novaDugme := pendingDugme
	oldDugme := dugme_2

	pendingx = 0
	pendingy = 0
	pendingMišDogađaj = false
	OmetanjeAktivna()

	if x != 0 || y != 0 {
		iMišDogađajhandler.NaMišPremesti(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maska := int8(0x1 << i)
		if (novaDugme & maska) != (oldDugme & maska) {
			if (novaDugme & maska) != 0 {
				iMišDogađajhandler.NaMišNiže(int8(i + 1))
			} else {
				iMišDogađajhandler.NaMišGore(int8(i + 1))
			}
		}
	}
	dugme_2 = novaDugme
}
