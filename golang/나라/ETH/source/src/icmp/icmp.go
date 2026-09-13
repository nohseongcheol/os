package icmp

import . "unsafe"
import . "console"
import . "ማስታወሻmanager"
import . "ethernetክፈፍ"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type Tኢንተርኔትcontrolመልእክትprotocolመልእክትbuffer struct {
	Tአይነት	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpመጠን int = 64

type Tኢንተርኔትcontrolመልእክትprotocolመልእክት struct {
	Tአይነት	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *Tኢንተርኔትcontrolመልእክትprotocolመልእክት) Init(buffer_2 Tኢንተርኔትcontrolመልእክትprotocolመልእክትbuffer) {
	self.Tአይነት = buffer_2.Tአይነት
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer_2.data))
}

func (self *Tኢንተርኔትcontrolመልእክትprotocolመልእክት) Setbuffer(buffer_2 *Tኢንተርኔትcontrolመልእክትprotocolመልእክትbuffer) {
	buffer_2.Tአይነት = self.Tአይነት
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toማዘጋጃ(self.checksum)
	buffer_2.data = Unsignedinteger32toማዘጋጃ(self.data)
}

type Icmphandler struct {
	Tኢንተርኔትprotocolhandler
}

var icmp *Tኢንተርኔትcontrolመልእክትprotocol

func (self *Icmphandler) Oኢንተርኔትprotocolreceivewhen(ምንጩipaddressኔትዎርክbyteorder uint32, destinationipaddressኔትዎርክbyteorder uint32, dataጠቋሚ uintptr, መጠን uint32) bool {
	return icmp.Oኢንተርኔትprotocolreceivewhen(ምንጩipaddressኔትዎርክbyteorder, destinationipaddressኔትዎርክbyteorder, dataጠቋሚ, መጠን)
}

var iphandler Iኢንተርኔትprotocolhandler

type Tኢንተርኔትcontrolመልእክትprotocol struct {
}

func (self *Tኢንተርኔትcontrolመልእክትprotocol) Init(backend Tኢንተርኔትprotocolprovider, handler Iኢንተርኔትprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *Tኢንተርኔትcontrolመልእክትprotocol) Oኢንተርኔትprotocolreceivewhen(ምንጩipaddressኔትዎርክbyteorder uint32, destinationipaddressኔትዎርክbyteorder uint32, dataጠቋሚ uintptr, መጠን uint32) bool {
	if መጠን < uint32(icmpመጠን) {
		return false
	}

	var buffer_2 *Tኢንተርኔትcontrolመልእክትprotocolመልእክትbuffer = (*Tኢንተርኔትcontrolመልእክትprotocolመልእክትbuffer)(Pointer(dataጠቋሚ))
	var msg Tኢንተርኔትcontrolመልእክትprotocolመልእክት = Tኢንተርኔትcontrolመልእክትprotocolመልእክት{}
	msg.Init(*buffer_2)

	icmpconsole.Mማተሚያ(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16ማተሚያ(uint16(msg.Tአይነት))
	icmpconsole.Mማተሚያ(([]byte)(":"))

	switch msg.Tአይነት {
	case 0:
		icmpconsole.Mማተሚያ(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.Mማተሚያ(([]byte)("ping send "))
		msg.Tአይነት = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataጠቋሚ)), uint32(icmpመጠን))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *Tኢንተርኔትcontrolመልእክትprotocol) Echorequestsend(ipኔትዎርክbyteorder uint32) bool {
	var icmp Tኢንተርኔትcontrolመልእክትprotocolመልእክት = Tኢንተርኔትcontrolመልእክትprotocolመልእክት{}

	var ማስታወሻmanager = &Tማስታወሻmanager{}
	var buffer_2 = (*Tኢንተርኔትcontrolመልእክትprotocolመልእክትbuffer)(ማስታወሻmanager.Malloc(1024))

	icmp.Tአይነት = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpመጠን))
	icmp.Setbuffer(buffer_2)

	var dataጠቋሚ uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipኔትዎርክbyteorder, 0x01, dataጠቋሚ, uint32(icmpመጠን))

	return false

}
