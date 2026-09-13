package лякальнаясеткаФрэйм

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var лякальнаясеткаconsole TConsole = TConsole{}

type TЛякальнаясеткаФрэймheaderbuffer struct {
	destinationmacbe	[6]byte
	крыніцаmacbe		[6]byte
	лякальнаясеткаТыпbe	[2]byte
}

var фрэймheaderПамер int = 14

type TЛякальнаясеткаФрэймheader struct {
	destinationmacbe	uint64
	крыніцаmacbe		uint64
	лякальнаясеткаТыпbe	uint16
}

func (self *TЛякальнаясеткаФрэймheader) Init(buffer_2 TЛякальнаясеткаФрэймheaderbuffer) {
	self.destinationmacbe = (Масіўtounsignedinteger48(buffer_2.destinationmacbe))
	self.крыніцаmacbe = (Масіўtounsignedinteger48(buffer_2.крыніцаmacbe))
	self.лякальнаясеткаТыпbe = (Масіўtounsignedinteger16(buffer_2.лякальнаясеткаТыпbe))

}
func (self *TЛякальнаясеткаФрэймheader) Вызначанаbuffer(buffer_2 *TЛякальнаясеткаФрэймheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toМасіў(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.крыніцаmacbe = Unsignedinteger48toМасіў(Unsignedinteger48r(self.крыніцаmacbe))
	buffer_2.лякальнаясеткаТыпbe = Unsignedinteger16toМасіў(Unsignedinteger16r(self.лякальнаясеткаТыпbe))
}

type IЛякальнаясеткаФрэймhandler interface {
	Init(backend TЛякальнаясеткаФрэймprovider)
	Вызначанаhandler(handler IЛякальнаясеткаФрэймhandler, лякальнаясеткаТып uint16)
	ЛякальнаясеткаФрэймreceivewhen(dataПаказальнік uintptr, памер int) bool
	Даслаць(destinationmacbe uint64, dataПаказальнік uintptr, памер uint32)
	ФрэймДаслаць(destinationmacbe uint64, лякальнаясеткаТыпbe uint16, dataПаказальнік uintptr, памер uint32)
	Providerget() TЛякальнаясеткаФрэймprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TЛякальнаясеткаФрэймhandler struct {
}

var фрэйм TЛякальнаясеткаФрэймheader
var Backend TЛякальнаясеткаФрэймprovider
var handler_2 [65535]IЛякальнаясеткаФрэймhandler
var efhandler *TЛякальнаясеткаФрэймhandler = nil

func (self *TЛякальнаясеткаФрэймhandler) Init(backend TЛякальнаясеткаФрэймprovider) {
	Backend = backend
}

func (self *TЛякальнаясеткаФрэймhandler) Вызначанаhandler(handler IЛякальнаясеткаФрэймhandler, pЛякальнаясеткаТып uint16) {
	handler_2[pЛякальнаясеткаТып] = handler
}
func (self *TЛякальнаясеткаФрэймhandler) Вызначанаbackend(backend TЛякальнаясеткаФрэймprovider) {
	Backend = backend
}
func (self *TЛякальнаясеткаФрэймhandler) Getbackend() TЛякальнаясеткаФрэймprovider {
	return Backend
}
func (self *TЛякальнаясеткаФрэймhandler) ЛякальнаясеткаФрэймreceivewhen(dataПаказальнік uintptr, памер int) bool {
	лякальнаясеткаconsole.MДрукаваць(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TЛякальнаясеткаФрэймhandler) Даслаць(destinationmacbe uint64, dataПаказальнік uintptr, памер uint32) {
	Backend.ФрэймДаслаць(destinationmacbe, фрэйм.лякальнаясеткаТыпbe, dataПаказальнік, памер)
}
func (self *TЛякальнаясеткаФрэймhandler) ФрэймДаслаць(destinationmacbe uint64, лякальнаясеткаТыпbe uint16, dataПаказальнік uintptr, памер uint32) {
	Backend.ФрэймДаслаць(destinationmacbe, лякальнаясеткаТыпbe, dataПаказальнік, памер)
}
func (self *TЛякальнаясеткаФрэймhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TЛякальнаясеткаФрэймhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TЛякальнаясеткаФрэймhandler) Providerget() TЛякальнаясеткаФрэймprovider {
	return Backend
}

type TЛякальнаясеткаФрэймrawdatahandler struct {
	TRawdatahandler
}

var provider TЛякальнаясеткаФрэймprovider

func (self *TЛякальнаясеткаФрэймrawdatahandler) Init(pprovider TЛякальнаясеткаФрэймprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TЛякальнаясеткаФрэймrawdatahandler) Onrawdatareceive(dataПаказальнік uintptr, памер int) bool {
	return provider.Onrawdatareceive(dataПаказальнік, памер)
}
func (self *TЛякальнаясеткаФрэймrawdatahandler) Даслаць(dataПаказальнік uintptr, памер uint32) {
	provider.Даслаць(dataПаказальнік, памер)
}
func (self *TЛякальнаясеткаФрэймrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TЛякальнаясеткаФрэймrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TЛякальнаясеткаФрэймrawdatahandler) Providerget() TЛякальнаясеткаФрэймprovider {
	return provider
}

type TЛякальнаясеткаФрэймprovider struct {
	сеткаКартачныя	Tamdam79c973
	handler_2	[65565]IЛякальнаясеткаФрэймhandler
}

func (self *TЛякальнаясеткаФрэймprovider) Init(backend Tamdam79c973) {

	self.сеткаКартачныя = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TЛякальнаясеткаФрэймprovider) Onrawdatareceive(dataПаказальнік uintptr, памер int) bool {

	var buffer_2 *TЛякальнаясеткаФрэймheaderbuffer = (*TЛякальнаясеткаФрэймheaderbuffer)(Pointer(dataПаказальнік))
	var фрэйм TЛякальнаясеткаФрэймheader = TЛякальнаясеткаФрэймheader{}
	фрэйм.Init(*buffer_2)
	var reply bool = false

	if фрэйм.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(фрэйм.destinationmacbe) == self.Getmacaddress() {
		if handler_2[фрэйм.лякальнаясеткаТыпbe] != nil {
			лякальнаясеткаconsole.MДрукаваць(([]byte)("provider\n"))

			var паказальнік uintptr = uintptr(Pointer(dataПаказальнік)) + uintptr(фрэймheaderПамер)
			reply = handler_2[фрэйм.лякальнаясеткаТыпbe].ЛякальнаясеткаФрэймreceivewhen(паказальнік, памер-фрэймheaderПамер)

		}
	}

	if reply {
		фрэйм.destinationmacbe = фрэйм.крыніцаmacbe
		фрэйм.крыніцаmacbe = Unsignedinteger48r(self.Getmacaddress())
		фрэйм.Вызначанаbuffer(buffer_2)

	}

	лякальнаясеткаconsole.MДрукавацьxy(([]byte)("spro["), 0, 1)
	лякальнаясеткаconsole.MUnsignedinteger64Друкаваць(фрэйм.крыніцаmacbe)
	лякальнаясеткаconsole.MДрукаваць(([]byte)(":"))
	лякальнаясеткаconsole.MUnsignedinteger64Друкаваць(фрэйм.destinationmacbe)
	лякальнаясеткаconsole.MДрукаваць(([]byte)(":]["))
	лякальнаясеткаconsole.MUnsignedinteger64Друкаваць(self.Getmacaddress())
	лякальнаясеткаconsole.MДрукаваць(([]byte)(":"))
	лякальнаясеткаconsole.MUnsignedinteger16Друкаваць(фрэйм.лякальнаясеткаТыпbe)
	лякальнаясеткаconsole.MДрукаваць(([]byte)("]"))

	return reply

}
func (self *TЛякальнаясеткаФрэймprovider) Даслаць(dataПаказальнік uintptr, памер uint32) {
	self.сеткаКартачныя.Даслаць(dataПаказальнік, памер)
}
func (self *TЛякальнаясеткаФрэймprovider) ФрэймДаслаць(destinationmacbe uint64, лякальнаясеткаТыпbe uint16, dataПаказальнік uintptr, памер uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TЛякальнаясеткаФрэймheaderbuffer = (*TЛякальнаясеткаФрэймheaderbuffer)(Pointer(&buffer2_2))

	var фрэйм TЛякальнаясеткаФрэймheader = TЛякальнаясеткаФрэймheader{}
	фрэйм.Init(*buffer_2)

	фрэйм.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	фрэйм.крыніцаmacbe = Unsignedinteger48r(self.сеткаКартачныя.Getmacaddress())
	фрэйм.лякальнаясеткаТыпbe = Unsignedinteger16r(лякальнаясеткаТыпbe)

	фрэйм.Вызначанаbuffer(buffer_2)
	var крыніца_2 [4096]byte = *(*([4096]byte))(Pointer(dataПаказальнік))

	var i uint32 = 0
	for i = 0; i < памер; i++ {
		buffer2_2[uint32(фрэймheaderПамер)+i] = крыніца_2[i]

	}

	var паказальнік uintptr = uintptr(Pointer(&buffer2_2))

	self.сеткаКартачныя.Даслаць(паказальнік, памер+uint32(фрэймheaderПамер))

}
func (self *TЛякальнаясеткаФрэймprovider) Getmacaddress() uint64 {
	return self.сеткаКартачныя.Getmacaddress()
}
func (self *TЛякальнаясеткаФрэймprovider) Getipaddress() uint64 {
	return self.сеткаКартачныя.Getipaddress()
}
