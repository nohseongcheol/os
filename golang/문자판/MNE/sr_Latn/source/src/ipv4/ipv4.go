package ipv4

import . "unsafe"
import . "util"
import . "konzola"
import . "žičanavezaOkvir"
import . "arp"

var ipKonzola TKonzola = TKonzola{}

type TInternetprotocolv4porukabuffer struct {
	lenver		byte
	tos		byte
	ukupnoDužina	[2]byte

	ident			[2]byte
	parametriandoffset	[2]byte

	vremetolive	byte
	protocol	byte
	checksum	[2]byte

	izvoripaddress		[4]byte
	odredišteipaddress	[4]byte
}

var ipVeličina uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4poruka struct {
	headerDužina	uint8
	izdanje		uint8
	tos		uint8
	ukupnoDužina	uint16

	ident			uint16
	parametriandoffset	uint16

	vremetolive	uint8
	protocol	uint8
	checksum	uint16

	izvoripaddress		uint32
	odredišteipaddress	uint32
}

func (isti *TInternetprotocolv4poruka) Init(buffer_2 TInternetprotocolv4porukabuffer) {

	isti.izdanje = ((buffer_2.lenver & 0xF0) >> 4)
	isti.headerDužina = buffer_2.lenver & 0x0F
	isti.tos = buffer_2.tos
	isti.ukupnoDužina = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.ukupnoDužina))

	isti.ident = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.ident))
	isti.parametriandoffset = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.parametriandoffset))

	isti.vremetolive = buffer_2.vremetolive
	isti.protocol = buffer_2.protocol
	isti.checksum = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.checksum))

	isti.izvoripaddress = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.izvoripaddress))
	isti.odredišteipaddress = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.odredišteipaddress))

}
func (isti *TInternetprotocolv4poruka) Skupbuffer(buffer_2 *TInternetprotocolv4porukabuffer) {

	buffer_2.lenver = byte(((isti.izdanje & 0x0F) << 4) | (isti.headerDužina & 0x0F))
	buffer_2.tos = isti.tos
	buffer_2.ukupnoDužina = Unsignedinteger16toNiz(isti.ukupnoDužina)

	buffer_2.ident = Unsignedinteger16toNiz(isti.ident)
	buffer_2.parametriandoffset = Unsignedinteger16toNiz(isti.parametriandoffset)

	buffer_2.vremetolive = isti.vremetolive
	buffer_2.protocol = isti.protocol
	buffer_2.checksum = Unsignedinteger16toNiz(isti.checksum)

	buffer_2.izvoripaddress = Unsignedinteger32toNiz(isti.izvoripaddress)
	buffer_2.odredišteipaddress = Unsignedinteger32toNiz(isti.odredišteipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, dataPokazivač uintptr, veličina uint32) bool
	Pošalji(odredišteipaddressMrežabyteorder uint32, pprotocol uint8, dataPokazivač uintptr, veličina uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipŽičanavezaOkvirhandler IpŽičanavezaOkvirhandler = IpŽičanavezaOkvirhandler{}
var protocol uint8

func (isti *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (isti *TInternetprotocolhandler) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, dataPokazivač uintptr, veličina uint32) bool {
	ipKonzola.MŠtampaj(([]byte)("ipHandler:OnInternet"))
	return false
}
func (isti *TInternetprotocolhandler) Pošalji(odredišteipaddressMrežabyteorder uint32, pprotocol uint8, dataPokazivač uintptr, veličina uint32) {

	ipprovider.Pošalji(odredišteipaddressMrežabyteorder, pprotocol, dataPokazivač, veličina)
}
func (isti *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpŽičanavezaOkvirhandler struct {
	TŽičanavezaOkvirhandler
}

var ipprovider TInternetprotocolprovider

func (isti *IpŽičanavezaOkvirhandler) ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, veličina int) bool {
	ipKonzola.MŠtampaj(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.ŽičanavezaOkvirreceivewhen(dataPokazivač, uint32(veličina))

}

func (isti *IpŽičanavezaOkvirhandler) Pošalji(odredišteipaddressMrežabyteorder uint64, dataPokazivač uintptr, veličina uint32) {
	ipKonzola.MŠtampaj(([]byte)("ipefhandler:send\n"))
	var žičanavezaVrstabe = Unsignedinteger16r(0x0800)
	isti.TŽičanavezaOkvirhandler.OkvirPošalji(odredišteipaddressMrežabyteorder, žičanavezaVrstabe, dataPokazivač, veličina)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaska	uint32
}

var efhandler IŽičanavezaOkvirhandler

func (isti *TInternetprotocolprovider) Init(pefprovider TŽičanavezaOkvirprovider, pefhandler IŽičanavezaOkvirhandler, arp Arpprovider, gatewayip uint32, subnetMaska uint32) {

	efhandler = pefhandler
	efhandler.Skuphandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	isti.arpprovider = arp
	isti.Gatewayip = gatewayip
	isti.SubnetMaska = subnetMaska
	ipprovider = *isti
}
func (isti *TInternetprotocolprovider) ŽičanavezaOkvirreceivewhen(žičanavezaOkvirpayload uintptr, veličina uint32) bool {
	if veličina < uint32(ipVeličina) {
		return false
	}

	var buffer_2 *TInternetprotocolv4porukabuffer = (*TInternetprotocolv4porukabuffer)(Pointer(žičanavezaOkvirpayload))
	var internetprotocolporuka TInternetprotocolv4poruka
	internetprotocolporuka.Init(*buffer_2)

	var reply bool = false

	if internetprotocolporuka.odredišteipaddress == uint32(efhandler.Getipaddress()) {

		var dužina uint32 = uint32(internetprotocolporuka.ukupnoDužina)
		if dužina > veličina {
			dužina = veličina
		}
		if handler_2[internetprotocolporuka.protocol] != nil {
			reply = handler_2[internetprotocolporuka.protocol].Internetprotocolreceivewhen(internetprotocolporuka.izvoripaddress, internetprotocolporuka.odredišteipaddress, žičanavezaOkvirpayload+uintptr(4*internetprotocolporuka.headerDužina), uint32(dužina-uint32(4*internetprotocolporuka.headerDužina)))

		}
	}

	if reply {

		var temporary = internetprotocolporuka.odredišteipaddress
		internetprotocolporuka.odredišteipaddress = internetprotocolporuka.izvoripaddress
		internetprotocolporuka.izvoripaddress = temporary

		internetprotocolporuka.vremetolive = 0x40
		internetprotocolporuka.checksum = 0

		internetprotocolporuka.Skupbuffer(buffer_2)
		internetprotocolporuka.checksum = isti.Checksum((*([4096]uint16))(Pointer(žičanavezaOkvirpayload)), uint32(4*internetprotocolporuka.headerDužina))

		internetprotocolporuka.Skupbuffer(buffer_2)

	}

	ipKonzola.MŠtampaj(([]byte)("ipmessage"))
	ipKonzola.MUnsignedinteger32Štampaj(internetprotocolporuka.izvoripaddress)
	ipKonzola.MŠtampaj(([]byte)(":"))
	ipKonzola.MUnsignedinteger32Štampaj(internetprotocolporuka.odredišteipaddress)
	ipKonzola.MŠtampaj(([]byte)(":"))
	ipKonzola.MUnsignedinteger16Štampaj(uint16(internetprotocolporuka.headerDužina))
	ipKonzola.MŠtampaj(([]byte)(":"))
	ipKonzola.MUnsignedinteger16Štampaj(uint16(internetprotocolporuka.izdanje))
	ipKonzola.MŠtampaj(([]byte)(":"))
	ipKonzola.MUnsignedinteger16Štampaj(internetprotocolporuka.ukupnoDužina)
	ipKonzola.MŠtampaj(([]byte)(":"))
	ipKonzola.MUnsignedinteger32Štampaj(uint32(efhandler.Getipaddress()))
	ipKonzola.MŠtampaj(([]byte)(":"))
	ipKonzola.MŠtampaj(([]byte)("\n"))

	return reply

}
func (isti *TInternetprotocolprovider) Pošalji(odredišteipaddressMrežabyteorder uint32, protocol uint8, dataPokazivač uintptr, veličina uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4porukabuffer = (*TInternetprotocolv4porukabuffer)(Pointer(&buffer1_2))
	var poruka TInternetprotocolv4poruka = TInternetprotocolv4poruka{}
	poruka.izdanje = 4
	poruka.headerDužina = ipVeličina / 4
	poruka.tos = 0
	poruka.ukupnoDužina = Unsignedinteger16r(uint16(veličina + uint32(ipVeličina)))

	poruka.ident = 0x0100
	poruka.parametriandoffset = 0x0040
	poruka.vremetolive = 0x40
	poruka.protocol = protocol

	poruka.odredišteipaddress = odredišteipaddressMrežabyteorder

	poruka.izvoripaddress = uint32(efhandler.Getipaddress())

	poruka.checksum = 0

	poruka.Skupbuffer(buffer_2)
	poruka.checksum = isti.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipVeličina))
	poruka.Skupbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))

	for i := 0; i < int(veličina); i++ {

		buffer1_2[i+int(ipVeličina)] = databuffer_2[i]
	}

	ipKonzola.MŠtampajxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(veličina)+int(ipVeličina); i++ {
		ipKonzola.MHexadecimalŠtampaj(buffer1_2[i])
	}
	ipKonzola.MŠtampaj(([]byte)(":"))
	ipKonzola.MŠtampaj(([]byte)("]\n"))

	var sledećehopipaddressMrežabyteorder uint32 = odredišteipaddressMrežabyteorder
	if (odredišteipaddressMrežabyteorder & isti.SubnetMaska) != (poruka.izvoripaddress & isti.SubnetMaska) {
		sledećehopipaddressMrežabyteorder = isti.Gatewayip
	}

	var pošaljidataPokazivač = uintptr(Pointer(&buffer1_2))
	ipKonzola.MUnsignedinteger32Štampaj(sledećehopipaddressMrežabyteorder)

	var žičanavezaVrstabe = Unsignedinteger16r(0x0800)
	efhandler.OkvirPošalji(isti.arpprovider.Resolve(sledećehopipaddressMrežabyteorder), žičanavezaVrstabe, pošaljidataPokazivač, uint32(ipVeličina)+uint32(veličina))

}
func (isti *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, dužinaPrimljenoBajtova uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBajtova [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (dužinaPrimljenoBajtova % 2) != 0 {
		temporary += uint32(uint16(dataBajtova[dužinaPrimljenoBajtova-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (isti *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
