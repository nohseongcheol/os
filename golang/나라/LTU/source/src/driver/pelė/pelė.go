package klaviatūra

import . "unsafe"

import . "prievadas"
import . "pertraukimas"
import . "console"

type IPelėĮvykishandler interface {
	ĮjungtaPelėŽemyn(mygtukas int8)
	ĮjungtaPelėAukštyn(mygtukas int8)
	ĮjungtaPelėPerkelti(x int8, y int8)
}

var iPelėĮvykishandler IPelėĮvykishandler

type TNumatytasisPelėĮvykishandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPozicija int16 = 0
var yPozicija int16 = 0

func (self TNumatytasisPelėĮvykishandler) ĮjungtaPelėŽemyn(mygtukas int8) {
	buffer := []byte("+")
	console_2.MSpausdintixy(buffer, uint16(previousx), uint16(previousy))
}
func (self TNumatytasisPelėĮvykishandler) ĮjungtaPelėAukštyn(mygtukas int8)	{}
func (self TNumatytasisPelėĮvykishandler) ĮjungtaPelėPerkelti(x int8, y int8) {

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
	console_2.MSpausdintixy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MSpausdintixy(buffer, uint16(xPozicija), uint16(yPozicija))

	previousx = xPozicija
	previousy = yPozicija
}

type TPelėdriver struct {
	TPertraukimashandler
}

var aktyvusPelėdriver *TPelėdriver
var pertraukimashandler func(uint32) uint32

var dataPrievadas_2 uint16 = 0x60
var komandaPrievadas_2 uint16 = 0x64

const ps2LauktiRiba = 100000

func lauktips2ĮvestisTuščia() bool {
	for i := 0; i < ps2LauktiRiba; i++ {
		if (PrievadasSkaitymasbyte(komandaPrievadas_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func lauktips2IšvestisPilna() bool {
	for i := 0; i < ps2LauktiRiba; i++ {
		if (PrievadasSkaitymasbyte(komandaPrievadas_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func rašymasps2Komanda(reikšmė uint8) bool {
	if !lauktips2ĮvestisTuščia() {
		return false
	}
	PrievadasRašymasbyte(komandaPrievadas_2, reikšmė)
	return true
}

func rašymasps2data(reikšmė uint8) bool {
	if !lauktips2ĮvestisTuščia() {
		return false
	}
	PrievadasRašymasbyte(dataPrievadas_2, reikšmė)
	return true
}

func skaitymasps2data() (uint8, bool) {
	if !lauktips2IšvestisPilna() {
		return 0, false
	}
	return PrievadasSkaitymasbyte(dataPrievadas_2), true
}

func siųstiPelėKomanda(reikšmė uint8) bool {
	if !rašymasps2Komanda(0xD4) || !rašymasps2data(reikšmė) {
		return false
	}
	ack, gerai := skaitymasps2data()
	return gerai && ack == 0xFA
}

func (self *TPelėdriver) Initdriver(manager *TPertraukimasmanager, pelėĮvykishandler IPelėĮvykishandler) {

	iPelėĮvykishandler = TNumatytasisPelėĮvykishandler{}

	if pelėĮvykishandler != nil {
		iPelėĮvykishandler = pelėĮvykishandler
	}

	aktyvusPelėdriver = self
	pertraukimashandler = pozicijaPelėPertraukimas
	var address uintptr
	address = uintptr(Pointer(&pertraukimashandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PrievadasSkaitymasbyte(komandaPrievadas_2)&0x01) != 0; i++ {
		PrievadasSkaitymasbyte(dataPrievadas_2)
	}

	if !rašymasps2Komanda(0xA8) || !rašymasps2Komanda(0x20) {
		return
	}
	būsena, gerai := skaitymasps2data()
	if !gerai {
		return
	}
	būsena |= 0x02
	būsena &^= 0x20
	if !rašymasps2Komanda(0x60) || !rašymasps2data(būsena) {
		return
	}

	if !siųstiPelėKomanda(0xF6) || !siųstiPelėKomanda(0xF4) {
		return
	}
	offset = 0

}

func pozicijaPelėPertraukimas(esp uint32) uint32 {
	if aktyvusPelėdriver == nil {
		PrievadasSkaitymasbyte(dataPrievadas_2)
		return esp
	}
	return aktyvusPelėdriver.PozicijaPertraukimas(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var mygtukas_2 int8
var pendingx int16
var pendingy int16
var pendingMygtukas int8
var pendingPelėĮvykis bool

func (self *TPelėdriver) PozicijaPertraukimas(esp uint32) uint32 {
	būsena := PrievadasSkaitymasbyte(komandaPrievadas_2)
	if (būsena&0x01) == 0 || (būsena&0x20) == 0 {
		return esp
	}

	data := PrievadasSkaitymasbyte(dataPrievadas_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetBūsena := uint8(buffer_2[0])

		if (packetBūsena & 0xC0) == 0 {
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
		pendingMygtukas = int8(packetBūsena & 0x07)
		pendingPelėĮvykis = true
	}

	return esp

}

func ProcesaspendingPelėĮvykiai() {
	if iPelėĮvykishandler == nil {
		return
	}

	Pertraukimasdeactive()
	if !pendingPelėĮvykis {
		PertraukimasAktyvus()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	naujasMygtukas := pendingMygtukas
	oldMygtukas := mygtukas_2

	pendingx = 0
	pendingy = 0
	pendingPelėĮvykis = false
	PertraukimasAktyvus()

	if x != 0 || y != 0 {
		iPelėĮvykishandler.ĮjungtaPelėPerkelti(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		kaukė := int8(0x1 << i)
		if (naujasMygtukas & kaukė) != (oldMygtukas & kaukė) {
			if (naujasMygtukas & kaukė) != 0 {
				iPelėĮvykishandler.ĮjungtaPelėŽemyn(int8(i + 1))
			} else {
				iPelėĮvykishandler.ĮjungtaPelėAukštyn(int8(i + 1))
			}
		}
	}
	mygtukas_2 = naujasMygtukas
}
