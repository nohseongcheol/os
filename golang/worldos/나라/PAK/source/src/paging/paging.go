/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "مداخلت"
import . "یادداشتmanager"
import . "util"

type Pصفحہڈائریکٹریentry_2 uintptr

const (
	Pصفحہموجود	uint32	= 0x001
	Pصفحہwritable	uint32	= 0x002
	Pصفحہصارف	uint32	= 0x004
	Pصفحہframe	uint32	= 0xFFFFF000
	Pصفحہcow	uint32	= 0x200
)

func Sسیٹbyteataddress(x byte, address uint32)
func Sسیٹunsignedinteger8ataddress(x uint8, address uint32)
func Sسیٹunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func سیٹcr3(صفحہڈائریکٹری uint32)
func getcr3() uint32

type Paging struct {
	Tمداخلتhandler
}
type Tcowframemanager struct {
	mem		*Tیادداشتmanager
	refs		[]uint16
	framecount	uint32
}

var (
	Pصفحہڈائریکٹریentry	uintptr
	Pصفحہجدولentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowframemanager		Tcowframemanager
)

func (self *Tcowframemanager) Init(mem *Tیادداشتmanager, framecount uint32) bool {
	self.mem = mem
	self.framecount = framecount
	referenceبائٹس := framecount * uint32(unsafe.Sizeof(uint16(0)))
	referenceپؤائنٹر := mem.Malloc(referenceبائٹس)
	if referenceپؤائنٹر == nil {
		self.refs = nil
		self.framecount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceپؤائنٹر)[:framecount:framecount]
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

func (self *Paging) Init(صفحہڈائریکٹریentry uintptr, صفحہجدولentry uint32, یادداشتmanager *Tیادداشتmanager) {

	Pصفحہڈائریکٹریentry = صفحہڈائریکٹریentry
	Pصفحہجدولentry = صفحہجدولentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframemanager.Init(یادداشتmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressپؤائنٹر, _ := یادداشتmanager.Alignedmalloc(0x1000)
			if addressپؤائنٹر == nil {
				return
			}
			address := uint32(uintptr(addressپؤائنٹر))

			Sسیٹunsignedinteger32ataddress(address|0x87, uint32(صفحہڈائریکٹریentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Sسیٹunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		صفحہڈائریکٹریentry = صفحہڈائریکٹریentry + 0x1000
	}

}
func (self *Paging) Sharedیادداشتregion() {

	صفحہڈائریکٹریentry := Pصفحہڈائریکٹریentry
	kصفحہڈائریکٹریentry := Pصفحہڈائریکٹریentry

	for i := uint32(1); i <= virtlen; i++ {

		صفحہڈائریکٹریentry = صفحہڈائریکٹریentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Getقدر(uint32(kصفحہڈائریکٹریentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sسیٹunsignedinteger32ataddress(v|0x87, uint32(صفحہڈائریکٹریentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getقدر(uint32(kصفحہڈائریکٹریentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sسیٹunsignedinteger32ataddress(v|0x87, uint32(صفحہڈائریکٹریentry)+pde*4)

		}

	}
}
func (self *Paging) Pصفحہfault(manager *Tمداخلتmanager) {
	مداخلتhandler = handlepagingمداخلت

	var address uintptr
	address = uintptr(unsafe.Pointer(&مداخلتhandler))
	self.Tمداخلتhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var مداخلتhandler func(uint32) uint32

func handlepagingمداخلت(esp uint32) uint32 {
	if Resolveکاپیچالولکھیںfault() {
		return esp
	}
	return Handlefatalمداخلتframe(esp, 0x0E)
}

func Cloneaddressspacecow(مصدرصفحہڈائریکٹری uint32) uint32 {
	if Aفعالیادداشتmanager == nil || مصدرصفحہڈائریکٹری == 0 {
		return 0
	}
	destinationپؤائنٹر, _ := Aفعالیادداشتmanager.Alignedmalloc(0x1000)
	if destinationپؤائنٹر == nil {
		return 0
	}
	destinationصفحہڈائریکٹری := uint32(uintptr(destinationپؤائنٹر))
	for i := uint32(0); i < 1024; i++ {
		Sسیٹunsignedinteger32ataddress(0, destinationصفحہڈائریکٹری+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		مصدرpdeaddress := مصدرصفحہڈائریکٹری + pde*4
		مصدرpde := Getقدر(مصدرpdeaddress)
		if (مصدرpde & Pصفحہموجود) == 0 {
			continue
		}
		if issharedpde(pde) {
			Sسیٹunsignedinteger32ataddress(مصدرpde, destinationصفحہڈائریکٹری+pde*4)
			continue
		}

		destinationptپؤائنٹر, _ := Aفعالیادداشتmanager.Alignedmalloc(0x1000)
		if destinationptپؤائنٹر == nil {
			continue
		}
		مصدرpt := مصدرpde & Pصفحہframe
		destinationpt := uint32(uintptr(destinationptپؤائنٹر))
		Sسیٹunsignedinteger32ataddress((destinationpt | (مصدرpde & 0xFFF)), destinationصفحہڈائریکٹری+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := مصدرpt + pte*4
			entry := Getقدر(pteaddress)
			if (entry & Pصفحہموجود) != 0 {
				if (entry & Pصفحہwritable) != 0 {
					entry = (entry &^ Pصفحہwritable) | Pصفحہcow
					Sسیٹunsignedinteger32ataddress(entry, pteaddress)
					cowframemanager.Increment(entry & Pصفحہframe)
				} else if (entry & Pصفحہcow) != 0 {
					cowframemanager.Increment(entry & Pصفحہframe)
				}
			}
			Sسیٹunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	دوبارہلادیںcr3()
	return destinationصفحہڈائریکٹری
}

func Resolveکاپیچالولکھیںfault() bool {
	if Aفعالیادداشتmanager == nil {
		return false
	}
	faultaddress := getcr2()
	صفحہڈائریکٹری := getcr3()
	pdeaddress := صفحہڈائریکٹری + ((faultaddress>>22)&0x3FF)*4
	pde := Getقدر(pdeaddress)
	if (pde & Pصفحہموجود) == 0 {
		return false
	}
	pt := pde & Pصفحہframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := Getقدر(pteaddress)
	if (pte&Pصفحہcow) == 0 || (pte&Pصفحہموجود) == 0 {
		return false
	}
	oldframe := pte & Pصفحہframe
	if cowframemanager.Reference(oldframe) <= 1 {
		Sسیٹunsignedinteger32ataddress((pte|Pصفحہwritable)&^Pصفحہcow, pteaddress)
		دوبارہلادیںcr3()
		return true
	}

	نیاپؤائنٹر, _ := Aفعالیادداشتmanager.Alignedmalloc(0x1000)
	if نیاپؤائنٹر == nil {
		return false
	}
	نیاframe := uint32(uintptr(نیاپؤائنٹر)) & Pصفحہframe

	مصدر_2 := Getبائٹسfromپؤائنٹر(uintptr(faultaddress&Pصفحہframe), 0x1000, 0x1000)
	destination_2 := Getبائٹسfromپؤائنٹر(uintptr(نیاframe), 0x1000, 0x1000)
	copy(destination_2, مصدر_2)
	cowframemanager.Decrement(oldframe)
	Sسیٹunsignedinteger32ataddress((نیاframe|(pte&0xFFF)|Pصفحہwritable)&^Pصفحہcow, pteaddress)
	دوبارہلادیںcr3()
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

func دوبارہلادیںcr3() {
	cr3 := getcr3()
	سیٹcr3(cr3)
}

func Sسیٹbyteاندرصفحہڈائریکٹری(x byte, address uint32, صفحہڈائریکٹری uint32) {
	oldcr3 := getcr3()
	سیٹcr3(صفحہڈائریکٹری)
	Sسیٹbyteataddress(x, address)
	سیٹcr3(oldcr3)
}

func Sسیٹblockاندرصفحہڈائریکٹری(مصدر_2 []byte, destination_2 []byte, حجم uint32, صفحہڈائریکٹری uint32) {
	if حجم == 0 || صفحہڈائریکٹری == 0 {
		return
	}
	oldcr3 := getcr3()
	سیٹcr3(صفحہڈائریکٹری)
	makerangeprivatewritableحالیہ(صفحہڈائریکٹری, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), حجم)

	for i := uint32(0); i < حجم; i++ {
		destination_2[i] = مصدر_2[i]
	}
	سیٹcr3(oldcr3)
}

func Zeroblockاندرصفحہڈائریکٹری(address uint32, حجم uint32, صفحہڈائریکٹری uint32) {
	if حجم == 0 || صفحہڈائریکٹری == 0 {
		return
	}
	oldcr3 := getcr3()
	سیٹcr3(صفحہڈائریکٹری)
	makerangeprivatewritableحالیہ(صفحہڈائریکٹری, address, حجم)
	destination_2 := Getبائٹسfromپؤائنٹر(uintptr(address), int(حجم), int(حجم))
	for i := uint32(0); i < حجم; i++ {
		destination_2[i] = 0
	}
	سیٹcr3(oldcr3)
}

func makeصفحہprivatewritableحالیہ(صفحہڈائریکٹری uint32, virtualaddress uint32) bool {
	pde := Getقدر(صفحہڈائریکٹری + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & Pصفحہموجود) == 0 {
		return false
	}
	pteaddress := (pde & Pصفحہframe) + ((virtualaddress>>12)&0x3FF)*4
	pte := Getقدر(pteaddress)
	if (pte & Pصفحہموجود) == 0 {
		return false
	}
	if (pte & Pصفحہcow) == 0 {
		return (pte & Pصفحہwritable) != 0
	}
	if Aفعالیادداشتmanager == nil {
		return false
	}
	نیاپؤائنٹر, _ := Aفعالیادداشتmanager.Alignedmalloc(0x1000)
	if نیاپؤائنٹر == nil {
		return false
	}
	نیاframe := uint32(uintptr(نیاپؤائنٹر)) & Pصفحہframe
	مصدر_2 := Getبائٹسfromپؤائنٹر(uintptr(virtualaddress&Pصفحہframe), 0x1000, 0x1000)
	destination_2 := Getبائٹسfromپؤائنٹر(uintptr(نیاframe), 0x1000, 0x1000)
	copy(destination_2, مصدر_2)
	cowframemanager.Decrement(pte & Pصفحہframe)
	Sسیٹunsignedinteger32ataddress((نیاframe|(pte&0xFFF)|Pصفحہwritable)&^Pصفحہcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	دوبارہلادیںcr3()
	return true
}

func makerangeprivatewritableحالیہ(صفحہڈائریکٹری uint32, address uint32, حجم uint32) bool {
	if حجم == 0 {
		return true
	}
	last := address + حجم - 1
	if last < address {
		return false
	}
	for صفحہ := address & Pصفحہframe; ; صفحہ += 0x1000 {
		if !makeصفحہprivatewritableحالیہ(صفحہڈائریکٹری, صفحہ) {
			return false
		}
		if صفحہ == (last & Pصفحہframe) {
			break
		}
	}
	return true
}

func Makerangeprivatewritable(صفحہڈائریکٹری uint32, address uint32, حجم uint32) bool {
	if صفحہڈائریکٹری == 0 {
		return false
	}
	oldcr3 := getcr3()
	سیٹcr3(صفحہڈائریکٹری)
	ok := makerangeprivatewritableحالیہ(صفحہڈائریکٹری, address, حجم)
	سیٹcr3(oldcr3)
	return ok
}

func Sسیٹunsignedinteger32اندرصفحہڈائریکٹری(x uint32, address uint32, صفحہڈائریکٹری uint32) {
	if صفحہڈائریکٹری == 0 {
		return
	}
	oldcr3 := getcr3()
	سیٹcr3(صفحہڈائریکٹری)
	Sسیٹunsignedinteger32ataddress(x, address)
	سیٹcr3(oldcr3)
}

func Getقدر(address uint32) uint32 {
	var orgقدر uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgقدر
}
func Getقدراندرصفحہڈائریکٹری(address uint32, صفحہڈائریکٹری uint32) uint32 {
	if صفحہڈائریکٹری == 0 {
		return 0
	}
	oldcr3 := getcr3()
	سیٹcr3(صفحہڈائریکٹری)
	v := Getقدر(address)
	سیٹcr3(oldcr3)
	return v
}

var v uint32 = 0

func Cکاپیصفحہframeblock(xصفحہڈائریکٹری uint32, yصفحہڈائریکٹری uint32, vaddress uint32) {
	if xصفحہڈائریکٹری == 0 || yصفحہڈائریکٹری == 0 {
		return
	}
	oldcr3 := getcr3()
	سیٹcr3(xصفحہڈائریکٹری)
	v = Getقدر(vaddress)
	Sسیٹunsignedinteger32اندرصفحہڈائریکٹری(v, vaddress, yصفحہڈائریکٹری)

	سیٹcr3(oldcr3)
}
