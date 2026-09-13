package متعددإدارةمهام

import . "unsafe"
import . "طرفية"
import . "reflect"
import mem "ذاكرةمدير"
import . "gdt"

var Tتجريب uint8

func halt()

type Tcpuالحالة struct {
	p1	uint32
	p2	uint32

	Eax	uint32
	Ebx	uint32
	Ecx	uint32
	Edx	uint32

	Esi	uint32
	Edi	uint32
	Ebp	uint32

	Gs	uint32
	Fs	uint32
	Es	uint32
	Ds	uint32

	Eip	uint32

	Cs	uint32
	Eflags	uint32

	Esp	uint32
	Ss	uint32
}

type Tمهمة struct {
	ذاكرة_مكدس		[4096]uint8
	المعالجالحالة	*Tcpuالحالة
}

func (نفسه *Tمهمة) Init(gdt *TShareddescriptorجدول, mem *mem.Tذاكرةمدير, entrypoint_2 func()) {

	نفسه.المعالجالحالة = (*Tcpuالحالة)(Pointer(uintptr(mem.Mتخصيص_الذاكرة(1024*1024)) + 1024*1024 - Sizeof(Tcpuالحالة{})))

	نفسه.المعالجالحالة.Eax = 0
	نفسه.المعالجالحالة.Ebx = 0
	نفسه.المعالجالحالة.Ecx = 0
	نفسه.المعالجالحالة.Edx = 0

	نفسه.المعالجالحالة.Esi = 0
	نفسه.المعالجالحالة.Edi = 0

	نفسه.المعالجالحالة.Gs = 0
	نفسه.المعالجالحالة.Fs = 0
	نفسه.المعالجالحالة.Es = 0
	نفسه.المعالجالحالة.Ds = 0

	نفسه.المعالجالحالة.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	نفسه.المعالجالحالة.Cs = Segنواةcode
	نفسه.المعالجالحالة.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(نفسه.المعالجالحالة)))

	نفسه.المعالجالحالة.Esp = stackaddress
	نفسه.المعالجالحالة.Ebp = stackaddress
	نفسه.المعالجالحالة.Ss = 0

}

type Tمهمةمدير struct {
}

var المهمات [256]Tمهمة
var الأرقامالمهمات int
var الحاليمهمة int

func (نفسه *Tمهمةمدير) Init() {
	الأرقامالمهمات = 0
	الحاليمهمة = -1
}

func (نفسه *Tمهمةمدير) Aأضفمهمة(مهمة Tمهمة) bool {
	if الأرقامالمهمات >= 255 {
		return false
	}
	المهمات[الأرقامالمهمات] = مهمة
	الأرقامالمهمات++
	return true
}

func (نفسه *Tمهمةمدير) Schedule(المعالجالحالة *Tcpuالحالة) *Tcpuالحالة {

	طرفية_2 := Tطرفية{}
	for i := 0; i < الأرقامالمهمات; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(المهمات[i].المعالجالحالة)))

		طرفية_2.MUnsignedinteger32اطبعxy(x, 10, uint16(15+i))
	}
	if الأرقامالمهمات <= 0 {
		return المعالجالحالة
	}

	if الحاليمهمة >= 0 {
		المهمات[الحاليمهمة].المعالجالحالة = المعالجالحالة
	}

	الحاليمهمة++
	if الحاليمهمة >= الأرقامالمهمات {
		الحاليمهمة %= الأرقامالمهمات

	}

	return المهمات[الحاليمهمة].المعالجالحالة
}
