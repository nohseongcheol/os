package フクスウタスクカンリ

import . "unsafe"
import . "コンソール"
import . "reflect"
import mem "メモリカンリシャ"
import . "gdt"

var Tテスト uint8

func halt()

type Tcpuジョウタイ struct {
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

type Tタスク struct {
	ツミカサネキオクリョウイキ	[4096]uint8
	cpuジョウタイ	*Tcpuジョウタイ
}

func (self *Tタスク) Init(gdt *TShareddescriptortable, mem *mem.Tメモリカンリシャ, entrypoint_2 func()) {

	self.cpuジョウタイ = (*Tcpuジョウタイ)(Pointer(uintptr(mem.Mキオクリョウイキヲカクホ(1024*1024)) + 1024*1024 - Sizeof(Tcpuジョウタイ{})))

	self.cpuジョウタイ.Eax = 0
	self.cpuジョウタイ.Ebx = 0
	self.cpuジョウタイ.Ecx = 0
	self.cpuジョウタイ.Edx = 0

	self.cpuジョウタイ.Esi = 0
	self.cpuジョウタイ.Edi = 0

	self.cpuジョウタイ.Gs = 0
	self.cpuジョウタイ.Fs = 0
	self.cpuジョウタイ.Es = 0
	self.cpuジョウタイ.Ds = 0

	self.cpuジョウタイ.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.cpuジョウタイ.Cs = Segチュウカクcode
	self.cpuジョウタイ.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpuジョウタイ)))

	self.cpuジョウタイ.Esp = stackaddress
	self.cpuジョウタイ.Ebp = stackaddress
	self.cpuジョウタイ.Ss = 0

}

type Tタスクカンリシャ struct {
}

var タスク_2 [256]Tタスク
var numberタスク int
var ゲンザイノニチジタスク int

func (self *Tタスクカンリシャ) Init() {
	numberタスク = 0
	ゲンザイノニチジタスク = -1
}

func (self *Tタスクカンリシャ) Aツイカタスク(タスク Tタスク) bool {
	if numberタスク >= 255 {
		return false
	}
	タスク_2[numberタスク] = タスク
	numberタスク++
	return true
}

func (self *Tタスクカンリシャ) Schedule(cpuジョウタイ *Tcpuジョウタイ) *Tcpuジョウタイ {

	コンソール_2 := Tコンソール{}
	for i := 0; i < numberタスク; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(タスク_2[i].cpuジョウタイ)))

		コンソール_2.MUnsignedinteger32インサツxy(x, 10, uint16(15+i))
	}
	if numberタスク <= 0 {
		return cpuジョウタイ
	}

	if ゲンザイノニチジタスク >= 0 {
		タスク_2[ゲンザイノニチジタスク].cpuジョウタイ = cpuジョウタイ
	}

	ゲンザイノニチジタスク++
	if ゲンザイノニチジタスク >= numberタスク {
		ゲンザイノニチジタスク %= numberタスク

	}

	return タスク_2[ゲンザイノニチジタスク].cpuジョウタイ
}
