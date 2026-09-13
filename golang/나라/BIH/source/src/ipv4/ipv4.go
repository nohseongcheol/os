package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetOkvir"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4Porukabuffer struct {
	lenver		byte
	tos		byte
	ukupnolength	[2]byte

	ident			[2]byte
	zastaveandoffset	[2]byte

	vrijemetolive	byte
	protocol	byte
	checksum	[2]byte

	izvoripaddress		[4]byte
	odredišteipaddress	[4]byte
}

var ipVeličina uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Poruka struct {
	headerlength	uint8
	verzija		uint8
	tos		uint8
	ukupnolength	uint16

	ident			uint16
	zastaveandoffset	uint16

	vrijemetolive	uint8
	protocol	uint8
	checksum	uint16

	izvoripaddress		uint32
	odredišteipaddress	uint32
}

func (self *TInternetprotocolv4Poruka) Init(buffer_2 TInternetprotocolv4Porukabuffer) {

	self.verzija = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerlength = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.ukupnolength = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ukupnolength))

	self.ident = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ident))
	self.zastaveandoffset = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.zastaveandoffset))

	self.vrijemetolive = buffer_2.vrijemetolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))

	self.izvoripaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.izvoripaddress))
	self.odredišteipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.odredišteipaddress))

}
func (self *TInternetprotocolv4Poruka) Skupbuffer(buffer_2 *TInternetprotocolv4Porukabuffer) {

	buffer_2.lenver = byte(((self.verzija & 0x0F) << 4) | (self.headerlength & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.ukupnolength = Unsignedinteger16toarray(self.ukupnolength)

	buffer_2.ident = Unsignedinteger16toarray(self.ident)
	buffer_2.zastaveandoffset = Unsignedinteger16toarray(self.zastaveandoffset)

	buffer_2.vrijemetolive = self.vrijemetolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

	buffer_2.izvoripaddress = Unsignedinteger32toarray(self.izvoripaddress)
	buffer_2.odredišteipaddress = Unsignedinteger32toarray(self.odredišteipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, datapointer uintptr, veličina uint32) bool
	Pošalji(odredišteipaddressMrežabyteorder uint32, pprotocol uint8, datapointer uintptr, veličina uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetOkvirhandler IpethernetOkvirhandler = IpethernetOkvirhandler{}
var protocol uint8

func (self *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, datapointer uintptr, veličina uint32) bool {
	ipconsole.MŠtampaj(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Pošalji(odredišteipaddressMrežabyteorder uint32, pprotocol uint8, datapointer uintptr, veličina uint32) {

	ipprovider.Pošalji(odredišteipaddressMrežabyteorder, pprotocol, datapointer, veličina)
}
func (self *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpethernetOkvirhandler struct {
	TEthernetOkvirhandler
}

var ipprovider TInternetprotocolprovider

func (self *IpethernetOkvirhandler) EthernetOkvirreceivewhen(datapointer uintptr, veličina int) bool {
	ipconsole.MŠtampaj(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetOkvirreceivewhen(datapointer, uint32(veličina))

}

func (self *IpethernetOkvirhandler) Pošalji(odredišteipaddressMrežabyteorder uint64, datapointer uintptr, veličina uint32) {
	ipconsole.MŠtampaj(([]byte)("ipefhandler:send\n"))
	var ethernetTipbe = Unsignedinteger16r(0x0800)
	self.TEthernetOkvirhandler.OkvirPošalji(odredišteipaddressMrežabyteorder, ethernetTipbe, datapointer, veličina)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaska	uint32
}

var efhandler IEthernetOkvirhandler

func (self *TInternetprotocolprovider) Init(pefprovider TEthernetOkvirprovider, pefhandler IEthernetOkvirhandler, arp Arpprovider, gatewayip uint32, subnetMaska uint32) {

	efhandler = pefhandler
	efhandler.Skuphandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.SubnetMaska = subnetMaska
	ipprovider = *self
}
func (self *TInternetprotocolprovider) EthernetOkvirreceivewhen(ethernetOkvirpayload uintptr, veličina uint32) bool {
	if veličina < uint32(ipVeličina) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Porukabuffer = (*TInternetprotocolv4Porukabuffer)(Pointer(ethernetOkvirpayload))
	var internetprotocolPoruka TInternetprotocolv4Poruka
	internetprotocolPoruka.Init(*buffer_2)

	var reply bool = false

	if internetprotocolPoruka.odredišteipaddress == uint32(efhandler.Getipaddress()) {

		var length uint32 = uint32(internetprotocolPoruka.ukupnolength)
		if length > veličina {
			length = veličina
		}
		if handler_2[internetprotocolPoruka.protocol] != nil {
			reply = handler_2[internetprotocolPoruka.protocol].Internetprotocolreceivewhen(internetprotocolPoruka.izvoripaddress, internetprotocolPoruka.odredišteipaddress, ethernetOkvirpayload+uintptr(4*internetprotocolPoruka.headerlength), uint32(length-uint32(4*internetprotocolPoruka.headerlength)))

		}
	}

	if reply {

		var temporary = internetprotocolPoruka.odredišteipaddress
		internetprotocolPoruka.odredišteipaddress = internetprotocolPoruka.izvoripaddress
		internetprotocolPoruka.izvoripaddress = temporary

		internetprotocolPoruka.vrijemetolive = 0x40
		internetprotocolPoruka.checksum = 0

		internetprotocolPoruka.Skupbuffer(buffer_2)
		internetprotocolPoruka.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetOkvirpayload)), uint32(4*internetprotocolPoruka.headerlength))

		internetprotocolPoruka.Skupbuffer(buffer_2)

	}

	ipconsole.MŠtampaj(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Štampaj(internetprotocolPoruka.izvoripaddress)
	ipconsole.MŠtampaj(([]byte)(":"))
	ipconsole.MUnsignedinteger32Štampaj(internetprotocolPoruka.odredišteipaddress)
	ipconsole.MŠtampaj(([]byte)(":"))
	ipconsole.MUnsignedinteger16Štampaj(uint16(internetprotocolPoruka.headerlength))
	ipconsole.MŠtampaj(([]byte)(":"))
	ipconsole.MUnsignedinteger16Štampaj(uint16(internetprotocolPoruka.verzija))
	ipconsole.MŠtampaj(([]byte)(":"))
	ipconsole.MUnsignedinteger16Štampaj(internetprotocolPoruka.ukupnolength)
	ipconsole.MŠtampaj(([]byte)(":"))
	ipconsole.MUnsignedinteger32Štampaj(uint32(efhandler.Getipaddress()))
	ipconsole.MŠtampaj(([]byte)(":"))
	ipconsole.MŠtampaj(([]byte)("\n"))

	return reply

}
func (self *TInternetprotocolprovider) Pošalji(odredišteipaddressMrežabyteorder uint32, protocol uint8, datapointer uintptr, veličina uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Porukabuffer = (*TInternetprotocolv4Porukabuffer)(Pointer(&buffer1_2))
	var poruka TInternetprotocolv4Poruka = TInternetprotocolv4Poruka{}
	poruka.verzija = 4
	poruka.headerlength = ipVeličina / 4
	poruka.tos = 0
	poruka.ukupnolength = Unsignedinteger16r(uint16(veličina + uint32(ipVeličina)))

	poruka.ident = 0x0100
	poruka.zastaveandoffset = 0x0040
	poruka.vrijemetolive = 0x40
	poruka.protocol = protocol

	poruka.odredišteipaddress = odredišteipaddressMrežabyteorder

	poruka.izvoripaddress = uint32(efhandler.Getipaddress())

	poruka.checksum = 0

	poruka.Skupbuffer(buffer_2)
	poruka.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipVeličina))
	poruka.Skupbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(veličina); i++ {

		buffer1_2[i+int(ipVeličina)] = databuffer_2[i]
	}

	ipconsole.MŠtampajxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(veličina)+int(ipVeličina); i++ {
		ipconsole.MHexadecimalŠtampaj(buffer1_2[i])
	}
	ipconsole.MŠtampaj(([]byte)(":"))
	ipconsole.MŠtampaj(([]byte)("]\n"))

	var sljedećehopipaddressMrežabyteorder uint32 = odredišteipaddressMrežabyteorder
	if (odredišteipaddressMrežabyteorder & self.SubnetMaska) != (poruka.izvoripaddress & self.SubnetMaska) {
		sljedećehopipaddressMrežabyteorder = self.Gatewayip
	}

	var pošaljidatapointer = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Štampaj(sljedećehopipaddressMrežabyteorder)

	var ethernetTipbe = Unsignedinteger16r(0x0800)
	efhandler.OkvirPošalji(self.arpprovider.Resolve(sljedećehopipaddressMrežabyteorder), ethernetTipbe, pošaljidatapointer, uint32(ipVeličina)+uint32(veličina))

}
func (self *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, lengthPrimljenoBajtova uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBajtova [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengthPrimljenoBajtova % 2) != 0 {
		temporary += uint32(uint16(dataBajtova[lengthPrimljenoBajtova-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
