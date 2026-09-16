/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package بروتوكول_الشبكة_المترابطة_4

import . "unsafe"
import . "أداة"
import . "طرفية"
import . "إطار_شبكة_ذات_وسط_مشترك"
import . "arp"

var ipطرفية Tطرفية = Tطرفية{}

type Tإنترنتالبروتوكولv4الرسالةbuffer struct {
	lenver		byte
	tos		byte
	المجموعالمدة	[2]byte

	ident		[2]byte
	خياراتandoffset	[2]byte

	الوقتtolive	byte
	البروتوكول	byte
	checksum	[2]byte

	المصدرipaddress	[4]byte
	المقصدipaddress	[4]byte
}

var ipالحجم uint8 = (4 + 4 + 4 + 8)

type Tإنترنتالبروتوكولv4الرسالة struct {
	ترويسةالمدة	uint8
	إصدار		uint8
	tos		uint8
	المجموعالمدة	uint16

	ident		uint16
	خياراتandoffset	uint16

	الوقتtolive	uint8
	البروتوكول	uint8
	checksum	uint16

	المصدرipaddress	uint32
	المقصدipaddress	uint32
}

func (نفسه *Tإنترنتالبروتوكولv4الرسالة) Init(buffer_2 Tإنترنتالبروتوكولv4الرسالةbuffer) {

	نفسه.إصدار = ((buffer_2.lenver & 0xF0) >> 4)
	نفسه.ترويسةالمدة = buffer_2.lenver & 0x0F
	نفسه.tos = buffer_2.tos
	نفسه.المجموعالمدة = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer_2.المجموعالمدة))

	نفسه.ident = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer_2.ident))
	نفسه.خياراتandoffset = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer_2.خياراتandoffset))

	نفسه.الوقتtolive = buffer_2.الوقتtolive
	نفسه.البروتوكول = buffer_2.البروتوكول
	نفسه.checksum = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer_2.checksum))

	نفسه.المصدرipaddress = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer_2.المصدرipaddress))
	نفسه.المقصدipaddress = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer_2.المقصدipaddress))

}
func (نفسه *Tإنترنتالبروتوكولv4الرسالة) Sتحديدbuffer(buffer_2 *Tإنترنتالبروتوكولv4الرسالةbuffer) {

	buffer_2.lenver = byte(((نفسه.إصدار & 0x0F) << 4) | (نفسه.ترويسةالمدة & 0x0F))
	buffer_2.tos = نفسه.tos
	buffer_2.المجموعالمدة = Unsignedinteger16toمصفوفة(نفسه.المجموعالمدة)

	buffer_2.ident = Unsignedinteger16toمصفوفة(نفسه.ident)
	buffer_2.خياراتandoffset = Unsignedinteger16toمصفوفة(نفسه.خياراتandoffset)

	buffer_2.الوقتtolive = نفسه.الوقتtolive
	buffer_2.البروتوكول = نفسه.البروتوكول
	buffer_2.checksum = Unsignedinteger16toمصفوفة(نفسه.checksum)

	buffer_2.المصدرipaddress = Unsignedinteger32toمصفوفة(نفسه.المصدرipaddress)
	buffer_2.المقصدipaddress = Unsignedinteger32toمصفوفة(نفسه.المقصدipaddress)

}

type Iإنترنتالبروتوكولhandler interface {
	Init(backend Tمزود_بروتوكول_الشبكة_المترابطة, pihandler Iإنترنتالبروتوكولhandler, pالبروتوكول uint8)
	Oإنترنتالبروتوكولreceivewhen(المصدرipaddressشبكةبايتorder uint32, المقصدipaddressشبكةبايتorder uint32, بياناتالمؤشر uintptr, الحجم uint32) bool
	Sأرسل(المقصدipaddressشبكةبايتorder uint32, pالبروتوكول uint8, بياناتالمؤشر uintptr, الحجم uint32)
	Providerget() *Tمزود_بروتوكول_الشبكة_المترابطة
}

type Tإنترنتالبروتوكولhandler struct {
}

var ipإيثرنتإطارhandler Ipإيثرنتإطارhandler = Ipإيثرنتإطارhandler{}
var البروتوكول uint8

func (نفسه *Tإنترنتالبروتوكولhandler) Init(backend Tمزود_بروتوكول_الشبكة_المترابطة, pihandler Iإنترنتالبروتوكولhandler, pالبروتوكول uint8) {
	البروتوكول = pالبروتوكول
	handler_2[البروتوكول] = pihandler
}
func (نفسه *Tإنترنتالبروتوكولhandler) Oإنترنتالبروتوكولreceivewhen(المصدرipaddressشبكةبايتorder uint32, المقصدipaddressشبكةبايتorder uint32, بياناتالمؤشر uintptr, الحجم uint32) bool {
	ipطرفية.Mاطبع(([]byte)("ipHandler:OnInternet"))
	return false
}
func (نفسه *Tإنترنتالبروتوكولhandler) Sأرسل(المقصدipaddressشبكةبايتorder uint32, pالبروتوكول uint8, بياناتالمؤشر uintptr, الحجم uint32) {

	مزود_بروتوكول_الشبكة_المترابطة.Sأرسل(المقصدipaddressشبكةبايتorder, pالبروتوكول, بياناتالمؤشر, الحجم)
}
func (نفسه *Tإنترنتالبروتوكولhandler) Providerget() *Tمزود_بروتوكول_الشبكة_المترابطة {
	return &مزود_بروتوكول_الشبكة_المترابطة
}

type Ipإيثرنتإطارhandler struct {
	Tإيثرنتإطارhandler
}

var مزود_بروتوكول_الشبكة_المترابطة Tمزود_بروتوكول_الشبكة_المترابطة

func (نفسه *Ipإيثرنتإطارhandler) Oإيثرنتإطارreceivewhen(بياناتالمؤشر uintptr, الحجم int) bool {
	ipطرفية.Mاطبع(([]byte)("iphandler:onEtherfameRecv\n"))
	return مزود_بروتوكول_الشبكة_المترابطة.Oإيثرنتإطارreceivewhen(بياناتالمؤشر, uint32(الحجم))

}

func (نفسه *Ipإيثرنتإطارhandler) Sأرسل(المقصدipaddressشبكةبايتorder uint64, بياناتالمؤشر uintptr, الحجم uint32) {
	ipطرفية.Mاطبع(([]byte)("ipefhandler:send\n"))
	var إيثرنتنوعbe = Unsignedinteger16r(0x0800)
	نفسه.Tإيثرنتإطارhandler.Sإطارأرسل(المقصدipaddressشبكةبايتorder, إيثرنتنوعbe, بياناتالمؤشر, الحجم)

}

var handler_2 [255]Iإنترنتالبروتوكولhandler

type Tمزود_بروتوكول_الشبكة_المترابطة struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler Iإيثرنتإطارhandler

func (نفسه *Tمزود_بروتوكول_الشبكة_المترابطة) Init(pefprovider Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك, pefhandler Iإيثرنتإطارhandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Sتحديدhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	نفسه.arpprovider = arp
	نفسه.Gatewayip = gatewayip
	نفسه.Subnetmask = subnetmask
	مزود_بروتوكول_الشبكة_المترابطة = *نفسه
}
func (نفسه *Tمزود_بروتوكول_الشبكة_المترابطة) Oإيثرنتإطارreceivewhen(إيثرنتإطارpayload uintptr, الحجم uint32) bool {
	if الحجم < uint32(ipالحجم) {
		return false
	}

	var buffer_2 *Tإنترنتالبروتوكولv4الرسالةbuffer = (*Tإنترنتالبروتوكولv4الرسالةbuffer)(Pointer(إيثرنتإطارpayload))
	var إنترنتالبروتوكولالرسالة Tإنترنتالبروتوكولv4الرسالة
	إنترنتالبروتوكولالرسالة.Init(*buffer_2)

	var reply bool = false

	if إنترنتالبروتوكولالرسالة.المقصدipaddress == uint32(efhandler.Getipaddress()) {

		var المدة uint32 = uint32(إنترنتالبروتوكولالرسالة.المجموعالمدة)
		if المدة > الحجم {
			المدة = الحجم
		}
		if handler_2[إنترنتالبروتوكولالرسالة.البروتوكول] != nil {
			reply = handler_2[إنترنتالبروتوكولالرسالة.البروتوكول].Oإنترنتالبروتوكولreceivewhen(إنترنتالبروتوكولالرسالة.المصدرipaddress, إنترنتالبروتوكولالرسالة.المقصدipaddress, إيثرنتإطارpayload+uintptr(4*إنترنتالبروتوكولالرسالة.ترويسةالمدة), uint32(المدة-uint32(4*إنترنتالبروتوكولالرسالة.ترويسةالمدة)))

		}
	}

	if reply {

		var temporary = إنترنتالبروتوكولالرسالة.المقصدipaddress
		إنترنتالبروتوكولالرسالة.المقصدipaddress = إنترنتالبروتوكولالرسالة.المصدرipaddress
		إنترنتالبروتوكولالرسالة.المصدرipaddress = temporary

		إنترنتالبروتوكولالرسالة.الوقتtolive = 0x40
		إنترنتالبروتوكولالرسالة.checksum = 0

		إنترنتالبروتوكولالرسالة.Sتحديدbuffer(buffer_2)
		إنترنتالبروتوكولالرسالة.checksum = نفسه.Checksum((*([4096]uint16))(Pointer(إيثرنتإطارpayload)), uint32(4*إنترنتالبروتوكولالرسالة.ترويسةالمدة))

		إنترنتالبروتوكولالرسالة.Sتحديدbuffer(buffer_2)

	}

	ipطرفية.Mاطبع(([]byte)("ipmessage"))
	ipطرفية.MUnsignedinteger32اطبع(إنترنتالبروتوكولالرسالة.المصدرipaddress)
	ipطرفية.Mاطبع(([]byte)(":"))
	ipطرفية.MUnsignedinteger32اطبع(إنترنتالبروتوكولالرسالة.المقصدipaddress)
	ipطرفية.Mاطبع(([]byte)(":"))
	ipطرفية.MUnsignedinteger16اطبع(uint16(إنترنتالبروتوكولالرسالة.ترويسةالمدة))
	ipطرفية.Mاطبع(([]byte)(":"))
	ipطرفية.MUnsignedinteger16اطبع(uint16(إنترنتالبروتوكولالرسالة.إصدار))
	ipطرفية.Mاطبع(([]byte)(":"))
	ipطرفية.MUnsignedinteger16اطبع(إنترنتالبروتوكولالرسالة.المجموعالمدة)
	ipطرفية.Mاطبع(([]byte)(":"))
	ipطرفية.MUnsignedinteger32اطبع(uint32(efhandler.Getipaddress()))
	ipطرفية.Mاطبع(([]byte)(":"))
	ipطرفية.Mاطبع(([]byte)("\n"))

	return reply

}
func (نفسه *Tمزود_بروتوكول_الشبكة_المترابطة) Sأرسل(المقصدipaddressشبكةبايتorder uint32, البروتوكول uint8, بياناتالمؤشر uintptr, الحجم uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tإنترنتالبروتوكولv4الرسالةbuffer = (*Tإنترنتالبروتوكولv4الرسالةbuffer)(Pointer(&buffer1_2))
	var الرسالة Tإنترنتالبروتوكولv4الرسالة = Tإنترنتالبروتوكولv4الرسالة{}
	الرسالة.إصدار = 4
	الرسالة.ترويسةالمدة = ipالحجم / 4
	الرسالة.tos = 0
	الرسالة.المجموعالمدة = Unsignedinteger16r(uint16(الحجم + uint32(ipالحجم)))

	الرسالة.ident = 0x0100
	الرسالة.خياراتandoffset = 0x0040
	الرسالة.الوقتtolive = 0x40
	الرسالة.البروتوكول = البروتوكول

	الرسالة.المقصدipaddress = المقصدipaddressشبكةبايتorder

	الرسالة.المصدرipaddress = uint32(efhandler.Getipaddress())

	الرسالة.checksum = 0

	الرسالة.Sتحديدbuffer(buffer_2)
	الرسالة.checksum = نفسه.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipالحجم))
	الرسالة.Sتحديدbuffer(buffer_2)

	var بياناتbuffer_2 [4096]byte = *(*([4096]byte))(Pointer(بياناتالمؤشر))

	for i := 0; i < int(الحجم); i++ {

		buffer1_2[i+int(ipالحجم)] = بياناتbuffer_2[i]
	}

	ipطرفية.Mاطبعxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(الحجم)+int(ipالحجم); i++ {
		ipطرفية.MHexadecimalاطبع(buffer1_2[i])
	}
	ipطرفية.Mاطبع(([]byte)(":"))
	ipطرفية.Mاطبع(([]byte)("]\n"))

	var التاليhopipaddressشبكةبايتorder uint32 = المقصدipaddressشبكةبايتorder
	if (المقصدipaddressشبكةبايتorder & نفسه.Subnetmask) != (الرسالة.المصدرipaddress & نفسه.Subnetmask) {
		التاليhopipaddressشبكةبايتorder = نفسه.Gatewayip
	}

	var أرسلبياناتالمؤشر = uintptr(Pointer(&buffer1_2))
	ipطرفية.MUnsignedinteger32اطبع(التاليhopipaddressشبكةبايتorder)

	var إيثرنتنوعbe = Unsignedinteger16r(0x0800)
	efhandler.Sإطارأرسل(نفسه.arpprovider.Rحل(التاليhopipaddressشبكةبايتorder), إيثرنتنوعbe, أرسلبياناتالمؤشر, uint32(ipالحجم)+uint32(الحجم))

}
func (نفسه *Tمزود_بروتوكول_الشبكة_المترابطة) Checksum(pبيانات *[4096]uint16, المدةداخلبايت uint32) uint16 {
	var بيانات [4096]uint16 = *pبيانات
	var temporary uint32 = 0
	var بياناتبايت [4096]byte = *(*([4096]byte))(Pointer(&بيانات))
	if (المدةداخلبايت % 2) != 0 {
		temporary += uint32(uint16(بياناتبايت[المدةداخلبايت-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (نفسه *Tمزود_بروتوكول_الشبكة_المترابطة) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
