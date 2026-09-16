/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupt"
import . "yaddaşmanager"
import . "util"

type SəhifəCərgəentry_2 uintptr

const (
	Səhifəpresent		uint32	= 0x001
	Səhifəwritable		uint32	= 0x002
	Səhifəİstifadəçi	uint32	= 0x004
	Səhifəframe		uint32	= 0xFFFFF000
	Səhifəcow		uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(səhifəCərgə uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type Tcowframemanager struct {
	mem		*TYaddaşmanager
	refs		[]uint16
	framecount	uint32
}

var (
	SəhifəCərgəentry	uintptr
	Səhifətableentry	uint32
	pdelen			uint32
	virtlen			uint32
	cowframemanager		Tcowframemanager
)

func (self *Tcowframemanager) Init(mem *TYaddaşmanager, framecount uint32) bool {
	self.mem = mem
	self.framecount = framecount
	referenceBayt := framecount * uint32(unsafe.Sizeof(uint16(0)))
	referencepointer := mem.Malloc(referenceBayt)
	if referencepointer == nil {
		self.refs = nil
		self.framecount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referencepointer)[:framecount:framecount]
	for i := uint32(0); i < framecount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcowframemanager) Reference(frame uint32) uint16 {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcowframemanager) Increment(frame uint32) {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcowframemanager) Decrement(frame uint32) {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(səhifəCərgəentry uintptr, səhifətableentry uint32, yaddaşmanager *TYaddaşmanager) {

	SəhifəCərgəentry = səhifəCərgəentry
	Səhifətableentry = səhifətableentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframemanager.Init(yaddaşmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addresspointer, _ := yaddaşmanager.Alignedmalloc(0x1000)
			if addresspointer == nil {
				return
			}
			address := uint32(uintptr(addresspointer))

			Setunsignedinteger32ataddress(address|0x87, uint32(səhifəCərgəentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		səhifəCərgəentry = səhifəCərgəentry + 0x1000
	}

}
func (self *Paging) SharedYaddaşregion() {

	səhifəCərgəentry := SəhifəCərgəentry
	kSəhifəCərgəentry := SəhifəCərgəentry

	for i := uint32(1); i <= virtlen; i++ {

		səhifəCərgəentry = səhifəCərgəentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetQiymət(uint32(kSəhifəCərgəentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(səhifəCərgəentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetQiymət(uint32(kSəhifəCərgəentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(səhifəCərgəentry)+pde*4)

		}

	}
}
func (self *Paging) Səhifəfault(manager *TInterruptmanager) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if ResolveKöçüronYazmafault() {
		return esp
	}
	return Handlefatalinterruptframe(esp, 0x0E)
}

func Cloneaddressspacecow(mənbəSəhifəCərgə uint32) uint32 {
	if FəalYaddaşmanager == nil || mənbəSəhifəCərgə == 0 {
		return 0
	}
	destinationpointer, _ := FəalYaddaşmanager.Alignedmalloc(0x1000)
	if destinationpointer == nil {
		return 0
	}
	destinationSəhifəCərgə := uint32(uintptr(destinationpointer))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationSəhifəCərgə+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		mənbəpdeaddress := mənbəSəhifəCərgə + pde*4
		mənbəpde := GetQiymət(mənbəpdeaddress)
		if (mənbəpde & Səhifəpresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(mənbəpde, destinationSəhifəCərgə+pde*4)
			continue
		}

		destinationptpointer, _ := FəalYaddaşmanager.Alignedmalloc(0x1000)
		if destinationptpointer == nil {
			continue
		}
		mənbəpt := mənbəpde & Səhifəframe
		destinationpt := uint32(uintptr(destinationptpointer))
		Setunsignedinteger32ataddress((destinationpt | (mənbəpde & 0xFFF)), destinationSəhifəCərgə+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := mənbəpt + pte*4
			entry := GetQiymət(pteaddress)
			if (entry & Səhifəpresent) != 0 {
				if (entry & Səhifəwritable) != 0 {
					entry = (entry &^ Səhifəwritable) | Səhifəcow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowframemanager.Increment(entry & Səhifəframe)
				} else if (entry & Səhifəcow) != 0 {
					cowframemanager.Increment(entry & Səhifəframe)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	yeniləcr3()
	return destinationSəhifəCərgə
}

func ResolveKöçüronYazmafault() bool {
	if FəalYaddaşmanager == nil {
		return false
	}
	faultaddress := getcr2()
	səhifəCərgə := getcr3()
	pdeaddress := səhifəCərgə + ((faultaddress>>22)&0x3FF)*4
	pde := GetQiymət(pdeaddress)
	if (pde & Səhifəpresent) == 0 {
		return false
	}
	pt := pde & Səhifəframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetQiymət(pteaddress)
	if (pte&Səhifəcow) == 0 || (pte&Səhifəpresent) == 0 {
		return false
	}
	oldframe := pte & Səhifəframe
	if cowframemanager.Reference(oldframe) <= 1 {
		Setunsignedinteger32ataddress((pte|Səhifəwritable)&^Səhifəcow, pteaddress)
		yeniləcr3()
		return true
	}

	yenipointer, _ := FəalYaddaşmanager.Alignedmalloc(0x1000)
	if yenipointer == nil {
		return false
	}
	yeniframe := uint32(uintptr(yenipointer)) & Səhifəframe

	mənbə_2 := GetBaytfrompointer(uintptr(faultaddress&Səhifəframe), 0x1000, 0x1000)
	destination_2 := GetBaytfrompointer(uintptr(yeniframe), 0x1000, 0x1000)
	copy(destination_2, mənbə_2)
	cowframemanager.Decrement(oldframe)
	Setunsignedinteger32ataddress((yeniframe|(pte&0xFFF)|Səhifəwritable)&^Səhifəcow, pteaddress)
	yeniləcr3()
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

func yeniləcr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func SetbyteinSəhifəCərgə(x byte, address uint32, səhifəCərgə uint32) {
	oldcr3 := getcr3()
	setcr3(səhifəCərgə)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func SetblockinSəhifəCərgə(mənbə_2 []byte, destination_2 []byte, böyüklük uint32, səhifəCərgə uint32) {
	if böyüklük == 0 || səhifəCərgə == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(səhifəCərgə)
	makerangeprivatewritablecurrent(səhifəCərgə, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), böyüklük)

	for i := uint32(0); i < böyüklük; i++ {
		destination_2[i] = mənbə_2[i]
	}
	setcr3(oldcr3)
}

func ZeroblockinSəhifəCərgə(address uint32, böyüklük uint32, səhifəCərgə uint32) {
	if böyüklük == 0 || səhifəCərgə == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(səhifəCərgə)
	makerangeprivatewritablecurrent(səhifəCərgə, address, böyüklük)
	destination_2 := GetBaytfrompointer(uintptr(address), int(böyüklük), int(böyüklük))
	for i := uint32(0); i < böyüklük; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makeSəhifəprivatewritablecurrent(səhifəCərgə uint32, virtualaddress uint32) bool {
	pde := GetQiymət(səhifəCərgə + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & Səhifəpresent) == 0 {
		return false
	}
	pteaddress := (pde & Səhifəframe) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetQiymət(pteaddress)
	if (pte & Səhifəpresent) == 0 {
		return false
	}
	if (pte & Səhifəcow) == 0 {
		return (pte & Səhifəwritable) != 0
	}
	if FəalYaddaşmanager == nil {
		return false
	}
	yenipointer, _ := FəalYaddaşmanager.Alignedmalloc(0x1000)
	if yenipointer == nil {
		return false
	}
	yeniframe := uint32(uintptr(yenipointer)) & Səhifəframe
	mənbə_2 := GetBaytfrompointer(uintptr(virtualaddress&Səhifəframe), 0x1000, 0x1000)
	destination_2 := GetBaytfrompointer(uintptr(yeniframe), 0x1000, 0x1000)
	copy(destination_2, mənbə_2)
	cowframemanager.Decrement(pte & Səhifəframe)
	Setunsignedinteger32ataddress((yeniframe|(pte&0xFFF)|Səhifəwritable)&^Səhifəcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	yeniləcr3()
	return true
}

func makerangeprivatewritablecurrent(səhifəCərgə uint32, address uint32, böyüklük uint32) bool {
	if böyüklük == 0 {
		return true
	}
	last := address + böyüklük - 1
	if last < address {
		return false
	}
	for səhifə := address & Səhifəframe; ; səhifə += 0x1000 {
		if !makeSəhifəprivatewritablecurrent(səhifəCərgə, səhifə) {
			return false
		}
		if səhifə == (last & Səhifəframe) {
			break
		}
	}
	return true
}

func Makerangeprivatewritable(səhifəCərgə uint32, address uint32, böyüklük uint32) bool {
	if səhifəCərgə == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(səhifəCərgə)
	oldu := makerangeprivatewritablecurrent(səhifəCərgə, address, böyüklük)
	setcr3(oldcr3)
	return oldu
}

func Setunsignedinteger32inSəhifəCərgə(x uint32, address uint32, səhifəCərgə uint32) {
	if səhifəCərgə == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(səhifəCərgə)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func GetQiymət(address uint32) uint32 {
	var orgQiymət uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgQiymət
}
func GetQiymətinSəhifəCərgə(address uint32, səhifəCərgə uint32) uint32 {
	if səhifəCərgə == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(səhifəCərgə)
	v := GetQiymət(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func KöçürSəhifəframeblock(xSəhifəCərgə uint32, ySəhifəCərgə uint32, vaddress uint32) {
	if xSəhifəCərgə == 0 || ySəhifəCərgə == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xSəhifəCərgə)
	v = GetQiymət(vaddress)
	Setunsignedinteger32inSəhifəCərgə(v, vaddress, ySəhifəCərgə)

	setcr3(oldcr3)
}
