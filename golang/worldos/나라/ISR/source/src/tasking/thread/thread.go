/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "multitasking"
import mem "זיכרוןmanager"
import . "וירטואליזיכרון"

const (
	Blocked	= 1
	Rמוכן	= 2
	Sמופסק	= 3
	Sהתחיל	= 4
)

const Threadstackגודל = 32 * 1024

type TThread struct {
	Cמעבדמצב		*Tcpuמצב
	Stack			uint32
	Uמשתמשstack_2		uint32
	Uמשתמשstackגודל_2	uint32
	Pמזההתהליך		uint32
	Parentמזההתהליך		uint32

	Pעמודספרייהentry	uint32

	Threadמצב	uint8
	Blockedמצב	uint8

	זמןdelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (self *TThread) Nחדש() {
}

type TThreadhelper struct {
	mem *mem.Tזיכרוןmanager
}

var console_2 = TConsole{}

func (self *TThreadhelper) Init(mem *mem.Tזיכרוןmanager) {
	self.mem = mem
	console_2.Mהדפסהxy(([]byte)("thread:"), 1, 14)
}
func (self *TThreadhelper) Createfromפונקציה(entrypoint_2 func(), Pעמודספרייהentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(self.mem.Malloc(Threadstackגודל)))
	if result.Stack == 0 {
		return result
	}
	console_2.Mהדפסה(([]byte)("[mem:"))
	console_2.MUnsignedinteger32הדפסה(result.Stack)

	result.Cמעבדמצב = (*Tcpuמצב)(Pointer(uintptr(result.Stack) + Threadstackגודל - Sizeof(Tcpuמצב{})))
	result.Cמעבדמצב.Esp = result.Stack + Threadstackגודל
	result.Cמעבדמצב.Ebp = result.Cמעבדמצב.Esp
	result.Cמעבדמצב.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Uמשתמשstack_2 = Uמשתמשstack
	result.Uמשתמשstackגודל_2 = Uמשתמשstackגודל
	result.Pמזההתהליך = 0
	result.Parentמזההתהליך = 0
	result.Pעמודספרייהentry = Pעמודספרייהentry
	console_2.Mהדפסה((([]byte)("cpu")))

	console_2.MUnsignedinteger32הדפסה(uint32(uintptr(Pointer(result.Cמעבדמצב))))

	console_2.Mהדפסה((([]byte)(":")))
	console_2.MUnsignedinteger32הדפסה(result.Cמעבדמצב.Eip)

	console_2.Mהדפסה("]")
	if iskernel == true {
		result.Cמעבדמצב.Cs = Segkernelcode
		result.Cמעבדמצב.Ds = Segkerneldata
		result.Cמעבדמצב.Es = Segkerneldata
		result.Cמעבדמצב.Fs = Segkerneldata
		result.Cמעבדמצב.Gs = Segkernelgs
		result.Cמעבדמצב.Ss = Segkerneldata
		result.Threadמצב = Rמוכן
		result.Cמעבדמצב.Eflags = 0x202
	} else {
		result.Cמעבדמצב.Cs = Segמשתמשcode
		result.Cמעבדמצב.Ds = Segמשתמשdata
		result.Cמעבדמצב.Es = Segמשתמשdata
		result.Cמעבדמצב.Fs = Segמשתמשdata
		result.Cמעבדמצב.Gs = Segמשתמשgs
		result.Cמעבדמצב.Ss = Segמשתמשdata
		result.Threadמצב = Sהתחיל
		result.Cמעבדמצב.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (self *TThreadhelper) Createסמןfromפונקציה(entrypoint_2 func(), Pעמודספרייהentry uint32, iskernel bool) *TThread {
	result := (*TThread)(self.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = self.Createfromפונקציה(entrypoint_2, Pעמודספרייהentry, iskernel)
	if result.Cמעבדמצב == nil {
		self.mem.Fפנוי(Pointer(result))
		return nil
	}
	return result
}
