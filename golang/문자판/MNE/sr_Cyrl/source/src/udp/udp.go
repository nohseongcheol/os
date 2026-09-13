package udp

import . "unsafe"
import . "конзола"
import . "util"
import . "меморијаmanager"
import . "ipv4"

var udpКонзола = TКонзола{}

type TКорисникdatagramprotocolheaderbuffer struct {
	изворПортброј		[2]byte
	одредиштеПортброј	[2]byte

	дужина		[2]byte
	checksum	[2]byte
}

var udpheaderВеличина uint32 = 8

type TКорисникdatagramprotocolheader struct {
	изворПортброј		uint16
	одредиштеПортброј	uint16

	дужина		uint16
	checksum	uint16
}

func (исти *TКорисникdatagramprotocolheader) Init(buffer_2 *TКорисникdatagramprotocolheaderbuffer) {
	исти.изворПортброј = Низtounsignedinteger16(buffer_2.изворПортброј)
	исти.одредиштеПортброј = Низtounsignedinteger16(buffer_2.одредиштеПортброј)

	исти.дужина = Низtounsignedinteger16(buffer_2.дужина)
	исти.checksum = Низtounsignedinteger16(buffer_2.checksum)
}
func (исти *TКорисникdatagramprotocolheader) Скупbuffer(buffer_2 *TКорисникdatagramprotocolheaderbuffer) {

	buffer_2.изворПортброј = Unsignedinteger16toНиз(исти.изворПортброј)
	buffer_2.одредиштеПортброј = Unsignedinteger16toНиз(исти.одредиштеПортброј)

	buffer_2.дужина = Unsignedinteger16toНиз(исти.дужина)
	buffer_2.checksum = Unsignedinteger16toНиз(исти.checksum)

}

type IКорисникdatagramprotocolhandler interface {
	РучкаКорисникdatagramprotocolпорука(прикључница *TКорисникdatagramprotocolПрикључница, data uintptr, величина uint16)
}

type TКорисникdatagramprotocolhandler struct {
}

func (исти *TКорисникdatagramprotocolhandler) Init(backend TИнтернетprotocolprovider) {
}
func (исти *TКорисникdatagramprotocolhandler) РучкаКорисникdatagramprotocolпорука(прикључница *TКорисникdatagramprotocolПрикључница, data uintptr, величина uint16) {
}

type IКорисникdatagramprotocolПрикључница interface {
	РучкаКорисникdatagramprotocolпорука(data uintptr, величина uint16)
}
type TКорисникdatagramprotocolПрикључница struct {
	удаљеноПортброј	uint16
	удаљеноip	uint32
	локалнаПортброј	uint16
	локалнаip	uint32

	listening	bool
}

var udpprovider TКорисникdatagramprotocolprovider
var udphandler IКорисникdatagramprotocolhandler

func (исти *TКорисникdatagramprotocolПрикључница) Тест() {
}
func (исти *TКорисникdatagramprotocolПрикључница) Init(pudpprovider TКорисникdatagramprotocolprovider, pudphandler IКорисникdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	исти.listening = false
}
func (исти *TКорисникdatagramprotocolПрикључница) РучкаКорисникdatagramprotocolпорука(data uintptr, величина uint16) {
	if udphandler != nil {
		udphandler.РучкаКорисникdatagramprotocolпорука(исти, data, величина)
	}
}
func (исти *TКорисникdatagramprotocolПрикључница) Пошаљи(pdata []byte, величина uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(величина); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Пошаљи(исти, data, величина)
}
func (исти *TКорисникdatagramprotocolПрикључница) Прекинивезу() {
	udpprovider.Прекинивезу(исти)
}

type TКорисникdatagramprotocolprovider struct {
}

var iphandler IИнтернетprotocolhandler
var sockets [65535]TКорисникdatagramprotocolПрикључница
var бројsockets int
var слободноПорт uint16

func (исти *TКорисникdatagramprotocolprovider) Init(pipprovider TИнтернетprotocolprovider, piphandler IИнтернетprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	бројsockets = 0
	слободноПорт = 1024
}
func (исти *TКорисникdatagramprotocolprovider) Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, интернетprotocolpayload uintptr, величина uint32) bool {
	if величина < udpheaderВеличина {
		return false
	}

	var buffer_2 *TКорисникdatagramprotocolheaderbuffer = (*TКорисникdatagramprotocolheaderbuffer)(Pointer(интернетprotocolpayload))
	var msg TКорисникdatagramprotocolheader
	msg.Init(buffer_2)

	var прикључница *TКорисникdatagramprotocolПрикључница = nil

	for i := 0; i < бројsockets && прикључница == nil; i++ {
		if sockets[i].локалнаПортброј == msg.одредиштеПортброј && sockets[i].локалнаip == одредиштеipaddressМрежаbyteorder && sockets[i].listening == true {
			прикључница = &sockets[i]
			прикључница.listening = false
			прикључница.удаљеноПортброј = msg.изворПортброј
			прикључница.удаљеноip = изворipaddressМрежаbyteorder
		} else if sockets[i].локалнаПортброј == msg.одредиштеПортброј && sockets[i].локалнаip == одредиштеipaddressМрежаbyteorder && sockets[i].удаљеноПортброј == msg.изворПортброј && sockets[i].удаљеноip == изворipaddressМрежаbyteorder {
			прикључница = &sockets[i]

		}
	}

	msg.Скупbuffer(buffer_2)
	if прикључница != nil {
		прикључница.РучкаКорисникdatagramprotocolпорука(интернетprotocolpayload+uintptr(udpheaderВеличина), uint16(величина-udpheaderВеличина))
	}

	return false
}

func (исти *TКорисникdatagramprotocolprovider) Повежисе(ip uint32, порт uint16) *TКорисникdatagramprotocolПрикључница {
	var меморијаmanager = &TМеморијаmanager{}
	var прикључница = (*TКорисникdatagramprotocolПрикључница)(меморијаmanager.Malloc(50))

	if прикључница != nil {

		прикључница.Init(*исти, nil)
		прикључница.удаљеноПортброј = порт
		прикључница.удаљеноip = ip
		прикључница.локалнаПортброј = слободноПорт
		слободноПорт++
		прикључница.локалнаip = uint32((*iphandler.Providerget()).Getipaddress())

		прикључница.удаљеноПортброј = Unsignedinteger16r(прикључница.удаљеноПортброј)
		прикључница.локалнаПортброј = Unsignedinteger16r(прикључница.локалнаПортброј)

		sockets[бројsockets] = *прикључница
		бројsockets++

	}
	return прикључница

}
func (исти *TКорисникdatagramprotocolprovider) Listen(порт uint16) *TКорисникdatagramprotocolПрикључница {
	var прикључница = &TКорисникdatagramprotocolПрикључница{}
	прикључница = nil
	if прикључница != nil {
		прикључница.Init(*исти, nil)
		прикључница.listening = true
		прикључница.локалнаПортброј = порт
		прикључница.локалнаip = uint32((*iphandler.Providerget()).Getipaddress())

		прикључница.локалнаПортброј = Unsignedinteger16r(прикључница.локалнаПортброј)
	}
	return прикључница
}
func (исти *TКорисникdatagramprotocolprovider) Прекинивезу(прикључница *TКорисникdatagramprotocolПрикључница) {
	for i := 0; i < бројsockets && прикључница == nil; i++ {
		if sockets[i] == *прикључница {
			бројsockets--
			sockets[i] = sockets[бројsockets]
			break
		}
	}
}
func (исти *TКорисникdatagramprotocolprovider) Пошаљи(прикључница *TКорисникdatagramprotocolПрикључница, pdata uintptr, величина uint16) {
	var укупноДужина = uint32(величина) + udpheaderВеличина

	var buffer_2 [4096]byte

	var msgbuffer = (*TКорисникdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TКорисникdatagramprotocolheader{}

	msg.изворПортброј = прикључница.локалнаПортброј
	msg.одредиштеПортброј = прикључница.удаљеноПортброј
	msg.дужина = Unsignedinteger16r(uint16(укупноДужина))

	msg.checksum = 0x0
	msg.Скупbuffer(msgbuffer)

	var dataБајтова [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(величина); i++ {
		buffer_2[int(udpheaderВеличина)+i] = dataБајтова[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Пошаљи(прикључница.удаљеноip, 0x11, data, укупноДужина)

}
func (исти *TКорисникdatagramprotocolprovider) Bind(прикључница *TКорисникdatagramprotocolПрикључница, handler *TКорисникdatagramprotocolhandler) {
}
