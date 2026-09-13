package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetRamka"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4XABARbuffer struct {
	lenver		byte
	tos		byte
	jamiUzunlik	[2]byte

	ident			[2]byte
	bayroqlarandoffset	[2]byte

	vaqttolive	byte
	protocol	byte
	checksum	[2]byte

	sourceipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipHajmi uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4XABAR struct {
	headerUzunlik	uint8
	version		uint8
	tos		uint8
	jamiUzunlik	uint16

	ident			uint16
	bayroqlarandoffset	uint16

	vaqttolive	uint8
	protocol	uint8
	checksum	uint16

	sourceipaddress		uint32
	destinationipaddress	uint32
}

func (self *TInternetprotocolv4XABAR) Init(buffer_2 TInternetprotocolv4XABARbuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerUzunlik = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.jamiUzunlik = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.jamiUzunlik))

	self.ident = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ident))
	self.bayroqlarandoffset = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.bayroqlarandoffset))

	self.vaqttolive = buffer_2.vaqttolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))

	self.sourceipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.sourceipaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TInternetprotocolv4XABAR) Setbuffer(buffer_2 *TInternetprotocolv4XABARbuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerUzunlik & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.jamiUzunlik = Unsignedinteger16toarray(self.jamiUzunlik)

	buffer_2.ident = Unsignedinteger16toarray(self.ident)
	buffer_2.bayroqlarandoffset = Unsignedinteger16toarray(self.bayroqlarandoffset)

	buffer_2.vaqttolive = self.vaqttolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

	buffer_2.sourceipaddress = Unsignedinteger32toarray(self.sourceipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(sourceipaddressTarmoqbyteorder uint32, destinationipaddressTarmoqbyteorder uint32, dataKorsatgich uintptr, hajmi uint32) bool
	Joʻnatish(destinationipaddressTarmoqbyteorder uint32, pprotocol uint8, dataKorsatgich uintptr, hajmi uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetRamkahandler IpethernetRamkahandler = IpethernetRamkahandler{}
var protocol uint8

func (self *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(sourceipaddressTarmoqbyteorder uint32, destinationipaddressTarmoqbyteorder uint32, dataKorsatgich uintptr, hajmi uint32) bool {
	ipconsole.MChopetish(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Joʻnatish(destinationipaddressTarmoqbyteorder uint32, pprotocol uint8, dataKorsatgich uintptr, hajmi uint32) {

	ipprovider.Joʻnatish(destinationipaddressTarmoqbyteorder, pprotocol, dataKorsatgich, hajmi)
}
func (self *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpethernetRamkahandler struct {
	TEthernetRamkahandler
}

var ipprovider TInternetprotocolprovider

func (self *IpethernetRamkahandler) EthernetRamkareceivewhen(dataKorsatgich uintptr, hajmi int) bool {
	ipconsole.MChopetish(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetRamkareceivewhen(dataKorsatgich, uint32(hajmi))

}

func (self *IpethernetRamkahandler) Joʻnatish(destinationipaddressTarmoqbyteorder uint64, dataKorsatgich uintptr, hajmi uint32) {
	ipconsole.MChopetish(([]byte)("ipefhandler:send\n"))
	var ethernetTuribe = Unsignedinteger16r(0x0800)
	self.TEthernetRamkahandler.RamkaJoʻnatish(destinationipaddressTarmoqbyteorder, ethernetTuribe, dataKorsatgich, hajmi)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetRamkahandler

func (self *TInternetprotocolprovider) Init(pefprovider TEthernetRamkaprovider, pefhandler IEthernetRamkahandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Sethandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnetmask = subnetmask
	ipprovider = *self
}
func (self *TInternetprotocolprovider) EthernetRamkareceivewhen(ethernetRamkapayload uintptr, hajmi uint32) bool {
	if hajmi < uint32(ipHajmi) {
		return false
	}

	var buffer_2 *TInternetprotocolv4XABARbuffer = (*TInternetprotocolv4XABARbuffer)(Pointer(ethernetRamkapayload))
	var internetprotocolXABAR TInternetprotocolv4XABAR
	internetprotocolXABAR.Init(*buffer_2)

	var reply bool = false

	if internetprotocolXABAR.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var uzunlik uint32 = uint32(internetprotocolXABAR.jamiUzunlik)
		if uzunlik > hajmi {
			uzunlik = hajmi
		}
		if handler_2[internetprotocolXABAR.protocol] != nil {
			reply = handler_2[internetprotocolXABAR.protocol].Internetprotocolreceivewhen(internetprotocolXABAR.sourceipaddress, internetprotocolXABAR.destinationipaddress, ethernetRamkapayload+uintptr(4*internetprotocolXABAR.headerUzunlik), uint32(uzunlik-uint32(4*internetprotocolXABAR.headerUzunlik)))

		}
	}

	if reply {

		var temporary = internetprotocolXABAR.destinationipaddress
		internetprotocolXABAR.destinationipaddress = internetprotocolXABAR.sourceipaddress
		internetprotocolXABAR.sourceipaddress = temporary

		internetprotocolXABAR.vaqttolive = 0x40
		internetprotocolXABAR.checksum = 0

		internetprotocolXABAR.Setbuffer(buffer_2)
		internetprotocolXABAR.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetRamkapayload)), uint32(4*internetprotocolXABAR.headerUzunlik))

		internetprotocolXABAR.Setbuffer(buffer_2)

	}

	ipconsole.MChopetish(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Chopetish(internetprotocolXABAR.sourceipaddress)
	ipconsole.MChopetish(([]byte)(":"))
	ipconsole.MUnsignedinteger32Chopetish(internetprotocolXABAR.destinationipaddress)
	ipconsole.MChopetish(([]byte)(":"))
	ipconsole.MUnsignedinteger16Chopetish(uint16(internetprotocolXABAR.headerUzunlik))
	ipconsole.MChopetish(([]byte)(":"))
	ipconsole.MUnsignedinteger16Chopetish(uint16(internetprotocolXABAR.version))
	ipconsole.MChopetish(([]byte)(":"))
	ipconsole.MUnsignedinteger16Chopetish(internetprotocolXABAR.jamiUzunlik)
	ipconsole.MChopetish(([]byte)(":"))
	ipconsole.MUnsignedinteger32Chopetish(uint32(efhandler.Getipaddress()))
	ipconsole.MChopetish(([]byte)(":"))
	ipconsole.MChopetish(([]byte)("\n"))

	return reply

}
func (self *TInternetprotocolprovider) Joʻnatish(destinationipaddressTarmoqbyteorder uint32, protocol uint8, dataKorsatgich uintptr, hajmi uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4XABARbuffer = (*TInternetprotocolv4XABARbuffer)(Pointer(&buffer1_2))
	var xABAR TInternetprotocolv4XABAR = TInternetprotocolv4XABAR{}
	xABAR.version = 4
	xABAR.headerUzunlik = ipHajmi / 4
	xABAR.tos = 0
	xABAR.jamiUzunlik = Unsignedinteger16r(uint16(hajmi + uint32(ipHajmi)))

	xABAR.ident = 0x0100
	xABAR.bayroqlarandoffset = 0x0040
	xABAR.vaqttolive = 0x40
	xABAR.protocol = protocol

	xABAR.destinationipaddress = destinationipaddressTarmoqbyteorder

	xABAR.sourceipaddress = uint32(efhandler.Getipaddress())

	xABAR.checksum = 0

	xABAR.Setbuffer(buffer_2)
	xABAR.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipHajmi))
	xABAR.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataKorsatgich))

	for i := 0; i < int(hajmi); i++ {

		buffer1_2[i+int(ipHajmi)] = databuffer_2[i]
	}

	ipconsole.MChopetishxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(hajmi)+int(ipHajmi); i++ {
		ipconsole.MHexadecimalChopetish(buffer1_2[i])
	}
	ipconsole.MChopetish(([]byte)(":"))
	ipconsole.MChopetish(([]byte)("]\n"))

	var keyingihopipaddressTarmoqbyteorder uint32 = destinationipaddressTarmoqbyteorder
	if (destinationipaddressTarmoqbyteorder & self.Subnetmask) != (xABAR.sourceipaddress & self.Subnetmask) {
		keyingihopipaddressTarmoqbyteorder = self.Gatewayip
	}

	var joʻnatishdataKorsatgich = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Chopetish(keyingihopipaddressTarmoqbyteorder)

	var ethernetTuribe = Unsignedinteger16r(0x0800)
	efhandler.RamkaJoʻnatish(self.arpprovider.Resolve(keyingihopipaddressTarmoqbyteorder), ethernetTuribe, joʻnatishdataKorsatgich, uint32(ipHajmi)+uint32(hajmi))

}
func (self *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, uzunlikYaqinlashtirishBaytlar uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBaytlar [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (uzunlikYaqinlashtirishBaytlar % 2) != 0 {
		temporary += uint32(uint16(dataBaytlar[uzunlikYaqinlashtirishBaytlar-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
