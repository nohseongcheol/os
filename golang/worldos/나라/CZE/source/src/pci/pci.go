/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "přerušení"
import . "konzole"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Zapnutogetdriver(zařízení TPeripheralcomponentinterconnectZařízenídescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TVýchozípcicontrollerhandler struct {
}

func (self TVýchozípcicontrollerhandler) Zapnutogetdriver(zařízení TPeripheralcomponentinterconnectZařízenídescriptor) {
}

type TBaseAdresaregister struct {
	prefetchcapable	bool
	adresa_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectZařízenídescriptor struct {
	Portbase	uint32
	Přerušení	uint32

	bus		uint16
	zařízení_2	uint16
	funkce		uint16

	Výrobceid	uint16
	Zařízeníid	uint16

	třídaid		uint8
	subclassid	uint8
	rozhraníid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectZařízenídescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	příkazport		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataport = 0xCFC
	self.příkazport = 0xCF8

	self.ipcicontrollerhandler = TVýchozípcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var iPočet int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Čtení(bus uint16, zařízení_2 uint16, funkce uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(zařízení_2&0x1f) << 11) | (uint32(funkce&0x07) << 8) | uint32(registeroffset&0xFC)

	PortZápisdword(self.příkazport, id)

	vÝSLEDEK1 := PortČtenídword(self.dataport)
	vÝSLEDEK2 := (vÝSLEDEK1 >> (8 * (registeroffset % 4)))

	return vÝSLEDEK2
}

func (self *TPeripheralcomponentinterconnectcontroller) Zápis(bus uint16, zařízení_2 uint16, funkce uint16, registeroffset uint32, hodnota uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((zařízení_2&0x1f)<<11) | uint32((funkce&0x07)<<8) | uint32(registeroffset&0xFC)
	PortZápisdword(self.příkazport, id)
	PortZápisdword(self.dataport, hodnota)
}
func (self *TPeripheralcomponentinterconnectcontroller) ZařízeníhasFunkce(bus uint16, zařízení_2 uint16) bool {
	vÝSLEDEK := self.Čtení(bus, zařízení_2, 0, 0x0E)
	if (vÝSLEDEK & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konzole TKonzole = TKonzole{}

func (self *TPeripheralcomponentinterconnectcontroller) Vybratdriver(drivermanager *TDrivermanager, interrupts *TPřerušenímanager) {
	for bus := 0; bus < 8; bus++ {
		for zařízení_2 := 0; zařízení_2 < 32; zařízení_2++ {

			var čísloFunkce int = 1
			if self.ZařízeníhasFunkce(uint16(bus), uint16(zařízení_2)) == true {
				čísloFunkce = 8
			} else {
				čísloFunkce = 1
			}

			for funkce := 0; funkce < čísloFunkce; funkce++ {
				var zařízení TPeripheralcomponentinterconnectZařízenídescriptor
				zařízení = self.GetZařízenídescriptor(uint16(bus), uint16(zařízení_2), uint16(funkce))
				if zařízení.Výrobceid == 0x0000 || zařízení.Výrobceid == 0xFFFF {
					continue
				}

				for pruhČíslo := 0; pruhČíslo < 6; pruhČíslo++ {
					var pruh TBaseAdresaregister = self.GetbaseAdresaregister(uint16(bus), uint16(zařízení_2), uint16(funkce), uint16(pruhČíslo))
					if pruh.adresa_2 != 0 && (pruh.regtype == 1) {
						zařízení.Portbase = pruh.adresa_2
					}

					self.Getdriver(zařízení, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetZařízenídescriptor(bus uint16, zařízení_2 uint16, funkce uint16) TPeripheralcomponentinterconnectZařízenídescriptor {
	var vÝSLEDEK TPeripheralcomponentinterconnectZařízenídescriptor
	vÝSLEDEK = TPeripheralcomponentinterconnectZařízenídescriptor{}
	vÝSLEDEK.bus = bus
	vÝSLEDEK.zařízení_2 = zařízení_2
	vÝSLEDEK.funkce = funkce

	vÝSLEDEK.Výrobceid = uint16(self.Čtení(bus, zařízení_2, funkce, 0x00))
	vÝSLEDEK.Zařízeníid = uint16(self.Čtení(bus, zařízení_2, funkce, 0x02))

	vÝSLEDEK.třídaid = uint8(self.Čtení(bus, zařízení_2, funkce, 0x0b))
	vÝSLEDEK.subclassid = uint8(self.Čtení(bus, zařízení_2, funkce, 0x0a))
	vÝSLEDEK.rozhraníid = uint8(self.Čtení(bus, zařízení_2, funkce, 0x09))

	vÝSLEDEK.revision = uint8(self.Čtení(bus, zařízení_2, funkce, 0x08))
	vÝSLEDEK.Přerušení = uint32(self.Čtení(bus, zařízení_2, funkce, 0x3C))

	return vÝSLEDEK
}
func (self *TPeripheralcomponentinterconnectcontroller) GetbaseAdresaregister(bus uint16, zařízení_2 uint16, funkce uint16, pruh uint16) TBaseAdresaregister {
	var vÝSLEDEK TBaseAdresaregister

	headertype := self.Čtení(bus, zařízení_2, funkce, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if pruh >= uint16(maxbars) {
		return vÝSLEDEK
	}

	pruhHodnota := self.Čtení(bus, zařízení_2, funkce, uint32(0x10+4*pruh))

	if (pruhHodnota & 0x1) != 0 {
		vÝSLEDEK.regtype = 1
	} else {
		vÝSLEDEK.regtype = 0
	}

	if vÝSLEDEK.regtype == 0 {
	} else {
		vÝSLEDEK.adresa_2 = pruhHodnota & ^uint32(0x3)
		vÝSLEDEK.prefetchcapable = false
	}

	return vÝSLEDEK
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(zařízení TPeripheralcomponentinterconnectZařízenídescriptor, interrupts *TPřerušenímanager) {

	self.ipcicontrollerhandler.Zapnutogetdriver(zařízení)

}
