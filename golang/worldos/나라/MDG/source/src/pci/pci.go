/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "irika"
import . "interrupt"
import . "konsoly"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ongetdriver(periferika TPeripheralcomponentinterconnectPeriferikadescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TTsotrapcicontrollerhandler struct {
}

func (nytena TTsotrapcicontrollerhandler) Ongetdriver(periferika TPeripheralcomponentinterconnectPeriferikadescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectPeriferikadescriptor struct {
	Irikabase	uint32
	Interrupt	uint32

	bus		uint16
	periferika_2	uint16
	function	uint16

	Vendorid	uint16
	Periferikaid	uint16

	sokajyid	uint8
	subclassid	uint8
	mPANERAid	uint8

	revision	uint8
}

func (nytena *TPeripheralcomponentinterconnectPeriferikadescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataIrika		uint16
	baikoIrika		uint16
}

func (nytena *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	nytena.dataIrika = 0xCFC
	nytena.baikoIrika = 0xCF8

	nytena.ipcicontrollerhandler = TTsotrapcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		nytena.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (nytena *TPeripheralcomponentinterconnectcontroller) Mamaky(bus uint16, periferika_2 uint16, function uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(periferika_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	IrikaManoratradword(nytena.baikoIrika, id)

	result1 := IrikaMamakydword(nytena.dataIrika)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (nytena *TPeripheralcomponentinterconnectcontroller) Manoratra(bus uint16, periferika_2 uint16, function uint16, registeroffset uint32, sanda uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((periferika_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	IrikaManoratradword(nytena.baikoIrika, id)
	IrikaManoratradword(nytena.dataIrika, sanda)
}
func (nytena *TPeripheralcomponentinterconnectcontroller) Periferikahasfunctions(bus uint16, periferika_2 uint16) bool {
	result := nytena.Mamaky(bus, periferika_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konsoly TKonsoly = TKonsoly{}

func (nytena *TPeripheralcomponentinterconnectcontroller) Selectdriver(driverMpandrindra *TDriverMpandrindra, interrupts *TInterruptMpandrindra) {
	for bus := 0; bus < 8; bus++ {
		for periferika_2 := 0; periferika_2 < 32; periferika_2++ {

			var numberfunctions int = 1
			if nytena.Periferikahasfunctions(uint16(bus), uint16(periferika_2)) == true {
				numberfunctions = 8
			} else {
				numberfunctions = 1
			}

			for function := 0; function < numberfunctions; function++ {
				var periferika TPeripheralcomponentinterconnectPeriferikadescriptor
				periferika = nytena.GetPeriferikadescriptor(uint16(bus), uint16(periferika_2), uint16(function))
				if periferika.Vendorid == 0x0000 || periferika.Vendorid == 0xFFFF {
					continue
				}

				for anjanumber := 0; anjanumber < 6; anjanumber++ {
					var anja TBaseaddressregister = nytena.Getbaseaddressregister(uint16(bus), uint16(periferika_2), uint16(function), uint16(anjanumber))
					if anja.address_2 != 0 && (anja.regtype == 1) {
						periferika.Irikabase = anja.address_2
					}

					nytena.Getdriver(periferika, interrupts)

				}

			}

		}
	}
}
func (nytena *TPeripheralcomponentinterconnectcontroller) GetPeriferikadescriptor(bus uint16, periferika_2 uint16, function uint16) TPeripheralcomponentinterconnectPeriferikadescriptor {
	var result TPeripheralcomponentinterconnectPeriferikadescriptor
	result = TPeripheralcomponentinterconnectPeriferikadescriptor{}
	result.bus = bus
	result.periferika_2 = periferika_2
	result.function = function

	result.Vendorid = uint16(nytena.Mamaky(bus, periferika_2, function, 0x00))
	result.Periferikaid = uint16(nytena.Mamaky(bus, periferika_2, function, 0x02))

	result.sokajyid = uint8(nytena.Mamaky(bus, periferika_2, function, 0x0b))
	result.subclassid = uint8(nytena.Mamaky(bus, periferika_2, function, 0x0a))
	result.mPANERAid = uint8(nytena.Mamaky(bus, periferika_2, function, 0x09))

	result.revision = uint8(nytena.Mamaky(bus, periferika_2, function, 0x08))
	result.Interrupt = uint32(nytena.Mamaky(bus, periferika_2, function, 0x3C))

	return result
}
func (nytena *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, periferika_2 uint16, function uint16, anja uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := nytena.Mamaky(bus, periferika_2, function, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if anja >= uint16(maxbars) {
		return result
	}

	anjaSanda := nytena.Mamaky(bus, periferika_2, function, uint32(0x10+4*anja))

	if (anjaSanda & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = anjaSanda & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (nytena *TPeripheralcomponentinterconnectcontroller) Getdriver(periferika TPeripheralcomponentinterconnectPeriferikadescriptor, interrupts *TInterruptMpandrindra) {

	nytena.ipcicontrollerhandler.Ongetdriver(periferika)

}
