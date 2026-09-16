/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "avbrudd"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Pågetdriver(enhet TPeripheralcomponentinterconnectEnhetdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TStandardpcicontrollerhandler struct {
}

func (selv TStandardpcicontrollerhandler) Pågetdriver(enhet TPeripheralcomponentinterconnectEnhetdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectEnhetdescriptor struct {
	Portbase	uint32
	Avbrudd		uint32

	bus		uint16
	enhet_2		uint16
	funksjon	uint16

	Leverandørid	uint16
	Enhetid		uint16

	klasseid	uint8
	subclassid	uint8
	gRENSESNITTid	uint8

	revision	uint8
}

func (selv *TPeripheralcomponentinterconnectEnhetdescriptor) Init() {
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

var iAntall int = 0

func (selv *TPeripheralcomponentinterconnectcontroller) Les(bus uint16, enhet_2 uint16, funksjon uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(enhet_2&0x1f) << 11) | (uint32(funksjon&0x07) << 8) | uint32(registeroffset&0xFC)

	PortSkrivdword(selv.kommandoport, id)

	result1 := PortLesdword(selv.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (selv *TPeripheralcomponentinterconnectcontroller) Skriv(bus uint16, enhet_2 uint16, funksjon uint16, registeroffset uint32, verdi uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((enhet_2&0x1f)<<11) | uint32((funksjon&0x07)<<8) | uint32(registeroffset&0xFC)
	PortSkrivdword(selv.kommandoport, id)
	PortSkrivdword(selv.dataport, verdi)
}
func (selv *TPeripheralcomponentinterconnectcontroller) EnhethasFunksjoner(bus uint16, enhet_2 uint16) bool {
	result := selv.Les(bus, enhet_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (selv *TPeripheralcomponentinterconnectcontroller) Velgdriver(drivermanager *TDrivermanager, interrupts *TAvbruddmanager) {
	for bus := 0; bus < 8; bus++ {
		for enhet_2 := 0; enhet_2 < 32; enhet_2++ {

			var tallFunksjoner int = 1
			if selv.EnhethasFunksjoner(uint16(bus), uint16(enhet_2)) == true {
				tallFunksjoner = 8
			} else {
				tallFunksjoner = 1
			}

			for funksjon := 0; funksjon < tallFunksjoner; funksjon++ {
				var enhet TPeripheralcomponentinterconnectEnhetdescriptor
				enhet = selv.GetEnhetdescriptor(uint16(bus), uint16(enhet_2), uint16(funksjon))
				if enhet.Leverandørid == 0x0000 || enhet.Leverandørid == 0xFFFF {
					continue
				}

				for linjeTall := 0; linjeTall < 6; linjeTall++ {
					var linje TBaseaddressregister = selv.Getbaseaddressregister(uint16(bus), uint16(enhet_2), uint16(funksjon), uint16(linjeTall))
					if linje.address_2 != 0 && (linje.regtype == 1) {
						enhet.Portbase = linje.address_2
					}

					selv.Getdriver(enhet, interrupts)

				}

			}

		}
	}
}
func (selv *TPeripheralcomponentinterconnectcontroller) GetEnhetdescriptor(bus uint16, enhet_2 uint16, funksjon uint16) TPeripheralcomponentinterconnectEnhetdescriptor {
	var result TPeripheralcomponentinterconnectEnhetdescriptor
	result = TPeripheralcomponentinterconnectEnhetdescriptor{}
	result.bus = bus
	result.enhet_2 = enhet_2
	result.funksjon = funksjon

	result.Leverandørid = uint16(selv.Les(bus, enhet_2, funksjon, 0x00))
	result.Enhetid = uint16(selv.Les(bus, enhet_2, funksjon, 0x02))

	result.klasseid = uint8(selv.Les(bus, enhet_2, funksjon, 0x0b))
	result.subclassid = uint8(selv.Les(bus, enhet_2, funksjon, 0x0a))
	result.gRENSESNITTid = uint8(selv.Les(bus, enhet_2, funksjon, 0x09))

	result.revision = uint8(selv.Les(bus, enhet_2, funksjon, 0x08))
	result.Avbrudd = uint32(selv.Les(bus, enhet_2, funksjon, 0x3C))

	return result
}
func (selv *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, enhet_2 uint16, funksjon uint16, linje uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := selv.Les(bus, enhet_2, funksjon, 0x0E) & 0x7F
	var maksbars int = int(6 - (4 * headertype))
	if linje >= uint16(maksbars) {
		return result
	}

	linjeVerdi := selv.Les(bus, enhet_2, funksjon, uint32(0x10+4*linje))

	if (linjeVerdi & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = linjeVerdi & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (selv *TPeripheralcomponentinterconnectcontroller) Getdriver(enhet TPeripheralcomponentinterconnectEnhetdescriptor, interrupts *TAvbruddmanager) {

	selv.ipcicontrollerhandler.Pågetdriver(enhet)

}
