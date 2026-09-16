/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "זיכרוןmanager"
import . "gdt"

var Tבדיקה uint8

func halt()

type Tcpuמצב struct {
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

type Tמשימה struct {
	stack	[4096]uint8
	מעבדמצב	*Tcpuמצב
}

func (self *Tמשימה) Init(gdt *TShareddescriptortable, mem *mem.Tזיכרוןmanager, entrypoint_2 func()) {

	self.מעבדמצב = (*Tcpuמצב)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(Tcpuמצב{})))

	self.מעבדמצב.Eax = 0
	self.מעבדמצב.Ebx = 0
	self.מעבדמצב.Ecx = 0
	self.מעבדמצב.Edx = 0

	self.מעבדמצב.Esi = 0
	self.מעבדמצב.Edi = 0

	self.מעבדמצב.Gs = 0
	self.מעבדמצב.Fs = 0
	self.מעבדמצב.Es = 0
	self.מעבדמצב.Ds = 0

	self.מעבדמצב.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.מעבדמצב.Cs = Segkernelcode
	self.מעבדמצב.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.מעבדמצב)))

	self.מעבדמצב.Esp = stackaddress
	self.מעבדמצב.Ebp = stackaddress
	self.מעבדמצב.Ss = 0

}

type Tמשימהmanager struct {
}

var משימות [256]Tמשימה
var מספרמשימות int
var נוכחימשימה int

func (self *Tמשימהmanager) Init() {
	מספרמשימות = 0
	נוכחימשימה = -1
}

func (self *Tמשימהmanager) Aהוספהמשימה(משימה Tמשימה) bool {
	if מספרמשימות >= 255 {
		return false
	}
	משימות[מספרמשימות] = משימה
	מספרמשימות++
	return true
}

func (self *Tמשימהmanager) Schedule(מעבדמצב *Tcpuמצב) *Tcpuמצב {

	console_2 := TConsole{}
	for i := 0; i < מספרמשימות; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(משימות[i].מעבדמצב)))

		console_2.MUnsignedinteger32הדפסהxy(x, 10, uint16(15+i))
	}
	if מספרמשימות <= 0 {
		return מעבדמצב
	}

	if נוכחימשימה >= 0 {
		משימות[נוכחימשימה].מעבדמצב = מעבדמצב
	}

	נוכחימשימה++
	if נוכחימשימה >= מספרמשימות {
		נוכחימשימה %= מספרמשימות

	}

	return משימות[נוכחימשימה].מעבדמצב
}
