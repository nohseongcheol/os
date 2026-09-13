package paging

import unsafe "unsafe"
import . "ማቋረጫ"
import . "ማስታወሻmanager"
import . "util"

type Pገጽዳይሬክቶሪentry_2 uintptr

const (
	Pገጽአሁን		uint32	= 0x001
	Pገጽwritable	uint32	= 0x002
	Pገጽተጠቃሚ		uint32	= 0x004
	Pገጽክፈፍ		uint32	= 0xFFFFF000
	Pገጽcow		uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(ገጽዳይሬክቶሪ uint32)
func getcr3() uint32

type Paging struct {
	Tማቋረጫhandler
}
type Tcowክፈፍmanager struct {
	mem		*Tማስታወሻmanager
	refs		[]uint16
	ክፈፍcount	uint32
}

var (
	Pገጽዳይሬክቶሪentry	uintptr
	Pገጽሰንጠረዥentry	uint32
	pdelen		uint32
	virtlen		uint32
	cowክፈፍmanager	Tcowክፈፍmanager
)

func (self *Tcowክፈፍmanager) Init(mem *Tማስታወሻmanager, ክፈፍcount uint32) bool {
	self.mem = mem
	self.ክፈፍcount = ክፈፍcount
	referenceባይትስ := ክፈፍcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceጠቋሚ := mem.Malloc(referenceባይትስ)
	if referenceጠቋሚ == nil {
		self.refs = nil
		self.ክፈፍcount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceጠቋሚ)[:ክፈፍcount:ክፈፍcount]
	for i := uint32(0); i < ክፈፍcount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcowክፈፍmanager) Reference(ክፈፍ uint32) uint16 {
	idx := ክፈፍ >> 12
	if idx >= self.ክፈፍcount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcowክፈፍmanager) Increment(ክፈፍ uint32) {
	idx := ክፈፍ >> 12
	if idx >= self.ክፈፍcount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcowክፈፍmanager) Decrement(ክፈፍ uint32) {
	idx := ክፈፍ >> 12
	if idx >= self.ክፈፍcount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(ገጽዳይሬክቶሪentry uintptr, ገጽሰንጠረዥentry uint32, ማስታወሻmanager *Tማስታወሻmanager) {

	Pገጽዳይሬክቶሪentry = ገጽዳይሬክቶሪentry
	Pገጽሰንጠረዥentry = ገጽሰንጠረዥentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowክፈፍmanager.Init(ማስታወሻmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressጠቋሚ, _ := ማስታወሻmanager.Alignedmalloc(0x1000)
			if addressጠቋሚ == nil {
				return
			}
			address := uint32(uintptr(addressጠቋሚ))

			Setunsignedinteger32ataddress(address|0x87, uint32(ገጽዳይሬክቶሪentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		ገጽዳይሬክቶሪentry = ገጽዳይሬክቶሪentry + 0x1000
	}

}
func (self *Paging) Sharedማስታወሻregion() {

	ገጽዳይሬክቶሪentry := Pገጽዳይሬክቶሪentry
	kገጽዳይሬክቶሪentry := Pገጽዳይሬክቶሪentry

	for i := uint32(1); i <= virtlen; i++ {

		ገጽዳይሬክቶሪentry = ገጽዳይሬክቶሪentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Getዋጋ(uint32(kገጽዳይሬክቶሪentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(ገጽዳይሬክቶሪentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getዋጋ(uint32(kገጽዳይሬክቶሪentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(ገጽዳይሬክቶሪentry)+pde*4)

		}

	}
}
func (self *Paging) Pገጽfault(manager *Tማቋረጫmanager) {
	ማቋረጫhandler = handlepagingማቋረጫ

	var address uintptr
	address = uintptr(unsafe.Pointer(&ማቋረጫhandler))
	self.Tማቋረጫhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var ማቋረጫhandler func(uint32) uint32

func handlepagingማቋረጫ(esp uint32) uint32 {
	if Resolveኮፒማብሪያመጻፊያfault() {
		return esp
	}
	return Handlefatalማቋረጫክፈፍ(esp, 0x0E)
}

func Cloneaddressspacecow(ምንጩገጽዳይሬክቶሪ uint32) uint32 {
	if Aአሰራማስታወሻmanager == nil || ምንጩገጽዳይሬክቶሪ == 0 {
		return 0
	}
	destinationጠቋሚ, _ := Aአሰራማስታወሻmanager.Alignedmalloc(0x1000)
	if destinationጠቋሚ == nil {
		return 0
	}
	destinationገጽዳይሬክቶሪ := uint32(uintptr(destinationጠቋሚ))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationገጽዳይሬክቶሪ+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		ምንጩpdeaddress := ምንጩገጽዳይሬክቶሪ + pde*4
		ምንጩpde := Getዋጋ(ምንጩpdeaddress)
		if (ምንጩpde & Pገጽአሁን) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(ምንጩpde, destinationገጽዳይሬክቶሪ+pde*4)
			continue
		}

		destinationptጠቋሚ, _ := Aአሰራማስታወሻmanager.Alignedmalloc(0x1000)
		if destinationptጠቋሚ == nil {
			continue
		}
		ምንጩpt := ምንጩpde & Pገጽክፈፍ
		destinationpt := uint32(uintptr(destinationptጠቋሚ))
		Setunsignedinteger32ataddress((destinationpt | (ምንጩpde & 0xFFF)), destinationገጽዳይሬክቶሪ+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := ምንጩpt + pte*4
			entry := Getዋጋ(pteaddress)
			if (entry & Pገጽአሁን) != 0 {
				if (entry & Pገጽwritable) != 0 {
					entry = (entry &^ Pገጽwritable) | Pገጽcow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowክፈፍmanager.Increment(entry & Pገጽክፈፍ)
				} else if (entry & Pገጽcow) != 0 {
					cowክፈፍmanager.Increment(entry & Pገጽክፈፍ)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	እንደገናመጫኛcr3()
	return destinationገጽዳይሬክቶሪ
}

func Resolveኮፒማብሪያመጻፊያfault() bool {
	if Aአሰራማስታወሻmanager == nil {
		return false
	}
	faultaddress := getcr2()
	ገጽዳይሬክቶሪ := getcr3()
	pdeaddress := ገጽዳይሬክቶሪ + ((faultaddress>>22)&0x3FF)*4
	pde := Getዋጋ(pdeaddress)
	if (pde & Pገጽአሁን) == 0 {
		return false
	}
	pt := pde & Pገጽክፈፍ
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := Getዋጋ(pteaddress)
	if (pte&Pገጽcow) == 0 || (pte&Pገጽአሁን) == 0 {
		return false
	}
	oldክፈፍ := pte & Pገጽክፈፍ
	if cowክፈፍmanager.Reference(oldክፈፍ) <= 1 {
		Setunsignedinteger32ataddress((pte|Pገጽwritable)&^Pገጽcow, pteaddress)
		እንደገናመጫኛcr3()
		return true
	}

	አዲስጠቋሚ, _ := Aአሰራማስታወሻmanager.Alignedmalloc(0x1000)
	if አዲስጠቋሚ == nil {
		return false
	}
	አዲስክፈፍ := uint32(uintptr(አዲስጠቋሚ)) & Pገጽክፈፍ

	ምንጩ_2 := Getባይትስfromጠቋሚ(uintptr(faultaddress&Pገጽክፈፍ), 0x1000, 0x1000)
	destination_2 := Getባይትስfromጠቋሚ(uintptr(አዲስክፈፍ), 0x1000, 0x1000)
	copy(destination_2, ምንጩ_2)
	cowክፈፍmanager.Decrement(oldክፈፍ)
	Setunsignedinteger32ataddress((አዲስክፈፍ|(pte&0xFFF)|Pገጽwritable)&^Pገጽcow, pteaddress)
	እንደገናመጫኛcr3()
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

func እንደገናመጫኛcr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func Setbyteውስጥገጽዳይሬክቶሪ(x byte, address uint32, ገጽዳይሬክቶሪ uint32) {
	oldcr3 := getcr3()
	setcr3(ገጽዳይሬክቶሪ)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func Setመከልከያውስጥገጽዳይሬክቶሪ(ምንጩ_2 []byte, destination_2 []byte, መጠን uint32, ገጽዳይሬክቶሪ uint32) {
	if መጠን == 0 || ገጽዳይሬክቶሪ == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(ገጽዳይሬክቶሪ)
	makeመጠንprivatewritablecurrent(ገጽዳይሬክቶሪ, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), መጠን)

	for i := uint32(0); i < መጠን; i++ {
		destination_2[i] = ምንጩ_2[i]
	}
	setcr3(oldcr3)
}

func Zeroመከልከያውስጥገጽዳይሬክቶሪ(address uint32, መጠን uint32, ገጽዳይሬክቶሪ uint32) {
	if መጠን == 0 || ገጽዳይሬክቶሪ == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(ገጽዳይሬክቶሪ)
	makeመጠንprivatewritablecurrent(ገጽዳይሬክቶሪ, address, መጠን)
	destination_2 := Getባይትስfromጠቋሚ(uintptr(address), int(መጠን), int(መጠን))
	for i := uint32(0); i < መጠን; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makeገጽprivatewritablecurrent(ገጽዳይሬክቶሪ uint32, virtualaddress uint32) bool {
	pde := Getዋጋ(ገጽዳይሬክቶሪ + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & Pገጽአሁን) == 0 {
		return false
	}
	pteaddress := (pde & Pገጽክፈፍ) + ((virtualaddress>>12)&0x3FF)*4
	pte := Getዋጋ(pteaddress)
	if (pte & Pገጽአሁን) == 0 {
		return false
	}
	if (pte & Pገጽcow) == 0 {
		return (pte & Pገጽwritable) != 0
	}
	if Aአሰራማስታወሻmanager == nil {
		return false
	}
	አዲስጠቋሚ, _ := Aአሰራማስታወሻmanager.Alignedmalloc(0x1000)
	if አዲስጠቋሚ == nil {
		return false
	}
	አዲስክፈፍ := uint32(uintptr(አዲስጠቋሚ)) & Pገጽክፈፍ
	ምንጩ_2 := Getባይትስfromጠቋሚ(uintptr(virtualaddress&Pገጽክፈፍ), 0x1000, 0x1000)
	destination_2 := Getባይትስfromጠቋሚ(uintptr(አዲስክፈፍ), 0x1000, 0x1000)
	copy(destination_2, ምንጩ_2)
	cowክፈፍmanager.Decrement(pte & Pገጽክፈፍ)
	Setunsignedinteger32ataddress((አዲስክፈፍ|(pte&0xFFF)|Pገጽwritable)&^Pገጽcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	እንደገናመጫኛcr3()
	return true
}

func makeመጠንprivatewritablecurrent(ገጽዳይሬክቶሪ uint32, address uint32, መጠን uint32) bool {
	if መጠን == 0 {
		return true
	}
	last := address + መጠን - 1
	if last < address {
		return false
	}
	for ገጽ := address & Pገጽክፈፍ; ; ገጽ += 0x1000 {
		if !makeገጽprivatewritablecurrent(ገጽዳይሬክቶሪ, ገጽ) {
			return false
		}
		if ገጽ == (last & Pገጽክፈፍ) {
			break
		}
	}
	return true
}

func Makeመጠንprivatewritable(ገጽዳይሬክቶሪ uint32, address uint32, መጠን uint32) bool {
	if ገጽዳይሬክቶሪ == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(ገጽዳይሬክቶሪ)
	እሺ := makeመጠንprivatewritablecurrent(ገጽዳይሬክቶሪ, address, መጠን)
	setcr3(oldcr3)
	return እሺ
}

func Setunsignedinteger32ውስጥገጽዳይሬክቶሪ(x uint32, address uint32, ገጽዳይሬክቶሪ uint32) {
	if ገጽዳይሬክቶሪ == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(ገጽዳይሬክቶሪ)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func Getዋጋ(address uint32) uint32 {
	var orgዋጋ uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgዋጋ
}
func Getዋጋውስጥገጽዳይሬክቶሪ(address uint32, ገጽዳይሬክቶሪ uint32) uint32 {
	if ገጽዳይሬክቶሪ == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(ገጽዳይሬክቶሪ)
	v := Getዋጋ(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func Cኮፒገጽክፈፍመከልከያ(xገጽዳይሬክቶሪ uint32, yገጽዳይሬክቶሪ uint32, vaddress uint32) {
	if xገጽዳይሬክቶሪ == 0 || yገጽዳይሬክቶሪ == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xገጽዳይሬክቶሪ)
	v = Getዋጋ(vaddress)
	Setunsignedinteger32ውስጥገጽዳይሬክቶሪ(v, vaddress, yገጽዳይሬክቶሪ)

	setcr3(oldcr3)
}
