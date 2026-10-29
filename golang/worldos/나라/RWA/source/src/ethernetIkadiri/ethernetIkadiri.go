/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ethernetIkadiri

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetIkadiriheaderbuffer struct {
	destinationmacbe	[6]byte
	inkomokomacbe		[6]byte
	ethernetUbwokobe	[2]byte
}

var ikadiriheaderIngano int = 14

type TEthernetIkadiriheader struct {
	destinationmacbe	uint64
	inkomokomacbe		uint64
	ethernetUbwokobe	uint16
}

func (self *TEthernetIkadiriheader) Init(buffer_2 TEthernetIkadiriheaderbuffer) {
	self.destinationmacbe = (Imbonerahamwetounsignedinteger48(buffer_2.destinationmacbe))
	self.inkomokomacbe = (Imbonerahamwetounsignedinteger48(buffer_2.inkomokomacbe))
	self.ethernetUbwokobe = (Imbonerahamwetounsignedinteger16(buffer_2.ethernetUbwokobe))

}
func (self *TEthernetIkadiriheader) Setbuffer(buffer_2 *TEthernetIkadiriheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toImbonerahamwe(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.inkomokomacbe = Unsignedinteger48toImbonerahamwe(Unsignedinteger48r(self.inkomokomacbe))
	buffer_2.ethernetUbwokobe = Unsignedinteger16toImbonerahamwe(Unsignedinteger16r(self.ethernetUbwokobe))
}

type IEthernetIkadirihandler interface {
	Init(backend TEthernetIkadiriprovider)
	Sethandler(handler IEthernetIkadirihandler, ethernetUbwoko uint16)
	EthernetIkadirireceivewhen(datapointer uintptr, ingano int) bool
	Send(destinationmacbe uint64, datapointer uintptr, ingano uint32)
	Ikadirisend(destinationmacbe uint64, ethernetUbwokobe uint16, datapointer uintptr, ingano uint32)
	Providerget() TEthernetIkadiriprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetIkadirihandler struct {
}

var ikadiri TEthernetIkadiriheader
var Backend TEthernetIkadiriprovider
var handler_2 [65535]IEthernetIkadirihandler
var efhandler *TEthernetIkadirihandler = nil

func (self *TEthernetIkadirihandler) Init(backend TEthernetIkadiriprovider) {
	Backend = backend
}

func (self *TEthernetIkadirihandler) Sethandler(handler IEthernetIkadirihandler, pethernetUbwoko uint16) {
	handler_2[pethernetUbwoko] = handler
}
func (self *TEthernetIkadirihandler) Setbackend(backend TEthernetIkadiriprovider) {
	Backend = backend
}
func (self *TEthernetIkadirihandler) Getbackend() TEthernetIkadiriprovider {
	return Backend
}
func (self *TEthernetIkadirihandler) EthernetIkadirireceivewhen(datapointer uintptr, ingano int) bool {
	ethernetconsole.MGucapa(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetIkadirihandler) Send(destinationmacbe uint64, datapointer uintptr, ingano uint32) {
	Backend.Ikadirisend(destinationmacbe, ikadiri.ethernetUbwokobe, datapointer, ingano)
}
func (self *TEthernetIkadirihandler) Ikadirisend(destinationmacbe uint64, ethernetUbwokobe uint16, datapointer uintptr, ingano uint32) {
	Backend.Ikadirisend(destinationmacbe, ethernetUbwokobe, datapointer, ingano)
}
func (self *TEthernetIkadirihandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernetIkadirihandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernetIkadirihandler) Providerget() TEthernetIkadiriprovider {
	return Backend
}

type TEthernetIkadirirawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetIkadiriprovider

func (self *TEthernetIkadirirawdatahandler) Init(pprovider TEthernetIkadiriprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetIkadirirawdatahandler) Kurirawdatareceive(datapointer uintptr, ingano int) bool {
	return provider.Kurirawdatareceive(datapointer, ingano)
}
func (self *TEthernetIkadirirawdatahandler) Send(datapointer uintptr, ingano uint32) {
	provider.Send(datapointer, ingano)
}
func (self *TEthernetIkadirirawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernetIkadirirawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernetIkadirirawdatahandler) Providerget() TEthernetIkadiriprovider {
	return provider
}

type TEthernetIkadiriprovider struct {
	urusobecard	Tamdam79c973
	handler_2	[65565]IEthernetIkadirihandler
}

func (self *TEthernetIkadiriprovider) Init(backend Tamdam79c973) {

	self.urusobecard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetIkadiriprovider) Kurirawdatareceive(datapointer uintptr, ingano int) bool {

	var buffer_2 *TEthernetIkadiriheaderbuffer = (*TEthernetIkadiriheaderbuffer)(Pointer(datapointer))
	var ikadiri TEthernetIkadiriheader = TEthernetIkadiriheader{}
	ikadiri.Init(*buffer_2)
	var reply bool = false

	if ikadiri.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(ikadiri.destinationmacbe) == self.Getmacaddress() {
		if handler_2[ikadiri.ethernetUbwokobe] != nil {
			ethernetconsole.MGucapa(([]byte)("provider\n"))

			var pointer uintptr = uintptr(Pointer(datapointer)) + uintptr(ikadiriheaderIngano)
			reply = handler_2[ikadiri.ethernetUbwokobe].EthernetIkadirireceivewhen(pointer, ingano-ikadiriheaderIngano)

		}
	}

	if reply {
		ikadiri.destinationmacbe = ikadiri.inkomokomacbe
		ikadiri.inkomokomacbe = Unsignedinteger48r(self.Getmacaddress())
		ikadiri.Setbuffer(buffer_2)

	}

	ethernetconsole.MGucapaxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Gucapa(ikadiri.inkomokomacbe)
	ethernetconsole.MGucapa(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Gucapa(ikadiri.destinationmacbe)
	ethernetconsole.MGucapa(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Gucapa(self.Getmacaddress())
	ethernetconsole.MGucapa(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Gucapa(ikadiri.ethernetUbwokobe)
	ethernetconsole.MGucapa(([]byte)("]"))

	return reply

}
func (self *TEthernetIkadiriprovider) Send(datapointer uintptr, ingano uint32) {
	self.urusobecard.Send(datapointer, ingano)
}
func (self *TEthernetIkadiriprovider) Ikadirisend(destinationmacbe uint64, ethernetUbwokobe uint16, datapointer uintptr, ingano uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetIkadiriheaderbuffer = (*TEthernetIkadiriheaderbuffer)(Pointer(&buffer2_2))

	var ikadiri TEthernetIkadiriheader = TEthernetIkadiriheader{}
	ikadiri.Init(*buffer_2)

	ikadiri.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	ikadiri.inkomokomacbe = Unsignedinteger48r(self.urusobecard.Getmacaddress())
	ikadiri.ethernetUbwokobe = Unsignedinteger16r(ethernetUbwokobe)

	ikadiri.Setbuffer(buffer_2)
	var inkomoko_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < ingano; i++ {
		buffer2_2[uint32(ikadiriheaderIngano)+i] = inkomoko_2[i]

	}

	var pointer uintptr = uintptr(Pointer(&buffer2_2))

	self.urusobecard.Send(pointer, ingano+uint32(ikadiriheaderIngano))

}
func (self *TEthernetIkadiriprovider) Getmacaddress() uint64 {
	return self.urusobecard.Getmacaddress()
}
func (self *TEthernetIkadiriprovider) Getipaddress() uint64 {
	return self.urusobecard.Getipaddress()
}
