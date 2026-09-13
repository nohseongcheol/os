package pci

import . "پورٹ"
import . "مداخلت"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Oچالوgetdriver(آلہ TPeripheralcomponentinterconnectآلہdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type Tطےشدہpcicontrollerhandler struct {
}

func (self Tطےشدہpcicontrollerhandler) Oچالوgetdriver(آلہ TPeripheralcomponentinterconnectآلہdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectآلہdescriptor struct {
	Pپورٹbase	uint32
	Iمداخلت		uint32

	bus		uint16
	آلہ_2		uint16
	function	uint16

	Vفروشندہآئیڈی	uint16
	Dآلہآئیڈی	uint16

	classآئیڈی	uint8
	subclassآئیڈی	uint8
	مواجہآئیڈی	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectآلہdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataپورٹ		uint16
	کمانڈپورٹ		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataپورٹ = 0xCFC
	self.کمانڈپورٹ = 0xCF8

	self.ipcicontrollerhandler = Tطےشدہpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Rپڑھیں(bus uint16, آلہ_2 uint16, function uint16, registeroffset uint32) uint32 {
	var آئیڈی uint32 = 0
	آئیڈی = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(آلہ_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	Pپورٹلکھیںdword(self.کمانڈپورٹ, آئیڈی)

	result1 := Pپورٹپڑھیںdword(self.dataپورٹ)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Wلکھیں(bus uint16, آلہ_2 uint16, function uint16, registeroffset uint32, قدر uint32) {
	var آئیڈی uint32
	آئیڈی = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((آلہ_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	Pپورٹلکھیںdword(self.کمانڈپورٹ, آئیڈی)
	Pپورٹلکھیںdword(self.dataپورٹ, قدر)
}
func (self *TPeripheralcomponentinterconnectcontroller) Dآلہhasfunctions(bus uint16, آلہ_2 uint16) bool {
	result := self.Rپڑھیں(bus, آلہ_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Sمنتخبکریںdriver(drivermanager *TDrivermanager, interrupts *Tمداخلتmanager) {
	for bus := 0; bus < 8; bus++ {
		for آلہ_2 := 0; آلہ_2 < 32; آلہ_2++ {

			var numberfunctions int = 1
			if self.Dآلہhasfunctions(uint16(bus), uint16(آلہ_2)) == true {
				numberfunctions = 8
			} else {
				numberfunctions = 1
			}

			for function := 0; function < numberfunctions; function++ {
				var آلہ TPeripheralcomponentinterconnectآلہdescriptor
				آلہ = self.Getآلہdescriptor(uint16(bus), uint16(آلہ_2), uint16(function))
				if آلہ.Vفروشندہآئیڈی == 0x0000 || آلہ.Vفروشندہآئیڈی == 0xFFFF {
					continue
				}

				for barnumber := 0; barnumber < 6; barnumber++ {
					var bar TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(آلہ_2), uint16(function), uint16(barnumber))
					if bar.address_2 != 0 && (bar.regtype == 1) {
						آلہ.Pپورٹbase = bar.address_2
					}

					self.Getdriver(آلہ, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) Getآلہdescriptor(bus uint16, آلہ_2 uint16, function uint16) TPeripheralcomponentinterconnectآلہdescriptor {
	var result TPeripheralcomponentinterconnectآلہdescriptor
	result = TPeripheralcomponentinterconnectآلہdescriptor{}
	result.bus = bus
	result.آلہ_2 = آلہ_2
	result.function = function

	result.Vفروشندہآئیڈی = uint16(self.Rپڑھیں(bus, آلہ_2, function, 0x00))
	result.Dآلہآئیڈی = uint16(self.Rپڑھیں(bus, آلہ_2, function, 0x02))

	result.classآئیڈی = uint8(self.Rپڑھیں(bus, آلہ_2, function, 0x0b))
	result.subclassآئیڈی = uint8(self.Rپڑھیں(bus, آلہ_2, function, 0x0a))
	result.مواجہآئیڈی = uint8(self.Rپڑھیں(bus, آلہ_2, function, 0x09))

	result.revision = uint8(self.Rپڑھیں(bus, آلہ_2, function, 0x08))
	result.Iمداخلت = uint32(self.Rپڑھیں(bus, آلہ_2, function, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, آلہ_2 uint16, function uint16, bar uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Rپڑھیں(bus, آلہ_2, function, 0x0E) & 0x7F
	var زیادہbars int = int(6 - (4 * headertype))
	if bar >= uint16(زیادہbars) {
		return result
	}

	barقدر := self.Rپڑھیں(bus, آلہ_2, function, uint32(0x10+4*bar))

	if (barقدر & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = barقدر & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(آلہ TPeripheralcomponentinterconnectآلہdescriptor, interrupts *Tمداخلتmanager) {

	self.ipcicontrollerhandler.Oچالوgetdriver(آلہ)

}
