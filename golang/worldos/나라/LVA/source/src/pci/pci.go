/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "ports"
import . "pārtraukums"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ieslēgtsgetdriver(ierīce TPeripheralcomponentinterconnectIerīcedescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TNoklusētaispcicontrollerhandler struct {
}

func (pats TNoklusētaispcicontrollerhandler) Ieslēgtsgetdriver(ierīce TPeripheralcomponentinterconnectIerīcedescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectIerīcedescriptor struct {
	Portsbase	uint32
	Pārtraukums	uint32

	bus		uint16
	ierīce_2	uint16
	funkcija	uint16

	Ražotājsid	uint16
	Ierīceid	uint16

	klaseid		uint8
	subclassid	uint8
	sASKARNEid	uint8

	revision	uint8
}

func (pats *TPeripheralcomponentinterconnectIerīcedescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataPorts		uint16
	komandaPorts		uint16
}

func (pats *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	pats.dataPorts = 0xCFC
	pats.komandaPorts = 0xCF8

	pats.ipcicontrollerhandler = TNoklusētaispcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		pats.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (pats *TPeripheralcomponentinterconnectcontroller) Lasīt(bus uint16, ierīce_2 uint16, funkcija uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(ierīce_2&0x1f) << 11) | (uint32(funkcija&0x07) << 8) | uint32(registeroffset&0xFC)

	PortsRakstītdword(pats.komandaPorts, id)

	result1 := PortsLasītdword(pats.dataPorts)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (pats *TPeripheralcomponentinterconnectcontroller) Rakstīt(bus uint16, ierīce_2 uint16, funkcija uint16, registeroffset uint32, vērtība uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((ierīce_2&0x1f)<<11) | uint32((funkcija&0x07)<<8) | uint32(registeroffset&0xFC)
	PortsRakstītdword(pats.komandaPorts, id)
	PortsRakstītdword(pats.dataPorts, vērtība)
}
func (pats *TPeripheralcomponentinterconnectcontroller) IerīcehasFunkcijas(bus uint16, ierīce_2 uint16) bool {
	result := pats.Lasīt(bus, ierīce_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (pats *TPeripheralcomponentinterconnectcontroller) Atlasītdriver(drivermanager *TDrivermanager, interrupts *TPārtraukumsmanager) {
	for bus := 0; bus < 8; bus++ {
		for ierīce_2 := 0; ierīce_2 < 32; ierīce_2++ {

			var skaitlisFunkcijas int = 1
			if pats.IerīcehasFunkcijas(uint16(bus), uint16(ierīce_2)) == true {
				skaitlisFunkcijas = 8
			} else {
				skaitlisFunkcijas = 1
			}

			for funkcija := 0; funkcija < skaitlisFunkcijas; funkcija++ {
				var ierīce TPeripheralcomponentinterconnectIerīcedescriptor
				ierīce = pats.GetIerīcedescriptor(uint16(bus), uint16(ierīce_2), uint16(funkcija))
				if ierīce.Ražotājsid == 0x0000 || ierīce.Ražotājsid == 0xFFFF {
					continue
				}

				for joslaSkaitlis := 0; joslaSkaitlis < 6; joslaSkaitlis++ {
					var josla TBaseaddressregister = pats.Getbaseaddressregister(uint16(bus), uint16(ierīce_2), uint16(funkcija), uint16(joslaSkaitlis))
					if josla.address_2 != 0 && (josla.regtype == 1) {
						ierīce.Portsbase = josla.address_2
					}

					pats.Getdriver(ierīce, interrupts)

				}

			}

		}
	}
}
func (pats *TPeripheralcomponentinterconnectcontroller) GetIerīcedescriptor(bus uint16, ierīce_2 uint16, funkcija uint16) TPeripheralcomponentinterconnectIerīcedescriptor {
	var result TPeripheralcomponentinterconnectIerīcedescriptor
	result = TPeripheralcomponentinterconnectIerīcedescriptor{}
	result.bus = bus
	result.ierīce_2 = ierīce_2
	result.funkcija = funkcija

	result.Ražotājsid = uint16(pats.Lasīt(bus, ierīce_2, funkcija, 0x00))
	result.Ierīceid = uint16(pats.Lasīt(bus, ierīce_2, funkcija, 0x02))

	result.klaseid = uint8(pats.Lasīt(bus, ierīce_2, funkcija, 0x0b))
	result.subclassid = uint8(pats.Lasīt(bus, ierīce_2, funkcija, 0x0a))
	result.sASKARNEid = uint8(pats.Lasīt(bus, ierīce_2, funkcija, 0x09))

	result.revision = uint8(pats.Lasīt(bus, ierīce_2, funkcija, 0x08))
	result.Pārtraukums = uint32(pats.Lasīt(bus, ierīce_2, funkcija, 0x3C))

	return result
}
func (pats *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, ierīce_2 uint16, funkcija uint16, josla uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := pats.Lasīt(bus, ierīce_2, funkcija, 0x0E) & 0x7F
	var maksbars int = int(6 - (4 * headertype))
	if josla >= uint16(maksbars) {
		return result
	}

	joslaVērtība := pats.Lasīt(bus, ierīce_2, funkcija, uint32(0x10+4*josla))

	if (joslaVērtība & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = joslaVērtība & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (pats *TPeripheralcomponentinterconnectcontroller) Getdriver(ierīce TPeripheralcomponentinterconnectIerīcedescriptor, interrupts *TPārtraukumsmanager) {

	pats.ipcicontrollerhandler.Ieslēgtsgetdriver(ierīce)

}
