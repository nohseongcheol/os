/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ethernetክፈፍ

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetክፈፍheaderbuffer struct {
	destinationmacbe	[6]byte
	ምንጩmacbe		[6]byte
	ethernetአይነትbe		[2]byte
}

var ክፈፍheaderመጠን int = 14

type TEthernetክፈፍheader struct {
	destinationmacbe	uint64
	ምንጩmacbe		uint64
	ethernetአይነትbe		uint16
}

func (self *TEthernetክፈፍheader) Init(buffer_2 TEthernetክፈፍheaderbuffer) {
	self.destinationmacbe = (Aማዘጋጃtounsignedinteger48(buffer_2.destinationmacbe))
	self.ምንጩmacbe = (Aማዘጋጃtounsignedinteger48(buffer_2.ምንጩmacbe))
	self.ethernetአይነትbe = (Aማዘጋጃtounsignedinteger16(buffer_2.ethernetአይነትbe))

}
func (self *TEthernetክፈፍheader) Setbuffer(buffer_2 *TEthernetክፈፍheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toማዘጋጃ(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.ምንጩmacbe = Unsignedinteger48toማዘጋጃ(Unsignedinteger48r(self.ምንጩmacbe))
	buffer_2.ethernetአይነትbe = Unsignedinteger16toማዘጋጃ(Unsignedinteger16r(self.ethernetአይነትbe))
}

type IEthernetክፈፍhandler interface {
	Init(backend TEthernetክፈፍprovider)
	Sethandler(handler IEthernetክፈፍhandler, ethernetአይነት uint16)
	Ethernetክፈፍreceivewhen(dataጠቋሚ uintptr, መጠን int) bool
	Send(destinationmacbe uint64, dataጠቋሚ uintptr, መጠን uint32)
	Sክፈፍsend(destinationmacbe uint64, ethernetአይነትbe uint16, dataጠቋሚ uintptr, መጠን uint32)
	Providerget() TEthernetክፈፍprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetክፈፍhandler struct {
}

var ክፈፍ TEthernetክፈፍheader
var Backend TEthernetክፈፍprovider
var handler_2 [65535]IEthernetክፈፍhandler
var efhandler *TEthernetክፈፍhandler = nil

func (self *TEthernetክፈፍhandler) Init(backend TEthernetክፈፍprovider) {
	Backend = backend
}

func (self *TEthernetክፈፍhandler) Sethandler(handler IEthernetክፈፍhandler, pethernetአይነት uint16) {
	handler_2[pethernetአይነት] = handler
}
func (self *TEthernetክፈፍhandler) Setbackend(backend TEthernetክፈፍprovider) {
	Backend = backend
}
func (self *TEthernetክፈፍhandler) Getbackend() TEthernetክፈፍprovider {
	return Backend
}
func (self *TEthernetክፈፍhandler) Ethernetክፈፍreceivewhen(dataጠቋሚ uintptr, መጠን int) bool {
	ethernetconsole.Mማተሚያ(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetክፈፍhandler) Send(destinationmacbe uint64, dataጠቋሚ uintptr, መጠን uint32) {
	Backend.Sክፈፍsend(destinationmacbe, ክፈፍ.ethernetአይነትbe, dataጠቋሚ, መጠን)
}
func (self *TEthernetክፈፍhandler) Sክፈፍsend(destinationmacbe uint64, ethernetአይነትbe uint16, dataጠቋሚ uintptr, መጠን uint32) {
	Backend.Sክፈፍsend(destinationmacbe, ethernetአይነትbe, dataጠቋሚ, መጠን)
}
func (self *TEthernetክፈፍhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernetክፈፍhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernetክፈፍhandler) Providerget() TEthernetክፈፍprovider {
	return Backend
}

type TEthernetክፈፍrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetክፈፍprovider

func (self *TEthernetክፈፍrawdatahandler) Init(pprovider TEthernetክፈፍprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetክፈፍrawdatahandler) Oማብሪያrawdatareceive(dataጠቋሚ uintptr, መጠን int) bool {
	return provider.Oማብሪያrawdatareceive(dataጠቋሚ, መጠን)
}
func (self *TEthernetክፈፍrawdatahandler) Send(dataጠቋሚ uintptr, መጠን uint32) {
	provider.Send(dataጠቋሚ, መጠን)
}
func (self *TEthernetክፈፍrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernetክፈፍrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernetክፈፍrawdatahandler) Providerget() TEthernetክፈፍprovider {
	return provider
}

type TEthernetክፈፍprovider struct {
	ኔትዎርክcard	Tamdam79c973
	handler_2	[65565]IEthernetክፈፍhandler
}

func (self *TEthernetክፈፍprovider) Init(backend Tamdam79c973) {

	self.ኔትዎርክcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetክፈፍprovider) Oማብሪያrawdatareceive(dataጠቋሚ uintptr, መጠን int) bool {

	var buffer_2 *TEthernetክፈፍheaderbuffer = (*TEthernetክፈፍheaderbuffer)(Pointer(dataጠቋሚ))
	var ክፈፍ TEthernetክፈፍheader = TEthernetክፈፍheader{}
	ክፈፍ.Init(*buffer_2)
	var reply bool = false

	if ክፈፍ.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(ክፈፍ.destinationmacbe) == self.Getmacaddress() {
		if handler_2[ክፈፍ.ethernetአይነትbe] != nil {
			ethernetconsole.Mማተሚያ(([]byte)("provider\n"))

			var ጠቋሚ uintptr = uintptr(Pointer(dataጠቋሚ)) + uintptr(ክፈፍheaderመጠን)
			reply = handler_2[ክፈፍ.ethernetአይነትbe].Ethernetክፈፍreceivewhen(ጠቋሚ, መጠን-ክፈፍheaderመጠን)

		}
	}

	if reply {
		ክፈፍ.destinationmacbe = ክፈፍ.ምንጩmacbe
		ክፈፍ.ምንጩmacbe = Unsignedinteger48r(self.Getmacaddress())
		ክፈፍ.Setbuffer(buffer_2)

	}

	ethernetconsole.Mማተሚያxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64ማተሚያ(ክፈፍ.ምንጩmacbe)
	ethernetconsole.Mማተሚያ(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64ማተሚያ(ክፈፍ.destinationmacbe)
	ethernetconsole.Mማተሚያ(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64ማተሚያ(self.Getmacaddress())
	ethernetconsole.Mማተሚያ(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16ማተሚያ(ክፈፍ.ethernetአይነትbe)
	ethernetconsole.Mማተሚያ(([]byte)("]"))

	return reply

}
func (self *TEthernetክፈፍprovider) Send(dataጠቋሚ uintptr, መጠን uint32) {
	self.ኔትዎርክcard.Send(dataጠቋሚ, መጠን)
}
func (self *TEthernetክፈፍprovider) Sክፈፍsend(destinationmacbe uint64, ethernetአይነትbe uint16, dataጠቋሚ uintptr, መጠን uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetክፈፍheaderbuffer = (*TEthernetክፈፍheaderbuffer)(Pointer(&buffer2_2))

	var ክፈፍ TEthernetክፈፍheader = TEthernetክፈፍheader{}
	ክፈፍ.Init(*buffer_2)

	ክፈፍ.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	ክፈፍ.ምንጩmacbe = Unsignedinteger48r(self.ኔትዎርክcard.Getmacaddress())
	ክፈፍ.ethernetአይነትbe = Unsignedinteger16r(ethernetአይነትbe)

	ክፈፍ.Setbuffer(buffer_2)
	var ምንጩ_2 [4096]byte = *(*([4096]byte))(Pointer(dataጠቋሚ))

	var i uint32 = 0
	for i = 0; i < መጠን; i++ {
		buffer2_2[uint32(ክፈፍheaderመጠን)+i] = ምንጩ_2[i]

	}

	var ጠቋሚ uintptr = uintptr(Pointer(&buffer2_2))

	self.ኔትዎርክcard.Send(ጠቋሚ, መጠን+uint32(ክፈፍheaderመጠን))

}
func (self *TEthernetክፈፍprovider) Getmacaddress() uint64 {
	return self.ኔትዎርክcard.Getmacaddress()
}
func (self *TEthernetክፈፍprovider) Getipaddress() uint64 {
	return self.ኔትዎርክcard.Getipaddress()
}
