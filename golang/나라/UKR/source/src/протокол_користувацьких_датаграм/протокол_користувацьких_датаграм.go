/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package протокол_користувацьких_датаграм

import . "unsafe"
import . "консоль"
import . "util"
import . "памятьmanager"
import . "протокол_обʼєднаної_мережі_4"

var udpКонсоль = TКонсоль{}

type TКористувачdatagramprotocolheaderbuffer struct {
	номер_порту_відправника	[2]byte
	номер_порту_одержувача	[2]byte

	довжина		[2]byte
	checksum	[2]byte
}

var udpheaderРозмір uint32 = 8

type TЗаголовок_користувацької_датаграми struct {
	номер_порту_відправника	uint16
	номер_порту_одержувача	uint16

	довжина		uint16
	checksum	uint16
}

func (поточний *TЗаголовок_користувацької_датаграми) Init(buffer_2 *TКористувачdatagramprotocolheaderbuffer) {
	поточний.номер_порту_відправника = Масивтоunsignedinteger16(buffer_2.номер_порту_відправника)
	поточний.номер_порту_одержувача = Масивтоunsignedinteger16(buffer_2.номер_порту_одержувача)

	поточний.довжина = Масивтоunsignedinteger16(buffer_2.довжина)
	поточний.checksum = Масивтоunsignedinteger16(buffer_2.checksum)
}
func (поточний *TЗаголовок_користувацької_датаграми) Множинаbuffer(buffer_2 *TКористувачdatagramprotocolheaderbuffer) {

	buffer_2.номер_порту_відправника = Unsignedinteger16тоМасив(поточний.номер_порту_відправника)
	buffer_2.номер_порту_одержувача = Unsignedinteger16тоМасив(поточний.номер_порту_одержувача)

	buffer_2.довжина = Unsignedinteger16тоМасив(поточний.довжина)
	buffer_2.checksum = Unsignedinteger16тоМасив(поточний.checksum)

}

type IКористувачdatagramprotocolhandler interface {
	ЕлементкеруванняКористувачdatagramprotocolПовідомлення(сокет *TКінцева_точка_користувацьких_датаграм, data uintptr, розмір uint16)
}

type TКористувачdatagramprotocolhandler struct {
}

func (поточний *TКористувачdatagramprotocolhandler) Init(backend TПостачальник_протоколу_обʼєднаної_мережі) {
}
func (поточний *TКористувачdatagramprotocolhandler) ЕлементкеруванняКористувачdatagramprotocolПовідомлення(сокет *TКінцева_точка_користувацьких_датаграм, data uintptr, розмір uint16) {
}

type IКористувачdatagramprotocolСокет interface {
	ЕлементкеруванняКористувачdatagramprotocolПовідомлення(data uintptr, розмір uint16)
}
type TКінцева_точка_користувацьких_датаграм struct {
	віддаленеПортЧисло	uint16
	віддаленеip		uint32
	локальнийПортЧисло	uint16
	локальнийip		uint32

	listening	bool
}

var udpprovider TКористувачdatagramprotocolprovider
var udphandler IКористувачdatagramprotocolhandler

func (поточний *TКінцева_точка_користувацьких_датаграм) Тест() {
}
func (поточний *TКінцева_точка_користувацьких_датаграм) Init(pudpprovider TКористувачdatagramprotocolprovider, pudphandler IКористувачdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	поточний.listening = false
}
func (поточний *TКінцева_точка_користувацьких_датаграм) ЕлементкеруванняКористувачdatagramprotocolПовідомлення(data uintptr, розмір uint16) {
	if udphandler != nil {
		udphandler.ЕлементкеруванняКористувачdatagramprotocolПовідомлення(поточний, data, розмір)
	}
}
func (поточний *TКінцева_точка_користувацьких_датаграм) Надіслати(pdata []byte, розмір uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(розмір); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Надіслати(поточний, data, розмір)
}
func (поточний *TКінцева_точка_користувацьких_датаграм) Відєднатися() {
	udpprovider.Відєднатися(поточний)
}

type TКористувачdatagramprotocolprovider struct {
}

var iphandler IІнтернетprotocolhandler
var sockets [65535]TКінцева_точка_користувацьких_датаграм
var числоsockets int
var вільноПорт uint16

func (поточний *TКористувачdatagramprotocolprovider) Init(pipprovider TПостачальник_протоколу_обʼєднаної_мережі, piphandler IІнтернетprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	числоsockets = 0
	вільноПорт = 1024
}
func (поточний *TКористувачdatagramprotocolprovider) Інтернетprotocolreceivewhen(джерелоipАдресаМережаbyteorder uint32, призначенняipАдресаМережаbyteorder uint32, інтернетprotocolpayload uintptr, розмір uint32) bool {
	if розмір < udpheaderРозмір {
		return false
	}

	var buffer_2 *TКористувачdatagramprotocolheaderbuffer = (*TКористувачdatagramprotocolheaderbuffer)(Pointer(інтернетprotocolpayload))
	var msg TЗаголовок_користувацької_датаграми
	msg.Init(buffer_2)

	var сокет *TКінцева_точка_користувацьких_датаграм = nil

	for i := 0; i < числоsockets && сокет == nil; i++ {
		if sockets[i].локальнийПортЧисло == msg.номер_порту_одержувача && sockets[i].локальнийip == призначенняipАдресаМережаbyteorder && sockets[i].listening == true {
			сокет = &sockets[i]
			сокет.listening = false
			сокет.віддаленеПортЧисло = msg.номер_порту_відправника
			сокет.віддаленеip = джерелоipАдресаМережаbyteorder
		} else if sockets[i].локальнийПортЧисло == msg.номер_порту_одержувача && sockets[i].локальнийip == призначенняipАдресаМережаbyteorder && sockets[i].віддаленеПортЧисло == msg.номер_порту_відправника && sockets[i].віддаленеip == джерелоipАдресаМережаbyteorder {
			сокет = &sockets[i]

		}
	}

	msg.Множинаbuffer(buffer_2)
	if сокет != nil {
		сокет.ЕлементкеруванняКористувачdatagramprotocolПовідомлення(інтернетprotocolpayload+uintptr(udpheaderРозмір), uint16(розмір-udpheaderРозмір))
	}

	return false
}

func (поточний *TКористувачdatagramprotocolprovider) Зєднати(ip uint32, порт uint16) *TКінцева_точка_користувацьких_датаграм {
	var памятьmanager = &TПамятьmanager{}
	var сокет = (*TКінцева_точка_користувацьких_датаграм)(памятьmanager.Виділити_памʼять(50))

	if сокет != nil {

		сокет.Init(*поточний, nil)
		сокет.віддаленеПортЧисло = порт
		сокет.віддаленеip = ip
		сокет.локальнийПортЧисло = вільноПорт
		вільноПорт++
		сокет.локальнийip = uint32((*iphandler.Providerget()).GetipАдреса())

		сокет.віддаленеПортЧисло = Unsignedinteger16r(сокет.віддаленеПортЧисло)
		сокет.локальнийПортЧисло = Unsignedinteger16r(сокет.локальнийПортЧисло)

		sockets[числоsockets] = *сокет
		числоsockets++

	}
	return сокет

}
func (поточний *TКористувачdatagramprotocolprovider) Listen(порт uint16) *TКінцева_точка_користувацьких_датаграм {
	var сокет = &TКінцева_точка_користувацьких_датаграм{}
	сокет = nil
	if сокет != nil {
		сокет.Init(*поточний, nil)
		сокет.listening = true
		сокет.локальнийПортЧисло = порт
		сокет.локальнийip = uint32((*iphandler.Providerget()).GetipАдреса())

		сокет.локальнийПортЧисло = Unsignedinteger16r(сокет.локальнийПортЧисло)
	}
	return сокет
}
func (поточний *TКористувачdatagramprotocolprovider) Відєднатися(сокет *TКінцева_точка_користувацьких_датаграм) {
	for i := 0; i < числоsockets && сокет == nil; i++ {
		if sockets[i] == *сокет {
			числоsockets--
			sockets[i] = sockets[числоsockets]
			break
		}
	}
}
func (поточний *TКористувачdatagramprotocolprovider) Надіслати(сокет *TКінцева_точка_користувацьких_датаграм, pdata uintptr, розмір uint16) {
	var усьогоДовжина = uint32(розмір) + udpheaderРозмір

	var buffer_2 [4096]byte

	var msgbuffer = (*TКористувачdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TЗаголовок_користувацької_датаграми{}

	msg.номер_порту_відправника = сокет.локальнийПортЧисло
	msg.номер_порту_одержувача = сокет.віддаленеПортЧисло
	msg.довжина = Unsignedinteger16r(uint16(усьогоДовжина))

	msg.checksum = 0x0
	msg.Множинаbuffer(msgbuffer)

	var dataБайт [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(розмір); i++ {
		buffer_2[int(udpheaderРозмір)+i] = dataБайт[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Надіслати(сокет.віддаленеip, 0x11, data, усьогоДовжина)

}
func (поточний *TКористувачdatagramprotocolprovider) Повязати(сокет *TКінцева_точка_користувацьких_датаграм, handler *TКористувачdatagramprotocolhandler,) {
}
