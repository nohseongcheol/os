/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ստեղնաշար

import . "unsafe"

import . "պորտ"
import . "ընդհատել"
import . "console"

type IՄկնիկeventhandler interface {
	ՄիացնելՄկնիկՆերքև(button int8)
	ՄիացնելՄկնիկՎերև(button int8)
	ՄիացնելՄկնիկՏեղաշարժել(x int8, y int8)
}

var iՄկնիկeventhandler IՄկնիկeventhandler

type TՀիմնականՄկնիկeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xԴիրք int16 = 0
var yԴիրք int16 = 0

func (ինքնուրույն TՀիմնականՄկնիկeventhandler) ՄիացնելՄկնիկՆերքև(button int8) {
	buffer := []byte("+")
	console_2.MՏպելxy(buffer, uint16(previousx), uint16(previousy))
}
func (ինքնուրույն TՀիմնականՄկնիկeventhandler) ՄիացնելՄկնիկՎերև(button int8)	{}
func (ինքնուրույն TՀիմնականՄկնիկeventhandler) ՄիացնելՄկնիկՏեղաշարժել(x int8, y int8) {

	xԴիրք += int16(x)
	if xԴիրք < 0 {
		xԴիրք = 0
	}
	if xԴիրք >= 80 {
		xԴիրք = 79
	}

	yԴիրք -= int16(y)

	if yԴիրք < 0 {
		yԴիրք = 0
	}
	if yԴիրք >= 25 {
		yԴիրք = 24
	}

	buffer := []byte(" ")
	console_2.MՏպելxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MՏպելxy(buffer, uint16(xԴիրք), uint16(yԴիրք))

	previousx = xԴիրք
	previousy = yԴիրք
}

type TՄկնիկdriver struct {
	TԸնդհատելhandler
}

var ակտիվՄկնիկdriver *TՄկնիկdriver
var ընդհատելhandler func(uint32) uint32

var dataՊորտ_2 uint16 = 0x60
var հրահանգՊորտ_2 uint16 = 0x64

const ps2Սպասելlimit = 100000

func սպասելps2ՀիմաԴատարկ() bool {
	for i := 0; i < ps2Սպասելlimit; i++ {
		if (ՊորտԸնթերցումbyte(հրահանգՊորտ_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func սպասելps2ԵլքԼրիվ() bool {
	for i := 0; i < ps2Սպասելlimit; i++ {
		if (ՊորտԸնթերցումbyte(հրահանգՊորտ_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func գրելps2Հրահանգ(արժեք uint8) bool {
	if !սպասելps2ՀիմաԴատարկ() {
		return false
	}
	ՊորտԳրելbyte(հրահանգՊորտ_2, արժեք)
	return true
}

func գրելps2data(արժեք uint8) bool {
	if !սպասելps2ՀիմաԴատարկ() {
		return false
	}
	ՊորտԳրելbyte(dataՊորտ_2, արժեք)
	return true
}

func ընթերցումps2data() (uint8, bool) {
	if !սպասելps2ԵլքԼրիվ() {
		return 0, false
	}
	return ՊորտԸնթերցումbyte(dataՊորտ_2), true
}

func ոՒղարկելՄկնիկՀրահանգ(արժեք uint8) bool {
	if !գրելps2Հրահանգ(0xD4) || !գրելps2data(արժեք) {
		return false
	}
	ack, ok := ընթերցումps2data()
	return ok && ack == 0xFA
}

func (ինքնուրույն *TՄկնիկdriver) Initdriver(manager *TԸնդհատելmanager, մկնիկeventhandler IՄկնիկeventhandler) {

	iՄկնիկeventhandler = TՀիմնականՄկնիկeventhandler{}

	if մկնիկeventhandler != nil {
		iՄկնիկeventhandler = մկնիկeventhandler
	}

	ակտիվՄկնիկdriver = ինքնուրույն
	ընդհատելhandler = handleՄկնիկԸնդհատել
	var address uintptr
	address = uintptr(Pointer(&ընդհատելhandler))
	ինքնուրույն.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ՊորտԸնթերցումbyte(հրահանգՊորտ_2)&0x01) != 0; i++ {
		ՊորտԸնթերցումbyte(dataՊորտ_2)
	}

	if !գրելps2Հրահանգ(0xA8) || !գրելps2Հրահանգ(0x20) {
		return
	}
	կարգավիճակ, ok := ընթերցումps2data()
	if !ok {
		return
	}
	կարգավիճակ |= 0x02
	կարգավիճակ &^= 0x20
	if !գրելps2Հրահանգ(0x60) || !գրելps2data(կարգավիճակ) {
		return
	}

	if !ոՒղարկելՄկնիկՀրահանգ(0xF6) || !ոՒղարկելՄկնիկՀրահանգ(0xF4) {
		return
	}
	offset = 0

}

func handleՄկնիկԸնդհատել(esp uint32) uint32 {
	if ակտիվՄկնիկdriver == nil {
		ՊորտԸնթերցումbyte(dataՊորտ_2)
		return esp
	}
	return ակտիվՄկնիկdriver.HandleԸնդհատել(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingՄկնիկevent bool

func (ինքնուրույն *TՄկնիկdriver) HandleԸնդհատել(esp uint32) uint32 {
	կարգավիճակ := ՊորտԸնթերցումbyte(հրահանգՊորտ_2)
	if (կարգավիճակ&0x01) == 0 || (կարգավիճակ&0x20) == 0 {
		return esp
	}

	data := ՊորտԸնթերցումbyte(dataՊորտ_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetԿարգավիճակ := uint8(buffer_2[0])

		if (packetԿարգավիճակ & 0xC0) == 0 {
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
		pendingbutton = int8(packetԿարգավիճակ & 0x07)
		pendingՄկնիկevent = true
	}

	return esp

}

func ԳործընթացpendingՄկնիկevents() {
	if iՄկնիկeventhandler == nil {
		return
	}

	Ընդհատելdeactive()
	if !pendingՄկնիկevent {
		ԸնդհատելԱկտիվ()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	նորbutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingՄկնիկevent = false
	ԸնդհատելԱկտիվ()

	if x != 0 || y != 0 {
		iՄկնիկeventhandler.ՄիացնելՄկնիկՏեղաշարժել(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (նորbutton & mask) != (oldbutton & mask) {
			if (նորbutton & mask) != 0 {
				iՄկնիկeventhandler.ՄիացնելՄկնիկՆերքև(int8(i + 1))
			} else {
				iՄկնիկeventhandler.ՄիացնելՄկնիկՎերև(int8(i + 1))
			}
		}
	}
	button_2 = նորbutton
}
