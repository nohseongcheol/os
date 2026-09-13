package pci

import . "порта"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Вклученоgetdriver(уред TPeripheralcomponentinterconnectУредdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TСтандардноpcicontrollerhandler struct {
}

func (само TСтандардноpcicontrollerhandler) Вклученоgetdriver(уред TPeripheralcomponentinterconnectУредdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectУредdescriptor struct {
	Портаbase	uint32
	Interrupt	uint32

	bus		uint16
	уред_2		uint16
	функција	uint16

	VendorИд	uint16
	УредИд		uint16

	класаИд		uint8
	subclassИд	uint8
	иНТЕРФЕЈСИд	uint8

	revision	uint8
}

func (само *TPeripheralcomponentinterconnectУредdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataПорта		uint16
	командаПорта		uint16
}

func (само *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	само.dataПорта = 0xCFC
	само.командаПорта = 0xCF8

	само.ipcicontrollerhandler = TСтандардноpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		само.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (само *TPeripheralcomponentinterconnectcontroller) Читај(bus uint16, уред_2 uint16, функција uint16, registeroffset uint32) uint32 {
	var ид uint32 = 0
	ид = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(уред_2&0x1f) << 11) | (uint32(функција&0x07) << 8) | uint32(registeroffset&0xFC)

	ПортаЗапишиdword(само.командаПорта, ид)

	result1 := ПортаЧитајdword(само.dataПорта)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (само *TPeripheralcomponentinterconnectcontroller) Запиши(bus uint16, уред_2 uint16, функција uint16, registeroffset uint32, вредност uint32) {
	var ид uint32
	ид = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((уред_2&0x1f)<<11) | uint32((функција&0x07)<<8) | uint32(registeroffset&0xFC)
	ПортаЗапишиdword(само.командаПорта, ид)
	ПортаЗапишиdword(само.dataПорта, вредност)
}
func (само *TPeripheralcomponentinterconnectcontroller) УредhasФункции(bus uint16, уред_2 uint16) bool {
	result := само.Читај(bus, уред_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (само *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for уред_2 := 0; уред_2 < 32; уред_2++ {

			var numberФункции int = 1
			if само.УредhasФункции(uint16(bus), uint16(уред_2)) == true {
				numberФункции = 8
			} else {
				numberФункции = 1
			}

			for функција := 0; функција < numberФункции; функција++ {
				var уред TPeripheralcomponentinterconnectУредdescriptor
				уред = само.GetУредdescriptor(uint16(bus), uint16(уред_2), uint16(функција))
				if уред.VendorИд == 0x0000 || уред.VendorИд == 0xFFFF {
					continue
				}

				for лентаnumber := 0; лентаnumber < 6; лентаnumber++ {
					var лента TBaseaddressregister = само.Getbaseaddressregister(uint16(bus), uint16(уред_2), uint16(функција), uint16(лентаnumber))
					if лента.address_2 != 0 && (лента.regtype == 1) {
						уред.Портаbase = лента.address_2
					}

					само.Getdriver(уред, interrupts)

				}

			}

		}
	}
}
func (само *TPeripheralcomponentinterconnectcontroller) GetУредdescriptor(bus uint16, уред_2 uint16, функција uint16) TPeripheralcomponentinterconnectУредdescriptor {
	var result TPeripheralcomponentinterconnectУредdescriptor
	result = TPeripheralcomponentinterconnectУредdescriptor{}
	result.bus = bus
	result.уред_2 = уред_2
	result.функција = функција

	result.VendorИд = uint16(само.Читај(bus, уред_2, функција, 0x00))
	result.УредИд = uint16(само.Читај(bus, уред_2, функција, 0x02))

	result.класаИд = uint8(само.Читај(bus, уред_2, функција, 0x0b))
	result.subclassИд = uint8(само.Читај(bus, уред_2, функција, 0x0a))
	result.иНТЕРФЕЈСИд = uint8(само.Читај(bus, уред_2, функција, 0x09))

	result.revision = uint8(само.Читај(bus, уред_2, функција, 0x08))
	result.Interrupt = uint32(само.Читај(bus, уред_2, функција, 0x3C))

	return result
}
func (само *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, уред_2 uint16, функција uint16, лента uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := само.Читај(bus, уред_2, функција, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if лента >= uint16(maxbars) {
		return result
	}

	лентаВредност := само.Читај(bus, уред_2, функција, uint32(0x10+4*лента))

	if (лентаВредност & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = лентаВредност & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (само *TPeripheralcomponentinterconnectcontroller) Getdriver(уред TPeripheralcomponentinterconnectУредdescriptor, interrupts *TInterruptmanager) {

	само.ipcicontrollerhandler.Вклученоgetdriver(уред)

}
