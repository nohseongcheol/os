package tastiera

import . "unsafe"

import . "porta"
import . "interrupt"
import . "konsolë"

type IMiuNgjarjehandler interface {
	OnMiuPoshtë(buton int8)
	OnMiuSipër(buton int8)
	OnMiuLëviz(x int8, y int8)
}

var iMiuNgjarjehandler IMiuNgjarjehandler

type TEprezgjedhurMiuNgjarjehandler struct {
}

var konsolë_2 TKonsolë = TKonsolë{}
var previousx int16 = 0
var previousy int16 = 0
var xPozicion int16 = 0
var yPozicion int16 = 0

func (vetvetja TEprezgjedhurMiuNgjarjehandler) OnMiuPoshtë(buton int8) {
	buffer := []byte("+")
	konsolë_2.MPrintoxy(buffer, uint16(previousx), uint16(previousy))
}
func (vetvetja TEprezgjedhurMiuNgjarjehandler) OnMiuSipër(buton int8)	{}
func (vetvetja TEprezgjedhurMiuNgjarjehandler) OnMiuLëviz(x int8, y int8) {

	xPozicion += int16(x)
	if xPozicion < 0 {
		xPozicion = 0
	}
	if xPozicion >= 80 {
		xPozicion = 79
	}

	yPozicion -= int16(y)

	if yPozicion < 0 {
		yPozicion = 0
	}
	if yPozicion >= 25 {
		yPozicion = 24
	}

	buffer := []byte(" ")
	konsolë_2.MPrintoxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	konsolë_2.MPrintoxy(buffer, uint16(xPozicion), uint16(yPozicion))

	previousx = xPozicion
	previousy = yPozicion
}

type TMiudriver struct {
	TInterrupthandler
}

var aktivMiudriver *TMiudriver
var interrupthandler func(uint32) uint32

var dataPorta_2 uint16 = 0x60
var urdhërPorta_2 uint16 = 0x64

const ps2PritKufi = 100000

func pritps2HyrjaBosh() bool {
	for i := 0; i < ps2PritKufi; i++ {
		if (PortaLeximibyte(urdhërPorta_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func pritps2outputIplotë() bool {
	for i := 0; i < ps2PritKufi; i++ {
		if (PortaLeximibyte(urdhërPorta_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func shkrimips2Urdhër(vlera uint8) bool {
	if !pritps2HyrjaBosh() {
		return false
	}
	PortaShkrimibyte(urdhërPorta_2, vlera)
	return true
}

func shkrimips2data(vlera uint8) bool {
	if !pritps2HyrjaBosh() {
		return false
	}
	PortaShkrimibyte(dataPorta_2, vlera)
	return true
}

func leximips2data() (uint8, bool) {
	if !pritps2outputIplotë() {
		return 0, false
	}
	return PortaLeximibyte(dataPorta_2), true
}

func dërgoMiuUrdhër(vlera uint8) bool {
	if !shkrimips2Urdhër(0xD4) || !shkrimips2data(vlera) {
		return false
	}
	ack, ok := leximips2data()
	return ok && ack == 0xFA
}

func (vetvetja *TMiudriver) Initdriver(manazhuesi *TInterruptManazhuesi, miuNgjarjehandler IMiuNgjarjehandler) {

	iMiuNgjarjehandler = TEprezgjedhurMiuNgjarjehandler{}

	if miuNgjarjehandler != nil {
		iMiuNgjarjehandler = miuNgjarjehandler
	}

	aktivMiudriver = vetvetja
	interrupthandler = handleMiuinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	vetvetja.Init(0x2C, uintptr(Pointer(manazhuesi)), address)

	for i := 0; i < 32 && (PortaLeximibyte(urdhërPorta_2)&0x01) != 0; i++ {
		PortaLeximibyte(dataPorta_2)
	}

	if !shkrimips2Urdhër(0xA8) || !shkrimips2Urdhër(0x20) {
		return
	}
	gjendja, ok := leximips2data()
	if !ok {
		return
	}
	gjendja |= 0x02
	gjendja &^= 0x20
	if !shkrimips2Urdhër(0x60) || !shkrimips2data(gjendja) {
		return
	}

	if !dërgoMiuUrdhër(0xF6) || !dërgoMiuUrdhër(0xF4) {
		return
	}
	offset = 0

}

func handleMiuinterrupt(esp uint32) uint32 {
	if aktivMiudriver == nil {
		PortaLeximibyte(dataPorta_2)
		return esp
	}
	return aktivMiudriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var buton_2 int8
var pendingx int16
var pendingy int16
var pendingButon int8
var pendingMiuNgjarje bool

func (vetvetja *TMiudriver) Handleinterrupt(esp uint32) uint32 {
	gjendja := PortaLeximibyte(urdhërPorta_2)
	if (gjendja&0x01) == 0 || (gjendja&0x20) == 0 {
		return esp
	}

	data := PortaLeximibyte(dataPorta_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetGjendja := uint8(buffer_2[0])

		if (packetGjendja & 0xC0) == 0 {
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
		pendingButon = int8(packetGjendja & 0x07)
		pendingMiuNgjarje = true
	}

	return esp

}

func ProçespendingMiuevents() {
	if iMiuNgjarjehandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingMiuNgjarje {
		Interruptaktiv()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	iRiButon := pendingButon
	oldButon := buton_2

	pendingx = 0
	pendingy = 0
	pendingMiuNgjarje = false
	Interruptaktiv()

	if x != 0 || y != 0 {
		iMiuNgjarjehandler.OnMiuLëviz(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (iRiButon & mask) != (oldButon & mask) {
			if (iRiButon & mask) != 0 {
				iMiuNgjarjehandler.OnMiuPoshtë(int8(i + 1))
			} else {
				iMiuNgjarjehandler.OnMiuSipër(int8(i + 1))
			}
		}
	}
	buton_2 = iRiButon
}
