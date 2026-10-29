/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "megszakítás"
import . "konzol"
import . "driver/driver"

type IpciVezérlőhandler interface {
	Begetdriver(eszköz TPeripheralcomponentinterconnectEszközdescriptor)
}

var ipciVezérlőhandler IpciVezérlőhandler

type TAlapértelmezettpciVezérlőhandler struct {
}

func (self TAlapértelmezettpciVezérlőhandler) Begetdriver(eszköz TPeripheralcomponentinterconnectEszközdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectEszközdescriptor struct {
	Portbase	uint32
	Megszakítás	uint32

	bus		uint16
	eszköz_2	uint16
	függvény	uint16

	GyártóAzonosító	uint16
	EszközAzonosító	uint16

	osztályAzonosító	uint8
	subclassAzonosító	uint8
	fELÜLETAzonosító	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectEszközdescriptor) Init() {
}

type TPeripheralcomponentinterconnectVezérlő struct {
	ipciVezérlőhandler	IpciVezérlőhandler
	dataport		uint16
	parancsport		uint16
}

func (self *TPeripheralcomponentinterconnectVezérlő) Init(ipciVezérlőhandler IpciVezérlőhandler) {
	self.dataport = 0xCFC
	self.parancsport = 0xCF8

	self.ipciVezérlőhandler = TAlapértelmezettpciVezérlőhandler{}
	if ipciVezérlőhandler != nil {
		self.ipciVezérlőhandler = ipciVezérlőhandler
	}
}

var iSzámláló int = 0

func (self *TPeripheralcomponentinterconnectVezérlő) Olvasás(bus uint16, eszköz_2 uint16, függvény uint16, registeroffset uint32) uint32 {
	var azonosító uint32 = 0
	azonosító = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(eszköz_2&0x1f) << 11) | (uint32(függvény&0x07) << 8) | uint32(registeroffset&0xFC)

	PortÍrásdword(self.parancsport, azonosító)

	result1 := PortOlvasásdword(self.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectVezérlő) Írás(bus uint16, eszköz_2 uint16, függvény uint16, registeroffset uint32, érték uint32) {
	var azonosító uint32
	azonosító = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((eszköz_2&0x1f)<<11) | uint32((függvény&0x07)<<8) | uint32(registeroffset&0xFC)
	PortÍrásdword(self.parancsport, azonosító)
	PortÍrásdword(self.dataport, érték)
}
func (self *TPeripheralcomponentinterconnectVezérlő) EszközHasDistrictFüggvények(bus uint16, eszköz_2 uint16) bool {
	result := self.Olvasás(bus, eszköz_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konzol TKonzol = TKonzol{}

func (self *TPeripheralcomponentinterconnectVezérlő) Kijelölésdriver(drivermanager *TDrivermanager, interrupts *TMegszakításmanager) {
	for bus := 0; bus < 8; bus++ {
		for eszköz_2 := 0; eszköz_2 < 32; eszköz_2++ {

			var számFüggvények int = 1
			if self.EszközHasDistrictFüggvények(uint16(bus), uint16(eszköz_2)) == true {
				számFüggvények = 8
			} else {
				számFüggvények = 1
			}

			for függvény := 0; függvény < számFüggvények; függvény++ {
				var eszköz TPeripheralcomponentinterconnectEszközdescriptor
				eszköz = self.GetEszközdescriptor(uint16(bus), uint16(eszköz_2), uint16(függvény))
				if eszköz.GyártóAzonosító == 0x0000 || eszköz.GyártóAzonosító == 0xFFFF {
					continue
				}

				for sávSzám := 0; sávSzám < 6; sávSzám++ {
					var sáv TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(eszköz_2), uint16(függvény), uint16(sávSzám))
					if sáv.address_2 != 0 && (sáv.regtype == 1) {
						eszköz.Portbase = sáv.address_2
					}

					self.Getdriver(eszköz, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectVezérlő) GetEszközdescriptor(bus uint16, eszköz_2 uint16, függvény uint16) TPeripheralcomponentinterconnectEszközdescriptor {
	var result TPeripheralcomponentinterconnectEszközdescriptor
	result = TPeripheralcomponentinterconnectEszközdescriptor{}
	result.bus = bus
	result.eszköz_2 = eszköz_2
	result.függvény = függvény

	result.GyártóAzonosító = uint16(self.Olvasás(bus, eszköz_2, függvény, 0x00))
	result.EszközAzonosító = uint16(self.Olvasás(bus, eszköz_2, függvény, 0x02))

	result.osztályAzonosító = uint8(self.Olvasás(bus, eszköz_2, függvény, 0x0b))
	result.subclassAzonosító = uint8(self.Olvasás(bus, eszköz_2, függvény, 0x0a))
	result.fELÜLETAzonosító = uint8(self.Olvasás(bus, eszköz_2, függvény, 0x09))

	result.revision = uint8(self.Olvasás(bus, eszköz_2, függvény, 0x08))
	result.Megszakítás = uint32(self.Olvasás(bus, eszköz_2, függvény, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectVezérlő) Getbaseaddressregister(bus uint16, eszköz_2 uint16, függvény uint16, sáv uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Olvasás(bus, eszköz_2, függvény, 0x0E) & 0x7F
	var maximumbars int = int(6 - (4 * headertype))
	if sáv >= uint16(maximumbars) {
		return result
	}

	sávÉrték := self.Olvasás(bus, eszköz_2, függvény, uint32(0x10+4*sáv))

	if (sávÉrték & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = sávÉrték & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectVezérlő) Getdriver(eszköz TPeripheralcomponentinterconnectEszközdescriptor, interrupts *TMegszakításmanager) {

	self.ipciVezérlőhandler.Begetdriver(eszköz)

}
