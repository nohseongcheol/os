package pci

import . "პორტი"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ongetdriver(მოწყობილობა TPeripheralcomponentinterconnectმოწყობილობაdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type Tნაგულისხმევიpcicontrollerhandler struct {
}

func (self Tნაგულისხმევიpcicontrollerhandler) Ongetdriver(მოწყობილობა TPeripheralcomponentinterconnectმოწყობილობაdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectმოწყობილობაdescriptor struct {
	Pპორტიbase	uint32
	Interrupt	uint32

	bus		uint16
	მოწყობილობა_2	uint16
	ფუნქცია		uint16

	Vendorid	uint16
	Dმოწყობილობაid	uint16

	კლასიid		uint8
	subclassid	uint8
	ინტერფეისიid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectმოწყობილობაdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataპორტი		uint16
	ბრძანებაპორტი		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataპორტი = 0xCFC
	self.ბრძანებაპორტი = 0xCF8

	self.ipcicontrollerhandler = Tნაგულისხმევიpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Rკითხვა(bus uint16, მოწყობილობა_2 uint16, ფუნქცია uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(მოწყობილობა_2&0x1f) << 11) | (uint32(ფუნქცია&0x07) << 8) | uint32(registeroffset&0xFC)

	Pპორტიჩაწერაdword(self.ბრძანებაპორტი, id)

	result1 := Pპორტიკითხვაdword(self.dataპორტი)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Wჩაწერა(bus uint16, მოწყობილობა_2 uint16, ფუნქცია uint16, registeroffset uint32, მნიშვნელობა uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((მოწყობილობა_2&0x1f)<<11) | uint32((ფუნქცია&0x07)<<8) | uint32(registeroffset&0xFC)
	Pპორტიჩაწერაdword(self.ბრძანებაპორტი, id)
	Pპორტიჩაწერაdword(self.dataპორტი, მნიშვნელობა)
}
func (self *TPeripheralcomponentinterconnectcontroller) Dმოწყობილობაhasfunctions(bus uint16, მოწყობილობა_2 uint16) bool {
	result := self.Rკითხვა(bus, მოწყობილობა_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for მოწყობილობა_2 := 0; მოწყობილობა_2 < 32; მოწყობილობა_2++ {

			var რიცხვიfunctions int = 1
			if self.Dმოწყობილობაhasfunctions(uint16(bus), uint16(მოწყობილობა_2)) == true {
				რიცხვიfunctions = 8
			} else {
				რიცხვიfunctions = 1
			}

			for ფუნქცია := 0; ფუნქცია < რიცხვიfunctions; ფუნქცია++ {
				var მოწყობილობა TPeripheralcomponentinterconnectმოწყობილობაdescriptor
				მოწყობილობა = self.Getმოწყობილობაdescriptor(uint16(bus), uint16(მოწყობილობა_2), uint16(ფუნქცია))
				if მოწყობილობა.Vendorid == 0x0000 || მოწყობილობა.Vendorid == 0xFFFF {
					continue
				}

				for ზოლირიცხვი := 0; ზოლირიცხვი < 6; ზოლირიცხვი++ {
					var ზოლი TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(მოწყობილობა_2), uint16(ფუნქცია), uint16(ზოლირიცხვი))
					if ზოლი.address_2 != 0 && (ზოლი.regtype == 1) {
						მოწყობილობა.Pპორტიbase = ზოლი.address_2
					}

					self.Getdriver(მოწყობილობა, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) Getმოწყობილობაdescriptor(bus uint16, მოწყობილობა_2 uint16, ფუნქცია uint16) TPeripheralcomponentinterconnectმოწყობილობაdescriptor {
	var result TPeripheralcomponentinterconnectმოწყობილობაdescriptor
	result = TPeripheralcomponentinterconnectმოწყობილობაdescriptor{}
	result.bus = bus
	result.მოწყობილობა_2 = მოწყობილობა_2
	result.ფუნქცია = ფუნქცია

	result.Vendorid = uint16(self.Rკითხვა(bus, მოწყობილობა_2, ფუნქცია, 0x00))
	result.Dმოწყობილობაid = uint16(self.Rკითხვა(bus, მოწყობილობა_2, ფუნქცია, 0x02))

	result.კლასიid = uint8(self.Rკითხვა(bus, მოწყობილობა_2, ფუნქცია, 0x0b))
	result.subclassid = uint8(self.Rკითხვა(bus, მოწყობილობა_2, ფუნქცია, 0x0a))
	result.ინტერფეისიid = uint8(self.Rკითხვა(bus, მოწყობილობა_2, ფუნქცია, 0x09))

	result.revision = uint8(self.Rკითხვა(bus, მოწყობილობა_2, ფუნქცია, 0x08))
	result.Interrupt = uint32(self.Rკითხვა(bus, მოწყობილობა_2, ფუნქცია, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, მოწყობილობა_2 uint16, ფუნქცია uint16, ზოლი uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Rკითხვა(bus, მოწყობილობა_2, ფუნქცია, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if ზოლი >= uint16(maxbars) {
		return result
	}

	ზოლიმნიშვნელობა := self.Rკითხვა(bus, მოწყობილობა_2, ფუნქცია, uint32(0x10+4*ზოლი))

	if (ზოლიმნიშვნელობა & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = ზოლიმნიშვნელობა & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(მოწყობილობა TPeripheralcomponentinterconnectმოწყობილობაdescriptor, interrupts *TInterruptmanager) {

	self.ipcicontrollerhandler.Ongetdriver(მოწყობილობა)

}
