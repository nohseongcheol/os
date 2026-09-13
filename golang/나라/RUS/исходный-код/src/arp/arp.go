package arp

import . "unsafe"
import . "консоль"
import . "кадр_сети_с_общей_средой"
import . "утилита"

var arpконсоль TКонсоль = TКонсоль{}

type ArpСообщениеbuffer struct {
	оборудованиетип			[2]byte
	protocol			[2]byte
	оборудованиеaddressРазмер	byte
	protocoladdressРазмер		byte
	команда				[2]byte

	источникmacaddress	[6]byte
	источникipaddress	[4]byte
	назначениеmacaddress	[6]byte
	назначениеipaddress	[4]byte
}

var arpmesgРазмер uint32 = (64+92+64)/8 + 2

type ArpСообщение struct {
	оборудованиетип			uint16
	protocol			uint16
	оборудованиеaddressРазмер	uint8
	protocoladdressРазмер		uint8
	команда				uint16

	источникmacaddress	uint64
	источникipaddress	uint32
	назначениеmacaddress	uint64
	назначениеipaddress	uint32
}

func (текущий *ArpСообщение) Init(buffer_2 *ArpСообщениеbuffer) {

	текущий.оборудованиетип = Unsignedinteger16r(Массивкunsignedinteger16(buffer_2.оборудованиетип))
	текущий.protocol = Unsignedinteger16r(Массивкunsignedinteger16(buffer_2.protocol))
	текущий.оборудованиеaddressРазмер = byte(buffer_2.оборудованиеaddressРазмер)
	текущий.protocoladdressРазмер = byte(buffer_2.protocoladdressРазмер)
	текущий.команда = Unsignedinteger16r(Массивкunsignedinteger16(buffer_2.команда))

	текущий.источникmacaddress = Unsignedinteger48r(Массивкunsignedinteger48(buffer_2.источникmacaddress))
	текущий.источникipaddress = Unsignedinteger32r(Массивкunsignedinteger32(buffer_2.источникipaddress))
	текущий.назначениеmacaddress = Unsignedinteger48r(Массивкunsignedinteger48(buffer_2.назначениеmacaddress))
	текущий.назначениеipaddress = Unsignedinteger32r(Массивкunsignedinteger32(buffer_2.назначениеipaddress))
}
func (текущий *ArpСообщение) Указатьbuffer(buffer_2 *ArpСообщениеbuffer) {
	buffer_2.оборудованиетип = Unsignedinteger16кмассив(текущий.оборудованиетип)
	buffer_2.protocol = Unsignedinteger16кмассив(текущий.protocol)
	buffer_2.оборудованиеaddressРазмер = uint8(текущий.оборудованиеaddressРазмер)
	buffer_2.protocoladdressРазмер = uint8(текущий.protocoladdressРазмер)

	buffer_2.команда = Unsignedinteger16кмассив(текущий.команда)
	buffer_2.источникmacaddress = Unsignedinteger48кмассив(текущий.источникmacaddress)
	buffer_2.источникipaddress = Unsignedinteger32кмассив(текущий.источникipaddress)
	buffer_2.назначениеmacaddress = Unsignedinteger48кмассив(текущий.назначениеmacaddress)
	buffer_2.назначениеipaddress = Unsignedinteger32кмассив(текущий.назначениеipaddress)
}

type ArpэфирнаяСетькадрhandler struct {
	TЭфирнаяСетькадрhandler
}

var arpprovider Arpprovider
var поставщик_кадров_сети_с_общей_средой TПоставщик_кадров_сети_с_общей_средой

func (текущий *ArpэфирнаяСетькадрhandler) ЭфирнаяСетькадрreceivewhen(данныеУказатели uintptr, размер int) bool {
	arpконсоль.MПечатьxy([]byte("arp recv:"), 0, 23)
	return arpprovider.ЭфирнаяСетькадрreceivewhen(данныеУказатели, uint32(размер))

}
func (текущий *ArpэфирнаяСетькадрhandler) Отправить(назначениеmacbe uint64, данныеУказатели uintptr, размер uint32) {
	arpконсоль.MПечатьxy([]byte("arp send:"), 0, 24)
	var эфирнаяСетьтипbe = Unsignedinteger16r(0x0806)
	текущий.TЭфирнаяСетькадрhandler.КадрОтправить(назначениеmacbe, эфирнаяСетьтипbe, данныеУказатели, размер)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	числоcacheзапись	int

	handler	IЭфирнаяСетькадрhandler
}

var handler IЭфирнаяСетькадрhandler

func (текущий *Arpprovider) Init(backend TПоставщик_кадров_сети_с_общей_средой, userhandler IЭфирнаяСетькадрhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Указатьhandler(userhandler, 0x0806)
	текущий.числоcacheзапись = 0
	arpprovider = *текущий

}

func (текущий *Arpprovider) ЭфирнаяСетькадрreceivewhen(данныеУказатели uintptr, размер uint32) bool {

	if размер < arpmesgРазмер {
		return false
	}
	var arpbuffer *ArpСообщениеbuffer = (*ArpСообщениеbuffer)(Pointer(данныеУказатели))
	var arp ArpСообщение = ArpСообщение{}
	arp.Init(arpbuffer)

	if arp.оборудованиетип == 0x0100 {

		if arp.protocol == 0x0008 && arp.оборудованиеaddressРазмер == 6 && arp.protocoladdressРазмер == 4 && uint64(arp.назначениеipaddress) == handler.Getipaddress() {

			arpконсоль.MПечать([]byte("arp onetherframe"))
			arpконсоль.MUnsignedinteger16Печать(arp.protocol)
			arpконсоль.MПечать([]byte(":"))
			arpконсоль.MUnsignedinteger64Печать(uint64(arp.назначениеmacaddress))
			arpконсоль.MПечать([]byte(":"))
			arpконсоль.MUnsignedinteger16Печать(arp.команда)
			arpконсоль.MПечать([]byte(":"))
			arpконсоль.MUnsignedinteger64Печать(handler.Getmacaddress())

			switch arp.команда {
			case 0x0100:

				if текущий.Getmacfromcache(arp.источникipaddress) == 0xFFFFFFFFFFFF {
					if текущий.числоcacheзапись < 128 {
						текущий.Ipcache[текущий.числоcacheзапись] = arp.источникipaddress
						текущий.Maccache[текущий.числоcacheзапись] = arp.источникmacaddress
						текущий.числоcacheзапись++
					}
				}
				arp.команда = 0x0200
				arp.назначениеipaddress = arp.источникipaddress
				arp.назначениеmacaddress = arp.источникmacaddress
				arp.источникipaddress = uint32(handler.Getipaddress())
				arp.источникmacaddress = handler.Getmacaddress()
				arp.Указатьbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpконсоль.MПечать(([]byte)("self.numCacheEntries"))

				if текущий.числоcacheзапись < 128 {
					текущий.Ipcache[текущий.числоcacheзапись] = arp.источникipaddress
					текущий.Maccache[текущий.числоcacheзапись] = arp.источникmacaddress
					текущий.числоcacheзапись++
				}
				break
			}

		}
	}
	return false

}

func (текущий *Arpprovider) Broadcastmacaddress(Ipсетьбайтorder uint32) {

	var arp ArpСообщение = ArpСообщение{}
	arp.оборудованиетип = 0x0100
	arp.protocol = 0x0008
	arp.оборудованиеaddressРазмер = 6
	arp.protocoladdressРазмер = 4
	arp.команда = 0x0200

	arp.источникipaddress = uint32(handler.Getipaddress())

	arp.назначениеmacaddress = текущий.Разрешить(Ipсетьбайтorder)
	arp.назначениеipaddress = Ipсетьбайтorder
	arpконсоль.MПечатьxy([]byte("broad mac"), 0, 15)

	arp.источникmacaddress = handler.Getmacaddress()

	var arpbuffer ArpСообщениеbuffer = ArpСообщениеbuffer{}
	arp.Указатьbuffer(&arpbuffer)

	var ссылка_на_адрес uintptr = uintptr(Pointer(&arpbuffer))
	handler.Отправить(arp.назначениеmacaddress, ссылка_на_адрес, arpmesgРазмер)
}
func (текущий *Arpprovider) Requestmacaddress(Ipсетьбайтorder uint32) {

	var arp ArpСообщение = ArpСообщение{}
	arp.оборудованиетип = 0x0100

	arp.protocol = 0x0008
	arp.оборудованиеaddressРазмер = 6
	arp.protocoladdressРазмер = 4
	arp.команда = 0x0100

	arp.источникmacaddress = handler.Getmacaddress()
	arp.источникipaddress = uint32(handler.Getipaddress())

	arp.назначениеmacaddress = 0xFFFFFFFFFFFF
	arp.назначениеipaddress = Ipсетьбайтorder

	var arpbuffer ArpСообщениеbuffer = ArpСообщениеbuffer{}
	arp.Указатьbuffer(&arpbuffer)

	var ссылка_на_адрес uintptr = uintptr(Pointer(&arpbuffer))
	handler.Отправить(arp.назначениеmacaddress, ссылка_на_адрес, arpmesgРазмер)
}
func (текущий *Arpprovider) ПроверитьПечать(данные *[]byte, размер uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(данные))
	arpконсоль.MПечатьxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpконсоль.MHexadecimalПечать(buffer_2[i])
		arpконсоль.MПечать([]byte(":"))
	}
	arpконсоль.MПечать([]byte("]"))
}

func (текущий *Arpprovider) Getmacfromcache(Ipсетьбайтorder uint32) uint64 {
	for i := 0; i < текущий.числоcacheзапись; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpконсоль.MПечать(([]byte)("["))
		arpконсоль.MUnsignedinteger32Печать(текущий.Ipcache[i])
		arpконсоль.MПечать(([]byte)(":"))
		arpконсоль.MUnsignedinteger32Печать(Ipсетьбайтorder)
		arpконсоль.MПечать(([]byte)(":"))
		arpконсоль.MПечать(([]byte)(":"))
		arpконсоль.MUnsignedinteger64Печать(текущий.Maccache[i])
		arpконсоль.MПечать(([]byte)("]\n"))

		if текущий.Ipcache[i] == Ipсетьбайтorder {
			arpконсоль.MПечать([]byte("getmacfromcache"))
			return текущий.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (текущий *Arpprovider) Разрешить(Ipсетьбайтorder uint32) uint64 {
	var рЕЗУЛЬТАТ uint64 = текущий.Getmacfromcache(Ipсетьбайтorder)
	if рЕЗУЛЬТАТ == 0xFFFFFFFFFFFF {
		текущий.Requestmacaddress(Ipсетьбайтorder)
	}
	for i := 0; i < 128 && рЕЗУЛЬТАТ == 0xFFFFFFFFFFFF; i++ {
		рЕЗУЛЬТАТ = текущий.Getmacfromcache(Ipсетьбайтorder)

	}

	return рЕЗУЛЬТАТ
}
