/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "konzol"
import . "reflect"
import mem "memóriamanager"
import . "gdt"

var Teszt uint8

func halt()

type TcpuÁllapot struct {
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

type TFeladat struct {
	stack		[4096]uint8
	cpuÁllapot	*TcpuÁllapot
}

func (self *TFeladat) Init(gdt *TShareddescriptorTáblázat, mem *mem.TMemóriamanager, bejegyzéspoint_2 func()) {

	self.cpuÁllapot = (*TcpuÁllapot)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuÁllapot{})))

	self.cpuÁllapot.Eax = 0
	self.cpuÁllapot.Ebx = 0
	self.cpuÁllapot.Ecx = 0
	self.cpuÁllapot.Edx = 0

	self.cpuÁllapot.Esi = 0
	self.cpuÁllapot.Edi = 0

	self.cpuÁllapot.Gs = 0
	self.cpuÁllapot.Fs = 0
	self.cpuÁllapot.Es = 0
	self.cpuÁllapot.Ds = 0

	self.cpuÁllapot.Eip = uint32(ValueOf(bejegyzéspoint_2).Pointer())
	self.cpuÁllapot.Cs = Segkernelcode
	self.cpuÁllapot.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpuÁllapot)))

	self.cpuÁllapot.Esp = stackaddress
	self.cpuÁllapot.Ebp = stackaddress
	self.cpuÁllapot.Ss = 0

}

type TFeladatmanager struct {
}

var feladatok [256]TFeladat
var számFeladatok int
var jelenlegiFeladat int

func (self *TFeladatmanager) Init() {
	számFeladatok = 0
	jelenlegiFeladat = -1
}

func (self *TFeladatmanager) HozzáadásFeladat(feladat TFeladat) bool {
	if számFeladatok >= 255 {
		return false
	}
	feladatok[számFeladatok] = feladat
	számFeladatok++
	return true
}

func (self *TFeladatmanager) Schedule(cpuÁllapot *TcpuÁllapot) *TcpuÁllapot {

	konzol_2 := TKonzol{}
	for i := 0; i < számFeladatok; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(feladatok[i].cpuÁllapot)))

		konzol_2.MUnsignedinteger32Nyomtatásxy(x, 10, uint16(15+i))
	}
	if számFeladatok <= 0 {
		return cpuÁllapot
	}

	if jelenlegiFeladat >= 0 {
		feladatok[jelenlegiFeladat].cpuÁllapot = cpuÁllapot
	}

	jelenlegiFeladat++
	if jelenlegiFeladat >= számFeladatok {
		jelenlegiFeladat %= számFeladatok

	}

	return feladatok[jelenlegiFeladat].cpuÁllapot
}
