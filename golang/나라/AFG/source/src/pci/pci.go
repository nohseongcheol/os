/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "درگاه"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Oروشنgetdriver(دستگاه TPeripheralcomponentinterconnectدستگاهdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TDefaultpcicontrollerhandler struct {
}

func (خود TDefaultpcicontrollerhandler) Oروشنgetdriver(دستگاه TPeripheralcomponentinterconnectدستگاهdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectدستگاهdescriptor struct {
	Pدرگاهbase	uint32
	Interrupt	uint32

	bus		uint16
	دستگاه_2	uint16
	تابع		uint16

	Vendorشناسه	uint16
	Dدستگاهشناسه	uint16

	ردهشناسه	uint8
	subclassشناسه	uint8
	واسطشناسه	uint8

	revision	uint8
}

func (خود *TPeripheralcomponentinterconnectدستگاهdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataدرگاه		uint16
	فرماندرگاه		uint16
}

func (خود *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	خود.dataدرگاه = 0xCFC
	خود.فرماندرگاه = 0xCF8

	خود.ipcicontrollerhandler = TDefaultpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		خود.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (خود *TPeripheralcomponentinterconnectcontroller) Rخواندن(bus uint16, دستگاه_2 uint16, تابع uint16, registeroffset uint32) uint32 {
	var شناسه uint32 = 0
	شناسه = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(دستگاه_2&0x1f) << 11) | (uint32(تابع&0x07) << 8) | uint32(registeroffset&0xFC)

	Pدرگاهنوشتنdword(خود.فرماندرگاه, شناسه)

	result1 := Pدرگاهخواندنdword(خود.dataدرگاه)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (خود *TPeripheralcomponentinterconnectcontroller) Wنوشتن(bus uint16, دستگاه_2 uint16, تابع uint16, registeroffset uint32, مقدار uint32) {
	var شناسه uint32
	شناسه = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((دستگاه_2&0x1f)<<11) | uint32((تابع&0x07)<<8) | uint32(registeroffset&0xFC)
	Pدرگاهنوشتنdword(خود.فرماندرگاه, شناسه)
	Pدرگاهنوشتنdword(خود.dataدرگاه, مقدار)
}
func (خود *TPeripheralcomponentinterconnectcontroller) Dدستگاهhasتابعها(bus uint16, دستگاه_2 uint16) bool {
	result := خود.Rخواندن(bus, دستگاه_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (خود *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for دستگاه_2 := 0; دستگاه_2 < 32; دستگاه_2++ {

			var numberتابعها int = 1
			if خود.Dدستگاهhasتابعها(uint16(bus), uint16(دستگاه_2)) == true {
				numberتابعها = 8
			} else {
				numberتابعها = 1
			}

			for تابع := 0; تابع < numberتابعها; تابع++ {
				var دستگاه TPeripheralcomponentinterconnectدستگاهdescriptor
				دستگاه = خود.Getدستگاهdescriptor(uint16(bus), uint16(دستگاه_2), uint16(تابع))
				if دستگاه.Vendorشناسه == 0x0000 || دستگاه.Vendorشناسه == 0xFFFF {
					continue
				}

				for نوارnumber := 0; نوارnumber < 6; نوارnumber++ {
					var نوار TBaseaddressregister = خود.Getbaseaddressregister(uint16(bus), uint16(دستگاه_2), uint16(تابع), uint16(نوارnumber))
					if نوار.address_2 != 0 && (نوار.regtype == 1) {
						دستگاه.Pدرگاهbase = نوار.address_2
					}

					خود.Getdriver(دستگاه, interrupts)

				}

			}

		}
	}
}
func (خود *TPeripheralcomponentinterconnectcontroller) Getدستگاهdescriptor(bus uint16, دستگاه_2 uint16, تابع uint16) TPeripheralcomponentinterconnectدستگاهdescriptor {
	var result TPeripheralcomponentinterconnectدستگاهdescriptor
	result = TPeripheralcomponentinterconnectدستگاهdescriptor{}
	result.bus = bus
	result.دستگاه_2 = دستگاه_2
	result.تابع = تابع

	result.Vendorشناسه = uint16(خود.Rخواندن(bus, دستگاه_2, تابع, 0x00))
	result.Dدستگاهشناسه = uint16(خود.Rخواندن(bus, دستگاه_2, تابع, 0x02))

	result.ردهشناسه = uint8(خود.Rخواندن(bus, دستگاه_2, تابع, 0x0b))
	result.subclassشناسه = uint8(خود.Rخواندن(bus, دستگاه_2, تابع, 0x0a))
	result.واسطشناسه = uint8(خود.Rخواندن(bus, دستگاه_2, تابع, 0x09))

	result.revision = uint8(خود.Rخواندن(bus, دستگاه_2, تابع, 0x08))
	result.Interrupt = uint32(خود.Rخواندن(bus, دستگاه_2, تابع, 0x3C))

	return result
}
func (خود *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, دستگاه_2 uint16, تابع uint16, نوار uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := خود.Rخواندن(bus, دستگاه_2, تابع, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if نوار >= uint16(maxbars) {
		return result
	}

	نوارمقدار := خود.Rخواندن(bus, دستگاه_2, تابع, uint32(0x10+4*نوار))

	if (نوارمقدار & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = نوارمقدار & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (خود *TPeripheralcomponentinterconnectcontroller) Getdriver(دستگاه TPeripheralcomponentinterconnectدستگاهdescriptor, interrupts *TInterruptmanager) {

	خود.ipcicontrollerhandler.Oروشنgetdriver(دستگاه)

}
