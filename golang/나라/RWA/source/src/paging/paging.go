package paging

import unsafe "unsafe"
import . "interrupt"
import . "ububikomanager"
import . "util"

type IpajiUbubikoentry_2 uintptr

const (
	Ipajipresent	uint32	= 0x001
	Ipajiwritable	uint32	= 0x002
	IpajiUkoresha	uint32	= 0x004
	IpajiIkadiri	uint32	= 0xFFFFF000
	Ipajicow	uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(ipajiUbubiko uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowIkadirimanager struct {
	mem		*TUbubikomanager
	refs		[]uint16
	ikadiricount	uint32
}

var (
	IpajiUbubikoentry	uintptr
	IpajiImbonerahamweentry	uint32
	pdelen			uint32
	virtlen			uint32
	cowIkadirimanager	TcowIkadirimanager
)

func (self *TcowIkadirimanager) Init(mem *TUbubikomanager, ikadiricount uint32) bool {
	self.mem = mem
	self.ikadiricount = ikadiricount
	referenceBayite := ikadiricount * uint32(unsafe.Sizeof(uint16(0)))
	referencepointer := mem.Malloc(referenceBayite)
	if referencepointer == nil {
		self.refs = nil
		self.ikadiricount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referencepointer)[:ikadiricount:ikadiricount]
	for i := uint32(0); i < ikadiricount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TcowIkadirimanager) Reference(ikadiri uint32) uint16 {
	idx := ikadiri >> 12
	if idx >= self.ikadiricount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowIkadirimanager) Increment(ikadiri uint32) {
	idx := ikadiri >> 12
	if idx >= self.ikadiricount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TcowIkadirimanager) Decrement(ikadiri uint32) {
	idx := ikadiri >> 12
	if idx >= self.ikadiricount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(ipajiUbubikoentry uintptr, ipajiImbonerahamweentry uint32, ububikomanager *TUbubikomanager) {

	IpajiUbubikoentry = ipajiUbubikoentry
	IpajiImbonerahamweentry = ipajiImbonerahamweentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowIkadirimanager.Init(ububikomanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addresspointer, _ := ububikomanager.Alignedmalloc(0x1000)
			if addresspointer == nil {
				return
			}
			address := uint32(uintptr(addresspointer))

			Setunsignedinteger32ataddress(address|0x87, uint32(ipajiUbubikoentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		ipajiUbubikoentry = ipajiUbubikoentry + 0x1000
	}

}
func (self *Paging) SharedUbubikoregion() {

	ipajiUbubikoentry := IpajiUbubikoentry
	kIpajiUbubikoentry := IpajiUbubikoentry

	for i := uint32(1); i <= virtlen; i++ {

		ipajiUbubikoentry = ipajiUbubikoentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetAgaciro(uint32(kIpajiUbubikoentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(ipajiUbubikoentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetAgaciro(uint32(kIpajiUbubikoentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(ipajiUbubikoentry)+pde*4)

		}

	}
}
func (self *Paging) Ipajifault(manager *TInterruptmanager) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if ResolveGukopororaKurikwandikafault() {
		return esp
	}
	return HandlefatalinterruptIkadiri(esp, 0x0E)
}

func Cloneaddressspacecow(inkomokoIpajiUbubiko uint32) uint32 {
	if GikoraUbubikomanager == nil || inkomokoIpajiUbubiko == 0 {
		return 0
	}
	destinationpointer, _ := GikoraUbubikomanager.Alignedmalloc(0x1000)
	if destinationpointer == nil {
		return 0
	}
	destinationIpajiUbubiko := uint32(uintptr(destinationpointer))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationIpajiUbubiko+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		inkomokopdeaddress := inkomokoIpajiUbubiko + pde*4
		inkomokopde := GetAgaciro(inkomokopdeaddress)
		if (inkomokopde & Ipajipresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(inkomokopde, destinationIpajiUbubiko+pde*4)
			continue
		}

		destinationptpointer, _ := GikoraUbubikomanager.Alignedmalloc(0x1000)
		if destinationptpointer == nil {
			continue
		}
		inkomokopt := inkomokopde & IpajiIkadiri
		destinationpt := uint32(uintptr(destinationptpointer))
		Setunsignedinteger32ataddress((destinationpt | (inkomokopde & 0xFFF)), destinationIpajiUbubiko+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := inkomokopt + pte*4
			entry := GetAgaciro(pteaddress)
			if (entry & Ipajipresent) != 0 {
				if (entry & Ipajiwritable) != 0 {
					entry = (entry &^ Ipajiwritable) | Ipajicow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowIkadirimanager.Increment(entry & IpajiIkadiri)
				} else if (entry & Ipajicow) != 0 {
					cowIkadirimanager.Increment(entry & IpajiIkadiri)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	reloadcr3()
	return destinationIpajiUbubiko
}

func ResolveGukopororaKurikwandikafault() bool {
	if GikoraUbubikomanager == nil {
		return false
	}
	faultaddress := getcr2()
	ipajiUbubiko := getcr3()
	pdeaddress := ipajiUbubiko + ((faultaddress>>22)&0x3FF)*4
	pde := GetAgaciro(pdeaddress)
	if (pde & Ipajipresent) == 0 {
		return false
	}
	pt := pde & IpajiIkadiri
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetAgaciro(pteaddress)
	if (pte&Ipajicow) == 0 || (pte&Ipajipresent) == 0 {
		return false
	}
	oldIkadiri := pte & IpajiIkadiri
	if cowIkadirimanager.Reference(oldIkadiri) <= 1 {
		Setunsignedinteger32ataddress((pte|Ipajiwritable)&^Ipajicow, pteaddress)
		reloadcr3()
		return true
	}

	newpointer, _ := GikoraUbubikomanager.Alignedmalloc(0x1000)
	if newpointer == nil {
		return false
	}
	newIkadiri := uint32(uintptr(newpointer)) & IpajiIkadiri

	inkomoko_2 := GetBayitefrompointer(uintptr(faultaddress&IpajiIkadiri), 0x1000, 0x1000)
	destination_2 := GetBayitefrompointer(uintptr(newIkadiri), 0x1000, 0x1000)
	copy(destination_2, inkomoko_2)
	cowIkadirimanager.Decrement(oldIkadiri)
	Setunsignedinteger32ataddress((newIkadiri|(pte&0xFFF)|Ipajiwritable)&^Ipajicow, pteaddress)
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

func SetbyteImbereIpajiUbubiko(x byte, address uint32, ipajiUbubiko uint32) {
	oldcr3 := getcr3()
	setcr3(ipajiUbubiko)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func SetblockImbereIpajiUbubiko(inkomoko_2 []byte, destination_2 []byte, ingano uint32, ipajiUbubiko uint32) {
	if ingano == 0 || ipajiUbubiko == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(ipajiUbubiko)
	makeIgiceprivatewritablecurrent(ipajiUbubiko, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), ingano)

	for i := uint32(0); i < ingano; i++ {
		destination_2[i] = inkomoko_2[i]
	}
	setcr3(oldcr3)
}

func ZeroblockImbereIpajiUbubiko(address uint32, ingano uint32, ipajiUbubiko uint32) {
	if ingano == 0 || ipajiUbubiko == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(ipajiUbubiko)
	makeIgiceprivatewritablecurrent(ipajiUbubiko, address, ingano)
	destination_2 := GetBayitefrompointer(uintptr(address), int(ingano), int(ingano))
	for i := uint32(0); i < ingano; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makeIpajiprivatewritablecurrent(ipajiUbubiko uint32, virtualaddress uint32) bool {
	pde := GetAgaciro(ipajiUbubiko + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & Ipajipresent) == 0 {
		return false
	}
	pteaddress := (pde & IpajiIkadiri) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetAgaciro(pteaddress)
	if (pte & Ipajipresent) == 0 {
		return false
	}
	if (pte & Ipajicow) == 0 {
		return (pte & Ipajiwritable) != 0
	}
	if GikoraUbubikomanager == nil {
		return false
	}
	newpointer, _ := GikoraUbubikomanager.Alignedmalloc(0x1000)
	if newpointer == nil {
		return false
	}
	newIkadiri := uint32(uintptr(newpointer)) & IpajiIkadiri
	inkomoko_2 := GetBayitefrompointer(uintptr(virtualaddress&IpajiIkadiri), 0x1000, 0x1000)
	destination_2 := GetBayitefrompointer(uintptr(newIkadiri), 0x1000, 0x1000)
	copy(destination_2, inkomoko_2)
	cowIkadirimanager.Decrement(pte & IpajiIkadiri)
	Setunsignedinteger32ataddress((newIkadiri|(pte&0xFFF)|Ipajiwritable)&^Ipajicow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	reloadcr3()
	return true
}

func makeIgiceprivatewritablecurrent(ipajiUbubiko uint32, address uint32, ingano uint32) bool {
	if ingano == 0 {
		return true
	}
	last := address + ingano - 1
	if last < address {
		return false
	}
	for ipaji := address & IpajiIkadiri; ; ipaji += 0x1000 {
		if !makeIpajiprivatewritablecurrent(ipajiUbubiko, ipaji) {
			return false
		}
		if ipaji == (last & IpajiIkadiri) {
			break
		}
	}
	return true
}

func MakeIgiceprivatewritable(ipajiUbubiko uint32, address uint32, ingano uint32) bool {
	if ipajiUbubiko == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(ipajiUbubiko)
	yEGO := makeIgiceprivatewritablecurrent(ipajiUbubiko, address, ingano)
	setcr3(oldcr3)
	return yEGO
}

func Setunsignedinteger32ImbereIpajiUbubiko(x uint32, address uint32, ipajiUbubiko uint32) {
	if ipajiUbubiko == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(ipajiUbubiko)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func GetAgaciro(address uint32) uint32 {
	var orgAgaciro uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgAgaciro
}
func GetAgaciroImbereIpajiUbubiko(address uint32, ipajiUbubiko uint32) uint32 {
	if ipajiUbubiko == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(ipajiUbubiko)
	v := GetAgaciro(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func GukopororaIpajiIkadiriblock(xIpajiUbubiko uint32, yIpajiUbubiko uint32, vaddress uint32) {
	if xIpajiUbubiko == 0 || yIpajiUbubiko == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xIpajiUbubiko)
	v = GetAgaciro(vaddress)
	Setunsignedinteger32ImbereIpajiUbubiko(v, vaddress, yIpajiUbubiko)

	setcr3(oldcr3)
}
