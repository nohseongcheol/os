/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "порт"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ongetdriver(түзүлүшү TPeripheralcomponentinterconnectТүзүлүшүdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TЖарыяланбасpcicontrollerhandler struct {
}

func (self TЖарыяланбасpcicontrollerhandler) Ongetdriver(түзүлүшү TPeripheralcomponentinterconnectТүзүлүшүdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectТүзүлүшүdescriptor struct {
	Портbase	uint32
	Interrupt	uint32

	bus		uint16
	түзүлүшү_2	uint16
	function	uint16

	ИштепчыгаруучуИДЕНТИФИКАТОР	uint16
	ТүзүлүшүИДЕНТИФИКАТОР		uint16

	classИДЕНТИФИКАТОР	uint8
	subclassИДЕНТИФИКАТОР	uint8
	interfaceИДЕНТИФИКАТОР	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectТүзүлүшүdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataПорт		uint16
	командаПорт		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataПорт = 0xCFC
	self.командаПорт = 0xCF8

	self.ipcicontrollerhandler = TЖарыяланбасpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Окуу(bus uint16, түзүлүшү_2 uint16, function uint16, registeroffset uint32) uint32 {
	var иДЕНТИФИКАТОР uint32 = 0
	иДЕНТИФИКАТОР = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(түзүлүшү_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	ПортЖазууdword(self.командаПорт, иДЕНТИФИКАТОР)

	result1 := ПортОкууdword(self.dataПорт)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Жазуу(bus uint16, түзүлүшү_2 uint16, function uint16, registeroffset uint32, мааниси uint32) {
	var иДЕНТИФИКАТОР uint32
	иДЕНТИФИКАТОР = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((түзүлүшү_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	ПортЖазууdword(self.командаПорт, иДЕНТИФИКАТОР)
	ПортЖазууdword(self.dataПорт, мааниси)
}
func (self *TPeripheralcomponentinterconnectcontroller) Түзүлүшүhasfunctions(bus uint16, түзүлүшү_2 uint16) bool {
	result := self.Окуу(bus, түзүлүшү_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for түзүлүшү_2 := 0; түзүлүшү_2 < 32; түзүлүшү_2++ {

			var нОМЕРfunctions int = 1
			if self.Түзүлүшүhasfunctions(uint16(bus), uint16(түзүлүшү_2)) == true {
				нОМЕРfunctions = 8
			} else {
				нОМЕРfunctions = 1
			}

			for function := 0; function < нОМЕРfunctions; function++ {
				var түзүлүшү TPeripheralcomponentinterconnectТүзүлүшүdescriptor
				түзүлүшү = self.GetТүзүлүшүdescriptor(uint16(bus), uint16(түзүлүшү_2), uint16(function))
				if түзүлүшү.ИштепчыгаруучуИДЕНТИФИКАТОР == 0x0000 || түзүлүшү.ИштепчыгаруучуИДЕНТИФИКАТОР == 0xFFFF {
					continue
				}

				for панельНОМЕР := 0; панельНОМЕР < 6; панельНОМЕР++ {
					var панель TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(түзүлүшү_2), uint16(function), uint16(панельНОМЕР))
					if панель.address_2 != 0 && (панель.regtype == 1) {
						түзүлүшү.Портbase = панель.address_2
					}

					self.Getdriver(түзүлүшү, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetТүзүлүшүdescriptor(bus uint16, түзүлүшү_2 uint16, function uint16) TPeripheralcomponentinterconnectТүзүлүшүdescriptor {
	var result TPeripheralcomponentinterconnectТүзүлүшүdescriptor
	result = TPeripheralcomponentinterconnectТүзүлүшүdescriptor{}
	result.bus = bus
	result.түзүлүшү_2 = түзүлүшү_2
	result.function = function

	result.ИштепчыгаруучуИДЕНТИФИКАТОР = uint16(self.Окуу(bus, түзүлүшү_2, function, 0x00))
	result.ТүзүлүшүИДЕНТИФИКАТОР = uint16(self.Окуу(bus, түзүлүшү_2, function, 0x02))

	result.classИДЕНТИФИКАТОР = uint8(self.Окуу(bus, түзүлүшү_2, function, 0x0b))
	result.subclassИДЕНТИФИКАТОР = uint8(self.Окуу(bus, түзүлүшү_2, function, 0x0a))
	result.interfaceИДЕНТИФИКАТОР = uint8(self.Окуу(bus, түзүлүшү_2, function, 0x09))

	result.revision = uint8(self.Окуу(bus, түзүлүшү_2, function, 0x08))
	result.Interrupt = uint32(self.Окуу(bus, түзүлүшү_2, function, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, түзүлүшү_2 uint16, function uint16, панель uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Окуу(bus, түзүлүшү_2, function, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if панель >= uint16(maxbars) {
		return result
	}

	панельМааниси := self.Окуу(bus, түзүлүшү_2, function, uint32(0x10+4*панель))

	if (панельМааниси & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = панельМааниси & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(түзүлүшү TPeripheralcomponentinterconnectТүзүлүшүdescriptor, interrupts *TInterruptmanager) {

	self.ipcicontrollerhandler.Ongetdriver(түзүлүшү)

}
