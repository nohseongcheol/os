/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "հիշողությունmanager"
import . "gdt"

var Թեստ uint8

func halt()

type TcpuՎիճակ struct {
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
	stack		[4096]uint8
	կՄՀՎիճակ	*TcpuՎիճակ
}

func (ինքնուրույն *TTask) Init(gdt *TShareddescriptorԱղյուսակ, mem *mem.TՀիշողությունmanager, entrypoint_2 func()) {

	ինքնուրույն.կՄՀՎիճակ = (*TcpuՎիճակ)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuՎիճակ{})))

	ինքնուրույն.կՄՀՎիճակ.Eax = 0
	ինքնուրույն.կՄՀՎիճակ.Ebx = 0
	ինքնուրույն.կՄՀՎիճակ.Ecx = 0
	ինքնուրույն.կՄՀՎիճակ.Edx = 0

	ինքնուրույն.կՄՀՎիճակ.Esi = 0
	ինքնուրույն.կՄՀՎիճակ.Edi = 0

	ինքնուրույն.կՄՀՎիճակ.Gs = 0
	ինքնուրույն.կՄՀՎիճակ.Fs = 0
	ինքնուրույն.կՄՀՎիճակ.Es = 0
	ինքնուրույն.կՄՀՎիճակ.Ds = 0

	ինքնուրույն.կՄՀՎիճակ.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	ինքնուրույն.կՄՀՎիճակ.Cs = Segkernelcode
	ինքնուրույն.կՄՀՎիճակ.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(ինքնուրույն.կՄՀՎիճակ)))

	ինքնուրույն.կՄՀՎիճակ.Esp = stackaddress
	ինքնուրույն.կՄՀՎիճակ.Ebp = stackaddress
	ինքնուրույն.կՄՀՎիճակ.Ss = 0

}

type TTaskmanager struct {
}

var առաջադրանքներ [256]TTask
var հԱՄԱՐԱռաջադրանքներ int
var currenttask int

func (ինքնուրույն *TTaskmanager) Init() {
	հԱՄԱՐԱռաջադրանքներ = 0
	currenttask = -1
}

func (ինքնուրույն *TTaskmanager) Ավելացնելtask(task TTask) bool {
	if հԱՄԱՐԱռաջադրանքներ >= 255 {
		return false
	}
	առաջադրանքներ[հԱՄԱՐԱռաջադրանքներ] = task
	հԱՄԱՐԱռաջադրանքներ++
	return true
}

func (ինքնուրույն *TTaskmanager) Schedule(կՄՀՎիճակ *TcpuՎիճակ) *TcpuՎիճակ {

	console_2 := TConsole{}
	for i := 0; i < հԱՄԱՐԱռաջադրանքներ; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(առաջադրանքներ[i].կՄՀՎիճակ)))

		console_2.MUnsignedinteger32Տպելxy(x, 10, uint16(15+i))
	}
	if հԱՄԱՐԱռաջադրանքներ <= 0 {
		return կՄՀՎիճակ
	}

	if currenttask >= 0 {
		առաջադրանքներ[currenttask].կՄՀՎիճակ = կՄՀՎիճակ
	}

	currenttask++
	if currenttask >= հԱՄԱՐԱռաջադրանքներ {
		currenttask %= հԱՄԱՐԱռաջադրանքներ

	}

	return առաջադրանքներ[currenttask].կՄՀՎիճակ
}
