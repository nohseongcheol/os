/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "μνήμηmanager"
import . "εικονικήΜνήμη"

const (
	Blocked		= 1
	Έτοιμο		= 2
	Τερματισμός	= 3
	Ξεκίνησε	= 4
)

const ThreadstackΜέγεθος = 32 * 1024

type TThread struct {
	ΕπεξεργαστήςΚατάσταση	*TcpuΚατάσταση
	Stack			uint32
	Χρήστηςstack_2		uint32
	ΧρήστηςstackΜέγεθος_2	uint32
	Pid			uint32
	Γονικόpid		uint32

	ΣελίδαΚατάλογοςκαταχώρηση	uint32

	ThreadΚατάσταση		uint8
	BlockedΚατάσταση	uint8

	ώραdelta	uint32

	Tlssegments	[Gdtκαταχώρηση]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Νέο() {
}

type TThreadhelper struct {
	mem *mem.TΜνήμηmanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.TΜνήμηmanager) {
	self.mem = mem
	console_2.MΕκτύπωσηxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) CreatefromΣυνάρτηση(καταχώρησηpoint_2 func(), ΣελίδαΚατάλογοςκαταχώρηση uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(ThreadstackΜέγεθος)))
	if result.Stack == 0 {
		return result
	}
	console_2.MΕκτύπωση(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Εκτύπωση(result.Stack)

	result.ΕπεξεργαστήςΚατάσταση = (*TcpuΚατάσταση)(Pointer(uintptr(result.Stack) + ThreadstackΜέγεθος - Sizeof(TcpuΚατάσταση{})))
	result.ΕπεξεργαστήςΚατάσταση.Esp = result.Stack + ThreadstackΜέγεθος
	result.ΕπεξεργαστήςΚατάσταση.Ebp = result.ΕπεξεργαστήςΚατάσταση.Esp
	result.ΕπεξεργαστήςΚατάσταση.Eip = uint32(ValueOf(καταχώρησηpoint_2).Pointer())
	result.Χρήστηςstack_2 = Χρήστηςstack
	result.ΧρήστηςstackΜέγεθος_2 = ΧρήστηςstackΜέγεθος
	result.Pid = 0
	result.Γονικόpid = 0
	result.ΣελίδαΚατάλογοςκαταχώρηση = ΣελίδαΚατάλογοςκαταχώρηση
	console_2.MΕκτύπωση((([]byte)("cpu")))

	console_2.MUnsignedinteger32Εκτύπωση(uint32(uintptr(Pointer(result.ΕπεξεργαστήςΚατάσταση))))

	console_2.MΕκτύπωση((([]byte)(":")))
	console_2.MUnsignedinteger32Εκτύπωση(result.ΕπεξεργαστήςΚατάσταση.Eip)

	console_2.MΕκτύπωση("]")
	if iskernel == true {
		result.ΕπεξεργαστήςΚατάσταση.Cs = Segkernelcode
		result.ΕπεξεργαστήςΚατάσταση.Ds = Segkerneldata
		result.ΕπεξεργαστήςΚατάσταση.Es = Segkerneldata
		result.ΕπεξεργαστήςΚατάσταση.Fs = Segkerneldata
		result.ΕπεξεργαστήςΚατάσταση.Gs = Segkernelgs
		result.ΕπεξεργαστήςΚατάσταση.Ss = Segkerneldata
		result.ThreadΚατάσταση = Έτοιμο
		result.ΕπεξεργαστήςΚατάσταση.Eflags = 0x202
	} else {
		result.ΕπεξεργαστήςΚατάσταση.Cs = SegΧρήστηςcode
		result.ΕπεξεργαστήςΚατάσταση.Ds = SegΧρήστηςdata
		result.ΕπεξεργαστήςΚατάσταση.Es = SegΧρήστηςdata
		result.ΕπεξεργαστήςΚατάσταση.Fs = SegΧρήστηςdata
		result.ΕπεξεργαστήςΚατάσταση.Gs = SegΧρήστηςgs
		result.ΕπεξεργαστήςΚατάσταση.Ss = SegΧρήστηςdata
		result.ThreadΚατάσταση = Ξεκίνησε
		result.ΕπεξεργαστήςΚατάσταση.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) CreateΔείκτηςfromΣυνάρτηση(καταχώρησηpoint_2 func(), ΣελίδαΚατάλογοςκαταχώρηση uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.CreatefromΣυνάρτηση(καταχώρησηpoint_2, ΣελίδαΚατάλογοςκαταχώρηση, iskernel)
	if result.ΕπεξεργαστήςΚατάσταση == nil {
		self.mem.Ελεύθερα(Pointer(result))
		return nil
	}
	return result
}
