package pci

import . "порт"
import . "переривання"
import . "консоль"
import . "driver/driver"

type IpciКонтролерhandler interface {
	Увімкненоgetdriver(пристрій TPeripheralcomponentinterconnectПристрійdescriptor)
}

var ipciКонтролерhandler IpciКонтролерhandler

type TТиповийpciКонтролерhandler struct {
}

func (поточний TТиповийpciКонтролерhandler) Увімкненоgetdriver(пристрій TPeripheralcomponentinterconnectПристрійdescriptor) {
}

type TBaseАдресаregister struct {
	prefetchcapable	bool
	адреса_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectПристрійdescriptor struct {
	Портbase	uint32
	Переривання	uint32

	bus		uint16
	пристрій_2	uint16
	функція		uint16

	ВиробникІДЕНТИФІКАТОР	uint16
	ПристрійІДЕНТИФІКАТОР	uint16

	класІДЕНТИФІКАТОР	uint8
	subclassІДЕНТИФІКАТОР	uint8
	інтерфейсІДЕНТИФІКАТОР	uint8

	revision	uint8
}

func (поточний *TPeripheralcomponentinterconnectПристрійdescriptor) Init() {
}

type TPeripheralcomponentinterconnectКонтролер struct {
	ipciКонтролерhandler	IpciКонтролерhandler
	dataПорт		uint16
	командаПорт		uint16
}

func (поточний *TPeripheralcomponentinterconnectКонтролер) Init(ipciКонтролерhandler IpciКонтролерhandler) {
	поточний.dataПорт = 0xCFC
	поточний.командаПорт = 0xCF8

	поточний.ipciКонтролерhandler = TТиповийpciКонтролерhandler{}
	if ipciКонтролерhandler != nil {
		поточний.ipciКонтролерhandler = ipciКонтролерhandler
	}
}

var iВідлік int = 0

func (поточний *TPeripheralcomponentinterconnectКонтролер) Читання(bus uint16, пристрій_2 uint16, функція uint16, registeroffset uint32) uint32 {
	var іДЕНТИФІКАТОР uint32 = 0
	іДЕНТИФІКАТОР = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(пристрій_2&0x1f) << 11) | (uint32(функція&0x07) << 8) | uint32(registeroffset&0xFC)

	ПортЗаписdword(поточний.командаПорт, іДЕНТИФІКАТОР)

	яРЛИК1 := ПортЧитанняdword(поточний.dataПорт)
	яРЛИК2 := (яРЛИК1 >> (8 * (registeroffset % 4)))

	return яРЛИК2
}

func (поточний *TPeripheralcomponentinterconnectКонтролер) Запис(bus uint16, пристрій_2 uint16, функція uint16, registeroffset uint32, значення uint32) {
	var іДЕНТИФІКАТОР uint32
	іДЕНТИФІКАТОР = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((пристрій_2&0x1f)<<11) | uint32((функція&0x07)<<8) | uint32(registeroffset&0xFC)
	ПортЗаписdword(поточний.командаПорт, іДЕНТИФІКАТОР)
	ПортЗаписdword(поточний.dataПорт, значення)
}
func (поточний *TPeripheralcomponentinterconnectКонтролер) ПристрійХасіФункції(bus uint16, пристрій_2 uint16) bool {
	яРЛИК := поточний.Читання(bus, пристрій_2, 0, 0x0E)
	if (яРЛИК & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var консоль TКонсоль = TКонсоль{}

func (поточний *TPeripheralcomponentinterconnectКонтролер) Виділитиdriver(drivermanager *TDrivermanager, interrupts *TПерериванняmanager) {
	for bus := 0; bus < 8; bus++ {
		for пристрій_2 := 0; пристрій_2 < 32; пристрій_2++ {

			var числоФункції int = 1
			if поточний.ПристрійХасіФункції(uint16(bus), uint16(пристрій_2)) == true {
				числоФункції = 8
			} else {
				числоФункції = 1
			}

			for функція := 0; функція < числоФункції; функція++ {
				var пристрій TPeripheralcomponentinterconnectПристрійdescriptor
				пристрій = поточний.GetПристрійdescriptor(uint16(bus), uint16(пристрій_2), uint16(функція))
				if пристрій.ВиробникІДЕНТИФІКАТОР == 0x0000 || пристрій.ВиробникІДЕНТИФІКАТОР == 0xFFFF {
					continue
				}

				for барЧисло := 0; барЧисло < 6; барЧисло++ {
					var бар TBaseАдресаregister = поточний.GetbaseАдресаregister(uint16(bus), uint16(пристрій_2), uint16(функція), uint16(барЧисло))
					if бар.адреса_2 != 0 && (бар.regtype == 1) {
						пристрій.Портbase = бар.адреса_2
					}

					поточний.Getdriver(пристрій, interrupts)

				}

			}

		}
	}
}
func (поточний *TPeripheralcomponentinterconnectКонтролер) GetПристрійdescriptor(bus uint16, пристрій_2 uint16, функція uint16) TPeripheralcomponentinterconnectПристрійdescriptor {
	var яРЛИК TPeripheralcomponentinterconnectПристрійdescriptor
	яРЛИК = TPeripheralcomponentinterconnectПристрійdescriptor{}
	яРЛИК.bus = bus
	яРЛИК.пристрій_2 = пристрій_2
	яРЛИК.функція = функція

	яРЛИК.ВиробникІДЕНТИФІКАТОР = uint16(поточний.Читання(bus, пристрій_2, функція, 0x00))
	яРЛИК.ПристрійІДЕНТИФІКАТОР = uint16(поточний.Читання(bus, пристрій_2, функція, 0x02))

	яРЛИК.класІДЕНТИФІКАТОР = uint8(поточний.Читання(bus, пристрій_2, функція, 0x0b))
	яРЛИК.subclassІДЕНТИФІКАТОР = uint8(поточний.Читання(bus, пристрій_2, функція, 0x0a))
	яРЛИК.інтерфейсІДЕНТИФІКАТОР = uint8(поточний.Читання(bus, пристрій_2, функція, 0x09))

	яРЛИК.revision = uint8(поточний.Читання(bus, пристрій_2, функція, 0x08))
	яРЛИК.Переривання = uint32(поточний.Читання(bus, пристрій_2, функція, 0x3C))

	return яРЛИК
}
func (поточний *TPeripheralcomponentinterconnectКонтролер) GetbaseАдресаregister(bus uint16, пристрій_2 uint16, функція uint16, бар uint16) TBaseАдресаregister {
	var яРЛИК TBaseАдресаregister

	headertype := поточний.Читання(bus, пристрій_2, функція, 0x0E) & 0x7F
	var максимумbars int = int(6 - (4 * headertype))
	if бар >= uint16(максимумbars) {
		return яРЛИК
	}

	барЗначення := поточний.Читання(bus, пристрій_2, функція, uint32(0x10+4*бар))

	if (барЗначення & 0x1) != 0 {
		яРЛИК.regtype = 1
	} else {
		яРЛИК.regtype = 0
	}

	if яРЛИК.regtype == 0 {
	} else {
		яРЛИК.адреса_2 = барЗначення & ^uint32(0x3)
		яРЛИК.prefetchcapable = false
	}

	return яРЛИК
}
func (поточний *TPeripheralcomponentinterconnectКонтролер) Getdriver(пристрій TPeripheralcomponentinterconnectПристрійdescriptor, interrupts *TПерериванняmanager) {

	поточний.ipciКонтролерhandler.Увімкненоgetdriver(пристрій)

}
