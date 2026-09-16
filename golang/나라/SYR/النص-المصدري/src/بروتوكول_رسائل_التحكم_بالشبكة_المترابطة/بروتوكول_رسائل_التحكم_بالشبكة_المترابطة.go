/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package بروتوكول_رسائل_التحكم_بالشبكة_المترابطة

import . "unsafe"
import . "طرفية"
import . "ذاكرةمدير"
import . "إطار_شبكة_ذات_وسط_مشترك"
import . "بروتوكول_الشبكة_المترابطة_4"
import . "أداة"

var icmpطرفية = Tطرفية{}

type Tإنترنتتحكمالرسالةالبروتوكولالرسالةbuffer struct {
	Tنوع	byte
	code	byte

	checksum	[2]byte
	بيانات		[4]byte
}

var icmpالحجم int = 64

type Tإنترنتتحكمالرسالةالبروتوكولالرسالة struct {
	Tنوع	uint8
	code	uint8

	checksum	uint16
	بيانات		uint32
}

func (نفسه *Tإنترنتتحكمالرسالةالبروتوكولالرسالة) Init(buffer_2 Tإنترنتتحكمالرسالةالبروتوكولالرسالةbuffer) {
	نفسه.Tنوع = buffer_2.Tنوع
	نفسه.code = buffer_2.code

	نفسه.checksum = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer_2.checksum))
	نفسه.بيانات = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer_2.بيانات))
}

func (نفسه *Tإنترنتتحكمالرسالةالبروتوكولالرسالة) Sتحديدbuffer(buffer_2 *Tإنترنتتحكمالرسالةالبروتوكولالرسالةbuffer) {
	buffer_2.Tنوع = نفسه.Tنوع
	buffer_2.code = نفسه.code

	buffer_2.checksum = Unsignedinteger16toمصفوفة(نفسه.checksum)
	buffer_2.بيانات = Unsignedinteger32toمصفوفة(نفسه.بيانات)
}

type Icmphandler struct {
	Tإنترنتالبروتوكولhandler
}

var بروتوكول_رسائل_التحكم_بالشبكة_المترابطة *Tبروتوكول_رسائل_التحكم_بالشبكة_المترابطة

func (نفسه *Icmphandler) Oإنترنتالبروتوكولreceivewhen(المصدرipaddressشبكةبايتorder uint32, المقصدipaddressشبكةبايتorder uint32, بياناتالمؤشر uintptr, الحجم uint32) bool {
	return بروتوكول_رسائل_التحكم_بالشبكة_المترابطة.Oإنترنتالبروتوكولreceivewhen(المصدرipaddressشبكةبايتorder, المقصدipaddressشبكةبايتorder, بياناتالمؤشر, الحجم)
}

var iphandler Iإنترنتالبروتوكولhandler

type Tبروتوكول_رسائل_التحكم_بالشبكة_المترابطة struct {
}

func (نفسه *Tبروتوكول_رسائل_التحكم_بالشبكة_المترابطة) Init(backend Tمزود_بروتوكول_الشبكة_المترابطة, handler Iإنترنتالبروتوكولhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	بروتوكول_رسائل_التحكم_بالشبكة_المترابطة = نفسه
}
func (نفسه *Tبروتوكول_رسائل_التحكم_بالشبكة_المترابطة) Oإنترنتالبروتوكولreceivewhen(المصدرipaddressشبكةبايتorder uint32, المقصدipaddressشبكةبايتorder uint32, بياناتالمؤشر uintptr, الحجم uint32) bool {
	if الحجم < uint32(icmpالحجم) {
		return false
	}

	var buffer_2 *Tإنترنتتحكمالرسالةالبروتوكولالرسالةbuffer = (*Tإنترنتتحكمالرسالةالبروتوكولالرسالةbuffer)(Pointer(بياناتالمؤشر))
	var msg Tإنترنتتحكمالرسالةالبروتوكولالرسالة = Tإنترنتتحكمالرسالةالبروتوكولالرسالة{}
	msg.Init(*buffer_2)

	icmpطرفية.Mاطبع(([]byte)("icmp:OnInternet"))
	icmpطرفية.MUnsignedinteger16اطبع(uint16(msg.Tنوع))
	icmpطرفية.Mاطبع(([]byte)(":"))

	switch msg.Tنوع {
	case 0:
		icmpطرفية.Mاطبع(([]byte)("ping response from "))
		break

	case 8:
		icmpطرفية.Mاطبع(([]byte)("ping send "))
		msg.Tنوع = 0

		msg.checksum = 0
		msg.Sتحديدbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(بياناتالمؤشر)), uint32(icmpالحجم))

		msg.Sتحديدbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (نفسه *Tبروتوكول_رسائل_التحكم_بالشبكة_المترابطة) Echorequestأرسل(ipشبكةبايتorder uint32) bool {
	var بروتوكول_رسائل_التحكم_بالشبكة_المترابطة Tإنترنتتحكمالرسالةالبروتوكولالرسالة = Tإنترنتتحكمالرسالةالبروتوكولالرسالة{}

	var ذاكرةمدير = &Tذاكرةمدير{}
	var buffer_2 = (*Tإنترنتتحكمالرسالةالبروتوكولالرسالةbuffer)(ذاكرةمدير.Mتخصيص_الذاكرة(1024))

	بروتوكول_رسائل_التحكم_بالشبكة_المترابطة.Tنوع = 8
	بروتوكول_رسائل_التحكم_بالشبكة_المترابطة.code = 0
	بروتوكول_رسائل_التحكم_بالشبكة_المترابطة.بيانات = 0x3713
	بروتوكول_رسائل_التحكم_بالشبكة_المترابطة.checksum = 0
	بروتوكول_رسائل_التحكم_بالشبكة_المترابطة.Sتحديدbuffer(buffer_2)
	بروتوكول_رسائل_التحكم_بالشبكة_المترابطة.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpالحجم))
	بروتوكول_رسائل_التحكم_بالشبكة_المترابطة.Sتحديدbuffer(buffer_2)

	var بياناتالمؤشر uintptr = uintptr(Pointer(buffer_2))
	iphandler.Sأرسل(ipشبكةبايتorder, 0x01, بياناتالمؤشر, uint32(icmpالحجم))

	return false

}
