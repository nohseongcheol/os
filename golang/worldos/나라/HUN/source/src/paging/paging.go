/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "megszakítás"
import . "memóriamanager"
import . "util"

type OldalKönyvtárbejegyzés_2 uintptr

const (
	OldalJelenvan		uint32	= 0x001
	Oldalwritable		uint32	= 0x002
	OldalFelhasználó	uint32	= 0x004
	OldalKeret		uint32	= 0xFFFFF000
	Oldalcow		uint32	= 0x200
)

func Halmazbyteataddress(x byte, address uint32)
func Halmazunsignedinteger8ataddress(x uint8, address uint32)
func Halmazunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func halmazcr3(oldalKönyvtár uint32)
func getcr3() uint32

type Paging struct {
	TMegszakításhandler
}
type TcowKeretmanager struct {
	mem		*TMemóriamanager
	refs		[]uint16
	keretSzámláló	uint32
}

var (
	OldalKönyvtárbejegyzés	uintptr
	OldalTáblázatbejegyzés	uint32
	pdelen			uint32
	virtlen			uint32
	cowKeretmanager		TcowKeretmanager
)

func (self *TcowKeretmanager) Init(mem *TMemóriamanager, keretSzámláló uint32) bool {
	self.mem = mem
	self.keretSzámláló = keretSzámláló
	referenceBájt := keretSzámláló * uint32(unsafe.Sizeof(uint16(0)))
	referenceMutató := mem.Malloc(referenceBájt)
	if referenceMutató == nil {
		self.refs = nil
		self.keretSzámláló = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceMutató)[:keretSzámláló:keretSzámláló]
	for i := uint32(0); i < keretSzámláló; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TcowKeretmanager) Reference(keret uint32) uint16 {
	idx := keret >> 12
	if idx >= self.keretSzámláló || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowKeretmanager) Increment(keret uint32) {
	idx := keret >> 12
	if idx >= self.keretSzámláló || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TcowKeretmanager) Decrement(keret uint32) {
	idx := keret >> 12
	if idx >= self.keretSzámláló || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(oldalKönyvtárbejegyzés uintptr, oldalTáblázatbejegyzés uint32, memóriamanager *TMemóriamanager) {

	OldalKönyvtárbejegyzés = oldalKönyvtárbejegyzés
	OldalTáblázatbejegyzés = oldalTáblázatbejegyzés

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowKeretmanager.Init(memóriamanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressMutató, _ := memóriamanager.Alignedmalloc(0x1000)
			if addressMutató == nil {
				return
			}
			address := uint32(uintptr(addressMutató))

			Halmazunsignedinteger32ataddress(address|0x87, uint32(oldalKönyvtárbejegyzés)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Halmazunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		oldalKönyvtárbejegyzés = oldalKönyvtárbejegyzés + 0x1000
	}

}
func (self *Paging) SharedMemóriaregion() {

	oldalKönyvtárbejegyzés := OldalKönyvtárbejegyzés
	kOldalKönyvtárbejegyzés := OldalKönyvtárbejegyzés

	for i := uint32(1); i <= virtlen; i++ {

		oldalKönyvtárbejegyzés = oldalKönyvtárbejegyzés + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetÉrték(uint32(kOldalKönyvtárbejegyzés) + pde*4)
			v = (v & 0xFFFFF000)
			Halmazunsignedinteger32ataddress(v|0x87, uint32(oldalKönyvtárbejegyzés)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetÉrték(uint32(kOldalKönyvtárbejegyzés) + pde*4)
			v = (v & 0xFFFFF000)
			Halmazunsignedinteger32ataddress(v|0x87, uint32(oldalKönyvtárbejegyzés)+pde*4)

		}

	}
}
func (self *Paging) Oldalfault(manager *TMegszakításmanager) {
	megszakításhandler = fogantyúpagingMegszakítás

	var address uintptr
	address = uintptr(unsafe.Pointer(&megszakításhandler))
	self.TMegszakításhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var megszakításhandler func(uint32) uint32

func fogantyúpagingMegszakítás(esp uint32) uint32 {
	if ResolveMásolásBeÍrásfault() {
		return esp
	}
	return FogantyúfatalMegszakításKeret(esp, 0x0E)
}

func CloneaddressSzóközcow(forrásOldalKönyvtár uint32) uint32 {
	if AktívMemóriamanager == nil || forrásOldalKönyvtár == 0 {
		return 0
	}
	célMutató, _ := AktívMemóriamanager.Alignedmalloc(0x1000)
	if célMutató == nil {
		return 0
	}
	célOldalKönyvtár := uint32(uintptr(célMutató))
	for i := uint32(0); i < 1024; i++ {
		Halmazunsignedinteger32ataddress(0, célOldalKönyvtár+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		forráspdeaddress := forrásOldalKönyvtár + pde*4
		forráspde := GetÉrték(forráspdeaddress)
		if (forráspde & OldalJelenvan) == 0 {
			continue
		}
		if issharedpde(pde) {
			Halmazunsignedinteger32ataddress(forráspde, célOldalKönyvtár+pde*4)
			continue
		}

		célptMutató, _ := AktívMemóriamanager.Alignedmalloc(0x1000)
		if célptMutató == nil {
			continue
		}
		forráspt := forráspde & OldalKeret
		célpt := uint32(uintptr(célptMutató))
		Halmazunsignedinteger32ataddress((célpt | (forráspde & 0xFFF)), célOldalKönyvtár+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := forráspt + pte*4
			bejegyzés := GetÉrték(pteaddress)
			if (bejegyzés & OldalJelenvan) != 0 {
				if (bejegyzés & Oldalwritable) != 0 {
					bejegyzés = (bejegyzés &^ Oldalwritable) | Oldalcow
					Halmazunsignedinteger32ataddress(bejegyzés, pteaddress)
					cowKeretmanager.Increment(bejegyzés & OldalKeret)
				} else if (bejegyzés & Oldalcow) != 0 {
					cowKeretmanager.Increment(bejegyzés & OldalKeret)
				}
			}
			Halmazunsignedinteger32ataddress(bejegyzés, célpt+pte*4)
		}
	}
	újratöltéscr3()
	return célOldalKönyvtár
}

func ResolveMásolásBeÍrásfault() bool {
	if AktívMemóriamanager == nil {
		return false
	}
	faultaddress := getcr2()
	oldalKönyvtár := getcr3()
	pdeaddress := oldalKönyvtár + ((faultaddress>>22)&0x3FF)*4
	pde := GetÉrték(pdeaddress)
	if (pde & OldalJelenvan) == 0 {
		return false
	}
	pt := pde & OldalKeret
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetÉrték(pteaddress)
	if (pte&Oldalcow) == 0 || (pte&OldalJelenvan) == 0 {
		return false
	}
	öregKeret := pte & OldalKeret
	if cowKeretmanager.Reference(öregKeret) <= 1 {
		Halmazunsignedinteger32ataddress((pte|Oldalwritable)&^Oldalcow, pteaddress)
		újratöltéscr3()
		return true
	}

	újMutató, _ := AktívMemóriamanager.Alignedmalloc(0x1000)
	if újMutató == nil {
		return false
	}
	újKeret := uint32(uintptr(újMutató)) & OldalKeret

	forrás_2 := GetBájtfromMutató(uintptr(faultaddress&OldalKeret), 0x1000, 0x1000)
	cél_2 := GetBájtfromMutató(uintptr(újKeret), 0x1000, 0x1000)
	copy(cél_2, forrás_2)
	cowKeretmanager.Decrement(öregKeret)
	Halmazunsignedinteger32ataddress((újKeret|(pte&0xFFF)|Oldalwritable)&^Oldalcow, pteaddress)
	újratöltéscr3()
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

func újratöltéscr3() {
	cr3 := getcr3()
	halmazcr3(cr3)
}

func HalmazbyteBeOldalKönyvtár(x byte, address uint32, oldalKönyvtár uint32) {
	öregcr3 := getcr3()
	halmazcr3(oldalKönyvtár)
	Halmazbyteataddress(x, address)
	halmazcr3(öregcr3)
}

func HalmazBlokkBeOldalKönyvtár(forrás_2 []byte, cél_2 []byte, méret uint32, oldalKönyvtár uint32) {
	if méret == 0 || oldalKönyvtár == 0 {
		return
	}
	öregcr3 := getcr3()
	halmazcr3(oldalKönyvtár)
	makeTartománySzemélyeswritableJelenlegi(oldalKönyvtár, uint32(uintptr(unsafe.Pointer(&cél_2[0]))), méret)

	for i := uint32(0); i < méret; i++ {
		cél_2[i] = forrás_2[i]
	}
	halmazcr3(öregcr3)
}

func NullaBlokkBeOldalKönyvtár(address uint32, méret uint32, oldalKönyvtár uint32) {
	if méret == 0 || oldalKönyvtár == 0 {
		return
	}
	öregcr3 := getcr3()
	halmazcr3(oldalKönyvtár)
	makeTartománySzemélyeswritableJelenlegi(oldalKönyvtár, address, méret)
	cél_2 := GetBájtfromMutató(uintptr(address), int(méret), int(méret))
	for i := uint32(0); i < méret; i++ {
		cél_2[i] = 0
	}
	halmazcr3(öregcr3)
}

func makeOldalSzemélyeswritableJelenlegi(oldalKönyvtár uint32, virtualaddress uint32) bool {
	pde := GetÉrték(oldalKönyvtár + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & OldalJelenvan) == 0 {
		return false
	}
	pteaddress := (pde & OldalKeret) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetÉrték(pteaddress)
	if (pte & OldalJelenvan) == 0 {
		return false
	}
	if (pte & Oldalcow) == 0 {
		return (pte & Oldalwritable) != 0
	}
	if AktívMemóriamanager == nil {
		return false
	}
	újMutató, _ := AktívMemóriamanager.Alignedmalloc(0x1000)
	if újMutató == nil {
		return false
	}
	újKeret := uint32(uintptr(újMutató)) & OldalKeret
	forrás_2 := GetBájtfromMutató(uintptr(virtualaddress&OldalKeret), 0x1000, 0x1000)
	cél_2 := GetBájtfromMutató(uintptr(újKeret), 0x1000, 0x1000)
	copy(cél_2, forrás_2)
	cowKeretmanager.Decrement(pte & OldalKeret)
	Halmazunsignedinteger32ataddress((újKeret|(pte&0xFFF)|Oldalwritable)&^Oldalcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	újratöltéscr3()
	return true
}

func makeTartománySzemélyeswritableJelenlegi(oldalKönyvtár uint32, address uint32, méret uint32) bool {
	if méret == 0 {
		return true
	}
	utolsó := address + méret - 1
	if utolsó < address {
		return false
	}
	for oldal := address & OldalKeret; ; oldal += 0x1000 {
		if !makeOldalSzemélyeswritableJelenlegi(oldalKönyvtár, oldal) {
			return false
		}
		if oldal == (utolsó & OldalKeret) {
			break
		}
	}
	return true
}

func MakeTartománySzemélyeswritable(oldalKönyvtár uint32, address uint32, méret uint32) bool {
	if oldalKönyvtár == 0 {
		return false
	}
	öregcr3 := getcr3()
	halmazcr3(oldalKönyvtár)
	ok := makeTartománySzemélyeswritableJelenlegi(oldalKönyvtár, address, méret)
	halmazcr3(öregcr3)
	return ok
}

func Halmazunsignedinteger32BeOldalKönyvtár(x uint32, address uint32, oldalKönyvtár uint32) {
	if oldalKönyvtár == 0 {
		return
	}
	öregcr3 := getcr3()
	halmazcr3(oldalKönyvtár)
	Halmazunsignedinteger32ataddress(x, address)
	halmazcr3(öregcr3)
}

func GetÉrték(address uint32) uint32 {
	var orgÉrték uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgÉrték
}
func GetÉrtékBeOldalKönyvtár(address uint32, oldalKönyvtár uint32) uint32 {
	if oldalKönyvtár == 0 {
		return 0
	}
	öregcr3 := getcr3()
	halmazcr3(oldalKönyvtár)
	v := GetÉrték(address)
	halmazcr3(öregcr3)
	return v
}

var v uint32 = 0

func MásolásOldalKeretBlokk(xOldalKönyvtár uint32, yOldalKönyvtár uint32, vaddress uint32) {
	if xOldalKönyvtár == 0 || yOldalKönyvtár == 0 {
		return
	}
	öregcr3 := getcr3()
	halmazcr3(xOldalKönyvtár)
	v = GetÉrték(vaddress)
	Halmazunsignedinteger32BeOldalKönyvtár(v, vaddress, yOldalKönyvtár)

	halmazcr3(öregcr3)
}
