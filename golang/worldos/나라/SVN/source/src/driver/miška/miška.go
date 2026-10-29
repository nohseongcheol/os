/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tipkovnica

import . "unsafe"

import . "vrata"
import . "prekinitev"
import . "console"

type IMiškaeventhandler interface {
	VključenoMiškaDol(gumb int8)
	VključenoMiškaGor(gumb int8)
	VključenoMiškaPremakni(x int8, y int8)
}

var iMiškaeventhandler IMiškaeventhandler

type TPrivzetoMiškaeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPoložaj int16 = 0
var yPoložaj int16 = 0

func (sam TPrivzetoMiškaeventhandler) VključenoMiškaDol(gumb int8) {
	buffer := []byte("+")
	console_2.MNatisnixy(buffer, uint16(previousx), uint16(previousy))
}
func (sam TPrivzetoMiškaeventhandler) VključenoMiškaGor(gumb int8)	{}
func (sam TPrivzetoMiškaeventhandler) VključenoMiškaPremakni(x int8, y int8) {

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
	console_2.MNatisnixy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MNatisnixy(buffer, uint16(xPoložaj), uint16(yPoložaj))

	previousx = xPoložaj
	previousy = yPoložaj
}

type TMiškadriver struct {
	TPrekinitevhandler
}

var dejavenMiškadriver *TMiškadriver
var prekinitevhandler func(uint32) uint32

var dataVrata_2 uint16 = 0x60
var ukazVrata_2 uint16 = 0x64

const ps2Počakajlimit = 100000

func počakajps2VhodPrazno() bool {
	for i := 0; i < ps2Počakajlimit; i++ {
		if (VrataBranjebyte(ukazVrata_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func počakajps2IzhodPolno() bool {
	for i := 0; i < ps2Počakajlimit; i++ {
		if (VrataBranjebyte(ukazVrata_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func pisanjeps2Ukaz(vrednost uint8) bool {
	if !počakajps2VhodPrazno() {
		return false
	}
	VrataPisanjebyte(ukazVrata_2, vrednost)
	return true
}

func pisanjeps2data(vrednost uint8) bool {
	if !počakajps2VhodPrazno() {
		return false
	}
	VrataPisanjebyte(dataVrata_2, vrednost)
	return true
}

func branjeps2data() (uint8, bool) {
	if !počakajps2IzhodPolno() {
		return 0, false
	}
	return VrataBranjebyte(dataVrata_2), true
}

func pošljiMiškaUkaz(vrednost uint8) bool {
	if !pisanjeps2Ukaz(0xD4) || !pisanjeps2data(vrednost) {
		return false
	}
	ack, vredu := branjeps2data()
	return vredu && ack == 0xFA
}

func (sam *TMiškadriver) Initdriver(manager *TPrekinitevmanager, miškaeventhandler IMiškaeventhandler) {

	iMiškaeventhandler = TPrivzetoMiškaeventhandler{}

	if miškaeventhandler != nil {
		iMiškaeventhandler = miškaeventhandler
	}

	dejavenMiškadriver = sam
	prekinitevhandler = ročicaMiškaPrekinitev
	var address uintptr
	address = uintptr(Pointer(&prekinitevhandler))
	sam.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (VrataBranjebyte(ukazVrata_2)&0x01) != 0; i++ {
		VrataBranjebyte(dataVrata_2)
	}

	if !pisanjeps2Ukaz(0xA8) || !pisanjeps2Ukaz(0x20) {
		return
	}
	stanje, vredu := branjeps2data()
	if !vredu {
		return
	}
	stanje |= 0x02
	stanje &^= 0x20
	if !pisanjeps2Ukaz(0x60) || !pisanjeps2data(stanje) {
		return
	}

	if !pošljiMiškaUkaz(0xF6) || !pošljiMiškaUkaz(0xF4) {
		return
	}
	offset = 0

}

func ročicaMiškaPrekinitev(esp uint32) uint32 {
	if dejavenMiškadriver == nil {
		VrataBranjebyte(dataVrata_2)
		return esp
	}
	return dejavenMiškadriver.RočicaPrekinitev(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var gumb_2 int8
var pendingx int16
var pendingy int16
var pendingGumb int8
var pendingMiškaevent bool

func (sam *TMiškadriver) RočicaPrekinitev(esp uint32) uint32 {
	stanje := VrataBranjebyte(ukazVrata_2)
	if (stanje&0x01) == 0 || (stanje&0x20) == 0 {
		return esp
	}

	data := VrataBranjebyte(dataVrata_2)

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
		pendingGumb = int8(packetStanje & 0x07)
		pendingMiškaevent = true
	}

	return esp

}

func OpravilopendingMiškaDogodki() {
	if iMiškaeventhandler == nil {
		return
	}

	Prekinitevdeactive()
	if !pendingMiškaevent {
		PrekinitevDejaven()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	novaGumb := pendingGumb
	oldGumb := gumb_2

	pendingx = 0
	pendingy = 0
	pendingMiškaevent = false
	PrekinitevDejaven()

	if x != 0 || y != 0 {
		iMiškaeventhandler.VključenoMiškaPremakni(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		maska := int8(0x1 << i)
		if (novaGumb & maska) != (oldGumb & maska) {
			if (novaGumb & maska) != 0 {
				iMiškaeventhandler.VključenoMiškaDol(int8(i + 1))
			} else {
				iMiškaeventhandler.VključenoMiškaGor(int8(i + 1))
			}
		}
	}
	gumb_2 = novaGumb
}
