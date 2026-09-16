/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "konsol"
import . "reflect"
import mem "bellekmanager"
import . "gdt"

var Dene uint8

func halt()

type TcpuDurum struct {
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

type TGörev struct {
	yığın_belleği		[4096]uint8
	mİBDurum	*TcpuDurum
}

func (self *TGörev) Init(gdt *TShareddescriptorTablo, mem *mem.TBellekmanager, girdipoint_2 func()) {

	self.mİBDurum = (*TcpuDurum)(Pointer(uintptr(mem.Bellek_ayır(1024*1024)) + 1024*1024 - Sizeof(TcpuDurum{})))

	self.mİBDurum.Eax = 0
	self.mİBDurum.Ebx = 0
	self.mİBDurum.Ecx = 0
	self.mİBDurum.Edx = 0

	self.mİBDurum.Esi = 0
	self.mİBDurum.Edi = 0

	self.mİBDurum.Gs = 0
	self.mİBDurum.Fs = 0
	self.mİBDurum.Es = 0
	self.mİBDurum.Ds = 0

	self.mİBDurum.Eip = uint32(ValueOf(girdipoint_2).Pointer())
	self.mİBDurum.Cs = Segkernelcode
	self.mİBDurum.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.mİBDurum)))

	self.mİBDurum.Esp = stackaddress
	self.mİBDurum.Ebp = stackaddress
	self.mİBDurum.Ss = 0

}

type TGörevmanager struct {
}

var işler [256]TGörev
var sayıİşler int
var şuanGörev int

func (self *TGörevmanager) Init() {
	sayıİşler = 0
	şuanGörev = -1
}

func (self *TGörevmanager) EkleGörev(görev TGörev) bool {
	if sayıİşler >= 255 {
		return false
	}
	işler[sayıİşler] = görev
	sayıİşler++
	return true
}

func (self *TGörevmanager) Schedule(mİBDurum *TcpuDurum) *TcpuDurum {

	konsol_2 := TKonsol{}
	for i := 0; i < sayıİşler; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(işler[i].mİBDurum)))

		konsol_2.MUnsignedinteger32Yazdırxy(x, 10, uint16(15+i))
	}
	if sayıİşler <= 0 {
		return mİBDurum
	}

	if şuanGörev >= 0 {
		işler[şuanGörev].mİBDurum = mİBDurum
	}

	şuanGörev++
	if şuanGörev >= sayıİşler {
		şuanGörev %= sayıİşler

	}

	return işler[şuanGörev].mİBDurum
}
