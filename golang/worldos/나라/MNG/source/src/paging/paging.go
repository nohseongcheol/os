/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupt"
import . "санахойЗохицуулагч"
import . "util"

type ХУУДАСЛавлахentry_2 uintptr

const (
	ХУУДАСpresent	uint32	= 0x001
	ХУУДАСwritable	uint32	= 0x002
	ХУУДАСХэрэглэгч	uint32	= 0x004
	ХУУДАСframe	uint32	= 0xFFFFF000
	ХУУДАСcow	uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(хУУДАСЛавлах uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowframeЗохицуулагч struct {
	mem		*TСанахойЗохицуулагч
	refs		[]uint16
	framecount	uint32
}

var (
	ХУУДАСЛавлахentry	uintptr
	ХУУДАСtableentry	uint32
	pdelen			uint32
	virtlen			uint32
	cowframeЗохицуулагч	TcowframeЗохицуулагч
)

func (self *TcowframeЗохицуулагч) Init(mem *TСанахойЗохицуулагч, framecount uint32) bool {
	self.mem = mem
	self.framecount = framecount
	referenceБайт := framecount * uint32(unsafe.Sizeof(uint16(0)))
	referencepointer := mem.Malloc(referenceБайт)
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

func (self *TcowframeЗохицуулагч) Reference(frame uint32) uint16 {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowframeЗохицуулагч) Increment(frame uint32) {
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

func (self *TcowframeЗохицуулагч) Decrement(frame uint32) {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(хУУДАСЛавлахentry uintptr, хУУДАСtableentry uint32, санахойЗохицуулагч *TСанахойЗохицуулагч) {

	ХУУДАСЛавлахentry = хУУДАСЛавлахentry
	ХУУДАСtableentry = хУУДАСtableentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframeЗохицуулагч.Init(санахойЗохицуулагч, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addresspointer, _ := санахойЗохицуулагч.Alignedmalloc(0x1000)
			if addresspointer == nil {
				return
			}
			address := uint32(uintptr(addresspointer))

			Setunsignedinteger32ataddress(address|0x87, uint32(хУУДАСЛавлахentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		хУУДАСЛавлахentry = хУУДАСЛавлахentry + 0x1000
	}

}
func (self *Paging) SharedСанахойregion() {

	хУУДАСЛавлахentry := ХУУДАСЛавлахentry
	kХУУДАСЛавлахentry := ХУУДАСЛавлахentry

	for i := uint32(1); i <= virtlen; i++ {

		хУУДАСЛавлахentry = хУУДАСЛавлахentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetУтга(uint32(kХУУДАСЛавлахentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(хУУДАСЛавлахentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetУтга(uint32(kХУУДАСЛавлахentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(хУУДАСЛавлахentry)+pde*4)

		}

	}
}
func (self *Paging) ХУУДАСfault(зохицуулагч *TInterruptЗохицуулагч) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(зохицуулагч)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if ResolveХуулахonБичихfault() {
		return esp
	}
	return Handlefatalinterruptframe(esp, 0x0E)
}

func Cloneaddressspacecow(эхХУУДАСЛавлах uint32) uint32 {
	if ИдэвхтэйСанахойЗохицуулагч == nil || эхХУУДАСЛавлах == 0 {
		return 0
	}
	destinationpointer, _ := ИдэвхтэйСанахойЗохицуулагч.Alignedmalloc(0x1000)
	if destinationpointer == nil {
		return 0
	}
	destinationХУУДАСЛавлах := uint32(uintptr(destinationpointer))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationХУУДАСЛавлах+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		эхpdeaddress := эхХУУДАСЛавлах + pde*4
		эхpde := GetУтга(эхpdeaddress)
		if (эхpde & ХУУДАСpresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(эхpde, destinationХУУДАСЛавлах+pde*4)
			continue
		}

		destinationptpointer, _ := ИдэвхтэйСанахойЗохицуулагч.Alignedmalloc(0x1000)
		if destinationptpointer == nil {
			continue
		}
		эхpt := эхpde & ХУУДАСframe
		destinationpt := uint32(uintptr(destinationptpointer))
		Setunsignedinteger32ataddress((destinationpt | (эхpde & 0xFFF)), destinationХУУДАСЛавлах+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := эхpt + pte*4
			entry := GetУтга(pteaddress)
			if (entry & ХУУДАСpresent) != 0 {
				if (entry & ХУУДАСwritable) != 0 {
					entry = (entry &^ ХУУДАСwritable) | ХУУДАСcow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowframeЗохицуулагч.Increment(entry & ХУУДАСframe)
				} else if (entry & ХУУДАСcow) != 0 {
					cowframeЗохицуулагч.Increment(entry & ХУУДАСframe)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	ахиначаалахcr3()
	return destinationХУУДАСЛавлах
}

func ResolveХуулахonБичихfault() bool {
	if ИдэвхтэйСанахойЗохицуулагч == nil {
		return false
	}
	faultaddress := getcr2()
	хУУДАСЛавлах := getcr3()
	pdeaddress := хУУДАСЛавлах + ((faultaddress>>22)&0x3FF)*4
	pde := GetУтга(pdeaddress)
	if (pde & ХУУДАСpresent) == 0 {
		return false
	}
	pt := pde & ХУУДАСframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetУтга(pteaddress)
	if (pte&ХУУДАСcow) == 0 || (pte&ХУУДАСpresent) == 0 {
		return false
	}
	oldframe := pte & ХУУДАСframe
	if cowframeЗохицуулагч.Reference(oldframe) <= 1 {
		Setunsignedinteger32ataddress((pte|ХУУДАСwritable)&^ХУУДАСcow, pteaddress)
		ахиначаалахcr3()
		return true
	}

	шинэpointer, _ := ИдэвхтэйСанахойЗохицуулагч.Alignedmalloc(0x1000)
	if шинэpointer == nil {
		return false
	}
	шинэframe := uint32(uintptr(шинэpointer)) & ХУУДАСframe

	эх_2 := GetБайтfrompointer(uintptr(faultaddress&ХУУДАСframe), 0x1000, 0x1000)
	destination_2 := GetБайтfrompointer(uintptr(шинэframe), 0x1000, 0x1000)
	copy(destination_2, эх_2)
	cowframeЗохицуулагч.Decrement(oldframe)
	Setunsignedinteger32ataddress((шинэframe|(pte&0xFFF)|ХУУДАСwritable)&^ХУУДАСcow, pteaddress)
	ахиначаалахcr3()
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

func ахиначаалахcr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func SetbyteinХУУДАСЛавлах(x byte, address uint32, хУУДАСЛавлах uint32) {
	oldcr3 := getcr3()
	setcr3(хУУДАСЛавлах)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func SetblockinХУУДАСЛавлах(эх_2 []byte, destination_2 []byte, хэмжээ uint32, хУУДАСЛавлах uint32) {
	if хэмжээ == 0 || хУУДАСЛавлах == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(хУУДАСЛавлах)
	makerangeprivatewritablecurrent(хУУДАСЛавлах, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), хэмжээ)

	for i := uint32(0); i < хэмжээ; i++ {
		destination_2[i] = эх_2[i]
	}
	setcr3(oldcr3)
}

func ZeroblockinХУУДАСЛавлах(address uint32, хэмжээ uint32, хУУДАСЛавлах uint32) {
	if хэмжээ == 0 || хУУДАСЛавлах == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(хУУДАСЛавлах)
	makerangeprivatewritablecurrent(хУУДАСЛавлах, address, хэмжээ)
	destination_2 := GetБайтfrompointer(uintptr(address), int(хэмжээ), int(хэмжээ))
	for i := uint32(0); i < хэмжээ; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makeХУУДАСprivatewritablecurrent(хУУДАСЛавлах uint32, virtualaddress uint32) bool {
	pde := GetУтга(хУУДАСЛавлах + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & ХУУДАСpresent) == 0 {
		return false
	}
	pteaddress := (pde & ХУУДАСframe) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetУтга(pteaddress)
	if (pte & ХУУДАСpresent) == 0 {
		return false
	}
	if (pte & ХУУДАСcow) == 0 {
		return (pte & ХУУДАСwritable) != 0
	}
	if ИдэвхтэйСанахойЗохицуулагч == nil {
		return false
	}
	шинэpointer, _ := ИдэвхтэйСанахойЗохицуулагч.Alignedmalloc(0x1000)
	if шинэpointer == nil {
		return false
	}
	шинэframe := uint32(uintptr(шинэpointer)) & ХУУДАСframe
	эх_2 := GetБайтfrompointer(uintptr(virtualaddress&ХУУДАСframe), 0x1000, 0x1000)
	destination_2 := GetБайтfrompointer(uintptr(шинэframe), 0x1000, 0x1000)
	copy(destination_2, эх_2)
	cowframeЗохицуулагч.Decrement(pte & ХУУДАСframe)
	Setunsignedinteger32ataddress((шинэframe|(pte&0xFFF)|ХУУДАСwritable)&^ХУУДАСcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	ахиначаалахcr3()
	return true
}

func makerangeprivatewritablecurrent(хУУДАСЛавлах uint32, address uint32, хэмжээ uint32) bool {
	if хэмжээ == 0 {
		return true
	}
	last := address + хэмжээ - 1
	if last < address {
		return false
	}
	for хУУДАС := address & ХУУДАСframe; ; хУУДАС += 0x1000 {
		if !makeХУУДАСprivatewritablecurrent(хУУДАСЛавлах, хУУДАС) {
			return false
		}
		if хУУДАС == (last & ХУУДАСframe) {
			break
		}
	}
	return true
}

func Makerangeprivatewritable(хУУДАСЛавлах uint32, address uint32, хэмжээ uint32) bool {
	if хУУДАСЛавлах == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(хУУДАСЛавлах)
	ok := makerangeprivatewritablecurrent(хУУДАСЛавлах, address, хэмжээ)
	setcr3(oldcr3)
	return ok
}

func Setunsignedinteger32inХУУДАСЛавлах(x uint32, address uint32, хУУДАСЛавлах uint32) {
	if хУУДАСЛавлах == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(хУУДАСЛавлах)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func GetУтга(address uint32) uint32 {
	var orgУтга uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgУтга
}
func GetУтгаinХУУДАСЛавлах(address uint32, хУУДАСЛавлах uint32) uint32 {
	if хУУДАСЛавлах == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(хУУДАСЛавлах)
	v := GetУтга(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func ХуулахХУУДАСframeblock(xХУУДАСЛавлах uint32, yХУУДАСЛавлах uint32, vaddress uint32) {
	if xХУУДАСЛавлах == 0 || yХУУДАСЛавлах == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xХУУДАСЛавлах)
	v = GetУтга(vaddress)
	Setunsignedinteger32inХУУДАСЛавлах(v, vaddress, yХУУДАСЛавлах)

	setcr3(oldcr3)
}
