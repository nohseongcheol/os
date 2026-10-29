/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "порт"
import . "ометање"
import . "конзола"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Nagetdriver(уређај TPeripheralcomponentinterconnectУређајdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TПодразумеваноpcicontrollerhandler struct {
}

func (isti TПодразумеваноpcicontrollerhandler) Nagetdriver(уређај TPeripheralcomponentinterconnectУређајdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectУређајdescriptor struct {
	Портbase	uint32
	Ометање		uint32

	bus		uint16
	уређај_2	uint16
	функција	uint16

	ProizvođačIB	uint16
	УређајIB	uint16

	класаIB		uint8
	subclassIB	uint8
	uREĐAJIB	uint8

	revision	uint8
}

func (isti *TPeripheralcomponentinterconnectУређајdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataПорт		uint16
	наредбаПорт		uint16
}

func (isti *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	isti.dataПорт = 0xCFC
	isti.наредбаПорт = 0xCF8

	isti.ipcicontrollerhandler = TПодразумеваноpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		isti.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (isti *TPeripheralcomponentinterconnectcontroller) Читање(bus uint16, уређај_2 uint16, функција uint16, registeroffset uint32) uint32 {
	var iB uint32 = 0
	iB = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(уређај_2&0x1f) << 11) | (uint32(функција&0x07) << 8) | uint32(registeroffset&0xFC)

	Портupisdword(isti.наредбаПорт, iB)

	иСХОД1 := Портчитањеdword(isti.dataПорт)
	иСХОД2 := (иСХОД1 >> (8 * (registeroffset % 4)))

	return иСХОД2
}

func (isti *TPeripheralcomponentinterconnectcontroller) Upis(bus uint16, уређај_2 uint16, функција uint16, registeroffset uint32, вредност uint32) {
	var iB uint32
	iB = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((уређај_2&0x1f)<<11) | uint32((функција&0x07)<<8) | uint32(registeroffset&0xFC)
	Портupisdword(isti.наредбаПорт, iB)
	Портupisdword(isti.dataПорт, вредност)
}
func (isti *TPeripheralcomponentinterconnectcontroller) УређајХасФункције(bus uint16, уређај_2 uint16) bool {
	иСХОД := isti.Читање(bus, уређај_2, 0, 0x0E)
	if (иСХОД & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var конзола TКонзола = TКонзола{}

func (isti *TPeripheralcomponentinterconnectcontroller) Изабериdriver(drivermanager *TDrivermanager, interrupts *TОметањеmanager) {
	for bus := 0; bus < 8; bus++ {
		for уређај_2 := 0; уређај_2 < 32; уређај_2++ {

			var бројФункције int = 1
			if isti.УређајХасФункције(uint16(bus), uint16(уређај_2)) == true {
				бројФункције = 8
			} else {
				бројФункције = 1
			}

			for функција := 0; функција < бројФункције; функција++ {
				var уређај TPeripheralcomponentinterconnectУређајdescriptor
				уређај = isti.GetУређајdescriptor(uint16(bus), uint16(уређај_2), uint16(функција))
				if уређај.ProizvođačIB == 0x0000 || уређај.ProizvođačIB == 0xFFFF {
					continue
				}

				for барброј := 0; барброј < 6; барброј++ {
					var бар TBaseaddressregister = isti.Getbaseaddressregister(uint16(bus), uint16(уређај_2), uint16(функција), uint16(барброј))
					if бар.address_2 != 0 && (бар.regtype == 1) {
						уређај.Портbase = бар.address_2
					}

					isti.Getdriver(уређај, interrupts)

				}

			}

		}
	}
}
func (isti *TPeripheralcomponentinterconnectcontroller) GetУређајdescriptor(bus uint16, уређај_2 uint16, функција uint16) TPeripheralcomponentinterconnectУређајdescriptor {
	var иСХОД TPeripheralcomponentinterconnectУређајdescriptor
	иСХОД = TPeripheralcomponentinterconnectУређајdescriptor{}
	иСХОД.bus = bus
	иСХОД.уређај_2 = уређај_2
	иСХОД.функција = функција

	иСХОД.ProizvođačIB = uint16(isti.Читање(bus, уређај_2, функција, 0x00))
	иСХОД.УређајIB = uint16(isti.Читање(bus, уређај_2, функција, 0x02))

	иСХОД.класаIB = uint8(isti.Читање(bus, уређај_2, функција, 0x0b))
	иСХОД.subclassIB = uint8(isti.Читање(bus, уређај_2, функција, 0x0a))
	иСХОД.uREĐAJIB = uint8(isti.Читање(bus, уређај_2, функција, 0x09))

	иСХОД.revision = uint8(isti.Читање(bus, уређај_2, функција, 0x08))
	иСХОД.Ометање = uint32(isti.Читање(bus, уређај_2, функција, 0x3C))

	return иСХОД
}
func (isti *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, уређај_2 uint16, функција uint16, бар uint16) TBaseaddressregister {
	var иСХОД TBaseaddressregister

	headertype := isti.Читање(bus, уређај_2, функција, 0x0E) & 0x7F
	var максbars int = int(6 - (4 * headertype))
	if бар >= uint16(максbars) {
		return иСХОД
	}

	барВредност := isti.Читање(bus, уређај_2, функција, uint32(0x10+4*бар))

	if (барВредност & 0x1) != 0 {
		иСХОД.regtype = 1
	} else {
		иСХОД.regtype = 0
	}

	if иСХОД.regtype == 0 {
	} else {
		иСХОД.address_2 = барВредност & ^uint32(0x3)
		иСХОД.prefetchcapable = false
	}

	return иСХОД
}
func (isti *TPeripheralcomponentinterconnectcontroller) Getdriver(уређај TPeripheralcomponentinterconnectУређајdescriptor, interrupts *TОметањеmanager) {

	isti.ipcicontrollerhandler.Nagetdriver(уређај)

}
