package スケジューラ

import . "unsafe"
import . "reflect"

import . "コンソール"
import . "gdt"
import . "ポート"
import . "汎用/一覧"

import . "割込み"
import . "タスク管理/スレッド"
import . "タスク管理/tss"
import . "複数タスク管理"
import mem "メモリ管理者"

const Sスケジューラ頻度 = 1
const K中核heap開始 = 1024 * 1024
const スケジューラdebug = false
const pit頻度 = 100

var 一覧 Linked一覧

type Sスケジューラデータ struct {
	頻度		uint32
	tickカウント	uint32

	switchforced	bool

	E有効	bool

	現在の日時スレッド	*Tスレッド
	tss		*Tssentry
}

var scheデータ Sスケジューラデータ = Sスケジューラデータ{}

func (self *Sスケジューラデータ) Init() {
	scheデータ.tickカウント = 0
	scheデータ.頻度 = Sスケジューラ頻度
	scheデータ.現在の日時スレッド = nil
	scheデータ.E有効 = false
	scheデータ.switchforced = false

}

var コンソール_2 = Tコンソール{}
var 現在の日時スレッド目次 int = 0
var 次プロセスid uint32 = 1

func Allocatepid() uint32 {
	pid := 次プロセスid
	次プロセスid++
	return pid
}

func (self *Sスケジューラデータ) Get次準備OKスレッド() *Tスレッド {
	if 一覧.Sサイズ_2 <= 0 {
		return nil
	}

	if scheデータ.現在の日時スレッド != nil {
		現在の日時スレッド目次 = 一覧.I目次of(uintptr(Pointer(scheデータ.現在の日時スレッド)))
		if 現在の日時スレッド目次 < 0 {
			現在の日時スレッド目次 = 0
		}
	} else {
		現在の日時スレッド目次 = -1
	}

	for checked := 0; checked < 一覧.Sサイズ_2; checked++ {
		現在の日時スレッド目次++
		if 現在の日時スレッド目次 >= 一覧.Sサイズ_2 {
			現在の日時スレッド目次 = 0
		}
		スレッド := (*Tスレッド)(一覧.Getat(現在の日時スレッド目次))
		if スレッド != nil && スレッド.Tスレッド状態 != Blocked && スレッド.Tスレッド状態 != S停止 {
			if スケジューラdebug {
				コンソール_2.M印刷("ti:")
				コンソール_2.MUnsignedinteger32印刷(uint32(現在の日時スレッド目次))
				コンソール_2.M印刷(":")
				コンソール_2.MUnsignedinteger32印刷(uint32(uintptr(Pointer(スレッド))))
			}
			return スレッド
		}
	}
	return scheデータ.現在の日時スレッド

}
func (self *Sスケジューラ) A追加スレッド(スレッド *Tスレッド) {
	if スレッド == nil {
		return
	}
	一覧.M末尾に追加(uintptr(Pointer(スレッド)))
}
func A追加runnableスレッド(スレッド *Tスレッド) {
	if スレッド == nil {
		return
	}
	一覧.M末尾に追加(uintptr(Pointer(スレッド)))
}

func C現在の日時pid() uint32 {
	if scheデータ.現在の日時スレッド == nil || scheデータ.現在の日時スレッド.Pid == 0 {
		return 1
	}
	return scheデータ.現在の日時スレッド.Pid
}

func C現在の日時parentpid() uint32 {
	if scheデータ.現在の日時スレッド == nil {
		return 0
	}
	return scheデータ.現在の日時スレッド.Parentpid
}
func (self *Sスケジューラ) R削除スレッド(スレッド *Tスレッド) {
	一覧.R削除(uintptr(Pointer(スレッド)))
}

func (self *Sスケジューラ) R削除スレッドat(目次 int) {
	一覧.R削除at(目次)
}

type Sスケジューラ struct {
	T割込みhandler
}

func (self *Sスケジューラ) Init(管理者 *T割込み管理者, mem *mem.Tメモリ管理者, tss *Tssentry) {
	scheデータ.Init()
	scheデータ.tss = tss
	initpit(pit頻度)

	一覧 = Linked一覧{}
	一覧.Init(mem)
	コンソール_2.M印刷("list:")
	コンソール_2.MUnsignedinteger32印刷(uint32(uintptr(Pointer(&一覧))))

	割込みhandler = 取っ手割込み
	var address uintptr
	address = uintptr(Pointer(&割込みhandler))
	self.T割込みhandler.Init(0x20, uintptr(Pointer(管理者)), address)
}

func (self *Sスケジューラ) E有効(有効 bool) {
	scheデータ.E有効 = 有効
}

func initpit(頻度 uint32) {
	if 頻度 == 0 {
		return
	}
	divisor := uint32(1193180) / 頻度
	Pポート書込みバイト(0x43, 0x36)
	Pポート書込みバイト(0x40, uint8(divisor&0xFF))
	Pポート書込みバイト(0x40, uint8((divisor>>8)&0xFF))
}

func ありds(dssegment uint32)
func ありgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func 復元fpregs(buffer_2 uintptr)

var jmp利用者 uint32 = 0
var 割込みhandler func(uint32) uint32

func schedulestack(fn func())
func ありcr3(address uint32)
func getcr3() uint32

func 取っ手割込み(esp uint32) uint32 {

	scheデータ.tickカウント++

	if スケジューラdebug {
		コンソール_2.M印刷xy(([]byte)("sche1:"), 1, 17)

		コンソール_2.M印刷(":")
		コンソール_2.MUnsignedinteger32印刷(esp)
		コンソール_2.M印刷(":")

		コンソール_2.MUnsignedinteger32印刷(uint32(scheデータ.tickカウント))
		コンソール_2.M印刷(":")
		コンソール_2.MUnsignedinteger32印刷(K中核heap開始)
	}

	if scheデータ.tickカウント == scheデータ.頻度 {
		scheデータ.tickカウント = 0

		if 一覧.Sサイズ_2 > 0 && scheデータ.E有効 == true {
			var 次スレッド = scheデータ.Get次準備OKスレッド()
			if 次スレッド == nil {
				return esp
			}
			if scheデータ.現在の日時スレッド == nil {
				MEmergencyログ文字列("\nSCHED first esp=")
				MEmergencyログunsignedinteger32(esp)
				MEmergencyログ文字列(" thread=")
				MEmergencyログunsignedinteger32(uint32(uintptr(Pointer(次スレッド))))
				MEmergencyログ文字列(" cpu=")
				MEmergencyログunsignedinteger32(uint32(uintptr(Pointer(次スレッド.Cpu状態))))
				MEmergencyログ文字列(" state=")
				MEmergencyログunsignedinteger32(uint32(次スレッド.Tスレッド状態))
				MEmergencyログ文字列(" eip=")
				MEmergencyログunsignedinteger32(次スレッド.Cpu状態.Eip)
				MEmergencyログ文字列(" cs=")
				MEmergencyログunsignedinteger32(次スレッド.Cpu状態.Cs)
				MEmergencyログ文字列("\n")
			}

			if esp >= K中核heap開始 && scheデータ.現在の日時スレッド != nil {
				scheデータ.現在の日時スレッド.Cpu状態 = (*Tcpu状態)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(scheデータ.現在の日時スレッド.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				scheデータ.現在の日時スレッド.Fpuoffset = offset
				backupfpregs(address + offset)
				if スケジューラdebug {
					コンソール_2.M印刷(([]byte)("backup"))
					コンソール_2.MUnsignedinteger32印刷(esp)
				}
			}

			address := uintptr(Pointer(&(次スレッド.Fpubuffer)))
			offset := 次スレッド.Fpuoffset
			if offset != 0xffffffff {
				復元fpregs(address + offset)
				if スケジューラdebug {
					コンソール_2.M印刷(([]byte)("restore"))
				}
			}

			scheデータ.現在の日時スレッド = 次スレッド

			if scheデータ.現在の日時スレッド.Tスレッド状態 == S起動日時 {
				scheデータ.現在の日時スレッド.Tスレッド状態 = R準備OK

				Initialスレッド利用者jump(scheデータ.現在の日時スレッド)
				return esp
			}

			esp = uint32(uintptr(Pointer(次スレッド.Cpu状態)))
			if 次スレッド.Stack != 0 {
				scheデータ.tss.Sありstack(Seg中核データ, 次スレッド.Stack+Tスレッドstackサイズ)
			}

			ありcr3(次スレッド.Pページディレクトリentry)
			ありgs(次スレッド.Cpu状態.Gs)

		}

	}

	return esp
}

func jumpユーザーモードiret(uint32, uint32, uint32, uint32, uint32, uint32)
func D不可int()

func getesp() uint32
func スレッド終了loop()

func ありスレッド終了loop状態(cpu状態 *Tcpu状態) {
	cpu状態.Eip = uint32(ValueOf(スレッド終了loop).Pointer())
	cpu状態.Cs = Seg中核code
	cpu状態.Ds = Seg中核データ
	cpu状態.Es = Seg中核データ
	cpu状態.Fs = Seg中核データ
	cpu状態.Gs = Seg中核gs
	cpu状態.Ss = Seg中核データ
	cpu状態.Eflags = 0x202
}

func S停止現在の日時スレッド(cpu状態 *Tcpu状態) *Tcpu状態 {
	if scheデータ.現在の日時スレッド == nil {
		ありスレッド終了loop状態(cpu状態)
		return cpu状態
	}

	停止スレッド := scheデータ.現在の日時スレッド
	for i := 0; i < 一覧.Sサイズ_2; i++ {
		スレッド := (*Tスレッド)(一覧.Getat(i))
		if スレッド != nil && スレッド.Cpu状態 == cpu状態 {
			停止スレッド = スレッド
			break
		}
	}
	停止スレッド.Cpu状態 = cpu状態
	停止スレッド.Tスレッド状態 = S停止
	scheデータ.現在の日時スレッド = 停止スレッド

	次スレッド := scheデータ.Get次準備OKスレッド()
	if 次スレッド == nil || 次スレッド == 停止スレッド || 次スレッド.Cpu状態 == nil || 次スレッド.Cpu状態 == cpu状態 {
		ありスレッド終了loop状態(cpu状態)
		return cpu状態
	}

	scheデータ.現在の日時スレッド = 次スレッド
	if 次スレッド.Stack != 0 && scheデータ.tss != nil {
		scheデータ.tss.Sありstack(Seg中核データ, 次スレッド.Stack+Tスレッドstackサイズ)
	}
	ありcr3(次スレッド.Pページディレクトリentry)
	ありgs(次スレッド.Cpu状態.Gs)
	return 次スレッド.Cpu状態
}

func Initialスレッド利用者jump(スレッド *Tスレッド) {

	D不可int()

	scheデータ.tss.Sありstack(Seg中核データ, スレッド.Stack+Tスレッドstackサイズ)

	ありcr3(スレッド.Pページディレクトリentry)
	ありgs(スレッド.Cpu状態.Gs)

	scheデータ.現在の日時スレッド = スレッド
	scheデータ.E有効 = true

	eip := スレッド.Cpu状態.Eip
	利用者esp := スレッド.U利用者stack_2 + スレッド.U利用者stackサイズ_2
	eflags := スレッド.Cpu状態.Eflags
	cs := スレッド.Cpu状態.Cs
	esp := scheデータ.tss.Getesp0()

	コンソール_2.M印刷(([]byte)("jump["))
	コンソール_2.MUnsignedinteger32印刷(eip)
	コンソール_2.M印刷(([]byte)(":"))
	コンソール_2.MUnsignedinteger32印刷(利用者esp)
	コンソール_2.M印刷(([]byte)(":"))
	コンソール_2.MUnsignedinteger32印刷(eflags)
	コンソール_2.M印刷(([]byte)(":"))
	コンソール_2.MUnsignedinteger32印刷(cs)
	コンソール_2.M印刷(([]byte)(":"))

	コンソール_2.MUnsignedinteger32印刷(esp)
	コンソール_2.M印刷(([]byte)("]"))

	userprocentry := スレッド.Cpu状態.Ecx
	全般offsettable_2 := スレッド.Cpu状態.Edx
	動的に := スレッド.Cpu状態.Esi

	Pポート書込みバイト(0x20, 0x20)
	jumpユーザーモードiret(eip, 利用者esp, eflags, userprocentry, 全般offsettable_2, 動的に)
	コンソール_2.M印刷(([]byte)("usermode end"))
}
func 印刷esp(esp uint32) {
	コンソール_2.M印刷(([]byte)("esp["))
	コンソール_2.MUnsignedinteger32印刷(esp)
}
