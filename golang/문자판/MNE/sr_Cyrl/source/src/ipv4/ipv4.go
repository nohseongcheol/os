/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "конзола"
import . "жичанавезаОквир"
import . "arp"

var ipКонзола TКонзола = TКонзола{}

type TИнтернетprotocolv4порукаbuffer struct {
	lenver		byte
	tos		byte
	укупноДужина	[2]byte

	ident			[2]byte
	параметриandoffset	[2]byte

	времеtolive	byte
	protocol	byte
	checksum	[2]byte

	изворipaddress		[4]byte
	одредиштеipaddress	[4]byte
}

var ipВеличина uint8 = (4 + 4 + 4 + 8)

type TИнтернетprotocolv4порука struct {
	headerДужина	uint8
	издање		uint8
	tos		uint8
	укупноДужина	uint16

	ident			uint16
	параметриandoffset	uint16

	времеtolive	uint8
	protocol	uint8
	checksum	uint16

	изворipaddress		uint32
	одредиштеipaddress	uint32
}

func (исти *TИнтернетprotocolv4порука) Init(buffer_2 TИнтернетprotocolv4порукаbuffer) {

	исти.издање = ((buffer_2.lenver & 0xF0) >> 4)
	исти.headerДужина = buffer_2.lenver & 0x0F
	исти.tos = buffer_2.tos
	исти.укупноДужина = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.укупноДужина))

	исти.ident = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.ident))
	исти.параметриandoffset = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.параметриandoffset))

	исти.времеtolive = buffer_2.времеtolive
	исти.protocol = buffer_2.protocol
	исти.checksum = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.checksum))

	исти.изворipaddress = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.изворipaddress))
	исти.одредиштеipaddress = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.одредиштеipaddress))

}
func (исти *TИнтернетprotocolv4порука) Скупbuffer(buffer_2 *TИнтернетprotocolv4порукаbuffer) {

	buffer_2.lenver = byte(((исти.издање & 0x0F) << 4) | (исти.headerДужина & 0x0F))
	buffer_2.tos = исти.tos
	buffer_2.укупноДужина = Unsignedinteger16toНиз(исти.укупноДужина)

	buffer_2.ident = Unsignedinteger16toНиз(исти.ident)
	buffer_2.параметриandoffset = Unsignedinteger16toНиз(исти.параметриandoffset)

	buffer_2.времеtolive = исти.времеtolive
	buffer_2.protocol = исти.protocol
	buffer_2.checksum = Unsignedinteger16toНиз(исти.checksum)

	buffer_2.изворipaddress = Unsignedinteger32toНиз(исти.изворipaddress)
	buffer_2.одредиштеipaddress = Unsignedinteger32toНиз(исти.одредиштеipaddress)

}

type IИнтернетprotocolhandler interface {
	Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8)
	Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, dataПоказивач uintptr, величина uint32) bool
	Пошаљи(одредиштеipaddressМрежаbyteorder uint32, pprotocol uint8, dataПоказивач uintptr, величина uint32)
	Providerget() *TИнтернетprotocolprovider
}

type TИнтернетprotocolhandler struct {
}

var ipЖичанавезаОквирhandler IpЖичанавезаОквирhandler = IpЖичанавезаОквирhandler{}
var protocol uint8

func (исти *TИнтернетprotocolhandler) Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (исти *TИнтернетprotocolhandler) Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, dataПоказивач uintptr, величина uint32) bool {
	ipКонзола.MШтампај(([]byte)("ipHandler:OnInternet"))
	return false
}
func (исти *TИнтернетprotocolhandler) Пошаљи(одредиштеipaddressМрежаbyteorder uint32, pprotocol uint8, dataПоказивач uintptr, величина uint32) {

	ipprovider.Пошаљи(одредиштеipaddressМрежаbyteorder, pprotocol, dataПоказивач, величина)
}
func (исти *TИнтернетprotocolhandler) Providerget() *TИнтернетprotocolprovider {
	return &ipprovider
}

type IpЖичанавезаОквирhandler struct {
	TЖичанавезаОквирhandler
}

var ipprovider TИнтернетprotocolprovider

func (исти *IpЖичанавезаОквирhandler) ЖичанавезаОквирreceivewhen(dataПоказивач uintptr, величина int) bool {
	ipКонзола.MШтампај(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.ЖичанавезаОквирreceivewhen(dataПоказивач, uint32(величина))

}

func (исти *IpЖичанавезаОквирhandler) Пошаљи(одредиштеipaddressМрежаbyteorder uint64, dataПоказивач uintptr, величина uint32) {
	ipКонзола.MШтампај(([]byte)("ipefhandler:send\n"))
	var жичанавезаВрстаbe = Unsignedinteger16r(0x0800)
	исти.TЖичанавезаОквирhandler.ОквирПошаљи(одредиштеipaddressМрежаbyteorder, жичанавезаВрстаbe, dataПоказивач, величина)

}

var handler_2 [255]IИнтернетprotocolhandler

type TИнтернетprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetМаска	uint32
}

var efhandler IЖичанавезаОквирhandler

func (исти *TИнтернетprotocolprovider) Init(pefprovider TЖичанавезаОквирprovider, pefhandler IЖичанавезаОквирhandler, arp Arpprovider, gatewayip uint32, subnetМаска uint32) {

	efhandler = pefhandler
	efhandler.Скупhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	исти.arpprovider = arp
	исти.Gatewayip = gatewayip
	исти.SubnetМаска = subnetМаска
	ipprovider = *исти
}
func (исти *TИнтернетprotocolprovider) ЖичанавезаОквирreceivewhen(жичанавезаОквирpayload uintptr, величина uint32) bool {
	if величина < uint32(ipВеличина) {
		return false
	}

	var buffer_2 *TИнтернетprotocolv4порукаbuffer = (*TИнтернетprotocolv4порукаbuffer)(Pointer(жичанавезаОквирpayload))
	var интернетprotocolпорука TИнтернетprotocolv4порука
	интернетprotocolпорука.Init(*buffer_2)

	var reply bool = false

	if интернетprotocolпорука.одредиштеipaddress == uint32(efhandler.Getipaddress()) {

		var дужина uint32 = uint32(интернетprotocolпорука.укупноДужина)
		if дужина > величина {
			дужина = величина
		}
		if handler_2[интернетprotocolпорука.protocol] != nil {
			reply = handler_2[интернетprotocolпорука.protocol].Интернетprotocolreceivewhen(интернетprotocolпорука.изворipaddress, интернетprotocolпорука.одредиштеipaddress, жичанавезаОквирpayload+uintptr(4*интернетprotocolпорука.headerДужина), uint32(дужина-uint32(4*интернетprotocolпорука.headerДужина)))

		}
	}

	if reply {

		var temporary = интернетprotocolпорука.одредиштеipaddress
		интернетprotocolпорука.одредиштеipaddress = интернетprotocolпорука.изворipaddress
		интернетprotocolпорука.изворipaddress = temporary

		интернетprotocolпорука.времеtolive = 0x40
		интернетprotocolпорука.checksum = 0

		интернетprotocolпорука.Скупbuffer(buffer_2)
		интернетprotocolпорука.checksum = исти.Checksum((*([4096]uint16))(Pointer(жичанавезаОквирpayload)), uint32(4*интернетprotocolпорука.headerДужина))

		интернетprotocolпорука.Скупbuffer(buffer_2)

	}

	ipКонзола.MШтампај(([]byte)("ipmessage"))
	ipКонзола.MUnsignedinteger32Штампај(интернетprotocolпорука.изворipaddress)
	ipКонзола.MШтампај(([]byte)(":"))
	ipКонзола.MUnsignedinteger32Штампај(интернетprotocolпорука.одредиштеipaddress)
	ipКонзола.MШтампај(([]byte)(":"))
	ipКонзола.MUnsignedinteger16Штампај(uint16(интернетprotocolпорука.headerДужина))
	ipКонзола.MШтампај(([]byte)(":"))
	ipКонзола.MUnsignedinteger16Штампај(uint16(интернетprotocolпорука.издање))
	ipКонзола.MШтампај(([]byte)(":"))
	ipКонзола.MUnsignedinteger16Штампај(интернетprotocolпорука.укупноДужина)
	ipКонзола.MШтампај(([]byte)(":"))
	ipКонзола.MUnsignedinteger32Штампај(uint32(efhandler.Getipaddress()))
	ipКонзола.MШтампај(([]byte)(":"))
	ipКонзола.MШтампај(([]byte)("\n"))

	return reply

}
func (исти *TИнтернетprotocolprovider) Пошаљи(одредиштеipaddressМрежаbyteorder uint32, protocol uint8, dataПоказивач uintptr, величина uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TИнтернетprotocolv4порукаbuffer = (*TИнтернетprotocolv4порукаbuffer)(Pointer(&buffer1_2))
	var порука TИнтернетprotocolv4порука = TИнтернетprotocolv4порука{}
	порука.издање = 4
	порука.headerДужина = ipВеличина / 4
	порука.tos = 0
	порука.укупноДужина = Unsignedinteger16r(uint16(величина + uint32(ipВеличина)))

	порука.ident = 0x0100
	порука.параметриandoffset = 0x0040
	порука.времеtolive = 0x40
	порука.protocol = protocol

	порука.одредиштеipaddress = одредиштеipaddressМрежаbyteorder

	порука.изворipaddress = uint32(efhandler.Getipaddress())

	порука.checksum = 0

	порука.Скупbuffer(buffer_2)
	порука.checksum = исти.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipВеличина))
	порука.Скупbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataПоказивач))

	for i := 0; i < int(величина); i++ {

		buffer1_2[i+int(ipВеличина)] = databuffer_2[i]
	}

	ipКонзола.MШтампајxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(величина)+int(ipВеличина); i++ {
		ipКонзола.MHexadecimalШтампај(buffer1_2[i])
	}
	ipКонзола.MШтампај(([]byte)(":"))
	ipКонзола.MШтампај(([]byte)("]\n"))

	var следећеhopipaddressМрежаbyteorder uint32 = одредиштеipaddressМрежаbyteorder
	if (одредиштеipaddressМрежаbyteorder & исти.SubnetМаска) != (порука.изворipaddress & исти.SubnetМаска) {
		следећеhopipaddressМрежаbyteorder = исти.Gatewayip
	}

	var пошаљиdataПоказивач = uintptr(Pointer(&buffer1_2))
	ipКонзола.MUnsignedinteger32Штампај(следећеhopipaddressМрежаbyteorder)

	var жичанавезаВрстаbe = Unsignedinteger16r(0x0800)
	efhandler.ОквирПошаљи(исти.arpprovider.Resolve(следећеhopipaddressМрежаbyteorder), жичанавезаВрстаbe, пошаљиdataПоказивач, uint32(ipВеличина)+uint32(величина))

}
func (исти *TИнтернетprotocolprovider) Checksum(pdata *[4096]uint16, дужинаПримљеноБајтова uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataБајтова [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (дужинаПримљеноБајтова % 2) != 0 {
		temporary += uint32(uint16(dataБајтова[дужинаПримљеноБајтова-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (исти *TИнтернетprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
