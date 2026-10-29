/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "паметmanager"
import . "ipv4"

var udpconsole = TConsole{}

type TСобственикdatagramprotocolheaderbuffer struct {
	източникПортЧисло	[2]byte
	назначениеПортЧисло	[2]byte

	дължина		[2]byte
	checksum	[2]byte
}

var udpheaderРазмер uint32 = 8

type TСобственикdatagramprotocolheader struct {
	източникПортЧисло	uint16
	назначениеПортЧисло	uint16

	дължина		uint16
	checksum	uint16
}

func (себеси *TСобственикdatagramprotocolheader) Init(buffer_2 *TСобственикdatagramprotocolheaderbuffer) {
	себеси.източникПортЧисло = Масивtounsignedinteger16(buffer_2.източникПортЧисло)
	себеси.назначениеПортЧисло = Масивtounsignedinteger16(buffer_2.назначениеПортЧисло)

	себеси.дължина = Масивtounsignedinteger16(buffer_2.дължина)
	себеси.checksum = Масивtounsignedinteger16(buffer_2.checksum)
}
func (себеси *TСобственикdatagramprotocolheader) Задайbuffer(buffer_2 *TСобственикdatagramprotocolheaderbuffer) {

	buffer_2.източникПортЧисло = Unsignedinteger16toМасив(себеси.източникПортЧисло)
	buffer_2.назначениеПортЧисло = Unsignedinteger16toМасив(себеси.назначениеПортЧисло)

	buffer_2.дължина = Unsignedinteger16toМасив(себеси.дължина)
	buffer_2.checksum = Unsignedinteger16toМасив(себеси.checksum)

}

type IСобственикdatagramprotocolhandler interface {
	РъкохваткаСобственикdatagramprotocolСЪОБЩЕНИЕ(socket *TСобственикdatagramprotocolsocket, data uintptr, размер uint16)
}

type TСобственикdatagramprotocolhandler struct {
}

func (себеси *TСобственикdatagramprotocolhandler) Init(backend TИнтернетprotocolprovider) {
}
func (себеси *TСобственикdatagramprotocolhandler) РъкохваткаСобственикdatagramprotocolСЪОБЩЕНИЕ(socket *TСобственикdatagramprotocolsocket, data uintptr, размер uint16) {
}

type IСобственикdatagramprotocolsocket interface {
	РъкохваткаСобственикdatagramprotocolСЪОБЩЕНИЕ(data uintptr, размер uint16)
}
type TСобственикdatagramprotocolsocket struct {
	отдалеченПортЧисло	uint16
	отдалеченip		uint32
	локалноПортЧисло	uint16
	локалноip		uint32

	listening	bool
}

var udpprovider TСобственикdatagramprotocolprovider
var udphandler IСобственикdatagramprotocolhandler

func (себеси *TСобственикdatagramprotocolsocket) Тест() {
}
func (себеси *TСобственикdatagramprotocolsocket) Init(pudpprovider TСобственикdatagramprotocolprovider, pudphandler IСобственикdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	себеси.listening = false
}
func (себеси *TСобственикdatagramprotocolsocket) РъкохваткаСобственикdatagramprotocolСЪОБЩЕНИЕ(data uintptr, размер uint16) {
	if udphandler != nil {
		udphandler.РъкохваткаСобственикdatagramprotocolСЪОБЩЕНИЕ(себеси, data, размер)
	}
}
func (себеси *TСобственикdatagramprotocolsocket) Изпращане(pdata []byte, размер uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(размер); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Изпращане(себеси, data, размер)
}
func (себеси *TСобственикdatagramprotocolsocket) Изключване() {
	udpprovider.Изключване(себеси)
}

type TСобственикdatagramprotocolprovider struct {
}

var iphandler IИнтернетprotocolhandler
var sockets [65535]TСобственикdatagramprotocolsocket
var числоsockets int
var свободноПорт uint16

func (себеси *TСобственикdatagramprotocolprovider) Init(pipprovider TИнтернетprotocolprovider, piphandler IИнтернетprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	числоsockets = 0
	свободноПорт = 1024
}
func (себеси *TСобственикdatagramprotocolprovider) Интернетprotocolreceivewhen(източникipaddressМрежаbyteorder uint32, назначениеipaddressМрежаbyteorder uint32, интернетprotocolpayload uintptr, размер uint32) bool {
	if размер < udpheaderРазмер {
		return false
	}

	var buffer_2 *TСобственикdatagramprotocolheaderbuffer = (*TСобственикdatagramprotocolheaderbuffer)(Pointer(интернетprotocolpayload))
	var msg TСобственикdatagramprotocolheader
	msg.Init(buffer_2)

	var socket *TСобственикdatagramprotocolsocket = nil

	for i := 0; i < числоsockets && socket == nil; i++ {
		if sockets[i].локалноПортЧисло == msg.назначениеПортЧисло && sockets[i].локалноip == назначениеipaddressМрежаbyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.отдалеченПортЧисло = msg.източникПортЧисло
			socket.отдалеченip = източникipaddressМрежаbyteorder
		} else if sockets[i].локалноПортЧисло == msg.назначениеПортЧисло && sockets[i].локалноip == назначениеipaddressМрежаbyteorder && sockets[i].отдалеченПортЧисло == msg.източникПортЧисло && sockets[i].отдалеченip == източникipaddressМрежаbyteorder {
			socket = &sockets[i]

		}
	}

	msg.Задайbuffer(buffer_2)
	if socket != nil {
		socket.РъкохваткаСобственикdatagramprotocolСЪОБЩЕНИЕ(интернетprotocolpayload+uintptr(udpheaderРазмер), uint16(размер-udpheaderРазмер))
	}

	return false
}

func (себеси *TСобственикdatagramprotocolprovider) Свързване(ip uint32, порт uint16) *TСобственикdatagramprotocolsocket {
	var паметmanager = &TПаметmanager{}
	var socket = (*TСобственикdatagramprotocolsocket)(паметmanager.Malloc(50))

	if socket != nil {

		socket.Init(*себеси, nil)
		socket.отдалеченПортЧисло = порт
		socket.отдалеченip = ip
		socket.локалноПортЧисло = свободноПорт
		свободноПорт++
		socket.локалноip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.отдалеченПортЧисло = Unsignedinteger16r(socket.отдалеченПортЧисло)
		socket.локалноПортЧисло = Unsignedinteger16r(socket.локалноПортЧисло)

		sockets[числоsockets] = *socket
		числоsockets++

	}
	return socket

}
func (себеси *TСобственикdatagramprotocolprovider) Listen(порт uint16) *TСобственикdatagramprotocolsocket {
	var socket = &TСобственикdatagramprotocolsocket{}
	socket = nil
	if socket != nil {
		socket.Init(*себеси, nil)
		socket.listening = true
		socket.локалноПортЧисло = порт
		socket.локалноip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.локалноПортЧисло = Unsignedinteger16r(socket.локалноПортЧисло)
	}
	return socket
}
func (себеси *TСобственикdatagramprotocolprovider) Изключване(socket *TСобственикdatagramprotocolsocket) {
	for i := 0; i < числоsockets && socket == nil; i++ {
		if sockets[i] == *socket {
			числоsockets--
			sockets[i] = sockets[числоsockets]
			break
		}
	}
}
func (себеси *TСобственикdatagramprotocolprovider) Изпращане(socket *TСобственикdatagramprotocolsocket, pdata uintptr, размер uint16) {
	var общодължина = uint32(размер) + udpheaderРазмер

	var buffer_2 [4096]byte

	var msgbuffer = (*TСобственикdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TСобственикdatagramprotocolheader{}

	msg.източникПортЧисло = socket.локалноПортЧисло
	msg.назначениеПортЧисло = socket.отдалеченПортЧисло
	msg.дължина = Unsignedinteger16r(uint16(общодължина))

	msg.checksum = 0x0
	msg.Задайbuffer(msgbuffer)

	var dataБайтове [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(размер); i++ {
		buffer_2[int(udpheaderРазмер)+i] = dataБайтове[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Изпращане(socket.отдалеченip, 0x11, data, общодължина)

}
func (себеси *TСобственикdatagramprotocolprovider) Bind(socket *TСобственикdatagramprotocolsocket, handler *TСобственикdatagramprotocolhandler,) {
}
