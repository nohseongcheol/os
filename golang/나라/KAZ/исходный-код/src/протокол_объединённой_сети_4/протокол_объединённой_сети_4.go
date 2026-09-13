package протокол_объединённой_сети_4

import . "unsafe"
import . "утилита"
import . "консоль"
import . "кадр_сети_с_общей_средой"
import . "arp"

var ipконсоль TКонсоль = TКонсоль{}

type TИнтернетprotocolv4Сообщениеbuffer struct {
	lenver		byte
	tos		byte
	всегоДлина	[2]byte

	ident		[2]byte
	флагииoffset	[2]byte

	времякlive	byte
	protocol	byte
	checksum	[2]byte

	источникipaddress	[4]byte
	назначениеipaddress	[4]byte
}

var ipРазмер uint8 = (4 + 4 + 4 + 8)

type TИнтернетprotocolv4Сообщение struct {
	заголовокДлина	uint8
	версия		uint8
	tos		uint8
	всегоДлина	uint16

	ident		uint16
	флагииoffset	uint16

	времякlive	uint8
	protocol	uint8
	checksum	uint16

	источникipaddress	uint32
	назначениеipaddress	uint32
}

func (текущий *TИнтернетprotocolv4Сообщение) Init(buffer_2 TИнтернетprotocolv4Сообщениеbuffer) {

	текущий.версия = ((buffer_2.lenver & 0xF0) >> 4)
	текущий.заголовокДлина = buffer_2.lenver & 0x0F
	текущий.tos = buffer_2.tos
	текущий.всегоДлина = Unsignedinteger16r(Массивкunsignedinteger16(buffer_2.всегоДлина))

	текущий.ident = Unsignedinteger16r(Массивкunsignedinteger16(buffer_2.ident))
	текущий.флагииoffset = Unsignedinteger16r(Массивкunsignedinteger16(buffer_2.флагииoffset))

	текущий.времякlive = buffer_2.времякlive
	текущий.protocol = buffer_2.protocol
	текущий.checksum = Unsignedinteger16r(Массивкunsignedinteger16(buffer_2.checksum))

	текущий.источникipaddress = Unsignedinteger32r(Массивкunsignedinteger32(buffer_2.источникipaddress))
	текущий.назначениеipaddress = Unsignedinteger32r(Массивкunsignedinteger32(buffer_2.назначениеipaddress))

}
func (текущий *TИнтернетprotocolv4Сообщение) Указатьbuffer(buffer_2 *TИнтернетprotocolv4Сообщениеbuffer) {

	buffer_2.lenver = byte(((текущий.версия & 0x0F) << 4) | (текущий.заголовокДлина & 0x0F))
	buffer_2.tos = текущий.tos
	buffer_2.всегоДлина = Unsignedinteger16кмассив(текущий.всегоДлина)

	buffer_2.ident = Unsignedinteger16кмассив(текущий.ident)
	buffer_2.флагииoffset = Unsignedinteger16кмассив(текущий.флагииoffset)

	buffer_2.времякlive = текущий.времякlive
	buffer_2.protocol = текущий.protocol
	buffer_2.checksum = Unsignedinteger16кмассив(текущий.checksum)

	buffer_2.источникipaddress = Unsignedinteger32кмассив(текущий.источникipaddress)
	buffer_2.назначениеipaddress = Unsignedinteger32кмассив(текущий.назначениеipaddress)

}

type IИнтернетprotocolhandler interface {
	Init(backend TПоставщик_протокола_объединённой_сети, pihandler IИнтернетprotocolhandler, pprotocol uint8)
	Интернетprotocolreceivewhen(источникipaddressсетьбайтorder uint32, назначениеipaddressсетьбайтorder uint32, данныеУказатели uintptr, размер uint32) bool
	Отправить(назначениеipaddressсетьбайтorder uint32, pprotocol uint8, данныеУказатели uintptr, размер uint32)
	Providerget() *TПоставщик_протокола_объединённой_сети
}

type TИнтернетprotocolhandler struct {
}

var ipэфирнаяСетькадрhandler IpэфирнаяСетькадрhandler = IpэфирнаяСетькадрhandler{}
var protocol uint8

func (текущий *TИнтернетprotocolhandler) Init(backend TПоставщик_протокола_объединённой_сети, pihandler IИнтернетprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (текущий *TИнтернетprotocolhandler) Интернетprotocolreceivewhen(источникipaddressсетьбайтorder uint32, назначениеipaddressсетьбайтorder uint32, данныеУказатели uintptr, размер uint32) bool {
	ipконсоль.MПечать(([]byte)("ipHandler:OnInternet"))
	return false
}
func (текущий *TИнтернетprotocolhandler) Отправить(назначениеipaddressсетьбайтorder uint32, pprotocol uint8, данныеУказатели uintptr, размер uint32) {

	поставщик_протокола_объединённой_сети.Отправить(назначениеipaddressсетьбайтorder, pprotocol, данныеУказатели, размер)
}
func (текущий *TИнтернетprotocolhandler) Providerget() *TПоставщик_протокола_объединённой_сети {
	return &поставщик_протокола_объединённой_сети
}

type IpэфирнаяСетькадрhandler struct {
	TЭфирнаяСетькадрhandler
}

var поставщик_протокола_объединённой_сети TПоставщик_протокола_объединённой_сети

func (текущий *IpэфирнаяСетькадрhandler) ЭфирнаяСетькадрreceivewhen(данныеУказатели uintptr, размер int) bool {
	ipконсоль.MПечать(([]byte)("iphandler:onEtherfameRecv\n"))
	return поставщик_протокола_объединённой_сети.ЭфирнаяСетькадрreceivewhen(данныеУказатели, uint32(размер))

}

func (текущий *IpэфирнаяСетькадрhandler) Отправить(назначениеipaddressсетьбайтorder uint64, данныеУказатели uintptr, размер uint32) {
	ipконсоль.MПечать(([]byte)("ipefhandler:send\n"))
	var эфирнаяСетьтипbe = Unsignedinteger16r(0x0800)
	текущий.TЭфирнаяСетькадрhandler.КадрОтправить(назначениеipaddressсетьбайтorder, эфирнаяСетьтипbe, данныеУказатели, размер)

}

var handler_2 [255]IИнтернетprotocolhandler

type TПоставщик_протокола_объединённой_сети struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetМаска	uint32
}

var efhandler IЭфирнаяСетькадрhandler

func (текущий *TПоставщик_протокола_объединённой_сети) Init(pefprovider TПоставщик_кадров_сети_с_общей_средой, pefhandler IЭфирнаяСетькадрhandler, arp Arpprovider, gatewayip uint32, subnetМаска uint32) {

	efhandler = pefhandler
	efhandler.Указатьhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	текущий.arpprovider = arp
	текущий.Gatewayip = gatewayip
	текущий.SubnetМаска = subnetМаска
	поставщик_протокола_объединённой_сети = *текущий
}
func (текущий *TПоставщик_протокола_объединённой_сети) ЭфирнаяСетькадрreceivewhen(эфирнаяСетькадрpayload uintptr, размер uint32) bool {
	if размер < uint32(ipРазмер) {
		return false
	}

	var buffer_2 *TИнтернетprotocolv4Сообщениеbuffer = (*TИнтернетprotocolv4Сообщениеbuffer)(Pointer(эфирнаяСетькадрpayload))
	var интернетprotocolСообщение TИнтернетprotocolv4Сообщение
	интернетprotocolСообщение.Init(*buffer_2)

	var reply bool = false

	if интернетprotocolСообщение.назначениеipaddress == uint32(efhandler.Getipaddress()) {

		var длина uint32 = uint32(интернетprotocolСообщение.всегоДлина)
		if длина > размер {
			длина = размер
		}
		if handler_2[интернетprotocolСообщение.protocol] != nil {
			reply = handler_2[интернетprotocolСообщение.protocol].Интернетprotocolreceivewhen(интернетprotocolСообщение.источникipaddress, интернетprotocolСообщение.назначениеipaddress, эфирнаяСетькадрpayload+uintptr(4*интернетprotocolСообщение.заголовокДлина), uint32(длина-uint32(4*интернетprotocolСообщение.заголовокДлина)))

		}
	}

	if reply {

		var temporary = интернетprotocolСообщение.назначениеipaddress
		интернетprotocolСообщение.назначениеipaddress = интернетprotocolСообщение.источникipaddress
		интернетprotocolСообщение.источникipaddress = temporary

		интернетprotocolСообщение.времякlive = 0x40
		интернетprotocolСообщение.checksum = 0

		интернетprotocolСообщение.Указатьbuffer(buffer_2)
		интернетprotocolСообщение.checksum = текущий.Checksum((*([4096]uint16))(Pointer(эфирнаяСетькадрpayload)), uint32(4*интернетprotocolСообщение.заголовокДлина))

		интернетprotocolСообщение.Указатьbuffer(buffer_2)

	}

	ipконсоль.MПечать(([]byte)("ipmessage"))
	ipконсоль.MUnsignedinteger32Печать(интернетprotocolСообщение.источникipaddress)
	ipконсоль.MПечать(([]byte)(":"))
	ipконсоль.MUnsignedinteger32Печать(интернетprotocolСообщение.назначениеipaddress)
	ipконсоль.MПечать(([]byte)(":"))
	ipконсоль.MUnsignedinteger16Печать(uint16(интернетprotocolСообщение.заголовокДлина))
	ipконсоль.MПечать(([]byte)(":"))
	ipконсоль.MUnsignedinteger16Печать(uint16(интернетprotocolСообщение.версия))
	ipконсоль.MПечать(([]byte)(":"))
	ipконсоль.MUnsignedinteger16Печать(интернетprotocolСообщение.всегоДлина)
	ipконсоль.MПечать(([]byte)(":"))
	ipконсоль.MUnsignedinteger32Печать(uint32(efhandler.Getipaddress()))
	ipконсоль.MПечать(([]byte)(":"))
	ipконсоль.MПечать(([]byte)("\n"))

	return reply

}
func (текущий *TПоставщик_протокола_объединённой_сети) Отправить(назначениеipaddressсетьбайтorder uint32, protocol uint8, данныеУказатели uintptr, размер uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TИнтернетprotocolv4Сообщениеbuffer = (*TИнтернетprotocolv4Сообщениеbuffer)(Pointer(&buffer1_2))
	var сообщение TИнтернетprotocolv4Сообщение = TИнтернетprotocolv4Сообщение{}
	сообщение.версия = 4
	сообщение.заголовокДлина = ipРазмер / 4
	сообщение.tos = 0
	сообщение.всегоДлина = Unsignedinteger16r(uint16(размер + uint32(ipРазмер)))

	сообщение.ident = 0x0100
	сообщение.флагииoffset = 0x0040
	сообщение.времякlive = 0x40
	сообщение.protocol = protocol

	сообщение.назначениеipaddress = назначениеipaddressсетьбайтorder

	сообщение.источникipaddress = uint32(efhandler.Getipaddress())

	сообщение.checksum = 0

	сообщение.Указатьbuffer(buffer_2)
	сообщение.checksum = текущий.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipРазмер))
	сообщение.Указатьbuffer(buffer_2)

	var данныеbuffer_2 [4096]byte = *(*([4096]byte))(Pointer(данныеУказатели))

	for i := 0; i < int(размер); i++ {

		buffer1_2[i+int(ipРазмер)] = данныеbuffer_2[i]
	}

	ipконсоль.MПечатьxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(размер)+int(ipРазмер); i++ {
		ipконсоль.MHexadecimalПечать(buffer1_2[i])
	}
	ipконсоль.MПечать(([]byte)(":"))
	ipконсоль.MПечать(([]byte)("]\n"))

	var далееhopipaddressсетьбайтorder uint32 = назначениеipaddressсетьбайтorder
	if (назначениеipaddressсетьбайтorder & текущий.SubnetМаска) != (сообщение.источникipaddress & текущий.SubnetМаска) {
		далееhopipaddressсетьбайтorder = текущий.Gatewayip
	}

	var отправитьданныеУказатели = uintptr(Pointer(&buffer1_2))
	ipконсоль.MUnsignedinteger32Печать(далееhopipaddressсетьбайтorder)

	var эфирнаяСетьтипbe = Unsignedinteger16r(0x0800)
	efhandler.КадрОтправить(текущий.arpprovider.Разрешить(далееhopipaddressсетьбайтorder), эфирнаяСетьтипbe, отправитьданныеУказатели, uint32(ipРазмер)+uint32(размер))

}
func (текущий *TПоставщик_протокола_объединённой_сети) Checksum(pданные *[4096]uint16, длинаИсходящийБайт uint32) uint16 {
	var данные [4096]uint16 = *pданные
	var temporary uint32 = 0
	var данныеБайт [4096]byte = *(*([4096]byte))(Pointer(&данные))
	if (длинаИсходящийБайт % 2) != 0 {
		temporary += uint32(uint16(данныеБайт[длинаИсходящийБайт-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (текущий *TПоставщик_протокола_объединённой_сети) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
