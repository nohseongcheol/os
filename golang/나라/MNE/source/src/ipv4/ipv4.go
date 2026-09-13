package ipv4

import . "unsafe"
import . "util"
import . "конзола"
import . "žičanavezaOkvir"
import . "arp"

var ipКонзола TКонзола = TКонзола{}

type TИнтернетprotocolv4порукаbuffer struct {
	lenver		byte
	tos		byte
	ukupnoDužina	[2]byte

	ident			[2]byte
	parametriandoffset	[2]byte

	времеtolive	byte
	protocol	byte
	checksum	[2]byte

	izvoripaddress		[4]byte
	odredišteipaddress	[4]byte
}

var ipВеличина uint8 = (4 + 4 + 4 + 8)

type TИнтернетprotocolv4порука struct {
	headerDužina	uint8
	издање		uint8
	tos		uint8
	ukupnoDužina	uint16

	ident			uint16
	parametriandoffset	uint16

	времеtolive	uint8
	protocol	uint8
	checksum	uint16

	izvoripaddress		uint32
	odredišteipaddress	uint32
}

func (isti *TИнтернетprotocolv4порука) Init(buffer_2 TИнтернетprotocolv4порукаbuffer) {

	isti.издање = ((buffer_2.lenver & 0xF0) >> 4)
	isti.headerDužina = buffer_2.lenver & 0x0F
	isti.tos = buffer_2.tos
	isti.ukupnoDužina = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.ukupnoDužina))

	isti.ident = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.ident))
	isti.parametriandoffset = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.parametriandoffset))

	isti.времеtolive = buffer_2.времеtolive
	isti.protocol = buffer_2.protocol
	isti.checksum = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.checksum))

	isti.izvoripaddress = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.izvoripaddress))
	isti.odredišteipaddress = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.odredišteipaddress))

}
func (isti *TИнтернетprotocolv4порука) Скупbuffer(buffer_2 *TИнтернетprotocolv4порукаbuffer) {

	buffer_2.lenver = byte(((isti.издање & 0x0F) << 4) | (isti.headerDužina & 0x0F))
	buffer_2.tos = isti.tos
	buffer_2.ukupnoDužina = Unsignedinteger16toНиз(isti.ukupnoDužina)

	buffer_2.ident = Unsignedinteger16toНиз(isti.ident)
	buffer_2.parametriandoffset = Unsignedinteger16toНиз(isti.parametriandoffset)

	buffer_2.времеtolive = isti.времеtolive
	buffer_2.protocol = isti.protocol
	buffer_2.checksum = Unsignedinteger16toНиз(isti.checksum)

	buffer_2.izvoripaddress = Unsignedinteger32toНиз(isti.izvoripaddress)
	buffer_2.odredišteipaddress = Unsignedinteger32toНиз(isti.odredišteipaddress)

}

type IИнтернетprotocolhandler interface {
	Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8)
	Интернетprotocolreceivewhen(izvoripaddressМрежаbyteorder uint32, odredišteipaddressМрежаbyteorder uint32, dataPokazivač uintptr, величина uint32) bool
	Пошаљи(odredišteipaddressМрежаbyteorder uint32, pprotocol uint8, dataPokazivač uintptr, величина uint32)
	Providerget() *TИнтернетprotocolprovider
}

type TИнтернетprotocolhandler struct {
}

var ipŽičanavezaOkvirhandler IpŽičanavezaOkvirhandler = IpŽičanavezaOkvirhandler{}
var protocol uint8

func (isti *TИнтернетprotocolhandler) Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (isti *TИнтернетprotocolhandler) Интернетprotocolreceivewhen(izvoripaddressМрежаbyteorder uint32, odredišteipaddressМрежаbyteorder uint32, dataPokazivač uintptr, величина uint32) bool {
	ipКонзола.MŠtampaj(([]byte)("ipHandler:OnInternet"))
	return false
}
func (isti *TИнтернетprotocolhandler) Пошаљи(odredišteipaddressМрежаbyteorder uint32, pprotocol uint8, dataPokazivač uintptr, величина uint32) {

	ipprovider.Пошаљи(odredišteipaddressМрежаbyteorder, pprotocol, dataPokazivač, величина)
}
func (isti *TИнтернетprotocolhandler) Providerget() *TИнтернетprotocolprovider {
	return &ipprovider
}

type IpŽičanavezaOkvirhandler struct {
	TŽičanavezaOkvirhandler
}

var ipprovider TИнтернетprotocolprovider

func (isti *IpŽičanavezaOkvirhandler) ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, величина int) bool {
	ipКонзола.MŠtampaj(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.ŽičanavezaOkvirreceivewhen(dataPokazivač, uint32(величина))

}

func (isti *IpŽičanavezaOkvirhandler) Пошаљи(odredišteipaddressМрежаbyteorder uint64, dataPokazivač uintptr, величина uint32) {
	ipКонзола.MŠtampaj(([]byte)("ipefhandler:send\n"))
	var žičanavezaВрстаbe = Unsignedinteger16r(0x0800)
	isti.TŽičanavezaOkvirhandler.OkvirПошаљи(odredišteipaddressМрежаbyteorder, žičanavezaВрстаbe, dataPokazivač, величина)

}

var handler_2 [255]IИнтернетprotocolhandler

type TИнтернетprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaska	uint32
}

var efhandler IŽičanavezaOkvirhandler

func (isti *TИнтернетprotocolprovider) Init(pefprovider TŽičanavezaOkvirprovider, pefhandler IŽičanavezaOkvirhandler, arp Arpprovider, gatewayip uint32, subnetMaska uint32) {

	efhandler = pefhandler
	efhandler.Скупhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	isti.arpprovider = arp
	isti.Gatewayip = gatewayip
	isti.SubnetMaska = subnetMaska
	ipprovider = *isti
}
func (isti *TИнтернетprotocolprovider) ŽičanavezaOkvirreceivewhen(žičanavezaOkvirpayload uintptr, величина uint32) bool {
	if величина < uint32(ipВеличина) {
		return false
	}

	var buffer_2 *TИнтернетprotocolv4порукаbuffer = (*TИнтернетprotocolv4порукаbuffer)(Pointer(žičanavezaOkvirpayload))
	var интернетprotocolпорука TИнтернетprotocolv4порука
	интернетprotocolпорука.Init(*buffer_2)

	var reply bool = false

	if интернетprotocolпорука.odredišteipaddress == uint32(efhandler.Getipaddress()) {

		var dužina uint32 = uint32(интернетprotocolпорука.ukupnoDužina)
		if dužina > величина {
			dužina = величина
		}
		if handler_2[интернетprotocolпорука.protocol] != nil {
			reply = handler_2[интернетprotocolпорука.protocol].Интернетprotocolreceivewhen(интернетprotocolпорука.izvoripaddress, интернетprotocolпорука.odredišteipaddress, žičanavezaOkvirpayload+uintptr(4*интернетprotocolпорука.headerDužina), uint32(dužina-uint32(4*интернетprotocolпорука.headerDužina)))

		}
	}

	if reply {

		var temporary = интернетprotocolпорука.odredišteipaddress
		интернетprotocolпорука.odredišteipaddress = интернетprotocolпорука.izvoripaddress
		интернетprotocolпорука.izvoripaddress = temporary

		интернетprotocolпорука.времеtolive = 0x40
		интернетprotocolпорука.checksum = 0

		интернетprotocolпорука.Скупbuffer(buffer_2)
		интернетprotocolпорука.checksum = isti.Checksum((*([4096]uint16))(Pointer(žičanavezaOkvirpayload)), uint32(4*интернетprotocolпорука.headerDužina))

		интернетprotocolпорука.Скупbuffer(buffer_2)

	}

	ipКонзола.MŠtampaj(([]byte)("ipmessage"))
	ipКонзола.MUnsignedinteger32Štampaj(интернетprotocolпорука.izvoripaddress)
	ipКонзола.MŠtampaj(([]byte)(":"))
	ipКонзола.MUnsignedinteger32Štampaj(интернетprotocolпорука.odredišteipaddress)
	ipКонзола.MŠtampaj(([]byte)(":"))
	ipКонзола.MUnsignedinteger16Štampaj(uint16(интернетprotocolпорука.headerDužina))
	ipКонзола.MŠtampaj(([]byte)(":"))
	ipКонзола.MUnsignedinteger16Štampaj(uint16(интернетprotocolпорука.издање))
	ipКонзола.MŠtampaj(([]byte)(":"))
	ipКонзола.MUnsignedinteger16Štampaj(интернетprotocolпорука.ukupnoDužina)
	ipКонзола.MŠtampaj(([]byte)(":"))
	ipКонзола.MUnsignedinteger32Štampaj(uint32(efhandler.Getipaddress()))
	ipКонзола.MŠtampaj(([]byte)(":"))
	ipКонзола.MŠtampaj(([]byte)("\n"))

	return reply

}
func (isti *TИнтернетprotocolprovider) Пошаљи(odredišteipaddressМрежаbyteorder uint32, protocol uint8, dataPokazivač uintptr, величина uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TИнтернетprotocolv4порукаbuffer = (*TИнтернетprotocolv4порукаbuffer)(Pointer(&buffer1_2))
	var порука TИнтернетprotocolv4порука = TИнтернетprotocolv4порука{}
	порука.издање = 4
	порука.headerDužina = ipВеличина / 4
	порука.tos = 0
	порука.ukupnoDužina = Unsignedinteger16r(uint16(величина + uint32(ipВеличина)))

	порука.ident = 0x0100
	порука.parametriandoffset = 0x0040
	порука.времеtolive = 0x40
	порука.protocol = protocol

	порука.odredišteipaddress = odredišteipaddressМрежаbyteorder

	порука.izvoripaddress = uint32(efhandler.Getipaddress())

	порука.checksum = 0

	порука.Скупbuffer(buffer_2)
	порука.checksum = isti.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipВеличина))
	порука.Скупbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))

	for i := 0; i < int(величина); i++ {

		buffer1_2[i+int(ipВеличина)] = databuffer_2[i]
	}

	ipКонзола.MŠtampajxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(величина)+int(ipВеличина); i++ {
		ipКонзола.MHexadecimalŠtampaj(buffer1_2[i])
	}
	ipКонзола.MŠtampaj(([]byte)(":"))
	ipКонзола.MŠtampaj(([]byte)("]\n"))

	var следећеhopipaddressМрежаbyteorder uint32 = odredišteipaddressМрежаbyteorder
	if (odredišteipaddressМрежаbyteorder & isti.SubnetMaska) != (порука.izvoripaddress & isti.SubnetMaska) {
		следећеhopipaddressМрежаbyteorder = isti.Gatewayip
	}

	var пошаљиdataPokazivač = uintptr(Pointer(&buffer1_2))
	ipКонзола.MUnsignedinteger32Štampaj(следећеhopipaddressМрежаbyteorder)

	var žičanavezaВрстаbe = Unsignedinteger16r(0x0800)
	efhandler.OkvirПошаљи(isti.arpprovider.Resolve(следећеhopipaddressМрежаbyteorder), žičanavezaВрстаbe, пошаљиdataPokazivač, uint32(ipВеличина)+uint32(величина))

}
func (isti *TИнтернетprotocolprovider) Checksum(pdata *[4096]uint16, dužinaПримљеноBajtova uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBajtova [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (dužinaПримљеноBajtova % 2) != 0 {
		temporary += uint32(uint16(dataBajtova[dužinaПримљеноBajtova-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (isti *TИнтернетprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
