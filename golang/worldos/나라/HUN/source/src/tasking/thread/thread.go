/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konzol"
import . "multitasking"
import mem "memóriamanager"
import . "virtualMemória"

const (
	Blocked		= 1
	Kész		= 2
	Leállítva	= 3
	Indítva		= 4
)

const ThreadstackMéret = 32 * 1024

type TThread struct {
	CpuÁllapot		*TcpuÁllapot
	Stack			uint32
	Felhasználóstack_2	uint32
	FelhasználóstackMéret_2	uint32
	Pid			uint32
	Parentpid		uint32

	OldalKönyvtárbejegyzés	uint32

	ThreadÁllapot	uint8
	BlockedÁllapot	uint8

	idődelta	uint32

	TlsDarabkák	[Gdtbejegyzés]TSegmentdescriptor
	FpuEltolás	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Új() {
}

type TThreadhelper struct {
	mem *mem.TMemóriamanager
}

var konzol_2 = TKonzol{}

func (self *TThreadhelper) Init(mem *mem.TMemóriamanager) {
	self.mem = mem
	konzol_2.MNyomtatásxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) CreatefromFüggvény(bejegyzéspoint_2 func(), OldalKönyvtárbejegyzés uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackMéret)))
	if result.Stack == 0 {
		return result
	}
	konzol_2.MNyomtatás(([]byte)("[mem:"))
	konzol_2.MUnsignedinteger32Nyomtatás(result.Stack)

	result.CpuÁllapot = (*TcpuÁllapot)(Pointer(uintptr(result.Stack) + ThreadstackMéret - Sizeof(TcpuÁllapot{})))
	result.CpuÁllapot.Esp = result.Stack + ThreadstackMéret
	result.CpuÁllapot.Ebp = result.CpuÁllapot.Esp
	result.CpuÁllapot.Eip = uint32(ValueOf(bejegyzéspoint_2).Pointer())
	result.Felhasználóstack_2 = Felhasználóstack
	result.FelhasználóstackMéret_2 = FelhasználóstackMéret
	result.Pid = 0
	result.Parentpid = 0
	result.OldalKönyvtárbejegyzés = OldalKönyvtárbejegyzés
	konzol_2.MNyomtatás((([]byte)("cpu")))

	konzol_2.MUnsignedinteger32Nyomtatás(uint32(uintptr(Pointer(result.CpuÁllapot))))

	konzol_2.MNyomtatás((([]byte)(":")))
	konzol_2.MUnsignedinteger32Nyomtatás(result.CpuÁllapot.Eip)

	konzol_2.MNyomtatás("]")
	if iskernel == true {
		result.CpuÁllapot.Cs = Segkernelcode
		result.CpuÁllapot.Ds = Segkerneldata
		result.CpuÁllapot.Es = Segkerneldata
		result.CpuÁllapot.Fs = Segkerneldata
		result.CpuÁllapot.Gs = Segkernelgs
		result.CpuÁllapot.Ss = Segkerneldata
		result.ThreadÁllapot = Kész
		result.CpuÁllapot.Eflags = 0x202
	} else {
		result.CpuÁllapot.Cs = SegFelhasználócode
		result.CpuÁllapot.Ds = SegFelhasználódata
		result.CpuÁllapot.Es = SegFelhasználódata
		result.CpuÁllapot.Fs = SegFelhasználódata
		result.CpuÁllapot.Gs = SegFelhasználógs
		result.CpuÁllapot.Ss = SegFelhasználódata
		result.ThreadÁllapot = Indítva
		result.CpuÁllapot.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.FpuEltolás = 0xffffffff

	return result
}

func (self *TThreadhelper) CreateMutatófromFüggvény(bejegyzéspoint_2 func(), OldalKönyvtárbejegyzés uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.CreatefromFüggvény(bejegyzéspoint_2, OldalKönyvtárbejegyzés, iskernel)
	if result.CpuÁllapot == nil {
		self.mem.Szabad(Pointer(result))
		return nil
	}
	return result
}
