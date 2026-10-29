/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 排程器

import . "unsafe"
import . "reflect"

import . "控制台"
import . "gdt"
import . "連接埠"
import . "工具/清單"

import . "中斷"
import . "工作管理/執行緒"
import . "工作管理/tss"
import . "多重工作管理"
import mem "記憶體管理器"

const S排程器頻率 = 1
const K核心heap啟動 = 1024 * 1024
const 排程器除錯 = false
const pit頻率 = 100

var 清單 Linked清單

type S排程器資料 struct {
	頻率	uint32
	tick計數	uint32

	switchforced	bool

	E已啟用	bool

	目前執行緒	*T執行緒
	tss	*Tss項目
}

var sche資料 S排程器資料 = S排程器資料{}

func (self *S排程器資料) Init() {
	sche資料.tick計數 = 0
	sche資料.頻率 = S排程器頻率
	sche資料.目前執行緒 = nil
	sche資料.E已啟用 = false
	sche資料.switchforced = false

}

var 控制台_2 = T控制台{}
var 目前執行緒索引 int = 0
var 下一個程序識別號 uint32 = 1

func Allocate行程代碼() uint32 {
	行程代碼 := 下一個程序識別號
	下一個程序識別號++
	return 行程代碼
}

func (self *S排程器資料) Get下一個準備就緒執行緒() *T執行緒 {
	if 清單.S大小_2 <= 0 {
		return nil
	}

	if sche資料.目前執行緒 != nil {
		目前執行緒索引 = 清單.I索引of(uintptr(Pointer(sche資料.目前執行緒)))
		if 目前執行緒索引 < 0 {
			目前執行緒索引 = 0
		}
	} else {
		目前執行緒索引 = -1
	}

	for checked := 0; checked < 清單.S大小_2; checked++ {
		目前執行緒索引++
		if 目前執行緒索引 >= 清單.S大小_2 {
			目前執行緒索引 = 0
		}
		執行緒 := (*T執行緒)(清單.Getat(目前執行緒索引))
		if 執行緒 != nil && 執行緒.T執行緒狀態 != Blocked && 執行緒.T執行緒狀態 != S已停止 {
			if 排程器除錯 {
				控制台_2.M列印("ti:")
				控制台_2.MUnsignedinteger32列印(uint32(目前執行緒索引))
				控制台_2.M列印(":")
				控制台_2.MUnsignedinteger32列印(uint32(uintptr(Pointer(執行緒))))
			}
			return 執行緒
		}
	}
	return sche資料.目前執行緒

}
func (self *S排程器) A加入執行緒(執行緒 *T執行緒) {
	if 執行緒 == nil {
		return
	}
	清單.M附加至串列尾端(uintptr(Pointer(執行緒)))
}
func A加入runnable執行緒(執行緒 *T執行緒) {
	if 執行緒 == nil {
		return
	}
	清單.M附加至串列尾端(uintptr(Pointer(執行緒)))
}

func C目前行程代碼() uint32 {
	if sche資料.目前執行緒 == nil || sche資料.目前執行緒.P行程代碼 == 0 {
		return 1
	}
	return sche資料.目前執行緒.P行程代碼
}

func C目前parent行程代碼() uint32 {
	if sche資料.目前執行緒 == nil {
		return 0
	}
	return sche資料.目前執行緒.Parent行程代碼
}
func (self *S排程器) R移除執行緒(執行緒 *T執行緒) {
	清單.R移除(uintptr(Pointer(執行緒)))
}

func (self *S排程器) R移除執行緒at(索引 int) {
	清單.R移除at(索引)
}

type S排程器 struct {
	T中斷handler
}

func (self *S排程器) Init(管理器 *T中斷管理器, mem *mem.T記憶體管理器, tss *Tss項目) {
	sche資料.Init()
	sche資料.tss = tss
	initpit(pit頻率)

	清單 = Linked清單{}
	清單.Init(mem)
	控制台_2.M列印("list:")
	控制台_2.MUnsignedinteger32列印(uint32(uintptr(Pointer(&清單))))

	中斷handler = 控制把中斷
	var address uintptr
	address = uintptr(Pointer(&中斷handler))
	self.T中斷handler.Init(0x20, uintptr(Pointer(管理器)), address)
}

func (self *S排程器) E已啟用(已啟用 bool) {
	sche資料.E已啟用 = 已啟用
}

func initpit(頻率 uint32) {
	if 頻率 == 0 {
		return
	}
	divisor := uint32(1193180) / 頻率
	P連接埠寫入位元組(0x43, 0x36)
	P連接埠寫入位元組(0x40, uint8(divisor&0xFF))
	P連接埠寫入位元組(0x40, uint8((divisor>>8)&0xFF))
}

func 設定ds(dssegment uint32)
func 設定gs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func 還原fpregs(buffer_2 uintptr)

var jmp使用者 uint32 = 0
var 中斷handler func(uint32) uint32

func schedulestack(fn func())
func 設定cr3(address uint32)
func getcr3() uint32

func 控制把中斷(esp uint32) uint32 {

	sche資料.tick計數++

	if 排程器除錯 {
		控制台_2.M列印xy(([]byte)("sche1:"), 1, 17)

		控制台_2.M列印(":")
		控制台_2.MUnsignedinteger32列印(esp)
		控制台_2.M列印(":")

		控制台_2.MUnsignedinteger32列印(uint32(sche資料.tick計數))
		控制台_2.M列印(":")
		控制台_2.MUnsignedinteger32列印(K核心heap啟動)
	}

	if sche資料.tick計數 == sche資料.頻率 {
		sche資料.tick計數 = 0

		if 清單.S大小_2 > 0 && sche資料.E已啟用 == true {
			var 下一個執行緒 = sche資料.Get下一個準備就緒執行緒()
			if 下一個執行緒 == nil {
				return esp
			}
			if sche資料.目前執行緒 == nil {
				MEmergency記錄字串("\nSCHED first esp=")
				MEmergency記錄unsignedinteger32(esp)
				MEmergency記錄字串(" thread=")
				MEmergency記錄unsignedinteger32(uint32(uintptr(Pointer(下一個執行緒))))
				MEmergency記錄字串(" cpu=")
				MEmergency記錄unsignedinteger32(uint32(uintptr(Pointer(下一個執行緒.Cpu狀態))))
				MEmergency記錄字串(" state=")
				MEmergency記錄unsignedinteger32(uint32(下一個執行緒.T執行緒狀態))
				MEmergency記錄字串(" eip=")
				MEmergency記錄unsignedinteger32(下一個執行緒.Cpu狀態.Eip)
				MEmergency記錄字串(" cs=")
				MEmergency記錄unsignedinteger32(下一個執行緒.Cpu狀態.Cs)
				MEmergency記錄字串("\n")
			}

			if esp >= K核心heap啟動 && sche資料.目前執行緒 != nil {
				sche資料.目前執行緒.Cpu狀態 = (*Tcpu狀態)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(sche資料.目前執行緒.Fpubuffer)))
				位移 := (16 - (address % 16)) & 0xF
				sche資料.目前執行緒.Fpu位移 = 位移
				backupfpregs(address + 位移)
				if 排程器除錯 {
					控制台_2.M列印(([]byte)("backup"))
					控制台_2.MUnsignedinteger32列印(esp)
				}
			}

			address := uintptr(Pointer(&(下一個執行緒.Fpubuffer)))
			位移 := 下一個執行緒.Fpu位移
			if 位移 != 0xffffffff {
				還原fpregs(address + 位移)
				if 排程器除錯 {
					控制台_2.M列印(([]byte)("restore"))
				}
			}

			sche資料.目前執行緒 = 下一個執行緒

			if sche資料.目前執行緒.T執行緒狀態 == S已開始 {
				sche資料.目前執行緒.T執行緒狀態 = R準備就緒

				Initial執行緒使用者jump(sche資料.目前執行緒)
				return esp
			}

			esp = uint32(uintptr(Pointer(下一個執行緒.Cpu狀態)))
			if 下一個執行緒.Stack != 0 {
				sche資料.tss.S設定stack(Seg核心資料, 下一個執行緒.Stack+T執行緒stack大小)
			}

			設定cr3(下一個執行緒.P頁目錄項目)
			設定gs(下一個執行緒.Cpu狀態.Gs)

		}

	}

	return esp
}

func jump使用者模式iret(uint32, uint32, uint32, uint32, uint32, uint32)
func D停用整數()

func getesp() uint32
func 執行緒離開迴圈()

func 設定執行緒離開迴圈狀態(cpu狀態 *Tcpu狀態) {
	cpu狀態.Eip = uint32(ValueOf(執行緒離開迴圈).Pointer())
	cpu狀態.Cs = Seg核心code
	cpu狀態.Ds = Seg核心資料
	cpu狀態.Es = Seg核心資料
	cpu狀態.Fs = Seg核心資料
	cpu狀態.Gs = Seg核心gs
	cpu狀態.Ss = Seg核心資料
	cpu狀態.Eflags = 0x202
}

func S停止目前執行緒(cpu狀態 *Tcpu狀態) *Tcpu狀態 {
	if sche資料.目前執行緒 == nil {
		設定執行緒離開迴圈狀態(cpu狀態)
		return cpu狀態
	}

	已停止執行緒 := sche資料.目前執行緒
	for i := 0; i < 清單.S大小_2; i++ {
		執行緒 := (*T執行緒)(清單.Getat(i))
		if 執行緒 != nil && 執行緒.Cpu狀態 == cpu狀態 {
			已停止執行緒 = 執行緒
			break
		}
	}
	已停止執行緒.Cpu狀態 = cpu狀態
	已停止執行緒.T執行緒狀態 = S已停止
	sche資料.目前執行緒 = 已停止執行緒

	下一個執行緒 := sche資料.Get下一個準備就緒執行緒()
	if 下一個執行緒 == nil || 下一個執行緒 == 已停止執行緒 || 下一個執行緒.Cpu狀態 == nil || 下一個執行緒.Cpu狀態 == cpu狀態 {
		設定執行緒離開迴圈狀態(cpu狀態)
		return cpu狀態
	}

	sche資料.目前執行緒 = 下一個執行緒
	if 下一個執行緒.Stack != 0 && sche資料.tss != nil {
		sche資料.tss.S設定stack(Seg核心資料, 下一個執行緒.Stack+T執行緒stack大小)
	}
	設定cr3(下一個執行緒.P頁目錄項目)
	設定gs(下一個執行緒.Cpu狀態.Gs)
	return 下一個執行緒.Cpu狀態
}

func Initial執行緒使用者jump(執行緒 *T執行緒) {

	D停用整數()

	sche資料.tss.S設定stack(Seg核心資料, 執行緒.Stack+T執行緒stack大小)

	設定cr3(執行緒.P頁目錄項目)
	設定gs(執行緒.Cpu狀態.Gs)

	sche資料.目前執行緒 = 執行緒
	sche資料.E已啟用 = true

	eip := 執行緒.Cpu狀態.Eip
	使用者esp := 執行緒.U使用者stack_2 + 執行緒.U使用者stack大小_2
	eflags := 執行緒.Cpu狀態.Eflags
	cs := 執行緒.Cpu狀態.Cs
	esp := sche資料.tss.Getesp0()

	控制台_2.M列印(([]byte)("jump["))
	控制台_2.MUnsignedinteger32列印(eip)
	控制台_2.M列印(([]byte)(":"))
	控制台_2.MUnsignedinteger32列印(使用者esp)
	控制台_2.M列印(([]byte)(":"))
	控制台_2.MUnsignedinteger32列印(eflags)
	控制台_2.M列印(([]byte)(":"))
	控制台_2.MUnsignedinteger32列印(cs)
	控制台_2.M列印(([]byte)(":"))

	控制台_2.MUnsignedinteger32列印(esp)
	控制台_2.M列印(([]byte)("]"))

	userproc項目 := 執行緒.Cpu狀態.Ecx
	全域位移table_2 := 執行緒.Cpu狀態.Edx
	動態 := 執行緒.Cpu狀態.Esi

	P連接埠寫入位元組(0x20, 0x20)
	jump使用者模式iret(eip, 使用者esp, eflags, userproc項目, 全域位移table_2, 動態)
	控制台_2.M列印(([]byte)("usermode end"))
}
func 列印esp(esp uint32) {
	控制台_2.M列印(([]byte)("esp["))
	控制台_2.MUnsignedinteger32列印(esp)
}
