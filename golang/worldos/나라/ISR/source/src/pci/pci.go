/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "שער"
import . "פסק"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Oפעילgetdriver(התקן TPeripheralcomponentinterconnectהתקןdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type Tברירתמחדלpcicontrollerhandler struct {
}

func (self Tברירתמחדלpcicontrollerhandler) Oפעילgetdriver(התקן TPeripheralcomponentinterconnectהתקןdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectהתקןdescriptor struct {
	Pשערbase	uint32
	Iפסק		uint32

	bus	uint16
	התקן_2	uint16
	פונקציה	uint16

	Vיצרןמזהה	uint16
	Dהתקןמזהה	uint16

	מחלקהמזהה	uint8
	subclassמזהה	uint8
	ממשקמזהה	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectהתקןdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataשער			uint16
	פקודהשער		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataשער = 0xCFC
	self.פקודהשער = 0xCF8

	self.ipcicontrollerhandler = Tברירתמחדלpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Rקריאה(bus uint16, התקן_2 uint16, פונקציה uint16, registeroffset uint32) uint32 {
	var מזהה_2 uint32 = 0
	מזהה_2 = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(התקן_2&0x1f) << 11) | (uint32(פונקציה&0x07) << 8) | uint32(registeroffset&0xFC)

	Pשערכתיבהdword(self.פקודהשער, מזהה_2)

	result1 := Pשערקריאהdword(self.dataשער)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Wכתיבה(bus uint16, התקן_2 uint16, פונקציה uint16, registeroffset uint32, ערך uint32) {
	var מזהה_2 uint32
	מזהה_2 = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((התקן_2&0x1f)<<11) | uint32((פונקציה&0x07)<<8) | uint32(registeroffset&0xFC)
	Pשערכתיבהdword(self.פקודהשער, מזהה_2)
	Pשערכתיבהdword(self.dataשער, ערך)
}
func (self *TPeripheralcomponentinterconnectcontroller) Dהתקןhasפונקציות(bus uint16, התקן_2 uint16) bool {
	result := self.Rקריאה(bus, התקן_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Sבחרdriver(drivermanager *TDrivermanager, interrupts *Tפסקmanager) {
	for bus := 0; bus < 8; bus++ {
		for התקן_2 := 0; התקן_2 < 32; התקן_2++ {

			var מספרפונקציות int = 1
			if self.Dהתקןhasפונקציות(uint16(bus), uint16(התקן_2)) == true {
				מספרפונקציות = 8
			} else {
				מספרפונקציות = 1
			}

			for פונקציה := 0; פונקציה < מספרפונקציות; פונקציה++ {
				var התקן TPeripheralcomponentinterconnectהתקןdescriptor
				התקן = self.Getהתקןdescriptor(uint16(bus), uint16(התקן_2), uint16(פונקציה))
				if התקן.Vיצרןמזהה == 0x0000 || התקן.Vיצרןמזהה == 0xFFFF {
					continue
				}

				for פסמספר := 0; פסמספר < 6; פסמספר++ {
					var פס TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(התקן_2), uint16(פונקציה), uint16(פסמספר))
					if פס.address_2 != 0 && (פס.regtype == 1) {
						התקן.Pשערbase = פס.address_2
					}

					self.Getdriver(התקן, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) Getהתקןdescriptor(bus uint16, התקן_2 uint16, פונקציה uint16) TPeripheralcomponentinterconnectהתקןdescriptor {
	var result TPeripheralcomponentinterconnectהתקןdescriptor
	result = TPeripheralcomponentinterconnectהתקןdescriptor{}
	result.bus = bus
	result.התקן_2 = התקן_2
	result.פונקציה = פונקציה

	result.Vיצרןמזהה = uint16(self.Rקריאה(bus, התקן_2, פונקציה, 0x00))
	result.Dהתקןמזהה = uint16(self.Rקריאה(bus, התקן_2, פונקציה, 0x02))

	result.מחלקהמזהה = uint8(self.Rקריאה(bus, התקן_2, פונקציה, 0x0b))
	result.subclassמזהה = uint8(self.Rקריאה(bus, התקן_2, פונקציה, 0x0a))
	result.ממשקמזהה = uint8(self.Rקריאה(bus, התקן_2, פונקציה, 0x09))

	result.revision = uint8(self.Rקריאה(bus, התקן_2, פונקציה, 0x08))
	result.Iפסק = uint32(self.Rקריאה(bus, התקן_2, פונקציה, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, התקן_2 uint16, פונקציה uint16, פס uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Rקריאה(bus, התקן_2, פונקציה, 0x0E) & 0x7F
	var מקסימוםbars int = int(6 - (4 * headertype))
	if פס >= uint16(מקסימוםbars) {
		return result
	}

	פסערך := self.Rקריאה(bus, התקן_2, פונקציה, uint32(0x10+4*פס))

	if (פסערך & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = פסערך & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(התקן TPeripheralcomponentinterconnectהתקןdescriptor, interrupts *Tפסקmanager) {

	self.ipcicontrollerhandler.Oפעילgetdriver(התקן)

}
