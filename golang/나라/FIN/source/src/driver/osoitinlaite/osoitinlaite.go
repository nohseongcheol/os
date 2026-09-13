package näppäimistö

import . "unsafe"

import . "portti"
import . "keskeytys"
import . "konsoli"

type IHiiriTapahtumahandler interface {
	PäälläHiiriAlas(painike int8)
	PäälläHiiriYlös(painike int8)
	PäälläHiiriSiirrä(x int8, y int8)
}

var iHiiriTapahtumahandler IHiiriTapahtumahandler

type TOletusHiiriTapahtumahandler struct {
}

var konsoli_2 TKonsoli = TKonsoli{}
var previousx int16 = 0
var previousy int16 = 0
var xSijainti int16 = 0
var ySijainti int16 = 0

func (itse TOletusHiiriTapahtumahandler) PäälläHiiriAlas(painike int8) {
	buffer := []byte("+")
	konsoli_2.MTulostaxy(buffer, uint16(previousx), uint16(previousy))
}
func (itse TOletusHiiriTapahtumahandler) PäälläHiiriYlös(painike int8)	{}
func (itse TOletusHiiriTapahtumahandler) PäälläHiiriSiirrä(x int8, y int8) {

	xSijainti += int16(x)
	if xSijainti < 0 {
		xSijainti = 0
	}
	if xSijainti >= 80 {
		xSijainti = 79
	}

	ySijainti -= int16(y)

	if ySijainti < 0 {
		ySijainti = 0
	}
	if ySijainti >= 25 {
		ySijainti = 24
	}

	buffer := []byte(" ")
	konsoli_2.MTulostaxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konsoli_2.MTulostaxy(buffer, uint16(xSijainti), uint16(ySijainti))

	previousx = xSijainti
	previousy = ySijainti
}

type THiiridriver struct {
	TKeskeytyshandler
}

var aktiivinenHiiridriver *THiiridriver
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

func lähetäHiiriKomento(arvo uint8) bool {
	if !kirjoitusps2Komento(0xD4) || !kirjoitusps2data(arvo) {
		return false
	}
	ack, ok := lukups2data()
	return ok && ack == 0xFA
}

func (itse *THiiridriver) Initdriver(manager *TKeskeytysmanager, hiiriTapahtumahandler IHiiriTapahtumahandler) {

	iHiiriTapahtumahandler = TOletusHiiriTapahtumahandler{}

	if hiiriTapahtumahandler != nil {
		iHiiriTapahtumahandler = hiiriTapahtumahandler
	}

	aktiivinenHiiridriver = itse
	keskeytyshandler = kahvaHiiriKeskeytys
	var address uintptr
	address = uintptr(Pointer(&keskeytyshandler))
	itse.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PorttiLukubyte(komentoPortti_2)&0x01) != 0; i++ {
		PorttiLukubyte(dataPortti_2)
	}

	if !kirjoitusps2Komento(0xA8) || !kirjoitusps2Komento(0x20) {
		return
	}
	tila, ok := lukups2data()
	if !ok {
		return
	}
	tila |= 0x02
	tila &^= 0x20
	if !kirjoitusps2Komento(0x60) || !kirjoitusps2data(tila) {
		return
	}

	if !lähetäHiiriKomento(0xF6) || !lähetäHiiriKomento(0xF4) {
		return
	}
	offset = 0

}

func kahvaHiiriKeskeytys(esp uint32) uint32 {
	if aktiivinenHiiridriver == nil {
		PorttiLukubyte(dataPortti_2)
		return esp
	}
	return aktiivinenHiiridriver.KahvaKeskeytys(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var painike_2 int8
var pendingx int16
var pendingy int16
var pendingPainike int8
var pendingHiiriTapahtuma bool

func (itse *THiiridriver) KahvaKeskeytys(esp uint32) uint32 {
	tila := PorttiLukubyte(komentoPortti_2)
	if (tila&0x01) == 0 || (tila&0x20) == 0 {
		return esp
	}

	data := PorttiLukubyte(dataPortti_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetTila := uint8(buffer_2[0])

		if (packetTila & 0xC0) == 0 {
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
		pendingPainike = int8(packetTila & 0x07)
		pendingHiiriTapahtuma = true
	}

	return esp

}

func ProsessipendingHiiriTapahtumat() {
	if iHiiriTapahtumahandler == nil {
		return
	}

	Keskeytysdeactive()
	if !pendingHiiriTapahtuma {
		KeskeytysAktiivinen()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	uusiPainike := pendingPainike
	oldPainike := painike_2

	pendingx = 0
	pendingy = 0
	pendingHiiriTapahtuma = false
	KeskeytysAktiivinen()

	if x != 0 || y != 0 {
		iHiiriTapahtumahandler.PäälläHiiriSiirrä(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		peite := int8(0x1 << i)
		if (uusiPainike & peite) != (oldPainike & peite) {
			if (uusiPainike & peite) != 0 {
				iHiiriTapahtumahandler.PäälläHiiriAlas(int8(i + 1))
			} else {
				iHiiriTapahtumahandler.PäälläHiiriYlös(int8(i + 1))
			}
		}
	}
	painike_2 = uusiPainike
}
