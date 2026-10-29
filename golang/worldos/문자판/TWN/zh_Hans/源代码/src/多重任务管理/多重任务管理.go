/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 多重任务管理

import . "unsafe"
import . "控制台"
import . "reflect"
import mem "内存管理器"
import . "gdt"

var T测试 uint8

func halt()

type Tcpu状态 struct {
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

type T任务 struct {
	栈存储区	[4096]uint8
	cpu状态	*Tcpu状态
}

func (self *T任务) Init(gdt *TShareddescriptor表格, mem *mem.T内存管理器, 条目point_2 func()) {

	self.cpu状态 = (*Tcpu状态)(Pointer(uintptr(mem.M分配内存(1024*1024)) + 1024*1024 - Sizeof(Tcpu状态{})))

	self.cpu状态.Eax = 0
	self.cpu状态.Ebx = 0
	self.cpu状态.Ecx = 0
	self.cpu状态.Edx = 0

	self.cpu状态.Esi = 0
	self.cpu状态.Edi = 0

	self.cpu状态.Gs = 0
	self.cpu状态.Fs = 0
	self.cpu状态.Es = 0
	self.cpu状态.Ds = 0

	self.cpu状态.Eip = uint32(ValueOf(条目point_2).Pointer())
	self.cpu状态.Cs = Seg内核code
	self.cpu状态.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpu状态)))

	self.cpu状态.Esp = stackaddress
	self.cpu状态.Ebp = stackaddress
	self.cpu状态.Ss = 0

}

type T任务管理器 struct {
}

var 任务_2 [256]T任务
var 数字任务 int
var 当前任务 int

func (self *T任务管理器) Init() {
	数字任务 = 0
	当前任务 = -1
}

func (self *T任务管理器) A添加任务(任务 T任务) bool {
	if 数字任务 >= 255 {
		return false
	}
	任务_2[数字任务] = 任务
	数字任务++
	return true
}

func (self *T任务管理器) Schedule(cpu状态 *Tcpu状态) *Tcpu状态 {

	控制台_2 := T控制台{}
	for i := 0; i < 数字任务; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(任务_2[i].cpu状态)))

		控制台_2.MUnsignedinteger32打印xy(x, 10, uint16(15+i))
	}
	if 数字任务 <= 0 {
		return cpu状态
	}

	if 当前任务 >= 0 {
		任务_2[当前任务].cpu状态 = cpu状态
	}

	当前任务++
	if 当前任务 >= 数字任务 {
		当前任务 %= 数字任务

	}

	return 任务_2[当前任务].cpu状态
}
