package T執行緒_2

import . "unsafe"
import . "reflect"
import . "gdt"
import . "控制台"
import . "多重工作管理"
import mem "記憶體管理器"
import . "虛擬記憶體"

const (
	Blocked	= 1
	R準備就緒	= 2
	S已停止	= 3
	S已開始	= 4
)

const T執行緒stack大小 = 32 * 1024

type T執行緒 struct {
	Cpu狀態		*Tcpu狀態
	Stack		uint32
	U使用者stack_2	uint32
	U使用者stack大小_2	uint32
	P行程代碼		uint32
	Parent行程代碼	uint32

	P頁目錄項目	uint32

	T執行緒狀態		uint8
	Blocked狀態	uint8

	時間德爾塔	uint32

	Tls線條		[Gdt項目]TSegmentdescriptor
	Fpu位移		uintptr
	Fpubuffer	[512 + 16]byte
	Is核心		bool
}

func (self *T執行緒) N新增() {
}

type T執行緒helper struct {
	mem *mem.T記憶體管理器
}

var 控制台_2 = T控制台{}

func (self *T執行緒helper) Init(mem *mem.T記憶體管理器) {
	self.mem = mem
	控制台_2.M列印xy(([]byte)("thread:"), 1, 14)
}
func (self *T執行緒helper) C建立from函式(項目point_2 func(), P頁目錄項目 uint32, is核心 bool) T執行緒 {
	結果 := T執行緒{}

	結果.Stack = uint32(uintptr(self.mem.M配置記憶體(T執行緒stack大小)))
	if 結果.Stack == 0 {
		return 結果
	}
	控制台_2.M列印(([]byte)("[mem:"))
	控制台_2.MUnsignedinteger32列印(結果.Stack)

	結果.Cpu狀態 = (*Tcpu狀態)(Pointer(uintptr(結果.Stack) + T執行緒stack大小 - Sizeof(Tcpu狀態{})))
	結果.Cpu狀態.Esp = 結果.Stack + T執行緒stack大小
	結果.Cpu狀態.Ebp = 結果.Cpu狀態.Esp
	結果.Cpu狀態.Eip = uint32(ValueOf(項目point_2).Pointer())
	結果.U使用者stack_2 = U使用者stack
	結果.U使用者stack大小_2 = U使用者stack大小
	結果.P行程代碼 = 0
	結果.Parent行程代碼 = 0
	結果.P頁目錄項目 = P頁目錄項目
	控制台_2.M列印((([]byte)("cpu")))

	控制台_2.MUnsignedinteger32列印(uint32(uintptr(Pointer(結果.Cpu狀態))))

	控制台_2.M列印((([]byte)(":")))
	控制台_2.MUnsignedinteger32列印(結果.Cpu狀態.Eip)

	控制台_2.M列印("]")
	if is核心 == true {
		結果.Cpu狀態.Cs = Seg核心code
		結果.Cpu狀態.Ds = Seg核心資料
		結果.Cpu狀態.Es = Seg核心資料
		結果.Cpu狀態.Fs = Seg核心資料
		結果.Cpu狀態.Gs = Seg核心gs
		結果.Cpu狀態.Ss = Seg核心資料
		結果.T執行緒狀態 = R準備就緒
		結果.Cpu狀態.Eflags = 0x202
	} else {
		結果.Cpu狀態.Cs = Seg使用者code
		結果.Cpu狀態.Ds = Seg使用者資料
		結果.Cpu狀態.Es = Seg使用者資料
		結果.Cpu狀態.Fs = Seg使用者資料
		結果.Cpu狀態.Gs = Seg使用者gs
		結果.Cpu狀態.Ss = Seg使用者資料
		結果.T執行緒狀態 = S已開始
		結果.Cpu狀態.Eflags = 0x222
	}
	結果.Is核心 = is核心
	結果.Fpu位移 = 0xffffffff

	return 結果
}

func (self *T執行緒helper) C建立指標from函式(項目point_2 func(), P頁目錄項目 uint32, is核心 bool) *T執行緒 {
	結果 := (*T執行緒)(self.mem.M配置記憶體(uint32(Sizeof(T執行緒{}))))
	if 結果 == nil {
		return nil
	}
	*結果 = self.C建立from函式(項目point_2, P頁目錄項目, is核心)
	if 結果.Cpu狀態 == nil {
		self.mem.F剩餘(Pointer(結果))
		return nil
	}
	return 結果
}
