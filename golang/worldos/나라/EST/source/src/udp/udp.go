/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "mälumanager"
import . "ipv4"

var udpconsole = TConsole{}

type TKasutajadatagramprotocolheaderbuffer struct {
	aLLIKASportArv	[2]byte
	sihtfailportArv	[2]byte

	kestus		[2]byte
	checksum	[2]byte
}

var udpheaderSuurus uint32 = 8

type TKasutajadatagramprotocolheader struct {
	aLLIKASportArv	uint16
	sihtfailportArv	uint16

	kestus		uint16
	checksum	uint16
}

func (ise *TKasutajadatagramprotocolheader) Init(buffer_2 *TKasutajadatagramprotocolheaderbuffer) {
	ise.aLLIKASportArv = Massiivtounsignedinteger16(buffer_2.aLLIKASportArv)
	ise.sihtfailportArv = Massiivtounsignedinteger16(buffer_2.sihtfailportArv)

	ise.kestus = Massiivtounsignedinteger16(buffer_2.kestus)
	ise.checksum = Massiivtounsignedinteger16(buffer_2.checksum)
}
func (ise *TKasutajadatagramprotocolheader) Määrabuffer(buffer_2 *TKasutajadatagramprotocolheaderbuffer) {

	buffer_2.aLLIKASportArv = Unsignedinteger16toMassiiv(ise.aLLIKASportArv)
	buffer_2.sihtfailportArv = Unsignedinteger16toMassiiv(ise.sihtfailportArv)

	buffer_2.kestus = Unsignedinteger16toMassiiv(ise.kestus)
	buffer_2.checksum = Unsignedinteger16toMassiiv(ise.checksum)

}

type IKasutajadatagramprotocolhandler interface {
	HandleKasutajadatagramprotocolTeade(sokkel *TKasutajadatagramprotocolSokkel, data uintptr, suurus uint16)
}

type TKasutajadatagramprotocolhandler struct {
}

func (ise *TKasutajadatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (ise *TKasutajadatagramprotocolhandler) HandleKasutajadatagramprotocolTeade(sokkel *TKasutajadatagramprotocolSokkel, data uintptr, suurus uint16) {
}

type IKasutajadatagramprotocolSokkel interface {
	HandleKasutajadatagramprotocolTeade(data uintptr, suurus uint16)
}
type TKasutajadatagramprotocolSokkel struct {
	võrgusportArv	uint16
	võrgusip	uint32
	kohalikportArv	uint16
	kohalikip	uint32

	listening	bool
}

var udpprovider TKasutajadatagramprotocolprovider
var udphandler IKasutajadatagramprotocolhandler

func (ise *TKasutajadatagramprotocolSokkel) Testi() {
}
func (ise *TKasutajadatagramprotocolSokkel) Init(pudpprovider TKasutajadatagramprotocolprovider, pudphandler IKasutajadatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	ise.listening = false
}
func (ise *TKasutajadatagramprotocolSokkel) HandleKasutajadatagramprotocolTeade(data uintptr, suurus uint16) {
	if udphandler != nil {
		udphandler.HandleKasutajadatagramprotocolTeade(ise, data, suurus)
	}
}
func (ise *TKasutajadatagramprotocolSokkel) Saada(pdata []byte, suurus uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(suurus); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Saada(ise, data, suurus)
}
func (ise *TKasutajadatagramprotocolSokkel) Katkestaühendus() {
	udpprovider.Katkestaühendus(ise)
}

type TKasutajadatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TKasutajadatagramprotocolSokkel
var arvsockets int
var vabaport uint16

func (ise *TKasutajadatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	arvsockets = 0
	vabaport = 1024
}
func (ise *TKasutajadatagramprotocolprovider) Internetprotocolreceivewhen(aLLIKASipaddressVõrkbyteorder uint32, sihtfailipaddressVõrkbyteorder uint32, internetprotocolpayload uintptr, suurus uint32) bool {
	if suurus < udpheaderSuurus {
		return false
	}

	var buffer_2 *TKasutajadatagramprotocolheaderbuffer = (*TKasutajadatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TKasutajadatagramprotocolheader
	msg.Init(buffer_2)

	var sokkel *TKasutajadatagramprotocolSokkel = nil

	for i := 0; i < arvsockets && sokkel == nil; i++ {
		if sockets[i].kohalikportArv == msg.sihtfailportArv && sockets[i].kohalikip == sihtfailipaddressVõrkbyteorder && sockets[i].listening == true {
			sokkel = &sockets[i]
			sokkel.listening = false
			sokkel.võrgusportArv = msg.aLLIKASportArv
			sokkel.võrgusip = aLLIKASipaddressVõrkbyteorder
		} else if sockets[i].kohalikportArv == msg.sihtfailportArv && sockets[i].kohalikip == sihtfailipaddressVõrkbyteorder && sockets[i].võrgusportArv == msg.aLLIKASportArv && sockets[i].võrgusip == aLLIKASipaddressVõrkbyteorder {
			sokkel = &sockets[i]

		}
	}

	msg.Määrabuffer(buffer_2)
	if sokkel != nil {
		sokkel.HandleKasutajadatagramprotocolTeade(internetprotocolpayload+uintptr(udpheaderSuurus), uint16(suurus-udpheaderSuurus))
	}

	return false
}

func (ise *TKasutajadatagramprotocolprovider) Ühendu(ip uint32, port uint16) *TKasutajadatagramprotocolSokkel {
	var mälumanager = &TMälumanager{}
	var sokkel = (*TKasutajadatagramprotocolSokkel)(mälumanager.Malloc(50))

	if sokkel != nil {

		sokkel.Init(*ise, nil)
		sokkel.võrgusportArv = port
		sokkel.võrgusip = ip
		sokkel.kohalikportArv = vabaport
		vabaport++
		sokkel.kohalikip = uint32((*iphandler.Providerget()).Getipaddress())

		sokkel.võrgusportArv = Unsignedinteger16r(sokkel.võrgusportArv)
		sokkel.kohalikportArv = Unsignedinteger16r(sokkel.kohalikportArv)

		sockets[arvsockets] = *sokkel
		arvsockets++

	}
	return sokkel

}
func (ise *TKasutajadatagramprotocolprovider) Listen(port uint16) *TKasutajadatagramprotocolSokkel {
	var sokkel = &TKasutajadatagramprotocolSokkel{}
	sokkel = nil
	if sokkel != nil {
		sokkel.Init(*ise, nil)
		sokkel.listening = true
		sokkel.kohalikportArv = port
		sokkel.kohalikip = uint32((*iphandler.Providerget()).Getipaddress())

		sokkel.kohalikportArv = Unsignedinteger16r(sokkel.kohalikportArv)
	}
	return sokkel
}
func (ise *TKasutajadatagramprotocolprovider) Katkestaühendus(sokkel *TKasutajadatagramprotocolSokkel) {
	for i := 0; i < arvsockets && sokkel == nil; i++ {
		if sockets[i] == *sokkel {
			arvsockets--
			sockets[i] = sockets[arvsockets]
			break
		}
	}
}
func (ise *TKasutajadatagramprotocolprovider) Saada(sokkel *TKasutajadatagramprotocolSokkel, pdata uintptr, suurus uint16) {
	var kokkuKestus = uint32(suurus) + udpheaderSuurus

	var buffer_2 [4096]byte

	var msgbuffer = (*TKasutajadatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TKasutajadatagramprotocolheader{}

	msg.aLLIKASportArv = sokkel.kohalikportArv
	msg.sihtfailportArv = sokkel.võrgusportArv
	msg.kestus = Unsignedinteger16r(uint16(kokkuKestus))

	msg.checksum = 0x0
	msg.Määrabuffer(msgbuffer)

	var databaiti [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(suurus); i++ {
		buffer_2[int(udpheaderSuurus)+i] = databaiti[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Saada(sokkel.võrgusip, 0x11, data, kokkuKestus)

}
func (ise *TKasutajadatagramprotocolprovider) Bind(sokkel *TKasutajadatagramprotocolSokkel, handler *TKasutajadatagramprotocolhandler) {
}
