/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "эсиmanager"
import . "gdt"

var Текшерүү uint8

func halt()

type TcpuАбал struct {
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

type TTask struct {
	stack	[4096]uint8
	бПАбал	*TcpuАбал
}

func (self *TTask) Init(gdt *TShareddescriptorЖадыбал, mem *mem.TЭсиmanager, entrypoint_2 func()) {

	self.бПАбал = (*TcpuАбал)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuАбал{})))

	self.бПАбал.Eax = 0
	self.бПАбал.Ebx = 0
	self.бПАбал.Ecx = 0
	self.бПАбал.Edx = 0

	self.бПАбал.Esi = 0
	self.бПАбал.Edi = 0

	self.бПАбал.Gs = 0
	self.бПАбал.Fs = 0
	self.бПАбал.Es = 0
	self.бПАбал.Ds = 0

	self.бПАбал.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.бПАбал.Cs = Segkernelcode
	self.бПАбал.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.бПАбал)))

	self.бПАбал.Esp = stackaddress
	self.бПАбал.Ebp = stackaddress
	self.бПАбал.Ss = 0

}

type TTaskmanager struct {
}

var маселелер [256]TTask
var нОМЕРМаселелер int
var currenttask int

func (self *TTaskmanager) Init() {
	нОМЕРМаселелер = 0
	currenttask = -1
}

func (self *TTaskmanager) Кошууtask(task TTask) bool {
	if нОМЕРМаселелер >= 255 {
		return false
	}
	маселелер[нОМЕРМаселелер] = task
	нОМЕРМаселелер++
	return true
}

func (self *TTaskmanager) Schedule(бПАбал *TcpuАбал) *TcpuАбал {

	console_2 := TConsole{}
	for i := 0; i < нОМЕРМаселелер; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(маселелер[i].бПАбал)))

		console_2.MUnsignedinteger32Басмаxy(x, 10, uint16(15+i))
	}
	if нОМЕРМаселелер <= 0 {
		return бПАбал
	}

	if currenttask >= 0 {
		маселелер[currenttask].бПАбал = бПАбал
	}

	currenttask++
	if currenttask >= нОМЕРМаселелер {
		currenttask %= нОМЕРМаселелер

	}

	return маселелер[currenttask].бПАбал
}
