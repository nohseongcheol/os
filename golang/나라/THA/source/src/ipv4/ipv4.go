/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetเฟรม"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4messagebuffer struct {
	lenver		byte
	tos		byte
	รวมความยาว	[2]byte

	ident		[2]byte
	flagsและoffset	[2]byte

	เวลาtolive	byte
	protocol	byte
	checksum	[2]byte

	sourceipaddress		[4]byte
	ปลายทางipaddress	[4]byte
}

var ipขนาด uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4message struct {
	headerความยาว	uint8
	version		uint8
	tos		uint8
	รวมความยาว	uint16

	ident		uint16
	flagsและoffset	uint16

	เวลาtolive	uint8
	protocol	uint8
	checksum	uint16

	sourceipaddress		uint32
	ปลายทางipaddress	uint32
}

func (self *TInternetprotocolv4message) Init(buffer_2 TInternetprotocolv4messagebuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerความยาว = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.รวมความยาว = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.รวมความยาว))

	self.ident = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ident))
	self.flagsและoffset = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.flagsและoffset))

	self.เวลาtolive = buffer_2.เวลาtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))

	self.sourceipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.sourceipaddress))
	self.ปลายทางipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.ปลายทางipaddress))

}
func (self *TInternetprotocolv4message) Sกำหนดbuffer(buffer_2 *TInternetprotocolv4messagebuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerความยาว & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.รวมความยาว = Unsignedinteger16toarray(self.รวมความยาว)

	buffer_2.ident = Unsignedinteger16toarray(self.ident)
	buffer_2.flagsและoffset = Unsignedinteger16toarray(self.flagsและoffset)

	buffer_2.เวลาtolive = self.เวลาtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

	buffer_2.sourceipaddress = Unsignedinteger32toarray(self.sourceipaddress)
	buffer_2.ปลายทางipaddress = Unsignedinteger32toarray(self.ปลายทางipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(sourceipaddressnetworkbyteorder uint32, ปลายทางipaddressnetworkbyteorder uint32, datapointer uintptr, ขนาด uint32) bool
	Send(ปลายทางipaddressnetworkbyteorder uint32, pprotocol uint8, datapointer uintptr, ขนาด uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetเฟรมhandler Ipethernetเฟรมhandler = Ipethernetเฟรมhandler{}
var protocol uint8

func (self *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(sourceipaddressnetworkbyteorder uint32, ปลายทางipaddressnetworkbyteorder uint32, datapointer uintptr, ขนาด uint32) bool {
	ipconsole.MPrint(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Send(ปลายทางipaddressnetworkbyteorder uint32, pprotocol uint8, datapointer uintptr, ขนาด uint32) {

	ipprovider.Send(ปลายทางipaddressnetworkbyteorder, pprotocol, datapointer, ขนาด)
}
func (self *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type Ipethernetเฟรมhandler struct {
	TEthernetเฟรมhandler
}

var ipprovider TInternetprotocolprovider

func (self *Ipethernetเฟรมhandler) Ethernetเฟรมreceivewhen(datapointer uintptr, ขนาด int) bool {
	ipconsole.MPrint(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Ethernetเฟรมreceivewhen(datapointer, uint32(ขนาด))

}

func (self *Ipethernetเฟรมhandler) Send(ปลายทางipaddressnetworkbyteorder uint64, datapointer uintptr, ขนาด uint32) {
	ipconsole.MPrint(([]byte)("ipefhandler:send\n"))
	var ethernetประเภทbe = Unsignedinteger16r(0x0800)
	self.TEthernetเฟรมhandler.Sเฟรมsend(ปลายทางipaddressnetworkbyteorder, ethernetประเภทbe, datapointer, ขนาด)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetเฟรมhandler

func (self *TInternetprotocolprovider) Init(pefprovider TEthernetเฟรมprovider, pefhandler IEthernetเฟรมhandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Sกำหนดhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnetmask = subnetmask
	ipprovider = *self
}
func (self *TInternetprotocolprovider) Ethernetเฟรมreceivewhen(ethernetเฟรมpayload uintptr, ขนาด uint32) bool {
	if ขนาด < uint32(ipขนาด) {
		return false
	}

	var buffer_2 *TInternetprotocolv4messagebuffer = (*TInternetprotocolv4messagebuffer)(Pointer(ethernetเฟรมpayload))
	var internetprotocolmessage TInternetprotocolv4message
	internetprotocolmessage.Init(*buffer_2)

	var reply bool = false

	if internetprotocolmessage.ปลายทางipaddress == uint32(efhandler.Getipaddress()) {

		var ความยาว uint32 = uint32(internetprotocolmessage.รวมความยาว)
		if ความยาว > ขนาด {
			ความยาว = ขนาด
		}
		if handler_2[internetprotocolmessage.protocol] != nil {
			reply = handler_2[internetprotocolmessage.protocol].Internetprotocolreceivewhen(internetprotocolmessage.sourceipaddress, internetprotocolmessage.ปลายทางipaddress, ethernetเฟรมpayload+uintptr(4*internetprotocolmessage.headerความยาว), uint32(ความยาว-uint32(4*internetprotocolmessage.headerความยาว)))

		}
	}

	if reply {

		var temporary = internetprotocolmessage.ปลายทางipaddress
		internetprotocolmessage.ปลายทางipaddress = internetprotocolmessage.sourceipaddress
		internetprotocolmessage.sourceipaddress = temporary

		internetprotocolmessage.เวลาtolive = 0x40
		internetprotocolmessage.checksum = 0

		internetprotocolmessage.Sกำหนดbuffer(buffer_2)
		internetprotocolmessage.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetเฟรมpayload)), uint32(4*internetprotocolmessage.headerความยาว))

		internetprotocolmessage.Sกำหนดbuffer(buffer_2)

	}

	ipconsole.MPrint(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32print(internetprotocolmessage.sourceipaddress)
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger32print(internetprotocolmessage.ปลายทางipaddress)
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger16print(uint16(internetprotocolmessage.headerความยาว))
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger16print(uint16(internetprotocolmessage.version))
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger16print(internetprotocolmessage.รวมความยาว)
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger32print(uint32(efhandler.Getipaddress()))
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MPrint(([]byte)("\n"))

	return reply

}
func (self *TInternetprotocolprovider) Send(ปลายทางipaddressnetworkbyteorder uint32, protocol uint8, datapointer uintptr, ขนาด uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4messagebuffer = (*TInternetprotocolv4messagebuffer)(Pointer(&buffer1_2))
	var message TInternetprotocolv4message = TInternetprotocolv4message{}
	message.version = 4
	message.headerความยาว = ipขนาด / 4
	message.tos = 0
	message.รวมความยาว = Unsignedinteger16r(uint16(ขนาด + uint32(ipขนาด)))

	message.ident = 0x0100
	message.flagsและoffset = 0x0040
	message.เวลาtolive = 0x40
	message.protocol = protocol

	message.ปลายทางipaddress = ปลายทางipaddressnetworkbyteorder

	message.sourceipaddress = uint32(efhandler.Getipaddress())

	message.checksum = 0

	message.Sกำหนดbuffer(buffer_2)
	message.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipขนาด))
	message.Sกำหนดbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(ขนาด); i++ {

		buffer1_2[i+int(ipขนาด)] = databuffer_2[i]
	}

	ipconsole.MPrintxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(ขนาด)+int(ipขนาด); i++ {
		ipconsole.MHexadecimalprint(buffer1_2[i])
	}
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MPrint(([]byte)("]\n"))

	var nexthopipaddressnetworkbyteorder uint32 = ปลายทางipaddressnetworkbyteorder
	if (ปลายทางipaddressnetworkbyteorder & self.Subnetmask) != (message.sourceipaddress & self.Subnetmask) {
		nexthopipaddressnetworkbyteorder = self.Gatewayip
	}

	var senddatapointer = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32print(nexthopipaddressnetworkbyteorder)

	var ethernetประเภทbe = Unsignedinteger16r(0x0800)
	efhandler.Sเฟรมsend(self.arpprovider.Resolve(nexthopipaddressnetworkbyteorder), ethernetประเภทbe, senddatapointer, uint32(ipขนาด)+uint32(ขนาด))

}
func (self *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, ความยาวขยายbytes uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var databytes [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (ความยาวขยายbytes % 2) != 0 {
		temporary += uint32(uint16(databytes[ความยาวขยายbytes-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
