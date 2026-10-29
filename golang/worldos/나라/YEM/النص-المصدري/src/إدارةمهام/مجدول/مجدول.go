/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package مجدول

import . "unsafe"
import . "reflect"

import . "طرفية"
import . "gdt"
import . "منفذ"
import . "أداة/قائمة"

import . "مقاطعة"
import . "إدارةمهام/خيطتنفيذ"
import . "إدارةمهام/tss"
import . "متعددإدارةمهام"
import mem "ذاكرةمدير"

const Sمجدولالتردد = 1
const Kنواةheapابدأ = 1024 * 1024
const مجدولتنقيح = false
const pitالتردد = 100

var قائمة Linkedقائمة

type Sمجدولبيانات struct {
	التردد		uint32
	tickcount	uint32

	switchforced	bool

	Eمفعل	bool

	الحاليخيطتنفيذ	*Tخيطتنفيذ
	tss		*Tssentry
}

var scheبيانات Sمجدولبيانات = Sمجدولبيانات{}

func (نفسه *Sمجدولبيانات) Init() {
	scheبيانات.tickcount = 0
	scheبيانات.التردد = Sمجدولالتردد
	scheبيانات.الحاليخيطتنفيذ = nil
	scheبيانات.Eمفعل = false
	scheبيانات.switchforced = false

}

var طرفية_2 = Tطرفية{}
var الحاليخيطتنفيذفهرس int = 0
var التاليعمليةالهوية uint32 = 1

func Allocateالهوية() uint32 {
	الهوية_2 := التاليعمليةالهوية
	التاليعمليةالهوية++
	return الهوية_2
}

func (نفسه *Sمجدولبيانات) Getالتاليجاهزخيطتنفيذ() *Tخيطتنفيذ {
	if قائمة.Sالحجم_2 <= 0 {
		return nil
	}

	if scheبيانات.الحاليخيطتنفيذ != nil {
		الحاليخيطتنفيذفهرس = قائمة.Iفهرسof(uintptr(Pointer(scheبيانات.الحاليخيطتنفيذ)))
		if الحاليخيطتنفيذفهرس < 0 {
			الحاليخيطتنفيذفهرس = 0
		}
	} else {
		الحاليخيطتنفيذفهرس = -1
	}

	for checked := 0; checked < قائمة.Sالحجم_2; checked++ {
		الحاليخيطتنفيذفهرس++
		if الحاليخيطتنفيذفهرس >= قائمة.Sالحجم_2 {
			الحاليخيطتنفيذفهرس = 0
		}
		خيطتنفيذ := (*Tخيطتنفيذ)(قائمة.Getat(الحاليخيطتنفيذفهرس))
		if خيطتنفيذ != nil && خيطتنفيذ.Tخيطتنفيذالحالة != Blocked && خيطتنفيذ.Tخيطتنفيذالحالة != Sمتوقفة {
			if مجدولتنقيح {
				طرفية_2.Mاطبع("ti:")
				طرفية_2.MUnsignedinteger32اطبع(uint32(الحاليخيطتنفيذفهرس))
				طرفية_2.Mاطبع(":")
				طرفية_2.MUnsignedinteger32اطبع(uint32(uintptr(Pointer(خيطتنفيذ))))
			}
			return خيطتنفيذ
		}
	}
	return scheبيانات.الحاليخيطتنفيذ

}
func (نفسه *Sمجدول) Aأضفخيطتنفيذ(خيطتنفيذ *Tخيطتنفيذ) {
	if خيطتنفيذ == nil {
		return
	}
	قائمة.Mإضافة_إلى_نهاية_القائمة(uintptr(Pointer(خيطتنفيذ)))
}
func Aأضفrunnableخيطتنفيذ(خيطتنفيذ *Tخيطتنفيذ) {
	if خيطتنفيذ == nil {
		return
	}
	قائمة.Mإضافة_إلى_نهاية_القائمة(uintptr(Pointer(خيطتنفيذ)))
}

func Cالحاليالهوية() uint32 {
	if scheبيانات.الحاليخيطتنفيذ == nil || scheبيانات.الحاليخيطتنفيذ.Pالهوية == 0 {
		return 1
	}
	return scheبيانات.الحاليخيطتنفيذ.Pالهوية
}

func Cالحاليأبالهوية() uint32 {
	if scheبيانات.الحاليخيطتنفيذ == nil {
		return 0
	}
	return scheبيانات.الحاليخيطتنفيذ.Pأبالهوية
}
func (نفسه *Sمجدول) Rأزلخيطتنفيذ(خيطتنفيذ *Tخيطتنفيذ) {
	قائمة.Rأزل(uintptr(Pointer(خيطتنفيذ)))
}

func (نفسه *Sمجدول) Rأزلخيطتنفيذat(فهرس int) {
	قائمة.Rأزلat(فهرس)
}

type Sمجدول struct {
	Tمقاطعةhandler
}

func (نفسه *Sمجدول) Init(مدير *Tمقاطعةمدير, mem *mem.Tذاكرةمدير, tss *Tssentry) {
	scheبيانات.Init()
	scheبيانات.tss = tss
	initpit(pitالتردد)

	قائمة = Linkedقائمة{}
	قائمة.Init(mem)
	طرفية_2.Mاطبع("list:")
	طرفية_2.MUnsignedinteger32اطبع(uint32(uintptr(Pointer(&قائمة))))

	مقاطعةhandler = التعاملمقاطعة
	var address uintptr
	address = uintptr(Pointer(&مقاطعةhandler))
	نفسه.Tمقاطعةhandler.Init(0x20, uintptr(Pointer(مدير)), address)
}

func (نفسه *Sمجدول) Eمفعل(مفعل bool) {
	scheبيانات.Eمفعل = مفعل
}

func initpit(التردد uint32) {
	if التردد == 0 {
		return
	}
	divisor := uint32(1193180) / التردد
	Pمنفذكتابةبايت(0x43, 0x36)
	Pمنفذكتابةبايت(0x40, uint8(divisor&0xFF))
	Pمنفذكتابةبايت(0x40, uint8((divisor>>8)&0xFF))
}

func تحديدds(dssegment uint32)
func تحديدgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func استعدfpregs(buffer_2 uintptr)

var jmpمستخدم uint32 = 0
var مقاطعةhandler func(uint32) uint32

func schedulestack(fn func())
func تحديدcr3(address uint32)
func getcr3() uint32

func التعاملمقاطعة(esp uint32) uint32 {

	scheبيانات.tickcount++

	if مجدولتنقيح {
		طرفية_2.Mاطبعxy(([]byte)("sche1:"), 1, 17)

		طرفية_2.Mاطبع(":")
		طرفية_2.MUnsignedinteger32اطبع(esp)
		طرفية_2.Mاطبع(":")

		طرفية_2.MUnsignedinteger32اطبع(uint32(scheبيانات.tickcount))
		طرفية_2.Mاطبع(":")
		طرفية_2.MUnsignedinteger32اطبع(Kنواةheapابدأ)
	}

	if scheبيانات.tickcount == scheبيانات.التردد {
		scheبيانات.tickcount = 0

		if قائمة.Sالحجم_2 > 0 && scheبيانات.Eمفعل == true {
			var التاليخيطتنفيذ = scheبيانات.Getالتاليجاهزخيطتنفيذ()
			if التاليخيطتنفيذ == nil {
				return esp
			}
			if scheبيانات.الحاليخيطتنفيذ == nil {
				MEmergencyالسجلسلسلة("\nSCHED first esp=")
				MEmergencyالسجلunsignedinteger32(esp)
				MEmergencyالسجلسلسلة(" thread=")
				MEmergencyالسجلunsignedinteger32(uint32(uintptr(Pointer(التاليخيطتنفيذ))))
				MEmergencyالسجلسلسلة(" cpu=")
				MEmergencyالسجلunsignedinteger32(uint32(uintptr(Pointer(التاليخيطتنفيذ.Cالمعالجالحالة))))
				MEmergencyالسجلسلسلة(" state=")
				MEmergencyالسجلunsignedinteger32(uint32(التاليخيطتنفيذ.Tخيطتنفيذالحالة))
				MEmergencyالسجلسلسلة(" eip=")
				MEmergencyالسجلunsignedinteger32(التاليخيطتنفيذ.Cالمعالجالحالة.Eip)
				MEmergencyالسجلسلسلة(" cs=")
				MEmergencyالسجلunsignedinteger32(التاليخيطتنفيذ.Cالمعالجالحالة.Cs)
				MEmergencyالسجلسلسلة("\n")
			}

			if esp >= Kنواةheapابدأ && scheبيانات.الحاليخيطتنفيذ != nil {
				scheبيانات.الحاليخيطتنفيذ.Cالمعالجالحالة = (*Tcpuالحالة)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(scheبيانات.الحاليخيطتنفيذ.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				scheبيانات.الحاليخيطتنفيذ.Fpuoffset = offset
				backupfpregs(address + offset)
				if مجدولتنقيح {
					طرفية_2.Mاطبع(([]byte)("backup"))
					طرفية_2.MUnsignedinteger32اطبع(esp)
				}
			}

			address := uintptr(Pointer(&(التاليخيطتنفيذ.Fpubuffer)))
			offset := التاليخيطتنفيذ.Fpuoffset
			if offset != 0xffffffff {
				استعدfpregs(address + offset)
				if مجدولتنقيح {
					طرفية_2.Mاطبع(([]byte)("restore"))
				}
			}

			scheبيانات.الحاليخيطتنفيذ = التاليخيطتنفيذ

			if scheبيانات.الحاليخيطتنفيذ.Tخيطتنفيذالحالة == Sوقتالبداية {
				scheبيانات.الحاليخيطتنفيذ.Tخيطتنفيذالحالة = Rجاهز

				Initialخيطتنفيذمستخدمjump(scheبيانات.الحاليخيطتنفيذ)
				return esp
			}

			esp = uint32(uintptr(Pointer(التاليخيطتنفيذ.Cالمعالجالحالة)))
			if التاليخيطتنفيذ.Stack != 0 {
				scheبيانات.tss.Sتحديدstack(Segنواةبيانات, التاليخيطتنفيذ.Stack+Tخيطتنفيذstackالحجم)
			}

			تحديدcr3(التاليخيطتنفيذ.Pصفحةدليلentry)
			تحديدgs(التاليخيطتنفيذ.Cالمعالجالحالة.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableعددصحيح()

func getesp() uint32
func خيطتنفيذخروجloop()

func تحديدخيطتنفيذخروجloopالحالة(المعالجالحالة *Tcpuالحالة) {
	المعالجالحالة.Eip = uint32(ValueOf(خيطتنفيذخروجloop).Pointer())
	المعالجالحالة.Cs = Segنواةcode
	المعالجالحالة.Ds = Segنواةبيانات
	المعالجالحالة.Es = Segنواةبيانات
	المعالجالحالة.Fs = Segنواةبيانات
	المعالجالحالة.Gs = Segنواةgs
	المعالجالحالة.Ss = Segنواةبيانات
	المعالجالحالة.Eflags = 0x202
}

func Sأوقفالحاليخيطتنفيذ(المعالجالحالة *Tcpuالحالة) *Tcpuالحالة {
	if scheبيانات.الحاليخيطتنفيذ == nil {
		تحديدخيطتنفيذخروجloopالحالة(المعالجالحالة)
		return المعالجالحالة
	}

	متوقفةخيطتنفيذ := scheبيانات.الحاليخيطتنفيذ
	for i := 0; i < قائمة.Sالحجم_2; i++ {
		خيطتنفيذ := (*Tخيطتنفيذ)(قائمة.Getat(i))
		if خيطتنفيذ != nil && خيطتنفيذ.Cالمعالجالحالة == المعالجالحالة {
			متوقفةخيطتنفيذ = خيطتنفيذ
			break
		}
	}
	متوقفةخيطتنفيذ.Cالمعالجالحالة = المعالجالحالة
	متوقفةخيطتنفيذ.Tخيطتنفيذالحالة = Sمتوقفة
	scheبيانات.الحاليخيطتنفيذ = متوقفةخيطتنفيذ

	التاليخيطتنفيذ := scheبيانات.Getالتاليجاهزخيطتنفيذ()
	if التاليخيطتنفيذ == nil || التاليخيطتنفيذ == متوقفةخيطتنفيذ || التاليخيطتنفيذ.Cالمعالجالحالة == nil || التاليخيطتنفيذ.Cالمعالجالحالة == المعالجالحالة {
		تحديدخيطتنفيذخروجloopالحالة(المعالجالحالة)
		return المعالجالحالة
	}

	scheبيانات.الحاليخيطتنفيذ = التاليخيطتنفيذ
	if التاليخيطتنفيذ.Stack != 0 && scheبيانات.tss != nil {
		scheبيانات.tss.Sتحديدstack(Segنواةبيانات, التاليخيطتنفيذ.Stack+Tخيطتنفيذstackالحجم)
	}
	تحديدcr3(التاليخيطتنفيذ.Pصفحةدليلentry)
	تحديدgs(التاليخيطتنفيذ.Cالمعالجالحالة.Gs)
	return التاليخيطتنفيذ.Cالمعالجالحالة
}

func Initialخيطتنفيذمستخدمjump(خيطتنفيذ *Tخيطتنفيذ) {

	Disableعددصحيح()

	scheبيانات.tss.Sتحديدstack(Segنواةبيانات, خيطتنفيذ.Stack+Tخيطتنفيذstackالحجم)

	تحديدcr3(خيطتنفيذ.Pصفحةدليلentry)
	تحديدgs(خيطتنفيذ.Cالمعالجالحالة.Gs)

	scheبيانات.الحاليخيطتنفيذ = خيطتنفيذ
	scheبيانات.Eمفعل = true

	eip := خيطتنفيذ.Cالمعالجالحالة.Eip
	مستخدمesp := خيطتنفيذ.Uمستخدمstack_2 + خيطتنفيذ.Uمستخدمstackالحجم_2
	eflags := خيطتنفيذ.Cالمعالجالحالة.Eflags
	cs := خيطتنفيذ.Cالمعالجالحالة.Cs
	esp := scheبيانات.tss.Getesp0()

	طرفية_2.Mاطبع(([]byte)("jump["))
	طرفية_2.MUnsignedinteger32اطبع(eip)
	طرفية_2.Mاطبع(([]byte)(":"))
	طرفية_2.MUnsignedinteger32اطبع(مستخدمesp)
	طرفية_2.Mاطبع(([]byte)(":"))
	طرفية_2.MUnsignedinteger32اطبع(eflags)
	طرفية_2.Mاطبع(([]byte)(":"))
	طرفية_2.MUnsignedinteger32اطبع(cs)
	طرفية_2.Mاطبع(([]byte)(":"))

	طرفية_2.MUnsignedinteger32اطبع(esp)
	طرفية_2.Mاطبع(([]byte)("]"))

	userprocentry := خيطتنفيذ.Cالمعالجالحالة.Ecx
	الاختصارالعامoffsetجدول_2 := خيطتنفيذ.Cالمعالجالحالة.Edx
	dynamic := خيطتنفيذ.Cالمعالجالحالة.Esi

	Pمنفذكتابةبايت(0x20, 0x20)
	jumpusermodeiret(eip, مستخدمesp, eflags, userprocentry, الاختصارالعامoffsetجدول_2, dynamic)
	طرفية_2.Mاطبع(([]byte)("usermode end"))
}
func اطبعesp(esp uint32) {
	طرفية_2.Mاطبع(([]byte)("esp["))
	طرفية_2.MUnsignedinteger32اطبع(esp)
}
