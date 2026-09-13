package 分頁管理

import unsafe "unsafe"
import . "中斷"
import . "記憶體管理器"
import . "工具"

type P頁目錄項目_2 uintptr

const (
	P頁目前		uint32	= 0x001
	P頁writable	uint32	= 0x002
	P頁使用者		uint32	= 0x004
	P頁框架		uint32	= 0xFFFFF000
	P頁cow		uint32	= 0x200
)

func S設定位元組ataddress(x byte, address uint32)
func S設定unsignedinteger8ataddress(x uint8, address uint32)
func S設定unsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func 設定cr3(頁目錄 uint32)
func getcr3() uint32

type P分頁管理 struct {
	T中斷handler
}
type Tcow框架管理器 struct {
	mem	*T記憶體管理器
	refs	[]uint16
	框架計數	uint32
}

var (
	P頁目錄項目		uintptr
	P頁table項目	uint32
	pdelen		uint32
	virtlen		uint32
	cow框架管理器	Tcow框架管理器
)

func (self *Tcow框架管理器) Init(mem *T記憶體管理器, 框架計數 uint32) bool {
	self.mem = mem
	self.框架計數 = 框架計數
	reference位元組 := 框架計數 * uint32(unsafe.Sizeof(uint16(0)))
	reference指標 := mem.M配置記憶體(reference位元組)
	if reference指標 == nil {
		self.refs = nil
		self.框架計數 = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(reference指標)[:框架計數:框架計數]
	for i := uint32(0); i < 框架計數; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcow框架管理器) Reference(框架 uint32) uint16 {
	idx := 框架 >> 12
	if idx >= self.框架計數 || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcow框架管理器) Increment(框架 uint32) {
	idx := 框架 >> 12
	if idx >= self.框架計數 || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcow框架管理器) Decrement(框架 uint32) {
	idx := 框架 >> 12
	if idx >= self.框架計數 || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *P分頁管理) Init(頁目錄項目 uintptr, 頁table項目 uint32, 記憶體管理器 *T記憶體管理器) {

	P頁目錄項目 = 頁目錄項目
	P頁table項目 = 頁table項目

	virtlen = uint32(6)
	pdelen = uint32(32)

	cow框架管理器.Init(記憶體管理器, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			address指標, _ := 記憶體管理器.Alignedmalloc(0x1000)
			if address指標 == nil {
				return
			}
			address := uint32(uintptr(address指標))

			S設定unsignedinteger32ataddress(address|0x87, uint32(頁目錄項目)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				S設定unsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		頁目錄項目 = 頁目錄項目 + 0x1000
	}

}
func (self *P分頁管理) Shared記憶體region() {

	頁目錄項目 := P頁目錄項目
	k頁目錄項目 := P頁目錄項目

	for i := uint32(1); i <= virtlen; i++ {

		頁目錄項目 = 頁目錄項目 + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Get數值(uint32(k頁目錄項目) + pde*4)
			v = (v & 0xFFFFF000)
			S設定unsignedinteger32ataddress(v|0x87, uint32(頁目錄項目)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Get數值(uint32(k頁目錄項目) + pde*4)
			v = (v & 0xFFFFF000)
			S設定unsignedinteger32ataddress(v|0x87, uint32(頁目錄項目)+pde*4)

		}

	}
}
func (self *P分頁管理) P頁故障(管理器 *T中斷管理器) {
	中斷handler = 控制把分頁管理中斷

	var address uintptr
	address = uintptr(unsafe.Pointer(&中斷handler))
	self.T中斷handler.Init(0xE, uintptr(unsafe.Pointer(管理器)), address)
}

var 中斷handler func(uint32) uint32

func 控制把分頁管理中斷(esp uint32) uint32 {
	if R解決複製時寫入故障() {
		return esp
	}
	return H控制把fatal中斷框架(esp, 0x0E)
}

func Cloneaddress空白cow(來源頁目錄 uint32) uint32 {
	if A啟用記憶體管理器 == nil || 來源頁目錄 == 0 {
		return 0
	}
	目的地指標, _ := A啟用記憶體管理器.Alignedmalloc(0x1000)
	if 目的地指標 == nil {
		return 0
	}
	目的地頁目錄 := uint32(uintptr(目的地指標))
	for i := uint32(0); i < 1024; i++ {
		S設定unsignedinteger32ataddress(0, 目的地頁目錄+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		來源pdeaddress := 來源頁目錄 + pde*4
		來源pde := Get數值(來源pdeaddress)
		if (來源pde & P頁目前) == 0 {
			continue
		}
		if issharedpde(pde) {
			S設定unsignedinteger32ataddress(來源pde, 目的地頁目錄+pde*4)
			continue
		}

		目的地pt指標, _ := A啟用記憶體管理器.Alignedmalloc(0x1000)
		if 目的地pt指標 == nil {
			continue
		}
		來源pt := 來源pde & P頁框架
		目的地pt := uint32(uintptr(目的地pt指標))
		S設定unsignedinteger32ataddress((目的地pt | (來源pde & 0xFFF)), 目的地頁目錄+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := 來源pt + pte*4
			項目 := Get數值(pteaddress)
			if (項目 & P頁目前) != 0 {
				if (項目 & P頁writable) != 0 {
					項目 = (項目 &^ P頁writable) | P頁cow
					S設定unsignedinteger32ataddress(項目, pteaddress)
					cow框架管理器.Increment(項目 & P頁框架)
				} else if (項目 & P頁cow) != 0 {
					cow框架管理器.Increment(項目 & P頁框架)
				}
			}
			S設定unsignedinteger32ataddress(項目, 目的地pt+pte*4)
		}
	}
	重新載入cr3()
	return 目的地頁目錄
}

func R解決複製時寫入故障() bool {
	if A啟用記憶體管理器 == nil {
		return false
	}
	故障address := getcr2()
	頁目錄 := getcr3()
	pdeaddress := 頁目錄 + ((故障address>>22)&0x3FF)*4
	pde := Get數值(pdeaddress)
	if (pde & P頁目前) == 0 {
		return false
	}
	pt := pde & P頁框架
	pteaddress := pt + ((故障address>>12)&0x3FF)*4
	pte := Get數值(pteaddress)
	if (pte&P頁cow) == 0 || (pte&P頁目前) == 0 {
		return false
	}
	old框架 := pte & P頁框架
	if cow框架管理器.Reference(old框架) <= 1 {
		S設定unsignedinteger32ataddress((pte|P頁writable)&^P頁cow, pteaddress)
		重新載入cr3()
		return true
	}

	新增指標, _ := A啟用記憶體管理器.Alignedmalloc(0x1000)
	if 新增指標 == nil {
		return false
	}
	新增框架 := uint32(uintptr(新增指標)) & P頁框架

	來源_2 := Get位元組from指標(uintptr(故障address&P頁框架), 0x1000, 0x1000)
	目的地_2 := Get位元組from指標(uintptr(新增框架), 0x1000, 0x1000)
	copy(目的地_2, 來源_2)
	cow框架管理器.Decrement(old框架)
	S設定unsignedinteger32ataddress((新增框架|(pte&0xFFF)|P頁writable)&^P頁cow, pteaddress)
	重新載入cr3()
	return true
}

func issharedpde(pde uint32) bool {
	if pde < 12 {
		return true
	}
	if pde >= 16 && pde < 20 {
		return true
	}
	return false
}

func 重新載入cr3() {
	cr3 := getcr3()
	設定cr3(cr3)
}

func S設定位元組進頁目錄(x byte, address uint32, 頁目錄 uint32) {
	oldcr3 := getcr3()
	設定cr3(頁目錄)
	S設定位元組ataddress(x, address)
	設定cr3(oldcr3)
}

func S設定區塊進頁目錄(來源_2 []byte, 目的地_2 []byte, 大小 uint32, 頁目錄 uint32) {
	if 大小 == 0 || 頁目錄 == 0 {
		return
	}
	oldcr3 := getcr3()
	設定cr3(頁目錄)
	makerange私密writable目前(頁目錄, uint32(uintptr(unsafe.Pointer(&目的地_2[0]))), 大小)

	for i := uint32(0); i < 大小; i++ {
		目的地_2[i] = 來源_2[i]
	}
	設定cr3(oldcr3)
}

func Z零區塊進頁目錄(address uint32, 大小 uint32, 頁目錄 uint32) {
	if 大小 == 0 || 頁目錄 == 0 {
		return
	}
	oldcr3 := getcr3()
	設定cr3(頁目錄)
	makerange私密writable目前(頁目錄, address, 大小)
	目的地_2 := Get位元組from指標(uintptr(address), int(大小), int(大小))
	for i := uint32(0); i < 大小; i++ {
		目的地_2[i] = 0
	}
	設定cr3(oldcr3)
}

func make頁私密writable目前(頁目錄 uint32, 虛擬address uint32) bool {
	pde := Get數值(頁目錄 + ((虛擬address>>22)&0x3FF)*4)
	if (pde & P頁目前) == 0 {
		return false
	}
	pteaddress := (pde & P頁框架) + ((虛擬address>>12)&0x3FF)*4
	pte := Get數值(pteaddress)
	if (pte & P頁目前) == 0 {
		return false
	}
	if (pte & P頁cow) == 0 {
		return (pte & P頁writable) != 0
	}
	if A啟用記憶體管理器 == nil {
		return false
	}
	新增指標, _ := A啟用記憶體管理器.Alignedmalloc(0x1000)
	if 新增指標 == nil {
		return false
	}
	新增框架 := uint32(uintptr(新增指標)) & P頁框架
	來源_2 := Get位元組from指標(uintptr(虛擬address&P頁框架), 0x1000, 0x1000)
	目的地_2 := Get位元組from指標(uintptr(新增框架), 0x1000, 0x1000)
	copy(目的地_2, 來源_2)
	cow框架管理器.Decrement(pte & P頁框架)
	S設定unsignedinteger32ataddress((新增框架|(pte&0xFFF)|P頁writable)&^P頁cow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	重新載入cr3()
	return true
}

func makerange私密writable目前(頁目錄 uint32, address uint32, 大小 uint32) bool {
	if 大小 == 0 {
		return true
	}
	最後 := address + 大小 - 1
	if 最後 < address {
		return false
	}
	for 頁 := address & P頁框架; ; 頁 += 0x1000 {
		if !make頁私密writable目前(頁目錄, 頁) {
			return false
		}
		if 頁 == (最後 & P頁框架) {
			break
		}
	}
	return true
}

func Makerange私密writable(頁目錄 uint32, address uint32, 大小 uint32) bool {
	if 頁目錄 == 0 {
		return false
	}
	oldcr3 := getcr3()
	設定cr3(頁目錄)
	確定 := makerange私密writable目前(頁目錄, address, 大小)
	設定cr3(oldcr3)
	return 確定
}

func S設定unsignedinteger32進頁目錄(x uint32, address uint32, 頁目錄 uint32) {
	if 頁目錄 == 0 {
		return
	}
	oldcr3 := getcr3()
	設定cr3(頁目錄)
	S設定unsignedinteger32ataddress(x, address)
	設定cr3(oldcr3)
}

func Get數值(address uint32) uint32 {
	var org數值 uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return org數值
}
func Get數值進頁目錄(address uint32, 頁目錄 uint32) uint32 {
	if 頁目錄 == 0 {
		return 0
	}
	oldcr3 := getcr3()
	設定cr3(頁目錄)
	v := Get數值(address)
	設定cr3(oldcr3)
	return v
}

var v uint32 = 0

func C複製頁框架區塊(x頁目錄 uint32, y頁目錄 uint32, vaddress uint32) {
	if x頁目錄 == 0 || y頁目錄 == 0 {
		return
	}
	oldcr3 := getcr3()
	設定cr3(x頁目錄)
	v = Get數值(vaddress)
	S設定unsignedinteger32進頁目錄(v, vaddress, y頁目錄)

	設定cr3(oldcr3)
}
