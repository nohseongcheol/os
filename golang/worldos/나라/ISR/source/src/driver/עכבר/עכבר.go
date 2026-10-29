/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package מקלדת

import . "unsafe"

import . "שער"
import . "פסק"
import . "console"

type Iעכברeventhandler interface {
	Oפעילעכברלמטה(לחצן int8)
	Oפעילעכברמעלה(לחצן int8)
	Oפעילעכברהזז(x int8, y int8)
}

var iעכברeventhandler Iעכברeventhandler

type Tברירתמחדלעכברeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xמיקום int16 = 0
var yמיקום int16 = 0

func (self Tברירתמחדלעכברeventhandler) Oפעילעכברלמטה(לחצן int8) {
	buffer := []byte("+")
	console_2.Mהדפסהxy(buffer, uint16(previousx), uint16(previousy))
}
func (self Tברירתמחדלעכברeventhandler) Oפעילעכברמעלה(לחצן int8)	{}
func (self Tברירתמחדלעכברeventhandler) Oפעילעכברהזז(x int8, y int8) {

	xמיקום += int16(x)
	if xמיקום < 0 {
		xמיקום = 0
	}
	if xמיקום >= 80 {
		xמיקום = 79
	}

	yמיקום -= int16(y)

	if yמיקום < 0 {
		yמיקום = 0
	}
	if yמיקום >= 25 {
		yמיקום = 24
	}

	buffer := []byte(" ")
	console_2.Mהדפסהxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.Mהדפסהxy(buffer, uint16(xמיקום), uint16(yמיקום))

	previousx = xמיקום
	previousy = yמיקום
}

type Tעכברdriver struct {
	Tפסקhandler
}

var פעילעכברdriver *Tעכברdriver
var פסקhandler func(uint32) uint32

var dataשער_2 uint16 = 0x60
var פקודהשער_2 uint16 = 0x64

const ps2המתנהlimit = 100000

func המתנהps2קלטריק() bool {
	for i := 0; i < ps2המתנהlimit; i++ {
		if (Pשערקריאהbyte(פקודהשער_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func המתנהps2פלטמלא() bool {
	for i := 0; i < ps2המתנהlimit; i++ {
		if (Pשערקריאהbyte(פקודהשער_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func כתיבהps2פקודה(ערך uint8) bool {
	if !המתנהps2קלטריק() {
		return false
	}
	Pשערכתיבהbyte(פקודהשער_2, ערך)
	return true
}

func כתיבהps2data(ערך uint8) bool {
	if !המתנהps2קלטריק() {
		return false
	}
	Pשערכתיבהbyte(dataשער_2, ערך)
	return true
}

func קריאהps2data() (uint8, bool) {
	if !המתנהps2פלטמלא() {
		return 0, false
	}
	return Pשערקריאהbyte(dataשער_2), true
}

func שלחעכברפקודה(ערך uint8) bool {
	if !כתיבהps2פקודה(0xD4) || !כתיבהps2data(ערך) {
		return false
	}
	ack, אישור := קריאהps2data()
	return אישור && ack == 0xFA
}

func (self *Tעכברdriver) Initdriver(manager *Tפסקmanager, עכברeventhandler Iעכברeventhandler) {

	iעכברeventhandler = Tברירתמחדלעכברeventhandler{}

	if עכברeventhandler != nil {
		iעכברeventhandler = עכברeventhandler
	}

	פעילעכברdriver = self
	פסקhandler = ידיתעכברפסק
	var address uintptr
	address = uintptr(Pointer(&פסקhandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Pשערקריאהbyte(פקודהשער_2)&0x01) != 0; i++ {
		Pשערקריאהbyte(dataשער_2)
	}

	if !כתיבהps2פקודה(0xA8) || !כתיבהps2פקודה(0x20) {
		return
	}
	מצב_2, אישור := קריאהps2data()
	if !אישור {
		return
	}
	מצב_2 |= 0x02
	מצב_2 &^= 0x20
	if !כתיבהps2פקודה(0x60) || !כתיבהps2data(מצב_2) {
		return
	}

	if !שלחעכברפקודה(0xF6) || !שלחעכברפקודה(0xF4) {
		return
	}
	offset = 0

}

func ידיתעכברפסק(esp uint32) uint32 {
	if פעילעכברdriver == nil {
		Pשערקריאהbyte(dataשער_2)
		return esp
	}
	return פעילעכברdriver.Hידיתפסק(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var לחצן_2 int8
var pendingx int16
var pendingy int16
var pendingלחצן int8
var pendingעכברevent bool

func (self *Tעכברdriver) Hידיתפסק(esp uint32) uint32 {
	מצב_2 := Pשערקריאהbyte(פקודהשער_2)
	if (מצב_2&0x01) == 0 || (מצב_2&0x20) == 0 {
		return esp
	}

	data := Pשערקריאהbyte(dataשער_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetמצב := uint8(buffer_2[0])

		if (packetמצב & 0xC0) == 0 {
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
		pendingלחצן = int8(packetמצב & 0x07)
		pendingעכברevent = true
	}

	return esp

}

func Pתהליךpendingעכבראירועים() {
	if iעכברeventhandler == nil {
		return
	}

	Iפסקdeactive()
	if !pendingעכברevent {
		Iפסקפעיל()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	חדשלחצן := pendingלחצן
	oldלחצן := לחצן_2

	pendingx = 0
	pendingy = 0
	pendingעכברevent = false
	Iפסקפעיל()

	if x != 0 || y != 0 {
		iעכברeventhandler.Oפעילעכברהזז(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		סינון := int8(0x1 << i)
		if (חדשלחצן & סינון) != (oldלחצן & סינון) {
			if (חדשלחצן & סינון) != 0 {
				iעכברeventhandler.Oפעילעכברלמטה(int8(i + 1))
			} else {
				iעכברeventhandler.Oפעילעכברמעלה(int8(i + 1))
			}
		}
	}
	לחצן_2 = חדשלחצן
}
