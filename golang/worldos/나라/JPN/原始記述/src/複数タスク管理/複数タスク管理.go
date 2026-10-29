/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 複数タスク管理

import . "unsafe"
import . "コンソール"
import . "reflect"
import mem "メモリ管理者"
import . "gdt"

var Tテスト uint8

func halt()

type Tcpu状態 struct {
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

type Tタスク struct {
	積重ね記憶領域	[4096]uint8
	cpu状態	*Tcpu状態
}

func (self *Tタスク) Init(gdt *TShareddescriptortable, mem *mem.Tメモリ管理者, entrypoint_2 func()) {

	self.cpu状態 = (*Tcpu状態)(Pointer(uintptr(mem.M記憶領域を確保(1024*1024)) + 1024*1024 - Sizeof(Tcpu状態{})))

	self.cpu状態.Eax = 0
	self.cpu状態.Ebx = 0
	self.cpu状態.Ecx = 0
	self.cpu状態.Edx = 0

	self.cpu状態.Esi = 0
	self.cpu状態.Edi = 0

	self.cpu状態.Gs = 0
	self.cpu状態.Fs = 0
	self.cpu状態.Es = 0
	self.cpu状態.Ds = 0

	self.cpu状態.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.cpu状態.Cs = Seg中核code
	self.cpu状態.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpu状態)))

	self.cpu状態.Esp = stackaddress
	self.cpu状態.Ebp = stackaddress
	self.cpu状態.Ss = 0

}

type Tタスク管理者 struct {
}

var タスク_2 [256]Tタスク
var numberタスク int
var 現在の日時タスク int

func (self *Tタスク管理者) Init() {
	numberタスク = 0
	現在の日時タスク = -1
}

func (self *Tタスク管理者) A追加タスク(タスク Tタスク) bool {
	if numberタスク >= 255 {
		return false
	}
	タスク_2[numberタスク] = タスク
	numberタスク++
	return true
}

func (self *Tタスク管理者) Schedule(cpu状態 *Tcpu状態) *Tcpu状態 {

	コンソール_2 := Tコンソール{}
	for i := 0; i < numberタスク; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(タスク_2[i].cpu状態)))

		コンソール_2.MUnsignedinteger32印刷xy(x, 10, uint16(15+i))
	}
	if numberタスク <= 0 {
		return cpu状態
	}

	if 現在の日時タスク >= 0 {
		タスク_2[現在の日時タスク].cpu状態 = cpu状態
	}

	現在の日時タスク++
	if 現在の日時タスク >= numberタスク {
		現在の日時タスク %= numberタスク

	}

	return タスク_2[現在の日時タスク].cpu状態
}
