/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Tændtgetdriver(enhed TPeripheralcomponentinterconnectEnheddescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TStandardpcicontrollerhandler struct {
}

func (selv TStandardpcicontrollerhandler) Tændtgetdriver(enhed TPeripheralcomponentinterconnectEnheddescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectEnheddescriptor struct {
	Portbase	uint32
	Interrupt	uint32

	bus		uint16
	enhed_2		uint16
	funktion	uint16

	Forhandlerid	uint16
	Enhedid		uint16

	klasseid	uint8
	subclassid	uint8
	gRÆNSEFLADEid	uint8

	revision	uint8
}

func (selv *TPeripheralcomponentinterconnectEnheddescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	kommandoport		uint16
}

func (selv *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	selv.dataport = 0xCFC
	selv.kommandoport = 0xCF8

	selv.ipcicontrollerhandler = TStandardpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		selv.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var iAntal int = 0

func (selv *TPeripheralcomponentinterconnectcontroller) Læse(bus uint16, enhed_2 uint16, funktion uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(enhed_2&0x1f) << 11) | (uint32(funktion&0x07) << 8) | uint32(registeroffset&0xFC)

	PortSkrivedword(selv.kommandoport, id)

	result1 := PortLæsedword(selv.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (selv *TPeripheralcomponentinterconnectcontroller) Skrive(bus uint16, enhed_2 uint16, funktion uint16, registeroffset uint32, værdi uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((enhed_2&0x1f)<<11) | uint32((funktion&0x07)<<8) | uint32(registeroffset&0xFC)
	PortSkrivedword(selv.kommandoport, id)
	PortSkrivedword(selv.dataport, værdi)
}
func (selv *TPeripheralcomponentinterconnectcontroller) EnhedhasFunktioner(bus uint16, enhed_2 uint16) bool {
	result := selv.Læse(bus, enhed_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (selv *TPeripheralcomponentinterconnectcontroller) Vælgdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for enhed_2 := 0; enhed_2 < 32; enhed_2++ {

			var talFunktioner int = 1
			if selv.EnhedhasFunktioner(uint16(bus), uint16(enhed_2)) == true {
				talFunktioner = 8
			} else {
				talFunktioner = 1
			}

			for funktion := 0; funktion < talFunktioner; funktion++ {
				var enhed TPeripheralcomponentinterconnectEnheddescriptor
				enhed = selv.GetEnheddescriptor(uint16(bus), uint16(enhed_2), uint16(funktion))
				if enhed.Forhandlerid == 0x0000 || enhed.Forhandlerid == 0xFFFF {
					continue
				}

				for linjeTal := 0; linjeTal < 6; linjeTal++ {
					var linje TBaseaddressregister = selv.Getbaseaddressregister(uint16(bus), uint16(enhed_2), uint16(funktion), uint16(linjeTal))
					if linje.address_2 != 0 && (linje.regtype == 1) {
						enhed.Portbase = linje.address_2
					}

					selv.Getdriver(enhed, interrupts)

				}

			}

		}
	}
}
func (selv *TPeripheralcomponentinterconnectcontroller) GetEnheddescriptor(bus uint16, enhed_2 uint16, funktion uint16) TPeripheralcomponentinterconnectEnheddescriptor {
	var result TPeripheralcomponentinterconnectEnheddescriptor
	result = TPeripheralcomponentinterconnectEnheddescriptor{}
	result.bus = bus
	result.enhed_2 = enhed_2
	result.funktion = funktion

	result.Forhandlerid = uint16(selv.Læse(bus, enhed_2, funktion, 0x00))
	result.Enhedid = uint16(selv.Læse(bus, enhed_2, funktion, 0x02))

	result.klasseid = uint8(selv.Læse(bus, enhed_2, funktion, 0x0b))
	result.subclassid = uint8(selv.Læse(bus, enhed_2, funktion, 0x0a))
	result.gRÆNSEFLADEid = uint8(selv.Læse(bus, enhed_2, funktion, 0x09))

	result.revision = uint8(selv.Læse(bus, enhed_2, funktion, 0x08))
	result.Interrupt = uint32(selv.Læse(bus, enhed_2, funktion, 0x3C))

	return result
}
func (selv *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, enhed_2 uint16, funktion uint16, linje uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := selv.Læse(bus, enhed_2, funktion, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if linje >= uint16(maxbars) {
		return result
	}

	linjeVærdi := selv.Læse(bus, enhed_2, funktion, uint32(0x10+4*linje))

	if (linjeVærdi & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = linjeVærdi & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (selv *TPeripheralcomponentinterconnectcontroller) Getdriver(enhed TPeripheralcomponentinterconnectEnheddescriptor, interrupts *TInterruptmanager) {

	selv.ipcicontrollerhandler.Tændtgetdriver(enhed)

}
