/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 分页管理

import unsafe "unsafe"
import . "中断"
import . "内存管理器"
import . "工具"

type P页目录条目_2 uintptr

const (
	P页当前电池		uint32	= 0x001
	P页writable	uint32	= 0x002
	P页用户		uint32	= 0x004
	P页帧		uint32	= 0xFFFFF000
	P页cow		uint32	= 0x200
)

func S集合字节ataddress(x byte, address uint32)
func S集合unsignedinteger8ataddress(x uint8, address uint32)
func S集合unsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func 集合cr3(页目录 uint32)
func getcr3() uint32

type P分页管理 struct {
	T中断handler
}
type Tcow帧管理器 struct {
	mem	*T内存管理器
	refs	[]uint16
	帧计数	uint32
}

var (
	P页目录条目	uintptr
	P页表格条目	uint32
	pdelen	uint32
	virtlen	uint32
	cow帧管理器	Tcow帧管理器
)

func (self *Tcow帧管理器) Init(mem *T内存管理器, 帧计数 uint32) bool {
	self.mem = mem
	self.帧计数 = 帧计数
	reference字节 := 帧计数 * uint32(unsafe.Sizeof(uint16(0)))
	reference指针 := mem.M分配内存(reference字节)
	if reference指针 == nil {
		self.refs = nil
		self.帧计数 = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(reference指针)[:帧计数:帧计数]
	for i := uint32(0); i < 帧计数; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcow帧管理器) Reference(帧 uint32) uint16 {
	idx := 帧 >> 12
	if idx >= self.帧计数 || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcow帧管理器) Increment(帧 uint32) {
	idx := 帧 >> 12
	if idx >= self.帧计数 || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcow帧管理器) Decrement(帧 uint32) {
	idx := 帧 >> 12
	if idx >= self.帧计数 || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *P分页管理) Init(页目录条目 uintptr, 页表格条目 uint32, 内存管理器 *T内存管理器) {

	P页目录条目 = 页目录条目
	P页表格条目 = 页表格条目

	virtlen = uint32(6)
	pdelen = uint32(32)

	cow帧管理器.Init(内存管理器, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			address指针, _ := 内存管理器.Alignedmalloc(0x1000)
			if address指针 == nil {
				return
			}
			address := uint32(uintptr(address指针))

			S集合unsignedinteger32ataddress(address|0x87, uint32(页目录条目)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				S集合unsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		页目录条目 = 页目录条目 + 0x1000
	}

}
func (self *P分页管理) Shared内存region() {

	页目录条目 := P页目录条目
	k页目录条目 := P页目录条目

	for i := uint32(1); i <= virtlen; i++ {

		页目录条目 = 页目录条目 + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Get值(uint32(k页目录条目) + pde*4)
			v = (v & 0xFFFFF000)
			S集合unsignedinteger32ataddress(v|0x87, uint32(页目录条目)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Get值(uint32(k页目录条目) + pde*4)
			v = (v & 0xFFFFF000)
			S集合unsignedinteger32ataddress(v|0x87, uint32(页目录条目)+pde*4)

		}

	}
}
func (self *P分页管理) P页故障(管理器 *T中断管理器) {
	中断handler = 控制器分页管理中断

	var address uintptr
	address = uintptr(unsafe.Pointer(&中断handler))
	self.T中断handler.Init(0xE, uintptr(unsafe.Pointer(管理器)), address)
}

var 中断handler func(uint32) uint32

func 控制器分页管理中断(esp uint32) uint32 {
	if R解决复制时写入故障() {
		return esp
	}
	return H控制器fatal中断帧(esp, 0x0E)
}

func Cloneaddress空格cow(源页目录 uint32) uint32 {
	if A活跃内存管理器 == nil || 源页目录 == 0 {
		return 0
	}
	目的指针, _ := A活跃内存管理器.Alignedmalloc(0x1000)
	if 目的指针 == nil {
		return 0
	}
	目的页目录 := uint32(uintptr(目的指针))
	for i := uint32(0); i < 1024; i++ {
		S集合unsignedinteger32ataddress(0, 目的页目录+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		源pdeaddress := 源页目录 + pde*4
		源pde := Get值(源pdeaddress)
		if (源pde & P页当前电池) == 0 {
			continue
		}
		if issharedpde(pde) {
			S集合unsignedinteger32ataddress(源pde, 目的页目录+pde*4)
			continue
		}

		目的pt指针, _ := A活跃内存管理器.Alignedmalloc(0x1000)
		if 目的pt指针 == nil {
			continue
		}
		源pt := 源pde & P页帧
		目的pt := uint32(uintptr(目的pt指针))
		S集合unsignedinteger32ataddress((目的pt | (源pde & 0xFFF)), 目的页目录+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := 源pt + pte*4
			条目 := Get值(pteaddress)
			if (条目 & P页当前电池) != 0 {
				if (条目 & P页writable) != 0 {
					条目 = (条目 &^ P页writable) | P页cow
					S集合unsignedinteger32ataddress(条目, pteaddress)
					cow帧管理器.Increment(条目 & P页帧)
				} else if (条目 & P页cow) != 0 {
					cow帧管理器.Increment(条目 & P页帧)
				}
			}
			S集合unsignedinteger32ataddress(条目, 目的pt+pte*4)
		}
	}
	重新载入cr3()
	return 目的页目录
}

func R解决复制时写入故障() bool {
	if A活跃内存管理器 == nil {
		return false
	}
	故障address := getcr2()
	页目录 := getcr3()
	pdeaddress := 页目录 + ((故障address>>22)&0x3FF)*4
	pde := Get值(pdeaddress)
	if (pde & P页当前电池) == 0 {
		return false
	}
	pt := pde & P页帧
	pteaddress := pt + ((故障address>>12)&0x3FF)*4
	pte := Get值(pteaddress)
	if (pte&P页cow) == 0 || (pte&P页当前电池) == 0 {
		return false
	}
	old帧 := pte & P页帧
	if cow帧管理器.Reference(old帧) <= 1 {
		S集合unsignedinteger32ataddress((pte|P页writable)&^P页cow, pteaddress)
		重新载入cr3()
		return true
	}

	新建指针, _ := A活跃内存管理器.Alignedmalloc(0x1000)
	if 新建指针 == nil {
		return false
	}
	新建帧 := uint32(uintptr(新建指针)) & P页帧

	源_2 := Get字节from指针(uintptr(故障address&P页帧), 0x1000, 0x1000)
	目的_2 := Get字节from指针(uintptr(新建帧), 0x1000, 0x1000)
	copy(目的_2, 源_2)
	cow帧管理器.Decrement(old帧)
	S集合unsignedinteger32ataddress((新建帧|(pte&0xFFF)|P页writable)&^P页cow, pteaddress)
	重新载入cr3()
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

func 重新载入cr3() {
	cr3 := getcr3()
	集合cr3(cr3)
}

func S集合字节进页目录(x byte, address uint32, 页目录 uint32) {
	oldcr3 := getcr3()
	集合cr3(页目录)
	S集合字节ataddress(x, address)
	集合cr3(oldcr3)
}

func S集合块进页目录(源_2 []byte, 目的_2 []byte, 大小 uint32, 页目录 uint32) {
	if 大小 == 0 || 页目录 == 0 {
		return
	}
	oldcr3 := getcr3()
	集合cr3(页目录)
	make范围专用writable当前(页目录, uint32(uintptr(unsafe.Pointer(&目的_2[0]))), 大小)

	for i := uint32(0); i < 大小; i++ {
		目的_2[i] = 源_2[i]
	}
	集合cr3(oldcr3)
}

func Z零块进页目录(address uint32, 大小 uint32, 页目录 uint32) {
	if 大小 == 0 || 页目录 == 0 {
		return
	}
	oldcr3 := getcr3()
	集合cr3(页目录)
	make范围专用writable当前(页目录, address, 大小)
	目的_2 := Get字节from指针(uintptr(address), int(大小), int(大小))
	for i := uint32(0); i < 大小; i++ {
		目的_2[i] = 0
	}
	集合cr3(oldcr3)
}

func make页专用writable当前(页目录 uint32, 虚拟address uint32) bool {
	pde := Get值(页目录 + ((虚拟address>>22)&0x3FF)*4)
	if (pde & P页当前电池) == 0 {
		return false
	}
	pteaddress := (pde & P页帧) + ((虚拟address>>12)&0x3FF)*4
	pte := Get值(pteaddress)
	if (pte & P页当前电池) == 0 {
		return false
	}
	if (pte & P页cow) == 0 {
		return (pte & P页writable) != 0
	}
	if A活跃内存管理器 == nil {
		return false
	}
	新建指针, _ := A活跃内存管理器.Alignedmalloc(0x1000)
	if 新建指针 == nil {
		return false
	}
	新建帧 := uint32(uintptr(新建指针)) & P页帧
	源_2 := Get字节from指针(uintptr(虚拟address&P页帧), 0x1000, 0x1000)
	目的_2 := Get字节from指针(uintptr(新建帧), 0x1000, 0x1000)
	copy(目的_2, 源_2)
	cow帧管理器.Decrement(pte & P页帧)
	S集合unsignedinteger32ataddress((新建帧|(pte&0xFFF)|P页writable)&^P页cow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	重新载入cr3()
	return true
}

func make范围专用writable当前(页目录 uint32, address uint32, 大小 uint32) bool {
	if 大小 == 0 {
		return true
	}
	最近 := address + 大小 - 1
	if 最近 < address {
		return false
	}
	for 页 := address & P页帧; ; 页 += 0x1000 {
		if !make页专用writable当前(页目录, 页) {
			return false
		}
		if 页 == (最近 & P页帧) {
			break
		}
	}
	return true
}

func Make范围专用writable(页目录 uint32, address uint32, 大小 uint32) bool {
	if 页目录 == 0 {
		return false
	}
	oldcr3 := getcr3()
	集合cr3(页目录)
	确定 := make范围专用writable当前(页目录, address, 大小)
	集合cr3(oldcr3)
	return 确定
}

func S集合unsignedinteger32进页目录(x uint32, address uint32, 页目录 uint32) {
	if 页目录 == 0 {
		return
	}
	oldcr3 := getcr3()
	集合cr3(页目录)
	S集合unsignedinteger32ataddress(x, address)
	集合cr3(oldcr3)
}

func Get值(address uint32) uint32 {
	var org值 uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return org值
}
func Get值进页目录(address uint32, 页目录 uint32) uint32 {
	if 页目录 == 0 {
		return 0
	}
	oldcr3 := getcr3()
	集合cr3(页目录)
	v := Get值(address)
	集合cr3(oldcr3)
	return v
}

var v uint32 = 0

func C复制页帧块(x页目录 uint32, y页目录 uint32, vaddress uint32) {
	if x页目录 == 0 || y页目录 == 0 {
		return
	}
	oldcr3 := getcr3()
	集合cr3(x页目录)
	v = Get值(vaddress)
	S集合unsignedinteger32进页目录(v, vaddress, y页目录)

	集合cr3(oldcr3)
}
