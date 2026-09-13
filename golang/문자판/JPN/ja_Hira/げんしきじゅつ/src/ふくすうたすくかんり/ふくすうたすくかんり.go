package ふくすうたすくかんり

import . "unsafe"
import . "こんそーる"
import . "reflect"
import mem "めもりかんりしゃ"
import . "gdt"

var Tてすと uint8

func halt()

type Tcpuじょうたい struct {
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

type Tたすく struct {
	つみかさねきおくりょういき	[4096]uint8
	cpuじょうたい	*Tcpuじょうたい
}

func (self *Tたすく) Init(gdt *TShareddescriptortable, mem *mem.Tめもりかんりしゃ, entrypoint_2 func()) {

	self.cpuじょうたい = (*Tcpuじょうたい)(Pointer(uintptr(mem.Mきおくりょういきをかくほ(1024*1024)) + 1024*1024 - Sizeof(Tcpuじょうたい{})))

	self.cpuじょうたい.Eax = 0
	self.cpuじょうたい.Ebx = 0
	self.cpuじょうたい.Ecx = 0
	self.cpuじょうたい.Edx = 0

	self.cpuじょうたい.Esi = 0
	self.cpuじょうたい.Edi = 0

	self.cpuじょうたい.Gs = 0
	self.cpuじょうたい.Fs = 0
	self.cpuじょうたい.Es = 0
	self.cpuじょうたい.Ds = 0

	self.cpuじょうたい.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.cpuじょうたい.Cs = Segちゅうかくcode
	self.cpuじょうたい.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpuじょうたい)))

	self.cpuじょうたい.Esp = stackaddress
	self.cpuじょうたい.Ebp = stackaddress
	self.cpuじょうたい.Ss = 0

}

type Tたすくかんりしゃ struct {
}

var たすく_2 [256]Tたすく
var numberたすく int
var げんざいのにちじたすく int

func (self *Tたすくかんりしゃ) Init() {
	numberたすく = 0
	げんざいのにちじたすく = -1
}

func (self *Tたすくかんりしゃ) Aついかたすく(たすく Tたすく) bool {
	if numberたすく >= 255 {
		return false
	}
	たすく_2[numberたすく] = たすく
	numberたすく++
	return true
}

func (self *Tたすくかんりしゃ) Schedule(cpuじょうたい *Tcpuじょうたい) *Tcpuじょうたい {

	こんそーる_2 := Tこんそーる{}
	for i := 0; i < numberたすく; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(たすく_2[i].cpuじょうたい)))

		こんそーる_2.MUnsignedinteger32いんさつxy(x, 10, uint16(15+i))
	}
	if numberたすく <= 0 {
		return cpuじょうたい
	}

	if げんざいのにちじたすく >= 0 {
		たすく_2[げんざいのにちじたすく].cpuじょうたい = cpuじょうたい
	}

	げんざいのにちじたすく++
	if げんざいのにちじたすく >= numberたすく {
		げんざいのにちじたすく %= numberたすく

	}

	return たすく_2[げんざいのにちじたすく].cpuじょうたい
}
