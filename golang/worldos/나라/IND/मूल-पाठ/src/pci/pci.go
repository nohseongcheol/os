/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ongetdriver(उपकरण TPeripheralcomponentinterconnectउपकरणdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TDefaultpcicontrollerhandler struct {
}

func (self TDefaultpcicontrollerhandler) Ongetdriver(उपकरण TPeripheralcomponentinterconnectउपकरणdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectउपकरणdescriptor struct {
	Portbase	uint32
	Interrupt	uint32

	bus		uint16
	उपकरण_2		uint16
	function	uint16

	Vendorid	uint16
	Dउपकरणid	uint16

	classid		uint8
	subclassid	uint8
	interfaceid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectउपकरणdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	commandport		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataport = 0xCFC
	self.commandport = 0xCF8

	self.ipcicontrollerhandler = TDefaultpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Padhna(bus uint16, उपकरण_2 uint16, function uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(उपकरण_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	Portlikhnadword(self.commandport, id)

	result1 := Portpadhnadword(self.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Likhna(bus uint16, उपकरण_2 uint16, function uint16, registeroffset uint32, value uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((उपकरण_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	Portlikhnadword(self.commandport, id)
	Portlikhnadword(self.dataport, value)
}
func (self *TPeripheralcomponentinterconnectcontroller) Dउपकरणhasfunctions(bus uint16, उपकरण_2 uint16) bool {
	result := self.Padhna(bus, उपकरण_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for उपकरण_2 := 0; उपकरण_2 < 32; उपकरण_2++ {

			var numberfunctions int = 1
			if self.Dउपकरणhasfunctions(uint16(bus), uint16(उपकरण_2)) == true {
				numberfunctions = 8
			} else {
				numberfunctions = 1
			}

			for function := 0; function < numberfunctions; function++ {
				var उपकरण TPeripheralcomponentinterconnectउपकरणdescriptor
				उपकरण = self.Getउपकरणdescriptor(uint16(bus), uint16(उपकरण_2), uint16(function))
				if उपकरण.Vendorid == 0x0000 || उपकरण.Vendorid == 0xFFFF {
					continue
				}

				for barnumber := 0; barnumber < 6; barnumber++ {
					var bar TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(उपकरण_2), uint16(function), uint16(barnumber))
					if bar.address_2 != 0 && (bar.regtype == 1) {
						उपकरण.Portbase = bar.address_2
					}

					self.Getdriver(उपकरण, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) Getउपकरणdescriptor(bus uint16, उपकरण_2 uint16, function uint16) TPeripheralcomponentinterconnectउपकरणdescriptor {
	var result TPeripheralcomponentinterconnectउपकरणdescriptor
	result = TPeripheralcomponentinterconnectउपकरणdescriptor{}
	result.bus = bus
	result.उपकरण_2 = उपकरण_2
	result.function = function

	result.Vendorid = uint16(self.Padhna(bus, उपकरण_2, function, 0x00))
	result.Dउपकरणid = uint16(self.Padhna(bus, उपकरण_2, function, 0x02))

	result.classid = uint8(self.Padhna(bus, उपकरण_2, function, 0x0b))
	result.subclassid = uint8(self.Padhna(bus, उपकरण_2, function, 0x0a))
	result.interfaceid = uint8(self.Padhna(bus, उपकरण_2, function, 0x09))

	result.revision = uint8(self.Padhna(bus, उपकरण_2, function, 0x08))
	result.Interrupt = uint32(self.Padhna(bus, उपकरण_2, function, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, उपकरण_2 uint16, function uint16, bar uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Padhna(bus, उपकरण_2, function, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if bar >= uint16(maxbars) {
		return result
	}

	barvalue := self.Padhna(bus, उपकरण_2, function, uint32(0x10+4*bar))

	if (barvalue & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = barvalue & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(उपकरण TPeripheralcomponentinterconnectउपकरणdescriptor, interrupts *TInterruptmanager) {

	self.ipcicontrollerhandler.Ongetdriver(उपकरण)

}
