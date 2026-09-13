package 程序

import . "unsafe"
import . "工具/清單"
import mem "記憶體管理器"
import . "工作管理/執行緒"
import . "工作管理/排程器"
import . "工具"

const Proc使用者heap大小 = 1 * 1024 * 1024

type P程序 struct {
	識別號		uint32
	syscall識別號	int
	Is使用者空白		bool
	參數		*[]byte

	T執行緒清單	Linked清單
	Threads	*Linked清單
	F檔案名稱	[]byte

	P頁目錄項目	uintptr
}

func (self *P程序) Init(mem *mem.T記憶體管理器) {
	self.T執行緒清單 = Linked清單{}
	self.Threads = &self.T執行緒清單
	self.Threads.Init(mem)
}

type P程序helper struct {
	程序_2	Linked清單
	mem	*mem.T記憶體管理器
	核心頁目錄項目	uintptr
}

func (self *P程序helper) Init(mem *mem.T記憶體管理器, 核心頁目錄項目 uintptr) {
	self.mem = mem
	self.程序_2 = Linked清單{}
	self.程序_2.Init(self.mem)
	self.核心頁目錄項目 = 核心頁目錄項目
}

func (self *P程序helper) C建立(項目point func(), 執行緒helper *T執行緒helper, P頁目錄項目 uint32, is核心 bool) P程序 {
	程序 := (*P程序)(self.mem.M配置記憶體(uint32(Sizeof(P程序{}))))
	if 程序 == nil {
		return P程序{}
	}
	程序.Init(self.mem)
	程序.識別號 = Allocate行程代碼()
	程序.P頁目錄項目 = uintptr(P頁目錄項目)
	主要執行緒 := 執行緒helper.C建立指標from函式(項目point, P頁目錄項目, is核心)
	if 主要執行緒 != nil {
		主要執行緒.P行程代碼 = 程序.識別號
		主要執行緒.Parent行程代碼 = 0
		程序.Threads.M附加至串列尾端(uintptr(Pointer(主要執行緒)))
	}

	self.程序_2.M附加至串列尾端(uintptr(Pointer(程序)))

	return *程序
}

func (self *P程序helper) Spawn(項目point func(), 執行緒helper *T執行緒helper, 排程器 *S排程器, P頁目錄項目 uint32, is核心 bool) P程序 {
	程序 := self.C建立(項目point, 執行緒helper, P頁目錄項目, is核心)
	if 程序.Threads != nil && 程序.Threads.S大小_2 > 0 {
		執行緒 := (*T執行緒)(程序.Threads.Getat(0))
		if 執行緒 != nil && 排程器 != nil {
			排程器.A加入執行緒(執行緒)
		}
	}
	return 程序
}

func (self *P程序helper) 複製頁目錄(來源項目 uintptr, 目的地項目 uintptr) {
	來源_2 := Getunsignedinteger32陣列from指標(來源項目, 1024, 1024)
	目的地_2 := Getunsignedinteger32陣列from指標(目的地項目, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		目的地_2[i] = 來源_2[i]
	}
}
func (self *P程序helper) C建立from資料() P程序 {
	程序 := P程序{}
	return 程序
}
