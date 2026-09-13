package paging

import unsafe "unsafe"
import . "interrupt"
import . "xotiramanager"
import . "util"

type SAHIFAJildentry_2 uintptr

const (
	SAHIFApresent		uint32	= 0x001
	SAHIFAwritable		uint32	= 0x002
	SAHIFAFoydalanuvchi	uint32	= 0x004
	SAHIFARamka		uint32	= 0xFFFFF000
	SAHIFAcow		uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(sAHIFAJild uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowRamkamanager struct {
	mem		*TXotiramanager
	refs		[]uint16
	ramkacount	uint32
}

var (
	SAHIFAJildentry		uintptr
	SAHIFAtableentry	uint32
	pdelen			uint32
	virtlen			uint32
	cowRamkamanager		TcowRamkamanager
)

func (self *TcowRamkamanager) Init(mem *TXotiramanager, ramkacount uint32) bool {
	self.mem = mem
	self.ramkacount = ramkacount
	referenceBaytlar := ramkacount * uint32(unsafe.Sizeof(uint16(0)))
	referenceKorsatgich := mem.Malloc(referenceBaytlar)
	if referenceKorsatgich == nil {
		self.refs = nil
		self.ramkacount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceKorsatgich)[:ramkacount:ramkacount]
	for i := uint32(0); i < ramkacount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TcowRamkamanager) Reference(ramka uint32) uint16 {
	idx := ramka >> 12
	if idx >= self.ramkacount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowRamkamanager) Increment(ramka uint32) {
	idx := ramka >> 12
	if idx >= self.ramkacount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TcowRamkamanager) Decrement(ramka uint32) {
	idx := ramka >> 12
	if idx >= self.ramkacount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(sAHIFAJildentry uintptr, sAHIFAtableentry uint32, xotiramanager *TXotiramanager) {

	SAHIFAJildentry = sAHIFAJildentry
	SAHIFAtableentry = sAHIFAtableentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRamkamanager.Init(xotiramanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressKorsatgich, _ := xotiramanager.Alignedmalloc(0x1000)
			if addressKorsatgich == nil {
				return
			}
			address := uint32(uintptr(addressKorsatgich))

			Setunsignedinteger32ataddress(address|0x87, uint32(sAHIFAJildentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		sAHIFAJildentry = sAHIFAJildentry + 0x1000
	}

}
func (self *Paging) SharedXotiraregion() {

	sAHIFAJildentry := SAHIFAJildentry
	kSAHIFAJildentry := SAHIFAJildentry

	for i := uint32(1); i <= virtlen; i++ {

		sAHIFAJildentry = sAHIFAJildentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetQiymat(uint32(kSAHIFAJildentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(sAHIFAJildentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetQiymat(uint32(kSAHIFAJildentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(sAHIFAJildentry)+pde*4)

		}

	}
}
func (self *Paging) SAHIFAfault(manager *TInterruptmanager) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if ResolveNusxaolishYoqishYozishfault() {
		return esp
	}
	return HandlefatalinterruptRamka(esp, 0x0E)
}

func CloneaddressBoʻshjoycow(sourceSAHIFAJild uint32) uint32 {
	if FaolXotiramanager == nil || sourceSAHIFAJild == 0 {
		return 0
	}
	destinationKorsatgich, _ := FaolXotiramanager.Alignedmalloc(0x1000)
	if destinationKorsatgich == nil {
		return 0
	}
	destinationSAHIFAJild := uint32(uintptr(destinationKorsatgich))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationSAHIFAJild+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		sourcepdeaddress := sourceSAHIFAJild + pde*4
		sourcepde := GetQiymat(sourcepdeaddress)
		if (sourcepde & SAHIFApresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(sourcepde, destinationSAHIFAJild+pde*4)
			continue
		}

		destinationptKorsatgich, _ := FaolXotiramanager.Alignedmalloc(0x1000)
		if destinationptKorsatgich == nil {
			continue
		}
		sourcept := sourcepde & SAHIFARamka
		destinationpt := uint32(uintptr(destinationptKorsatgich))
		Setunsignedinteger32ataddress((destinationpt | (sourcepde & 0xFFF)), destinationSAHIFAJild+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := sourcept + pte*4
			entry := GetQiymat(pteaddress)
			if (entry & SAHIFApresent) != 0 {
				if (entry & SAHIFAwritable) != 0 {
					entry = (entry &^ SAHIFAwritable) | SAHIFAcow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowRamkamanager.Increment(entry & SAHIFARamka)
				} else if (entry & SAHIFAcow) != 0 {
					cowRamkamanager.Increment(entry & SAHIFARamka)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	qaytayuklashcr3()
	return destinationSAHIFAJild
}

func ResolveNusxaolishYoqishYozishfault() bool {
	if FaolXotiramanager == nil {
		return false
	}
	faultaddress := getcr2()
	sAHIFAJild := getcr3()
	pdeaddress := sAHIFAJild + ((faultaddress>>22)&0x3FF)*4
	pde := GetQiymat(pdeaddress)
	if (pde & SAHIFApresent) == 0 {
		return false
	}
	pt := pde & SAHIFARamka
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetQiymat(pteaddress)
	if (pte&SAHIFAcow) == 0 || (pte&SAHIFApresent) == 0 {
		return false
	}
	oldRamka := pte & SAHIFARamka
	if cowRamkamanager.Reference(oldRamka) <= 1 {
		Setunsignedinteger32ataddress((pte|SAHIFAwritable)&^SAHIFAcow, pteaddress)
		qaytayuklashcr3()
		return true
	}

	yangiKorsatgich, _ := FaolXotiramanager.Alignedmalloc(0x1000)
	if yangiKorsatgich == nil {
		return false
	}
	yangiRamka := uint32(uintptr(yangiKorsatgich)) & SAHIFARamka

	source_2 := GetBaytlarfromKorsatgich(uintptr(faultaddress&SAHIFARamka), 0x1000, 0x1000)
	destination_2 := GetBaytlarfromKorsatgich(uintptr(yangiRamka), 0x1000, 0x1000)
	copy(destination_2, source_2)
	cowRamkamanager.Decrement(oldRamka)
	Setunsignedinteger32ataddress((yangiRamka|(pte&0xFFF)|SAHIFAwritable)&^SAHIFAcow, pteaddress)
	qaytayuklashcr3()
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

func qaytayuklashcr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func SetbyteYaqinlashtirishSAHIFAJild(x byte, address uint32, sAHIFAJild uint32) {
	oldcr3 := getcr3()
	setcr3(sAHIFAJild)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func SetBlokYaqinlashtirishSAHIFAJild(source_2 []byte, destination_2 []byte, hajmi uint32, sAHIFAJild uint32) {
	if hajmi == 0 || sAHIFAJild == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(sAHIFAJild)
	makerangeprivatewritablecurrent(sAHIFAJild, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), hajmi)

	for i := uint32(0); i < hajmi; i++ {
		destination_2[i] = source_2[i]
	}
	setcr3(oldcr3)
}

func ZeroBlokYaqinlashtirishSAHIFAJild(address uint32, hajmi uint32, sAHIFAJild uint32) {
	if hajmi == 0 || sAHIFAJild == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(sAHIFAJild)
	makerangeprivatewritablecurrent(sAHIFAJild, address, hajmi)
	destination_2 := GetBaytlarfromKorsatgich(uintptr(address), int(hajmi), int(hajmi))
	for i := uint32(0); i < hajmi; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makeSAHIFAprivatewritablecurrent(sAHIFAJild uint32, virtualaddress uint32) bool {
	pde := GetQiymat(sAHIFAJild + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & SAHIFApresent) == 0 {
		return false
	}
	pteaddress := (pde & SAHIFARamka) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetQiymat(pteaddress)
	if (pte & SAHIFApresent) == 0 {
		return false
	}
	if (pte & SAHIFAcow) == 0 {
		return (pte & SAHIFAwritable) != 0
	}
	if FaolXotiramanager == nil {
		return false
	}
	yangiKorsatgich, _ := FaolXotiramanager.Alignedmalloc(0x1000)
	if yangiKorsatgich == nil {
		return false
	}
	yangiRamka := uint32(uintptr(yangiKorsatgich)) & SAHIFARamka
	source_2 := GetBaytlarfromKorsatgich(uintptr(virtualaddress&SAHIFARamka), 0x1000, 0x1000)
	destination_2 := GetBaytlarfromKorsatgich(uintptr(yangiRamka), 0x1000, 0x1000)
	copy(destination_2, source_2)
	cowRamkamanager.Decrement(pte & SAHIFARamka)
	Setunsignedinteger32ataddress((yangiRamka|(pte&0xFFF)|SAHIFAwritable)&^SAHIFAcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	qaytayuklashcr3()
	return true
}

func makerangeprivatewritablecurrent(sAHIFAJild uint32, address uint32, hajmi uint32) bool {
	if hajmi == 0 {
		return true
	}
	last := address + hajmi - 1
	if last < address {
		return false
	}
	for sAHIFA := address & SAHIFARamka; ; sAHIFA += 0x1000 {
		if !makeSAHIFAprivatewritablecurrent(sAHIFAJild, sAHIFA) {
			return false
		}
		if sAHIFA == (last & SAHIFARamka) {
			break
		}
	}
	return true
}

func Makerangeprivatewritable(sAHIFAJild uint32, address uint32, hajmi uint32) bool {
	if sAHIFAJild == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(sAHIFAJild)
	ok := makerangeprivatewritablecurrent(sAHIFAJild, address, hajmi)
	setcr3(oldcr3)
	return ok
}

func Setunsignedinteger32YaqinlashtirishSAHIFAJild(x uint32, address uint32, sAHIFAJild uint32) {
	if sAHIFAJild == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(sAHIFAJild)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func GetQiymat(address uint32) uint32 {
	var orgQiymat uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgQiymat
}
func GetQiymatYaqinlashtirishSAHIFAJild(address uint32, sAHIFAJild uint32) uint32 {
	if sAHIFAJild == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(sAHIFAJild)
	v := GetQiymat(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func NusxaolishSAHIFARamkaBlok(xSAHIFAJild uint32, ySAHIFAJild uint32, vaddress uint32) {
	if xSAHIFAJild == 0 || ySAHIFAJild == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xSAHIFAJild)
	v = GetQiymat(vaddress)
	Setunsignedinteger32YaqinlashtirishSAHIFAJild(v, vaddress, ySAHIFAJild)

	setcr3(oldcr3)
}
