package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "ማስታወሻmanager"
import . "virtualማስታወሻ"

const (
	Blocked	= 1
	Rዝግጁ	= 2
	Sቆሟል	= 3
	Sጀምሯል	= 4
)

const Threadstackመጠን = 32 * 1024

type TThread struct {
	Cpuሁኔታ		*Tcpuሁኔታ
	Stack		uint32
	Uተጠቃሚstack_2	uint32
	Uተጠቃሚstackመጠን_2	uint32
	Pid		uint32
	Pወላጅpid		uint32

	Pገጽዳይሬክቶሪentry	uint32

	Threadሁኔታ	uint8
	Blockedሁኔታ	uint8

	ሰዓትdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Nአዲስ() {
}

type TThreadhelper struct {
	mem *mem.Tማስታወሻmanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.Tማስታወሻmanager) {
	self.mem = mem
	console_2.Mማተሚያxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromfunction(entrypoint_2 func(), Pገጽዳይሬክቶሪentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(Threadstackመጠን)))
	if result.Stack == 0 {
		return result
	}
	console_2.Mማተሚያ(([]byte)("[mem:"))
	console_2.MUnsignedinteger32ማተሚያ(result.Stack)

	result.Cpuሁኔታ = (*Tcpuሁኔታ)(Pointer(uintptr(result.Stack) + Threadstackመጠን - Sizeof(Tcpuሁኔታ{})))
	result.Cpuሁኔታ.Esp = result.Stack + Threadstackመጠን
	result.Cpuሁኔታ.Ebp = result.Cpuሁኔታ.Esp
	result.Cpuሁኔታ.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Uተጠቃሚstack_2 = Uተጠቃሚstack
	result.Uተጠቃሚstackመጠን_2 = Uተጠቃሚstackመጠን
	result.Pid = 0
	result.Pወላጅpid = 0
	result.Pገጽዳይሬክቶሪentry = Pገጽዳይሬክቶሪentry
	console_2.Mማተሚያ((([]byte)("cpu")))

	console_2.MUnsignedinteger32ማተሚያ(uint32(uintptr(Pointer(result.Cpuሁኔታ))))

	console_2.Mማተሚያ((([]byte)(":")))
	console_2.MUnsignedinteger32ማተሚያ(result.Cpuሁኔታ.Eip)

	console_2.Mማተሚያ("]")
	if iskernel == true {
		result.Cpuሁኔታ.Cs = Segkernelcode
		result.Cpuሁኔታ.Ds = Segkerneldata
		result.Cpuሁኔታ.Es = Segkerneldata
		result.Cpuሁኔታ.Fs = Segkerneldata
		result.Cpuሁኔታ.Gs = Segkernelgs
		result.Cpuሁኔታ.Ss = Segkerneldata
		result.Threadሁኔታ = Rዝግጁ
		result.Cpuሁኔታ.Eflags = 0x202
	} else {
		result.Cpuሁኔታ.Cs = Segተጠቃሚcode
		result.Cpuሁኔታ.Ds = Segተጠቃሚdata
		result.Cpuሁኔታ.Es = Segተጠቃሚdata
		result.Cpuሁኔታ.Fs = Segተጠቃሚdata
		result.Cpuሁኔታ.Gs = Segተጠቃሚgs
		result.Cpuሁኔታ.Ss = Segተጠቃሚdata
		result.Threadሁኔታ = Sጀምሯል
		result.Cpuሁኔታ.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createጠቋሚfromfunction(entrypoint_2 func(), Pገጽዳይሬክቶሪentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromfunction(entrypoint_2, Pገጽዳይሬክቶሪentry, iskernel)
	if result.Cpuሁኔታ == nil {
		self.mem.Fነፃ(Pointer(result))
		return nil
	}
	return result
}
