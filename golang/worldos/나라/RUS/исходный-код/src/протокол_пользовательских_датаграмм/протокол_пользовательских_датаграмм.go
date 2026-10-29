/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package протокол_пользовательских_датаграмм

import . "unsafe"
import . "консоль"
import . "утилита"
import . "памятьдиспетчер"
import . "протокол_объединённой_сети_4"

var udpконсоль = TКонсоль{}

type TПользовательdatagramprotocolзаголовокbuffer struct {
	номер_порта_отправителя	[2]byte
	номер_порта_получателя	[2]byte

	длина		[2]byte
	checksum	[2]byte
}

var udpзаголовокРазмер uint32 = 8

type TЗаголовок_пользовательской_датаграммы struct {
	номер_порта_отправителя	uint16
	номер_порта_получателя	uint16

	длина		uint16
	checksum	uint16
}

func (текущий *TЗаголовок_пользовательской_датаграммы) Init(buffer_2 *TПользовательdatagramprotocolзаголовокbuffer) {
	текущий.номер_порта_отправителя = Массивкunsignedinteger16(buffer_2.номер_порта_отправителя)
	текущий.номер_порта_получателя = Массивкunsignedinteger16(buffer_2.номер_порта_получателя)

	текущий.длина = Массивкunsignedinteger16(buffer_2.длина)
	текущий.checksum = Массивкunsignedinteger16(buffer_2.checksum)
}
func (текущий *TЗаголовок_пользовательской_датаграммы) Указатьbuffer(buffer_2 *TПользовательdatagramprotocolзаголовокbuffer) {

	buffer_2.номер_порта_отправителя = Unsignedinteger16кмассив(текущий.номер_порта_отправителя)
	buffer_2.номер_порта_получателя = Unsignedinteger16кмассив(текущий.номер_порта_получателя)

	buffer_2.длина = Unsignedinteger16кмассив(текущий.длина)
	buffer_2.checksum = Unsignedinteger16кмассив(текущий.checksum)

}

type IПользовательdatagramprotocolhandler interface {
	РучкапользовательdatagramprotocolСообщение(сокет *TКонечная_точка_пользовательских_датаграмм, данные uintptr, размер uint16)
}

type TПользовательdatagramprotocolhandler struct {
}

func (текущий *TПользовательdatagramprotocolhandler) Init(backend TПоставщик_протокола_объединённой_сети) {
}
func (текущий *TПользовательdatagramprotocolhandler) РучкапользовательdatagramprotocolСообщение(сокет *TКонечная_точка_пользовательских_датаграмм, данные uintptr, размер uint16) {
}

type IПользовательdatagramprotocolсокет interface {
	РучкапользовательdatagramprotocolСообщение(данные uintptr, размер uint16)
}
type TКонечная_точка_пользовательских_датаграмм struct {
	сетьпортЧисло		uint16
	сетьip			uint32
	локальныйпортЧисло	uint16
	локальныйip		uint32

	listening	bool
}

var udpprovider TПользовательdatagramprotocolprovider
var udphandler IПользовательdatagramprotocolhandler

func (текущий *TКонечная_точка_пользовательских_датаграмм) Проверить() {
}
func (текущий *TКонечная_точка_пользовательских_датаграмм) Init(pudpprovider TПользовательdatagramprotocolprovider, pudphandler IПользовательdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	текущий.listening = false
}
func (текущий *TКонечная_точка_пользовательских_датаграмм) РучкапользовательdatagramprotocolСообщение(данные uintptr, размер uint16) {
	if udphandler != nil {
		udphandler.РучкапользовательdatagramprotocolСообщение(текущий, данные, размер)
	}
}
func (текущий *TКонечная_точка_пользовательских_датаграмм) Отправить(pданные []byte, размер uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(размер); i++ {
		buffer_2[i] = pданные[i]
	}
	var данные = uintptr(Pointer(&buffer_2))
	udpprovider.Отправить(текущий, данные, размер)
}
func (текущий *TКонечная_точка_пользовательских_датаграмм) Отключиться() {
	udpprovider.Отключиться(текущий)
}

type TПользовательdatagramprotocolprovider struct {
}

var iphandler IИнтернетprotocolhandler
var sockets [65535]TКонечная_точка_пользовательских_датаграмм
var числоsockets int
var свободнопорт uint16

func (текущий *TПользовательdatagramprotocolprovider) Init(pipprovider TПоставщик_протокола_объединённой_сети, piphandler IИнтернетprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	числоsockets = 0
	свободнопорт = 1024
}
func (текущий *TПользовательdatagramprotocolprovider) Интернетprotocolreceivewhen(источникipaddressсетьбайтorder uint32, назначениеipaddressсетьбайтorder uint32, интернетprotocolpayload uintptr, размер uint32) bool {
	if размер < udpзаголовокРазмер {
		return false
	}

	var buffer_2 *TПользовательdatagramprotocolзаголовокbuffer = (*TПользовательdatagramprotocolзаголовокbuffer)(Pointer(интернетprotocolpayload))
	var msg TЗаголовок_пользовательской_датаграммы
	msg.Init(buffer_2)

	var сокет *TКонечная_точка_пользовательских_датаграмм = nil

	for i := 0; i < числоsockets && сокет == nil; i++ {
		if sockets[i].локальныйпортЧисло == msg.номер_порта_получателя && sockets[i].локальныйip == назначениеipaddressсетьбайтorder && sockets[i].listening == true {
			сокет = &sockets[i]
			сокет.listening = false
			сокет.сетьпортЧисло = msg.номер_порта_отправителя
			сокет.сетьip = источникipaddressсетьбайтorder
		} else if sockets[i].локальныйпортЧисло == msg.номер_порта_получателя && sockets[i].локальныйip == назначениеipaddressсетьбайтorder && sockets[i].сетьпортЧисло == msg.номер_порта_отправителя && sockets[i].сетьip == источникipaddressсетьбайтorder {
			сокет = &sockets[i]

		}
	}

	msg.Указатьbuffer(buffer_2)
	if сокет != nil {
		сокет.РучкапользовательdatagramprotocolСообщение(интернетprotocolpayload+uintptr(udpзаголовокРазмер), uint16(размер-udpзаголовокРазмер))
	}

	return false
}

func (текущий *TПользовательdatagramprotocolprovider) Подключить(ip uint32, порт uint16) *TКонечная_точка_пользовательских_датаграмм {
	var памятьдиспетчер = &TПамятьдиспетчер{}
	var сокет = (*TКонечная_точка_пользовательских_датаграмм)(памятьдиспетчер.Выделить_память(50))

	if сокет != nil {

		сокет.Init(*текущий, nil)
		сокет.сетьпортЧисло = порт
		сокет.сетьip = ip
		сокет.локальныйпортЧисло = свободнопорт
		свободнопорт++
		сокет.локальныйip = uint32((*iphandler.Providerget()).Getipaddress())

		сокет.сетьпортЧисло = Unsignedinteger16r(сокет.сетьпортЧисло)
		сокет.локальныйпортЧисло = Unsignedinteger16r(сокет.локальныйпортЧисло)

		sockets[числоsockets] = *сокет
		числоsockets++

	}
	return сокет

}
func (текущий *TПользовательdatagramprotocolprovider) Listen(порт uint16) *TКонечная_точка_пользовательских_датаграмм {
	var сокет = &TКонечная_точка_пользовательских_датаграмм{}
	сокет = nil
	if сокет != nil {
		сокет.Init(*текущий, nil)
		сокет.listening = true
		сокет.локальныйпортЧисло = порт
		сокет.локальныйip = uint32((*iphandler.Providerget()).Getipaddress())

		сокет.локальныйпортЧисло = Unsignedinteger16r(сокет.локальныйпортЧисло)
	}
	return сокет
}
func (текущий *TПользовательdatagramprotocolprovider) Отключиться(сокет *TКонечная_точка_пользовательских_датаграмм) {
	for i := 0; i < числоsockets && сокет == nil; i++ {
		if sockets[i] == *сокет {
			числоsockets--
			sockets[i] = sockets[числоsockets]
			break
		}
	}
}
func (текущий *TПользовательdatagramprotocolprovider) Отправить(сокет *TКонечная_точка_пользовательских_датаграмм, pданные uintptr, размер uint16) {
	var всегоДлина = uint32(размер) + udpзаголовокРазмер

	var buffer_2 [4096]byte

	var msgbuffer = (*TПользовательdatagramprotocolзаголовокbuffer)(Pointer(&buffer_2))

	var msg = TЗаголовок_пользовательской_датаграммы{}

	msg.номер_порта_отправителя = сокет.локальныйпортЧисло
	msg.номер_порта_получателя = сокет.сетьпортЧисло
	msg.длина = Unsignedinteger16r(uint16(всегоДлина))

	msg.checksum = 0x0
	msg.Указатьbuffer(msgbuffer)

	var данныеБайт [4096]byte = *(*[4096]byte)(Pointer(pданные))
	for i := 0; i < int(размер); i++ {
		buffer_2[int(udpзаголовокРазмер)+i] = данныеБайт[i]
	}

	var данные uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Отправить(сокет.сетьip, 0x11, данные, всегоДлина)

}
func (текущий *TПользовательdatagramprotocolprovider) Прослушивать(сокет *TКонечная_точка_пользовательских_датаграмм, handler *TПользовательdatagramprotocolhandler,) {
}
