/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "poort"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Aangetdriver(apparaat TPeripheralcomponentinterconnectApparaatdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TStandaardpcicontrollerhandler struct {
}

func (zelf TStandaardpcicontrollerhandler) Aangetdriver(apparaat TPeripheralcomponentinterconnectApparaatdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectApparaatdescriptor struct {
	Poortbase	uint32
	Interrupt	uint32

	bus		uint16
	apparaat_2	uint16
	functie		uint16

	Verkoperid	uint16
	Apparaatid	uint16

	klasseid	uint8
	subclassid	uint8
	netwerkkaartid	uint8

	revision	uint8
}

func (zelf *TPeripheralcomponentinterconnectApparaatdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataPoort		uint16
	opdrachtPoort		uint16
}

func (zelf *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	zelf.dataPoort = 0xCFC
	zelf.opdrachtPoort = 0xCF8

	zelf.ipcicontrollerhandler = TStandaardpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		zelf.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var iAantal int = 0

func (zelf *TPeripheralcomponentinterconnectcontroller) Lezen(bus uint16, apparaat_2 uint16, functie uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(apparaat_2&0x1f) << 11) | (uint32(functie&0x07) << 8) | uint32(registeroffset&0xFC)

	PoortSchrijvendword(zelf.opdrachtPoort, id)

	rESULTAAT1 := PoortLezendword(zelf.dataPoort)
	rESULTAAT2 := (rESULTAAT1 >> (8 * (registeroffset % 4)))

	return rESULTAAT2
}

func (zelf *TPeripheralcomponentinterconnectcontroller) Schrijven(bus uint16, apparaat_2 uint16, functie uint16, registeroffset uint32, waarde uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((apparaat_2&0x1f)<<11) | uint32((functie&0x07)<<8) | uint32(registeroffset&0xFC)
	PoortSchrijvendword(zelf.opdrachtPoort, id)
	PoortSchrijvendword(zelf.dataPoort, waarde)
}
func (zelf *TPeripheralcomponentinterconnectcontroller) ApparaathasFuncties(bus uint16, apparaat_2 uint16) bool {
	rESULTAAT := zelf.Lezen(bus, apparaat_2, 0, 0x0E)
	if (rESULTAAT & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (zelf *TPeripheralcomponentinterconnectcontroller) Selecterendriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for apparaat_2 := 0; apparaat_2 < 32; apparaat_2++ {

			var getalFuncties int = 1
			if zelf.ApparaathasFuncties(uint16(bus), uint16(apparaat_2)) == true {
				getalFuncties = 8
			} else {
				getalFuncties = 1
			}

			for functie := 0; functie < getalFuncties; functie++ {
				var apparaat TPeripheralcomponentinterconnectApparaatdescriptor
				apparaat = zelf.GetApparaatdescriptor(uint16(bus), uint16(apparaat_2), uint16(functie))
				if apparaat.Verkoperid == 0x0000 || apparaat.Verkoperid == 0xFFFF {
					continue
				}

				for balkGetal := 0; balkGetal < 6; balkGetal++ {
					var balk TBaseaddressregister = zelf.Getbaseaddressregister(uint16(bus), uint16(apparaat_2), uint16(functie), uint16(balkGetal))
					if balk.address_2 != 0 && (balk.regtype == 1) {
						apparaat.Poortbase = balk.address_2
					}

					zelf.Getdriver(apparaat, interrupts)

				}

			}

		}
	}
}
func (zelf *TPeripheralcomponentinterconnectcontroller) GetApparaatdescriptor(bus uint16, apparaat_2 uint16, functie uint16) TPeripheralcomponentinterconnectApparaatdescriptor {
	var rESULTAAT TPeripheralcomponentinterconnectApparaatdescriptor
	rESULTAAT = TPeripheralcomponentinterconnectApparaatdescriptor{}
	rESULTAAT.bus = bus
	rESULTAAT.apparaat_2 = apparaat_2
	rESULTAAT.functie = functie

	rESULTAAT.Verkoperid = uint16(zelf.Lezen(bus, apparaat_2, functie, 0x00))
	rESULTAAT.Apparaatid = uint16(zelf.Lezen(bus, apparaat_2, functie, 0x02))

	rESULTAAT.klasseid = uint8(zelf.Lezen(bus, apparaat_2, functie, 0x0b))
	rESULTAAT.subclassid = uint8(zelf.Lezen(bus, apparaat_2, functie, 0x0a))
	rESULTAAT.netwerkkaartid = uint8(zelf.Lezen(bus, apparaat_2, functie, 0x09))

	rESULTAAT.revision = uint8(zelf.Lezen(bus, apparaat_2, functie, 0x08))
	rESULTAAT.Interrupt = uint32(zelf.Lezen(bus, apparaat_2, functie, 0x3C))

	return rESULTAAT
}
func (zelf *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, apparaat_2 uint16, functie uint16, balk uint16) TBaseaddressregister {
	var rESULTAAT TBaseaddressregister

	headertype := zelf.Lezen(bus, apparaat_2, functie, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if balk >= uint16(maxbars) {
		return rESULTAAT
	}

	balkWaarde := zelf.Lezen(bus, apparaat_2, functie, uint32(0x10+4*balk))

	if (balkWaarde & 0x1) != 0 {
		rESULTAAT.regtype = 1
	} else {
		rESULTAAT.regtype = 0
	}

	if rESULTAAT.regtype == 0 {
	} else {
		rESULTAAT.address_2 = balkWaarde & ^uint32(0x3)
		rESULTAAT.prefetchcapable = false
	}

	return rESULTAAT
}
func (zelf *TPeripheralcomponentinterconnectcontroller) Getdriver(apparaat TPeripheralcomponentinterconnectApparaatdescriptor, interrupts *TInterruptmanager) {

	zelf.ipcicontrollerhandler.Aangetdriver(apparaat)

}
