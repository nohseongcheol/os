/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Tخيطتنفيذ_2

import . "unsafe"
import . "reflect"
import . "gdt"
import . "طرفية"
import . "متعددإدارةمهام"
import mem "ذاكرةمدير"
import . "افتراضيذاكرة"

const (
	Blocked		= 1
	Rجاهز		= 2
	Sمتوقفة		= 3
	Sوقتالبداية	= 4
)

const Tخيطتنفيذstackالحجم = 32 * 1024

type Tخيطتنفيذ struct {
	Cالمعالجالحالة		*Tcpuالحالة
	Stack			uint32
	Uمستخدمstack_2		uint32
	Uمستخدمstackالحجم_2	uint32
	Pالهوية			uint32
	Pأبالهوية		uint32

	Pصفحةدليلentry	uint32

	Tخيطتنفيذالحالة	uint8
	Blockedالحالة	uint8

	الوقتdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Isنواة		bool
}

func (نفسه *Tخيطتنفيذ) Nجديد() {
}

type Tخيطتنفيذhelper struct {
	mem *mem.Tذاكرةمدير
}

var طرفية_2 = Tطرفية{}

func (نفسه *Tخيطتنفيذhelper) Init(mem *mem.Tذاكرةمدير) {
	نفسه.mem = mem
	طرفية_2.Mاطبعxy(([]byte)("thread:"), 1, 14)
}
func (نفسه *Tخيطتنفيذhelper) Cإنشاءfromfunction(entrypoint_2 func(), Pصفحةدليلentry uint32, isنواة bool) Tخيطتنفيذ {
	result := Tخيطتنفيذ{}

	result.Stack = uint32(uintptr(نفسه.mem.Mتخصيص_الذاكرة(Tخيطتنفيذstackالحجم)))
	if result.Stack == 0 {
		return result
	}
	طرفية_2.Mاطبع(([]byte)("[mem:"))
	طرفية_2.MUnsignedinteger32اطبع(result.Stack)

	result.Cالمعالجالحالة = (*Tcpuالحالة)(Pointer(uintptr(result.Stack) + Tخيطتنفيذstackالحجم - Sizeof(Tcpuالحالة{})))
	result.Cالمعالجالحالة.Esp = result.Stack + Tخيطتنفيذstackالحجم
	result.Cالمعالجالحالة.Ebp = result.Cالمعالجالحالة.Esp
	result.Cالمعالجالحالة.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Uمستخدمstack_2 = Uمستخدمstack
	result.Uمستخدمstackالحجم_2 = Uمستخدمstackالحجم
	result.Pالهوية = 0
	result.Pأبالهوية = 0
	result.Pصفحةدليلentry = Pصفحةدليلentry
	طرفية_2.Mاطبع((([]byte)("cpu")))

	طرفية_2.MUnsignedinteger32اطبع(uint32(uintptr(Pointer(result.Cالمعالجالحالة))))

	طرفية_2.Mاطبع((([]byte)(":")))
	طرفية_2.MUnsignedinteger32اطبع(result.Cالمعالجالحالة.Eip)

	طرفية_2.Mاطبع("]")
	if isنواة == true {
		result.Cالمعالجالحالة.Cs = Segنواةcode
		result.Cالمعالجالحالة.Ds = Segنواةبيانات
		result.Cالمعالجالحالة.Es = Segنواةبيانات
		result.Cالمعالجالحالة.Fs = Segنواةبيانات
		result.Cالمعالجالحالة.Gs = Segنواةgs
		result.Cالمعالجالحالة.Ss = Segنواةبيانات
		result.Tخيطتنفيذالحالة = Rجاهز
		result.Cالمعالجالحالة.Eflags = 0x202
	} else {
		result.Cالمعالجالحالة.Cs = Segمستخدمcode
		result.Cالمعالجالحالة.Ds = Segمستخدمبيانات
		result.Cالمعالجالحالة.Es = Segمستخدمبيانات
		result.Cالمعالجالحالة.Fs = Segمستخدمبيانات
		result.Cالمعالجالحالة.Gs = Segمستخدمgs
		result.Cالمعالجالحالة.Ss = Segمستخدمبيانات
		result.Tخيطتنفيذالحالة = Sوقتالبداية
		result.Cالمعالجالحالة.Eflags = 0x222
	}
	result.Isنواة = isنواة
	result.Fpuoffset = 0xffffffff

	return result
}

func (نفسه *Tخيطتنفيذhelper) Cإنشاءالمؤشرfromfunction(entrypoint_2 func(), Pصفحةدليلentry uint32, isنواة bool) *Tخيطتنفيذ {
	result := (*Tخيطتنفيذ)(نفسه.mem.Mتخصيص_الذاكرة(uint32(Sizeof(Tخيطتنفيذ{}))))
	if result == nil {
		return nil
	}
	*result = نفسه.Cإنشاءfromfunction(entrypoint_2, Pصفحةدليلentry, isنواة)
	if result.Cالمعالجالحالة == nil {
		نفسه.mem.Fخالي(Pointer(result))
		return nil
	}
	return result
}
