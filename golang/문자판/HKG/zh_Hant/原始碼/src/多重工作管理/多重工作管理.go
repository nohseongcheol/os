/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 多重工作管理

import . "unsafe"
import . "控制台"
import . "reflect"
import mem "記憶體管理器"
import . "gdt"

var T測試 uint8

func halt()

type Tcpu狀態 struct {
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

type T工作 struct {
	堆疊記憶區	[4096]uint8
	cpu狀態	*Tcpu狀態
}

func (self *T工作) Init(gdt *TShareddescriptortable, mem *mem.T記憶體管理器, 項目point_2 func()) {

	self.cpu狀態 = (*Tcpu狀態)(Pointer(uintptr(mem.M配置記憶體(1024*1024)) + 1024*1024 - Sizeof(Tcpu狀態{})))

	self.cpu狀態.Eax = 0
	self.cpu狀態.Ebx = 0
	self.cpu狀態.Ecx = 0
	self.cpu狀態.Edx = 0

	self.cpu狀態.Esi = 0
	self.cpu狀態.Edi = 0

	self.cpu狀態.Gs = 0
	self.cpu狀態.Fs = 0
	self.cpu狀態.Es = 0
	self.cpu狀態.Ds = 0

	self.cpu狀態.Eip = uint32(ValueOf(項目point_2).Pointer())
	self.cpu狀態.Cs = Seg核心code
	self.cpu狀態.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpu狀態)))

	self.cpu狀態.Esp = stackaddress
	self.cpu狀態.Ebp = stackaddress
	self.cpu狀態.Ss = 0

}

type T工作管理器 struct {
}

var 工作_2 [256]T工作
var 數字工作 int
var 目前工作 int

func (self *T工作管理器) Init() {
	數字工作 = 0
	目前工作 = -1
}

func (self *T工作管理器) A加入工作(工作 T工作) bool {
	if 數字工作 >= 255 {
		return false
	}
	工作_2[數字工作] = 工作
	數字工作++
	return true
}

func (self *T工作管理器) Schedule(cpu狀態 *Tcpu狀態) *Tcpu狀態 {

	控制台_2 := T控制台{}
	for i := 0; i < 數字工作; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(工作_2[i].cpu狀態)))

		控制台_2.MUnsignedinteger32列印xy(x, 10, uint16(15+i))
	}
	if 數字工作 <= 0 {
		return cpu狀態
	}

	if 目前工作 >= 0 {
		工作_2[目前工作].cpu狀態 = cpu狀態
	}

	目前工作++
	if 目前工作 >= 數字工作 {
		目前工作 %= 數字工作

	}

	return 工作_2[目前工作].cpu狀態
}
