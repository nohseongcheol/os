package toetsenbord

import . "unsafe"

import . "poort"
import . "interrupt"
import . "console"

type IMuisGebeurtenishandler interface {
	AanMuisOmlaag(knop int8)
	AanMuisOmhoog(knop int8)
	AanMuisVerplaatsen(x int8, y int8)
}

var iMuisGebeurtenishandler IMuisGebeurtenishandler

type TStandaardMuisGebeurtenishandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPositie int16 = 0
var yPositie int16 = 0

func (zelf TStandaardMuisGebeurtenishandler) AanMuisOmlaag(knop int8) {
	buffer := []byte("+")
	console_2.MAfdrukkenxy(buffer, uint16(previousx), uint16(previousy))
}
func (zelf TStandaardMuisGebeurtenishandler) AanMuisOmhoog(knop int8)	{}
func (zelf TStandaardMuisGebeurtenishandler) AanMuisVerplaatsen(x int8, y int8) {

	xPositie += int16(x)
	if xPositie < 0 {
		xPositie = 0
	}
	if xPositie >= 80 {
		xPositie = 79
	}

	yPositie -= int16(y)

	if yPositie < 0 {
		yPositie = 0
	}
	if yPositie >= 25 {
		yPositie = 24
	}

	buffer := []byte(" ")
	console_2.MAfdrukkenxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MAfdrukkenxy(buffer, uint16(xPositie), uint16(yPositie))

	previousx = xPositie
	previousy = yPositie
}

type TMuisdriver struct {
	TInterrupthandler
}

var actiefMuisdriver *TMuisdriver
var interrupthandler func(uint32) uint32

var dataPoort_2 uint16 = 0x60
var opdrachtPoort_2 uint16 = 0x64

const ps2WachtenBeperken = 100000

func wachtenps2InvoerLeeg() bool {
	for i := 0; i < ps2WachtenBeperken; i++ {
		if (PoortLezenbyte(opdrachtPoort_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func wachtenps2UitvoerVolledig() bool {
	for i := 0; i < ps2WachtenBeperken; i++ {
		if (PoortLezenbyte(opdrachtPoort_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func schrijvenps2Opdracht(waarde uint8) bool {
	if !wachtenps2InvoerLeeg() {
		return false
	}
	PoortSchrijvenbyte(opdrachtPoort_2, waarde)
	return true
}

func schrijvenps2data(waarde uint8) bool {
	if !wachtenps2InvoerLeeg() {
		return false
	}
	PoortSchrijvenbyte(dataPoort_2, waarde)
	return true
}

func lezenps2data() (uint8, bool) {
	if !wachtenps2UitvoerVolledig() {
		return 0, false
	}
	return PoortLezenbyte(dataPoort_2), true
}

func verzendenMuisOpdracht(waarde uint8) bool {
	if !schrijvenps2Opdracht(0xD4) || !schrijvenps2data(waarde) {
		return false
	}
	ack, ok := lezenps2data()
	return ok && ack == 0xFA
}

func (zelf *TMuisdriver) Initdriver(manager *TInterruptmanager, muisGebeurtenishandler IMuisGebeurtenishandler) {

	iMuisGebeurtenishandler = TStandaardMuisGebeurtenishandler{}

	if muisGebeurtenishandler != nil {
		iMuisGebeurtenishandler = muisGebeurtenishandler
	}

	actiefMuisdriver = zelf
	interrupthandler = handgreepMuisinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	zelf.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PoortLezenbyte(opdrachtPoort_2)&0x01) != 0; i++ {
		PoortLezenbyte(dataPoort_2)
	}

	if !schrijvenps2Opdracht(0xA8) || !schrijvenps2Opdracht(0x20) {
		return
	}
	status, ok := lezenps2data()
	if !ok {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !schrijvenps2Opdracht(0x60) || !schrijvenps2data(status) {
		return
	}

	if !verzendenMuisOpdracht(0xF6) || !verzendenMuisOpdracht(0xF4) {
		return
	}
	verschuiving = 0

}

func handgreepMuisinterrupt(esp uint32) uint32 {
	if actiefMuisdriver == nil {
		PoortLezenbyte(dataPoort_2)
		return esp
	}
	return actiefMuisdriver.Handgreepinterrupt(esp)
}

var aantal uint8 = 0
var buffer_2 [3]int8
var verschuiving uint8 = 0

var knop_2 int8
var pendingx int16
var pendingy int16
var pendingKnop int8
var pendingMuisGebeurtenis bool

func (zelf *TMuisdriver) Handgreepinterrupt(esp uint32) uint32 {
	status := PoortLezenbyte(opdrachtPoort_2)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	data := PoortLezenbyte(dataPoort_2)

	if verschuiving == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[verschuiving] = int8(data)
	verschuiving = (verschuiving + 1) % 3
	if verschuiving == 0 {
		pAKKETstatus := uint8(buffer_2[0])

		if (pAKKETstatus & 0xC0) == 0 {
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
		pendingKnop = int8(pAKKETstatus & 0x07)
		pendingMuisGebeurtenis = true
	}

	return esp

}

func ProcespendingMuisGebeurtenissen() {
	if iMuisGebeurtenishandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingMuisGebeurtenis {
		InterruptActief()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	nieuwKnop := pendingKnop
	oudKnop := knop_2

	pendingx = 0
	pendingy = 0
	pendingMuisGebeurtenis = false
	InterruptActief()

	if x != 0 || y != 0 {
		iMuisGebeurtenishandler.AanMuisVerplaatsen(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		masker := int8(0x1 << i)
		if (nieuwKnop & masker) != (oudKnop & masker) {
			if (nieuwKnop & masker) != 0 {
				iMuisGebeurtenishandler.AanMuisOmlaag(int8(i + 1))
			} else {
				iMuisGebeurtenishandler.AanMuisOmhoog(int8(i + 1))
			}
		}
	}
	knop_2 = nieuwKnop
}
