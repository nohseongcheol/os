package pci

import . "պորտ"
import . "ընդհատել"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Միացնելgetdriver(սարք TPeripheralcomponentinterconnectՍարքdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TՀիմնականpcicontrollerhandler struct {
}

func (ինքնուրույն TՀիմնականpcicontrollerhandler) Միացնելgetdriver(սարք TPeripheralcomponentinterconnectՍարքdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectՍարքdescriptor struct {
	Պորտbase	uint32
	Ընդհատել	uint32

	bus		uint16
	սարք_2		uint16
	function	uint16

	Վաճառողid	uint16
	Սարքid		uint16

	կարգid		uint8
	subclassid	uint8
	ինտերֆեյսid	uint8

	revision	uint8
}

func (ինքնուրույն *TPeripheralcomponentinterconnectՍարքdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataՊորտ		uint16
	հրահանգՊորտ		uint16
}

func (ինքնուրույն *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	ինքնուրույն.dataՊորտ = 0xCFC
	ինքնուրույն.հրահանգՊորտ = 0xCF8

	ինքնուրույն.ipcicontrollerhandler = TՀիմնականpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		ինքնուրույն.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (ինքնուրույն *TPeripheralcomponentinterconnectcontroller) Ընթերցում(bus uint16, սարք_2 uint16, function uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(սարք_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	ՊորտԳրելdword(ինքնուրույն.հրահանգՊորտ, id)

	result1 := ՊորտԸնթերցումdword(ինքնուրույն.dataՊորտ)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (ինքնուրույն *TPeripheralcomponentinterconnectcontroller) Գրել(bus uint16, սարք_2 uint16, function uint16, registeroffset uint32, արժեք uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((սարք_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	ՊորտԳրելdword(ինքնուրույն.հրահանգՊորտ, id)
	ՊորտԳրելdword(ինքնուրույն.dataՊորտ, արժեք)
}
func (ինքնուրույն *TPeripheralcomponentinterconnectcontroller) Սարքhasfunctions(bus uint16, սարք_2 uint16) bool {
	result := ինքնուրույն.Ընթերցում(bus, սարք_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (ինքնուրույն *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TԸնդհատելmanager) {
	for bus := 0; bus < 8; bus++ {
		for սարք_2 := 0; սարք_2 < 32; սարք_2++ {

			var հԱՄԱՐfunctions int = 1
			if ինքնուրույն.Սարքhasfunctions(uint16(bus), uint16(սարք_2)) == true {
				հԱՄԱՐfunctions = 8
			} else {
				հԱՄԱՐfunctions = 1
			}

			for function := 0; function < հԱՄԱՐfunctions; function++ {
				var սարք TPeripheralcomponentinterconnectՍարքdescriptor
				սարք = ինքնուրույն.GetՍարքdescriptor(uint16(bus), uint16(սարք_2), uint16(function))
				if սարք.Վաճառողid == 0x0000 || սարք.Վաճառողid == 0xFFFF {
					continue
				}

				for գծիկՀԱՄԱՐ := 0; գծիկՀԱՄԱՐ < 6; գծիկՀԱՄԱՐ++ {
					var գծիկ TBaseaddressregister = ինքնուրույն.Getbaseaddressregister(uint16(bus), uint16(սարք_2), uint16(function), uint16(գծիկՀԱՄԱՐ))
					if գծիկ.address_2 != 0 && (գծիկ.regtype == 1) {
						սարք.Պորտbase = գծիկ.address_2
					}

					ինքնուրույն.Getdriver(սարք, interrupts)

				}

			}

		}
	}
}
func (ինքնուրույն *TPeripheralcomponentinterconnectcontroller) GetՍարքdescriptor(bus uint16, սարք_2 uint16, function uint16) TPeripheralcomponentinterconnectՍարքdescriptor {
	var result TPeripheralcomponentinterconnectՍարքdescriptor
	result = TPeripheralcomponentinterconnectՍարքdescriptor{}
	result.bus = bus
	result.սարք_2 = սարք_2
	result.function = function

	result.Վաճառողid = uint16(ինքնուրույն.Ընթերցում(bus, սարք_2, function, 0x00))
	result.Սարքid = uint16(ինքնուրույն.Ընթերցում(bus, սարք_2, function, 0x02))

	result.կարգid = uint8(ինքնուրույն.Ընթերցում(bus, սարք_2, function, 0x0b))
	result.subclassid = uint8(ինքնուրույն.Ընթերցում(bus, սարք_2, function, 0x0a))
	result.ինտերֆեյսid = uint8(ինքնուրույն.Ընթերցում(bus, սարք_2, function, 0x09))

	result.revision = uint8(ինքնուրույն.Ընթերցում(bus, սարք_2, function, 0x08))
	result.Ընդհատել = uint32(ինքնուրույն.Ընթերցում(bus, սարք_2, function, 0x3C))

	return result
}
func (ինքնուրույն *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, սարք_2 uint16, function uint16, գծիկ uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := ինքնուրույն.Ընթերցում(bus, սարք_2, function, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if գծիկ >= uint16(maxbars) {
		return result
	}

	գծիկԱրժեք := ինքնուրույն.Ընթերցում(bus, սարք_2, function, uint32(0x10+4*գծիկ))

	if (գծիկԱրժեք & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = գծիկԱրժեք & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (ինքնուրույն *TPeripheralcomponentinterconnectcontroller) Getdriver(սարք TPeripheralcomponentinterconnectՍարքdescriptor, interrupts *TԸնդհատելmanager) {

	ինքնուրույն.ipcicontrollerhandler.Միացնելgetdriver(սարք)

}
