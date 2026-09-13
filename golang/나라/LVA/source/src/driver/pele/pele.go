package klaviatūra

import . "unsafe"

import . "ports"
import . "pārtraukums"
import . "console"

type IPeleNotikumshandler interface {
	IeslēgtsPeleLejup(pogas int8)
	IeslēgtsPeleAugšup(pogas int8)
	IeslēgtsPelePārvietot(x int8, y int8)
}

var iPeleNotikumshandler IPeleNotikumshandler

type TNoklusētaisPeleNotikumshandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xNovietojums int16 = 0
var yNovietojums int16 = 0

func (pats TNoklusētaisPeleNotikumshandler) IeslēgtsPeleLejup(pogas int8) {
	buffer := []byte("+")
	console_2.MDrukātxy(buffer, uint16(previousx), uint16(previousy))
}
func (pats TNoklusētaisPeleNotikumshandler) IeslēgtsPeleAugšup(pogas int8)	{}
func (pats TNoklusētaisPeleNotikumshandler) IeslēgtsPelePārvietot(x int8, y int8) {

	xNovietojums += int16(x)
	if xNovietojums < 0 {
		xNovietojums = 0
	}
	if xNovietojums >= 80 {
		xNovietojums = 79
	}

	yNovietojums -= int16(y)

	if yNovietojums < 0 {
		yNovietojums = 0
	}
	if yNovietojums >= 25 {
		yNovietojums = 24
	}

	buffer := []byte(" ")
	console_2.MDrukātxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MDrukātxy(buffer, uint16(xNovietojums), uint16(yNovietojums))

	previousx = xNovietojums
	previousy = yNovietojums
}

type TPeledriver struct {
	TPārtraukumshandler
}

var aktīvsPeledriver *TPeledriver
var pārtraukumshandler func(uint32) uint32

var dataPorts_2 uint16 = 0x60
var komandaPorts_2 uint16 = 0x64

const ps2GaidītIerobežot = 100000

func gaidītps2IevadeTukšs() bool {
	for i := 0; i < ps2GaidītIerobežot; i++ {
		if (PortsLasītbyte(komandaPorts_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func gaidītps2IzvadePilns() bool {
	for i := 0; i < ps2GaidītIerobežot; i++ {
		if (PortsLasītbyte(komandaPorts_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func rakstītps2Komanda(vērtība uint8) bool {
	if !gaidītps2IevadeTukšs() {
		return false
	}
	PortsRakstītbyte(komandaPorts_2, vērtība)
	return true
}

func rakstītps2data(vērtība uint8) bool {
	if !gaidītps2IevadeTukšs() {
		return false
	}
	PortsRakstītbyte(dataPorts_2, vērtība)
	return true
}

func lasītps2data() (uint8, bool) {
	if !gaidītps2IzvadePilns() {
		return 0, false
	}
	return PortsLasītbyte(dataPorts_2), true
}

func sūtītPeleKomanda(vērtība uint8) bool {
	if !rakstītps2Komanda(0xD4) || !rakstītps2data(vērtība) {
		return false
	}
	ack, labi := lasītps2data()
	return labi && ack == 0xFA
}

func (pats *TPeledriver) Initdriver(manager *TPārtraukumsmanager, peleNotikumshandler IPeleNotikumshandler) {

	iPeleNotikumshandler = TNoklusētaisPeleNotikumshandler{}

	if peleNotikumshandler != nil {
		iPeleNotikumshandler = peleNotikumshandler
	}

	aktīvsPeledriver = pats
	pārtraukumshandler = handlePelePārtraukums
	var address uintptr
	address = uintptr(Pointer(&pārtraukumshandler))
	pats.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortsLasītbyte(komandaPorts_2)&0x01) != 0; i++ {
		PortsLasītbyte(dataPorts_2)
	}

	if !rakstītps2Komanda(0xA8) || !rakstītps2Komanda(0x20) {
		return
	}
	statuss, labi := lasītps2data()
	if !labi {
		return
	}
	statuss |= 0x02
	statuss &^= 0x20
	if !rakstītps2Komanda(0x60) || !rakstītps2data(statuss) {
		return
	}

	if !sūtītPeleKomanda(0xF6) || !sūtītPeleKomanda(0xF4) {
		return
	}
	offset = 0

}

func handlePelePārtraukums(esp uint32) uint32 {
	if aktīvsPeledriver == nil {
		PortsLasītbyte(dataPorts_2)
		return esp
	}
	return aktīvsPeledriver.HandlePārtraukums(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var pogas_2 int8
var pendingx int16
var pendingy int16
var pendingPogas int8
var pendingPeleNotikums bool

func (pats *TPeledriver) HandlePārtraukums(esp uint32) uint32 {
	statuss := PortsLasītbyte(komandaPorts_2)
	if (statuss&0x01) == 0 || (statuss&0x20) == 0 {
		return esp
	}

	data := PortsLasītbyte(dataPorts_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetStatuss := uint8(buffer_2[0])

		if (packetStatuss & 0xC0) == 0 {
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
		pendingPogas = int8(packetStatuss & 0x07)
		pendingPeleNotikums = true
	}

	return esp

}

func ProcesspendingPeleevents() {
	if iPeleNotikumshandler == nil {
		return
	}

	Pārtraukumsdeactive()
	if !pendingPeleNotikums {
		PārtraukumsAktīvs()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	jaunsPogas := pendingPogas
	oldPogas := pogas_2

	pendingx = 0
	pendingy = 0
	pendingPeleNotikums = false
	PārtraukumsAktīvs()

	if x != 0 || y != 0 {
		iPeleNotikumshandler.IeslēgtsPelePārvietot(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maska := int8(0x1 << i)
		if (jaunsPogas & maska) != (oldPogas & maska) {
			if (jaunsPogas & maska) != 0 {
				iPeleNotikumshandler.IeslēgtsPeleLejup(int8(i + 1))
			} else {
				iPeleNotikumshandler.IeslēgtsPeleAugšup(int8(i + 1))
			}
		}
	}
	pogas_2 = jaunsPogas
}
