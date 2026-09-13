package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetRamme"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4Meddelelsebuffer struct {
	lenver		byte
	tos		byte
	totalLængde	[2]byte

	ident			[2]byte
	flagogForskydning	[2]byte

	tidtolive	byte
	protocol	byte
	checksum	[2]byte

	kildeipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipStørrelse uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Meddelelse struct {
	headerLængde	uint8
	version		uint8
	tos		uint8
	totalLængde	uint16

	ident			uint16
	flagogForskydning	uint16

	tidtolive	uint8
	protocol	uint8
	checksum	uint16

	kildeipaddress		uint32
	destinationipaddress	uint32
}

func (selv *TInternetprotocolv4Meddelelse) Init(buffer_2 TInternetprotocolv4Meddelelsebuffer) {

	selv.version = ((buffer_2.lenver & 0xF0) >> 4)
	selv.headerLængde = buffer_2.lenver & 0x0F
	selv.tos = buffer_2.tos
	selv.totalLængde = Unsignedinteger16r(Tabeltounsignedinteger16(buffer_2.totalLængde))

	selv.ident = Unsignedinteger16r(Tabeltounsignedinteger16(buffer_2.ident))
	selv.flagogForskydning = Unsignedinteger16r(Tabeltounsignedinteger16(buffer_2.flagogForskydning))

	selv.tidtolive = buffer_2.tidtolive
	selv.protocol = buffer_2.protocol
	selv.checksum = Unsignedinteger16r(Tabeltounsignedinteger16(buffer_2.checksum))

	selv.kildeipaddress = Unsignedinteger32r(Tabeltounsignedinteger32(buffer_2.kildeipaddress))
	selv.destinationipaddress = Unsignedinteger32r(Tabeltounsignedinteger32(buffer_2.destinationipaddress))

}
func (selv *TInternetprotocolv4Meddelelse) Satbuffer(buffer_2 *TInternetprotocolv4Meddelelsebuffer) {

	buffer_2.lenver = byte(((selv.version & 0x0F) << 4) | (selv.headerLængde & 0x0F))
	buffer_2.tos = selv.tos
	buffer_2.totalLængde = Unsignedinteger16toTabel(selv.totalLængde)

	buffer_2.ident = Unsignedinteger16toTabel(selv.ident)
	buffer_2.flagogForskydning = Unsignedinteger16toTabel(selv.flagogForskydning)

	buffer_2.tidtolive = selv.tidtolive
	buffer_2.protocol = selv.protocol
	buffer_2.checksum = Unsignedinteger16toTabel(selv.checksum)

	buffer_2.kildeipaddress = Unsignedinteger32toTabel(selv.kildeipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toTabel(selv.destinationipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(kildeipaddressNetværkbyteorder uint32, destinationipaddressNetværkbyteorder uint32, dataMarkør uintptr, størrelse uint32) bool
	Send(destinationipaddressNetværkbyteorder uint32, pprotocol uint8, dataMarkør uintptr, størrelse uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetRammehandler IpethernetRammehandler = IpethernetRammehandler{}
var protocol uint8

func (selv *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (selv *TInternetprotocolhandler) Internetprotocolreceivewhen(kildeipaddressNetværkbyteorder uint32, destinationipaddressNetværkbyteorder uint32, dataMarkør uintptr, størrelse uint32) bool {
	ipconsole.MUdskriv(([]byte)("ipHandler:OnInternet"))
	return false
}
func (selv *TInternetprotocolhandler) Send(destinationipaddressNetværkbyteorder uint32, pprotocol uint8, dataMarkør uintptr, størrelse uint32) {

	ipprovider.Send(destinationipaddressNetværkbyteorder, pprotocol, dataMarkør, størrelse)
}
func (selv *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpethernetRammehandler struct {
	TEthernetRammehandler
}

var ipprovider TInternetprotocolprovider

func (selv *IpethernetRammehandler) EthernetRammereceivewhen(dataMarkør uintptr, størrelse int) bool {
	ipconsole.MUdskriv(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetRammereceivewhen(dataMarkør, uint32(størrelse))

}

func (selv *IpethernetRammehandler) Send(destinationipaddressNetværkbyteorder uint64, dataMarkør uintptr, størrelse uint32) {
	ipconsole.MUdskriv(([]byte)("ipefhandler:send\n"))
	var ethernettypebe = Unsignedinteger16r(0x0800)
	selv.TEthernetRammehandler.Rammesend(destinationipaddressNetværkbyteorder, ethernettypebe, dataMarkør, størrelse)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaske	uint32
}

var efhandler IEthernetRammehandler

func (selv *TInternetprotocolprovider) Init(pefprovider TEthernetRammeprovider, pefhandler IEthernetRammehandler, arp Arpprovider, gatewayip uint32, subnetMaske uint32) {

	efhandler = pefhandler
	efhandler.Sathandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	selv.arpprovider = arp
	selv.Gatewayip = gatewayip
	selv.SubnetMaske = subnetMaske
	ipprovider = *selv
}
func (selv *TInternetprotocolprovider) EthernetRammereceivewhen(ethernetRammepayload uintptr, størrelse uint32) bool {
	if størrelse < uint32(ipStørrelse) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Meddelelsebuffer = (*TInternetprotocolv4Meddelelsebuffer)(Pointer(ethernetRammepayload))
	var internetprotocolMeddelelse TInternetprotocolv4Meddelelse
	internetprotocolMeddelelse.Init(*buffer_2)

	var reply bool = false

	if internetprotocolMeddelelse.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var længde uint32 = uint32(internetprotocolMeddelelse.totalLængde)
		if længde > størrelse {
			længde = størrelse
		}
		if handler_2[internetprotocolMeddelelse.protocol] != nil {
			reply = handler_2[internetprotocolMeddelelse.protocol].Internetprotocolreceivewhen(internetprotocolMeddelelse.kildeipaddress, internetprotocolMeddelelse.destinationipaddress, ethernetRammepayload+uintptr(4*internetprotocolMeddelelse.headerLængde), uint32(længde-uint32(4*internetprotocolMeddelelse.headerLængde)))

		}
	}

	if reply {

		var temporary = internetprotocolMeddelelse.destinationipaddress
		internetprotocolMeddelelse.destinationipaddress = internetprotocolMeddelelse.kildeipaddress
		internetprotocolMeddelelse.kildeipaddress = temporary

		internetprotocolMeddelelse.tidtolive = 0x40
		internetprotocolMeddelelse.checksum = 0

		internetprotocolMeddelelse.Satbuffer(buffer_2)
		internetprotocolMeddelelse.checksum = selv.Checksum((*([4096]uint16))(Pointer(ethernetRammepayload)), uint32(4*internetprotocolMeddelelse.headerLængde))

		internetprotocolMeddelelse.Satbuffer(buffer_2)

	}

	ipconsole.MUdskriv(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Udskriv(internetprotocolMeddelelse.kildeipaddress)
	ipconsole.MUdskriv(([]byte)(":"))
	ipconsole.MUnsignedinteger32Udskriv(internetprotocolMeddelelse.destinationipaddress)
	ipconsole.MUdskriv(([]byte)(":"))
	ipconsole.MUnsignedinteger16Udskriv(uint16(internetprotocolMeddelelse.headerLængde))
	ipconsole.MUdskriv(([]byte)(":"))
	ipconsole.MUnsignedinteger16Udskriv(uint16(internetprotocolMeddelelse.version))
	ipconsole.MUdskriv(([]byte)(":"))
	ipconsole.MUnsignedinteger16Udskriv(internetprotocolMeddelelse.totalLængde)
	ipconsole.MUdskriv(([]byte)(":"))
	ipconsole.MUnsignedinteger32Udskriv(uint32(efhandler.Getipaddress()))
	ipconsole.MUdskriv(([]byte)(":"))
	ipconsole.MUdskriv(([]byte)("\n"))

	return reply

}
func (selv *TInternetprotocolprovider) Send(destinationipaddressNetværkbyteorder uint32, protocol uint8, dataMarkør uintptr, størrelse uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Meddelelsebuffer = (*TInternetprotocolv4Meddelelsebuffer)(Pointer(&buffer1_2))
	var meddelelse TInternetprotocolv4Meddelelse = TInternetprotocolv4Meddelelse{}
	meddelelse.version = 4
	meddelelse.headerLængde = ipStørrelse / 4
	meddelelse.tos = 0
	meddelelse.totalLængde = Unsignedinteger16r(uint16(størrelse + uint32(ipStørrelse)))

	meddelelse.ident = 0x0100
	meddelelse.flagogForskydning = 0x0040
	meddelelse.tidtolive = 0x40
	meddelelse.protocol = protocol

	meddelelse.destinationipaddress = destinationipaddressNetværkbyteorder

	meddelelse.kildeipaddress = uint32(efhandler.Getipaddress())

	meddelelse.checksum = 0

	meddelelse.Satbuffer(buffer_2)
	meddelelse.checksum = selv.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipStørrelse))
	meddelelse.Satbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataMarkør))

	for i := 0; i < int(størrelse); i++ {

		buffer1_2[i+int(ipStørrelse)] = databuffer_2[i]
	}

	ipconsole.MUdskrivxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(størrelse)+int(ipStørrelse); i++ {
		ipconsole.MHexadecimalUdskriv(buffer1_2[i])
	}
	ipconsole.MUdskriv(([]byte)(":"))
	ipconsole.MUdskriv(([]byte)("]\n"))

	var næstehopipaddressNetværkbyteorder uint32 = destinationipaddressNetværkbyteorder
	if (destinationipaddressNetværkbyteorder & selv.SubnetMaske) != (meddelelse.kildeipaddress & selv.SubnetMaske) {
		næstehopipaddressNetværkbyteorder = selv.Gatewayip
	}

	var senddataMarkør = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Udskriv(næstehopipaddressNetværkbyteorder)

	var ethernettypebe = Unsignedinteger16r(0x0800)
	efhandler.Rammesend(selv.arpprovider.Resolve(næstehopipaddressNetværkbyteorder), ethernettypebe, senddataMarkør, uint32(ipStørrelse)+uint32(størrelse))

}
func (selv *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, længdeIndByte uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataByte [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (længdeIndByte % 2) != 0 {
		temporary += uint32(uint16(dataByte[længdeIndByte-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (selv *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
