/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "konzol"
import . "ethernetKeret"
import . "arp"

var ipKonzol TKonzol = TKonzol{}

type TInternetprotocolv4Üzenetbuffer struct {
	lenver		byte
	tos		byte
	összesenHossz	[2]byte

	ident		[2]byte
	flagekÉSEltolás	[2]byte

	időtolive	byte
	protocol	byte
	checksum	[2]byte

	forrásipaddress	[4]byte
	célipaddress	[4]byte
}

var ipMéret uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Üzenet struct {
	headerHossz	uint8
	verzió		uint8
	tos		uint8
	összesenHossz	uint16

	ident		uint16
	flagekÉSEltolás	uint16

	időtolive	uint8
	protocol	uint8
	checksum	uint16

	forrásipaddress	uint32
	célipaddress	uint32
}

func (self *TInternetprotocolv4Üzenet) Init(buffer_2 TInternetprotocolv4Üzenetbuffer) {

	self.verzió = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerHossz = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.összesenHossz = Unsignedinteger16r(Tömbtounsignedinteger16(buffer_2.összesenHossz))

	self.ident = Unsignedinteger16r(Tömbtounsignedinteger16(buffer_2.ident))
	self.flagekÉSEltolás = Unsignedinteger16r(Tömbtounsignedinteger16(buffer_2.flagekÉSEltolás))

	self.időtolive = buffer_2.időtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Tömbtounsignedinteger16(buffer_2.checksum))

	self.forrásipaddress = Unsignedinteger32r(Tömbtounsignedinteger32(buffer_2.forrásipaddress))
	self.célipaddress = Unsignedinteger32r(Tömbtounsignedinteger32(buffer_2.célipaddress))

}
func (self *TInternetprotocolv4Üzenet) Halmazbuffer(buffer_2 *TInternetprotocolv4Üzenetbuffer) {

	buffer_2.lenver = byte(((self.verzió & 0x0F) << 4) | (self.headerHossz & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.összesenHossz = Unsignedinteger16toTömb(self.összesenHossz)

	buffer_2.ident = Unsignedinteger16toTömb(self.ident)
	buffer_2.flagekÉSEltolás = Unsignedinteger16toTömb(self.flagekÉSEltolás)

	buffer_2.időtolive = self.időtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toTömb(self.checksum)

	buffer_2.forrásipaddress = Unsignedinteger32toTömb(self.forrásipaddress)
	buffer_2.célipaddress = Unsignedinteger32toTömb(self.célipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(forrásipaddressHálózatbyteorder uint32, célipaddressHálózatbyteorder uint32, dataMutató uintptr, méret uint32) bool
	Küldés(célipaddressHálózatbyteorder uint32, pprotocol uint8, dataMutató uintptr, méret uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetKerethandler IpethernetKerethandler = IpethernetKerethandler{}
var protocol uint8

func (self *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(forrásipaddressHálózatbyteorder uint32, célipaddressHálózatbyteorder uint32, dataMutató uintptr, méret uint32) bool {
	ipKonzol.MNyomtatás(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Küldés(célipaddressHálózatbyteorder uint32, pprotocol uint8, dataMutató uintptr, méret uint32) {

	ipprovider.Küldés(célipaddressHálózatbyteorder, pprotocol, dataMutató, méret)
}
func (self *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpethernetKerethandler struct {
	TEthernetKerethandler
}

var ipprovider TInternetprotocolprovider

func (self *IpethernetKerethandler) EthernetKeretreceivewhen(dataMutató uintptr, méret int) bool {
	ipKonzol.MNyomtatás(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetKeretreceivewhen(dataMutató, uint32(méret))

}

func (self *IpethernetKerethandler) Küldés(célipaddressHálózatbyteorder uint64, dataMutató uintptr, méret uint32) {
	ipKonzol.MNyomtatás(([]byte)("ipefhandler:send\n"))
	var ethernetTípusbe = Unsignedinteger16r(0x0800)
	self.TEthernetKerethandler.KeretKüldés(célipaddressHálózatbyteorder, ethernetTípusbe, dataMutató, méret)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Átjáróip	uint32
	SubnetMaszk	uint32
}

var efhandler IEthernetKerethandler

func (self *TInternetprotocolprovider) Init(pefprovider TEthernetKeretprovider, pefhandler IEthernetKerethandler, arp Arpprovider, átjáróip uint32, subnetMaszk uint32) {

	efhandler = pefhandler
	efhandler.Halmazhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Átjáróip = átjáróip
	self.SubnetMaszk = subnetMaszk
	ipprovider = *self
}
func (self *TInternetprotocolprovider) EthernetKeretreceivewhen(ethernetKeretpayload uintptr, méret uint32) bool {
	if méret < uint32(ipMéret) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Üzenetbuffer = (*TInternetprotocolv4Üzenetbuffer)(Pointer(ethernetKeretpayload))
	var internetprotocolÜzenet TInternetprotocolv4Üzenet
	internetprotocolÜzenet.Init(*buffer_2)

	var reply bool = false

	if internetprotocolÜzenet.célipaddress == uint32(efhandler.Getipaddress()) {

		var hossz uint32 = uint32(internetprotocolÜzenet.összesenHossz)
		if hossz > méret {
			hossz = méret
		}
		if handler_2[internetprotocolÜzenet.protocol] != nil {
			reply = handler_2[internetprotocolÜzenet.protocol].Internetprotocolreceivewhen(internetprotocolÜzenet.forrásipaddress, internetprotocolÜzenet.célipaddress, ethernetKeretpayload+uintptr(4*internetprotocolÜzenet.headerHossz), uint32(hossz-uint32(4*internetprotocolÜzenet.headerHossz)))

		}
	}

	if reply {

		var temporary = internetprotocolÜzenet.célipaddress
		internetprotocolÜzenet.célipaddress = internetprotocolÜzenet.forrásipaddress
		internetprotocolÜzenet.forrásipaddress = temporary

		internetprotocolÜzenet.időtolive = 0x40
		internetprotocolÜzenet.checksum = 0

		internetprotocolÜzenet.Halmazbuffer(buffer_2)
		internetprotocolÜzenet.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetKeretpayload)), uint32(4*internetprotocolÜzenet.headerHossz))

		internetprotocolÜzenet.Halmazbuffer(buffer_2)

	}

	ipKonzol.MNyomtatás(([]byte)("ipmessage"))
	ipKonzol.MUnsignedinteger32Nyomtatás(internetprotocolÜzenet.forrásipaddress)
	ipKonzol.MNyomtatás(([]byte)(":"))
	ipKonzol.MUnsignedinteger32Nyomtatás(internetprotocolÜzenet.célipaddress)
	ipKonzol.MNyomtatás(([]byte)(":"))
	ipKonzol.MUnsignedinteger16Nyomtatás(uint16(internetprotocolÜzenet.headerHossz))
	ipKonzol.MNyomtatás(([]byte)(":"))
	ipKonzol.MUnsignedinteger16Nyomtatás(uint16(internetprotocolÜzenet.verzió))
	ipKonzol.MNyomtatás(([]byte)(":"))
	ipKonzol.MUnsignedinteger16Nyomtatás(internetprotocolÜzenet.összesenHossz)
	ipKonzol.MNyomtatás(([]byte)(":"))
	ipKonzol.MUnsignedinteger32Nyomtatás(uint32(efhandler.Getipaddress()))
	ipKonzol.MNyomtatás(([]byte)(":"))
	ipKonzol.MNyomtatás(([]byte)("\n"))

	return reply

}
func (self *TInternetprotocolprovider) Küldés(célipaddressHálózatbyteorder uint32, protocol uint8, dataMutató uintptr, méret uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Üzenetbuffer = (*TInternetprotocolv4Üzenetbuffer)(Pointer(&buffer1_2))
	var üzenet TInternetprotocolv4Üzenet = TInternetprotocolv4Üzenet{}
	üzenet.verzió = 4
	üzenet.headerHossz = ipMéret / 4
	üzenet.tos = 0
	üzenet.összesenHossz = Unsignedinteger16r(uint16(méret + uint32(ipMéret)))

	üzenet.ident = 0x0100
	üzenet.flagekÉSEltolás = 0x0040
	üzenet.időtolive = 0x40
	üzenet.protocol = protocol

	üzenet.célipaddress = célipaddressHálózatbyteorder

	üzenet.forrásipaddress = uint32(efhandler.Getipaddress())

	üzenet.checksum = 0

	üzenet.Halmazbuffer(buffer_2)
	üzenet.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipMéret))
	üzenet.Halmazbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataMutató))

	for i := 0; i < int(méret); i++ {

		buffer1_2[i+int(ipMéret)] = databuffer_2[i]
	}

	ipKonzol.MNyomtatásxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(méret)+int(ipMéret); i++ {
		ipKonzol.MHexadecimalNyomtatás(buffer1_2[i])
	}
	ipKonzol.MNyomtatás(([]byte)(":"))
	ipKonzol.MNyomtatás(([]byte)("]\n"))

	var következőhopipaddressHálózatbyteorder uint32 = célipaddressHálózatbyteorder
	if (célipaddressHálózatbyteorder & self.SubnetMaszk) != (üzenet.forrásipaddress & self.SubnetMaszk) {
		következőhopipaddressHálózatbyteorder = self.Átjáróip
	}

	var küldésdataMutató = uintptr(Pointer(&buffer1_2))
	ipKonzol.MUnsignedinteger32Nyomtatás(következőhopipaddressHálózatbyteorder)

	var ethernetTípusbe = Unsignedinteger16r(0x0800)
	efhandler.KeretKüldés(self.arpprovider.Resolve(következőhopipaddressHálózatbyteorder), ethernetTípusbe, küldésdataMutató, uint32(ipMéret)+uint32(méret))

}
func (self *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, hosszBeBájt uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBájt [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (hosszBeBájt % 2) != 0 {
		temporary += uint32(uint16(dataBájt[hosszBeBájt-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
