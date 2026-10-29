/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetframe"
import . "arp"

var ipconsole TConsole = TConsole{}

type Tინტერნეტიprotocolv4შეტყობინებაbuffer struct {
	lenver		byte
	tos		byte
	სულlength	[2]byte

	ident		[2]byte
	ალმებიandoffset	[2]byte

	დროtolive	byte
	protocol	byte
	checksum	[2]byte

	წყაროipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipზომა uint8 = (4 + 4 + 4 + 8)

type Tინტერნეტიprotocolv4შეტყობინება struct {
	headerlength	uint8
	version		uint8
	tos		uint8
	სულlength	uint16

	ident		uint16
	ალმებიandoffset	uint16

	დროtolive	uint8
	protocol	uint8
	checksum	uint16

	წყაროipaddress		uint32
	destinationipaddress	uint32
}

func (self *Tინტერნეტიprotocolv4შეტყობინება) Init(buffer_2 Tინტერნეტიprotocolv4შეტყობინებაbuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerlength = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.სულlength = Unsignedinteger16r(Aმასივიtounsignedinteger16(buffer_2.სულlength))

	self.ident = Unsignedinteger16r(Aმასივიtounsignedinteger16(buffer_2.ident))
	self.ალმებიandoffset = Unsignedinteger16r(Aმასივიtounsignedinteger16(buffer_2.ალმებიandoffset))

	self.დროtolive = buffer_2.დროtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Aმასივიtounsignedinteger16(buffer_2.checksum))

	self.წყაროipaddress = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer_2.წყაროipaddress))
	self.destinationipaddress = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *Tინტერნეტიprotocolv4შეტყობინება) Setbuffer(buffer_2 *Tინტერნეტიprotocolv4შეტყობინებაbuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerlength & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.სულlength = Unsignedinteger16toმასივი(self.სულlength)

	buffer_2.ident = Unsignedinteger16toმასივი(self.ident)
	buffer_2.ალმებიandoffset = Unsignedinteger16toმასივი(self.ალმებიandoffset)

	buffer_2.დროtolive = self.დროtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toმასივი(self.checksum)

	buffer_2.წყაროipaddress = Unsignedinteger32toმასივი(self.წყაროipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toმასივი(self.destinationipaddress)

}

type Iინტერნეტიprotocolhandler interface {
	Init(backend Tინტერნეტიprotocolprovider, pihandler Iინტერნეტიprotocolhandler, pprotocol uint8)
	Oინტერნეტიprotocolreceivewhen(წყაროipaddressქსელიbyteorder uint32, destinationipaddressქსელიbyteorder uint32, dataკურსორი uintptr, ზომა uint32) bool
	Sგაგზავნა(destinationipaddressქსელიbyteorder uint32, pprotocol uint8, dataკურსორი uintptr, ზომა uint32)
	Providerget() *Tინტერნეტიprotocolprovider
}

type Tინტერნეტიprotocolhandler struct {
}

var ipethernetframehandler Ipethernetframehandler = Ipethernetframehandler{}
var protocol uint8

func (self *Tინტერნეტიprotocolhandler) Init(backend Tინტერნეტიprotocolprovider, pihandler Iინტერნეტიprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *Tინტერნეტიprotocolhandler) Oინტერნეტიprotocolreceivewhen(წყაროipaddressქსელიbyteorder uint32, destinationipaddressქსელიbyteorder uint32, dataკურსორი uintptr, ზომა uint32) bool {
	ipconsole.Mბეჭდვა(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *Tინტერნეტიprotocolhandler) Sგაგზავნა(destinationipaddressქსელიbyteorder uint32, pprotocol uint8, dataკურსორი uintptr, ზომა uint32) {

	ipprovider.Sგაგზავნა(destinationipaddressქსელიbyteorder, pprotocol, dataკურსორი, ზომა)
}
func (self *Tინტერნეტიprotocolhandler) Providerget() *Tინტერნეტიprotocolprovider {
	return &ipprovider
}

type Ipethernetframehandler struct {
	TEthernetframehandler
}

var ipprovider Tინტერნეტიprotocolprovider

func (self *Ipethernetframehandler) Ethernetframereceivewhen(dataკურსორი uintptr, ზომა int) bool {
	ipconsole.Mბეჭდვა(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Ethernetframereceivewhen(dataკურსორი, uint32(ზომა))

}

func (self *Ipethernetframehandler) Sგაგზავნა(destinationipaddressქსელიbyteorder uint64, dataკურსორი uintptr, ზომა uint32) {
	ipconsole.Mბეჭდვა(([]byte)("ipefhandler:send\n"))
	var ethernetტიპიbe = Unsignedinteger16r(0x0800)
	self.TEthernetframehandler.Frameგაგზავნა(destinationipaddressქსელიbyteorder, ethernetტიპიbe, dataკურსორი, ზომა)

}

var handler_2 [255]Iინტერნეტიprotocolhandler

type Tინტერნეტიprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetframehandler

func (self *Tინტერნეტიprotocolprovider) Init(pefprovider TEthernetframeprovider, pefhandler IEthernetframehandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

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
func (self *Tინტერნეტიprotocolprovider) Ethernetframereceivewhen(ethernetframepayload uintptr, ზომა uint32) bool {
	if ზომა < uint32(ipზომა) {
		return false
	}

	var buffer_2 *Tინტერნეტიprotocolv4შეტყობინებაbuffer = (*Tინტერნეტიprotocolv4შეტყობინებაbuffer)(Pointer(ethernetframepayload))
	var ინტერნეტიprotocolშეტყობინება Tინტერნეტიprotocolv4შეტყობინება
	ინტერნეტიprotocolშეტყობინება.Init(*buffer_2)

	var reply bool = false

	if ინტერნეტიprotocolშეტყობინება.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var length uint32 = uint32(ინტერნეტიprotocolშეტყობინება.სულlength)
		if length > ზომა {
			length = ზომა
		}
		if handler_2[ინტერნეტიprotocolშეტყობინება.protocol] != nil {
			reply = handler_2[ინტერნეტიprotocolშეტყობინება.protocol].Oინტერნეტიprotocolreceivewhen(ინტერნეტიprotocolშეტყობინება.წყაროipaddress, ინტერნეტიprotocolშეტყობინება.destinationipaddress, ethernetframepayload+uintptr(4*ინტერნეტიprotocolშეტყობინება.headerlength), uint32(length-uint32(4*ინტერნეტიprotocolშეტყობინება.headerlength)))

		}
	}

	if reply {

		var temporary = ინტერნეტიprotocolშეტყობინება.destinationipaddress
		ინტერნეტიprotocolშეტყობინება.destinationipaddress = ინტერნეტიprotocolშეტყობინება.წყაროipaddress
		ინტერნეტიprotocolშეტყობინება.წყაროipaddress = temporary

		ინტერნეტიprotocolშეტყობინება.დროtolive = 0x40
		ინტერნეტიprotocolშეტყობინება.checksum = 0

		ინტერნეტიprotocolშეტყობინება.Setbuffer(buffer_2)
		ინტერნეტიprotocolშეტყობინება.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetframepayload)), uint32(4*ინტერნეტიprotocolშეტყობინება.headerlength))

		ინტერნეტიprotocolშეტყობინება.Setbuffer(buffer_2)

	}

	ipconsole.Mბეჭდვა(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32ბეჭდვა(ინტერნეტიprotocolშეტყობინება.წყაროipaddress)
	ipconsole.Mბეჭდვა(([]byte)(":"))
	ipconsole.MUnsignedinteger32ბეჭდვა(ინტერნეტიprotocolშეტყობინება.destinationipaddress)
	ipconsole.Mბეჭდვა(([]byte)(":"))
	ipconsole.MUnsignedinteger16ბეჭდვა(uint16(ინტერნეტიprotocolშეტყობინება.headerlength))
	ipconsole.Mბეჭდვა(([]byte)(":"))
	ipconsole.MUnsignedinteger16ბეჭდვა(uint16(ინტერნეტიprotocolშეტყობინება.version))
	ipconsole.Mბეჭდვა(([]byte)(":"))
	ipconsole.MUnsignedinteger16ბეჭდვა(ინტერნეტიprotocolშეტყობინება.სულlength)
	ipconsole.Mბეჭდვა(([]byte)(":"))
	ipconsole.MUnsignedinteger32ბეჭდვა(uint32(efhandler.Getipaddress()))
	ipconsole.Mბეჭდვა(([]byte)(":"))
	ipconsole.Mბეჭდვა(([]byte)("\n"))

	return reply

}
func (self *Tინტერნეტიprotocolprovider) Sგაგზავნა(destinationipaddressქსელიbyteorder uint32, protocol uint8, dataკურსორი uintptr, ზომა uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tინტერნეტიprotocolv4შეტყობინებაbuffer = (*Tინტერნეტიprotocolv4შეტყობინებაbuffer)(Pointer(&buffer1_2))
	var შეტყობინება Tინტერნეტიprotocolv4შეტყობინება = Tინტერნეტიprotocolv4შეტყობინება{}
	შეტყობინება.version = 4
	შეტყობინება.headerlength = ipზომა / 4
	შეტყობინება.tos = 0
	შეტყობინება.სულlength = Unsignedinteger16r(uint16(ზომა + uint32(ipზომა)))

	შეტყობინება.ident = 0x0100
	შეტყობინება.ალმებიandoffset = 0x0040
	შეტყობინება.დროtolive = 0x40
	შეტყობინება.protocol = protocol

	შეტყობინება.destinationipaddress = destinationipaddressქსელიbyteorder

	შეტყობინება.წყაროipaddress = uint32(efhandler.Getipaddress())

	შეტყობინება.checksum = 0

	შეტყობინება.Setbuffer(buffer_2)
	შეტყობინება.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipზომა))
	შეტყობინება.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataკურსორი))

	for i := 0; i < int(ზომა); i++ {

		buffer1_2[i+int(ipზომა)] = databuffer_2[i]
	}

	ipconsole.Mბეჭდვაxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(ზომა)+int(ipზომა); i++ {
		ipconsole.MHexadecimalბეჭდვა(buffer1_2[i])
	}
	ipconsole.Mბეჭდვა(([]byte)(":"))
	ipconsole.Mბეჭდვა(([]byte)("]\n"))

	var შემდეგიhopipaddressქსელიbyteorder uint32 = destinationipaddressქსელიbyteorder
	if (destinationipaddressქსელიbyteorder & self.Subnetmask) != (შეტყობინება.წყაროipaddress & self.Subnetmask) {
		შემდეგიhopipaddressქსელიbyteorder = self.Gatewayip
	}

	var გაგზავნაdataკურსორი = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32ბეჭდვა(შემდეგიhopipaddressქსელიbyteorder)

	var ethernetტიპიbe = Unsignedinteger16r(0x0800)
	efhandler.Frameგაგზავნა(self.arpprovider.Resolve(შემდეგიhopipaddressქსელიbyteorder), ethernetტიპიbe, გაგზავნაdataკურსორი, uint32(ipზომა)+uint32(ზომა))

}
func (self *Tინტერნეტიprotocolprovider) Checksum(pdata *[4096]uint16, lengthგადიდებაბაიტი uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataბაიტი [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengthგადიდებაბაიტი % 2) != 0 {
		temporary += uint32(uint16(dataბაიტი[lengthგადიდებაბაიტი-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *Tინტერნეტიprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
