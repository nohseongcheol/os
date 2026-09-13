package tipkovnica

import . "unsafe"

import . "port"
import . "prekid"
import . "console"

type IMišDogađajhandler interface {
	UključenoMišDolje(dugme int8)
	UključenoMišGore(dugme int8)
	UključenoMišPremjesti(x int8, y int8)
}

var iMišDogađajhandler IMišDogađajhandler

type TZadanoMišDogađajhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPozicija int16 = 0
var yPozicija int16 = 0

func (sam TZadanoMišDogađajhandler) UključenoMišDolje(dugme int8) {
	buffer := []byte("+")
	console_2.MIspisxy(buffer, uint16(previousx), uint16(previousy))
}
func (sam TZadanoMišDogađajhandler) UključenoMišGore(dugme int8)	{}
func (sam TZadanoMišDogađajhandler) UključenoMišPremjesti(x int8, y int8) {

	xPozicija += int16(x)
	if xPozicija < 0 {
		xPozicija = 0
	}
	if xPozicija >= 80 {
		xPozicija = 79
	}

	yPozicija -= int16(y)

	if yPozicija < 0 {
		yPozicija = 0
	}
	if yPozicija >= 25 {
		yPozicija = 24
	}

	buffer := []byte(" ")
	console_2.MIspisxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MIspisxy(buffer, uint16(xPozicija), uint16(yPozicija))

	previousx = xPozicija
	previousy = yPozicija
}

type TMišdriver struct {
	TPrekidhandler
}

var aktivanMišdriver *TMišdriver
var prekidhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var naredbaport_2 uint16 = 0x64

const ps2ČekajOgraničenje = 100000

func čekajps2UlazPrazno() bool {
	for i := 0; i < ps2ČekajOgraničenje; i++ {
		if (PortČitajbyte(naredbaport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func čekajps2IzlazPun() bool {
	for i := 0; i < ps2ČekajOgraničenje; i++ {
		if (PortČitajbyte(naredbaport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func zapišips2Naredba(vrijednost uint8) bool {
	if !čekajps2UlazPrazno() {
		return false
	}
	PortZapišibyte(naredbaport_2, vrijednost)
	return true
}

func zapišips2data(vrijednost uint8) bool {
	if !čekajps2UlazPrazno() {
		return false
	}
	PortZapišibyte(dataport_2, vrijednost)
	return true
}

func čitajps2data() (uint8, bool) {
	if !čekajps2IzlazPun() {
		return 0, false
	}
	return PortČitajbyte(dataport_2), true
}

func pošaljiMišNaredba(vrijednost uint8) bool {
	if !zapišips2Naredba(0xD4) || !zapišips2data(vrijednost) {
		return false
	}
	ack, uredu := čitajps2data()
	return uredu && ack == 0xFA
}

func (sam *TMišdriver) Initdriver(manager *TPrekidmanager, mišDogađajhandler IMišDogađajhandler) {

	iMišDogađajhandler = TZadanoMišDogađajhandler{}

	if mišDogađajhandler != nil {
		iMišDogađajhandler = mišDogađajhandler
	}

	aktivanMišdriver = sam
	prekidhandler = ručkaMišPrekid
	var address uintptr
	address = uintptr(Pointer(&prekidhandler))
	sam.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortČitajbyte(naredbaport_2)&0x01) != 0; i++ {
		PortČitajbyte(dataport_2)
	}

	if !zapišips2Naredba(0xA8) || !zapišips2Naredba(0x20) {
		return
	}
	stanje, uredu := čitajps2data()
	if !uredu {
		return
	}
	stanje |= 0x02
	stanje &^= 0x20
	if !zapišips2Naredba(0x60) || !zapišips2data(stanje) {
		return
	}

	if !pošaljiMišNaredba(0xF6) || !pošaljiMišNaredba(0xF4) {
		return
	}
	offset = 0

}

func ručkaMišPrekid(esp uint32) uint32 {
	if aktivanMišdriver == nil {
		PortČitajbyte(dataport_2)
		return esp
	}
	return aktivanMišdriver.RučkaPrekid(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var dugme_2 int8
var pendingx int16
var pendingy int16
var pendingDugme int8
var pendingMišDogađaj bool

func (sam *TMišdriver) RučkaPrekid(esp uint32) uint32 {
	stanje := PortČitajbyte(naredbaport_2)
	if (stanje&0x01) == 0 || (stanje&0x20) == 0 {
		return esp
	}

	data := PortČitajbyte(dataport_2)

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

func ProcespendingMiševents() {
	if iMišDogađajhandler == nil {
		return
	}

	Prekiddeactive()
	if !pendingMišDogađaj {
		PrekidAktivan()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	noviDugme := pendingDugme
	oldDugme := dugme_2

	pendingx = 0
	pendingy = 0
	pendingMišDogađaj = false
	PrekidAktivan()

	if x != 0 || y != 0 {
		iMišDogađajhandler.UključenoMišPremjesti(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maska := int8(0x1 << i)
		if (noviDugme & maska) != (oldDugme & maska) {
			if (noviDugme & maska) != 0 {
				iMišDogađajhandler.UključenoMišDolje(int8(i + 1))
			} else {
				iMišDogađajhandler.UključenoMišGore(int8(i + 1))
			}
		}
	}
	dugme_2 = noviDugme
}
