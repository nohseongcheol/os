package tastatură

import . "unsafe"

import . "port"
import . "intrerupere"
import . "console"

type IMausEvenimenthandler interface {
	PornitMausÎnjos(buton int8)
	PornitMausSus(buton int8)
	PornitMausMutare(x int8, y int8)
}

var iMausEvenimenthandler IMausEvenimenthandler

type TImplicităMausEvenimenthandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPoziție int16 = 0
var yPoziție int16 = 0

func (sine TImplicităMausEvenimenthandler) PornitMausÎnjos(buton int8) {
	buffer := []byte("+")
	console_2.MTipăreștexy(buffer, uint16(previousx), uint16(previousy))
}
func (sine TImplicităMausEvenimenthandler) PornitMausSus(buton int8)	{}
func (sine TImplicităMausEvenimenthandler) PornitMausMutare(x int8, y int8) {

	xPoziție += int16(x)
	if xPoziție < 0 {
		xPoziție = 0
	}
	if xPoziție >= 80 {
		xPoziție = 79
	}

	yPoziție -= int16(y)

	if yPoziție < 0 {
		yPoziție = 0
	}
	if yPoziție >= 25 {
		yPoziție = 24
	}

	buffer := []byte(" ")
	console_2.MTipăreștexy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MTipăreștexy(buffer, uint16(xPoziție), uint16(yPoziție))

	previousx = xPoziție
	previousy = yPoziție
}

type TMausdriver struct {
	TIntreruperehandler
}

var activMausdriver *TMausdriver
var intreruperehandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var comandăport_2 uint16 = 0x64

const ps2AșteaptăLimită = 100000

func așteaptăps2IntroducețiGol() bool {
	for i := 0; i < ps2AșteaptăLimită; i++ {
		if (PortCitirebyte(comandăport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func așteaptăps2RezultatComplet() bool {
	for i := 0; i < ps2AșteaptăLimită; i++ {
		if (PortCitirebyte(comandăport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func scriereps2Comandă(valoare uint8) bool {
	if !așteaptăps2IntroducețiGol() {
		return false
	}
	PortScrierebyte(comandăport_2, valoare)
	return true
}

func scriereps2data(valoare uint8) bool {
	if !așteaptăps2IntroducețiGol() {
		return false
	}
	PortScrierebyte(dataport_2, valoare)
	return true
}

func citireps2data() (uint8, bool) {
	if !așteaptăps2RezultatComplet() {
		return 0, false
	}
	return PortCitirebyte(dataport_2), true
}

func trimiteMausComandă(valoare uint8) bool {
	if !scriereps2Comandă(0xD4) || !scriereps2data(valoare) {
		return false
	}
	ack, ok := citireps2data()
	return ok && ack == 0xFA
}

func (sine *TMausdriver) Initdriver(manager *TIntreruperemanager, mausEvenimenthandler IMausEvenimenthandler) {

	iMausEvenimenthandler = TImplicităMausEvenimenthandler{}

	if mausEvenimenthandler != nil {
		iMausEvenimenthandler = mausEvenimenthandler
	}

	activMausdriver = sine
	intreruperehandler = mânerMausIntrerupere
	var address uintptr
	address = uintptr(Pointer(&intreruperehandler))
	sine.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortCitirebyte(comandăport_2)&0x01) != 0; i++ {
		PortCitirebyte(dataport_2)
	}

	if !scriereps2Comandă(0xA8) || !scriereps2Comandă(0x20) {
		return
	}
	stare, ok := citireps2data()
	if !ok {
		return
	}
	stare |= 0x02
	stare &^= 0x20
	if !scriereps2Comandă(0x60) || !scriereps2data(stare) {
		return
	}

	if !trimiteMausComandă(0xF6) || !trimiteMausComandă(0xF4) {
		return
	}
	offset = 0

}

func mânerMausIntrerupere(esp uint32) uint32 {
	if activMausdriver == nil {
		PortCitirebyte(dataport_2)
		return esp
	}
	return activMausdriver.MânerIntrerupere(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var buton_2 int8
var pendingx int16
var pendingy int16
var pendingButon int8
var pendingMausEveniment bool

func (sine *TMausdriver) MânerIntrerupere(esp uint32) uint32 {
	stare := PortCitirebyte(comandăport_2)
	if (stare&0x01) == 0 || (stare&0x20) == 0 {
		return esp
	}

	data := PortCitirebyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetStare := uint8(buffer_2[0])

		if (packetStare & 0xC0) == 0 {
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
		pendingButon = int8(packetStare & 0x07)
		pendingMausEveniment = true
	}

	return esp

}

func ProcespendingMausevents() {
	if iMausEvenimenthandler == nil {
		return
	}

	Intreruperedeactive()
	if !pendingMausEveniment {
		IntrerupereActiv()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	nouButon := pendingButon
	oldButon := buton_2

	pendingx = 0
	pendingy = 0
	pendingMausEveniment = false
	IntrerupereActiv()

	if x != 0 || y != 0 {
		iMausEvenimenthandler.PornitMausMutare(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		masca := int8(0x1 << i)
		if (nouButon & masca) != (oldButon & masca) {
			if (nouButon & masca) != 0 {
				iMausEvenimenthandler.PornitMausÎnjos(int8(i + 1))
			} else {
				iMausEvenimenthandler.PornitMausSus(int8(i + 1))
			}
		}
	}
	buton_2 = nouButon
}
