package tastatura

import . "unsafe"

import . "port"
import . "interrupt"
import . "console"

type IMiševenthandler interface {
	UključenMišdown(button int8)
	UključenMišGore(button int8)
	UključenMišPremjesti(x int8, y int8)
}

var iMiševenthandler IMiševenthandler

type TUobičajenoMiševenthandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xpoložaj int16 = 0
var ypoložaj int16 = 0

func (self TUobičajenoMiševenthandler) UključenMišdown(button int8) {
	buffer := []byte("+")
	console_2.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TUobičajenoMiševenthandler) UključenMišGore(button int8)	{}
func (self TUobičajenoMiševenthandler) UključenMišPremjesti(x int8, y int8) {

	xpoložaj += int16(x)
	if xpoložaj < 0 {
		xpoložaj = 0
	}
	if xpoložaj >= 80 {
		xpoložaj = 79
	}

	ypoložaj -= int16(y)

	if ypoložaj < 0 {
		ypoložaj = 0
	}
	if ypoložaj >= 25 {
		ypoložaj = 24
	}

	buffer := []byte(" ")
	console_2.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MŠtampajxy(buffer, uint16(xpoložaj), uint16(ypoložaj))

	previousx = xpoložaj
	previousy = ypoložaj
}

type TMišdriver struct {
	TInterrupthandler
}

var activeMišdriver *TMišdriver
var interrupthandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var naredbaport_2 uint16 = 0x64

const ps2Sačekajlimit = 100000

func sačekajps2Ulazempty() bool {
	for i := 0; i < ps2Sačekajlimit; i++ {
		if (PortČitajbyte(naredbaport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func sačekajps2IzlazPotpuno() bool {
	for i := 0; i < ps2Sačekajlimit; i++ {
		if (PortČitajbyte(naredbaport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func pišips2Naredba(vrijednost uint8) bool {
	if !sačekajps2Ulazempty() {
		return false
	}
	PortPišibyte(naredbaport_2, vrijednost)
	return true
}

func pišips2data(vrijednost uint8) bool {
	if !sačekajps2Ulazempty() {
		return false
	}
	PortPišibyte(dataport_2, vrijednost)
	return true
}

func čitajps2data() (uint8, bool) {
	if !sačekajps2IzlazPotpuno() {
		return 0, false
	}
	return PortČitajbyte(dataport_2), true
}

func pošaljiMišNaredba(vrijednost uint8) bool {
	if !pišips2Naredba(0xD4) || !pišips2data(vrijednost) {
		return false
	}
	ack, uredu := čitajps2data()
	return uredu && ack == 0xFA
}

func (self *TMišdriver) Initdriver(manager *TInterruptmanager, miševenthandler IMiševenthandler) {

	iMiševenthandler = TUobičajenoMiševenthandler{}

	if miševenthandler != nil {
		iMiševenthandler = miševenthandler
	}

	activeMišdriver = self
	interrupthandler = handleMišinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortČitajbyte(naredbaport_2)&0x01) != 0; i++ {
		PortČitajbyte(dataport_2)
	}

	if !pišips2Naredba(0xA8) || !pišips2Naredba(0x20) {
		return
	}
	status, uredu := čitajps2data()
	if !uredu {
		return
	}
	status |= 0x02
	status &^= 0x20
	if !pišips2Naredba(0x60) || !pišips2data(status) {
		return
	}

	if !pošaljiMišNaredba(0xF6) || !pošaljiMišNaredba(0xF4) {
		return
	}
	offset = 0

}

func handleMišinterrupt(esp uint32) uint32 {
	if activeMišdriver == nil {
		PortČitajbyte(dataport_2)
		return esp
	}
	return activeMišdriver.Handleinterrupt(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingMiševent bool

func (self *TMišdriver) Handleinterrupt(esp uint32) uint32 {
	status := PortČitajbyte(naredbaport_2)
	if (status&0x01) == 0 || (status&0x20) == 0 {
		return esp
	}

	data := PortČitajbyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetstatus := uint8(buffer_2[0])

		if (packetstatus & 0xC0) == 0 {
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
		pendingbutton = int8(packetstatus & 0x07)
		pendingMiševent = true
	}

	return esp

}

func ProcesspendingMiševents() {
	if iMiševenthandler == nil {
		return
	}

	Interruptdeactive()
	if !pendingMiševent {
		Interruptactive()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	novabutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingMiševent = false
	Interruptactive()

	if x != 0 || y != 0 {
		iMiševenthandler.UključenMišPremjesti(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maska := int8(0x1 << i)
		if (novabutton & maska) != (oldbutton & maska) {
			if (novabutton & maska) != 0 {
				iMiševenthandler.UključenMišdown(int8(i + 1))
			} else {
				iMiševenthandler.UključenMišGore(int8(i + 1))
			}
		}
	}
	button_2 = novabutton
}
