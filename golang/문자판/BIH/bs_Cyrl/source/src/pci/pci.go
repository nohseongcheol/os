/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Uključengetdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TUobičajenopcicontrollerhandler struct {
}

func (self TUobičajenopcicontrollerhandler) Uključengetdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectUređajdescriptor struct {
	Portbase	uint32
	Interrupt	uint32

	bus		uint16
	uređaj_2	uint16
	funkcija	uint16

	Vendorid	uint16
	Uređajid	uint16

	klasaid		uint8
	subclassid	uint8
	interfejsid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectUređajdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	naredbaport		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataport = 0xCFC
	self.naredbaport = 0xCF8

	self.ipcicontrollerhandler = TUobičajenopcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Čitaj(bus uint16, uređaj_2 uint16, funkcija uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(uređaj_2&0x1f) << 11) | (uint32(funkcija&0x07) << 8) | uint32(registeroffset&0xFC)

	PortPišidword(self.naredbaport, id)

	result1 := PortČitajdword(self.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Piši(bus uint16, uređaj_2 uint16, funkcija uint16, registeroffset uint32, vrijednost uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((uređaj_2&0x1f)<<11) | uint32((funkcija&0x07)<<8) | uint32(registeroffset&0xFC)
	PortPišidword(self.naredbaport, id)
	PortPišidword(self.dataport, vrijednost)
}
func (self *TPeripheralcomponentinterconnectcontroller) UređajhasFunkcije(bus uint16, uređaj_2 uint16) bool {
	result := self.Čitaj(bus, uređaj_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for uređaj_2 := 0; uređaj_2 < 32; uređaj_2++ {

			var brojFunkcije int = 1
			if self.UređajhasFunkcije(uint16(bus), uint16(uređaj_2)) == true {
				brojFunkcije = 8
			} else {
				brojFunkcije = 1
			}

			for funkcija := 0; funkcija < brojFunkcije; funkcija++ {
				var uređaj TPeripheralcomponentinterconnectUređajdescriptor
				uređaj = self.GetUređajdescriptor(uint16(bus), uint16(uređaj_2), uint16(funkcija))
				if uređaj.Vendorid == 0x0000 || uređaj.Vendorid == 0xFFFF {
					continue
				}

				for trakaBroj := 0; trakaBroj < 6; trakaBroj++ {
					var traka TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(uređaj_2), uint16(funkcija), uint16(trakaBroj))
					if traka.address_2 != 0 && (traka.regtype == 1) {
						uređaj.Portbase = traka.address_2
					}

					self.Getdriver(uređaj, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetUređajdescriptor(bus uint16, uređaj_2 uint16, funkcija uint16) TPeripheralcomponentinterconnectUređajdescriptor {
	var result TPeripheralcomponentinterconnectUređajdescriptor
	result = TPeripheralcomponentinterconnectUređajdescriptor{}
	result.bus = bus
	result.uređaj_2 = uređaj_2
	result.funkcija = funkcija

	result.Vendorid = uint16(self.Čitaj(bus, uređaj_2, funkcija, 0x00))
	result.Uređajid = uint16(self.Čitaj(bus, uređaj_2, funkcija, 0x02))

	result.klasaid = uint8(self.Čitaj(bus, uređaj_2, funkcija, 0x0b))
	result.subclassid = uint8(self.Čitaj(bus, uređaj_2, funkcija, 0x0a))
	result.interfejsid = uint8(self.Čitaj(bus, uređaj_2, funkcija, 0x09))

	result.revision = uint8(self.Čitaj(bus, uređaj_2, funkcija, 0x08))
	result.Interrupt = uint32(self.Čitaj(bus, uređaj_2, funkcija, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, uređaj_2 uint16, funkcija uint16, traka uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Čitaj(bus, uređaj_2, funkcija, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if traka >= uint16(maxbars) {
		return result
	}

	trakaVrijednost := self.Čitaj(bus, uređaj_2, funkcija, uint32(0x10+4*traka))

	if (trakaVrijednost & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = trakaVrijednost & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor, interrupts *TInterruptmanager) {

	self.ipcicontrollerhandler.Uključengetdriver(uređaj)

}
