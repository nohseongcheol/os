package pci

import . "port"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Yoqishgetdriver(uskuna TPeripheralcomponentinterconnectUskunadescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TAndozapcicontrollerhandler struct {
}

func (self TAndozapcicontrollerhandler) Yoqishgetdriver(uskuna TPeripheralcomponentinterconnectUskunadescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectUskunadescriptor struct {
	Portbase	uint32
	Interrupt	uint32

	bus		uint16
	uskuna_2	uint16
	function	uint16

	Ishlabchiqaruvchiid	uint16
	Uskunaid		uint16

	sinfid		uint8
	subclassid	uint8
	interfeysid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectUskunadescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	buyruqport		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataport = 0xCFC
	self.buyruqport = 0xCF8

	self.ipcicontrollerhandler = TAndozapcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Oʻqish(bus uint16, uskuna_2 uint16, function uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(uskuna_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	PortYozishdword(self.buyruqport, id)

	result1 := PortOʻqishdword(self.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Yozish(bus uint16, uskuna_2 uint16, function uint16, registeroffset uint32, qiymat uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((uskuna_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	PortYozishdword(self.buyruqport, id)
	PortYozishdword(self.dataport, qiymat)
}
func (self *TPeripheralcomponentinterconnectcontroller) Uskunahasfunctions(bus uint16, uskuna_2 uint16) bool {
	result := self.Oʻqish(bus, uskuna_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for uskuna_2 := 0; uskuna_2 < 32; uskuna_2++ {

			var rAQAMfunctions int = 1
			if self.Uskunahasfunctions(uint16(bus), uint16(uskuna_2)) == true {
				rAQAMfunctions = 8
			} else {
				rAQAMfunctions = 1
			}

			for function := 0; function < rAQAMfunctions; function++ {
				var uskuna TPeripheralcomponentinterconnectUskunadescriptor
				uskuna = self.GetUskunadescriptor(uint16(bus), uint16(uskuna_2), uint16(function))
				if uskuna.Ishlabchiqaruvchiid == 0x0000 || uskuna.Ishlabchiqaruvchiid == 0xFFFF {
					continue
				}

				for barRAQAM := 0; barRAQAM < 6; barRAQAM++ {
					var bar TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(uskuna_2), uint16(function), uint16(barRAQAM))
					if bar.address_2 != 0 && (bar.regtype == 1) {
						uskuna.Portbase = bar.address_2
					}

					self.Getdriver(uskuna, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetUskunadescriptor(bus uint16, uskuna_2 uint16, function uint16) TPeripheralcomponentinterconnectUskunadescriptor {
	var result TPeripheralcomponentinterconnectUskunadescriptor
	result = TPeripheralcomponentinterconnectUskunadescriptor{}
	result.bus = bus
	result.uskuna_2 = uskuna_2
	result.function = function

	result.Ishlabchiqaruvchiid = uint16(self.Oʻqish(bus, uskuna_2, function, 0x00))
	result.Uskunaid = uint16(self.Oʻqish(bus, uskuna_2, function, 0x02))

	result.sinfid = uint8(self.Oʻqish(bus, uskuna_2, function, 0x0b))
	result.subclassid = uint8(self.Oʻqish(bus, uskuna_2, function, 0x0a))
	result.interfeysid = uint8(self.Oʻqish(bus, uskuna_2, function, 0x09))

	result.revision = uint8(self.Oʻqish(bus, uskuna_2, function, 0x08))
	result.Interrupt = uint32(self.Oʻqish(bus, uskuna_2, function, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, uskuna_2 uint16, function uint16, bar uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Oʻqish(bus, uskuna_2, function, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if bar >= uint16(maxbars) {
		return result
	}

	barQiymat := self.Oʻqish(bus, uskuna_2, function, uint32(0x10+4*bar))

	if (barQiymat & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = barQiymat & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(uskuna TPeripheralcomponentinterconnectUskunadescriptor, interrupts *TInterruptmanager) {

	self.ipcicontrollerhandler.Yoqishgetdriver(uskuna)

}
