/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "منفذ"
import . "مقاطعة"
import . "طرفية"
import . "مشغل/مشغل"

type Ipciمتحكمhandler interface {
	Oعندgetمشغل(الجهاز TPeripheralcomponentinterconnectالجهازdescriptor)
}

var ipciمتحكمhandler Ipciمتحكمhandler

type Tالافتراضيpciمتحكمhandler struct {
}

func (نفسه Tالافتراضيpciمتحكمhandler) Oعندgetمشغل(الجهاز TPeripheralcomponentinterconnectالجهازdescriptor) {
}

type TBaseaddressسجل struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectالجهازdescriptor struct {
	Pمنفذbase	uint32
	Iمقاطعة		uint32

	bus		uint16
	الجهاز_2	uint16
	function	uint16

	Vبائعالهوية	uint16
	Dالجهازالهوية	uint16

	الفئةالهوية	uint8
	subclassالهوية	uint8
	الواجهةالهوية	uint8

	revision	uint8
}

func (نفسه *TPeripheralcomponentinterconnectالجهازdescriptor) Init() {
}

type TPeripheralcomponentinterconnectمتحكم struct {
	ipciمتحكمhandler	Ipciمتحكمhandler
	بياناتمنفذ		uint16
	أمرمنفذ			uint16
}

func (نفسه *TPeripheralcomponentinterconnectمتحكم) Init(ipciمتحكمhandler Ipciمتحكمhandler) {
	نفسه.بياناتمنفذ = 0xCFC
	نفسه.أمرمنفذ = 0xCF8

	نفسه.ipciمتحكمhandler = Tالافتراضيpciمتحكمhandler{}
	if ipciمتحكمhandler != nil {
		نفسه.ipciمتحكمhandler = ipciمتحكمhandler
	}
}

var icount int = 0

func (نفسه *TPeripheralcomponentinterconnectمتحكم) Rقراءة(bus uint16, الجهاز_2 uint16, function uint16, registeroffset uint32) uint32 {
	var الهوية uint32 = 0
	الهوية = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(الجهاز_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	Pمنفذكتابةdword(نفسه.أمرمنفذ, الهوية)

	result1 := Pمنفذقراءةdword(نفسه.بياناتمنفذ)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (نفسه *TPeripheralcomponentinterconnectمتحكم) Wكتابة(bus uint16, الجهاز_2 uint16, function uint16, registeroffset uint32, القيمة uint32) {
	var الهوية uint32
	الهوية = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((الجهاز_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	Pمنفذكتابةdword(نفسه.أمرمنفذ, الهوية)
	Pمنفذكتابةdword(نفسه.بياناتمنفذ, القيمة)
}
func (نفسه *TPeripheralcomponentinterconnectمتحكم) Dالجهازhasfunctions(bus uint16, الجهاز_2 uint16) bool {
	result := نفسه.Rقراءة(bus, الجهاز_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var طرفية Tطرفية = Tطرفية{}

func (نفسه *TPeripheralcomponentinterconnectمتحكم) Sإختيارمشغل(مشغلمدير *Tمشغلمدير, interrupts *Tمقاطعةمدير) {
	for bus := 0; bus < 8; bus++ {
		for الجهاز_2 := 0; الجهاز_2 < 32; الجهاز_2++ {

			var الأرقامfunctions int = 1
			if نفسه.Dالجهازhasfunctions(uint16(bus), uint16(الجهاز_2)) == true {
				الأرقامfunctions = 8
			} else {
				الأرقامfunctions = 1
			}

			for function := 0; function < الأرقامfunctions; function++ {
				var الجهاز TPeripheralcomponentinterconnectالجهازdescriptor
				الجهاز = نفسه.Getالجهازdescriptor(uint16(bus), uint16(الجهاز_2), uint16(function))
				if الجهاز.Vبائعالهوية == 0x0000 || الجهاز.Vبائعالهوية == 0xFFFF {
					continue
				}

				for شريطالأرقام := 0; شريطالأرقام < 6; شريطالأرقام++ {
					var شريط TBaseaddressسجل = نفسه.Getbaseaddressسجل(uint16(bus), uint16(الجهاز_2), uint16(function), uint16(شريطالأرقام))
					if شريط.address_2 != 0 && (شريط.regtype == 1) {
						الجهاز.Pمنفذbase = شريط.address_2
					}

					نفسه.Getمشغل(الجهاز, interrupts)

				}

			}

		}
	}
}
func (نفسه *TPeripheralcomponentinterconnectمتحكم) Getالجهازdescriptor(bus uint16, الجهاز_2 uint16, function uint16) TPeripheralcomponentinterconnectالجهازdescriptor {
	var result TPeripheralcomponentinterconnectالجهازdescriptor
	result = TPeripheralcomponentinterconnectالجهازdescriptor{}
	result.bus = bus
	result.الجهاز_2 = الجهاز_2
	result.function = function

	result.Vبائعالهوية = uint16(نفسه.Rقراءة(bus, الجهاز_2, function, 0x00))
	result.Dالجهازالهوية = uint16(نفسه.Rقراءة(bus, الجهاز_2, function, 0x02))

	result.الفئةالهوية = uint8(نفسه.Rقراءة(bus, الجهاز_2, function, 0x0b))
	result.subclassالهوية = uint8(نفسه.Rقراءة(bus, الجهاز_2, function, 0x0a))
	result.الواجهةالهوية = uint8(نفسه.Rقراءة(bus, الجهاز_2, function, 0x09))

	result.revision = uint8(نفسه.Rقراءة(bus, الجهاز_2, function, 0x08))
	result.Iمقاطعة = uint32(نفسه.Rقراءة(bus, الجهاز_2, function, 0x3C))

	return result
}
func (نفسه *TPeripheralcomponentinterconnectمتحكم) Getbaseaddressسجل(bus uint16, الجهاز_2 uint16, function uint16, شريط uint16) TBaseaddressسجل {
	var result TBaseaddressسجل

	headertype := نفسه.Rقراءة(bus, الجهاز_2, function, 0x0E) & 0x7F
	var أقصىbars int = int(6 - (4 * headertype))
	if شريط >= uint16(أقصىbars) {
		return result
	}

	شريطالقيمة := نفسه.Rقراءة(bus, الجهاز_2, function, uint32(0x10+4*شريط))

	if (شريطالقيمة & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = شريطالقيمة & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (نفسه *TPeripheralcomponentinterconnectمتحكم) Getمشغل(الجهاز TPeripheralcomponentinterconnectالجهازdescriptor, interrupts *Tمقاطعةمدير) {

	نفسه.ipciمتحكمhandler.Oعندgetمشغل(الجهاز)

}
