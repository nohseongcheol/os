package paging

import unsafe "unsafe"
import . "interrupt"
import . "geheugenmanager"
import . "util"

type PaginaMapItem_2 uintptr

const (
	PaginaAanwezig	uint32	= 0x001
	Paginawritable	uint32	= 0x002
	PaginaGebruiker	uint32	= 0x004
	Paginaframe	uint32	= 0xFFFFF000
	Paginacow	uint32	= 0x200
)

func Instellenbyteataddress(x byte, address uint32)
func Instellenunsignedinteger8ataddress(x uint8, address uint32)
func Instellenunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func instellencr3(paginamap uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type Tcowframemanager struct {
	mem		*TGeheugenmanager
	refs		[]uint16
	frameAantal	uint32
}

var (
	PaginaMapItem	uintptr
	PaginaTabelItem	uint32
	pdelen		uint32
	virtlen		uint32
	cowframemanager	Tcowframemanager
)

func (zelf *Tcowframemanager) Init(mem *TGeheugenmanager, frameAantal uint32) bool {
	zelf.mem = mem
	zelf.frameAantal = frameAantal
	referencebytes := frameAantal * uint32(unsafe.Sizeof(uint16(0)))
	referenceMuisaanwijzer := mem.Geheugen_toewijzen(referencebytes)
	if referenceMuisaanwijzer == nil {
		zelf.refs = nil
		zelf.frameAantal = 0
		return false
	}
	zelf.refs = (*[1 << 28]uint16)(referenceMuisaanwijzer)[:frameAantal:frameAantal]
	for i := uint32(0); i < frameAantal; i++ {
		zelf.refs[i] = 0
	}
	return true
}

func (zelf *Tcowframemanager) Reference(frame uint32) uint16 {
	idx := frame >> 12
	if idx >= zelf.frameAantal || zelf.refs == nil {
		return 0
	}
	return zelf.refs[idx]
}

func (zelf *Tcowframemanager) Increment(frame uint32) {
	idx := frame >> 12
	if idx >= zelf.frameAantal || zelf.refs == nil {
		return
	}
	if zelf.refs[idx] == 0 {
		zelf.refs[idx] = 2
	} else {
		zelf.refs[idx]++
	}
}

func (zelf *Tcowframemanager) Decrement(frame uint32) {
	idx := frame >> 12
	if idx >= zelf.frameAantal || zelf.refs == nil || zelf.refs[idx] == 0 {
		return
	}
	zelf.refs[idx]--
}

func (zelf *Paging) Init(paginaMapItem uintptr, paginaTabelItem uint32, geheugenmanager *TGeheugenmanager) {

	PaginaMapItem = paginaMapItem
	PaginaTabelItem = paginaTabelItem

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframemanager.Init(geheugenmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressMuisaanwijzer, _ := geheugenmanager.Alignedmalloc(0x1000)
			if addressMuisaanwijzer == nil {
				return
			}
			address := uint32(uintptr(addressMuisaanwijzer))

			Instellenunsignedinteger32ataddress(address|0x87, uint32(paginaMapItem)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Instellenunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		paginaMapItem = paginaMapItem + 0x1000
	}

}
func (zelf *Paging) SharedGeheugenregion() {

	paginaMapItem := PaginaMapItem
	kPaginaMapItem := PaginaMapItem

	for i := uint32(1); i <= virtlen; i++ {

		paginaMapItem = paginaMapItem + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetWaarde(uint32(kPaginaMapItem) + pde*4)
			v = (v & 0xFFFFF000)
			Instellenunsignedinteger32ataddress(v|0x87, uint32(paginaMapItem)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetWaarde(uint32(kPaginaMapItem) + pde*4)
			v = (v & 0xFFFFF000)
			Instellenunsignedinteger32ataddress(v|0x87, uint32(paginaMapItem)+pde*4)

		}

	}
}
func (zelf *Paging) Paginafault(manager *TInterruptmanager) {
	interrupthandler = handgreeppaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	zelf.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handgreeppaginginterrupt(esp uint32) uint32 {
	if ResolveKopiërenAanSchrijvenfault() {
		return esp
	}
	return Handgreepfatalinterruptframe(esp, 0x0E)
}

func CloneaddressSpatiecow(bronPaginaMap uint32) uint32 {
	if ActiefGeheugenmanager == nil || bronPaginaMap == 0 {
		return 0
	}
	bestemmingMuisaanwijzer, _ := ActiefGeheugenmanager.Alignedmalloc(0x1000)
	if bestemmingMuisaanwijzer == nil {
		return 0
	}
	bestemmingPaginaMap := uint32(uintptr(bestemmingMuisaanwijzer))
	for i := uint32(0); i < 1024; i++ {
		Instellenunsignedinteger32ataddress(0, bestemmingPaginaMap+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		bronpdeaddress := bronPaginaMap + pde*4
		bronpde := GetWaarde(bronpdeaddress)
		if (bronpde & PaginaAanwezig) == 0 {
			continue
		}
		if issharedpde(pde) {
			Instellenunsignedinteger32ataddress(bronpde, bestemmingPaginaMap+pde*4)
			continue
		}

		bestemmingptMuisaanwijzer, _ := ActiefGeheugenmanager.Alignedmalloc(0x1000)
		if bestemmingptMuisaanwijzer == nil {
			continue
		}
		bronpt := bronpde & Paginaframe
		bestemmingpt := uint32(uintptr(bestemmingptMuisaanwijzer))
		Instellenunsignedinteger32ataddress((bestemmingpt | (bronpde & 0xFFF)), bestemmingPaginaMap+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := bronpt + pte*4
			item := GetWaarde(pteaddress)
			if (item & PaginaAanwezig) != 0 {
				if (item & Paginawritable) != 0 {
					item = (item &^ Paginawritable) | Paginacow
					Instellenunsignedinteger32ataddress(item, pteaddress)
					cowframemanager.Increment(item & Paginaframe)
				} else if (item & Paginacow) != 0 {
					cowframemanager.Increment(item & Paginaframe)
				}
			}
			Instellenunsignedinteger32ataddress(item, bestemmingpt+pte*4)
		}
	}
	herladencr3()
	return bestemmingPaginaMap
}

func ResolveKopiërenAanSchrijvenfault() bool {
	if ActiefGeheugenmanager == nil {
		return false
	}
	faultaddress := getcr2()
	paginamap := getcr3()
	pdeaddress := paginamap + ((faultaddress>>22)&0x3FF)*4
	pde := GetWaarde(pdeaddress)
	if (pde & PaginaAanwezig) == 0 {
		return false
	}
	pt := pde & Paginaframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetWaarde(pteaddress)
	if (pte&Paginacow) == 0 || (pte&PaginaAanwezig) == 0 {
		return false
	}
	oudframe := pte & Paginaframe
	if cowframemanager.Reference(oudframe) <= 1 {
		Instellenunsignedinteger32ataddress((pte|Paginawritable)&^Paginacow, pteaddress)
		herladencr3()
		return true
	}

	nieuwMuisaanwijzer, _ := ActiefGeheugenmanager.Alignedmalloc(0x1000)
	if nieuwMuisaanwijzer == nil {
		return false
	}
	nieuwframe := uint32(uintptr(nieuwMuisaanwijzer)) & Paginaframe

	bron_2 := GetbytesvanMuisaanwijzer(uintptr(faultaddress&Paginaframe), 0x1000, 0x1000)
	bestemming_2 := GetbytesvanMuisaanwijzer(uintptr(nieuwframe), 0x1000, 0x1000)
	copy(bestemming_2, bron_2)
	cowframemanager.Decrement(oudframe)
	Instellenunsignedinteger32ataddress((nieuwframe|(pte&0xFFF)|Paginawritable)&^Paginacow, pteaddress)
	herladencr3()
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

func herladencr3() {
	cr3 := getcr3()
	instellencr3(cr3)
}

func InstellenbyteinPaginaMap(x byte, address uint32, paginamap uint32) {
	oudcr3 := getcr3()
	instellencr3(paginamap)
	Instellenbyteataddress(x, address)
	instellencr3(oudcr3)
}

func InstellenBlokinPaginaMap(bron_2 []byte, bestemming_2 []byte, grootte uint32, paginamap uint32) {
	if grootte == 0 || paginamap == 0 {
		return
	}
	oudcr3 := getcr3()
	instellencr3(paginamap)
	makeBereikPrivéwritableHuidig(paginamap, uint32(uintptr(unsafe.Pointer(&bestemming_2[0]))), grootte)

	for i := uint32(0); i < grootte; i++ {
		bestemming_2[i] = bron_2[i]
	}
	instellencr3(oudcr3)
}

func ZeroBlokinPaginaMap(address uint32, grootte uint32, paginamap uint32) {
	if grootte == 0 || paginamap == 0 {
		return
	}
	oudcr3 := getcr3()
	instellencr3(paginamap)
	makeBereikPrivéwritableHuidig(paginamap, address, grootte)
	bestemming_2 := GetbytesvanMuisaanwijzer(uintptr(address), int(grootte), int(grootte))
	for i := uint32(0); i < grootte; i++ {
		bestemming_2[i] = 0
	}
	instellencr3(oudcr3)
}

func makePaginaPrivéwritableHuidig(paginamap uint32, virtueeladdress uint32) bool {
	pde := GetWaarde(paginamap + ((virtueeladdress>>22)&0x3FF)*4)
	if (pde & PaginaAanwezig) == 0 {
		return false
	}
	pteaddress := (pde & Paginaframe) + ((virtueeladdress>>12)&0x3FF)*4
	pte := GetWaarde(pteaddress)
	if (pte & PaginaAanwezig) == 0 {
		return false
	}
	if (pte & Paginacow) == 0 {
		return (pte & Paginawritable) != 0
	}
	if ActiefGeheugenmanager == nil {
		return false
	}
	nieuwMuisaanwijzer, _ := ActiefGeheugenmanager.Alignedmalloc(0x1000)
	if nieuwMuisaanwijzer == nil {
		return false
	}
	nieuwframe := uint32(uintptr(nieuwMuisaanwijzer)) & Paginaframe
	bron_2 := GetbytesvanMuisaanwijzer(uintptr(virtueeladdress&Paginaframe), 0x1000, 0x1000)
	bestemming_2 := GetbytesvanMuisaanwijzer(uintptr(nieuwframe), 0x1000, 0x1000)
	copy(bestemming_2, bron_2)
	cowframemanager.Decrement(pte & Paginaframe)
	Instellenunsignedinteger32ataddress((nieuwframe|(pte&0xFFF)|Paginawritable)&^Paginacow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	herladencr3()
	return true
}

func makeBereikPrivéwritableHuidig(paginamap uint32, address uint32, grootte uint32) bool {
	if grootte == 0 {
		return true
	}
	laatst := address + grootte - 1
	if laatst < address {
		return false
	}
	for pagina := address & Paginaframe; ; pagina += 0x1000 {
		if !makePaginaPrivéwritableHuidig(paginamap, pagina) {
			return false
		}
		if pagina == (laatst & Paginaframe) {
			break
		}
	}
	return true
}

func MakeBereikPrivéwritable(paginamap uint32, address uint32, grootte uint32) bool {
	if paginamap == 0 {
		return false
	}
	oudcr3 := getcr3()
	instellencr3(paginamap)
	ok := makeBereikPrivéwritableHuidig(paginamap, address, grootte)
	instellencr3(oudcr3)
	return ok
}

func Instellenunsignedinteger32inPaginaMap(x uint32, address uint32, paginamap uint32) {
	if paginamap == 0 {
		return
	}
	oudcr3 := getcr3()
	instellencr3(paginamap)
	Instellenunsignedinteger32ataddress(x, address)
	instellencr3(oudcr3)
}

func GetWaarde(address uint32) uint32 {
	var orgWaarde uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgWaarde
}
func GetWaardeinPaginaMap(address uint32, paginamap uint32) uint32 {
	if paginamap == 0 {
		return 0
	}
	oudcr3 := getcr3()
	instellencr3(paginamap)
	v := GetWaarde(address)
	instellencr3(oudcr3)
	return v
}

var v uint32 = 0

func KopiërenPaginaframeBlok(xPaginaMap uint32, yPaginaMap uint32, vaddress uint32) {
	if xPaginaMap == 0 || yPaginaMap == 0 {
		return
	}
	oudcr3 := getcr3()
	instellencr3(xPaginaMap)
	v = GetWaarde(vaddress)
	Instellenunsignedinteger32inPaginaMap(v, vaddress, yPaginaMap)

	instellencr3(oudcr3)
}
