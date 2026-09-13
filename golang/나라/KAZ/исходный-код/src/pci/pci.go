package pci

import . "порт"
import . "прерывание"
import . "консоль"
import . "драйвер/драйвер"

type Ipciконтроллерhandler interface {
	Приgetдрайвер(устройство TPeripheralcomponentinterconnectУстройствоdescriptor)
}

var ipciконтроллерhandler Ipciконтроллерhandler

type TПоумолчаниюpciконтроллерhandler struct {
}

func (текущий TПоумолчаниюpciконтроллерhandler) Приgetдрайвер(устройство TPeripheralcomponentinterconnectУстройствоdescriptor) {
}

type TBaseaddressрегистр struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectУстройствоdescriptor struct {
	Портbase	uint32
	Прерывание	uint32

	bus		uint16
	устройство_2	uint16
	функция		uint16

	ПроизводительИДЕНТИФИКАТОР	uint16
	УстройствоИДЕНТИФИКАТОР		uint16

	классИДЕНТИФИКАТОР	uint8
	subclassИДЕНТИФИКАТОР	uint8
	интерфейсИДЕНТИФИКАТОР	uint8

	revision	uint8
}

func (текущий *TPeripheralcomponentinterconnectУстройствоdescriptor) Init() {
}

type TPeripheralcomponentinterconnectконтроллер struct {
	ipciконтроллерhandler	Ipciконтроллерhandler
	данныепорт		uint16
	командапорт		uint16
}

func (текущий *TPeripheralcomponentinterconnectконтроллер) Init(ipciконтроллерhandler Ipciконтроллерhandler) {
	текущий.данныепорт = 0xCFC
	текущий.командапорт = 0xCF8

	текущий.ipciконтроллерhandler = TПоумолчаниюpciконтроллерhandler{}
	if ipciконтроллерhandler != nil {
		текущий.ipciконтроллерhandler = ipciконтроллерhandler
	}
}

var iКоличество int = 0

func (текущий *TPeripheralcomponentinterconnectконтроллер) Читать(bus uint16, устройство_2 uint16, функция uint16, registeroffset uint32) uint32 {
	var иДЕНТИФИКАТОР uint32 = 0
	иДЕНТИФИКАТОР = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(устройство_2&0x1f) << 11) | (uint32(функция&0x07) << 8) | uint32(registeroffset&0xFC)

	Портписатьdword(текущий.командапорт, иДЕНТИФИКАТОР)

	рЕЗУЛЬТАТ1 := Портчитатьdword(текущий.данныепорт)
	рЕЗУЛЬТАТ2 := (рЕЗУЛЬТАТ1 >> (8 * (registeroffset % 4)))

	return рЕЗУЛЬТАТ2
}

func (текущий *TPeripheralcomponentinterconnectконтроллер) Писать(bus uint16, устройство_2 uint16, функция uint16, registeroffset uint32, значение uint32) {
	var иДЕНТИФИКАТОР uint32
	иДЕНТИФИКАТОР = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((устройство_2&0x1f)<<11) | uint32((функция&0x07)<<8) | uint32(registeroffset&0xFC)
	Портписатьdword(текущий.командапорт, иДЕНТИФИКАТОР)
	Портписатьdword(текущий.данныепорт, значение)
}
func (текущий *TPeripheralcomponentinterconnectконтроллер) УстройствоhasФункции(bus uint16, устройство_2 uint16) bool {
	рЕЗУЛЬТАТ := текущий.Читать(bus, устройство_2, 0, 0x0E)
	if (рЕЗУЛЬТАТ & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var консоль TКонсоль = TКонсоль{}

func (текущий *TPeripheralcomponentinterconnectконтроллер) Выбратьдрайвер(драйвердиспетчер *TДрайвердиспетчер, interrupts *TПрерываниедиспетчер) {
	for bus := 0; bus < 8; bus++ {
		for устройство_2 := 0; устройство_2 < 32; устройство_2++ {

			var числоФункции int = 1
			if текущий.УстройствоhasФункции(uint16(bus), uint16(устройство_2)) == true {
				числоФункции = 8
			} else {
				числоФункции = 1
			}

			for функция := 0; функция < числоФункции; функция++ {
				var устройство TPeripheralcomponentinterconnectУстройствоdescriptor
				устройство = текущий.GetУстройствоdescriptor(uint16(bus), uint16(устройство_2), uint16(функция))
				if устройство.ПроизводительИДЕНТИФИКАТОР == 0x0000 || устройство.ПроизводительИДЕНТИФИКАТОР == 0xFFFF {
					continue
				}

				for полосаЧисло := 0; полосаЧисло < 6; полосаЧисло++ {
					var полоса TBaseaddressрегистр = текущий.Getbaseaddressрегистр(uint16(bus), uint16(устройство_2), uint16(функция), uint16(полосаЧисло))
					if полоса.address_2 != 0 && (полоса.regtype == 1) {
						устройство.Портbase = полоса.address_2
					}

					текущий.Getдрайвер(устройство, interrupts)

				}

			}

		}
	}
}
func (текущий *TPeripheralcomponentinterconnectконтроллер) GetУстройствоdescriptor(bus uint16, устройство_2 uint16, функция uint16) TPeripheralcomponentinterconnectУстройствоdescriptor {
	var рЕЗУЛЬТАТ TPeripheralcomponentinterconnectУстройствоdescriptor
	рЕЗУЛЬТАТ = TPeripheralcomponentinterconnectУстройствоdescriptor{}
	рЕЗУЛЬТАТ.bus = bus
	рЕЗУЛЬТАТ.устройство_2 = устройство_2
	рЕЗУЛЬТАТ.функция = функция

	рЕЗУЛЬТАТ.ПроизводительИДЕНТИФИКАТОР = uint16(текущий.Читать(bus, устройство_2, функция, 0x00))
	рЕЗУЛЬТАТ.УстройствоИДЕНТИФИКАТОР = uint16(текущий.Читать(bus, устройство_2, функция, 0x02))

	рЕЗУЛЬТАТ.классИДЕНТИФИКАТОР = uint8(текущий.Читать(bus, устройство_2, функция, 0x0b))
	рЕЗУЛЬТАТ.subclassИДЕНТИФИКАТОР = uint8(текущий.Читать(bus, устройство_2, функция, 0x0a))
	рЕЗУЛЬТАТ.интерфейсИДЕНТИФИКАТОР = uint8(текущий.Читать(bus, устройство_2, функция, 0x09))

	рЕЗУЛЬТАТ.revision = uint8(текущий.Читать(bus, устройство_2, функция, 0x08))
	рЕЗУЛЬТАТ.Прерывание = uint32(текущий.Читать(bus, устройство_2, функция, 0x3C))

	return рЕЗУЛЬТАТ
}
func (текущий *TPeripheralcomponentinterconnectконтроллер) Getbaseaddressрегистр(bus uint16, устройство_2 uint16, функция uint16, полоса uint16) TBaseaddressрегистр {
	var рЕЗУЛЬТАТ TBaseaddressрегистр

	headertype := текущий.Читать(bus, устройство_2, функция, 0x0E) & 0x7F
	var максимумbars int = int(6 - (4 * headertype))
	if полоса >= uint16(максимумbars) {
		return рЕЗУЛЬТАТ
	}

	полосаЗначение := текущий.Читать(bus, устройство_2, функция, uint32(0x10+4*полоса))

	if (полосаЗначение & 0x1) != 0 {
		рЕЗУЛЬТАТ.regtype = 1
	} else {
		рЕЗУЛЬТАТ.regtype = 0
	}

	if рЕЗУЛЬТАТ.regtype == 0 {
	} else {
		рЕЗУЛЬТАТ.address_2 = полосаЗначение & ^uint32(0x3)
		рЕЗУЛЬТАТ.prefetchcapable = false
	}

	return рЕЗУЛЬТАТ
}
func (текущий *TPeripheralcomponentinterconnectконтроллер) Getдрайвер(устройство TPeripheralcomponentinterconnectУстройствоdescriptor, interrupts *TПрерываниедиспетчер) {

	текущий.ipciконтроллерhandler.Приgetдрайвер(устройство)

}
