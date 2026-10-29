/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "етернетРамка"
import . "arp"

var ipconsole TConsole = TConsole{}

type TИнтернетprotocolv4Поракаbuffer struct {
	lenver		byte
	tos		byte
	вкупноДолжина	[2]byte

	ident			[2]byte
	атрибутиandoffset	[2]byte

	времеtolive	byte
	protocol	byte
	checksum	[2]byte

	изворipaddress		[4]byte
	одредиштеipaddress	[4]byte
}

var ipГолемина uint8 = (4 + 4 + 4 + 8)

type TИнтернетprotocolv4Порака struct {
	headerДолжина	uint8
	version		uint8
	tos		uint8
	вкупноДолжина	uint16

	ident			uint16
	атрибутиandoffset	uint16

	времеtolive	uint8
	protocol	uint8
	checksum	uint16

	изворipaddress		uint32
	одредиштеipaddress	uint32
}

func (само *TИнтернетprotocolv4Порака) Init(buffer_2 TИнтернетprotocolv4Поракаbuffer) {

	само.version = ((buffer_2.lenver & 0xF0) >> 4)
	само.headerДолжина = buffer_2.lenver & 0x0F
	само.tos = buffer_2.tos
	само.вкупноДолжина = Unsignedinteger16r(Построиtounsignedinteger16(buffer_2.вкупноДолжина))

	само.ident = Unsignedinteger16r(Построиtounsignedinteger16(buffer_2.ident))
	само.атрибутиandoffset = Unsignedinteger16r(Построиtounsignedinteger16(buffer_2.атрибутиandoffset))

	само.времеtolive = buffer_2.времеtolive
	само.protocol = buffer_2.protocol
	само.checksum = Unsignedinteger16r(Построиtounsignedinteger16(buffer_2.checksum))

	само.изворipaddress = Unsignedinteger32r(Построиtounsignedinteger32(buffer_2.изворipaddress))
	само.одредиштеipaddress = Unsignedinteger32r(Построиtounsignedinteger32(buffer_2.одредиштеipaddress))

}
func (само *TИнтернетprotocolv4Порака) Поставиbuffer(buffer_2 *TИнтернетprotocolv4Поракаbuffer) {

	buffer_2.lenver = byte(((само.version & 0x0F) << 4) | (само.headerДолжина & 0x0F))
	buffer_2.tos = само.tos
	buffer_2.вкупноДолжина = Unsignedinteger16toПострои(само.вкупноДолжина)

	buffer_2.ident = Unsignedinteger16toПострои(само.ident)
	buffer_2.атрибутиandoffset = Unsignedinteger16toПострои(само.атрибутиandoffset)

	buffer_2.времеtolive = само.времеtolive
	buffer_2.protocol = само.protocol
	buffer_2.checksum = Unsignedinteger16toПострои(само.checksum)

	buffer_2.изворipaddress = Unsignedinteger32toПострои(само.изворipaddress)
	buffer_2.одредиштеipaddress = Unsignedinteger32toПострои(само.одредиштеipaddress)

}

type IИнтернетprotocolhandler interface {
	Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8)
	Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, dataСтрелка uintptr, големина uint32) bool
	Испрати(одредиштеipaddressМрежаbyteorder uint32, pprotocol uint8, dataСтрелка uintptr, големина uint32)
	Providerget() *TИнтернетprotocolprovider
}

type TИнтернетprotocolhandler struct {
}

var ipЕтернетРамкаhandler IpЕтернетРамкаhandler = IpЕтернетРамкаhandler{}
var protocol uint8

func (само *TИнтернетprotocolhandler) Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (само *TИнтернетprotocolhandler) Интернетprotocolreceivewhen(изворipaddressМрежаbyteorder uint32, одредиштеipaddressМрежаbyteorder uint32, dataСтрелка uintptr, големина uint32) bool {
	ipconsole.MПечати(([]byte)("ipHandler:OnInternet"))
	return false
}
func (само *TИнтернетprotocolhandler) Испрати(одредиштеipaddressМрежаbyteorder uint32, pprotocol uint8, dataСтрелка uintptr, големина uint32) {

	ipprovider.Испрати(одредиштеipaddressМрежаbyteorder, pprotocol, dataСтрелка, големина)
}
func (само *TИнтернетprotocolhandler) Providerget() *TИнтернетprotocolprovider {
	return &ipprovider
}

type IpЕтернетРамкаhandler struct {
	TЕтернетРамкаhandler
}

var ipprovider TИнтернетprotocolprovider

func (само *IpЕтернетРамкаhandler) ЕтернетРамкаreceivewhen(dataСтрелка uintptr, големина int) bool {
	ipconsole.MПечати(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.ЕтернетРамкаreceivewhen(dataСтрелка, uint32(големина))

}

func (само *IpЕтернетРамкаhandler) Испрати(одредиштеipaddressМрежаbyteorder uint64, dataСтрелка uintptr, големина uint32) {
	ipconsole.MПечати(([]byte)("ipefhandler:send\n"))
	var етернетТипbe = Unsignedinteger16r(0x0800)
	само.TЕтернетРамкаhandler.РамкаИспрати(одредиштеipaddressМрежаbyteorder, етернетТипbe, dataСтрелка, големина)

}

var handler_2 [255]IИнтернетprotocolhandler

type TИнтернетprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetМаска	uint32
}

var efhandler IЕтернетРамкаhandler

func (само *TИнтернетprotocolprovider) Init(pefprovider TЕтернетРамкаprovider, pefhandler IЕтернетРамкаhandler, arp Arpprovider, gatewayip uint32, subnetМаска uint32) {

	efhandler = pefhandler
	efhandler.Поставиhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	само.arpprovider = arp
	само.Gatewayip = gatewayip
	само.SubnetМаска = subnetМаска
	ipprovider = *само
}
func (само *TИнтернетprotocolprovider) ЕтернетРамкаreceivewhen(етернетРамкаpayload uintptr, големина uint32) bool {
	if големина < uint32(ipГолемина) {
		return false
	}

	var buffer_2 *TИнтернетprotocolv4Поракаbuffer = (*TИнтернетprotocolv4Поракаbuffer)(Pointer(етернетРамкаpayload))
	var интернетprotocolПорака TИнтернетprotocolv4Порака
	интернетprotocolПорака.Init(*buffer_2)

	var reply bool = false

	if интернетprotocolПорака.одредиштеipaddress == uint32(efhandler.Getipaddress()) {

		var должина uint32 = uint32(интернетprotocolПорака.вкупноДолжина)
		if должина > големина {
			должина = големина
		}
		if handler_2[интернетprotocolПорака.protocol] != nil {
			reply = handler_2[интернетprotocolПорака.protocol].Интернетprotocolreceivewhen(интернетprotocolПорака.изворipaddress, интернетprotocolПорака.одредиштеipaddress, етернетРамкаpayload+uintptr(4*интернетprotocolПорака.headerДолжина), uint32(должина-uint32(4*интернетprotocolПорака.headerДолжина)))

		}
	}

	if reply {

		var temporary = интернетprotocolПорака.одредиштеipaddress
		интернетprotocolПорака.одредиштеipaddress = интернетprotocolПорака.изворipaddress
		интернетprotocolПорака.изворipaddress = temporary

		интернетprotocolПорака.времеtolive = 0x40
		интернетprotocolПорака.checksum = 0

		интернетprotocolПорака.Поставиbuffer(buffer_2)
		интернетprotocolПорака.checksum = само.Checksum((*([4096]uint16))(Pointer(етернетРамкаpayload)), uint32(4*интернетprotocolПорака.headerДолжина))

		интернетprotocolПорака.Поставиbuffer(buffer_2)

	}

	ipconsole.MПечати(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Печати(интернетprotocolПорака.изворipaddress)
	ipconsole.MПечати(([]byte)(":"))
	ipconsole.MUnsignedinteger32Печати(интернетprotocolПорака.одредиштеipaddress)
	ipconsole.MПечати(([]byte)(":"))
	ipconsole.MUnsignedinteger16Печати(uint16(интернетprotocolПорака.headerДолжина))
	ipconsole.MПечати(([]byte)(":"))
	ipconsole.MUnsignedinteger16Печати(uint16(интернетprotocolПорака.version))
	ipconsole.MПечати(([]byte)(":"))
	ipconsole.MUnsignedinteger16Печати(интернетprotocolПорака.вкупноДолжина)
	ipconsole.MПечати(([]byte)(":"))
	ipconsole.MUnsignedinteger32Печати(uint32(efhandler.Getipaddress()))
	ipconsole.MПечати(([]byte)(":"))
	ipconsole.MПечати(([]byte)("\n"))

	return reply

}
func (само *TИнтернетprotocolprovider) Испрати(одредиштеipaddressМрежаbyteorder uint32, protocol uint8, dataСтрелка uintptr, големина uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TИнтернетprotocolv4Поракаbuffer = (*TИнтернетprotocolv4Поракаbuffer)(Pointer(&buffer1_2))
	var порака TИнтернетprotocolv4Порака = TИнтернетprotocolv4Порака{}
	порака.version = 4
	порака.headerДолжина = ipГолемина / 4
	порака.tos = 0
	порака.вкупноДолжина = Unsignedinteger16r(uint16(големина + uint32(ipГолемина)))

	порака.ident = 0x0100
	порака.атрибутиandoffset = 0x0040
	порака.времеtolive = 0x40
	порака.protocol = protocol

	порака.одредиштеipaddress = одредиштеipaddressМрежаbyteorder

	порака.изворipaddress = uint32(efhandler.Getipaddress())

	порака.checksum = 0

	порака.Поставиbuffer(buffer_2)
	порака.checksum = само.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipГолемина))
	порака.Поставиbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataСтрелка))

	for i := 0; i < int(големина); i++ {

		buffer1_2[i+int(ipГолемина)] = databuffer_2[i]
	}

	ipconsole.MПечатиxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(големина)+int(ipГолемина); i++ {
		ipconsole.MHexadecimalПечати(buffer1_2[i])
	}
	ipconsole.MПечати(([]byte)(":"))
	ipconsole.MПечати(([]byte)("]\n"))

	var следнаhopipaddressМрежаbyteorder uint32 = одредиштеipaddressМрежаbyteorder
	if (одредиштеipaddressМрежаbyteorder & само.SubnetМаска) != (порака.изворipaddress & само.SubnetМаска) {
		следнаhopipaddressМрежаbyteorder = само.Gatewayip
	}

	var испратиdataСтрелка = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Печати(следнаhopipaddressМрежаbyteorder)

	var етернетТипbe = Unsignedinteger16r(0x0800)
	efhandler.РамкаИспрати(само.arpprovider.Resolve(следнаhopipaddressМрежаbyteorder), етернетТипbe, испратиdataСтрелка, uint32(ipГолемина)+uint32(големина))

}
func (само *TИнтернетprotocolprovider) Checksum(pdata *[4096]uint16, должинавобајти uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataбајти [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (должинавобајти % 2) != 0 {
		temporary += uint32(uint16(dataбајти[должинавобајти-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (само *TИнтернетprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
