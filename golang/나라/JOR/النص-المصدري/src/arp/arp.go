/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "طرفية"
import . "إطار_شبكة_ذات_وسط_مشترك"
import . "أداة"

var arpطرفية Tطرفية = Tطرفية{}

type Arpالرسالةbuffer struct {
	العتادنوع		[2]byte
	البروتوكول		[2]byte
	العتادaddressالحجم	byte
	البروتوكولaddressالحجم	byte
	أمر			[2]byte

	المصدرmacaddress	[6]byte
	المصدرipaddress		[4]byte
	المقصدmacaddress	[6]byte
	المقصدipaddress		[4]byte
}

var arpmesgالحجم uint32 = (64+92+64)/8 + 2

type Arpالرسالة struct {
	العتادنوع		uint16
	البروتوكول		uint16
	العتادaddressالحجم	uint8
	البروتوكولaddressالحجم	uint8
	أمر			uint16

	المصدرmacaddress	uint64
	المصدرipaddress		uint32
	المقصدmacaddress	uint64
	المقصدipaddress		uint32
}

func (نفسه *Arpالرسالة) Init(buffer_2 *Arpالرسالةbuffer) {

	نفسه.العتادنوع = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer_2.العتادنوع))
	نفسه.البروتوكول = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer_2.البروتوكول))
	نفسه.العتادaddressالحجم = byte(buffer_2.العتادaddressالحجم)
	نفسه.البروتوكولaddressالحجم = byte(buffer_2.البروتوكولaddressالحجم)
	نفسه.أمر = Unsignedinteger16r(Aمصفوفةtounsignedinteger16(buffer_2.أمر))

	نفسه.المصدرmacaddress = Unsignedinteger48r(Aمصفوفةtounsignedinteger48(buffer_2.المصدرmacaddress))
	نفسه.المصدرipaddress = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer_2.المصدرipaddress))
	نفسه.المقصدmacaddress = Unsignedinteger48r(Aمصفوفةtounsignedinteger48(buffer_2.المقصدmacaddress))
	نفسه.المقصدipaddress = Unsignedinteger32r(Aمصفوفةtounsignedinteger32(buffer_2.المقصدipaddress))
}
func (نفسه *Arpالرسالة) Sتحديدbuffer(buffer_2 *Arpالرسالةbuffer) {
	buffer_2.العتادنوع = Unsignedinteger16toمصفوفة(نفسه.العتادنوع)
	buffer_2.البروتوكول = Unsignedinteger16toمصفوفة(نفسه.البروتوكول)
	buffer_2.العتادaddressالحجم = uint8(نفسه.العتادaddressالحجم)
	buffer_2.البروتوكولaddressالحجم = uint8(نفسه.البروتوكولaddressالحجم)

	buffer_2.أمر = Unsignedinteger16toمصفوفة(نفسه.أمر)
	buffer_2.المصدرmacaddress = Unsignedinteger48toمصفوفة(نفسه.المصدرmacaddress)
	buffer_2.المصدرipaddress = Unsignedinteger32toمصفوفة(نفسه.المصدرipaddress)
	buffer_2.المقصدmacaddress = Unsignedinteger48toمصفوفة(نفسه.المقصدmacaddress)
	buffer_2.المقصدipaddress = Unsignedinteger32toمصفوفة(نفسه.المقصدipaddress)
}

type Arpإيثرنتإطارhandler struct {
	Tإيثرنتإطارhandler
}

var arpprovider Arpprovider
var مزود_إطارات_الشبكة_ذات_الوسط_المشترك Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك

func (نفسه *Arpإيثرنتإطارhandler) Oإيثرنتإطارreceivewhen(بياناتالمؤشر uintptr, الحجم int) bool {
	arpطرفية.Mاطبعxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Oإيثرنتإطارreceivewhen(بياناتالمؤشر, uint32(الحجم))

}
func (نفسه *Arpإيثرنتإطارhandler) Sأرسل(المقصدmacbe uint64, بياناتالمؤشر uintptr, الحجم uint32) {
	arpطرفية.Mاطبعxy([]byte("arp send:"), 0, 24)
	var إيثرنتنوعbe = Unsignedinteger16r(0x0806)
	نفسه.Tإيثرنتإطارhandler.Sإطارأرسل(المقصدmacbe, إيثرنتنوعbe, بياناتالمؤشر, الحجم)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	الأرقامcacheentry	int

	handler	Iإيثرنتإطارhandler
}

var handler Iإيثرنتإطارhandler

func (نفسه *Arpprovider) Init(backend Tمزود_إطارات_الشبكة_ذات_الوسط_المشترك, userhandler Iإيثرنتإطارhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sتحديدhandler(userhandler, 0x0806)
	نفسه.الأرقامcacheentry = 0
	arpprovider = *نفسه

}

func (نفسه *Arpprovider) Oإيثرنتإطارreceivewhen(بياناتالمؤشر uintptr, الحجم uint32) bool {

	if الحجم < arpmesgالحجم {
		return false
	}
	var arpbuffer *Arpالرسالةbuffer = (*Arpالرسالةbuffer)(Pointer(بياناتالمؤشر))
	var arp Arpالرسالة = Arpالرسالة{}
	arp.Init(arpbuffer)

	if arp.العتادنوع == 0x0100 {

		if arp.البروتوكول == 0x0008 && arp.العتادaddressالحجم == 6 && arp.البروتوكولaddressالحجم == 4 && uint64(arp.المقصدipaddress) == handler.Getipaddress() {

			arpطرفية.Mاطبع([]byte("arp onetherframe"))
			arpطرفية.MUnsignedinteger16اطبع(arp.البروتوكول)
			arpطرفية.Mاطبع([]byte(":"))
			arpطرفية.MUnsignedinteger64اطبع(uint64(arp.المقصدmacaddress))
			arpطرفية.Mاطبع([]byte(":"))
			arpطرفية.MUnsignedinteger16اطبع(arp.أمر)
			arpطرفية.Mاطبع([]byte(":"))
			arpطرفية.MUnsignedinteger64اطبع(handler.Getmacaddress())

			switch arp.أمر {
			case 0x0100:

				if نفسه.Getmacfromcache(arp.المصدرipaddress) == 0xFFFFFFFFFFFF {
					if نفسه.الأرقامcacheentry < 128 {
						نفسه.Ipcache[نفسه.الأرقامcacheentry] = arp.المصدرipaddress
						نفسه.Maccache[نفسه.الأرقامcacheentry] = arp.المصدرmacaddress
						نفسه.الأرقامcacheentry++
					}
				}
				arp.أمر = 0x0200
				arp.المقصدipaddress = arp.المصدرipaddress
				arp.المقصدmacaddress = arp.المصدرmacaddress
				arp.المصدرipaddress = uint32(handler.Getipaddress())
				arp.المصدرmacaddress = handler.Getmacaddress()
				arp.Sتحديدbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpطرفية.Mاطبع(([]byte)("self.numCacheEntries"))

				if نفسه.الأرقامcacheentry < 128 {
					نفسه.Ipcache[نفسه.الأرقامcacheentry] = arp.المصدرipaddress
					نفسه.Maccache[نفسه.الأرقامcacheentry] = arp.المصدرmacaddress
					نفسه.الأرقامcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (نفسه *Arpprovider) Broadcastmacaddress(Ipشبكةبايتorder uint32) {

	var arp Arpالرسالة = Arpالرسالة{}
	arp.العتادنوع = 0x0100
	arp.البروتوكول = 0x0008
	arp.العتادaddressالحجم = 6
	arp.البروتوكولaddressالحجم = 4
	arp.أمر = 0x0200

	arp.المصدرipaddress = uint32(handler.Getipaddress())

	arp.المقصدmacaddress = نفسه.Rحل(Ipشبكةبايتorder)
	arp.المقصدipaddress = Ipشبكةبايتorder
	arpطرفية.Mاطبعxy([]byte("broad mac"), 0, 15)

	arp.المصدرmacaddress = handler.Getmacaddress()

	var arpbuffer Arpالرسالةbuffer = Arpالرسالةbuffer{}
	arp.Sتحديدbuffer(&arpbuffer)

	var مرجع_عنوان uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sأرسل(arp.المقصدmacaddress, مرجع_عنوان, arpmesgالحجم)
}
func (نفسه *Arpprovider) Requestmacaddress(Ipشبكةبايتorder uint32) {

	var arp Arpالرسالة = Arpالرسالة{}
	arp.العتادنوع = 0x0100

	arp.البروتوكول = 0x0008
	arp.العتادaddressالحجم = 6
	arp.البروتوكولaddressالحجم = 4
	arp.أمر = 0x0100

	arp.المصدرmacaddress = handler.Getmacaddress()
	arp.المصدرipaddress = uint32(handler.Getipaddress())

	arp.المقصدmacaddress = 0xFFFFFFFFFFFF
	arp.المقصدipaddress = Ipشبكةبايتorder

	var arpbuffer Arpالرسالةbuffer = Arpالرسالةbuffer{}
	arp.Sتحديدbuffer(&arpbuffer)

	var مرجع_عنوان uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sأرسل(arp.المقصدmacaddress, مرجع_عنوان, arpmesgالحجم)
}
func (نفسه *Arpprovider) Tتجريباطبع(بيانات *[]byte, الحجم uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(بيانات))
	arpطرفية.Mاطبعxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpطرفية.MHexadecimalاطبع(buffer_2[i])
		arpطرفية.Mاطبع([]byte(":"))
	}
	arpطرفية.Mاطبع([]byte("]"))
}

func (نفسه *Arpprovider) Getmacfromcache(Ipشبكةبايتorder uint32) uint64 {
	for i := 0; i < نفسه.الأرقامcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpطرفية.Mاطبع(([]byte)("["))
		arpطرفية.MUnsignedinteger32اطبع(نفسه.Ipcache[i])
		arpطرفية.Mاطبع(([]byte)(":"))
		arpطرفية.MUnsignedinteger32اطبع(Ipشبكةبايتorder)
		arpطرفية.Mاطبع(([]byte)(":"))
		arpطرفية.Mاطبع(([]byte)(":"))
		arpطرفية.MUnsignedinteger64اطبع(نفسه.Maccache[i])
		arpطرفية.Mاطبع(([]byte)("]\n"))

		if نفسه.Ipcache[i] == Ipشبكةبايتorder {
			arpطرفية.Mاطبع([]byte("getmacfromcache"))
			return نفسه.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (نفسه *Arpprovider) Rحل(Ipشبكةبايتorder uint32) uint64 {
	var result uint64 = نفسه.Getmacfromcache(Ipشبكةبايتorder)
	if result == 0xFFFFFFFFFFFF {
		نفسه.Requestmacaddress(Ipشبكةبايتorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = نفسه.Getmacfromcache(Ipشبكةبايتorder)

	}

	return result
}
