/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Tすれっど_2

import . "unsafe"
import . "reflect"
import . "gdt"
import . "こんそーる"
import . "ふくすうたすくかんり"
import mem "めもりかんりしゃ"
import . "かそうめもり"

const (
	Blocked	= 1
	RじゅんびOK	= 2
	Sていし	= 3
	Sきどうにちじ	= 4
)

const Tすれっどstackさいず = 32 * 1024

type Tすれっど struct {
	Cpuじょうたい		*Tcpuじょうたい
	Stack		uint32
	Uりようしゃstack_2	uint32
	Uりようしゃstackさいず_2	uint32
	Pid		uint32
	Parentpid	uint32

	Pぺーじでぃれくとりentry	uint32

	Tすれっどじょうたい		uint8
	Blockedじょうたい	uint8

	じかんでるた	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Isちゅうかく		bool
}

func (self *Tすれっど) Nしんき() {
}

type Tすれっどhelper struct {
	mem *mem.Tめもりかんりしゃ
}

var こんそーる_2 = Tこんそーる{}

func (self *Tすれっどhelper) Init(mem *mem.Tめもりかんりしゃ) {
	self.mem = mem
	こんそーる_2.Mいんさつxy(([]byte)("thread:"), 1, 14)
}
func (self *Tすれっどhelper) Cさくせいからかんすう(entrypoint_2 func(), Pぺーじでぃれくとりentry uint32, isちゅうかく bool) Tすれっど {
	せいせいさき := Tすれっど{}

	せいせいさき.Stack = uint32(uintptr(self.mem.Mきおくりょういきをかくほ(Tすれっどstackさいず)))
	if せいせいさき.Stack == 0 {
		return せいせいさき
	}
	こんそーる_2.Mいんさつ(([]byte)("[mem:"))
	こんそーる_2.MUnsignedinteger32いんさつ(せいせいさき.Stack)

	せいせいさき.Cpuじょうたい = (*Tcpuじょうたい)(Pointer(uintptr(せいせいさき.Stack) + Tすれっどstackさいず - Sizeof(Tcpuじょうたい{})))
	せいせいさき.Cpuじょうたい.Esp = せいせいさき.Stack + Tすれっどstackさいず
	せいせいさき.Cpuじょうたい.Ebp = せいせいさき.Cpuじょうたい.Esp
	せいせいさき.Cpuじょうたい.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	せいせいさき.Uりようしゃstack_2 = Uりようしゃstack
	せいせいさき.Uりようしゃstackさいず_2 = Uりようしゃstackさいず
	せいせいさき.Pid = 0
	せいせいさき.Parentpid = 0
	せいせいさき.Pぺーじでぃれくとりentry = Pぺーじでぃれくとりentry
	こんそーる_2.Mいんさつ((([]byte)("cpu")))

	こんそーる_2.MUnsignedinteger32いんさつ(uint32(uintptr(Pointer(せいせいさき.Cpuじょうたい))))

	こんそーる_2.Mいんさつ((([]byte)(":")))
	こんそーる_2.MUnsignedinteger32いんさつ(せいせいさき.Cpuじょうたい.Eip)

	こんそーる_2.Mいんさつ("]")
	if isちゅうかく == true {
		せいせいさき.Cpuじょうたい.Cs = Segちゅうかくcode
		せいせいさき.Cpuじょうたい.Ds = Segちゅうかくでーた
		せいせいさき.Cpuじょうたい.Es = Segちゅうかくでーた
		せいせいさき.Cpuじょうたい.Fs = Segちゅうかくでーた
		せいせいさき.Cpuじょうたい.Gs = Segちゅうかくgs
		せいせいさき.Cpuじょうたい.Ss = Segちゅうかくでーた
		せいせいさき.Tすれっどじょうたい = RじゅんびOK
		せいせいさき.Cpuじょうたい.Eflags = 0x202
	} else {
		せいせいさき.Cpuじょうたい.Cs = Segりようしゃcode
		せいせいさき.Cpuじょうたい.Ds = Segりようしゃでーた
		せいせいさき.Cpuじょうたい.Es = Segりようしゃでーた
		せいせいさき.Cpuじょうたい.Fs = Segりようしゃでーた
		せいせいさき.Cpuじょうたい.Gs = Segりようしゃgs
		せいせいさき.Cpuじょうたい.Ss = Segりようしゃでーた
		せいせいさき.Tすれっどじょうたい = Sきどうにちじ
		せいせいさき.Cpuじょうたい.Eflags = 0x222
	}
	せいせいさき.Isちゅうかく = isちゅうかく
	せいせいさき.Fpuoffset = 0xffffffff

	return せいせいさき
}

func (self *Tすれっどhelper) Cさくせいぽいんたからかんすう(entrypoint_2 func(), Pぺーじでぃれくとりentry uint32, isちゅうかく bool) *Tすれっど {
	せいせいさき := (*Tすれっど)(self.mem.Mきおくりょういきをかくほ(uint32(Sizeof(Tすれっど{}))))
	if せいせいさき == nil {
		return nil
	}
	*せいせいさき = self.Cさくせいからかんすう(entrypoint_2, Pぺーじでぃれくとりentry, isちゅうかく)
	if せいせいさき.Cpuじょうたい == nil {
		self.mem.Fあき(Pointer(せいせいさき))
		return nil
	}
	return せいせいさき
}
