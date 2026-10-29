/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "umuyoboro"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Kurigetdriver(ububiko TPeripheralcomponentinterconnectUbubikodescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TMburabuzipcicontrollerhandler struct {
}

func (self TMburabuzipcicontrollerhandler) Kurigetdriver(ububiko TPeripheralcomponentinterconnectUbubikodescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectUbubikodescriptor struct {
	Umuyoborobase	uint32
	Interrupt	uint32

	bus		uint16
	ububiko_2	uint16
	function	uint16

	Vendorid	uint16
	Ububikoid	uint16

	classid		uint8
	subclassid	uint8
	interfaceid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectUbubikodescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataUmuyoboro		uint16
	icyowifuzaUmuyoboro	uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataUmuyoboro = 0xCFC
	self.icyowifuzaUmuyoboro = 0xCF8

	self.ipcicontrollerhandler = TMburabuzipcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Gusoma(bus uint16, ububiko_2 uint16, function uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(ububiko_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	Umuyoborokwandikadword(self.icyowifuzaUmuyoboro, id)

	result1 := Umuyoborogusomadword(self.dataUmuyoboro)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Kwandika(bus uint16, ububiko_2 uint16, function uint16, registeroffset uint32, agaciro uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((ububiko_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	Umuyoborokwandikadword(self.icyowifuzaUmuyoboro, id)
	Umuyoborokwandikadword(self.dataUmuyoboro, agaciro)
}
func (self *TPeripheralcomponentinterconnectcontroller) Ububikohasfunctions(bus uint16, ububiko_2 uint16) bool {
	result := self.Gusoma(bus, ububiko_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for ububiko_2 := 0; ububiko_2 < 32; ububiko_2++ {

			var numberfunctions int = 1
			if self.Ububikohasfunctions(uint16(bus), uint16(ububiko_2)) == true {
				numberfunctions = 8
			} else {
				numberfunctions = 1
			}

			for function := 0; function < numberfunctions; function++ {
				var ububiko TPeripheralcomponentinterconnectUbubikodescriptor
				ububiko = self.GetUbubikodescriptor(uint16(bus), uint16(ububiko_2), uint16(function))
				if ububiko.Vendorid == 0x0000 || ububiko.Vendorid == 0xFFFF {
					continue
				}

				for barnumber := 0; barnumber < 6; barnumber++ {
					var bar TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(ububiko_2), uint16(function), uint16(barnumber))
					if bar.address_2 != 0 && (bar.regtype == 1) {
						ububiko.Umuyoborobase = bar.address_2
					}

					self.Getdriver(ububiko, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetUbubikodescriptor(bus uint16, ububiko_2 uint16, function uint16) TPeripheralcomponentinterconnectUbubikodescriptor {
	var result TPeripheralcomponentinterconnectUbubikodescriptor
	result = TPeripheralcomponentinterconnectUbubikodescriptor{}
	result.bus = bus
	result.ububiko_2 = ububiko_2
	result.function = function

	result.Vendorid = uint16(self.Gusoma(bus, ububiko_2, function, 0x00))
	result.Ububikoid = uint16(self.Gusoma(bus, ububiko_2, function, 0x02))

	result.classid = uint8(self.Gusoma(bus, ububiko_2, function, 0x0b))
	result.subclassid = uint8(self.Gusoma(bus, ububiko_2, function, 0x0a))
	result.interfaceid = uint8(self.Gusoma(bus, ububiko_2, function, 0x09))

	result.revision = uint8(self.Gusoma(bus, ububiko_2, function, 0x08))
	result.Interrupt = uint32(self.Gusoma(bus, ububiko_2, function, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, ububiko_2 uint16, function uint16, bar uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Gusoma(bus, ububiko_2, function, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if bar >= uint16(maxbars) {
		return result
	}

	barAgaciro := self.Gusoma(bus, ububiko_2, function, uint32(0x10+4*bar))

	if (barAgaciro & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = barAgaciro & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(ububiko TPeripheralcomponentinterconnectUbubikodescriptor, interrupts *TInterruptmanager) {

	self.ipcicontrollerhandler.Kurigetdriver(ububiko)

}
