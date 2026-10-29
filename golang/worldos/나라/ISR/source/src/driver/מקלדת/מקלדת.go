/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package מקלדת

import . "unsafe"

import . "שער"
import . "פסק"

import . "console"
import . "מערכתcall"

type Iמקלדתeventhandler interface {
	Oפעילמפתחלמטה(מפתח_2 byte)
	Oפעילמפתחמעלה(מפתח_2 byte)
}

var iמקלדתeventhandler Iמקלדתeventhandler
var ברירתמחדלמקלדתeventhandler Tברירתמחדלמקלדתeventhandler

type Tברירתמחדלמקלדתeventhandler struct {
}

func (self *Tברירתמחדלמקלדתeventhandler) Oפעילמפתחלמטה(מפתח_2 byte) {
	הקסדצימלי := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = הקסדצימלי[((מפתח_2 >> 4) & 0xF)]
	buffer[18] = הקסדצימלי[מפתח_2&0xF]

	console_2 := TConsole{}
	console_2.Mהדפסה(buffer)

}
func (self *Tברירתמחדלמקלדתeventhandler) Oפעילמפתחמעלה(מפתח_2 byte) {
}

type Tמקלדתdriver struct {
	Tפסקhandler
}

var פעילמקלדתdriver *Tמקלדתdriver
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

func (self *Tמקלדתdriver) Initdriver(manager *Tפסקmanager, מקלדתeventhandler Iמקלדתeventhandler) {

	iמקלדתeventhandler = &ברירתמחדלמקלדתeventhandler
	if מקלדתeventhandler != nil {
		iמקלדתeventhandler = מקלדתeventhandler
	}

	פעילמקלדתdriver = self
	פסקhandler = ידיתמקלדתפסק
	var address uintptr
	address = uintptr(Pointer(&פסקhandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Pשערקריאהbyte(פקודהשער_2)&0x01) != 0; i++ {
		Pשערקריאהbyte(dataשער_2)
	}

	if !כתיבהps2פקודה(0xAE) || !כתיבהps2פקודה(0x20) {
		return
	}
	מצב_2, אישור := קריאהps2data()
	if !אישור {
		return
	}
	מצב_2 |= 0x01
	מצב_2 &^= 0x10
	if !כתיבהps2פקודה(0x60) || !כתיבהps2data(מצב_2) {
		return
	}

	if !כתיבהps2data(0xF4) {
		return
	}
	ack, אישור := קריאהps2data()
	if !אישור || ack != 0xFA {
		return
	}

}

func ידיתמקלדתפסק(esp uint32) uint32 {
	if פעילמקלדתdriver == nil {
		Pשערקריאהbyte(dataשער_2)
		return esp
	}
	return פעילמקלדתdriver.Hידיתפסק(esp)
}

const מקלדתqueueגודל = 64

var מקלדתqueue [מקלדתqueueגודל]byte
var מקלדתqueueקריאה uint8
var מקלדתqueueכתיבה uint8
var שמאלshift bool
var ימיןshift bool
var extendedסרוקcode bool

func queueמקלדתbyte(מפתח_2 byte) {
	הבא := (מקלדתqueueכתיבה + 1) % מקלדתqueueגודל
	if הבא == מקלדתqueueקריאה {
		return
	}
	מקלדתqueue[מקלדתqueueכתיבה] = מפתח_2
	מקלדתqueueכתיבה = הבא
}

func Pתהליךpendingמקלדתאירועים() {
	for מקלדתqueueקריאה != מקלדתqueueכתיבה {
		מפתח_2 := מקלדתqueue[מקלדתqueueקריאה]
		מקלדתqueueקריאה = (מקלדתqueueקריאה + 1) % מקלדתqueueגודל
		Stdinputbyte(מפתח_2)
		if iמקלדתeventhandler != nil {
			iמקלדתeventhandler.Oפעילמפתחלמטה(מפתח_2)
		}
	}
}

func סרוקcodetobyte(סרוקcode uint8) (byte, bool) {
	shift := שמאלshift || ימיןshift

	if סרוקcode >= 0x02 && סרוקcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[סרוקcode-0x02], true
		}
		return "1234567890"[סרוקcode-0x02], true
	}
	if סרוקcode >= 0x10 && סרוקcode <= 0x19 {
		מפתח_2 := "qwertyuiop"[סרוקcode-0x10]
		if shift {
			מפתח_2 -= 'a' - 'A'
		}
		return מפתח_2, true
	}
	if סרוקcode >= 0x1E && סרוקcode <= 0x26 {
		מפתח_2 := "asdfghjkl"[סרוקcode-0x1E]
		if shift {
			מפתח_2 -= 'a' - 'A'
		}
		return מפתח_2, true
	}
	if סרוקcode >= 0x2C && סרוקcode <= 0x32 {
		מפתח_2 := "zxcvbnm"[סרוקcode-0x2C]
		if shift {
			מפתח_2 -= 'a' - 'A'
		}
		return מפתח_2, true
	}

	switch סרוקcode {
	case 0x0C:
		if shift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (self *Tמקלדתdriver) Hידיתפסק(esp uint32) uint32 {
	מצב_2 := Pשערקריאהbyte(פקודהשער_2)
	if (מצב_2&0x01) == 0 || (מצב_2&0x20) != 0 {
		return esp
	}

	סרוקcode := Pשערקריאהbyte(dataשער_2)
	if סרוקcode == 0xE0 {
		extendedסרוקcode = true
		return esp
	}
	if extendedסרוקcode {
		extendedסרוקcode = false
		return esp
	}

	released := (סרוקcode & 0x80) != 0
	basecode := סרוקcode & 0x7F
	if basecode == 0x2A {
		שמאלshift = !released
		return esp
	}
	if basecode == 0x36 {
		ימיןshift = !released
		return esp
	}
	if released {
		return esp
	}

	if מפתח_2, אישור := סרוקcodetobyte(basecode); אישור {
		queueמקלדתbyte(מפתח_2)
	}

	return esp
}
