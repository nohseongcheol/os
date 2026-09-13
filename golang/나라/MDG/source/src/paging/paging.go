package paging

import unsafe "unsafe"
import . "interrupt"
import . "arikaMpandrindra"
import . "util"

type PEJYLahatahiryentry_2 uintptr

const (
	PEJYpresent	uint32	= 0x001
	PEJYwritable	uint32	= 0x002
	PEJYMpampiasa	uint32	= 0x004
	PEJYframe	uint32	= 0xFFFFF000
	PEJYcow		uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(pEJYLahatahiry uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowframeMpandrindra struct {
	mem		*TArikaMpandrindra
	refs		[]uint16
	framecount	uint32
}

var (
	PEJYLahatahiryentry	uintptr
	PEJYFafanaentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowframeMpandrindra	TcowframeMpandrindra
)

func (nytena *TcowframeMpandrindra) Init(mem *TArikaMpandrindra, framecount uint32) bool {
	nytena.mem = mem
	nytena.framecount = framecount
	referenceOctet := framecount * uint32(unsafe.Sizeof(uint16(0)))
	referencepointer := mem.Malloc(referenceOctet)
	if referencepointer == nil {
		nytena.refs = nil
		nytena.framecount = 0
		return false
	}
	nytena.refs = (*[1 << 28]uint16)(referencepointer)[:framecount:framecount]
	for i := uint32(0); i < framecount; i++ {
		nytena.refs[i] = 0
	}
	return true
}

func (nytena *TcowframeMpandrindra) Reference(frame uint32) uint16 {
	idx := frame >> 12
	if idx >= nytena.framecount || nytena.refs == nil {
		return 0
	}
	return nytena.refs[idx]
}

func (nytena *TcowframeMpandrindra) Increment(frame uint32) {
	idx := frame >> 12
	if idx >= nytena.framecount || nytena.refs == nil {
		return
	}
	if nytena.refs[idx] == 0 {
		nytena.refs[idx] = 2
	} else {
		nytena.refs[idx]++
	}
}

func (nytena *TcowframeMpandrindra) Decrement(frame uint32) {
	idx := frame >> 12
	if idx >= nytena.framecount || nytena.refs == nil || nytena.refs[idx] == 0 {
		return
	}
	nytena.refs[idx]--
}

func (nytena *Paging) Init(pEJYLahatahiryentry uintptr, pEJYFafanaentry uint32, arikaMpandrindra *TArikaMpandrindra) {

	PEJYLahatahiryentry = pEJYLahatahiryentry
	PEJYFafanaentry = pEJYFafanaentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframeMpandrindra.Init(arikaMpandrindra, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addresspointer, _ := arikaMpandrindra.Alignedmalloc(0x1000)
			if addresspointer == nil {
				return
			}
			address := uint32(uintptr(addresspointer))

			Setunsignedinteger32ataddress(address|0x87, uint32(pEJYLahatahiryentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		pEJYLahatahiryentry = pEJYLahatahiryentry + 0x1000
	}

}
func (nytena *Paging) SharedArikaregion() {

	pEJYLahatahiryentry := PEJYLahatahiryentry
	kPEJYLahatahiryentry := PEJYLahatahiryentry

	for i := uint32(1); i <= virtlen; i++ {

		pEJYLahatahiryentry = pEJYLahatahiryentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetSanda(uint32(kPEJYLahatahiryentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(pEJYLahatahiryentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetSanda(uint32(kPEJYLahatahiryentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(pEJYLahatahiryentry)+pde*4)

		}

	}
}
func (nytena *Paging) PEJYfault(mpandrindra *TInterruptMpandrindra) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	nytena.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(mpandrindra)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if ResolveAdikaoonManoratrafault() {
		return esp
	}
	return Handlefatalinterruptframe(esp, 0x0E)
}

func Cloneaddressspacecow(loharanoPEJYLahatahiry uint32) uint32 {
	if MiasaArikaMpandrindra == nil || loharanoPEJYLahatahiry == 0 {
		return 0
	}
	destinationpointer, _ := MiasaArikaMpandrindra.Alignedmalloc(0x1000)
	if destinationpointer == nil {
		return 0
	}
	destinationPEJYLahatahiry := uint32(uintptr(destinationpointer))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationPEJYLahatahiry+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		loharanopdeaddress := loharanoPEJYLahatahiry + pde*4
		loharanopde := GetSanda(loharanopdeaddress)
		if (loharanopde & PEJYpresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(loharanopde, destinationPEJYLahatahiry+pde*4)
			continue
		}

		destinationptpointer, _ := MiasaArikaMpandrindra.Alignedmalloc(0x1000)
		if destinationptpointer == nil {
			continue
		}
		loharanopt := loharanopde & PEJYframe
		destinationpt := uint32(uintptr(destinationptpointer))
		Setunsignedinteger32ataddress((destinationpt | (loharanopde & 0xFFF)), destinationPEJYLahatahiry+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := loharanopt + pte*4
			entry := GetSanda(pteaddress)
			if (entry & PEJYpresent) != 0 {
				if (entry & PEJYwritable) != 0 {
					entry = (entry &^ PEJYwritable) | PEJYcow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowframeMpandrindra.Increment(entry & PEJYframe)
				} else if (entry & PEJYcow) != 0 {
					cowframeMpandrindra.Increment(entry & PEJYframe)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	averenoasehocr3()
	return destinationPEJYLahatahiry
}

func ResolveAdikaoonManoratrafault() bool {
	if MiasaArikaMpandrindra == nil {
		return false
	}
	faultaddress := getcr2()
	pEJYLahatahiry := getcr3()
	pdeaddress := pEJYLahatahiry + ((faultaddress>>22)&0x3FF)*4
	pde := GetSanda(pdeaddress)
	if (pde & PEJYpresent) == 0 {
		return false
	}
	pt := pde & PEJYframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetSanda(pteaddress)
	if (pte&PEJYcow) == 0 || (pte&PEJYpresent) == 0 {
		return false
	}
	oldframe := pte & PEJYframe
	if cowframeMpandrindra.Reference(oldframe) <= 1 {
		Setunsignedinteger32ataddress((pte|PEJYwritable)&^PEJYcow, pteaddress)
		averenoasehocr3()
		return true
	}

	vaovaopointer, _ := MiasaArikaMpandrindra.Alignedmalloc(0x1000)
	if vaovaopointer == nil {
		return false
	}
	vaovaoframe := uint32(uintptr(vaovaopointer)) & PEJYframe

	loharano_2 := GetOctetfrompointer(uintptr(faultaddress&PEJYframe), 0x1000, 0x1000)
	destination_2 := GetOctetfrompointer(uintptr(vaovaoframe), 0x1000, 0x1000)
	copy(destination_2, loharano_2)
	cowframeMpandrindra.Decrement(oldframe)
	Setunsignedinteger32ataddress((vaovaoframe|(pte&0xFFF)|PEJYwritable)&^PEJYcow, pteaddress)
	averenoasehocr3()
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

func averenoasehocr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func SetbyteAnatyPEJYLahatahiry(x byte, address uint32, pEJYLahatahiry uint32) {
	oldcr3 := getcr3()
	setcr3(pEJYLahatahiry)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func SetblockAnatyPEJYLahatahiry(loharano_2 []byte, destination_2 []byte, habe uint32, pEJYLahatahiry uint32) {
	if habe == 0 || pEJYLahatahiry == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(pEJYLahatahiry)
	makeElanelanaprivatewritablecurrent(pEJYLahatahiry, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), habe)

	for i := uint32(0); i < habe; i++ {
		destination_2[i] = loharano_2[i]
	}
	setcr3(oldcr3)
}

func ZeroblockAnatyPEJYLahatahiry(address uint32, habe uint32, pEJYLahatahiry uint32) {
	if habe == 0 || pEJYLahatahiry == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(pEJYLahatahiry)
	makeElanelanaprivatewritablecurrent(pEJYLahatahiry, address, habe)
	destination_2 := GetOctetfrompointer(uintptr(address), int(habe), int(habe))
	for i := uint32(0); i < habe; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makePEJYprivatewritablecurrent(pEJYLahatahiry uint32, virtualaddress uint32) bool {
	pde := GetSanda(pEJYLahatahiry + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & PEJYpresent) == 0 {
		return false
	}
	pteaddress := (pde & PEJYframe) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetSanda(pteaddress)
	if (pte & PEJYpresent) == 0 {
		return false
	}
	if (pte & PEJYcow) == 0 {
		return (pte & PEJYwritable) != 0
	}
	if MiasaArikaMpandrindra == nil {
		return false
	}
	vaovaopointer, _ := MiasaArikaMpandrindra.Alignedmalloc(0x1000)
	if vaovaopointer == nil {
		return false
	}
	vaovaoframe := uint32(uintptr(vaovaopointer)) & PEJYframe
	loharano_2 := GetOctetfrompointer(uintptr(virtualaddress&PEJYframe), 0x1000, 0x1000)
	destination_2 := GetOctetfrompointer(uintptr(vaovaoframe), 0x1000, 0x1000)
	copy(destination_2, loharano_2)
	cowframeMpandrindra.Decrement(pte & PEJYframe)
	Setunsignedinteger32ataddress((vaovaoframe|(pte&0xFFF)|PEJYwritable)&^PEJYcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	averenoasehocr3()
	return true
}

func makeElanelanaprivatewritablecurrent(pEJYLahatahiry uint32, address uint32, habe uint32) bool {
	if habe == 0 {
		return true
	}
	last := address + habe - 1
	if last < address {
		return false
	}
	for pEJY := address & PEJYframe; ; pEJY += 0x1000 {
		if !makePEJYprivatewritablecurrent(pEJYLahatahiry, pEJY) {
			return false
		}
		if pEJY == (last & PEJYframe) {
			break
		}
	}
	return true
}

func MakeElanelanaprivatewritable(pEJYLahatahiry uint32, address uint32, habe uint32) bool {
	if pEJYLahatahiry == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(pEJYLahatahiry)
	ok := makeElanelanaprivatewritablecurrent(pEJYLahatahiry, address, habe)
	setcr3(oldcr3)
	return ok
}

func Setunsignedinteger32AnatyPEJYLahatahiry(x uint32, address uint32, pEJYLahatahiry uint32) {
	if pEJYLahatahiry == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(pEJYLahatahiry)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func GetSanda(address uint32) uint32 {
	var orgSanda uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgSanda
}
func GetSandaAnatyPEJYLahatahiry(address uint32, pEJYLahatahiry uint32) uint32 {
	if pEJYLahatahiry == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(pEJYLahatahiry)
	v := GetSanda(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func AdikaoPEJYframeblock(xPEJYLahatahiry uint32, yPEJYLahatahiry uint32, vaddress uint32) {
	if xPEJYLahatahiry == 0 || yPEJYLahatahiry == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xPEJYLahatahiry)
	v = GetSanda(vaddress)
	Setunsignedinteger32AnatyPEJYLahatahiry(v, vaddress, yPEJYLahatahiry)

	setcr3(oldcr3)
}
