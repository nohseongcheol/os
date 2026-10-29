/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetክፈፍ"
import . "arp"

var ipconsole TConsole = TConsole{}

type Tኢንተርኔትprotocolv4መልእክትbuffer struct {
	lenver		byte
	tos		byte
	ጠቅላላእርዝመት	[2]byte

	ident		[2]byte
	ባንዲራዎችandoffset	[2]byte

	ሰዓትtolive	byte
	protocol	byte
	checksum	[2]byte

	ምንጩipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipመጠን uint8 = (4 + 4 + 4 + 8)

type Tኢንተርኔትprotocolv4መልእክት struct {
	headerእርዝመት	uint8
	እትም		uint8
	tos		uint8
	ጠቅላላእርዝመት	uint16

	ident		uint16
	ባንዲራዎችandoffset	uint16

	ሰዓትtolive	uint8
	protocol	uint8
	checksum	uint16

	ምንጩipaddress		uint32
	destinationipaddress	uint32
}

func (self *Tኢንተርኔትprotocolv4መልእክት) Init(buffer_2 Tኢንተርኔትprotocolv4መልእክትbuffer) {

	self.እትም = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerእርዝመት = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.ጠቅላላእርዝመት = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer_2.ጠቅላላእርዝመት))

	self.ident = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer_2.ident))
	self.ባንዲራዎችandoffset = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer_2.ባንዲራዎችandoffset))

	self.ሰዓትtolive = buffer_2.ሰዓትtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer_2.checksum))

	self.ምንጩipaddress = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer_2.ምንጩipaddress))
	self.destinationipaddress = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *Tኢንተርኔትprotocolv4መልእክት) Setbuffer(buffer_2 *Tኢንተርኔትprotocolv4መልእክትbuffer) {

	buffer_2.lenver = byte(((self.እትም & 0x0F) << 4) | (self.headerእርዝመት & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.ጠቅላላእርዝመት = Unsignedinteger16toማዘጋጃ(self.ጠቅላላእርዝመት)

	buffer_2.ident = Unsignedinteger16toማዘጋጃ(self.ident)
	buffer_2.ባንዲራዎችandoffset = Unsignedinteger16toማዘጋጃ(self.ባንዲራዎችandoffset)

	buffer_2.ሰዓትtolive = self.ሰዓትtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toማዘጋጃ(self.checksum)

	buffer_2.ምንጩipaddress = Unsignedinteger32toማዘጋጃ(self.ምንጩipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toማዘጋጃ(self.destinationipaddress)

}

type Iኢንተርኔትprotocolhandler interface {
	Init(backend Tኢንተርኔትprotocolprovider, pihandler Iኢንተርኔትprotocolhandler, pprotocol uint8)
	Oኢንተርኔትprotocolreceivewhen(ምንጩipaddressኔትዎርክbyteorder uint32, destinationipaddressኔትዎርክbyteorder uint32, dataጠቋሚ uintptr, መጠን uint32) bool
	Send(destinationipaddressኔትዎርክbyteorder uint32, pprotocol uint8, dataጠቋሚ uintptr, መጠን uint32)
	Providerget() *Tኢንተርኔትprotocolprovider
}

type Tኢንተርኔትprotocolhandler struct {
}

var ipethernetክፈፍhandler Ipethernetክፈፍhandler = Ipethernetክፈፍhandler{}
var protocol uint8

func (self *Tኢንተርኔትprotocolhandler) Init(backend Tኢንተርኔትprotocolprovider, pihandler Iኢንተርኔትprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *Tኢንተርኔትprotocolhandler) Oኢንተርኔትprotocolreceivewhen(ምንጩipaddressኔትዎርክbyteorder uint32, destinationipaddressኔትዎርክbyteorder uint32, dataጠቋሚ uintptr, መጠን uint32) bool {
	ipconsole.Mማተሚያ(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *Tኢንተርኔትprotocolhandler) Send(destinationipaddressኔትዎርክbyteorder uint32, pprotocol uint8, dataጠቋሚ uintptr, መጠን uint32) {

	ipprovider.Send(destinationipaddressኔትዎርክbyteorder, pprotocol, dataጠቋሚ, መጠን)
}
func (self *Tኢንተርኔትprotocolhandler) Providerget() *Tኢንተርኔትprotocolprovider {
	return &ipprovider
}

type Ipethernetክፈፍhandler struct {
	TEthernetክፈፍhandler
}

var ipprovider Tኢንተርኔትprotocolprovider

func (self *Ipethernetክፈፍhandler) Ethernetክፈፍreceivewhen(dataጠቋሚ uintptr, መጠን int) bool {
	ipconsole.Mማተሚያ(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Ethernetክፈፍreceivewhen(dataጠቋሚ, uint32(መጠን))

}

func (self *Ipethernetክፈፍhandler) Send(destinationipaddressኔትዎርክbyteorder uint64, dataጠቋሚ uintptr, መጠን uint32) {
	ipconsole.Mማተሚያ(([]byte)("ipefhandler:send\n"))
	var ethernetአይነትbe = Unsignedinteger16r(0x0800)
	self.TEthernetክፈፍhandler.Sክፈፍsend(destinationipaddressኔትዎርክbyteorder, ethernetአይነትbe, dataጠቋሚ, መጠን)

}

var handler_2 [255]Iኢንተርኔትprotocolhandler

type Tኢንተርኔትprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetክፈፍhandler

func (self *Tኢንተርኔትprotocolprovider) Init(pefprovider TEthernetክፈፍprovider, pefhandler IEthernetክፈፍhandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

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
func (self *Tኢንተርኔትprotocolprovider) Ethernetክፈፍreceivewhen(ethernetክፈፍpayload uintptr, መጠን uint32) bool {
	if መጠን < uint32(ipመጠን) {
		return false
	}

	var buffer_2 *Tኢንተርኔትprotocolv4መልእክትbuffer = (*Tኢንተርኔትprotocolv4መልእክትbuffer)(Pointer(ethernetክፈፍpayload))
	var ኢንተርኔትprotocolመልእክት Tኢንተርኔትprotocolv4መልእክት
	ኢንተርኔትprotocolመልእክት.Init(*buffer_2)

	var reply bool = false

	if ኢንተርኔትprotocolመልእክት.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var እርዝመት_2 uint32 = uint32(ኢንተርኔትprotocolመልእክት.ጠቅላላእርዝመት)
		if እርዝመት_2 > መጠን {
			እርዝመት_2 = መጠን
		}
		if handler_2[ኢንተርኔትprotocolመልእክት.protocol] != nil {
			reply = handler_2[ኢንተርኔትprotocolመልእክት.protocol].Oኢንተርኔትprotocolreceivewhen(ኢንተርኔትprotocolመልእክት.ምንጩipaddress, ኢንተርኔትprotocolመልእክት.destinationipaddress, ethernetክፈፍpayload+uintptr(4*ኢንተርኔትprotocolመልእክት.headerእርዝመት), uint32(እርዝመት_2-uint32(4*ኢንተርኔትprotocolመልእክት.headerእርዝመት)))

		}
	}

	if reply {

		var temporary = ኢንተርኔትprotocolመልእክት.destinationipaddress
		ኢንተርኔትprotocolመልእክት.destinationipaddress = ኢንተርኔትprotocolመልእክት.ምንጩipaddress
		ኢንተርኔትprotocolመልእክት.ምንጩipaddress = temporary

		ኢንተርኔትprotocolመልእክት.ሰዓትtolive = 0x40
		ኢንተርኔትprotocolመልእክት.checksum = 0

		ኢንተርኔትprotocolመልእክት.Setbuffer(buffer_2)
		ኢንተርኔትprotocolመልእክት.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetክፈፍpayload)), uint32(4*ኢንተርኔትprotocolመልእክት.headerእርዝመት))

		ኢንተርኔትprotocolመልእክት.Setbuffer(buffer_2)

	}

	ipconsole.Mማተሚያ(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32ማተሚያ(ኢንተርኔትprotocolመልእክት.ምንጩipaddress)
	ipconsole.Mማተሚያ(([]byte)(":"))
	ipconsole.MUnsignedinteger32ማተሚያ(ኢንተርኔትprotocolመልእክት.destinationipaddress)
	ipconsole.Mማተሚያ(([]byte)(":"))
	ipconsole.MUnsignedinteger16ማተሚያ(uint16(ኢንተርኔትprotocolመልእክት.headerእርዝመት))
	ipconsole.Mማተሚያ(([]byte)(":"))
	ipconsole.MUnsignedinteger16ማተሚያ(uint16(ኢንተርኔትprotocolመልእክት.እትም))
	ipconsole.Mማተሚያ(([]byte)(":"))
	ipconsole.MUnsignedinteger16ማተሚያ(ኢንተርኔትprotocolመልእክት.ጠቅላላእርዝመት)
	ipconsole.Mማተሚያ(([]byte)(":"))
	ipconsole.MUnsignedinteger32ማተሚያ(uint32(efhandler.Getipaddress()))
	ipconsole.Mማተሚያ(([]byte)(":"))
	ipconsole.Mማተሚያ(([]byte)("\n"))

	return reply

}
func (self *Tኢንተርኔትprotocolprovider) Send(destinationipaddressኔትዎርክbyteorder uint32, protocol uint8, dataጠቋሚ uintptr, መጠን uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tኢንተርኔትprotocolv4መልእክትbuffer = (*Tኢንተርኔትprotocolv4መልእክትbuffer)(Pointer(&buffer1_2))
	var መልእክት Tኢንተርኔትprotocolv4መልእክት = Tኢንተርኔትprotocolv4መልእክት{}
	መልእክት.እትም = 4
	መልእክት.headerእርዝመት = ipመጠን / 4
	መልእክት.tos = 0
	መልእክት.ጠቅላላእርዝመት = Unsignedinteger16r(uint16(መጠን + uint32(ipመጠን)))

	መልእክት.ident = 0x0100
	መልእክት.ባንዲራዎችandoffset = 0x0040
	መልእክት.ሰዓትtolive = 0x40
	መልእክት.protocol = protocol

	መልእክት.destinationipaddress = destinationipaddressኔትዎርክbyteorder

	መልእክት.ምንጩipaddress = uint32(efhandler.Getipaddress())

	መልእክት.checksum = 0

	መልእክት.Setbuffer(buffer_2)
	መልእክት.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipመጠን))
	መልእክት.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataጠቋሚ))

	for i := 0; i < int(መጠን); i++ {

		buffer1_2[i+int(ipመጠን)] = databuffer_2[i]
	}

	ipconsole.Mማተሚያxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(መጠን)+int(ipመጠን); i++ {
		ipconsole.MHexadecimalማተሚያ(buffer1_2[i])
	}
	ipconsole.Mማተሚያ(([]byte)(":"))
	ipconsole.Mማተሚያ(([]byte)("]\n"))

	var የሚቀጥለውhopipaddressኔትዎርክbyteorder uint32 = destinationipaddressኔትዎርክbyteorder
	if (destinationipaddressኔትዎርክbyteorder & self.Subnetmask) != (መልእክት.ምንጩipaddress & self.Subnetmask) {
		የሚቀጥለውhopipaddressኔትዎርክbyteorder = self.Gatewayip
	}

	var senddataጠቋሚ = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32ማተሚያ(የሚቀጥለውhopipaddressኔትዎርክbyteorder)

	var ethernetአይነትbe = Unsignedinteger16r(0x0800)
	efhandler.Sክፈፍsend(self.arpprovider.Resolve(የሚቀጥለውhopipaddressኔትዎርክbyteorder), ethernetአይነትbe, senddataጠቋሚ, uint32(ipመጠን)+uint32(መጠን))

}
func (self *Tኢንተርኔትprotocolprovider) Checksum(pdata *[4096]uint16, እርዝመትውስጥባይትስ uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataባይትስ [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (እርዝመትውስጥባይትስ % 2) != 0 {
		temporary += uint32(uint16(dataባይትስ[እርዝመትውስጥባይትስ-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *Tኢንተርኔትprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
