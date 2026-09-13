package paging

import unsafe "unsafe"
import . "interrupt"
import . "მეხსიერებაmanager"
import . "util"

type Pგვერდიდასტაentry_2 uintptr

const (
	Pგვერდიpresent		uint32	= 0x001
	Pგვერდიwritable		uint32	= 0x002
	Pგვერდიმომხმარებელი	uint32	= 0x004
	Pგვერდიframe		uint32	= 0xFFFFF000
	Pგვერდიcow		uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(გვერდიდასტა uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type Tcowframemanager struct {
	mem		*Tმეხსიერებაmanager
	refs		[]uint16
	framecount	uint32
}

var (
	Pგვერდიდასტაentry	uintptr
	Pგვერდიცხრილიentry	uint32
	pdelen			uint32
	virtlen			uint32
	cowframemanager		Tcowframemanager
)

func (self *Tcowframemanager) Init(mem *Tმეხსიერებაmanager, framecount uint32) bool {
	self.mem = mem
	self.framecount = framecount
	referenceბაიტი := framecount * uint32(unsafe.Sizeof(uint16(0)))
	referenceკურსორი := mem.Malloc(referenceბაიტი)
	if referenceკურსორი == nil {
		self.refs = nil
		self.framecount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceკურსორი)[:framecount:framecount]
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

func (self *Paging) Init(გვერდიდასტაentry uintptr, გვერდიცხრილიentry uint32, მეხსიერებაmanager *Tმეხსიერებაmanager) {

	Pგვერდიდასტაentry = გვერდიდასტაentry
	Pგვერდიცხრილიentry = გვერდიცხრილიentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframemanager.Init(მეხსიერებაmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressკურსორი, _ := მეხსიერებაmanager.Alignedmalloc(0x1000)
			if addressკურსორი == nil {
				return
			}
			address := uint32(uintptr(addressკურსორი))

			Setunsignedinteger32ataddress(address|0x87, uint32(გვერდიდასტაentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		გვერდიდასტაentry = გვერდიდასტაentry + 0x1000
	}

}
func (self *Paging) Sharedმეხსიერებაregion() {

	გვერდიდასტაentry := Pგვერდიდასტაentry
	kგვერდიდასტაentry := Pგვერდიდასტაentry

	for i := uint32(1); i <= virtlen; i++ {

		გვერდიდასტაentry = გვერდიდასტაentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Getმნიშვნელობა(uint32(kგვერდიდასტაentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(გვერდიდასტაentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getმნიშვნელობა(uint32(kგვერდიდასტაentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(გვერდიდასტაentry)+pde*4)

		}

	}
}
func (self *Paging) Pგვერდიfault(manager *TInterruptmanager) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if Resolveდააკოპირეonჩაწერაfault() {
		return esp
	}
	return Handlefatalinterruptframe(esp, 0x0E)
}

func Cloneaddressspacecow(წყაროგვერდიდასტა uint32) uint32 {
	if Aაქტიურიმეხსიერებაmanager == nil || წყაროგვერდიდასტა == 0 {
		return 0
	}
	destinationკურსორი, _ := Aაქტიურიმეხსიერებაmanager.Alignedmalloc(0x1000)
	if destinationკურსორი == nil {
		return 0
	}
	destinationგვერდიდასტა := uint32(uintptr(destinationკურსორი))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationგვერდიდასტა+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		წყაროpdeaddress := წყაროგვერდიდასტა + pde*4
		წყაროpde := Getმნიშვნელობა(წყაროpdeaddress)
		if (წყაროpde & Pგვერდიpresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(წყაროpde, destinationგვერდიდასტა+pde*4)
			continue
		}

		destinationptკურსორი, _ := Aაქტიურიმეხსიერებაmanager.Alignedmalloc(0x1000)
		if destinationptკურსორი == nil {
			continue
		}
		წყაროpt := წყაროpde & Pგვერდიframe
		destinationpt := uint32(uintptr(destinationptკურსორი))
		Setunsignedinteger32ataddress((destinationpt | (წყაროpde & 0xFFF)), destinationგვერდიდასტა+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := წყაროpt + pte*4
			entry := Getმნიშვნელობა(pteaddress)
			if (entry & Pგვერდიpresent) != 0 {
				if (entry & Pგვერდიwritable) != 0 {
					entry = (entry &^ Pგვერდიwritable) | Pგვერდიcow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowframemanager.Increment(entry & Pგვერდიframe)
				} else if (entry & Pგვერდიcow) != 0 {
					cowframemanager.Increment(entry & Pგვერდიframe)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	გადატვირთვაcr3()
	return destinationგვერდიდასტა
}

func Resolveდააკოპირეonჩაწერაfault() bool {
	if Aაქტიურიმეხსიერებაmanager == nil {
		return false
	}
	faultaddress := getcr2()
	გვერდიდასტა := getcr3()
	pdeaddress := გვერდიდასტა + ((faultaddress>>22)&0x3FF)*4
	pde := Getმნიშვნელობა(pdeaddress)
	if (pde & Pგვერდიpresent) == 0 {
		return false
	}
	pt := pde & Pგვერდიframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := Getმნიშვნელობა(pteaddress)
	if (pte&Pგვერდიcow) == 0 || (pte&Pგვერდიpresent) == 0 {
		return false
	}
	oldframe := pte & Pგვერდიframe
	if cowframemanager.Reference(oldframe) <= 1 {
		Setunsignedinteger32ataddress((pte|Pგვერდიwritable)&^Pგვერდიcow, pteaddress)
		გადატვირთვაcr3()
		return true
	}

	ახალიკურსორი, _ := Aაქტიურიმეხსიერებაmanager.Alignedmalloc(0x1000)
	if ახალიკურსორი == nil {
		return false
	}
	ახალიframe := uint32(uintptr(ახალიკურსორი)) & Pგვერდიframe

	წყარო_2 := Getბაიტიfromკურსორი(uintptr(faultaddress&Pგვერდიframe), 0x1000, 0x1000)
	destination_2 := Getბაიტიfromკურსორი(uintptr(ახალიframe), 0x1000, 0x1000)
	copy(destination_2, წყარო_2)
	cowframemanager.Decrement(oldframe)
	Setunsignedinteger32ataddress((ახალიframe|(pte&0xFFF)|Pგვერდიwritable)&^Pგვერდიcow, pteaddress)
	გადატვირთვაcr3()
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

func გადატვირთვაcr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func Setbyteგადიდებაგვერდიდასტა(x byte, address uint32, გვერდიდასტა uint32) {
	oldcr3 := getcr3()
	setcr3(გვერდიდასტა)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func Setblockგადიდებაგვერდიდასტა(წყარო_2 []byte, destination_2 []byte, ზომა uint32, გვერდიდასტა uint32) {
	if ზომა == 0 || გვერდიდასტა == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(გვერდიდასტა)
	makerangeprivatewritablecurrent(გვერდიდასტა, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), ზომა)

	for i := uint32(0); i < ზომა; i++ {
		destination_2[i] = წყარო_2[i]
	}
	setcr3(oldcr3)
}

func Zeroblockგადიდებაგვერდიდასტა(address uint32, ზომა uint32, გვერდიდასტა uint32) {
	if ზომა == 0 || გვერდიდასტა == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(გვერდიდასტა)
	makerangeprivatewritablecurrent(გვერდიდასტა, address, ზომა)
	destination_2 := Getბაიტიfromკურსორი(uintptr(address), int(ზომა), int(ზომა))
	for i := uint32(0); i < ზომა; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makeგვერდიprivatewritablecurrent(გვერდიდასტა uint32, virtualaddress uint32) bool {
	pde := Getმნიშვნელობა(გვერდიდასტა + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & Pგვერდიpresent) == 0 {
		return false
	}
	pteaddress := (pde & Pგვერდიframe) + ((virtualaddress>>12)&0x3FF)*4
	pte := Getმნიშვნელობა(pteaddress)
	if (pte & Pგვერდიpresent) == 0 {
		return false
	}
	if (pte & Pგვერდიcow) == 0 {
		return (pte & Pგვერდიwritable) != 0
	}
	if Aაქტიურიმეხსიერებაmanager == nil {
		return false
	}
	ახალიკურსორი, _ := Aაქტიურიმეხსიერებაmanager.Alignedmalloc(0x1000)
	if ახალიკურსორი == nil {
		return false
	}
	ახალიframe := uint32(uintptr(ახალიკურსორი)) & Pგვერდიframe
	წყარო_2 := Getბაიტიfromკურსორი(uintptr(virtualaddress&Pგვერდიframe), 0x1000, 0x1000)
	destination_2 := Getბაიტიfromკურსორი(uintptr(ახალიframe), 0x1000, 0x1000)
	copy(destination_2, წყარო_2)
	cowframemanager.Decrement(pte & Pგვერდიframe)
	Setunsignedinteger32ataddress((ახალიframe|(pte&0xFFF)|Pგვერდიwritable)&^Pგვერდიcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	გადატვირთვაcr3()
	return true
}

func makerangeprivatewritablecurrent(გვერდიდასტა uint32, address uint32, ზომა uint32) bool {
	if ზომა == 0 {
		return true
	}
	last := address + ზომა - 1
	if last < address {
		return false
	}
	for გვერდი := address & Pგვერდიframe; ; გვერდი += 0x1000 {
		if !makeგვერდიprivatewritablecurrent(გვერდიდასტა, გვერდი) {
			return false
		}
		if გვერდი == (last & Pგვერდიframe) {
			break
		}
	}
	return true
}

func Makerangeprivatewritable(გვერდიდასტა uint32, address uint32, ზომა uint32) bool {
	if გვერდიდასტა == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(გვერდიდასტა)
	ok := makerangeprivatewritablecurrent(გვერდიდასტა, address, ზომა)
	setcr3(oldcr3)
	return ok
}

func Setunsignedinteger32გადიდებაგვერდიდასტა(x uint32, address uint32, გვერდიდასტა uint32) {
	if გვერდიდასტა == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(გვერდიდასტა)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func Getმნიშვნელობა(address uint32) uint32 {
	var orgმნიშვნელობა uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgმნიშვნელობა
}
func Getმნიშვნელობაგადიდებაგვერდიდასტა(address uint32, გვერდიდასტა uint32) uint32 {
	if გვერდიდასტა == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(გვერდიდასტა)
	v := Getმნიშვნელობა(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func Cდააკოპირეგვერდიframeblock(xგვერდიდასტა uint32, yგვერდიდასტა uint32, vaddress uint32) {
	if xგვერდიდასტა == 0 || yგვერდიდასტა == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xგვერდიდასტა)
	v = Getმნიშვნელობა(vaddress)
	Setunsignedinteger32გადიდებაგვერდიდასტა(v, vaddress, yგვერდიდასტა)

	setcr3(oldcr3)
}
