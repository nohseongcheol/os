/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package لوحةمفاتيح

import . "unsafe"

import . "منفذ"
import . "مقاطعة"
import . "طرفية"

type Iفأرةحدثhandler interface {
	Oعندفأرةأسفل(زر int8)
	Oعندفأرةأعلى(زر int8)
	Oعندفأرةانقل(x int8, y int8)
}

var iفأرةحدثhandler Iفأرةحدثhandler

type Tالافتراضيفأرةحدثhandler struct {
}

var طرفية_2 Tطرفية = Tطرفية{}
var previousx int16 = 0
var previousy int16 = 0
var xالموضع int16 = 0
var yالموضع int16 = 0

func (نفسه Tالافتراضيفأرةحدثhandler) Oعندفأرةأسفل(زر int8) {
	buffer := []byte("+")
	طرفية_2.Mاطبعxy(buffer, uint16(previousx), uint16(previousy))
}
func (نفسه Tالافتراضيفأرةحدثhandler) Oعندفأرةأعلى(زر int8)	{}
func (نفسه Tالافتراضيفأرةحدثhandler) Oعندفأرةانقل(x int8, y int8) {

	xالموضع += int16(x)
	if xالموضع < 0 {
		xالموضع = 0
	}
	if xالموضع >= 80 {
		xالموضع = 79
	}

	yالموضع -= int16(y)

	if yالموضع < 0 {
		yالموضع = 0
	}
	if yالموضع >= 25 {
		yالموضع = 24
	}

	buffer := []byte(" ")
	طرفية_2.Mاطبعxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	طرفية_2.Mاطبعxy(buffer, uint16(xالموضع), uint16(yالموضع))

	previousx = xالموضع
	previousy = yالموضع
}

type Tفأرةمشغل struct {
	Tمقاطعةhandler
}

var نشطفأرةمشغل *Tفأرةمشغل
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

func أرسلفأرةأمر(القيمة uint8) bool {
	if !كتابةps2أمر(0xD4) || !كتابةps2بيانات(القيمة) {
		return false
	}
	ack, موافق := قراءةps2بيانات()
	return موافق && ack == 0xFA
}

func (نفسه *Tفأرةمشغل) Initمشغل(مدير *Tمقاطعةمدير, فأرةحدثhandler Iفأرةحدثhandler) {

	iفأرةحدثhandler = Tالافتراضيفأرةحدثhandler{}

	if فأرةحدثhandler != nil {
		iفأرةحدثhandler = فأرةحدثhandler
	}

	نشطفأرةمشغل = نفسه
	مقاطعةhandler = التعاملفأرةمقاطعة
	var address uintptr
	address = uintptr(Pointer(&مقاطعةhandler))
	نفسه.Init(0x2C, uintptr(Pointer(مدير)), address)

	for i := 0; i < 32 && (Pمنفذقراءةبايت(أمرمنفذ_2)&0x01) != 0; i++ {
		Pمنفذقراءةبايت(بياناتمنفذ_2)
	}

	if !كتابةps2أمر(0xA8) || !كتابةps2أمر(0x20) {
		return
	}
	الحالة, موافق := قراءةps2بيانات()
	if !موافق {
		return
	}
	الحالة |= 0x02
	الحالة &^= 0x20
	if !كتابةps2أمر(0x60) || !كتابةps2بيانات(الحالة) {
		return
	}

	if !أرسلفأرةأمر(0xF6) || !أرسلفأرةأمر(0xF4) {
		return
	}
	offset = 0

}

func التعاملفأرةمقاطعة(esp uint32) uint32 {
	if نشطفأرةمشغل == nil {
		Pمنفذقراءةبايت(بياناتمنفذ_2)
		return esp
	}
	return نشطفأرةمشغل.Hالتعاملمقاطعة(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var زر_2 int8
var معلقx int16
var معلقy int16
var معلقزر int8
var معلقفأرةحدث bool

func (نفسه *Tفأرةمشغل) Hالتعاملمقاطعة(esp uint32) uint32 {
	الحالة := Pمنفذقراءةبايت(أمرمنفذ_2)
	if (الحالة&0x01) == 0 || (الحالة&0x20) == 0 {
		return esp
	}

	بيانات := Pمنفذقراءةبايت(بياناتمنفذ_2)

	if offset == 0 && (بيانات&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(بيانات)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetالحالة := uint8(buffer_2[0])

		if (packetالحالة & 0xC0) == 0 {
			معلقx += int16(buffer_2[1])
			معلقy += int16(buffer_2[2])
			if معلقx > 127 {
				معلقx = 127
			} else if معلقx < -127 {
				معلقx = -127
			}
			if معلقy > 127 {
				معلقy = 127
			} else if معلقy < -127 {
				معلقy = -127
			}
		}
		معلقزر = int8(packetالحالة & 0x07)
		معلقفأرةحدث = true
	}

	return esp

}

func Pعمليةمعلقفأرةأحداث() {
	if iفأرةحدثhandler == nil {
		return
	}

	Iمقاطعةdeactive()
	if !معلقفأرةحدث {
		Iمقاطعةنشط()
		return
	}
	x := int8(معلقx)
	y := int8(معلقy)
	جديدزر := معلقزر
	oldزر := زر_2

	معلقx = 0
	معلقy = 0
	معلقفأرةحدث = false
	Iمقاطعةنشط()

	if x != 0 || y != 0 {
		iفأرةحدثhandler.Oعندفأرةانقل(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (جديدزر & mask) != (oldزر & mask) {
			if (جديدزر & mask) != 0 {
				iفأرةحدثhandler.Oعندفأرةأسفل(int8(i + 1))
			} else {
				iفأرةحدثhandler.Oعندفأرةأعلى(int8(i + 1))
			}
		}
	}
	زر_2 = جديدزر
}
