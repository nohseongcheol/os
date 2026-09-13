package بروتوكول_رزم_المستخدم

import . "unsafe"
import . "طرفية"
import . "أداة"
import . "ذاكرةمدير"
import . "بروتوكول_الشبكة_المترابطة_4"

var udpطرفية = Tطرفية{}

type Tمستخدمdatagramالبروتوكولترويسةbuffer struct {
	رقم_منفذ_المصدر	[2]byte
	رقم_منفذ_الوجهة	[2]byte

	المدة		[2]byte
	checksum	[2]byte
}

var udpترويسةالحجم uint32 = 8

type Tترويسة_رزم_المستخدم struct {
	رقم_منفذ_المصدر	uint16
	رقم_منفذ_الوجهة	uint16

	المدة		uint16
	checksum	uint16
}

func (نفسه *Tترويسة_رزم_المستخدم) Init(buffer_2 *Tمستخدمdatagramالبروتوكولترويسةbuffer) {
	نفسه.رقم_منفذ_المصدر = Aمصفوفةtounsignedinteger16(buffer_2.رقم_منفذ_المصدر)
	نفسه.رقم_منفذ_الوجهة = Aمصفوفةtounsignedinteger16(buffer_2.رقم_منفذ_الوجهة)

	نفسه.المدة = Aمصفوفةtounsignedinteger16(buffer_2.المدة)
	نفسه.checksum = Aمصفوفةtounsignedinteger16(buffer_2.checksum)
}
func (نفسه *Tترويسة_رزم_المستخدم) Sتحديدbuffer(buffer_2 *Tمستخدمdatagramالبروتوكولترويسةbuffer) {

	buffer_2.رقم_منفذ_المصدر = Unsignedinteger16toمصفوفة(نفسه.رقم_منفذ_المصدر)
	buffer_2.رقم_منفذ_الوجهة = Unsignedinteger16toمصفوفة(نفسه.رقم_منفذ_الوجهة)

	buffer_2.المدة = Unsignedinteger16toمصفوفة(نفسه.المدة)
	buffer_2.checksum = Unsignedinteger16toمصفوفة(نفسه.checksum)

}

type Iمستخدمdatagramالبروتوكولhandler interface {
	Hالتعاملمستخدمdatagramالبروتوكولالرسالة(مقبس *Tنقطة_اتصال_رزم_المستخدم, بيانات uintptr, الحجم uint16)
}

type Tمستخدمdatagramالبروتوكولhandler struct {
}

func (نفسه *Tمستخدمdatagramالبروتوكولhandler) Init(backend Tمزود_بروتوكول_الشبكة_المترابطة) {
}
func (نفسه *Tمستخدمdatagramالبروتوكولhandler) Hالتعاملمستخدمdatagramالبروتوكولالرسالة(مقبس *Tنقطة_اتصال_رزم_المستخدم, بيانات uintptr, الحجم uint16) {
}

type Iمستخدمdatagramالبروتوكولمقبس interface {
	Hالتعاملمستخدمdatagramالبروتوكولالرسالة(بيانات uintptr, الحجم uint16)
}
type Tنقطة_اتصال_رزم_المستخدم struct {
	البعيدمنفذالأرقام	uint16
	البعيدip		uint32
	محليمنفذالأرقام		uint16
	محليip			uint32

	listening	bool
}

var udpprovider Tمستخدمdatagramالبروتوكولprovider
var udphandler Iمستخدمdatagramالبروتوكولhandler

func (نفسه *Tنقطة_اتصال_رزم_المستخدم) Tتجريب() {
}
func (نفسه *Tنقطة_اتصال_رزم_المستخدم) Init(pudpprovider Tمستخدمdatagramالبروتوكولprovider, pudphandler Iمستخدمdatagramالبروتوكولhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	نفسه.listening = false
}
func (نفسه *Tنقطة_اتصال_رزم_المستخدم) Hالتعاملمستخدمdatagramالبروتوكولالرسالة(بيانات uintptr, الحجم uint16) {
	if udphandler != nil {
		udphandler.Hالتعاملمستخدمdatagramالبروتوكولالرسالة(نفسه, بيانات, الحجم)
	}
}
func (نفسه *Tنقطة_اتصال_رزم_المستخدم) Sأرسل(pبيانات []byte, الحجم uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(الحجم); i++ {
		buffer_2[i] = pبيانات[i]
	}
	var بيانات = uintptr(Pointer(&buffer_2))
	udpprovider.Sأرسل(نفسه, بيانات, الحجم)
}
func (نفسه *Tنقطة_اتصال_رزم_المستخدم) Dقطعالإتصال() {
	udpprovider.Dقطعالإتصال(نفسه)
}

type Tمستخدمdatagramالبروتوكولprovider struct {
}

var iphandler Iإنترنتالبروتوكولhandler
var sockets [65535]Tنقطة_اتصال_رزم_المستخدم
var الأرقامsockets int
var خاليمنفذ uint16

func (نفسه *Tمستخدمdatagramالبروتوكولprovider) Init(pipprovider Tمزود_بروتوكول_الشبكة_المترابطة, piphandler Iإنترنتالبروتوكولhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	الأرقامsockets = 0
	خاليمنفذ = 1024
}
func (نفسه *Tمستخدمdatagramالبروتوكولprovider) Oإنترنتالبروتوكولreceivewhen(المصدرipaddressشبكةبايتorder uint32, المقصدipaddressشبكةبايتorder uint32, إنترنتالبروتوكولpayload uintptr, الحجم uint32) bool {
	if الحجم < udpترويسةالحجم {
		return false
	}

	var buffer_2 *Tمستخدمdatagramالبروتوكولترويسةbuffer = (*Tمستخدمdatagramالبروتوكولترويسةbuffer)(Pointer(إنترنتالبروتوكولpayload))
	var msg Tترويسة_رزم_المستخدم
	msg.Init(buffer_2)

	var مقبس *Tنقطة_اتصال_رزم_المستخدم = nil

	for i := 0; i < الأرقامsockets && مقبس == nil; i++ {
		if sockets[i].محليمنفذالأرقام == msg.رقم_منفذ_الوجهة && sockets[i].محليip == المقصدipaddressشبكةبايتorder && sockets[i].listening == true {
			مقبس = &sockets[i]
			مقبس.listening = false
			مقبس.البعيدمنفذالأرقام = msg.رقم_منفذ_المصدر
			مقبس.البعيدip = المصدرipaddressشبكةبايتorder
		} else if sockets[i].محليمنفذالأرقام == msg.رقم_منفذ_الوجهة && sockets[i].محليip == المقصدipaddressشبكةبايتorder && sockets[i].البعيدمنفذالأرقام == msg.رقم_منفذ_المصدر && sockets[i].البعيدip == المصدرipaddressشبكةبايتorder {
			مقبس = &sockets[i]

		}
	}

	msg.Sتحديدbuffer(buffer_2)
	if مقبس != nil {
		مقبس.Hالتعاملمستخدمdatagramالبروتوكولالرسالة(إنترنتالبروتوكولpayload+uintptr(udpترويسةالحجم), uint16(الحجم-udpترويسةالحجم))
	}

	return false
}

func (نفسه *Tمستخدمdatagramالبروتوكولprovider) Connect(ip uint32, منفذ uint16) *Tنقطة_اتصال_رزم_المستخدم {
	var ذاكرةمدير = &Tذاكرةمدير{}
	var مقبس = (*Tنقطة_اتصال_رزم_المستخدم)(ذاكرةمدير.Mتخصيص_الذاكرة(50))

	if مقبس != nil {

		مقبس.Init(*نفسه, nil)
		مقبس.البعيدمنفذالأرقام = منفذ
		مقبس.البعيدip = ip
		مقبس.محليمنفذالأرقام = خاليمنفذ
		خاليمنفذ++
		مقبس.محليip = uint32((*iphandler.Providerget()).Getipaddress())

		مقبس.البعيدمنفذالأرقام = Unsignedinteger16r(مقبس.البعيدمنفذالأرقام)
		مقبس.محليمنفذالأرقام = Unsignedinteger16r(مقبس.محليمنفذالأرقام)

		sockets[الأرقامsockets] = *مقبس
		الأرقامsockets++

	}
	return مقبس

}
func (نفسه *Tمستخدمdatagramالبروتوكولprovider) Listen(منفذ uint16) *Tنقطة_اتصال_رزم_المستخدم {
	var مقبس = &Tنقطة_اتصال_رزم_المستخدم{}
	مقبس = nil
	if مقبس != nil {
		مقبس.Init(*نفسه, nil)
		مقبس.listening = true
		مقبس.محليمنفذالأرقام = منفذ
		مقبس.محليip = uint32((*iphandler.Providerget()).Getipaddress())

		مقبس.محليمنفذالأرقام = Unsignedinteger16r(مقبس.محليمنفذالأرقام)
	}
	return مقبس
}
func (نفسه *Tمستخدمdatagramالبروتوكولprovider) Dقطعالإتصال(مقبس *Tنقطة_اتصال_رزم_المستخدم) {
	for i := 0; i < الأرقامsockets && مقبس == nil; i++ {
		if sockets[i] == *مقبس {
			الأرقامsockets--
			sockets[i] = sockets[الأرقامsockets]
			break
		}
	}
}
func (نفسه *Tمستخدمdatagramالبروتوكولprovider) Sأرسل(مقبس *Tنقطة_اتصال_رزم_المستخدم, pبيانات uintptr, الحجم uint16) {
	var المجموعالمدة = uint32(الحجم) + udpترويسةالحجم

	var buffer_2 [4096]byte

	var msgbuffer = (*Tمستخدمdatagramالبروتوكولترويسةbuffer)(Pointer(&buffer_2))

	var msg = Tترويسة_رزم_المستخدم{}

	msg.رقم_منفذ_المصدر = مقبس.محليمنفذالأرقام
	msg.رقم_منفذ_الوجهة = مقبس.البعيدمنفذالأرقام
	msg.المدة = Unsignedinteger16r(uint16(المجموعالمدة))

	msg.checksum = 0x0
	msg.Sتحديدbuffer(msgbuffer)

	var بياناتبايت [4096]byte = *(*[4096]byte)(Pointer(pبيانات))
	for i := 0; i < int(الحجم); i++ {
		buffer_2[int(udpترويسةالحجم)+i] = بياناتبايت[i]
	}

	var بيانات uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Sأرسل(مقبس.البعيدip, 0x11, بيانات, المجموعالمدة)

}
func (نفسه *Tمستخدمdatagramالبروتوكولprovider) Bind(مقبس *Tنقطة_اتصال_رزم_المستخدم, handler *Tمستخدمdatagramالبروتوكولhandler,) {
}
