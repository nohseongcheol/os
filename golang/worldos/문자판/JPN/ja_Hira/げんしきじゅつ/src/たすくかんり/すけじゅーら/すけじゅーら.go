/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package すけじゅーら

import . "unsafe"
import . "reflect"

import . "こんそーる"
import . "gdt"
import . "ぽーと"
import . "はんよう/いちらん"

import . "わりこみ"
import . "たすくかんり/すれっど"
import . "たすくかんり/tss"
import . "ふくすうたすくかんり"
import mem "めもりかんりしゃ"

const Sすけじゅーらひんど = 1
const Kちゅうかくheapかいし = 1024 * 1024
const すけじゅーらdebug = false
const pitひんど = 100

var いちらん Linkedいちらん

type Sすけじゅーらでーた struct {
	ひんど		uint32
	tickかうんと	uint32

	switchforced	bool

	Eゆうこう	bool

	げんざいのにちじすれっど	*Tすれっど
	tss		*Tssentry
}

var scheでーた Sすけじゅーらでーた = Sすけじゅーらでーた{}

func (self *Sすけじゅーらでーた) Init() {
	scheでーた.tickかうんと = 0
	scheでーた.ひんど = Sすけじゅーらひんど
	scheでーた.げんざいのにちじすれっど = nil
	scheでーた.Eゆうこう = false
	scheでーた.switchforced = false

}

var こんそーる_2 = Tこんそーる{}
var げんざいのにちじすれっどもくじ int = 0
var つぎぷろせすid uint32 = 1

func Allocatepid() uint32 {
	pid := つぎぷろせすid
	つぎぷろせすid++
	return pid
}

func (self *Sすけじゅーらでーた) GetつぎじゅんびOKすれっど() *Tすれっど {
	if いちらん.Sさいず_2 <= 0 {
		return nil
	}

	if scheでーた.げんざいのにちじすれっど != nil {
		げんざいのにちじすれっどもくじ = いちらん.Iもくじof(uintptr(Pointer(scheでーた.げんざいのにちじすれっど)))
		if げんざいのにちじすれっどもくじ < 0 {
			げんざいのにちじすれっどもくじ = 0
		}
	} else {
		げんざいのにちじすれっどもくじ = -1
	}

	for checked := 0; checked < いちらん.Sさいず_2; checked++ {
		げんざいのにちじすれっどもくじ++
		if げんざいのにちじすれっどもくじ >= いちらん.Sさいず_2 {
			げんざいのにちじすれっどもくじ = 0
		}
		すれっど := (*Tすれっど)(いちらん.Getat(げんざいのにちじすれっどもくじ))
		if すれっど != nil && すれっど.Tすれっどじょうたい != Blocked && すれっど.Tすれっどじょうたい != Sていし {
			if すけじゅーらdebug {
				こんそーる_2.Mいんさつ("ti:")
				こんそーる_2.MUnsignedinteger32いんさつ(uint32(げんざいのにちじすれっどもくじ))
				こんそーる_2.Mいんさつ(":")
				こんそーる_2.MUnsignedinteger32いんさつ(uint32(uintptr(Pointer(すれっど))))
			}
			return すれっど
		}
	}
	return scheでーた.げんざいのにちじすれっど

}
func (self *Sすけじゅーら) Aついかすれっど(すれっど *Tすれっど) {
	if すれっど == nil {
		return
	}
	いちらん.Mまつびについか(uintptr(Pointer(すれっど)))
}
func Aついかrunnableすれっど(すれっど *Tすれっど) {
	if すれっど == nil {
		return
	}
	いちらん.Mまつびについか(uintptr(Pointer(すれっど)))
}

func Cげんざいのにちじpid() uint32 {
	if scheでーた.げんざいのにちじすれっど == nil || scheでーた.げんざいのにちじすれっど.Pid == 0 {
		return 1
	}
	return scheでーた.げんざいのにちじすれっど.Pid
}

func Cげんざいのにちじparentpid() uint32 {
	if scheでーた.げんざいのにちじすれっど == nil {
		return 0
	}
	return scheでーた.げんざいのにちじすれっど.Parentpid
}
func (self *Sすけじゅーら) Rさくじょすれっど(すれっど *Tすれっど) {
	いちらん.Rさくじょ(uintptr(Pointer(すれっど)))
}

func (self *Sすけじゅーら) Rさくじょすれっどat(もくじ int) {
	いちらん.Rさくじょat(もくじ)
}

type Sすけじゅーら struct {
	Tわりこみhandler
}

func (self *Sすけじゅーら) Init(かんりしゃ *Tわりこみかんりしゃ, mem *mem.Tめもりかんりしゃ, tss *Tssentry) {
	scheでーた.Init()
	scheでーた.tss = tss
	initpit(pitひんど)

	いちらん = Linkedいちらん{}
	いちらん.Init(mem)
	こんそーる_2.Mいんさつ("list:")
	こんそーる_2.MUnsignedinteger32いんさつ(uint32(uintptr(Pointer(&いちらん))))

	わりこみhandler = とってわりこみ
	var address uintptr
	address = uintptr(Pointer(&わりこみhandler))
	self.Tわりこみhandler.Init(0x20, uintptr(Pointer(かんりしゃ)), address)
}

func (self *Sすけじゅーら) Eゆうこう(ゆうこう bool) {
	scheでーた.Eゆうこう = ゆうこう
}

func initpit(ひんど uint32) {
	if ひんど == 0 {
		return
	}
	divisor := uint32(1193180) / ひんど
	Pぽーとかきこみばいと(0x43, 0x36)
	Pぽーとかきこみばいと(0x40, uint8(divisor&0xFF))
	Pぽーとかきこみばいと(0x40, uint8((divisor>>8)&0xFF))
}

func ありds(dssegment uint32)
func ありgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func ふくげんfpregs(buffer_2 uintptr)

var jmpりようしゃ uint32 = 0
var わりこみhandler func(uint32) uint32

func schedulestack(fn func())
func ありcr3(address uint32)
func getcr3() uint32

func とってわりこみ(esp uint32) uint32 {

	scheでーた.tickかうんと++

	if すけじゅーらdebug {
		こんそーる_2.Mいんさつxy(([]byte)("sche1:"), 1, 17)

		こんそーる_2.Mいんさつ(":")
		こんそーる_2.MUnsignedinteger32いんさつ(esp)
		こんそーる_2.Mいんさつ(":")

		こんそーる_2.MUnsignedinteger32いんさつ(uint32(scheでーた.tickかうんと))
		こんそーる_2.Mいんさつ(":")
		こんそーる_2.MUnsignedinteger32いんさつ(Kちゅうかくheapかいし)
	}

	if scheでーた.tickかうんと == scheでーた.ひんど {
		scheでーた.tickかうんと = 0

		if いちらん.Sさいず_2 > 0 && scheでーた.Eゆうこう == true {
			var つぎすれっど = scheでーた.GetつぎじゅんびOKすれっど()
			if つぎすれっど == nil {
				return esp
			}
			if scheでーた.げんざいのにちじすれっど == nil {
				MEmergencyろぐもじれつ("\nSCHED first esp=")
				MEmergencyろぐunsignedinteger32(esp)
				MEmergencyろぐもじれつ(" thread=")
				MEmergencyろぐunsignedinteger32(uint32(uintptr(Pointer(つぎすれっど))))
				MEmergencyろぐもじれつ(" cpu=")
				MEmergencyろぐunsignedinteger32(uint32(uintptr(Pointer(つぎすれっど.Cpuじょうたい))))
				MEmergencyろぐもじれつ(" state=")
				MEmergencyろぐunsignedinteger32(uint32(つぎすれっど.Tすれっどじょうたい))
				MEmergencyろぐもじれつ(" eip=")
				MEmergencyろぐunsignedinteger32(つぎすれっど.Cpuじょうたい.Eip)
				MEmergencyろぐもじれつ(" cs=")
				MEmergencyろぐunsignedinteger32(つぎすれっど.Cpuじょうたい.Cs)
				MEmergencyろぐもじれつ("\n")
			}

			if esp >= Kちゅうかくheapかいし && scheでーた.げんざいのにちじすれっど != nil {
				scheでーた.げんざいのにちじすれっど.Cpuじょうたい = (*Tcpuじょうたい)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(scheでーた.げんざいのにちじすれっど.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				scheでーた.げんざいのにちじすれっど.Fpuoffset = offset
				backupfpregs(address + offset)
				if すけじゅーらdebug {
					こんそーる_2.Mいんさつ(([]byte)("backup"))
					こんそーる_2.MUnsignedinteger32いんさつ(esp)
				}
			}

			address := uintptr(Pointer(&(つぎすれっど.Fpubuffer)))
			offset := つぎすれっど.Fpuoffset
			if offset != 0xffffffff {
				ふくげんfpregs(address + offset)
				if すけじゅーらdebug {
					こんそーる_2.Mいんさつ(([]byte)("restore"))
				}
			}

			scheでーた.げんざいのにちじすれっど = つぎすれっど

			if scheでーた.げんざいのにちじすれっど.Tすれっどじょうたい == Sきどうにちじ {
				scheでーた.げんざいのにちじすれっど.Tすれっどじょうたい = RじゅんびOK

				Initialすれっどりようしゃjump(scheでーた.げんざいのにちじすれっど)
				return esp
			}

			esp = uint32(uintptr(Pointer(つぎすれっど.Cpuじょうたい)))
			if つぎすれっど.Stack != 0 {
				scheでーた.tss.Sありstack(Segちゅうかくでーた, つぎすれっど.Stack+Tすれっどstackさいず)
			}

			ありcr3(つぎすれっど.Pぺーじでぃれくとりentry)
			ありgs(つぎすれっど.Cpuじょうたい.Gs)

		}

	}

	return esp
}

func jumpゆーざーもーどiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Dふかint()

func getesp() uint32
func すれっどしゅうりょうloop()

func ありすれっどしゅうりょうloopじょうたい(cpuじょうたい *Tcpuじょうたい) {
	cpuじょうたい.Eip = uint32(ValueOf(すれっどしゅうりょうloop).Pointer())
	cpuじょうたい.Cs = Segちゅうかくcode
	cpuじょうたい.Ds = Segちゅうかくでーた
	cpuじょうたい.Es = Segちゅうかくでーた
	cpuじょうたい.Fs = Segちゅうかくでーた
	cpuじょうたい.Gs = Segちゅうかくgs
	cpuじょうたい.Ss = Segちゅうかくでーた
	cpuじょうたい.Eflags = 0x202
}

func Sていしげんざいのにちじすれっど(cpuじょうたい *Tcpuじょうたい) *Tcpuじょうたい {
	if scheでーた.げんざいのにちじすれっど == nil {
		ありすれっどしゅうりょうloopじょうたい(cpuじょうたい)
		return cpuじょうたい
	}

	ていしすれっど := scheでーた.げんざいのにちじすれっど
	for i := 0; i < いちらん.Sさいず_2; i++ {
		すれっど := (*Tすれっど)(いちらん.Getat(i))
		if すれっど != nil && すれっど.Cpuじょうたい == cpuじょうたい {
			ていしすれっど = すれっど
			break
		}
	}
	ていしすれっど.Cpuじょうたい = cpuじょうたい
	ていしすれっど.Tすれっどじょうたい = Sていし
	scheでーた.げんざいのにちじすれっど = ていしすれっど

	つぎすれっど := scheでーた.GetつぎじゅんびOKすれっど()
	if つぎすれっど == nil || つぎすれっど == ていしすれっど || つぎすれっど.Cpuじょうたい == nil || つぎすれっど.Cpuじょうたい == cpuじょうたい {
		ありすれっどしゅうりょうloopじょうたい(cpuじょうたい)
		return cpuじょうたい
	}

	scheでーた.げんざいのにちじすれっど = つぎすれっど
	if つぎすれっど.Stack != 0 && scheでーた.tss != nil {
		scheでーた.tss.Sありstack(Segちゅうかくでーた, つぎすれっど.Stack+Tすれっどstackさいず)
	}
	ありcr3(つぎすれっど.Pぺーじでぃれくとりentry)
	ありgs(つぎすれっど.Cpuじょうたい.Gs)
	return つぎすれっど.Cpuじょうたい
}

func Initialすれっどりようしゃjump(すれっど *Tすれっど) {

	Dふかint()

	scheでーた.tss.Sありstack(Segちゅうかくでーた, すれっど.Stack+Tすれっどstackさいず)

	ありcr3(すれっど.Pぺーじでぃれくとりentry)
	ありgs(すれっど.Cpuじょうたい.Gs)

	scheでーた.げんざいのにちじすれっど = すれっど
	scheでーた.Eゆうこう = true

	eip := すれっど.Cpuじょうたい.Eip
	りようしゃesp := すれっど.Uりようしゃstack_2 + すれっど.Uりようしゃstackさいず_2
	eflags := すれっど.Cpuじょうたい.Eflags
	cs := すれっど.Cpuじょうたい.Cs
	esp := scheでーた.tss.Getesp0()

	こんそーる_2.Mいんさつ(([]byte)("jump["))
	こんそーる_2.MUnsignedinteger32いんさつ(eip)
	こんそーる_2.Mいんさつ(([]byte)(":"))
	こんそーる_2.MUnsignedinteger32いんさつ(りようしゃesp)
	こんそーる_2.Mいんさつ(([]byte)(":"))
	こんそーる_2.MUnsignedinteger32いんさつ(eflags)
	こんそーる_2.Mいんさつ(([]byte)(":"))
	こんそーる_2.MUnsignedinteger32いんさつ(cs)
	こんそーる_2.Mいんさつ(([]byte)(":"))

	こんそーる_2.MUnsignedinteger32いんさつ(esp)
	こんそーる_2.Mいんさつ(([]byte)("]"))

	userprocentry := すれっど.Cpuじょうたい.Ecx
	ぜんぱんoffsettable_2 := すれっど.Cpuじょうたい.Edx
	どうてきに := すれっど.Cpuじょうたい.Esi

	Pぽーとかきこみばいと(0x20, 0x20)
	jumpゆーざーもーどiret(eip, りようしゃesp, eflags, userprocentry, ぜんぱんoffsettable_2, どうてきに)
	こんそーる_2.Mいんさつ(([]byte)("usermode end"))
}
func いんさつesp(esp uint32) {
	こんそーる_2.Mいんさつ(([]byte)("esp["))
	こんそーる_2.MUnsignedinteger32いんさつ(esp)
}
