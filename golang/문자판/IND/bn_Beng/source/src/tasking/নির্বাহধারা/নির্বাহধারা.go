package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "স্মৃতি"
import . "virtmem"

const (
	Blocked	= 1
	Ready	= 2
	Stopped	= 3
	Started	= 4
)

const THREAD_STACK_SIZE = 32 * 1024

type Tনির্বাহধারা struct {
	CpuState	*TCPUState
	Stack		uint32
	UserStack	uint32
	UserStackSize	uint32
	Pid		uint32
	ParentPid		uint32

	PageDirEntry	uint32

	ThreadState	uint8
	BlockedState	uint8

	timeDelta	uint32

	TlsSegments	[GDT_ENTRIES]T조각설명자
	FPUOffset	uintptr
	FPUBuffer	[512 + 16]byte
	IsKernel	bool
}

func (self *Tনির্বাহধারা) New() {
}

type TThreadHelper struct {
	mem *mem.TMemoryManager
}

var 콘솔 = T콘솔{}

func (self *TThreadHelper) Vআরম্ভ_করা(mem *mem.TMemoryManager) {
	self.mem = mem
	콘솔.M출력XY(([]byte)("thread:"), 1, 14)
}
func (self *TThreadHelper) CreateFromFunction(entrypoint func(), PageDirEntry uint32, isKernel bool) Tনির্বাহধারা {
	result := Tনির্বাহধারা{}

	result.Stack = uint32(uintptr(self.mem.Vস্মৃতি_বরাদ্দ_করা(THREAD_STACK_SIZE)))
	if result.Stack == 0 {
		return result
	}
	콘솔.M출력(([]byte)("[mem:"))
	콘솔.MUint32출력(result.Stack)

	result.CpuState = (*TCPUState)(Pointer(uintptr(result.Stack) + THREAD_STACK_SIZE - Sizeof(TCPUState{})))
	result.CpuState.Esp = result.Stack + THREAD_STACK_SIZE
	result.CpuState.Ebp = result.CpuState.Esp
	result.CpuState.Eip = uint32(ValueOf(entrypoint).Pointer())
	result.UserStack = USER_STACK
	result.UserStackSize = USER_STACK_SIZE
	result.Pid = 0
	result.ParentPid = 0
	result.PageDirEntry = PageDirEntry
	콘솔.M출력((([]byte)("cpu")))

	콘솔.MUint32출력(uint32(uintptr(Pointer(result.CpuState))))

	콘솔.M출력((([]byte)(":")))
	콘솔.MUint32출력(result.CpuState.Eip)

	콘솔.M출력("]")
	if isKernel == true {
		result.CpuState.Cs = SEG_KERNEL_CODE
		result.CpuState.Ds = SEG_KERNEL_DATA
		result.CpuState.Es = SEG_KERNEL_DATA
		result.CpuState.Fs = SEG_KERNEL_DATA
		result.CpuState.Gs = SEG_KERNEL_GS
		result.CpuState.Ss = SEG_KERNEL_DATA
		result.ThreadState = Ready
		result.CpuState.Eflags = 0x202
	} else {
		result.CpuState.Cs = SEG_USER_CODE
		result.CpuState.Ds = SEG_USER_DATA
		result.CpuState.Es = SEG_USER_DATA
		result.CpuState.Fs = SEG_USER_DATA
		result.CpuState.Gs = SEG_USER_GS
		result.CpuState.Ss = SEG_USER_DATA
		result.ThreadState = Started
		result.CpuState.Eflags = 0x222
	}
	result.IsKernel = isKernel
	result.FPUOffset = 0xffffffff

	return result
}

func (self *TThreadHelper) CreatePtrFromFunction(entrypoint func(), PageDirEntry uint32, isKernel bool) *Tনির্বাহধারা {
	result := (*Tনির্বাহধারা)(self.mem.Vস্মৃতি_বরাদ্দ_করা(uint32(Sizeof(Tনির্বাহধারা{}))))
	if result == nil {
		return nil
	}
	*result = self.CreateFromFunction(entrypoint, PageDirEntry, isKernel)
	if result.CpuState == nil {
		self.mem.Vস্মৃতি_মুক্ত_করা(Pointer(result))
		return nil
	}
	return result
}
