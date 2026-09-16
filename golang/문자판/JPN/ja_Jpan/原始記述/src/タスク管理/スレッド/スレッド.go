/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Tスレッド_2

import . "unsafe"
import . "reflect"
import . "gdt"
import . "コンソール"
import . "複数タスク管理"
import mem "メモリ管理者"
import . "仮想メモリ"

const (
	Blocked	= 1
	R準備OK	= 2
	S停止	= 3
	S起動日時	= 4
)

const Tスレッドstackサイズ = 32 * 1024

type Tスレッド struct {
	Cpu状態		*Tcpu状態
	Stack		uint32
	U利用者stack_2	uint32
	U利用者stackサイズ_2	uint32
	Pid		uint32
	Parentpid	uint32

	Pページディレクトリentry	uint32

	Tスレッド状態		uint8
	Blocked状態	uint8

	時間デルタ	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Is中核		bool
}

func (self *Tスレッド) N新規() {
}

type Tスレッドhelper struct {
	mem *mem.Tメモリ管理者
}

var コンソール_2 = Tコンソール{}

func (self *Tスレッドhelper) Init(mem *mem.Tメモリ管理者) {
	self.mem = mem
	コンソール_2.M印刷xy(([]byte)("thread:"), 1, 14)
}
func (self *Tスレッドhelper) C作成から関数(entrypoint_2 func(), Pページディレクトリentry uint32, is中核 bool) Tスレッド {
	生成先 := Tスレッド{}

	生成先.Stack = uint32(uintptr(self.mem.M記憶領域を確保(Tスレッドstackサイズ)))
	if 生成先.Stack == 0 {
		return 生成先
	}
	コンソール_2.M印刷(([]byte)("[mem:"))
	コンソール_2.MUnsignedinteger32印刷(生成先.Stack)

	生成先.Cpu状態 = (*Tcpu状態)(Pointer(uintptr(生成先.Stack) + Tスレッドstackサイズ - Sizeof(Tcpu状態{})))
	生成先.Cpu状態.Esp = 生成先.Stack + Tスレッドstackサイズ
	生成先.Cpu状態.Ebp = 生成先.Cpu状態.Esp
	生成先.Cpu状態.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	生成先.U利用者stack_2 = U利用者stack
	生成先.U利用者stackサイズ_2 = U利用者stackサイズ
	生成先.Pid = 0
	生成先.Parentpid = 0
	生成先.Pページディレクトリentry = Pページディレクトリentry
	コンソール_2.M印刷((([]byte)("cpu")))

	コンソール_2.MUnsignedinteger32印刷(uint32(uintptr(Pointer(生成先.Cpu状態))))

	コンソール_2.M印刷((([]byte)(":")))
	コンソール_2.MUnsignedinteger32印刷(生成先.Cpu状態.Eip)

	コンソール_2.M印刷("]")
	if is中核 == true {
		生成先.Cpu状態.Cs = Seg中核code
		生成先.Cpu状態.Ds = Seg中核データ
		生成先.Cpu状態.Es = Seg中核データ
		生成先.Cpu状態.Fs = Seg中核データ
		生成先.Cpu状態.Gs = Seg中核gs
		生成先.Cpu状態.Ss = Seg中核データ
		生成先.Tスレッド状態 = R準備OK
		生成先.Cpu状態.Eflags = 0x202
	} else {
		生成先.Cpu状態.Cs = Seg利用者code
		生成先.Cpu状態.Ds = Seg利用者データ
		生成先.Cpu状態.Es = Seg利用者データ
		生成先.Cpu状態.Fs = Seg利用者データ
		生成先.Cpu状態.Gs = Seg利用者gs
		生成先.Cpu状態.Ss = Seg利用者データ
		生成先.Tスレッド状態 = S起動日時
		生成先.Cpu状態.Eflags = 0x222
	}
	生成先.Is中核 = is中核
	生成先.Fpuoffset = 0xffffffff

	return 生成先
}

func (self *Tスレッドhelper) C作成ポインタから関数(entrypoint_2 func(), Pページディレクトリentry uint32, is中核 bool) *Tスレッド {
	生成先 := (*Tスレッド)(self.mem.M記憶領域を確保(uint32(Sizeof(Tスレッド{}))))
	if 生成先 == nil {
		return nil
	}
	*生成先 = self.C作成から関数(entrypoint_2, Pページディレクトリentry, is中核)
	if 生成先.Cpu状態 == nil {
		self.mem.F空き(Pointer(生成先))
		return nil
	}
	return 生成先
}
