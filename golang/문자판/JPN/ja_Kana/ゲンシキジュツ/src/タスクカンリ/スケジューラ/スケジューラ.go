package スケジューラ

import . "unsafe"
import . "reflect"

import . "コンソール"
import . "gdt"
import . "ポート"
import . "ハンヨウ/イチラン"

import . "ワリコミ"
import . "タスクカンリ/スレッド"
import . "タスクカンリ/tss"
import . "フクスウタスクカンリ"
import mem "メモリカンリシャ"

const Sスケジューラヒンド = 1
const Kチュウカクheapカイシ = 1024 * 1024
const スケジューラdebug = false
const pitヒンド = 100

var イチラン Linkedイチラン

type Sスケジューラデータ struct {
	ヒンド		uint32
	tickカウント	uint32

	switchforced	bool

	Eユウコウ	bool

	ゲンザイノニチジスレッド	*Tスレッド
	tss		*Tssentry
}

var scheデータ Sスケジューラデータ = Sスケジューラデータ{}

func (self *Sスケジューラデータ) Init() {
	scheデータ.tickカウント = 0
	scheデータ.ヒンド = Sスケジューラヒンド
	scheデータ.ゲンザイノニチジスレッド = nil
	scheデータ.Eユウコウ = false
	scheデータ.switchforced = false

}

var コンソール_2 = Tコンソール{}
var ゲンザイノニチジスレッドモクジ int = 0
var ツギプロセスid uint32 = 1

func Allocatepid() uint32 {
	pid := ツギプロセスid
	ツギプロセスid++
	return pid
}

func (self *Sスケジューラデータ) GetツギジュンビOKスレッド() *Tスレッド {
	if イチラン.Sサイズ_2 <= 0 {
		return nil
	}

	if scheデータ.ゲンザイノニチジスレッド != nil {
		ゲンザイノニチジスレッドモクジ = イチラン.Iモクジof(uintptr(Pointer(scheデータ.ゲンザイノニチジスレッド)))
		if ゲンザイノニチジスレッドモクジ < 0 {
			ゲンザイノニチジスレッドモクジ = 0
		}
	} else {
		ゲンザイノニチジスレッドモクジ = -1
	}

	for checked := 0; checked < イチラン.Sサイズ_2; checked++ {
		ゲンザイノニチジスレッドモクジ++
		if ゲンザイノニチジスレッドモクジ >= イチラン.Sサイズ_2 {
			ゲンザイノニチジスレッドモクジ = 0
		}
		スレッド := (*Tスレッド)(イチラン.Getat(ゲンザイノニチジスレッドモクジ))
		if スレッド != nil && スレッド.Tスレッドジョウタイ != Blocked && スレッド.Tスレッドジョウタイ != Sテイシ {
			if スケジューラdebug {
				コンソール_2.Mインサツ("ti:")
				コンソール_2.MUnsignedinteger32インサツ(uint32(ゲンザイノニチジスレッドモクジ))
				コンソール_2.Mインサツ(":")
				コンソール_2.MUnsignedinteger32インサツ(uint32(uintptr(Pointer(スレッド))))
			}
			return スレッド
		}
	}
	return scheデータ.ゲンザイノニチジスレッド

}
func (self *Sスケジューラ) Aツイカスレッド(スレッド *Tスレッド) {
	if スレッド == nil {
		return
	}
	イチラン.Mマツビニツイカ(uintptr(Pointer(スレッド)))
}
func Aツイカrunnableスレッド(スレッド *Tスレッド) {
	if スレッド == nil {
		return
	}
	イチラン.Mマツビニツイカ(uintptr(Pointer(スレッド)))
}

func Cゲンザイノニチジpid() uint32 {
	if scheデータ.ゲンザイノニチジスレッド == nil || scheデータ.ゲンザイノニチジスレッド.Pid == 0 {
		return 1
	}
	return scheデータ.ゲンザイノニチジスレッド.Pid
}

func Cゲンザイノニチジparentpid() uint32 {
	if scheデータ.ゲンザイノニチジスレッド == nil {
		return 0
	}
	return scheデータ.ゲンザイノニチジスレッド.Parentpid
}
func (self *Sスケジューラ) Rサクジョスレッド(スレッド *Tスレッド) {
	イチラン.Rサクジョ(uintptr(Pointer(スレッド)))
}

func (self *Sスケジューラ) Rサクジョスレッドat(モクジ int) {
	イチラン.Rサクジョat(モクジ)
}

type Sスケジューラ struct {
	Tワリコミhandler
}

func (self *Sスケジューラ) Init(カンリシャ *Tワリコミカンリシャ, mem *mem.Tメモリカンリシャ, tss *Tssentry) {
	scheデータ.Init()
	scheデータ.tss = tss
	initpit(pitヒンド)

	イチラン = Linkedイチラン{}
	イチラン.Init(mem)
	コンソール_2.Mインサツ("list:")
	コンソール_2.MUnsignedinteger32インサツ(uint32(uintptr(Pointer(&イチラン))))

	ワリコミhandler = トッテワリコミ
	var address uintptr
	address = uintptr(Pointer(&ワリコミhandler))
	self.Tワリコミhandler.Init(0x20, uintptr(Pointer(カンリシャ)), address)
}

func (self *Sスケジューラ) Eユウコウ(ユウコウ bool) {
	scheデータ.Eユウコウ = ユウコウ
}

func initpit(ヒンド uint32) {
	if ヒンド == 0 {
		return
	}
	divisor := uint32(1193180) / ヒンド
	Pポートカキコミバイト(0x43, 0x36)
	Pポートカキコミバイト(0x40, uint8(divisor&0xFF))
	Pポートカキコミバイト(0x40, uint8((divisor>>8)&0xFF))
}

func アリds(dssegment uint32)
func アリgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func フクゲンfpregs(buffer_2 uintptr)

var jmpリヨウシャ uint32 = 0
var ワリコミhandler func(uint32) uint32

func schedulestack(fn func())
func アリcr3(address uint32)
func getcr3() uint32

func トッテワリコミ(esp uint32) uint32 {

	scheデータ.tickカウント++

	if スケジューラdebug {
		コンソール_2.Mインサツxy(([]byte)("sche1:"), 1, 17)

		コンソール_2.Mインサツ(":")
		コンソール_2.MUnsignedinteger32インサツ(esp)
		コンソール_2.Mインサツ(":")

		コンソール_2.MUnsignedinteger32インサツ(uint32(scheデータ.tickカウント))
		コンソール_2.Mインサツ(":")
		コンソール_2.MUnsignedinteger32インサツ(Kチュウカクheapカイシ)
	}

	if scheデータ.tickカウント == scheデータ.ヒンド {
		scheデータ.tickカウント = 0

		if イチラン.Sサイズ_2 > 0 && scheデータ.Eユウコウ == true {
			var ツギスレッド = scheデータ.GetツギジュンビOKスレッド()
			if ツギスレッド == nil {
				return esp
			}
			if scheデータ.ゲンザイノニチジスレッド == nil {
				MEmergencyログモジレツ("\nSCHED first esp=")
				MEmergencyログunsignedinteger32(esp)
				MEmergencyログモジレツ(" thread=")
				MEmergencyログunsignedinteger32(uint32(uintptr(Pointer(ツギスレッド))))
				MEmergencyログモジレツ(" cpu=")
				MEmergencyログunsignedinteger32(uint32(uintptr(Pointer(ツギスレッド.Cpuジョウタイ))))
				MEmergencyログモジレツ(" state=")
				MEmergencyログunsignedinteger32(uint32(ツギスレッド.Tスレッドジョウタイ))
				MEmergencyログモジレツ(" eip=")
				MEmergencyログunsignedinteger32(ツギスレッド.Cpuジョウタイ.Eip)
				MEmergencyログモジレツ(" cs=")
				MEmergencyログunsignedinteger32(ツギスレッド.Cpuジョウタイ.Cs)
				MEmergencyログモジレツ("\n")
			}

			if esp >= Kチュウカクheapカイシ && scheデータ.ゲンザイノニチジスレッド != nil {
				scheデータ.ゲンザイノニチジスレッド.Cpuジョウタイ = (*Tcpuジョウタイ)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(scheデータ.ゲンザイノニチジスレッド.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				scheデータ.ゲンザイノニチジスレッド.Fpuoffset = offset
				backupfpregs(address + offset)
				if スケジューラdebug {
					コンソール_2.Mインサツ(([]byte)("backup"))
					コンソール_2.MUnsignedinteger32インサツ(esp)
				}
			}

			address := uintptr(Pointer(&(ツギスレッド.Fpubuffer)))
			offset := ツギスレッド.Fpuoffset
			if offset != 0xffffffff {
				フクゲンfpregs(address + offset)
				if スケジューラdebug {
					コンソール_2.Mインサツ(([]byte)("restore"))
				}
			}

			scheデータ.ゲンザイノニチジスレッド = ツギスレッド

			if scheデータ.ゲンザイノニチジスレッド.Tスレッドジョウタイ == Sキドウニチジ {
				scheデータ.ゲンザイノニチジスレッド.Tスレッドジョウタイ = RジュンビOK

				Initialスレッドリヨウシャjump(scheデータ.ゲンザイノニチジスレッド)
				return esp
			}

			esp = uint32(uintptr(Pointer(ツギスレッド.Cpuジョウタイ)))
			if ツギスレッド.Stack != 0 {
				scheデータ.tss.Sアリstack(Segチュウカクデータ, ツギスレッド.Stack+Tスレッドstackサイズ)
			}

			アリcr3(ツギスレッド.Pページディレクトリentry)
			アリgs(ツギスレッド.Cpuジョウタイ.Gs)

		}

	}

	return esp
}

func jumpユーザーモードiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Dフカint()

func getesp() uint32
func スレッドシュウリョウloop()

func アリスレッドシュウリョウloopジョウタイ(cpuジョウタイ *Tcpuジョウタイ) {
	cpuジョウタイ.Eip = uint32(ValueOf(スレッドシュウリョウloop).Pointer())
	cpuジョウタイ.Cs = Segチュウカクcode
	cpuジョウタイ.Ds = Segチュウカクデータ
	cpuジョウタイ.Es = Segチュウカクデータ
	cpuジョウタイ.Fs = Segチュウカクデータ
	cpuジョウタイ.Gs = Segチュウカクgs
	cpuジョウタイ.Ss = Segチュウカクデータ
	cpuジョウタイ.Eflags = 0x202
}

func Sテイシゲンザイノニチジスレッド(cpuジョウタイ *Tcpuジョウタイ) *Tcpuジョウタイ {
	if scheデータ.ゲンザイノニチジスレッド == nil {
		アリスレッドシュウリョウloopジョウタイ(cpuジョウタイ)
		return cpuジョウタイ
	}

	テイシスレッド := scheデータ.ゲンザイノニチジスレッド
	for i := 0; i < イチラン.Sサイズ_2; i++ {
		スレッド := (*Tスレッド)(イチラン.Getat(i))
		if スレッド != nil && スレッド.Cpuジョウタイ == cpuジョウタイ {
			テイシスレッド = スレッド
			break
		}
	}
	テイシスレッド.Cpuジョウタイ = cpuジョウタイ
	テイシスレッド.Tスレッドジョウタイ = Sテイシ
	scheデータ.ゲンザイノニチジスレッド = テイシスレッド

	ツギスレッド := scheデータ.GetツギジュンビOKスレッド()
	if ツギスレッド == nil || ツギスレッド == テイシスレッド || ツギスレッド.Cpuジョウタイ == nil || ツギスレッド.Cpuジョウタイ == cpuジョウタイ {
		アリスレッドシュウリョウloopジョウタイ(cpuジョウタイ)
		return cpuジョウタイ
	}

	scheデータ.ゲンザイノニチジスレッド = ツギスレッド
	if ツギスレッド.Stack != 0 && scheデータ.tss != nil {
		scheデータ.tss.Sアリstack(Segチュウカクデータ, ツギスレッド.Stack+Tスレッドstackサイズ)
	}
	アリcr3(ツギスレッド.Pページディレクトリentry)
	アリgs(ツギスレッド.Cpuジョウタイ.Gs)
	return ツギスレッド.Cpuジョウタイ
}

func Initialスレッドリヨウシャjump(スレッド *Tスレッド) {

	Dフカint()

	scheデータ.tss.Sアリstack(Segチュウカクデータ, スレッド.Stack+Tスレッドstackサイズ)

	アリcr3(スレッド.Pページディレクトリentry)
	アリgs(スレッド.Cpuジョウタイ.Gs)

	scheデータ.ゲンザイノニチジスレッド = スレッド
	scheデータ.Eユウコウ = true

	eip := スレッド.Cpuジョウタイ.Eip
	リヨウシャesp := スレッド.Uリヨウシャstack_2 + スレッド.Uリヨウシャstackサイズ_2
	eflags := スレッド.Cpuジョウタイ.Eflags
	cs := スレッド.Cpuジョウタイ.Cs
	esp := scheデータ.tss.Getesp0()

	コンソール_2.Mインサツ(([]byte)("jump["))
	コンソール_2.MUnsignedinteger32インサツ(eip)
	コンソール_2.Mインサツ(([]byte)(":"))
	コンソール_2.MUnsignedinteger32インサツ(リヨウシャesp)
	コンソール_2.Mインサツ(([]byte)(":"))
	コンソール_2.MUnsignedinteger32インサツ(eflags)
	コンソール_2.Mインサツ(([]byte)(":"))
	コンソール_2.MUnsignedinteger32インサツ(cs)
	コンソール_2.Mインサツ(([]byte)(":"))

	コンソール_2.MUnsignedinteger32インサツ(esp)
	コンソール_2.Mインサツ(([]byte)("]"))

	userprocentry := スレッド.Cpuジョウタイ.Ecx
	ゼンパンoffsettable_2 := スレッド.Cpuジョウタイ.Edx
	ドウテキニ := スレッド.Cpuジョウタイ.Esi

	Pポートカキコミバイト(0x20, 0x20)
	jumpユーザーモードiret(eip, リヨウシャesp, eflags, userprocentry, ゼンパンoffsettable_2, ドウテキニ)
	コンソール_2.Mインサツ(([]byte)("usermode end"))
}
func インサツesp(esp uint32) {
	コンソール_2.Mインサツ(([]byte)("esp["))
	コンソール_2.MUnsignedinteger32インサツ(esp)
}
