/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "intrerupere"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Pornitgetdriver(dispozitiv TPeripheralcomponentinterconnectDispozitivdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TImplicităpcicontrollerhandler struct {
}

func (sine TImplicităpcicontrollerhandler) Pornitgetdriver(dispozitiv TPeripheralcomponentinterconnectDispozitivdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectDispozitivdescriptor struct {
	Portbase	uint32
	Intrerupere	uint32

	bus		uint16
	dispozitiv_2	uint16
	funcție		uint16

	Comerciantid	uint16
	Dispozitivid	uint16

	clasaid		uint8
	subclassid	uint8
	iNTERFAȚĂid	uint8

	revision	uint8
}

func (sine *TPeripheralcomponentinterconnectDispozitivdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	comandăport		uint16
}

func (sine *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	sine.dataport = 0xCFC
	sine.comandăport = 0xCF8

	sine.ipcicontrollerhandler = TImplicităpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		sine.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (sine *TPeripheralcomponentinterconnectcontroller) Citire(bus uint16, dispozitiv_2 uint16, funcție uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(dispozitiv_2&0x1f) << 11) | (uint32(funcție&0x07) << 8) | uint32(registeroffset&0xFC)

	PortScrieredword(sine.comandăport, id)

	result1 := PortCitiredword(sine.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (sine *TPeripheralcomponentinterconnectcontroller) Scriere(bus uint16, dispozitiv_2 uint16, funcție uint16, registeroffset uint32, valoare uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((dispozitiv_2&0x1f)<<11) | uint32((funcție&0x07)<<8) | uint32(registeroffset&0xFC)
	PortScrieredword(sine.comandăport, id)
	PortScrieredword(sine.dataport, valoare)
}
func (sine *TPeripheralcomponentinterconnectcontroller) DispozitivhasFuncții(bus uint16, dispozitiv_2 uint16) bool {
	result := sine.Citire(bus, dispozitiv_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (sine *TPeripheralcomponentinterconnectcontroller) Selecteazădriver(drivermanager *TDrivermanager, interrupts *TIntreruperemanager) {
	for bus := 0; bus < 8; bus++ {
		for dispozitiv_2 := 0; dispozitiv_2 < 32; dispozitiv_2++ {

			var numărFuncții int = 1
			if sine.DispozitivhasFuncții(uint16(bus), uint16(dispozitiv_2)) == true {
				numărFuncții = 8
			} else {
				numărFuncții = 1
			}

			for funcție := 0; funcție < numărFuncții; funcție++ {
				var dispozitiv TPeripheralcomponentinterconnectDispozitivdescriptor
				dispozitiv = sine.GetDispozitivdescriptor(uint16(bus), uint16(dispozitiv_2), uint16(funcție))
				if dispozitiv.Comerciantid == 0x0000 || dispozitiv.Comerciantid == 0xFFFF {
					continue
				}

				for barăNumăr := 0; barăNumăr < 6; barăNumăr++ {
					var bară TBaseaddressregister = sine.Getbaseaddressregister(uint16(bus), uint16(dispozitiv_2), uint16(funcție), uint16(barăNumăr))
					if bară.address_2 != 0 && (bară.regtype == 1) {
						dispozitiv.Portbase = bară.address_2
					}

					sine.Getdriver(dispozitiv, interrupts)

				}

			}

		}
	}
}
func (sine *TPeripheralcomponentinterconnectcontroller) GetDispozitivdescriptor(bus uint16, dispozitiv_2 uint16, funcție uint16) TPeripheralcomponentinterconnectDispozitivdescriptor {
	var result TPeripheralcomponentinterconnectDispozitivdescriptor
	result = TPeripheralcomponentinterconnectDispozitivdescriptor{}
	result.bus = bus
	result.dispozitiv_2 = dispozitiv_2
	result.funcție = funcție

	result.Comerciantid = uint16(sine.Citire(bus, dispozitiv_2, funcție, 0x00))
	result.Dispozitivid = uint16(sine.Citire(bus, dispozitiv_2, funcție, 0x02))

	result.clasaid = uint8(sine.Citire(bus, dispozitiv_2, funcție, 0x0b))
	result.subclassid = uint8(sine.Citire(bus, dispozitiv_2, funcție, 0x0a))
	result.iNTERFAȚĂid = uint8(sine.Citire(bus, dispozitiv_2, funcție, 0x09))

	result.revision = uint8(sine.Citire(bus, dispozitiv_2, funcție, 0x08))
	result.Intrerupere = uint32(sine.Citire(bus, dispozitiv_2, funcție, 0x3C))

	return result
}
func (sine *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, dispozitiv_2 uint16, funcție uint16, bară uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := sine.Citire(bus, dispozitiv_2, funcție, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if bară >= uint16(maxbars) {
		return result
	}

	barăValoare := sine.Citire(bus, dispozitiv_2, funcție, uint32(0x10+4*bară))

	if (barăValoare & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = barăValoare & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (sine *TPeripheralcomponentinterconnectcontroller) Getdriver(dispozitiv TPeripheralcomponentinterconnectDispozitivdescriptor, interrupts *TIntreruperemanager) {

	sine.ipcicontrollerhandler.Pornitgetdriver(dispozitiv)

}
