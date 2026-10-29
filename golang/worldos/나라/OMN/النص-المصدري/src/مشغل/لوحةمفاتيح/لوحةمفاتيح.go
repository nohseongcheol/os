/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package لوحةمفاتيح

import . "unsafe"

import . "منفذ"
import . "مقاطعة"

import . "طرفية"
import . "نظامنداء"

type Iلوحةمفاتيححدثhandler interface {
	Oعندمفتاحأسفل(مفتاح byte)
	Oعندمفتاحأعلى(مفتاح byte)
}

var iلوحةمفاتيححدثhandler Iلوحةمفاتيححدثhandler
var الافتراضيلوحةمفاتيححدثhandler Tالافتراضيلوحةمفاتيححدثhandler

type Tالافتراضيلوحةمفاتيححدثhandler struct {
}

func (نفسه *Tالافتراضيلوحةمفاتيححدثhandler) Oعندمفتاحأسفل(مفتاح byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((مفتاح >> 4) & 0xF)]
	buffer[18] = hex[مفتاح&0xF]

	طرفية_2 := Tطرفية{}
	طرفية_2.Mاطبع(buffer)

}
func (نفسه *Tالافتراضيلوحةمفاتيححدثhandler) Oعندمفتاحأعلى(مفتاح byte) {
}

type Tلوحةمفاتيحمشغل struct {
	Tمقاطعةhandler
}

var نشطلوحةمفاتيحمشغل *Tلوحةمفاتيحمشغل
var مقاطعةhandler func(uint32) uint32

var بياناتمنفذ_2 uint16 = 0x60
var أمرمنفذ_2 uint16 = 0x64

const ps2انتظرتحديد = 100000

func انتظرps2دخلفارغ() bool {
	for i := 0; i < ps2انتظرتحديد; i++ {
		if (Pمنفذقراءةبايت(أمرمنفذ_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func انتظرps2الخرجكامل() bool {
	for i := 0; i < ps2انتظرتحديد; i++ {
		if (Pمنفذقراءةبايت(أمرمنفذ_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func كتابةps2أمر(القيمة uint8) bool {
	if !انتظرps2دخلفارغ() {
		return false
	}
	Pمنفذكتابةبايت(أمرمنفذ_2, القيمة)
	return true
}

func كتابةps2بيانات(القيمة uint8) bool {
	if !انتظرps2دخلفارغ() {
		return false
	}
	Pمنفذكتابةبايت(بياناتمنفذ_2, القيمة)
	return true
}

func قراءةps2بيانات() (uint8, bool) {
	if !انتظرps2الخرجكامل() {
		return 0, false
	}
	return Pمنفذقراءةبايت(بياناتمنفذ_2), true
}

func (نفسه *Tلوحةمفاتيحمشغل) Initمشغل(مدير *Tمقاطعةمدير, لوحةمفاتيححدثhandler Iلوحةمفاتيححدثhandler) {

	iلوحةمفاتيححدثhandler = &الافتراضيلوحةمفاتيححدثhandler
	if لوحةمفاتيححدثhandler != nil {
		iلوحةمفاتيححدثhandler = لوحةمفاتيححدثhandler
	}

	نشطلوحةمفاتيحمشغل = نفسه
	مقاطعةhandler = التعامللوحةمفاتيحمقاطعة
	var address uintptr
	address = uintptr(Pointer(&مقاطعةhandler))

	نفسه.Init(0x21, uintptr(Pointer(مدير)), address)

	for i := 0; i < 32 && (Pمنفذقراءةبايت(أمرمنفذ_2)&0x01) != 0; i++ {
		Pمنفذقراءةبايت(بياناتمنفذ_2)
	}

	if !كتابةps2أمر(0xAE) || !كتابةps2أمر(0x20) {
		return
	}
	الحالة, موافق := قراءةps2بيانات()
	if !موافق {
		return
	}
	الحالة |= 0x01
	الحالة &^= 0x10
	if !كتابةps2أمر(0x60) || !كتابةps2بيانات(الحالة) {
		return
	}

	if !كتابةps2بيانات(0xF4) {
		return
	}
	ack, موافق := قراءةps2بيانات()
	if !موافق || ack != 0xFA {
		return
	}

}

func التعامللوحةمفاتيحمقاطعة(esp uint32) uint32 {
	if نشطلوحةمفاتيحمشغل == nil {
		Pمنفذقراءةبايت(بياناتمنفذ_2)
		return esp
	}
	return نشطلوحةمفاتيحمشغل.Hالتعاملمقاطعة(esp)
}

const لوحةمفاتيحطابورالحجم = 64

var لوحةمفاتيحطابور [لوحةمفاتيحطابورالحجم]byte
var لوحةمفاتيحطابورقراءة uint8
var لوحةمفاتيحطابوركتابة uint8
var يسارمفتاحShift bool
var يمينمفتاحShift bool
var extendedافحصcode bool

func طابورلوحةمفاتيحبايت(مفتاح byte) {
	التالي := (لوحةمفاتيحطابوركتابة + 1) % لوحةمفاتيحطابورالحجم
	if التالي == لوحةمفاتيحطابورقراءة {
		return
	}
	لوحةمفاتيحطابور[لوحةمفاتيحطابوركتابة] = مفتاح
	لوحةمفاتيحطابوركتابة = التالي
}

func Pعمليةمعلقلوحةمفاتيحأحداث() {
	for لوحةمفاتيحطابورقراءة != لوحةمفاتيحطابوركتابة {
		مفتاح := لوحةمفاتيحطابور[لوحةمفاتيحطابورقراءة]
		لوحةمفاتيحطابورقراءة = (لوحةمفاتيحطابورقراءة + 1) % لوحةمفاتيحطابورالحجم
		Stdinputبايت(مفتاح)
		if iلوحةمفاتيححدثhandler != nil {
			iلوحةمفاتيححدثhandler.Oعندمفتاحأسفل(مفتاح)
		}
	}
}

func افحصcodetoبايت(افحصcode uint8) (byte, bool) {
	مفتاحShift := يسارمفتاحShift || يمينمفتاحShift

	if افحصcode >= 0x02 && افحصcode <= 0x0B {
		if مفتاحShift {
			return "!@#$%^&*()"[افحصcode-0x02], true
		}
		return "1234567890"[افحصcode-0x02], true
	}
	if افحصcode >= 0x10 && افحصcode <= 0x19 {
		مفتاح := "qwertyuiop"[افحصcode-0x10]
		if مفتاحShift {
			مفتاح -= 'a' - 'A'
		}
		return مفتاح, true
	}
	if افحصcode >= 0x1E && افحصcode <= 0x26 {
		مفتاح := "asdfghjkl"[افحصcode-0x1E]
		if مفتاحShift {
			مفتاح -= 'a' - 'A'
		}
		return مفتاح, true
	}
	if افحصcode >= 0x2C && افحصcode <= 0x32 {
		مفتاح := "zxcvbnm"[افحصcode-0x2C]
		if مفتاحShift {
			مفتاح -= 'a' - 'A'
		}
		return مفتاح, true
	}

	switch افحصcode {
	case 0x0C:
		if مفتاحShift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if مفتاحShift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if مفتاحShift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if مفتاحShift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if مفتاحShift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if مفتاحShift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if مفتاحShift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if مفتاحShift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if مفتاحShift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if مفتاحShift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if مفتاحShift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (نفسه *Tلوحةمفاتيحمشغل) Hالتعاملمقاطعة(esp uint32) uint32 {
	الحالة := Pمنفذقراءةبايت(أمرمنفذ_2)
	if (الحالة&0x01) == 0 || (الحالة&0x20) != 0 {
		return esp
	}

	افحصcode := Pمنفذقراءةبايت(بياناتمنفذ_2)
	if افحصcode == 0xE0 {
		extendedافحصcode = true
		return esp
	}
	if extendedافحصcode {
		extendedافحصcode = false
		return esp
	}

	released := (افحصcode & 0x80) != 0
	basecode := افحصcode & 0x7F
	if basecode == 0x2A {
		يسارمفتاحShift = !released
		return esp
	}
	if basecode == 0x36 {
		يمينمفتاحShift = !released
		return esp
	}
	if released {
		return esp
	}

	if مفتاح, موافق := افحصcodetoبايت(basecode); موافق {
		طابورلوحةمفاتيحبايت(مفتاح)
	}

	return esp
}
