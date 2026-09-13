package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetRammi"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetiðprotocolv4SKILABOÐbuffer struct {
	lenver		byte
	tos		byte
	totalLengd	[2]byte

	ident		[2]byte
	flagsandoffset	[2]byte

	tímitolive	byte
	protocol	byte
	checksum	[2]byte

	uppruniipaddress	[4]byte
	áfangastaðuripaddress	[4]byte
}

var ipStærð uint8 = (4 + 4 + 4 + 8)

type TInternetiðprotocolv4SKILABOÐ struct {
	headerLengd	uint8
	version		uint8
	tos		uint8
	totalLengd	uint16

	ident		uint16
	flagsandoffset	uint16

	tímitolive	uint8
	protocol	uint8
	checksum	uint16

	uppruniipaddress	uint32
	áfangastaðuripaddress	uint32
}

func (sjálft *TInternetiðprotocolv4SKILABOÐ) Init(buffer_2 TInternetiðprotocolv4SKILABOÐbuffer) {

	sjálft.version = ((buffer_2.lenver & 0xF0) >> 4)
	sjálft.headerLengd = buffer_2.lenver & 0x0F
	sjálft.tos = buffer_2.tos
	sjálft.totalLengd = Unsignedinteger16r(Fylkitounsignedinteger16(buffer_2.totalLengd))

	sjálft.ident = Unsignedinteger16r(Fylkitounsignedinteger16(buffer_2.ident))
	sjálft.flagsandoffset = Unsignedinteger16r(Fylkitounsignedinteger16(buffer_2.flagsandoffset))

	sjálft.tímitolive = buffer_2.tímitolive
	sjálft.protocol = buffer_2.protocol
	sjálft.checksum = Unsignedinteger16r(Fylkitounsignedinteger16(buffer_2.checksum))

	sjálft.uppruniipaddress = Unsignedinteger32r(Fylkitounsignedinteger32(buffer_2.uppruniipaddress))
	sjálft.áfangastaðuripaddress = Unsignedinteger32r(Fylkitounsignedinteger32(buffer_2.áfangastaðuripaddress))

}
func (sjálft *TInternetiðprotocolv4SKILABOÐ) Setjabuffer(buffer_2 *TInternetiðprotocolv4SKILABOÐbuffer) {

	buffer_2.lenver = byte(((sjálft.version & 0x0F) << 4) | (sjálft.headerLengd & 0x0F))
	buffer_2.tos = sjálft.tos
	buffer_2.totalLengd = Unsignedinteger16toFylki(sjálft.totalLengd)

	buffer_2.ident = Unsignedinteger16toFylki(sjálft.ident)
	buffer_2.flagsandoffset = Unsignedinteger16toFylki(sjálft.flagsandoffset)

	buffer_2.tímitolive = sjálft.tímitolive
	buffer_2.protocol = sjálft.protocol
	buffer_2.checksum = Unsignedinteger16toFylki(sjálft.checksum)

	buffer_2.uppruniipaddress = Unsignedinteger32toFylki(sjálft.uppruniipaddress)
	buffer_2.áfangastaðuripaddress = Unsignedinteger32toFylki(sjálft.áfangastaðuripaddress)

}

type IInternetiðprotocolhandler interface {
	Init(backend TInternetiðprotocolprovider, pihandler IInternetiðprotocolhandler, pprotocol uint8)
	Internetiðprotocolreceivewhen(uppruniipaddressNetkerfibyteorder uint32, áfangastaðuripaddressNetkerfibyteorder uint32, dataBendill uintptr, stærð uint32) bool
	Senda(áfangastaðuripaddressNetkerfibyteorder uint32, pprotocol uint8, dataBendill uintptr, stærð uint32)
	Providerget() *TInternetiðprotocolprovider
}

type TInternetiðprotocolhandler struct {
}

var ipethernetRammihandler IpethernetRammihandler = IpethernetRammihandler{}
var protocol uint8

func (sjálft *TInternetiðprotocolhandler) Init(backend TInternetiðprotocolprovider, pihandler IInternetiðprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (sjálft *TInternetiðprotocolhandler) Internetiðprotocolreceivewhen(uppruniipaddressNetkerfibyteorder uint32, áfangastaðuripaddressNetkerfibyteorder uint32, dataBendill uintptr, stærð uint32) bool {
	ipconsole.MPrenta(([]byte)("ipHandler:OnInternet"))
	return false
}
func (sjálft *TInternetiðprotocolhandler) Senda(áfangastaðuripaddressNetkerfibyteorder uint32, pprotocol uint8, dataBendill uintptr, stærð uint32) {

	ipprovider.Senda(áfangastaðuripaddressNetkerfibyteorder, pprotocol, dataBendill, stærð)
}
func (sjálft *TInternetiðprotocolhandler) Providerget() *TInternetiðprotocolprovider {
	return &ipprovider
}

type IpethernetRammihandler struct {
	TEthernetRammihandler
}

var ipprovider TInternetiðprotocolprovider

func (sjálft *IpethernetRammihandler) EthernetRammireceivewhen(dataBendill uintptr, stærð int) bool {
	ipconsole.MPrenta(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetRammireceivewhen(dataBendill, uint32(stærð))

}

func (sjálft *IpethernetRammihandler) Senda(áfangastaðuripaddressNetkerfibyteorder uint64, dataBendill uintptr, stærð uint32) {
	ipconsole.MPrenta(([]byte)("ipefhandler:send\n"))
	var ethernetTegundbe = Unsignedinteger16r(0x0800)
	sjálft.TEthernetRammihandler.RammiSenda(áfangastaðuripaddressNetkerfibyteorder, ethernetTegundbe, dataBendill, stærð)

}

var handler_2 [255]IInternetiðprotocolhandler

type TInternetiðprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMöskvi	uint32
}

var efhandler IEthernetRammihandler

func (sjálft *TInternetiðprotocolprovider) Init(pefprovider TEthernetRammiprovider, pefhandler IEthernetRammihandler, arp Arpprovider, gatewayip uint32, subnetMöskvi uint32) {

	efhandler = pefhandler
	efhandler.Setjahandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	sjálft.arpprovider = arp
	sjálft.Gatewayip = gatewayip
	sjálft.SubnetMöskvi = subnetMöskvi
	ipprovider = *sjálft
}
func (sjálft *TInternetiðprotocolprovider) EthernetRammireceivewhen(ethernetRammipayload uintptr, stærð uint32) bool {
	if stærð < uint32(ipStærð) {
		return false
	}

	var buffer_2 *TInternetiðprotocolv4SKILABOÐbuffer = (*TInternetiðprotocolv4SKILABOÐbuffer)(Pointer(ethernetRammipayload))
	var internetiðprotocolSKILABOÐ TInternetiðprotocolv4SKILABOÐ
	internetiðprotocolSKILABOÐ.Init(*buffer_2)

	var reply bool = false

	if internetiðprotocolSKILABOÐ.áfangastaðuripaddress == uint32(efhandler.Getipaddress()) {

		var lengd uint32 = uint32(internetiðprotocolSKILABOÐ.totalLengd)
		if lengd > stærð {
			lengd = stærð
		}
		if handler_2[internetiðprotocolSKILABOÐ.protocol] != nil {
			reply = handler_2[internetiðprotocolSKILABOÐ.protocol].Internetiðprotocolreceivewhen(internetiðprotocolSKILABOÐ.uppruniipaddress, internetiðprotocolSKILABOÐ.áfangastaðuripaddress, ethernetRammipayload+uintptr(4*internetiðprotocolSKILABOÐ.headerLengd), uint32(lengd-uint32(4*internetiðprotocolSKILABOÐ.headerLengd)))

		}
	}

	if reply {

		var temporary = internetiðprotocolSKILABOÐ.áfangastaðuripaddress
		internetiðprotocolSKILABOÐ.áfangastaðuripaddress = internetiðprotocolSKILABOÐ.uppruniipaddress
		internetiðprotocolSKILABOÐ.uppruniipaddress = temporary

		internetiðprotocolSKILABOÐ.tímitolive = 0x40
		internetiðprotocolSKILABOÐ.checksum = 0

		internetiðprotocolSKILABOÐ.Setjabuffer(buffer_2)
		internetiðprotocolSKILABOÐ.checksum = sjálft.Checksum((*([4096]uint16))(Pointer(ethernetRammipayload)), uint32(4*internetiðprotocolSKILABOÐ.headerLengd))

		internetiðprotocolSKILABOÐ.Setjabuffer(buffer_2)

	}

	ipconsole.MPrenta(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Prenta(internetiðprotocolSKILABOÐ.uppruniipaddress)
	ipconsole.MPrenta(([]byte)(":"))
	ipconsole.MUnsignedinteger32Prenta(internetiðprotocolSKILABOÐ.áfangastaðuripaddress)
	ipconsole.MPrenta(([]byte)(":"))
	ipconsole.MUnsignedinteger16Prenta(uint16(internetiðprotocolSKILABOÐ.headerLengd))
	ipconsole.MPrenta(([]byte)(":"))
	ipconsole.MUnsignedinteger16Prenta(uint16(internetiðprotocolSKILABOÐ.version))
	ipconsole.MPrenta(([]byte)(":"))
	ipconsole.MUnsignedinteger16Prenta(internetiðprotocolSKILABOÐ.totalLengd)
	ipconsole.MPrenta(([]byte)(":"))
	ipconsole.MUnsignedinteger32Prenta(uint32(efhandler.Getipaddress()))
	ipconsole.MPrenta(([]byte)(":"))
	ipconsole.MPrenta(([]byte)("\n"))

	return reply

}
func (sjálft *TInternetiðprotocolprovider) Senda(áfangastaðuripaddressNetkerfibyteorder uint32, protocol uint8, dataBendill uintptr, stærð uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetiðprotocolv4SKILABOÐbuffer = (*TInternetiðprotocolv4SKILABOÐbuffer)(Pointer(&buffer1_2))
	var sKILABOÐ TInternetiðprotocolv4SKILABOÐ = TInternetiðprotocolv4SKILABOÐ{}
	sKILABOÐ.version = 4
	sKILABOÐ.headerLengd = ipStærð / 4
	sKILABOÐ.tos = 0
	sKILABOÐ.totalLengd = Unsignedinteger16r(uint16(stærð + uint32(ipStærð)))

	sKILABOÐ.ident = 0x0100
	sKILABOÐ.flagsandoffset = 0x0040
	sKILABOÐ.tímitolive = 0x40
	sKILABOÐ.protocol = protocol

	sKILABOÐ.áfangastaðuripaddress = áfangastaðuripaddressNetkerfibyteorder

	sKILABOÐ.uppruniipaddress = uint32(efhandler.Getipaddress())

	sKILABOÐ.checksum = 0

	sKILABOÐ.Setjabuffer(buffer_2)
	sKILABOÐ.checksum = sjálft.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipStærð))
	sKILABOÐ.Setjabuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataBendill))

	for i := 0; i < int(stærð); i++ {

		buffer1_2[i+int(ipStærð)] = databuffer_2[i]
	}

	ipconsole.MPrentaxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(stærð)+int(ipStærð); i++ {
		ipconsole.MHexadecimalPrenta(buffer1_2[i])
	}
	ipconsole.MPrenta(([]byte)(":"))
	ipconsole.MPrenta(([]byte)("]\n"))

	var næstahopipaddressNetkerfibyteorder uint32 = áfangastaðuripaddressNetkerfibyteorder
	if (áfangastaðuripaddressNetkerfibyteorder & sjálft.SubnetMöskvi) != (sKILABOÐ.uppruniipaddress & sjálft.SubnetMöskvi) {
		næstahopipaddressNetkerfibyteorder = sjálft.Gatewayip
	}

	var sendadataBendill = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Prenta(næstahopipaddressNetkerfibyteorder)

	var ethernetTegundbe = Unsignedinteger16r(0x0800)
	efhandler.RammiSenda(sjálft.arpprovider.Resolve(næstahopipaddressNetkerfibyteorder), ethernetTegundbe, sendadataBendill, uint32(ipStærð)+uint32(stærð))

}
func (sjálft *TInternetiðprotocolprovider) Checksum(pdata *[4096]uint16, lengdInnBæti uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBæti [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengdInnBæti % 2) != 0 {
		temporary += uint32(uint16(dataBæti[lengdInnBæti-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (sjálft *TInternetiðprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
