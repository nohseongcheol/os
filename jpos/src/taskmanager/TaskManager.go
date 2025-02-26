package taskmanager

import . "unsafe"
import . "reflect"
import . "gdt"

type T中央処理装置の状態 struct{
	アキュムレタレジスタ uint32 			// Extended Accumulator Register (EAX)
	ベースレジスタ uint32 			// Extended Base Addreスタック領域 Register(EBX)
	カウンタレジスタ uint32 			// Extended Counter Register(ECX)
	データレジスタ uint32 			// Extended Data Register (EDX)

	ソースレジスタ uint32			// Extended Source Index(ESI)
	デスティネーションレジスタ uint32			// Extended Destination Index(EDI)
	スタックベースポインタレジスタ uint32			// Extended Base Pointer Register(ebp)

	//error uint32
	
	命令ポインタ uint32			// Extend Instruction Pointer(eip)
	コード領域 uint32					// Code Segment
	eflags uint32
	
	拡張スタック指示子 uint32
	スタック領域 uint32
}
type T作業資料 struct{
	スタック [4096] uint8
	中央処理装置の状態 *T中央処理装置の状態
}
var 作業資料 T作業資料

type T作業 struct{
	スタック [4096] uint8
	中央処理装置の状態 *T中央処理装置の状態
}
var スタック [256][4096] uint8
var 中央処理装置の状態 *T中央処理装置の状態
var ジョブ番号 uint8=0

func (自身 *T作業) M初期化(gdt *T大域記述子表, 進入点 func()){
	
	自身.中央処理装置の状態 = (*T中央処理装置の状態)(Pointer(uintptr(Pointer(&スタック[ジョブ番号])) + 4096 - Sizeof(T中央処理装置の状態{})))
	//自身.中央処理装置の状態 = (*T中央処理装置の状態)(Pointer(&スタック[int(ジョブ番号) + 4096 - int(Sizeof(T中央処理装置の状態{}))]))
	ジョブ番号++

	自身.中央処理装置の状態.アキュムレタレジスタ = 0
	自身.中央処理装置の状態.ベースレジスタ = 0
	自身.中央処理装置の状態.カウンタレジスタ = 0
	自身.中央処理装置の状態.データレジスタ = 0


	自身.中央処理装置の状態.ソースレジスタ = 0
	自身.中央処理装置の状態.デスティネーションレジスタ = 0
	自身.中央処理装置の状態.スタックベースポインタレジスタ = 0

	自身.中央処理装置の状態.命令ポインタ = uint32(ValueOf(進入点).Pointer())
	自身.中央処理装置の状態.コード領域 = uint32(gdt.M符号の分節を選択())
	自身.中央処理装置の状態.eflags = 0x202

	自身.中央処理装置の状態.拡張スタック指示子 = 0
	自身.中央処理装置の状態.スタック領域 = 0

}
type T作業管理者 struct{
}
var 作業たち [256] T作業
var 作業本数 int
var 現在作業 int
func (自身 * T作業管理者) M初期化() {
	作業本数 = 0
	現在作業 = -1 
}

func (自身 *T作業管理者) M作業追加(作業 T作業) bool {
	if(作業本数 >= 255){
		return false
	}
	作業たち[作業本数] = 作業
	作業本数++
	return true
}
func (自身 *T作業管理者) M作業日程(中央処理装置の状態 *T中央処理装置の状態) *T中央処理装置の状態{

	if 作業本数 <= 0 {
		return 中央処理装置の状態
	}
	
	if 現在作業 >= 0 {
		作業たち[現在作業].中央処理装置の状態 = 中央処理装置の状態
	}
	
	現在作業++
	if 現在作業 >= 作業本数 {
		現在作業 %= 作業本数
	}

	return 作業たち[現在作業].中央処理装置の状態
}
