package протокол_управляющих_сообщений_объединённой_сети

import . "unsafe"
import . "консоль"
import . "памятьдиспетчер"
import . "кадр_сети_с_общей_средой"
import . "протокол_объединённой_сети_4"
import . "утилита"

var icmpконсоль = TКонсоль{}

type TИнтернетCtrlСообщениеprotocolСообщениеbuffer struct {
	Тип	byte
	code	byte

	checksum	[2]byte
	данные		[4]byte
}

var icmpРазмер int = 64

type TИнтернетCtrlСообщениеprotocolСообщение struct {
	Тип	uint8
	code	uint8

	checksum	uint16
	данные		uint32
}

func (текущий *TИнтернетCtrlСообщениеprotocolСообщение) Init(buffer_2 TИнтернетCtrlСообщениеprotocolСообщениеbuffer) {
	текущий.Тип = buffer_2.Тип
	текущий.code = buffer_2.code

	текущий.checksum = Unsignedinteger16r(Массивкunsignedinteger16(buffer_2.checksum))
	текущий.данные = Unsignedinteger32r(Массивкunsignedinteger32(buffer_2.данные))
}

func (текущий *TИнтернетCtrlСообщениеprotocolСообщение) Указатьbuffer(buffer_2 *TИнтернетCtrlСообщениеprotocolСообщениеbuffer) {
	buffer_2.Тип = текущий.Тип
	buffer_2.code = текущий.code

	buffer_2.checksum = Unsignedinteger16кмассив(текущий.checksum)
	buffer_2.данные = Unsignedinteger32кмассив(текущий.данные)
}

type Icmphandler struct {
	TИнтернетprotocolhandler
}

var протокол_управляющих_сообщений_объединённой_сети *TПротокол_управляющих_сообщений_объединённой_сети

func (текущий *Icmphandler) Интернетprotocolreceivewhen(источникipaddressсетьбайтorder uint32, назначениеipaddressсетьбайтorder uint32, данныеУказатели uintptr, размер uint32) bool {
	return протокол_управляющих_сообщений_объединённой_сети.Интернетprotocolreceivewhen(источникipaddressсетьбайтorder, назначениеipaddressсетьбайтorder, данныеУказатели, размер)
}

var iphandler IИнтернетprotocolhandler

type TПротокол_управляющих_сообщений_объединённой_сети struct {
}

func (текущий *TПротокол_управляющих_сообщений_объединённой_сети) Init(backend TПоставщик_протокола_объединённой_сети, handler IИнтернетprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	протокол_управляющих_сообщений_объединённой_сети = текущий
}
func (текущий *TПротокол_управляющих_сообщений_объединённой_сети) Интернетprotocolreceivewhen(источникipaddressсетьбайтorder uint32, назначениеipaddressсетьбайтorder uint32, данныеУказатели uintptr, размер uint32) bool {
	if размер < uint32(icmpРазмер) {
		return false
	}

	var buffer_2 *TИнтернетCtrlСообщениеprotocolСообщениеbuffer = (*TИнтернетCtrlСообщениеprotocolСообщениеbuffer)(Pointer(данныеУказатели))
	var msg TИнтернетCtrlСообщениеprotocolСообщение = TИнтернетCtrlСообщениеprotocolСообщение{}
	msg.Init(*buffer_2)

	icmpконсоль.MПечать(([]byte)("icmp:OnInternet"))
	icmpконсоль.MUnsignedinteger16Печать(uint16(msg.Тип))
	icmpконсоль.MПечать(([]byte)(":"))

	switch msg.Тип {
	case 0:
		icmpконсоль.MПечать(([]byte)("ping response from "))
		break

	case 8:
		icmpконсоль.MПечать(([]byte)("ping send "))
		msg.Тип = 0

		msg.checksum = 0
		msg.Указатьbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(данныеУказатели)), uint32(icmpРазмер))

		msg.Указатьbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (текущий *TПротокол_управляющих_сообщений_объединённой_сети) EchorequestОтправить(ipсетьбайтorder uint32) bool {
	var протокол_управляющих_сообщений_объединённой_сети TИнтернетCtrlСообщениеprotocolСообщение = TИнтернетCtrlСообщениеprotocolСообщение{}

	var памятьдиспетчер = &TПамятьдиспетчер{}
	var buffer_2 = (*TИнтернетCtrlСообщениеprotocolСообщениеbuffer)(памятьдиспетчер.Выделить_память(1024))

	протокол_управляющих_сообщений_объединённой_сети.Тип = 8
	протокол_управляющих_сообщений_объединённой_сети.code = 0
	протокол_управляющих_сообщений_объединённой_сети.данные = 0x3713
	протокол_управляющих_сообщений_объединённой_сети.checksum = 0
	протокол_управляющих_сообщений_объединённой_сети.Указатьbuffer(buffer_2)
	протокол_управляющих_сообщений_объединённой_сети.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpРазмер))
	протокол_управляющих_сообщений_объединённой_сети.Указатьbuffer(buffer_2)

	var данныеУказатели uintptr = uintptr(Pointer(buffer_2))
	iphandler.Отправить(ipсетьбайтorder, 0x01, данныеУказатели, uint32(icmpРазмер))

	return false

}
