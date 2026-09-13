package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetRamme"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternettprotocolv4Meldingbuffer struct {
	lenver		byte
	tos		byte
	totaltLengde	[2]byte

	ident		[2]byte
	flaggogAvstand	[2]byte

	tidtolive	byte
	protocol	byte
	checksum	[2]byte

	kildeipaddress	[4]byte
	målipaddress	[4]byte
}

var ipStørrelse uint8 = (4 + 4 + 4 + 8)

type TInternettprotocolv4Melding struct {
	topptekstLengde	uint8
	versjon		uint8
	tos		uint8
	totaltLengde	uint16

	ident		uint16
	flaggogAvstand	uint16

	tidtolive	uint8
	protocol	uint8
	checksum	uint16

	kildeipaddress	uint32
	målipaddress	uint32
}

func (selv *TInternettprotocolv4Melding) Init(buffer_2 TInternettprotocolv4Meldingbuffer) {

	selv.versjon = ((buffer_2.lenver & 0xF0) >> 4)
	selv.topptekstLengde = buffer_2.lenver & 0x0F
	selv.tos = buffer_2.tos
	selv.totaltLengde = Unsignedinteger16r(Tabelltounsignedinteger16(buffer_2.totaltLengde))

	selv.ident = Unsignedinteger16r(Tabelltounsignedinteger16(buffer_2.ident))
	selv.flaggogAvstand = Unsignedinteger16r(Tabelltounsignedinteger16(buffer_2.flaggogAvstand))

	selv.tidtolive = buffer_2.tidtolive
	selv.protocol = buffer_2.protocol
	selv.checksum = Unsignedinteger16r(Tabelltounsignedinteger16(buffer_2.checksum))

	selv.kildeipaddress = Unsignedinteger32r(Tabelltounsignedinteger32(buffer_2.kildeipaddress))
	selv.målipaddress = Unsignedinteger32r(Tabelltounsignedinteger32(buffer_2.målipaddress))

}
func (selv *TInternettprotocolv4Melding) Settbuffer(buffer_2 *TInternettprotocolv4Meldingbuffer) {

	buffer_2.lenver = byte(((selv.versjon & 0x0F) << 4) | (selv.topptekstLengde & 0x0F))
	buffer_2.tos = selv.tos
	buffer_2.totaltLengde = Unsignedinteger16toTabell(selv.totaltLengde)

	buffer_2.ident = Unsignedinteger16toTabell(selv.ident)
	buffer_2.flaggogAvstand = Unsignedinteger16toTabell(selv.flaggogAvstand)

	buffer_2.tidtolive = selv.tidtolive
	buffer_2.protocol = selv.protocol
	buffer_2.checksum = Unsignedinteger16toTabell(selv.checksum)

	buffer_2.kildeipaddress = Unsignedinteger32toTabell(selv.kildeipaddress)
	buffer_2.målipaddress = Unsignedinteger32toTabell(selv.målipaddress)

}

type IInternettprotocolhandler interface {
	Init(backend TInternettprotocolprovider, pihandler IInternettprotocolhandler, pprotocol uint8)
	Internettprotocolreceivewhen(kildeipaddressNettverkbyteorder uint32, målipaddressNettverkbyteorder uint32, dataPeker uintptr, størrelse uint32) bool
	Send(målipaddressNettverkbyteorder uint32, pprotocol uint8, dataPeker uintptr, størrelse uint32)
	Providerget() *TInternettprotocolprovider
}

type TInternettprotocolhandler struct {
}

var ipethernetRammehandler IpethernetRammehandler = IpethernetRammehandler{}
var protocol uint8

func (selv *TInternettprotocolhandler) Init(backend TInternettprotocolprovider, pihandler IInternettprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (selv *TInternettprotocolhandler) Internettprotocolreceivewhen(kildeipaddressNettverkbyteorder uint32, målipaddressNettverkbyteorder uint32, dataPeker uintptr, størrelse uint32) bool {
	ipconsole.MSkrivut(([]byte)("ipHandler:OnInternet"))
	return false
}
func (selv *TInternettprotocolhandler) Send(målipaddressNettverkbyteorder uint32, pprotocol uint8, dataPeker uintptr, størrelse uint32) {

	ipprovider.Send(målipaddressNettverkbyteorder, pprotocol, dataPeker, størrelse)
}
func (selv *TInternettprotocolhandler) Providerget() *TInternettprotocolprovider {
	return &ipprovider
}

type IpethernetRammehandler struct {
	TEthernetRammehandler
}

var ipprovider TInternettprotocolprovider

func (selv *IpethernetRammehandler) EthernetRammereceivewhen(dataPeker uintptr, størrelse int) bool {
	ipconsole.MSkrivut(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetRammereceivewhen(dataPeker, uint32(størrelse))

}

func (selv *IpethernetRammehandler) Send(målipaddressNettverkbyteorder uint64, dataPeker uintptr, størrelse uint32) {
	ipconsole.MSkrivut(([]byte)("ipefhandler:send\n"))
	var ethernetFiltypebe = Unsignedinteger16r(0x0800)
	selv.TEthernetRammehandler.Rammesend(målipaddressNettverkbyteorder, ethernetFiltypebe, dataPeker, størrelse)

}

var handler_2 [255]IInternettprotocolhandler

type TInternettprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaske	uint32
}

var efhandler IEthernetRammehandler

func (selv *TInternettprotocolprovider) Init(pefprovider TEthernetRammeprovider, pefhandler IEthernetRammehandler, arp Arpprovider, gatewayip uint32, subnetMaske uint32) {

	efhandler = pefhandler
	efhandler.Setthandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	selv.arpprovider = arp
	selv.Gatewayip = gatewayip
	selv.SubnetMaske = subnetMaske
	ipprovider = *selv
}
func (selv *TInternettprotocolprovider) EthernetRammereceivewhen(ethernetRammepayload uintptr, størrelse uint32) bool {
	if størrelse < uint32(ipStørrelse) {
		return false
	}

	var buffer_2 *TInternettprotocolv4Meldingbuffer = (*TInternettprotocolv4Meldingbuffer)(Pointer(ethernetRammepayload))
	var internettprotocolMelding TInternettprotocolv4Melding
	internettprotocolMelding.Init(*buffer_2)

	var reply bool = false

	if internettprotocolMelding.målipaddress == uint32(efhandler.Getipaddress()) {

		var lengde uint32 = uint32(internettprotocolMelding.totaltLengde)
		if lengde > størrelse {
			lengde = størrelse
		}
		if handler_2[internettprotocolMelding.protocol] != nil {
			reply = handler_2[internettprotocolMelding.protocol].Internettprotocolreceivewhen(internettprotocolMelding.kildeipaddress, internettprotocolMelding.målipaddress, ethernetRammepayload+uintptr(4*internettprotocolMelding.topptekstLengde), uint32(lengde-uint32(4*internettprotocolMelding.topptekstLengde)))

		}
	}

	if reply {

		var temporary = internettprotocolMelding.målipaddress
		internettprotocolMelding.målipaddress = internettprotocolMelding.kildeipaddress
		internettprotocolMelding.kildeipaddress = temporary

		internettprotocolMelding.tidtolive = 0x40
		internettprotocolMelding.checksum = 0

		internettprotocolMelding.Settbuffer(buffer_2)
		internettprotocolMelding.checksum = selv.Checksum((*([4096]uint16))(Pointer(ethernetRammepayload)), uint32(4*internettprotocolMelding.topptekstLengde))

		internettprotocolMelding.Settbuffer(buffer_2)

	}

	ipconsole.MSkrivut(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Skrivut(internettprotocolMelding.kildeipaddress)
	ipconsole.MSkrivut(([]byte)(":"))
	ipconsole.MUnsignedinteger32Skrivut(internettprotocolMelding.målipaddress)
	ipconsole.MSkrivut(([]byte)(":"))
	ipconsole.MUnsignedinteger16Skrivut(uint16(internettprotocolMelding.topptekstLengde))
	ipconsole.MSkrivut(([]byte)(":"))
	ipconsole.MUnsignedinteger16Skrivut(uint16(internettprotocolMelding.versjon))
	ipconsole.MSkrivut(([]byte)(":"))
	ipconsole.MUnsignedinteger16Skrivut(internettprotocolMelding.totaltLengde)
	ipconsole.MSkrivut(([]byte)(":"))
	ipconsole.MUnsignedinteger32Skrivut(uint32(efhandler.Getipaddress()))
	ipconsole.MSkrivut(([]byte)(":"))
	ipconsole.MSkrivut(([]byte)("\n"))

	return reply

}
func (selv *TInternettprotocolprovider) Send(målipaddressNettverkbyteorder uint32, protocol uint8, dataPeker uintptr, størrelse uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternettprotocolv4Meldingbuffer = (*TInternettprotocolv4Meldingbuffer)(Pointer(&buffer1_2))
	var melding TInternettprotocolv4Melding = TInternettprotocolv4Melding{}
	melding.versjon = 4
	melding.topptekstLengde = ipStørrelse / 4
	melding.tos = 0
	melding.totaltLengde = Unsignedinteger16r(uint16(størrelse + uint32(ipStørrelse)))

	melding.ident = 0x0100
	melding.flaggogAvstand = 0x0040
	melding.tidtolive = 0x40
	melding.protocol = protocol

	melding.målipaddress = målipaddressNettverkbyteorder

	melding.kildeipaddress = uint32(efhandler.Getipaddress())

	melding.checksum = 0

	melding.Settbuffer(buffer_2)
	melding.checksum = selv.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipStørrelse))
	melding.Settbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataPeker))

	for i := 0; i < int(størrelse); i++ {

		buffer1_2[i+int(ipStørrelse)] = databuffer_2[i]
	}

	ipconsole.MSkrivutxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(størrelse)+int(ipStørrelse); i++ {
		ipconsole.MHexadecimalSkrivut(buffer1_2[i])
	}
	ipconsole.MSkrivut(([]byte)(":"))
	ipconsole.MSkrivut(([]byte)("]\n"))

	var nestehopipaddressNettverkbyteorder uint32 = målipaddressNettverkbyteorder
	if (målipaddressNettverkbyteorder & selv.SubnetMaske) != (melding.kildeipaddress & selv.SubnetMaske) {
		nestehopipaddressNettverkbyteorder = selv.Gatewayip
	}

	var senddataPeker = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Skrivut(nestehopipaddressNettverkbyteorder)

	var ethernetFiltypebe = Unsignedinteger16r(0x0800)
	efhandler.Rammesend(selv.arpprovider.Resolve(nestehopipaddressNettverkbyteorder), ethernetFiltypebe, senddataPeker, uint32(ipStørrelse)+uint32(størrelse))

}
func (selv *TInternettprotocolprovider) Checksum(pdata *[4096]uint16, lengdeInnByte uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataByte [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengdeInnByte % 2) != 0 {
		temporary += uint32(uint16(dataByte[lengdeInnByte-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (selv *TInternettprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
