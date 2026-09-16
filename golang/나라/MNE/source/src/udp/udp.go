/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "конзола"
import . "util"
import . "memorijamanager"
import . "ipv4"

var udpКонзола = TКонзола{}

type TKorisnikdatagramprotocolheaderbuffer struct {
	izvorПортброј		[2]byte
	odredišteПортброј	[2]byte

	dužina		[2]byte
	checksum	[2]byte
}

var udpheaderВеличина uint32 = 8

type TKorisnikdatagramprotocolheader struct {
	izvorПортброј		uint16
	odredišteПортброј	uint16

	dužina		uint16
	checksum	uint16
}

func (isti *TKorisnikdatagramprotocolheader) Init(buffer_2 *TKorisnikdatagramprotocolheaderbuffer) {
	isti.izvorПортброј = Низtounsignedinteger16(buffer_2.izvorПортброј)
	isti.odredišteПортброј = Низtounsignedinteger16(buffer_2.odredišteПортброј)

	isti.dužina = Низtounsignedinteger16(buffer_2.dužina)
	isti.checksum = Низtounsignedinteger16(buffer_2.checksum)
}
func (isti *TKorisnikdatagramprotocolheader) Скупbuffer(buffer_2 *TKorisnikdatagramprotocolheaderbuffer) {

	buffer_2.izvorПортброј = Unsignedinteger16toНиз(isti.izvorПортброј)
	buffer_2.odredišteПортброј = Unsignedinteger16toНиз(isti.odredišteПортброј)

	buffer_2.dužina = Unsignedinteger16toНиз(isti.dužina)
	buffer_2.checksum = Unsignedinteger16toНиз(isti.checksum)

}

type IKorisnikdatagramprotocolhandler interface {
	РучкаKorisnikdatagramprotocolпорука(прикључница *TKorisnikdatagramprotocolПрикључница, data uintptr, величина uint16)
}

type TKorisnikdatagramprotocolhandler struct {
}

func (isti *TKorisnikdatagramprotocolhandler) Init(backend TИнтернетprotocolprovider) {
}
func (isti *TKorisnikdatagramprotocolhandler) РучкаKorisnikdatagramprotocolпорука(прикључница *TKorisnikdatagramprotocolПрикључница, data uintptr, величина uint16) {
}

type IKorisnikdatagramprotocolПрикључница interface {
	РучкаKorisnikdatagramprotocolпорука(data uintptr, величина uint16)
}
type TKorisnikdatagramprotocolПрикључница struct {
	удаљеноПортброј	uint16
	удаљеноip	uint32
	локалнаПортброј	uint16
	локалнаip	uint32

	listening	bool
}

var udpprovider TKorisnikdatagramprotocolprovider
var udphandler IKorisnikdatagramprotocolhandler

func (isti *TKorisnikdatagramprotocolПрикључница) Тест() {
}
func (isti *TKorisnikdatagramprotocolПрикључница) Init(pudpprovider TKorisnikdatagramprotocolprovider, pudphandler IKorisnikdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	isti.listening = false
}
func (isti *TKorisnikdatagramprotocolПрикључница) РучкаKorisnikdatagramprotocolпорука(data uintptr, величина uint16) {
	if udphandler != nil {
		udphandler.РучкаKorisnikdatagramprotocolпорука(isti, data, величина)
	}
}
func (isti *TKorisnikdatagramprotocolПрикључница) Пошаљи(pdata []byte, величина uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(величина); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Пошаљи(isti, data, величина)
}
func (isti *TKorisnikdatagramprotocolПрикључница) Prekinivezu() {
	udpprovider.Prekinivezu(isti)
}

type TKorisnikdatagramprotocolprovider struct {
}

var iphandler IИнтернетprotocolhandler
var sockets [65535]TKorisnikdatagramprotocolПрикључница
var бројsockets int
var slobodnoПорт uint16

func (isti *TKorisnikdatagramprotocolprovider) Init(pipprovider TИнтернетprotocolprovider, piphandler IИнтернетprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	бројsockets = 0
	slobodnoПорт = 1024
}
func (isti *TKorisnikdatagramprotocolprovider) Интернетprotocolreceivewhen(izvoripaddressМрежаbyteorder uint32, odredišteipaddressМрежаbyteorder uint32, интернетprotocolpayload uintptr, величина uint32) bool {
	if величина < udpheaderВеличина {
		return false
	}

	var buffer_2 *TKorisnikdatagramprotocolheaderbuffer = (*TKorisnikdatagramprotocolheaderbuffer)(Pointer(интернетprotocolpayload))
	var msg TKorisnikdatagramprotocolheader
	msg.Init(buffer_2)

	var прикључница *TKorisnikdatagramprotocolПрикључница = nil

	for i := 0; i < бројsockets && прикључница == nil; i++ {
		if sockets[i].локалнаПортброј == msg.odredišteПортброј && sockets[i].локалнаip == odredišteipaddressМрежаbyteorder && sockets[i].listening == true {
			прикључница = &sockets[i]
			прикључница.listening = false
			прикључница.удаљеноПортброј = msg.izvorПортброј
			прикључница.удаљеноip = izvoripaddressМрежаbyteorder
		} else if sockets[i].локалнаПортброј == msg.odredišteПортброј && sockets[i].локалнаip == odredišteipaddressМрежаbyteorder && sockets[i].удаљеноПортброј == msg.izvorПортброј && sockets[i].удаљеноip == izvoripaddressМрежаbyteorder {
			прикључница = &sockets[i]

		}
	}

	msg.Скупbuffer(buffer_2)
	if прикључница != nil {
		прикључница.РучкаKorisnikdatagramprotocolпорука(интернетprotocolpayload+uintptr(udpheaderВеличина), uint16(величина-udpheaderВеличина))
	}

	return false
}

func (isti *TKorisnikdatagramprotocolprovider) Povežise(ip uint32, порт uint16) *TKorisnikdatagramprotocolПрикључница {
	var memorijamanager = &TMemorijamanager{}
	var прикључница = (*TKorisnikdatagramprotocolПрикључница)(memorijamanager.Malloc(50))

	if прикључница != nil {

		прикључница.Init(*isti, nil)
		прикључница.удаљеноПортброј = порт
		прикључница.удаљеноip = ip
		прикључница.локалнаПортброј = slobodnoПорт
		slobodnoПорт++
		прикључница.локалнаip = uint32((*iphandler.Providerget()).Getipaddress())

		прикључница.удаљеноПортброј = Unsignedinteger16r(прикључница.удаљеноПортброј)
		прикључница.локалнаПортброј = Unsignedinteger16r(прикључница.локалнаПортброј)

		sockets[бројsockets] = *прикључница
		бројsockets++

	}
	return прикључница

}
func (isti *TKorisnikdatagramprotocolprovider) Listen(порт uint16) *TKorisnikdatagramprotocolПрикључница {
	var прикључница = &TKorisnikdatagramprotocolПрикључница{}
	прикључница = nil
	if прикључница != nil {
		прикључница.Init(*isti, nil)
		прикључница.listening = true
		прикључница.локалнаПортброј = порт
		прикључница.локалнаip = uint32((*iphandler.Providerget()).Getipaddress())

		прикључница.локалнаПортброј = Unsignedinteger16r(прикључница.локалнаПортброј)
	}
	return прикључница
}
func (isti *TKorisnikdatagramprotocolprovider) Prekinivezu(прикључница *TKorisnikdatagramprotocolПрикључница) {
	for i := 0; i < бројsockets && прикључница == nil; i++ {
		if sockets[i] == *прикључница {
			бројsockets--
			sockets[i] = sockets[бројsockets]
			break
		}
	}
}
func (isti *TKorisnikdatagramprotocolprovider) Пошаљи(прикључница *TKorisnikdatagramprotocolПрикључница, pdata uintptr, величина uint16) {
	var ukupnoDužina = uint32(величина) + udpheaderВеличина

	var buffer_2 [4096]byte

	var msgbuffer = (*TKorisnikdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TKorisnikdatagramprotocolheader{}

	msg.izvorПортброј = прикључница.локалнаПортброј
	msg.odredišteПортброј = прикључница.удаљеноПортброј
	msg.dužina = Unsignedinteger16r(uint16(ukupnoDužina))

	msg.checksum = 0x0
	msg.Скупbuffer(msgbuffer)

	var dataBajtova [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(величина); i++ {
		buffer_2[int(udpheaderВеличина)+i] = dataBajtova[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Пошаљи(прикључница.удаљеноip, 0x11, data, ukupnoDužina)

}
func (isti *TKorisnikdatagramprotocolprovider) Bind(прикључница *TKorisnikdatagramprotocolПрикључница, handler *TKorisnikdatagramprotocolhandler) {
}
