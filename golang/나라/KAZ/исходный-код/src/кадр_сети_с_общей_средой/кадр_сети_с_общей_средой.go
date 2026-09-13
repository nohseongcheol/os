package кадр_сети_с_общей_средой

import . "консоль"

import . "amdam79c973"
import . "unsafe"
import . "утилита"

var эфирнаяСетьконсоль TКонсоль = TКонсоль{}

type TЭфирнаяСетькадрзаголовокbuffer struct {
	назначениеmacbe		[6]byte
	источникmacbe		[6]byte
	эфирнаяСетьтипbe	[2]byte
}

var кадрзаголовокРазмер int = 14

type TЗаголовок_кадра_сети_с_общей_средой struct {
	назначениеmacbe		uint64
	источникmacbe		uint64
	эфирнаяСетьтипbe	uint16
}

func (текущий *TЗаголовок_кадра_сети_с_общей_средой) Init(buffer_2 TЭфирнаяСетькадрзаголовокbuffer) {
	текущий.назначениеmacbe = (Массивкunsignedinteger48(buffer_2.назначениеmacbe))
	текущий.источникmacbe = (Массивкunsignedinteger48(buffer_2.источникmacbe))
	текущий.эфирнаяСетьтипbe = (Массивкunsignedinteger16(buffer_2.эфирнаяСетьтипbe))

}
func (текущий *TЗаголовок_кадра_сети_с_общей_средой) Указатьbuffer(buffer_2 *TЭфирнаяСетькадрзаголовокbuffer) {
	buffer_2.назначениеmacbe = Unsignedinteger48кмассив(Unsignedinteger48r(текущий.назначениеmacbe))
	buffer_2.источникmacbe = Unsignedinteger48кмассив(Unsignedinteger48r(текущий.источникmacbe))
	buffer_2.эфирнаяСетьтипbe = Unsignedinteger16кмассив(Unsignedinteger16r(текущий.эфирнаяСетьтипbe))
}

type IЭфирнаяСетькадрhandler interface {
	Init(backend TПоставщик_кадров_сети_с_общей_средой)
	Указатьhandler(handler IЭфирнаяСетькадрhandler, эфирнаяСетьтип uint16)
	ЭфирнаяСетькадрreceivewhen(данныеУказатели uintptr, размер int) bool
	Отправить(назначениеmacbe uint64, данныеУказатели uintptr, размер uint32)
	КадрОтправить(назначениеmacbe uint64, эфирнаяСетьтипbe uint16, данныеУказатели uintptr, размер uint32)
	Providerget() TПоставщик_кадров_сети_с_общей_средой
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TЭфирнаяСетькадрhandler struct {
}

var кадр TЗаголовок_кадра_сети_с_общей_средой
var Backend TПоставщик_кадров_сети_с_общей_средой
var handler_2 [65535]IЭфирнаяСетькадрhandler
var efhandler *TЭфирнаяСетькадрhandler = nil

func (текущий *TЭфирнаяСетькадрhandler) Init(backend TПоставщик_кадров_сети_с_общей_средой) {
	Backend = backend
}

func (текущий *TЭфирнаяСетькадрhandler) Указатьhandler(handler IЭфирнаяСетькадрhandler, pэфирнаяСетьтип uint16) {
	handler_2[pэфирнаяСетьтип] = handler
}
func (текущий *TЭфирнаяСетькадрhandler) Указатьbackend(backend TПоставщик_кадров_сети_с_общей_средой) {
	Backend = backend
}
func (текущий *TЭфирнаяСетькадрhandler) Getbackend() TПоставщик_кадров_сети_с_общей_средой {
	return Backend
}
func (текущий *TЭфирнаяСетькадрhandler) ЭфирнаяСетькадрreceivewhen(данныеУказатели uintptr, размер int) bool {
	эфирнаяСетьконсоль.MПечать(([]byte)("OnEtherFrameReceived"))
	return false
}
func (текущий *TЭфирнаяСетькадрhandler) Отправить(назначениеmacbe uint64, данныеУказатели uintptr, размер uint32) {
	Backend.КадрОтправить(назначениеmacbe, кадр.эфирнаяСетьтипbe, данныеУказатели, размер)
}
func (текущий *TЭфирнаяСетькадрhandler) КадрОтправить(назначениеmacbe uint64, эфирнаяСетьтипbe uint16, данныеУказатели uintptr, размер uint32) {
	Backend.КадрОтправить(назначениеmacbe, эфирнаяСетьтипbe, данныеУказатели, размер)
}
func (текущий *TЭфирнаяСетькадрhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (текущий *TЭфирнаяСетькадрhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (текущий *TЭфирнаяСетькадрhandler) Providerget() TПоставщик_кадров_сети_с_общей_средой {
	return Backend
}

type TЭфирнаяСетькадрrawданныеhandler struct {
	TRawданныеhandler
}

var provider TПоставщик_кадров_сети_с_общей_средой

func (текущий *TЭфирнаяСетькадрrawданныеhandler) Init(pprovider TПоставщик_кадров_сети_с_общей_средой, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (текущий *TЭфирнаяСетькадрrawданныеhandler) Приrawданныеreceive(данныеУказатели uintptr, размер int) bool {
	return provider.Приrawданныеreceive(данныеУказатели, размер)
}
func (текущий *TЭфирнаяСетькадрrawданныеhandler) Отправить(данныеУказатели uintptr, размер uint32) {
	provider.Отправить(данныеУказатели, размер)
}
func (текущий *TЭфирнаяСетькадрrawданныеhandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (текущий *TЭфирнаяСетькадрrawданныеhandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (текущий *TЭфирнаяСетькадрrawданныеhandler) Providerget() TПоставщик_кадров_сети_с_общей_средой {
	return provider
}

type TПоставщик_кадров_сети_с_общей_средой struct {
	сетьКарточные	Tamdam79c973
	handler_2	[65565]IЭфирнаяСетькадрhandler
}

func (текущий *TПоставщик_кадров_сети_с_общей_средой) Init(backend Tamdam79c973) {

	текущий.сетьКарточные = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		текущий.handler_2[i] = nil
	}
}

var количество uint16 = 0

func (текущий *TПоставщик_кадров_сети_с_общей_средой) Приrawданныеreceive(данныеУказатели uintptr, размер int) bool {

	var buffer_2 *TЭфирнаяСетькадрзаголовокbuffer = (*TЭфирнаяСетькадрзаголовокbuffer)(Pointer(данныеУказатели))
	var кадр TЗаголовок_кадра_сети_с_общей_средой = TЗаголовок_кадра_сети_с_общей_средой{}
	кадр.Init(*buffer_2)
	var reply bool = false

	if кадр.назначениеmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(кадр.назначениеmacbe) == текущий.Getmacaddress() {
		if handler_2[кадр.эфирнаяСетьтипbe] != nil {
			эфирнаяСетьконсоль.MПечать(([]byte)("provider\n"))

			var ссылка_на_адрес uintptr = uintptr(Pointer(данныеУказатели)) + uintptr(кадрзаголовокРазмер)
			reply = handler_2[кадр.эфирнаяСетьтипbe].ЭфирнаяСетькадрreceivewhen(ссылка_на_адрес, размер-кадрзаголовокРазмер)

		}
	}

	if reply {
		кадр.назначениеmacbe = кадр.источникmacbe
		кадр.источникmacbe = Unsignedinteger48r(текущий.Getmacaddress())
		кадр.Указатьbuffer(buffer_2)

	}

	эфирнаяСетьконсоль.MПечатьxy(([]byte)("spro["), 0, 1)
	эфирнаяСетьконсоль.MUnsignedinteger64Печать(кадр.источникmacbe)
	эфирнаяСетьконсоль.MПечать(([]byte)(":"))
	эфирнаяСетьконсоль.MUnsignedinteger64Печать(кадр.назначениеmacbe)
	эфирнаяСетьконсоль.MПечать(([]byte)(":]["))
	эфирнаяСетьконсоль.MUnsignedinteger64Печать(текущий.Getmacaddress())
	эфирнаяСетьконсоль.MПечать(([]byte)(":"))
	эфирнаяСетьконсоль.MUnsignedinteger16Печать(кадр.эфирнаяСетьтипbe)
	эфирнаяСетьконсоль.MПечать(([]byte)("]"))

	return reply

}
func (текущий *TПоставщик_кадров_сети_с_общей_средой) Отправить(данныеУказатели uintptr, размер uint32) {
	текущий.сетьКарточные.Отправить(данныеУказатели, размер)
}
func (текущий *TПоставщик_кадров_сети_с_общей_средой) КадрОтправить(назначениеmacbe uint64, эфирнаяСетьтипbe uint16, данныеУказатели uintptr, размер uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TЭфирнаяСетькадрзаголовокbuffer = (*TЭфирнаяСетькадрзаголовокbuffer)(Pointer(&buffer2_2))

	var кадр TЗаголовок_кадра_сети_с_общей_средой = TЗаголовок_кадра_сети_с_общей_средой{}
	кадр.Init(*buffer_2)

	кадр.назначениеmacbe = Unsignedinteger48r(назначениеmacbe)
	кадр.источникmacbe = Unsignedinteger48r(текущий.сетьКарточные.Getmacaddress())
	кадр.эфирнаяСетьтипbe = Unsignedinteger16r(эфирнаяСетьтипbe)

	кадр.Указатьbuffer(buffer_2)
	var источник_2 [4096]byte = *(*([4096]byte))(Pointer(данныеУказатели))

	var i uint32 = 0
	for i = 0; i < размер; i++ {
		buffer2_2[uint32(кадрзаголовокРазмер)+i] = источник_2[i]

	}

	var ссылка_на_адрес uintptr = uintptr(Pointer(&buffer2_2))

	текущий.сетьКарточные.Отправить(ссылка_на_адрес, размер+uint32(кадрзаголовокРазмер))

}
func (текущий *TПоставщик_кадров_сети_с_общей_средой) Getmacaddress() uint64 {
	return текущий.сетьКарточные.Getmacaddress()
}
func (текущий *TПоставщик_кадров_сети_с_общей_средой) Getipaddress() uint64 {
	return текущий.сетьКарточные.Getipaddress()
}
