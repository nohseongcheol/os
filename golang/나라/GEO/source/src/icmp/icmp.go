/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "მეხსიერებაmanager"
import . "ethernetframe"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინებაbuffer struct {
	Tტიპი	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpზომა int = 64

type Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინება struct {
	Tტიპი	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინება) Init(buffer_2 Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინებაbuffer) {
	self.Tტიპი = buffer_2.Tტიპი
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Aმასივიtounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer_2.data))
}

func (self *Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინება) Setbuffer(buffer_2 *Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინებაbuffer) {
	buffer_2.Tტიპი = self.Tტიპი
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toმასივი(self.checksum)
	buffer_2.data = Unsignedinteger32toმასივი(self.data)
}

type Icmphandler struct {
	Tინტერნეტიprotocolhandler
}

var icmp *Tინტერნეტიcontrolშეტყობინებაprotocol

func (self *Icmphandler) Oინტერნეტიprotocolreceivewhen(წყაროipaddressქსელიbyteorder uint32, destinationipaddressქსელიbyteorder uint32, dataკურსორი uintptr, ზომა uint32) bool {
	return icmp.Oინტერნეტიprotocolreceivewhen(წყაროipaddressქსელიbyteorder, destinationipaddressქსელიbyteorder, dataკურსორი, ზომა)
}

var iphandler Iინტერნეტიprotocolhandler

type Tინტერნეტიcontrolშეტყობინებაprotocol struct {
}

func (self *Tინტერნეტიcontrolშეტყობინებაprotocol) Init(backend Tინტერნეტიprotocolprovider, handler Iინტერნეტიprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *Tინტერნეტიcontrolშეტყობინებაprotocol) Oინტერნეტიprotocolreceivewhen(წყაროipaddressქსელიbyteorder uint32, destinationipaddressქსელიbyteorder uint32, dataკურსორი uintptr, ზომა uint32) bool {
	if ზომა < uint32(icmpზომა) {
		return false
	}

	var buffer_2 *Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინებაbuffer = (*Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინებაbuffer)(Pointer(dataკურსორი))
	var msg Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინება = Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინება{}
	msg.Init(*buffer_2)

	icmpconsole.Mბეჭდვა(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16ბეჭდვა(uint16(msg.Tტიპი))
	icmpconsole.Mბეჭდვა(([]byte)(":"))

	switch msg.Tტიპი {
	case 0:
		icmpconsole.Mბეჭდვა(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.Mბეჭდვა(([]byte)("ping send "))
		msg.Tტიპი = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataკურსორი)), uint32(icmpზომა))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *Tინტერნეტიcontrolშეტყობინებაprotocol) Echorequestგაგზავნა(ipქსელიbyteorder uint32) bool {
	var icmp Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინება = Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინება{}

	var მეხსიერებაmanager = &Tმეხსიერებაmanager{}
	var buffer_2 = (*Tინტერნეტიcontrolშეტყობინებაprotocolშეტყობინებაbuffer)(მეხსიერებაmanager.Malloc(1024))

	icmp.Tტიპი = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpზომა))
	icmp.Setbuffer(buffer_2)

	var dataკურსორი uintptr = uintptr(Pointer(buffer_2))
	iphandler.Sგაგზავნა(ipქსელიbyteorder, 0x01, dataკურსორი, uint32(icmpზომა))

	return false

}
