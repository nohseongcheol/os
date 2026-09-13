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
	Pageเฟรม	uint32	= 0xFFFFF000
	Pagecow		uint32	= 0x200
)

func Sกำหนดbyteataddress(x byte, address uint32)
func Sกำหนดunsignedinteger8ataddress(x uint8, address uint32)
func Sกำหนดunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func กำหนดcr3(pagedirectory uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type Tcowเฟรมmanager struct {
	mem		*TMemorymanager
	refs		[]uint16
	เฟรมcount	uint32
}

var (
	Pagedirectoryentry	uintptr
	Pageตารางentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowเฟรมmanager		Tcowเฟรมmanager
)

func (self *Tcowเฟรมmanager) Init(mem *TMemorymanager, เฟรมcount uint32) bool {
	self.mem = mem
	self.เฟรมcount = เฟรมcount
	referencebytes := เฟรมcount * uint32(unsafe.Sizeof(uint16(0)))
	referencepointer := mem.Malloc(referencebytes)
	if referencepointer == nil {
		self.refs = nil
		self.เฟรมcount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referencepointer)[:เฟรมcount:เฟรมcount]
	for i := uint32(0); i < เฟรมcount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcowเฟรมmanager) Reference(เฟรม uint32) uint16 {
	idx := เฟรม >> 12
	if idx >= self.เฟรมcount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcowเฟรมmanager) Increment(เฟรม uint32) {
	idx := เฟรม >> 12
	if idx >= self.เฟรมcount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcowเฟรมmanager) Decrement(เฟรม uint32) {
	idx := เฟรม >> 12
	if idx >= self.เฟรมcount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(pagedirectoryentry uintptr, pageตารางentry uint32, memorymanager *TMemorymanager) {

	Pagedirectoryentry = pagedirectoryentry
	Pageตารางentry = pageตารางentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowเฟรมmanager.Init(memorymanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addresspointer, _ := memorymanager.Alignedmalloc(0x1000)
			if addresspointer == nil {
				return
			}
			address := uint32(uintptr(addresspointer))

			Sกำหนดunsignedinteger32ataddress(address|0x87, uint32(pagedirectoryentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Sกำหนดunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
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
			Sกำหนดunsignedinteger32ataddress(v|0x87, uint32(pagedirectoryentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getvalue(uint32(kpagedirectoryentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sกำหนดunsignedinteger32ataddress(v|0x87, uint32(pagedirectoryentry)+pde*4)

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
	if Resolvecopyonkhianfault() {
		return esp
	}
	return Handlefatalinterruptเฟรม(esp, 0x0E)
}

func Cloneaddressspacecow(sourcepagedirectory uint32) uint32 {
	if Aทำงานmemorymanager == nil || sourcepagedirectory == 0 {
		return 0
	}
	ปลายทางpointer, _ := Aทำงานmemorymanager.Alignedmalloc(0x1000)
	if ปลายทางpointer == nil {
		return 0
	}
	ปลายทางpagedirectory := uint32(uintptr(ปลายทางpointer))
	for i := uint32(0); i < 1024; i++ {
		Sกำหนดunsignedinteger32ataddress(0, ปลายทางpagedirectory+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		sourcepdeaddress := sourcepagedirectory + pde*4
		sourcepde := Getvalue(sourcepdeaddress)
		if (sourcepde & Pagepresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Sกำหนดunsignedinteger32ataddress(sourcepde, ปลายทางpagedirectory+pde*4)
			continue
		}

		ปลายทางptpointer, _ := Aทำงานmemorymanager.Alignedmalloc(0x1000)
		if ปลายทางptpointer == nil {
			continue
		}
		sourcept := sourcepde & Pageเฟรม
		ปลายทางpt := uint32(uintptr(ปลายทางptpointer))
		Sกำหนดunsignedinteger32ataddress((ปลายทางpt | (sourcepde & 0xFFF)), ปลายทางpagedirectory+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := sourcept + pte*4
			entry := Getvalue(pteaddress)
			if (entry & Pagepresent) != 0 {
				if (entry & Pagewritable) != 0 {
					entry = (entry &^ Pagewritable) | Pagecow
					Sกำหนดunsignedinteger32ataddress(entry, pteaddress)
					cowเฟรมmanager.Increment(entry & Pageเฟรม)
				} else if (entry & Pagecow) != 0 {
					cowเฟรมmanager.Increment(entry & Pageเฟรม)
				}
			}
			Sกำหนดunsignedinteger32ataddress(entry, ปลายทางpt+pte*4)
		}
	}
	reloadcr3()
	return ปลายทางpagedirectory
}

func Resolvecopyonkhianfault() bool {
	if Aทำงานmemorymanager == nil {
		return false
	}
	faultaddress := getcr2()
	pagedirectory := getcr3()
	pdeaddress := pagedirectory + ((faultaddress>>22)&0x3FF)*4
	pde := Getvalue(pdeaddress)
	if (pde & Pagepresent) == 0 {
		return false
	}
	pt := pde & Pageเฟรม
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := Getvalue(pteaddress)
	if (pte&Pagecow) == 0 || (pte&Pagepresent) == 0 {
		return false
	}
	oldเฟรม := pte & Pageเฟรม
	if cowเฟรมmanager.Reference(oldเฟรม) <= 1 {
		Sกำหนดunsignedinteger32ataddress((pte|Pagewritable)&^Pagecow, pteaddress)
		reloadcr3()
		return true
	}

	newpointer, _ := Aทำงานmemorymanager.Alignedmalloc(0x1000)
	if newpointer == nil {
		return false
	}
	newเฟรม := uint32(uintptr(newpointer)) & Pageเฟรม

	source_2 := Getbytesfrompointer(uintptr(faultaddress&Pageเฟรม), 0x1000, 0x1000)
	ปลายทาง_2 := Getbytesfrompointer(uintptr(newเฟรม), 0x1000, 0x1000)
	copy(ปลายทาง_2, source_2)
	cowเฟรมmanager.Decrement(oldเฟรม)
	Sกำหนดunsignedinteger32ataddress((newเฟรม|(pte&0xFFF)|Pagewritable)&^Pagecow, pteaddress)
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
	กำหนดcr3(cr3)
}

func Sกำหนดbyteขยายpagedirectory(x byte, address uint32, pagedirectory uint32) {
	oldcr3 := getcr3()
	กำหนดcr3(pagedirectory)
	Sกำหนดbyteataddress(x, address)
	กำหนดcr3(oldcr3)
}

func Sกำหนดblockขยายpagedirectory(source_2 []byte, ปลายทาง_2 []byte, ขนาด uint32, pagedirectory uint32) {
	if ขนาด == 0 || pagedirectory == 0 {
		return
	}
	oldcr3 := getcr3()
	กำหนดcr3(pagedirectory)
	makerangeprivatewritablecurrent(pagedirectory, uint32(uintptr(unsafe.Pointer(&ปลายทาง_2[0]))), ขนาด)

	for i := uint32(0); i < ขนาด; i++ {
		ปลายทาง_2[i] = source_2[i]
	}
	กำหนดcr3(oldcr3)
}

func Zeroblockขยายpagedirectory(address uint32, ขนาด uint32, pagedirectory uint32) {
	if ขนาด == 0 || pagedirectory == 0 {
		return
	}
	oldcr3 := getcr3()
	กำหนดcr3(pagedirectory)
	makerangeprivatewritablecurrent(pagedirectory, address, ขนาด)
	ปลายทาง_2 := Getbytesfrompointer(uintptr(address), int(ขนาด), int(ขนาด))
	for i := uint32(0); i < ขนาด; i++ {
		ปลายทาง_2[i] = 0
	}
	กำหนดcr3(oldcr3)
}

func makepageprivatewritablecurrent(pagedirectory uint32, virtualaddress uint32) bool {
	pde := Getvalue(pagedirectory + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & Pagepresent) == 0 {
		return false
	}
	pteaddress := (pde & Pageเฟรม) + ((virtualaddress>>12)&0x3FF)*4
	pte := Getvalue(pteaddress)
	if (pte & Pagepresent) == 0 {
		return false
	}
	if (pte & Pagecow) == 0 {
		return (pte & Pagewritable) != 0
	}
	if Aทำงานmemorymanager == nil {
		return false
	}
	newpointer, _ := Aทำงานmemorymanager.Alignedmalloc(0x1000)
	if newpointer == nil {
		return false
	}
	newเฟรม := uint32(uintptr(newpointer)) & Pageเฟรม
	source_2 := Getbytesfrompointer(uintptr(virtualaddress&Pageเฟรม), 0x1000, 0x1000)
	ปลายทาง_2 := Getbytesfrompointer(uintptr(newเฟรม), 0x1000, 0x1000)
	copy(ปลายทาง_2, source_2)
	cowเฟรมmanager.Decrement(pte & Pageเฟรม)
	Sกำหนดunsignedinteger32ataddress((newเฟรม|(pte&0xFFF)|Pagewritable)&^Pagecow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	reloadcr3()
	return true
}

func makerangeprivatewritablecurrent(pagedirectory uint32, address uint32, ขนาด uint32) bool {
	if ขนาด == 0 {
		return true
	}
	last := address + ขนาด - 1
	if last < address {
		return false
	}
	for page := address & Pageเฟรม; ; page += 0x1000 {
		if !makepageprivatewritablecurrent(pagedirectory, page) {
			return false
		}
		if page == (last & Pageเฟรม) {
			break
		}
	}
	return true
}

func Makerangeprivatewritable(pagedirectory uint32, address uint32, ขนาด uint32) bool {
	if pagedirectory == 0 {
		return false
	}
	oldcr3 := getcr3()
	กำหนดcr3(pagedirectory)
	ตกลง := makerangeprivatewritablecurrent(pagedirectory, address, ขนาด)
	กำหนดcr3(oldcr3)
	return ตกลง
}

func Sกำหนดunsignedinteger32ขยายpagedirectory(x uint32, address uint32, pagedirectory uint32) {
	if pagedirectory == 0 {
		return
	}
	oldcr3 := getcr3()
	กำหนดcr3(pagedirectory)
	Sกำหนดunsignedinteger32ataddress(x, address)
	กำหนดcr3(oldcr3)
}

func Getvalue(address uint32) uint32 {
	var orgvalue uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgvalue
}
func Getvalueขยายpagedirectory(address uint32, pagedirectory uint32) uint32 {
	if pagedirectory == 0 {
		return 0
	}
	oldcr3 := getcr3()
	กำหนดcr3(pagedirectory)
	v := Getvalue(address)
	กำหนดcr3(oldcr3)
	return v
}

var v uint32 = 0

func Copypageเฟรมblock(xpagedirectory uint32, ypagedirectory uint32, vaddress uint32) {
	if xpagedirectory == 0 || ypagedirectory == 0 {
		return
	}
	oldcr3 := getcr3()
	กำหนดcr3(xpagedirectory)
	v = Getvalue(vaddress)
	Sกำหนดunsignedinteger32ขยายpagedirectory(v, vaddress, ypagedirectory)

	กำหนดcr3(oldcr3)
}
