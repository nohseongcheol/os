/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "памяцьmanager"
import . "ipv4"

var udpconsole = TConsole{}

type TКарыстальнікdatagramprotocolheaderbuffer struct {
	крыніцаПортНУМАР	[2]byte
	destinationПортНУМАР	[2]byte

	даўжыня		[2]byte
	checksum	[2]byte
}

var udpheaderПамер uint32 = 8

type TКарыстальнікdatagramprotocolheader struct {
	крыніцаПортНУМАР	uint16
	destinationПортНУМАР	uint16

	даўжыня		uint16
	checksum	uint16
}

func (self *TКарыстальнікdatagramprotocolheader) Init(buffer_2 *TКарыстальнікdatagramprotocolheaderbuffer) {
	self.крыніцаПортНУМАР = Масіўtounsignedinteger16(buffer_2.крыніцаПортНУМАР)
	self.destinationПортНУМАР = Масіўtounsignedinteger16(buffer_2.destinationПортНУМАР)

	self.даўжыня = Масіўtounsignedinteger16(buffer_2.даўжыня)
	self.checksum = Масіўtounsignedinteger16(buffer_2.checksum)
}
func (self *TКарыстальнікdatagramprotocolheader) Вызначанаbuffer(buffer_2 *TКарыстальнікdatagramprotocolheaderbuffer) {

	buffer_2.крыніцаПортНУМАР = Unsignedinteger16toМасіў(self.крыніцаПортНУМАР)
	buffer_2.destinationПортНУМАР = Unsignedinteger16toМасіў(self.destinationПортНУМАР)

	buffer_2.даўжыня = Unsignedinteger16toМасіў(self.даўжыня)
	buffer_2.checksum = Unsignedinteger16toМасіў(self.checksum)

}

type IКарыстальнікdatagramprotocolhandler interface {
	HandleКарыстальнікdatagramprotocolпаведамленне(сокет *TКарыстальнікdatagramprotocolСокет, data uintptr, памер uint16)
}

type TКарыстальнікdatagramprotocolhandler struct {
}

func (self *TКарыстальнікdatagramprotocolhandler) Init(backend TІнтэрнэтprotocolprovider) {
}
func (self *TКарыстальнікdatagramprotocolhandler) HandleКарыстальнікdatagramprotocolпаведамленне(сокет *TКарыстальнікdatagramprotocolСокет, data uintptr, памер uint16) {
}

type IКарыстальнікdatagramprotocolСокет interface {
	HandleКарыстальнікdatagramprotocolпаведамленне(data uintptr, памер uint16)
}
type TКарыстальнікdatagramprotocolСокет struct {
	аддаленыПортНУМАР	uint16
	аддаленыip		uint32
	лакальныяПортНУМАР	uint16
	лакальныяip		uint32

	listening	bool
}

var udpprovider TКарыстальнікdatagramprotocolprovider
var udphandler IКарыстальнікdatagramprotocolhandler

func (self *TКарыстальнікdatagramprotocolСокет) Праверка() {
}
func (self *TКарыстальнікdatagramprotocolСокет) Init(pudpprovider TКарыстальнікdatagramprotocolprovider, pudphandler IКарыстальнікdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TКарыстальнікdatagramprotocolСокет) HandleКарыстальнікdatagramprotocolпаведамленне(data uintptr, памер uint16) {
	if udphandler != nil {
		udphandler.HandleКарыстальнікdatagramprotocolпаведамленне(self, data, памер)
	}
}
func (self *TКарыстальнікdatagramprotocolСокет) Даслаць(pdata []byte, памер uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(памер); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Даслаць(self, data, памер)
}
func (self *TКарыстальнікdatagramprotocolСокет) Адлучыцца() {
	udpprovider.Адлучыцца(self)
}

type TКарыстальнікdatagramprotocolprovider struct {
}

var iphandler IІнтэрнэтprotocolhandler
var sockets [65535]TКарыстальнікdatagramprotocolСокет
var нУМАРsockets int
var вольнаПорт uint16

func (self *TКарыстальнікdatagramprotocolprovider) Init(pipprovider TІнтэрнэтprotocolprovider, piphandler IІнтэрнэтprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	нУМАРsockets = 0
	вольнаПорт = 1024
}
func (self *TКарыстальнікdatagramprotocolprovider) Інтэрнэтprotocolreceivewhen(крыніцаipaddressСеткаbyteorder uint32, destinationipaddressСеткаbyteorder uint32, інтэрнэтprotocolpayload uintptr, памер uint32) bool {
	if памер < udpheaderПамер {
		return false
	}

	var buffer_2 *TКарыстальнікdatagramprotocolheaderbuffer = (*TКарыстальнікdatagramprotocolheaderbuffer)(Pointer(інтэрнэтprotocolpayload))
	var msg TКарыстальнікdatagramprotocolheader
	msg.Init(buffer_2)

	var сокет *TКарыстальнікdatagramprotocolСокет = nil

	for i := 0; i < нУМАРsockets && сокет == nil; i++ {
		if sockets[i].лакальныяПортНУМАР == msg.destinationПортНУМАР && sockets[i].лакальныяip == destinationipaddressСеткаbyteorder && sockets[i].listening == true {
			сокет = &sockets[i]
			сокет.listening = false
			сокет.аддаленыПортНУМАР = msg.крыніцаПортНУМАР
			сокет.аддаленыip = крыніцаipaddressСеткаbyteorder
		} else if sockets[i].лакальныяПортНУМАР == msg.destinationПортНУМАР && sockets[i].лакальныяip == destinationipaddressСеткаbyteorder && sockets[i].аддаленыПортНУМАР == msg.крыніцаПортНУМАР && sockets[i].аддаленыip == крыніцаipaddressСеткаbyteorder {
			сокет = &sockets[i]

		}
	}

	msg.Вызначанаbuffer(buffer_2)
	if сокет != nil {
		сокет.HandleКарыстальнікdatagramprotocolпаведамленне(інтэрнэтprotocolpayload+uintptr(udpheaderПамер), uint16(памер-udpheaderПамер))
	}

	return false
}

func (self *TКарыстальнікdatagramprotocolprovider) Злучыцца(ip uint32, порт uint16) *TКарыстальнікdatagramprotocolСокет {
	var памяцьmanager = &TПамяцьmanager{}
	var сокет = (*TКарыстальнікdatagramprotocolСокет)(памяцьmanager.Malloc(50))

	if сокет != nil {

		сокет.Init(*self, nil)
		сокет.аддаленыПортНУМАР = порт
		сокет.аддаленыip = ip
		сокет.лакальныяПортНУМАР = вольнаПорт
		вольнаПорт++
		сокет.лакальныяip = uint32((*iphandler.Providerget()).Getipaddress())

		сокет.аддаленыПортНУМАР = Unsignedinteger16r(сокет.аддаленыПортНУМАР)
		сокет.лакальныяПортНУМАР = Unsignedinteger16r(сокет.лакальныяПортНУМАР)

		sockets[нУМАРsockets] = *сокет
		нУМАРsockets++

	}
	return сокет

}
func (self *TКарыстальнікdatagramprotocolprovider) Listen(порт uint16) *TКарыстальнікdatagramprotocolСокет {
	var сокет = &TКарыстальнікdatagramprotocolСокет{}
	сокет = nil
	if сокет != nil {
		сокет.Init(*self, nil)
		сокет.listening = true
		сокет.лакальныяПортНУМАР = порт
		сокет.лакальныяip = uint32((*iphandler.Providerget()).Getipaddress())

		сокет.лакальныяПортНУМАР = Unsignedinteger16r(сокет.лакальныяПортНУМАР)
	}
	return сокет
}
func (self *TКарыстальнікdatagramprotocolprovider) Адлучыцца(сокет *TКарыстальнікdatagramprotocolСокет) {
	for i := 0; i < нУМАРsockets && сокет == nil; i++ {
		if sockets[i] == *сокет {
			нУМАРsockets--
			sockets[i] = sockets[нУМАРsockets]
			break
		}
	}
}
func (self *TКарыстальнікdatagramprotocolprovider) Даслаць(сокет *TКарыстальнікdatagramprotocolСокет, pdata uintptr, памер uint16) {
	var агуламДаўжыня = uint32(памер) + udpheaderПамер

	var buffer_2 [4096]byte

	var msgbuffer = (*TКарыстальнікdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TКарыстальнікdatagramprotocolheader{}

	msg.крыніцаПортНУМАР = сокет.лакальныяПортНУМАР
	msg.destinationПортНУМАР = сокет.аддаленыПортНУМАР
	msg.даўжыня = Unsignedinteger16r(uint16(агуламДаўжыня))

	msg.checksum = 0x0
	msg.Вызначанаbuffer(msgbuffer)

	var dataБайтаў [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(памер); i++ {
		buffer_2[int(udpheaderПамер)+i] = dataБайтаў[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Даслаць(сокет.аддаленыip, 0x11, data, агуламДаўжыня)

}
func (self *TКарыстальнікdatagramprotocolprovider) Bind(сокет *TКарыстальнікdatagramprotocolСокет, handler *TКарыстальнікdatagramprotocolhandler,) {
}
