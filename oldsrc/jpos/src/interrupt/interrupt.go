/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/
package Interrupt

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "taskmanager"
import . "console"

///////////////////////////////////////////////////////////////////////////////
//
// 	割り込み = 割り込み = Interrupt
//
///////////////////////////////////////////////////////////////////////////////
func 割り込み_無視する()

func 割り込み_例外処理()
func 割り込み_例外処理0x00()
func 割り込み_例外処理0x01()
func 割り込み_例外処理0x02()
func 割り込み_例外処理0x03()
func 割り込み_例外処理0x04()
func 割り込み_例外処理0x05()
func 割り込み_例外処理0x06()
func 割り込み_例外処理0x07()
func 割り込み_例外処理0x08()
func 割り込み_例外処理0x09()
func 割り込み_例外処理0x0A()
func 割り込み_例外処理0x0B()
func 割り込み_例外処理0x0C()
func 割り込み_例外処理0x0D()
func 割り込み_例外処理0x0E()
func 割り込み_例外処理0x0F()

func 割り込み_要請処理0x00()
func 割り込み_要請処理0x01()
func 割り込み_要請処理0x02()
func 割り込み_要請処理0x03()
func 割り込み_要請処理0x04()
func 割り込み_要請処理0x05()
func 割り込み_要請処理0x06()
func 割り込み_要請処理0x07()
func 割り込み_要請処理0x08()
func 割り込み_要請処理0x09()
func 割り込み_要請処理0x0A()
func 割り込み_要請処理0x0B()
func 割り込み_要請処理0x0C()
func 割り込み_要請処理0x0D()
func 割り込み_要請処理0x0E()
func 割り込み_要請処理0x0F()


///////////////////////////////////////////////////////////////////////////////
//
//	割り込み_處理器 = InteruptHandler, 割り込み番号 = interruptnumber
//
///////////////////////////////////////////////////////////////////////////////
type T割り込み_處理器 struct{
	割り込み番号 uint8
	割り込み_管理者 uintptr 
}
var 多数處理器 [256] uintptr  // handler

func (自身 *T割り込み_處理器) M初期化(割り込み番号 uint8, 割り込み_管理者 uintptr, 関数アドレス uintptr){

	多数處理器[割り込み番号] = 関数アドレス

	自身.割り込み番号 = 割り込み番号 
	自身.割り込み_管理者 = 割り込み_管理者

}
func (自身 *T割り込み_處理器) SetHandleInterruptFuction(アドレス uintptr){
	多数處理器[自身.割り込み番号] = アドレス 
}
func (自身 *T割り込み_處理器) M消滅する(){
	自身정수アドレス := uintptr(Pointer(自身))
	割り込み_管理者 := (*T割り込み_管理者)(Pointer(自身.割り込み_管理者))
	if 自身정수アドレス == 割り込み_管理者.M處理器_갖기(自身.割り込み番号) {
		割り込み_管理者.M處理器_設定(0, 自身.割り込み番号)
	}

}
func (自身 *T割り込み_處理器) 割り込み_管理者設定(割り込み_管理者 uintptr){
}
func (自身 *T割り込み_處理器) 割り込み_管理者番号設定(割り込み番号 uint8){
	自身.割り込み番号 = 割り込み番号
}
///////////////////////////////////////////////////////////////////////////////
type TGateDescriptor struct{
	gateData [8] uint8

	// handlerAddrressLowBits uint16 -- 
	// gdt_codeSegmentSelector uint16 --
	// reserved uint8 // 
	// access uint8   // 
	// handlerAddressHightBits uint16 -- 
}
var 割り込み記述子表_データ [256*8] uint8
var 活性割り込み_管理者 uintptr = 0

///////////////////////////////////////////////////////////////////////////////
//
//		割り込み_管理者 = InterruptManager
//
///////////////////////////////////////////////////////////////////////////////
type T割り込み_管理者 struct {
	多数處理器 [256] uintptr
	ハードウェア割り込み位置 uint16
	作業管理者 *T作業管理者

	// PIC = Programable Interrupt Controller = 設定可能な割り込みコントローラ
	マスター_PIC_命令語_入出力ポート Tバイト入出力ポート // pic master command port
	マスター_PIC_データ_入出力ポート Tバイト入出力ポート // pic master data port
	スレイブ_PIC_命令語_入出力ポート Tバイト入出力ポート // pic slave command port
	スレイブ_PIC_データ_入出力ポート Tバイト入出力ポート // pic slave datga port

}

func (自身 *T割り込み_管理者) M初期化(ハードウェア割り込み位置 uint16, 大域記述子表 *T大域記述子表, 作業管理者 *T作業管理者){
	
	自身.作業管理者 = 作業管理者
	自身.ハードウェア割り込み位置 = ハードウェア割り込み位置	

	符号の分節 := 大域記述子表.M符号の分節を選択()


	for i:=0; i<(256*8); i++{
		割り込み記述子表_データ[i] = 0
	}
	var アドレス uint32
	var IDT_INTERRUPT_GATE uint8 = 0xE // 割り込み 32bit

	アドレス = uint32(ValueOf(割り込み_無視する).Pointer())
	for i:=0; i<256; i++ {
		多数處理器[i] = 0
		アドレス = uint32(ValueOf(割り込み_例外処理0x0F).Pointer())
		自身.割り込み記述子表項目を設定(i, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 
	} 

	アドレス = uint32(ValueOf(割り込み_例外処理0x00).Pointer())
	自身.割り込み記述子表項目を設定(0x00, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x01).Pointer())
	自身.割り込み記述子表項目を設定(0x01, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 
	アドレス = uint32(ValueOf(割り込み_例外処理0x02).Pointer())
	自身.割り込み記述子表項目を設定(0x02, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x03).Pointer())
	自身.割り込み記述子表項目を設定(0x03, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x04).Pointer())
	自身.割り込み記述子表項目を設定(0x04, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x05).Pointer())
	自身.割り込み記述子表項目を設定(0x05, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x06).Pointer())
	自身.割り込み記述子表項目を設定(0x06, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x07).Pointer())
	自身.割り込み記述子表項目を設定(0x07, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x08).Pointer())
	自身.割り込み記述子表項目を設定(0x08, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x09).Pointer())
	自身.割り込み記述子表項目を設定(0x09, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x0A).Pointer())
	自身.割り込み記述子表項目を設定(0x0A, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x0B).Pointer())
	自身.割り込み記述子表項目を設定(0x0B, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 
	アドレス = uint32(ValueOf(割り込み_例外処理0x0C).Pointer())
	自身.割り込み記述子表項目を設定(0x0C, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 
	アドレス = uint32(ValueOf(割り込み_例外処理0x0D).Pointer())
	自身.割り込み記述子表項目を設定(0x0D, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x0E).Pointer())
	自身.割り込み記述子表項目を設定(0x0E, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_例外処理0x0F).Pointer())
	自身.割り込み記述子表項目を設定(0x0F, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 
	///////////////////////////////////////////////////////////////////////////

	アドレス = uint32(ValueOf(割り込み_要請処理0x00).Pointer())
	自身.割り込み記述子表項目を設定(0x20, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	
	アドレス = uint32(ValueOf(割り込み_要請処理0x01).Pointer())
	自身.割り込み記述子表項目を設定(0x21, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 
	アドレス = uint32(ValueOf(割り込み_要請処理0x02).Pointer())
	自身.割り込み記述子表項目を設定(0x22, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x03).Pointer())
	自身.割り込み記述子表項目を設定(0x23, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x04).Pointer())
	自身.割り込み記述子表項目を設定(0x24, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x05).Pointer())
	自身.割り込み記述子表項目を設定(0x25, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x06).Pointer())
	自身.割り込み記述子表項目を設定(0x26, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x07).Pointer())
	自身.割り込み記述子表項目を設定(0x27, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x08).Pointer())
	自身.割り込み記述子表項目を設定(0x28, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x09).Pointer())
	自身.割り込み記述子表項目を設定(0x29, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x0A).Pointer())
	自身.割り込み記述子表項目を設定(0x2A, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x0B).Pointer())
	自身.割り込み記述子表項目を設定(0x2B, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 
	アドレス = uint32(ValueOf(割り込み_要請処理0x0C).Pointer())
	自身.割り込み記述子表項目を設定(0x2C, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 
	アドレス = uint32(ValueOf(割り込み_要請処理0x0D).Pointer())
	自身.割り込み記述子表項目を設定(0x2D, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x0E).Pointer())
	自身.割り込み記述子表項目を設定(0x2E, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 

	アドレス = uint32(ValueOf(割り込み_要請処理0x0F).Pointer())
	自身.割り込み記述子表項目を設定(0x2F, 符号の分節, アドレス, 0, IDT_INTERRUPT_GATE) 


	自身.マスター_PIC_命令語_入出力ポート = Tバイト入出力ポート{}
	自身.マスター_PIC_データ_入出力ポート = Tバイト入出力ポート{}
	
	自身.スレイブ_PIC_命令語_入出力ポート = Tバイト入出力ポート{}
	自身.スレイブ_PIC_データ_入出力ポート = Tバイト入出力ポート{}	

	自身.マスター_PIC_命令語_入出力ポート.M初期化(0x20)
	自身.マスター_PIC_データ_入出力ポート.M初期化(0x21)

	自身.スレイブ_PIC_命令語_入出力ポート.M初期化(0xA0)
	自身.スレイブ_PIC_データ_入出力ポート.M初期化(0xA1)

	自身.マスター_PIC_命令語_入出力ポート.M作成(0x11)
	自身.スレイブ_PIC_命令語_入出力ポート.M作成(0x11)

	自身.マスター_PIC_データ_入出力ポート.M作成(0x20)
	自身.スレイブ_PIC_データ_入出力ポート.M作成(0x28)

	自身.マスター_PIC_データ_入出力ポート.M作成(0x04)
	自身.スレイブ_PIC_データ_入出力ポート.M作成(0x02)

	自身.マスター_PIC_データ_入出力ポート.M作成(0x01)
	自身.スレイブ_PIC_データ_入出力ポート.M作成(0x01)

	自身.マスター_PIC_データ_入出力ポート.M作成(0x00) // all master pic
	自身.スレイブ_PIC_データ_入出力ポート.M作成(0x00) // all slave pic


	割り込み記述子表_アドレス := [6]uint8{0, 0, 0, 0, 0, 0}
	大きさ := (*uint16)(Pointer(&割り込み記述子表_アドレス[0]))
	(*大きさ) = (uint16)(Sizeof(割り込み記述子表_データ) -1)
	
	基準 := (*uint32)(Pointer(&割り込み記述子表_アドレス[2]))
	(*基準) = uint32(uintptr(Pointer(&割り込み記述子表_データ)))
	
	割り込み記述子表を搭載(uintptr(Pointer(&割り込み記述子表_アドレス)))
}
func 割り込み記述子表を搭載(割り込み記述子表_アドレス uintptr)

func (自身 *T割り込み_管理者) 割り込み記述子表項目を設定(割り込み int, 
							符号の分節 uint16,
							處理器 uint32,
							記述子の特権段階 uint8,
							記述子類型 uint8){ 

	處理器アドレスlo := (*uint16)(Pointer(&割り込み記述子表_データ[割り込み*8+0]))
	(*處理器アドレスlo) = uint16(處理器 & 0xFFFF)

	gdt_codeSegmentSelector := (*uint16)(Pointer(&割り込み記述子表_データ[割り込み*8+2]))
	(*gdt_codeSegmentSelector) = 符号の分節

	予約 := (*uint8)(Pointer(&割り込み記述子表_データ[割り込み*8+4]))
	(*予約) = 0

	var IDT_DESC_PRESENT uint8 = 0x80
	アクセス権限 := (*uint8)(Pointer(&割り込み記述子表_データ[割り込み*8+5]))
	(*アクセス権限) = (IDT_DESC_PRESENT | 記述子類型 | ((記述子の特権段階 & 3) << 5)) 

	處理器アドレスhi := (*uint16)(Pointer(&割り込み記述子表_データ[割り込み*8+6]))
	(*處理器アドレスhi) = uint16((處理器 >> 16) & 0xFFFF)

}

func (自身 *T割り込み_管理者) M處理器_設定(處理器 uintptr, 割り込み番号 uint8){	// set handler
	多数處理器[割り込み番号] = 處理器
}
func (自身 *T割り込み_管理者) M處理器_갖기(割り込み番号 uint8) uintptr{		// get handler
	return 多数處理器[割り込み番号]
}


func (自身 *T割り込み_管理者) 割り込み_処理する(割り込み uint8, esp uint32) uint32{		// handle interrupt
	端末機 := T端末機{}
	端末機.M出力(esp, 2, 14)

	if 多数處理器[割り込み] != 0 {

		ユーザ関数 := (*(*func())(Pointer(多数處理器[割り込み])))
		ユーザ関数()

	} else if 割り込み != 0x20 { // ?? 
		if 割り込み >= 0x21 {
		}
		
	}
	if 割り込み == uint8(自身.ハードウェア割り込み位置) {
		esp = uint32(uintptr(Pointer(自身.作業管理者.M作業日程((*T中央処理装置の状態)(Pointer(uintptr(esp)))))))
	}
	if 割り込み <= 0x1F{
	}	
	if 0x20 <= 割り込み && 割り込み < 0x30 {
		自身.マスター_PIC_命令語_入出力ポート.M作成(0x20)
		if 0x28 <= 割り込み {
			自身.スレイブ_PIC_命令語_入出力ポート.M作成(0x20)
		}
	}
	return esp
}
func 割り込み処理(esp uint32, 割り込み uint8) uint32{

	if 活性割り込み_管理者 != 0 {
		割り込み_管理者 := (*T割り込み_管理者)(Pointer(活性割り込み_管理者))
		return 割り込み_管理者.割り込み_処理する(割り込み, esp)
	}

	return esp
}
var 例外番号 uint8
func 例外処理(esp uint32, 割り込み uint8) uint32{
	hex := []byte("0123456789ABCDEF");
        臨時 := []byte("\n           HandleException :   ")
	臨時[29] = 例外番号
	臨時[31] = hex[割り込み & 0x0F]
	臨時[30] = hex[(割り込み & 0xF0)>>2]
	例外番号++

        端末機 := new(T端末機)
	端末機.M出力(臨時)
	端末機.M出力("esp[")
	端末機.M出力(esp)
	端末機.M出力(":")
	端末機.M出力(割り込み)
	端末機.M出力("]")

	return esp
}

func 割り込み活性化()
func (自身 *T割り込み_管理者) M活性化(){
	if 活性割り込み_管理者 != 0 {
		自身.M非活性化()
	}
	アドレス := uintptr(Pointer(自身))
	活性割り込み_管理者 = アドレス
	割り込み活性化()
}

func 割り込み非活性化()
func (自身 *T割り込み_管理者) M非活性化(){
	活性割り込み_管理者 = 0
	割り込み非活性化()
}

