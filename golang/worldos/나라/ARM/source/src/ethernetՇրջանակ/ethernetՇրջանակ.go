/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ethernetՇրջանակ

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetՇրջանակheaderbuffer struct {
	destinationmacbe	[6]byte
	աղբյուրmacbe		[6]byte
	ethernetՏիպbe		[2]byte
}

var շրջանակheaderՉափս int = 14

type TEthernetՇրջանակheader struct {
	destinationmacbe	uint64
	աղբյուրmacbe		uint64
	ethernetՏիպbe		uint16
}

func (ինքնուրույն *TEthernetՇրջանակheader) Init(buffer_2 TEthernetՇրջանակheaderbuffer) {
	ինքնուրույն.destinationmacbe = (Զանգվածtounsignedinteger48(buffer_2.destinationmacbe))
	ինքնուրույն.աղբյուրmacbe = (Զանգվածtounsignedinteger48(buffer_2.աղբյուրmacbe))
	ինքնուրույն.ethernetՏիպbe = (Զանգվածtounsignedinteger16(buffer_2.ethernetՏիպbe))

}
func (ինքնուրույն *TEthernetՇրջանակheader) Setbuffer(buffer_2 *TEthernetՇրջանակheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toԶանգված(Unsignedinteger48r(ինքնուրույն.destinationmacbe))
	buffer_2.աղբյուրmacbe = Unsignedinteger48toԶանգված(Unsignedinteger48r(ինքնուրույն.աղբյուրmacbe))
	buffer_2.ethernetՏիպbe = Unsignedinteger16toԶանգված(Unsignedinteger16r(ինքնուրույն.ethernetՏիպbe))
}

type IEthernetՇրջանակhandler interface {
	Init(backend TEthernetՇրջանակprovider)
	Sethandler(handler IEthernetՇրջանակhandler, ethernetՏիպ uint16)
	EthernetՇրջանակreceivewhen(dataՑուցիչ uintptr, չափս int) bool
	ՈՒղարկել(destinationmacbe uint64, dataՑուցիչ uintptr, չափս uint32)
	ՇրջանակՈՒղարկել(destinationmacbe uint64, ethernetՏիպbe uint16, dataՑուցիչ uintptr, չափս uint32)
	Providerget() TEthernetՇրջանակprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetՇրջանակhandler struct {
}

var շրջանակ TEthernetՇրջանակheader
var Backend TEthernetՇրջանակprovider
var handler_2 [65535]IEthernetՇրջանակhandler
var efhandler *TEthernetՇրջանակhandler = nil

func (ինքնուրույն *TEthernetՇրջանակhandler) Init(backend TEthernetՇրջանակprovider) {
	Backend = backend
}

func (ինքնուրույն *TEthernetՇրջանակhandler) Sethandler(handler IEthernetՇրջանակhandler, pethernetՏիպ uint16) {
	handler_2[pethernetՏիպ] = handler
}
func (ինքնուրույն *TEthernetՇրջանակhandler) Setbackend(backend TEthernetՇրջանակprovider) {
	Backend = backend
}
func (ինքնուրույն *TEthernetՇրջանակhandler) Getbackend() TEthernetՇրջանակprovider {
	return Backend
}
func (ինքնուրույն *TEthernetՇրջանակhandler) EthernetՇրջանակreceivewhen(dataՑուցիչ uintptr, չափս int) bool {
	ethernetconsole.MՏպել(([]byte)("OnEtherFrameReceived"))
	return false
}
func (ինքնուրույն *TEthernetՇրջանակhandler) ՈՒղարկել(destinationmacbe uint64, dataՑուցիչ uintptr, չափս uint32) {
	Backend.ՇրջանակՈՒղարկել(destinationmacbe, շրջանակ.ethernetՏիպbe, dataՑուցիչ, չափս)
}
func (ինքնուրույն *TEthernetՇրջանակhandler) ՇրջանակՈՒղարկել(destinationmacbe uint64, ethernetՏիպbe uint16, dataՑուցիչ uintptr, չափս uint32) {
	Backend.ՇրջանակՈՒղարկել(destinationmacbe, ethernetՏիպbe, dataՑուցիչ, չափս)
}
func (ինքնուրույն *TEthernetՇրջանակhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (ինքնուրույն *TEthernetՇրջանակhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (ինքնուրույն *TEthernetՇրջանակhandler) Providerget() TEthernetՇրջանակprovider {
	return Backend
}

type TEthernetՇրջանակrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetՇրջանակprovider

func (ինքնուրույն *TEthernetՇրջանակrawdatahandler) Init(pprovider TEthernetՇրջանակprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (ինքնուրույն *TEthernetՇրջանակrawdatahandler) Միացնելrawdatareceive(dataՑուցիչ uintptr, չափս int) bool {
	return provider.Միացնելrawdatareceive(dataՑուցիչ, չափս)
}
func (ինքնուրույն *TEthernetՇրջանակrawdatahandler) ՈՒղարկել(dataՑուցիչ uintptr, չափս uint32) {
	provider.ՈՒղարկել(dataՑուցիչ, չափս)
}
func (ինքնուրույն *TEthernetՇրջանակrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (ինքնուրույն *TEthernetՇրջանակrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (ինքնուրույն *TEthernetՇրջանակrawdatahandler) Providerget() TEthernetՇրջանակprovider {
	return provider
}

type TEthernetՇրջանակprovider struct {
	ցանցcard	Tamdam79c973
	handler_2	[65565]IEthernetՇրջանակhandler
}

func (ինքնուրույն *TEthernetՇրջանակprovider) Init(backend Tamdam79c973) {

	ինքնուրույն.ցանցcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		ինքնուրույն.handler_2[i] = nil
	}
}

var count uint16 = 0

func (ինքնուրույն *TEthernetՇրջանակprovider) Միացնելrawdatareceive(dataՑուցիչ uintptr, չափս int) bool {

	var buffer_2 *TEthernetՇրջանակheaderbuffer = (*TEthernetՇրջանակheaderbuffer)(Pointer(dataՑուցիչ))
	var շրջանակ TEthernetՇրջանակheader = TEthernetՇրջանակheader{}
	շրջանակ.Init(*buffer_2)
	var reply bool = false

	if շրջանակ.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(շրջանակ.destinationmacbe) == ինքնուրույն.Getmacaddress() {
		if handler_2[շրջանակ.ethernetՏիպbe] != nil {
			ethernetconsole.MՏպել(([]byte)("provider\n"))

			var ցուցիչ uintptr = uintptr(Pointer(dataՑուցիչ)) + uintptr(շրջանակheaderՉափս)
			reply = handler_2[շրջանակ.ethernetՏիպbe].EthernetՇրջանակreceivewhen(ցուցիչ, չափս-շրջանակheaderՉափս)

		}
	}

	if reply {
		շրջանակ.destinationmacbe = շրջանակ.աղբյուրmacbe
		շրջանակ.աղբյուրmacbe = Unsignedinteger48r(ինքնուրույն.Getmacaddress())
		շրջանակ.Setbuffer(buffer_2)

	}

	ethernetconsole.MՏպելxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Տպել(շրջանակ.աղբյուրmacbe)
	ethernetconsole.MՏպել(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Տպել(շրջանակ.destinationmacbe)
	ethernetconsole.MՏպել(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Տպել(ինքնուրույն.Getmacaddress())
	ethernetconsole.MՏպել(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Տպել(շրջանակ.ethernetՏիպbe)
	ethernetconsole.MՏպել(([]byte)("]"))

	return reply

}
func (ինքնուրույն *TEthernetՇրջանակprovider) ՈՒղարկել(dataՑուցիչ uintptr, չափս uint32) {
	ինքնուրույն.ցանցcard.ՈՒղարկել(dataՑուցիչ, չափս)
}
func (ինքնուրույն *TEthernetՇրջանակprovider) ՇրջանակՈՒղարկել(destinationmacbe uint64, ethernetՏիպbe uint16, dataՑուցիչ uintptr, չափս uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetՇրջանակheaderbuffer = (*TEthernetՇրջանակheaderbuffer)(Pointer(&buffer2_2))

	var շրջանակ TEthernetՇրջանակheader = TEthernetՇրջանակheader{}
	շրջանակ.Init(*buffer_2)

	շրջանակ.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	շրջանակ.աղբյուրmacbe = Unsignedinteger48r(ինքնուրույն.ցանցcard.Getmacaddress())
	շրջանակ.ethernetՏիպbe = Unsignedinteger16r(ethernetՏիպbe)

	շրջանակ.Setbuffer(buffer_2)
	var աղբյուր_2 [4096]byte = *(*([4096]byte))(Pointer(dataՑուցիչ))

	var i uint32 = 0
	for i = 0; i < չափս; i++ {
		buffer2_2[uint32(շրջանակheaderՉափս)+i] = աղբյուր_2[i]

	}

	var ցուցիչ uintptr = uintptr(Pointer(&buffer2_2))

	ինքնուրույն.ցանցcard.ՈՒղարկել(ցուցիչ, չափս+uint32(շրջանակheaderՉափս))

}
func (ինքնուրույն *TEthernetՇրջանակprovider) Getmacaddress() uint64 {
	return ինքնուրույն.ցանցcard.Getmacaddress()
}
func (ինքնուրույն *TEthernetՇրջանակprovider) Getipaddress() uint64 {
	return ինքնուրույն.ցանցcard.Getipaddress()
}
