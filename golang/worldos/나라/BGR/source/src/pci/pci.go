/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "порт"
import . "прекъсване"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Вклgetdriver(устройство TPeripheralcomponentinterconnectУстройствоdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TПоподразбиранеpcicontrollerhandler struct {
}

func (себеси TПоподразбиранеpcicontrollerhandler) Вклgetdriver(устройство TPeripheralcomponentinterconnectУстройствоdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectУстройствоdescriptor struct {
	Портbase	uint32
	Прекъсване	uint32

	bus		uint16
	устройство_2	uint16
	функция		uint16

	ПроизводителИДЕНТИФИКАТОР	uint16
	УстройствоИДЕНТИФИКАТОР		uint16

	класИДЕНТИФИКАТОР	uint8
	subclassИДЕНТИФИКАТОР	uint8
	иНТЕРФЕЙСИДЕНТИФИКАТОР	uint8

	revision	uint8
}

func (себеси *TPeripheralcomponentinterconnectУстройствоdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataПорт		uint16
	командаПорт		uint16
}

func (себеси *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	себеси.dataПорт = 0xCFC
	себеси.командаПорт = 0xCF8

	себеси.ipcicontrollerhandler = TПоподразбиранеpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		себеси.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (себеси *TPeripheralcomponentinterconnectcontroller) Четене(bus uint16, устройство_2 uint16, функция uint16, registeroffset uint32) uint32 {
	var иДЕНТИФИКАТОР uint32 = 0
	иДЕНТИФИКАТОР = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(устройство_2&0x1f) << 11) | (uint32(функция&0x07) << 8) | uint32(registeroffset&0xFC)

	ПортПисанеdword(себеси.командаПорт, иДЕНТИФИКАТОР)

	рЕЗУЛТАТ1 := ПортЧетенеdword(себеси.dataПорт)
	рЕЗУЛТАТ2 := (рЕЗУЛТАТ1 >> (8 * (registeroffset % 4)))

	return рЕЗУЛТАТ2
}

func (себеси *TPeripheralcomponentinterconnectcontroller) Писане(bus uint16, устройство_2 uint16, функция uint16, registeroffset uint32, стойност uint32) {
	var иДЕНТИФИКАТОР uint32
	иДЕНТИФИКАТОР = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((устройство_2&0x1f)<<11) | uint32((функция&0x07)<<8) | uint32(registeroffset&0xFC)
	ПортПисанеdword(себеси.командаПорт, иДЕНТИФИКАТОР)
	ПортПисанеdword(себеси.dataПорт, стойност)
}
func (себеси *TPeripheralcomponentinterconnectcontroller) УстройствоhasФункции(bus uint16, устройство_2 uint16) bool {
	рЕЗУЛТАТ := себеси.Четене(bus, устройство_2, 0, 0x0E)
	if (рЕЗУЛТАТ & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (себеси *TPeripheralcomponentinterconnectcontroller) Избиранеdriver(drivermanager *TDrivermanager, interrupts *TПрекъсванеmanager) {
	for bus := 0; bus < 8; bus++ {
		for устройство_2 := 0; устройство_2 < 32; устройство_2++ {

			var числоФункции int = 1
			if себеси.УстройствоhasФункции(uint16(bus), uint16(устройство_2)) == true {
				числоФункции = 8
			} else {
				числоФункции = 1
			}

			for функция := 0; функция < числоФункции; функция++ {
				var устройство TPeripheralcomponentinterconnectУстройствоdescriptor
				устройство = себеси.GetУстройствоdescriptor(uint16(bus), uint16(устройство_2), uint16(функция))
				if устройство.ПроизводителИДЕНТИФИКАТОР == 0x0000 || устройство.ПроизводителИДЕНТИФИКАТОР == 0xFFFF {
					continue
				}

				for лентаЧисло := 0; лентаЧисло < 6; лентаЧисло++ {
					var лента TBaseaddressregister = себеси.Getbaseaddressregister(uint16(bus), uint16(устройство_2), uint16(функция), uint16(лентаЧисло))
					if лента.address_2 != 0 && (лента.regtype == 1) {
						устройство.Портbase = лента.address_2
					}

					себеси.Getdriver(устройство, interrupts)

				}

			}

		}
	}
}
func (себеси *TPeripheralcomponentinterconnectcontroller) GetУстройствоdescriptor(bus uint16, устройство_2 uint16, функция uint16) TPeripheralcomponentinterconnectУстройствоdescriptor {
	var рЕЗУЛТАТ TPeripheralcomponentinterconnectУстройствоdescriptor
	рЕЗУЛТАТ = TPeripheralcomponentinterconnectУстройствоdescriptor{}
	рЕЗУЛТАТ.bus = bus
	рЕЗУЛТАТ.устройство_2 = устройство_2
	рЕЗУЛТАТ.функция = функция

	рЕЗУЛТАТ.ПроизводителИДЕНТИФИКАТОР = uint16(себеси.Четене(bus, устройство_2, функция, 0x00))
	рЕЗУЛТАТ.УстройствоИДЕНТИФИКАТОР = uint16(себеси.Четене(bus, устройство_2, функция, 0x02))

	рЕЗУЛТАТ.класИДЕНТИФИКАТОР = uint8(себеси.Четене(bus, устройство_2, функция, 0x0b))
	рЕЗУЛТАТ.subclassИДЕНТИФИКАТОР = uint8(себеси.Четене(bus, устройство_2, функция, 0x0a))
	рЕЗУЛТАТ.иНТЕРФЕЙСИДЕНТИФИКАТОР = uint8(себеси.Четене(bus, устройство_2, функция, 0x09))

	рЕЗУЛТАТ.revision = uint8(себеси.Четене(bus, устройство_2, функция, 0x08))
	рЕЗУЛТАТ.Прекъсване = uint32(себеси.Четене(bus, устройство_2, функция, 0x3C))

	return рЕЗУЛТАТ
}
func (себеси *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, устройство_2 uint16, функция uint16, лента uint16) TBaseaddressregister {
	var рЕЗУЛТАТ TBaseaddressregister

	headertype := себеси.Четене(bus, устройство_2, функция, 0x0E) & 0x7F
	var максbars int = int(6 - (4 * headertype))
	if лента >= uint16(максbars) {
		return рЕЗУЛТАТ
	}

	лентаСтойност := себеси.Четене(bus, устройство_2, функция, uint32(0x10+4*лента))

	if (лентаСтойност & 0x1) != 0 {
		рЕЗУЛТАТ.regtype = 1
	} else {
		рЕЗУЛТАТ.regtype = 0
	}

	if рЕЗУЛТАТ.regtype == 0 {
	} else {
		рЕЗУЛТАТ.address_2 = лентаСтойност & ^uint32(0x3)
		рЕЗУЛТАТ.prefetchcapable = false
	}

	return рЕЗУЛТАТ
}
func (себеси *TPeripheralcomponentinterconnectcontroller) Getdriver(устройство TPeripheralcomponentinterconnectУстройствоdescriptor, interrupts *TПрекъсванеmanager) {

	себеси.ipcicontrollerhandler.Вклgetdriver(устройство)

}
