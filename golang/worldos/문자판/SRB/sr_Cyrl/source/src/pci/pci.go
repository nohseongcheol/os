/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "порт"
import . "ометање"
import . "конзола"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Наgetdriver(уређај TPeripheralcomponentinterconnectУређајdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TПодразумеваноpcicontrollerhandler struct {
}

func (исти TПодразумеваноpcicontrollerhandler) Наgetdriver(уређај TPeripheralcomponentinterconnectУређајdescriptor) {
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

	ПроизвођачИБ	uint16
	УређајИБ	uint16

	класаИБ		uint8
	subclassИБ	uint8
	уРЕЂАЈИБ	uint8

	revision	uint8
}

func (исти *TPeripheralcomponentinterconnectУређајdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataПорт		uint16
	наредбаПорт		uint16
}

func (исти *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	исти.dataПорт = 0xCFC
	исти.наредбаПорт = 0xCF8

	исти.ipcicontrollerhandler = TПодразумеваноpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		исти.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (исти *TPeripheralcomponentinterconnectcontroller) Читање(bus uint16, уређај_2 uint16, функција uint16, registeroffset uint32) uint32 {
	var иБ uint32 = 0
	иБ = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(уређај_2&0x1f) << 11) | (uint32(функција&0x07) << 8) | uint32(registeroffset&0xFC)

	ПортПишеdword(исти.наредбаПорт, иБ)

	иСХОД1 := Портчитањеdword(исти.dataПорт)
	иСХОД2 := (иСХОД1 >> (8 * (registeroffset % 4)))

	return иСХОД2
}

func (исти *TPeripheralcomponentinterconnectcontroller) Пише(bus uint16, уређај_2 uint16, функција uint16, registeroffset uint32, вредност uint32) {
	var иБ uint32
	иБ = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((уређај_2&0x1f)<<11) | uint32((функција&0x07)<<8) | uint32(registeroffset&0xFC)
	ПортПишеdword(исти.наредбаПорт, иБ)
	ПортПишеdword(исти.dataПорт, вредност)
}
func (исти *TPeripheralcomponentinterconnectcontroller) УређајХасФункције(bus uint16, уређај_2 uint16) bool {
	иСХОД := исти.Читање(bus, уређај_2, 0, 0x0E)
	if (иСХОД & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var конзола TКонзола = TКонзола{}

func (исти *TPeripheralcomponentinterconnectcontroller) Изабериdriver(drivermanager *TDrivermanager, interrupts *TОметањеmanager) {
	for bus := 0; bus < 8; bus++ {
		for уређај_2 := 0; уређај_2 < 32; уређај_2++ {

			var бројФункције int = 1
			if исти.УређајХасФункције(uint16(bus), uint16(уређај_2)) == true {
				бројФункције = 8
			} else {
				бројФункције = 1
			}

			for функција := 0; функција < бројФункције; функција++ {
				var уређај TPeripheralcomponentinterconnectУређајdescriptor
				уређај = исти.GetУређајdescriptor(uint16(bus), uint16(уређај_2), uint16(функција))
				if уређај.ПроизвођачИБ == 0x0000 || уређај.ПроизвођачИБ == 0xFFFF {
					continue
				}

				for барброј := 0; барброј < 6; барброј++ {
					var бар TBaseaddressregister = исти.Getbaseaddressregister(uint16(bus), uint16(уређај_2), uint16(функција), uint16(барброј))
					if бар.address_2 != 0 && (бар.regtype == 1) {
						уређај.Портbase = бар.address_2
					}

					исти.Getdriver(уређај, interrupts)

				}

			}

		}
	}
}
func (исти *TPeripheralcomponentinterconnectcontroller) GetУређајdescriptor(bus uint16, уређај_2 uint16, функција uint16) TPeripheralcomponentinterconnectУређајdescriptor {
	var иСХОД TPeripheralcomponentinterconnectУређајdescriptor
	иСХОД = TPeripheralcomponentinterconnectУређајdescriptor{}
	иСХОД.bus = bus
	иСХОД.уређај_2 = уређај_2
	иСХОД.функција = функција

	иСХОД.ПроизвођачИБ = uint16(исти.Читање(bus, уређај_2, функција, 0x00))
	иСХОД.УређајИБ = uint16(исти.Читање(bus, уређај_2, функција, 0x02))

	иСХОД.класаИБ = uint8(исти.Читање(bus, уређај_2, функција, 0x0b))
	иСХОД.subclassИБ = uint8(исти.Читање(bus, уређај_2, функција, 0x0a))
	иСХОД.уРЕЂАЈИБ = uint8(исти.Читање(bus, уређај_2, функција, 0x09))

	иСХОД.revision = uint8(исти.Читање(bus, уређај_2, функција, 0x08))
	иСХОД.Ометање = uint32(исти.Читање(bus, уређај_2, функција, 0x3C))

	return иСХОД
}
func (исти *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, уређај_2 uint16, функција uint16, бар uint16) TBaseaddressregister {
	var иСХОД TBaseaddressregister

	headertype := исти.Читање(bus, уређај_2, функција, 0x0E) & 0x7F
	var максbars int = int(6 - (4 * headertype))
	if бар >= uint16(максbars) {
		return иСХОД
	}

	барВредност := исти.Читање(bus, уређај_2, функција, uint32(0x10+4*бар))

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
func (исти *TPeripheralcomponentinterconnectcontroller) Getdriver(уређај TPeripheralcomponentinterconnectУређајdescriptor, interrupts *TОметањеmanager) {

	исти.ipcicontrollerhandler.Наgetdriver(уређај)

}
