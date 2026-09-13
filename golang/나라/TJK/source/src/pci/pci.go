package pci

import . "port"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ongetdriver(дастгоҳ TPeripheralcomponentinterconnectДастгоҳdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TСтандартӣpcicontrollerhandler struct {
}

func (self TСтандартӣpcicontrollerhandler) Ongetdriver(дастгоҳ TPeripheralcomponentinterconnectДастгоҳdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectДастгоҳdescriptor struct {
	Portbase	uint32
	Interrupt	uint32

	bus		uint16
	дастгоҳ_2	uint16
	функсия		uint16

	Vendorid	uint16
	Дастгоҳid	uint16

	синфid		uint8
	subclassid	uint8
	interfaceid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectДастгоҳdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	commandport		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataport = 0xCFC
	self.commandport = 0xCF8

	self.ipcicontrollerhandler = TСтандартӣpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Хондан(bus uint16, дастгоҳ_2 uint16, функсия uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(дастгоҳ_2&0x1f) << 11) | (uint32(функсия&0x07) << 8) | uint32(registeroffset&0xFC)

	PortНавиштанdword(self.commandport, id)

	result1 := PortХонданdword(self.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Навиштан(bus uint16, дастгоҳ_2 uint16, функсия uint16, registeroffset uint32, value uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((дастгоҳ_2&0x1f)<<11) | uint32((функсия&0x07)<<8) | uint32(registeroffset&0xFC)
	PortНавиштанdword(self.commandport, id)
	PortНавиштанdword(self.dataport, value)
}
func (self *TPeripheralcomponentinterconnectcontroller) Дастгоҳhasfunctions(bus uint16, дастгоҳ_2 uint16) bool {
	result := self.Хондан(bus, дастгоҳ_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for дастгоҳ_2 := 0; дастгоҳ_2 < 32; дастгоҳ_2++ {

			var numberfunctions int = 1
			if self.Дастгоҳhasfunctions(uint16(bus), uint16(дастгоҳ_2)) == true {
				numberfunctions = 8
			} else {
				numberfunctions = 1
			}

			for функсия := 0; функсия < numberfunctions; функсия++ {
				var дастгоҳ TPeripheralcomponentinterconnectДастгоҳdescriptor
				дастгоҳ = self.GetДастгоҳdescriptor(uint16(bus), uint16(дастгоҳ_2), uint16(функсия))
				if дастгоҳ.Vendorid == 0x0000 || дастгоҳ.Vendorid == 0xFFFF {
					continue
				}

				for barnumber := 0; barnumber < 6; barnumber++ {
					var bar TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(дастгоҳ_2), uint16(функсия), uint16(barnumber))
					if bar.address_2 != 0 && (bar.regtype == 1) {
						дастгоҳ.Portbase = bar.address_2
					}

					self.Getdriver(дастгоҳ, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetДастгоҳdescriptor(bus uint16, дастгоҳ_2 uint16, функсия uint16) TPeripheralcomponentinterconnectДастгоҳdescriptor {
	var result TPeripheralcomponentinterconnectДастгоҳdescriptor
	result = TPeripheralcomponentinterconnectДастгоҳdescriptor{}
	result.bus = bus
	result.дастгоҳ_2 = дастгоҳ_2
	result.функсия = функсия

	result.Vendorid = uint16(self.Хондан(bus, дастгоҳ_2, функсия, 0x00))
	result.Дастгоҳid = uint16(self.Хондан(bus, дастгоҳ_2, функсия, 0x02))

	result.синфid = uint8(self.Хондан(bus, дастгоҳ_2, функсия, 0x0b))
	result.subclassid = uint8(self.Хондан(bus, дастгоҳ_2, функсия, 0x0a))
	result.interfaceid = uint8(self.Хондан(bus, дастгоҳ_2, функсия, 0x09))

	result.revision = uint8(self.Хондан(bus, дастгоҳ_2, функсия, 0x08))
	result.Interrupt = uint32(self.Хондан(bus, дастгоҳ_2, функсия, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, дастгоҳ_2 uint16, функсия uint16, bar uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Хондан(bus, дастгоҳ_2, функсия, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if bar >= uint16(maxbars) {
		return result
	}

	barvalue := self.Хондан(bus, дастгоҳ_2, функсия, uint32(0x10+4*bar))

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
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(дастгоҳ TPeripheralcomponentinterconnectДастгоҳdescriptor, interrupts *TInterruptmanager) {

	self.ipcicontrollerhandler.Ongetdriver(дастгоҳ)

}
