/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupt"
import . "memorymanager"
import . "util"

type Pagedirectoryentry_2 uintptr

const (
	Pagepresent	uint32	= 0x001
	Pagewritable	uint32	= 0x002
	Pageuser	uint32	= 0x004
	Pageframe	uint32	= 0xFFFFF000
	Pagecow		uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(pagedirectory uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type Tcowframemanager struct {
	mem		*TMemorymanager
	refs		[]uint16
	framecount	uint32
}

var (
	Pagedirectoryentry	uintptr
	Pagetableentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowframemanager		Tcowframemanager
)

func (self *Tcowframemanager) Init(mem *TMemorymanager, framecount uint32) bool {
	self.mem = mem
	self.framecount = framecount
	referencebytes := framecount * uint32(unsafe.Sizeof(uint16(0)))
	referencepointer := mem.Malloc(referencebytes)
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

func (self *Paging) Init(pagedirectoryentry uintptr, pagetableentry uint32, memorymanager *TMemorymanager) {

	Pagedirectoryentry = pagedirectoryentry
	Pagetableentry = pagetableentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframemanager.Init(memorymanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addresspointer, _ := memorymanager.Alignedmalloc(0x1000)
			if addresspointer == nil {
				return
			}
			address := uint32(uintptr(addresspointer))

			Setunsignedinteger32ataddress(address|0x87, uint32(pagedirectoryentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		pagedirectoryentry = pagedirectoryentry + 0x1000
	}

}
func (self *Paging) Sharedmemoryregion() {

	pagedirectoryentry := Pagedirectoryentry
	kpagedirectoryentry := Pagedirectoryentry

	for i := uint32(1); i <= virtlen; i++ {

		pagedirectoryentry = pagedirectoryentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Getvalue(uint32(kpagedirectoryentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(pagedirectoryentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getvalue(uint32(kpagedirectoryentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(pagedirectoryentry)+pde*4)

		}

	}
}
func (self *Paging) Pagefault(manager *TInterruptmanager) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if Resolvecopyonbindfault() {
		return esp
	}
	return Handlefatalinterruptframe(esp, 0x0E)
}

func Cloneaddressspacecow(sourcepagedirectory uint32) uint32 {
	if Activememorymanager == nil || sourcepagedirectory == 0 {
		return 0
	}
	destinationpointer, _ := Activememorymanager.Alignedmalloc(0x1000)
	if destinationpointer == nil {
		return 0
	}
	destinationpagedirectory := uint32(uintptr(destinationpointer))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationpagedirectory+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		sourcepdeaddress := sourcepagedirectory + pde*4
		sourcepde := Getvalue(sourcepdeaddress)
		if (sourcepde & Pagepresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(sourcepde, destinationpagedirectory+pde*4)
			continue
		}

		destinationptpointer, _ := Activememorymanager.Alignedmalloc(0x1000)
		if destinationptpointer == nil {
			continue
		}
		sourcept := sourcepde & Pageframe
		destinationpt := uint32(uintptr(destinationptpointer))
		Setunsignedinteger32ataddress((destinationpt | (sourcepde & 0xFFF)), destinationpagedirectory+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := sourcept + pte*4
			entry := Getvalue(pteaddress)
			if (entry & Pagepresent) != 0 {
				if (entry & Pagewritable) != 0 {
					entry = (entry &^ Pagewritable) | Pagecow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowframemanager.Increment(entry & Pageframe)
				} else if (entry & Pagecow) != 0 {
					cowframemanager.Increment(entry & Pageframe)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	reloadcr3()
	return destinationpagedirectory
}

func Resolvecopyonbindfault() bool {
	if Activememorymanager == nil {
		return false
	}
	faultaddress := getcr2()
	pagedirectory := getcr3()
	pdeaddress := pagedirectory + ((faultaddress>>22)&0x3FF)*4
	pde := Getvalue(pdeaddress)
	if (pde & Pagepresent) == 0 {
		return false
	}
	pt := pde & Pageframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := Getvalue(pteaddress)
	if (pte&Pagecow) == 0 || (pte&Pagepresent) == 0 {
		return false
	}
	oldframe := pte & Pageframe
	if cowframemanager.Reference(oldframe) <= 1 {
		Setunsignedinteger32ataddress((pte|Pagewritable)&^Pagecow, pteaddress)
		reloadcr3()
		return true
	}

	newpointer, _ := Activememorymanager.Alignedmalloc(0x1000)
	if newpointer == nil {
		return false
	}
	newframe := uint32(uintptr(newpointer)) & Pageframe

	source_2 := Getbytesfrompointer(uintptr(faultaddress&Pageframe), 0x1000, 0x1000)
	destination_2 := Getbytesfrompointer(uintptr(newframe), 0x1000, 0x1000)
	copy(destination_2, source_2)
	cowframemanager.Decrement(oldframe)
	Setunsignedinteger32ataddress((newframe|(pte&0xFFF)|Pagewritable)&^Pagecow, pteaddress)
	reloadcr3()
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

func reloadcr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func Setbyteinpagedirectory(x byte, address uint32, pagedirectory uint32) {
	oldcr3 := getcr3()
	setcr3(pagedirectory)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func Setblockinpagedirectory(source_2 []byte, destination_2 []byte, size uint32, pagedirectory uint32) {
	if size == 0 || pagedirectory == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(pagedirectory)
	makerangeprivatewritablecurrent(pagedirectory, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), size)

	for i := uint32(0); i < size; i++ {
		destination_2[i] = source_2[i]
	}
	setcr3(oldcr3)
}

func Zeroblockinpagedirectory(address uint32, size uint32, pagedirectory uint32) {
	if size == 0 || pagedirectory == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(pagedirectory)
	makerangeprivatewritablecurrent(pagedirectory, address, size)
	destination_2 := Getbytesfrompointer(uintptr(address), int(size), int(size))
	for i := uint32(0); i < size; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makepageprivatewritablecurrent(pagedirectory uint32, virtualaddress uint32) bool {
	pde := Getvalue(pagedirectory + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & Pagepresent) == 0 {
		return false
	}
	pteaddress := (pde & Pageframe) + ((virtualaddress>>12)&0x3FF)*4
	pte := Getvalue(pteaddress)
	if (pte & Pagepresent) == 0 {
		return false
	}
	if (pte & Pagecow) == 0 {
		return (pte & Pagewritable) != 0
	}
	if Activememorymanager == nil {
		return false
	}
	newpointer, _ := Activememorymanager.Alignedmalloc(0x1000)
	if newpointer == nil {
		return false
	}
	newframe := uint32(uintptr(newpointer)) & Pageframe
	source_2 := Getbytesfrompointer(uintptr(virtualaddress&Pageframe), 0x1000, 0x1000)
	destination_2 := Getbytesfrompointer(uintptr(newframe), 0x1000, 0x1000)
	copy(destination_2, source_2)
	cowframemanager.Decrement(pte & Pageframe)
	Setunsignedinteger32ataddress((newframe|(pte&0xFFF)|Pagewritable)&^Pagecow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	reloadcr3()
	return true
}

func makerangeprivatewritablecurrent(pagedirectory uint32, address uint32, size uint32) bool {
	if size == 0 {
		return true
	}
	last := address + size - 1
	if last < address {
		return false
	}
	for page := address & Pageframe; ; page += 0x1000 {
		if !makepageprivatewritablecurrent(pagedirectory, page) {
			return false
		}
		if page == (last & Pageframe) {
			break
		}
	}
	return true
}

func Makerangeprivatewritable(pagedirectory uint32, address uint32, size uint32) bool {
	if pagedirectory == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(pagedirectory)
	ok := makerangeprivatewritablecurrent(pagedirectory, address, size)
	setcr3(oldcr3)
	return ok
}

func Setunsignedinteger32inpagedirectory(x uint32, address uint32, pagedirectory uint32) {
	if pagedirectory == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(pagedirectory)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func Getvalue(address uint32) uint32 {
	var orgvalue uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgvalue
}
func Getvalueinpagedirectory(address uint32, pagedirectory uint32) uint32 {
	if pagedirectory == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(pagedirectory)
	v := Getvalue(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func Copypageframeblock(xpagedirectory uint32, ypagedirectory uint32, vaddress uint32) {
	if xpagedirectory == 0 || ypagedirectory == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xpagedirectory)
	v = Getvalue(vaddress)
	Setunsignedinteger32inpagedirectory(v, vaddress, ypagedirectory)

	setcr3(oldcr3)
}
