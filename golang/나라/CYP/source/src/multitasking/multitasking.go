/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "μνήμηmanager"
import . "gdt"

var Δοκιμή uint8

func halt()

type TcpuΚατάσταση struct {
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

type TΔιεργασία struct {
	stack			[4096]uint8
	επεξεργαστήςΚατάσταση	*TcpuΚατάσταση
}

func (self *TΔιεργασία) Init(gdt *TShareddescriptorΠίνακας, mem *mem.TΜνήμηmanager, καταχώρησηpoint_2 func()) {

	self.επεξεργαστήςΚατάσταση = (*TcpuΚατάσταση)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuΚατάσταση{})))

	self.επεξεργαστήςΚατάσταση.Eax = 0
	self.επεξεργαστήςΚατάσταση.Ebx = 0
	self.επεξεργαστήςΚατάσταση.Ecx = 0
	self.επεξεργαστήςΚατάσταση.Edx = 0

	self.επεξεργαστήςΚατάσταση.Esi = 0
	self.επεξεργαστήςΚατάσταση.Edi = 0

	self.επεξεργαστήςΚατάσταση.Gs = 0
	self.επεξεργαστήςΚατάσταση.Fs = 0
	self.επεξεργαστήςΚατάσταση.Es = 0
	self.επεξεργαστήςΚατάσταση.Ds = 0

	self.επεξεργαστήςΚατάσταση.Eip = uint32(ValueOf(καταχώρησηpoint_2).Pointer())
	self.επεξεργαστήςΚατάσταση.Cs = Segkernelcode
	self.επεξεργαστήςΚατάσταση.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.επεξεργαστήςΚατάσταση)))

	self.επεξεργαστήςΚατάσταση.Esp = stackaddress
	self.επεξεργαστήςΚατάσταση.Ebp = stackaddress
	self.επεξεργαστήςΚατάσταση.Ss = 0

}

type TΔιεργασίαmanager struct {
}

var εργασίες [256]TΔιεργασία
var αριθμόςΕργασίες int
var τρέχονΔιεργασία int

func (self *TΔιεργασίαmanager) Init() {
	αριθμόςΕργασίες = 0
	τρέχονΔιεργασία = -1
}

func (self *TΔιεργασίαmanager) ΠροσθήκηΔιεργασία(διεργασία_2 TΔιεργασία) bool {
	if αριθμόςΕργασίες >= 255 {
		return false
	}
	εργασίες[αριθμόςΕργασίες] = διεργασία_2
	αριθμόςΕργασίες++
	return true
}

func (self *TΔιεργασίαmanager) Schedule(επεξεργαστήςΚατάσταση *TcpuΚατάσταση) *TcpuΚατάσταση {

	console_2 := TConsole{}
	for i := 0; i < αριθμόςΕργασίες; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(εργασίες[i].επεξεργαστήςΚατάσταση)))

		console_2.MUnsignedinteger32Εκτύπωσηxy(x, 10, uint16(15+i))
	}
	if αριθμόςΕργασίες <= 0 {
		return επεξεργαστήςΚατάσταση
	}

	if τρέχονΔιεργασία >= 0 {
		εργασίες[τρέχονΔιεργασία].επεξεργαστήςΚατάσταση = επεξεργαστήςΚατάσταση
	}

	τρέχονΔιεργασία++
	if τρέχονΔιεργασία >= αριθμόςΕργασίες {
		τρέχονΔιεργασία %= αριθμόςΕργασίες

	}

	return εργασίες[τρέχονΔιεργασία].επεξεργαστήςΚατάσταση
}
