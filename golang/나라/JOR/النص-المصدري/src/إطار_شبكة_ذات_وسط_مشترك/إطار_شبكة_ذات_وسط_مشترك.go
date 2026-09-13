package إطار_شبكة_ذات_وسط_مشترك

import . "طرفية"

import . "amdam79c973"
import . "unsafe"
import . "أداة"

var إيثرنتطرفية Tطرفية = Tطرفية{}

type Tإيثرنتإطارترويسةbuffer struct {
	المقصدmacbe	[6]byte
	المصدرmacbe	[6]byte
	إيثرنتنوعbe	[2]byte
}

var إطارترويسةالحجم int = 14

type Tترويسة_إطار_الشبكة_ذات_الوسط_المشترك struct {
	المقصدmacbe	uint64
	المصدرmacbe	uint64
	إيثرنتنوعbe	uint16
}

func (نفسه *Tترويسة_إطار_الشبكة_ذات_الوسط_المشترك) Init(buffer_2 Tإيثرنتإطارترويسةbuffer) {
	نفسه.المقصدmacbe = (Aمصفوفةtounsignedinteger48(buffer_2.المقصدmacbe))
	نفسه.المصدرmacbe = (Aمصفوفةtounsignedinteger48(buffer_2.المصدرmacbe))
	نفسه.إيثرنتنوعbe = (Aمصفوفةtounsignedinteger16(buffer_2.إيثرنتنوعbe))

}
func (نفسه *Tترويسة_إطار_الشبكة_ذات_الوسط_المشترك) Sتحديدbuffer(buffer_2 *Tإيثرنتإطارترويسةbuffer) {
	buffer_2.المقصدmacbe = Unsignedinteger48toمصفوفة(Unsignedinteger48r(نفسه.المقصدmacbe))
	buffer_2.المصدرmacbe = Unsignedinteger48toمصفوفة(Unsignedinteger48r(نفسه.المصدرmacbe))
	buffer_2.إيثرنتنوعbe = Unsignedinteger16toمصفوفة(Unsignedinteger16r(نفسه.إيثرنتنوعbe))
}

type Iإيثرنتإطارhandler interface {
	Init(backend Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك)
	Sتحديدhandler(handler Iإيثرنتإطارhandler, إيثرنتنوع uint16)
	Oإيثرنتإطارreceivewhen(بياناتالمؤشر uintptr, الحجم int) bool
	Sأرسل(المقصدmacbe uint64, بياناتالمؤشر uintptr, الحجم uint32)
	Sإطارأرسل(المقصدmacbe uint64, إيثرنتنوعbe uint16, بياناتالمؤشر uintptr, الحجم uint32)
	Providerget() Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك
	Getmacaddress() uint64
	Getipaddress() uint64
}

type Tإيثرنتإطارhandler struct {
}

var إطار Tترويسة_إطار_الشبكة_ذات_الوسط_المشترك
var Backend Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك
var handler_2 [65535]Iإيثرنتإطارhandler
var efhandler *Tإيثرنتإطارhandler = nil

func (نفسه *Tإيثرنتإطارhandler) Init(backend Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك) {
	Backend = backend
}

func (نفسه *Tإيثرنتإطارhandler) Sتحديدhandler(handler Iإيثرنتإطارhandler, pإيثرنتنوع uint16) {
	handler_2[pإيثرنتنوع] = handler
}
func (نفسه *Tإيثرنتإطارhandler) Sتحديدbackend(backend Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك) {
	Backend = backend
}
func (نفسه *Tإيثرنتإطارhandler) Getbackend() Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك {
	return Backend
}
func (نفسه *Tإيثرنتإطارhandler) Oإيثرنتإطارreceivewhen(بياناتالمؤشر uintptr, الحجم int) bool {
	إيثرنتطرفية.Mاطبع(([]byte)("OnEtherFrameReceived"))
	return false
}
func (نفسه *Tإيثرنتإطارhandler) Sأرسل(المقصدmacbe uint64, بياناتالمؤشر uintptr, الحجم uint32) {
	Backend.Sإطارأرسل(المقصدmacbe, إطار.إيثرنتنوعbe, بياناتالمؤشر, الحجم)
}
func (نفسه *Tإيثرنتإطارhandler) Sإطارأرسل(المقصدmacbe uint64, إيثرنتنوعbe uint16, بياناتالمؤشر uintptr, الحجم uint32) {
	Backend.Sإطارأرسل(المقصدmacbe, إيثرنتنوعbe, بياناتالمؤشر, الحجم)
}
func (نفسه *Tإيثرنتإطارhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (نفسه *Tإيثرنتإطارhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (نفسه *Tإيثرنتإطارhandler) Providerget() Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك {
	return Backend
}

type Tإيثرنتإطارrawبياناتhandler struct {
	TRawبياناتhandler
}

var provider Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك

func (نفسه *Tإيثرنتإطارrawبياناتhandler) Init(pprovider Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (نفسه *Tإيثرنتإطارrawبياناتhandler) Oعندrawبياناتreceive(بياناتالمؤشر uintptr, الحجم int) bool {
	return provider.Oعندrawبياناتreceive(بياناتالمؤشر, الحجم)
}
func (نفسه *Tإيثرنتإطارrawبياناتhandler) Sأرسل(بياناتالمؤشر uintptr, الحجم uint32) {
	provider.Sأرسل(بياناتالمؤشر, الحجم)
}
func (نفسه *Tإيثرنتإطارrawبياناتhandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (نفسه *Tإيثرنتإطارrawبياناتhandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (نفسه *Tإيثرنتإطارrawبياناتhandler) Providerget() Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك {
	return provider
}

type Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك struct {
	شبكةورق		Tamdam79c973
	handler_2	[65565]Iإيثرنتإطارhandler
}

func (نفسه *Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك) Init(backend Tamdam79c973) {

	نفسه.شبكةورق = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		نفسه.handler_2[i] = nil
	}
}

var count uint16 = 0

func (نفسه *Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك) Oعندrawبياناتreceive(بياناتالمؤشر uintptr, الحجم int) bool {

	var buffer_2 *Tإيثرنتإطارترويسةbuffer = (*Tإيثرنتإطارترويسةbuffer)(Pointer(بياناتالمؤشر))
	var إطار Tترويسة_إطار_الشبكة_ذات_الوسط_المشترك = Tترويسة_إطار_الشبكة_ذات_الوسط_المشترك{}
	إطار.Init(*buffer_2)
	var reply bool = false

	if إطار.المقصدmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(إطار.المقصدmacbe) == نفسه.Getmacaddress() {
		if handler_2[إطار.إيثرنتنوعbe] != nil {
			إيثرنتطرفية.Mاطبع(([]byte)("provider\n"))

			var مرجع_عنوان uintptr = uintptr(Pointer(بياناتالمؤشر)) + uintptr(إطارترويسةالحجم)
			reply = handler_2[إطار.إيثرنتنوعbe].Oإيثرنتإطارreceivewhen(مرجع_عنوان, الحجم-إطارترويسةالحجم)

		}
	}

	if reply {
		إطار.المقصدmacbe = إطار.المصدرmacbe
		إطار.المصدرmacbe = Unsignedinteger48r(نفسه.Getmacaddress())
		إطار.Sتحديدbuffer(buffer_2)

	}

	إيثرنتطرفية.Mاطبعxy(([]byte)("spro["), 0, 1)
	إيثرنتطرفية.MUnsignedinteger64اطبع(إطار.المصدرmacbe)
	إيثرنتطرفية.Mاطبع(([]byte)(":"))
	إيثرنتطرفية.MUnsignedinteger64اطبع(إطار.المقصدmacbe)
	إيثرنتطرفية.Mاطبع(([]byte)(":]["))
	إيثرنتطرفية.MUnsignedinteger64اطبع(نفسه.Getmacaddress())
	إيثرنتطرفية.Mاطبع(([]byte)(":"))
	إيثرنتطرفية.MUnsignedinteger16اطبع(إطار.إيثرنتنوعbe)
	إيثرنتطرفية.Mاطبع(([]byte)("]"))

	return reply

}
func (نفسه *Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك) Sأرسل(بياناتالمؤشر uintptr, الحجم uint32) {
	نفسه.شبكةورق.Sأرسل(بياناتالمؤشر, الحجم)
}
func (نفسه *Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك) Sإطارأرسل(المقصدmacbe uint64, إيثرنتنوعbe uint16, بياناتالمؤشر uintptr, الحجم uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *Tإيثرنتإطارترويسةbuffer = (*Tإيثرنتإطارترويسةbuffer)(Pointer(&buffer2_2))

	var إطار Tترويسة_إطار_الشبكة_ذات_الوسط_المشترك = Tترويسة_إطار_الشبكة_ذات_الوسط_المشترك{}
	إطار.Init(*buffer_2)

	إطار.المقصدmacbe = Unsignedinteger48r(المقصدmacbe)
	إطار.المصدرmacbe = Unsignedinteger48r(نفسه.شبكةورق.Getmacaddress())
	إطار.إيثرنتنوعbe = Unsignedinteger16r(إيثرنتنوعbe)

	إطار.Sتحديدbuffer(buffer_2)
	var المصدر_2 [4096]byte = *(*([4096]byte))(Pointer(بياناتالمؤشر))

	var i uint32 = 0
	for i = 0; i < الحجم; i++ {
		buffer2_2[uint32(إطارترويسةالحجم)+i] = المصدر_2[i]

	}

	var مرجع_عنوان uintptr = uintptr(Pointer(&buffer2_2))

	نفسه.شبكةورق.Sأرسل(مرجع_عنوان, الحجم+uint32(إطارترويسةالحجم))

}
func (نفسه *Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك) Getmacaddress() uint64 {
	return نفسه.شبكةورق.Getmacaddress()
}
func (نفسه *Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك) Getipaddress() uint64 {
	return نفسه.شبكةورق.Getipaddress()
}
