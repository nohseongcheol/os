package Tスレッド_2

import . "unsafe"
import . "reflect"
import . "gdt"
import . "コンソール"
import . "フクスウタスクカンリ"
import mem "メモリカンリシャ"
import . "カソウメモリ"

const (
	Blocked	= 1
	RジュンビOK	= 2
	Sテイシ	= 3
	Sキドウニチジ	= 4
)

const Tスレッドstackサイズ = 32 * 1024

type Tスレッド struct {
	Cpuジョウタイ		*Tcpuジョウタイ
	Stack		uint32
	Uリヨウシャstack_2	uint32
	Uリヨウシャstackサイズ_2	uint32
	Pid		uint32
	Parentpid	uint32

	Pページディレクトリentry	uint32

	Tスレッドジョウタイ		uint8
	Blockedジョウタイ	uint8

	ジカンデルタ	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Isチュウカク		bool
}

func (self *Tスレッド) Nシンキ() {
}

type Tスレッドhelper struct {
	mem *mem.Tメモリカンリシャ
}

var コンソール_2 = Tコンソール{}

func (self *Tスレッドhelper) Init(mem *mem.Tメモリカンリシャ) {
	self.mem = mem
	コンソール_2.Mインサツxy(([]byte)("thread:"), 1, 14)
}
func (self *Tスレッドhelper) Cサクセイカラカンスウ(entrypoint_2 func(), Pページディレクトリentry uint32, isチュウカク bool) Tスレッド {
	セイセイサキ := Tスレッド{}

	セイセイサキ.Stack = uint32(uintptr(self.mem.Mキオクリョウイキヲカクホ(Tスレッドstackサイズ)))
	if セイセイサキ.Stack == 0 {
		return セイセイサキ
	}
	コンソール_2.Mインサツ(([]byte)("[mem:"))
	コンソール_2.MUnsignedinteger32インサツ(セイセイサキ.Stack)

	セイセイサキ.Cpuジョウタイ = (*Tcpuジョウタイ)(Pointer(uintptr(セイセイサキ.Stack) + Tスレッドstackサイズ - Sizeof(Tcpuジョウタイ{})))
	セイセイサキ.Cpuジョウタイ.Esp = セイセイサキ.Stack + Tスレッドstackサイズ
	セイセイサキ.Cpuジョウタイ.Ebp = セイセイサキ.Cpuジョウタイ.Esp
	セイセイサキ.Cpuジョウタイ.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	セイセイサキ.Uリヨウシャstack_2 = Uリヨウシャstack
	セイセイサキ.Uリヨウシャstackサイズ_2 = Uリヨウシャstackサイズ
	セイセイサキ.Pid = 0
	セイセイサキ.Parentpid = 0
	セイセイサキ.Pページディレクトリentry = Pページディレクトリentry
	コンソール_2.Mインサツ((([]byte)("cpu")))

	コンソール_2.MUnsignedinteger32インサツ(uint32(uintptr(Pointer(セイセイサキ.Cpuジョウタイ))))

	コンソール_2.Mインサツ((([]byte)(":")))
	コンソール_2.MUnsignedinteger32インサツ(セイセイサキ.Cpuジョウタイ.Eip)

	コンソール_2.Mインサツ("]")
	if isチュウカク == true {
		セイセイサキ.Cpuジョウタイ.Cs = Segチュウカクcode
		セイセイサキ.Cpuジョウタイ.Ds = Segチュウカクデータ
		セイセイサキ.Cpuジョウタイ.Es = Segチュウカクデータ
		セイセイサキ.Cpuジョウタイ.Fs = Segチュウカクデータ
		セイセイサキ.Cpuジョウタイ.Gs = Segチュウカクgs
		セイセイサキ.Cpuジョウタイ.Ss = Segチュウカクデータ
		セイセイサキ.Tスレッドジョウタイ = RジュンビOK
		セイセイサキ.Cpuジョウタイ.Eflags = 0x202
	} else {
		セイセイサキ.Cpuジョウタイ.Cs = Segリヨウシャcode
		セイセイサキ.Cpuジョウタイ.Ds = Segリヨウシャデータ
		セイセイサキ.Cpuジョウタイ.Es = Segリヨウシャデータ
		セイセイサキ.Cpuジョウタイ.Fs = Segリヨウシャデータ
		セイセイサキ.Cpuジョウタイ.Gs = Segリヨウシャgs
		セイセイサキ.Cpuジョウタイ.Ss = Segリヨウシャデータ
		セイセイサキ.Tスレッドジョウタイ = Sキドウニチジ
		セイセイサキ.Cpuジョウタイ.Eflags = 0x222
	}
	セイセイサキ.Isチュウカク = isチュウカク
	セイセイサキ.Fpuoffset = 0xffffffff

	return セイセイサキ
}

func (self *Tスレッドhelper) Cサクセイポインタカラカンスウ(entrypoint_2 func(), Pページディレクトリentry uint32, isチュウカク bool) *Tスレッド {
	セイセイサキ := (*Tスレッド)(self.mem.Mキオクリョウイキヲカクホ(uint32(Sizeof(Tスレッド{}))))
	if セイセイサキ == nil {
		return nil
	}
	*セイセイサキ = self.Cサクセイカラカンスウ(entrypoint_2, Pページディレクトリentry, isチュウカク)
	if セイセイサキ.Cpuジョウタイ == nil {
		self.mem.Fアキ(Pointer(セイセイサキ))
		return nil
	}
	return セイセイサキ
}
