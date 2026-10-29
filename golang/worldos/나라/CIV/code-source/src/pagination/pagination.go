/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pagination

import unsafe "unsafe"
import . "interruption"
import . "mémoiregestionnaire"
import . "utilitaire"

type Pagerépertoireélément_2 uintptr

const (
	PagePrésente	uint32	= 0x001
	Pagewritable	uint32	= 0x002
	Pageutilisateur	uint32	= 0x004
	Pagetrame	uint32	= 0xFFFFF000
	Pagecow		uint32	= 0x200
)

func Ensembleoctetataddress(x byte, address uint32)
func Ensembleunsignedinteger8ataddress(x uint8, address uint32)
func Ensembleunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func ensemblecr3(répertoire_de_pages uint32)
func getcr3() uint32

type Pagination struct {
	TInterruptionhandler
}
type Tcowtramegestionnaire struct {
	mem		*TMémoiregestionnaire
	refs		[]uint16
	trameNombre	uint32
}

var (
	Pagerépertoireélément	uintptr
	PageTableauélément	uint32
	pdelen			uint32
	virtlen			uint32
	cowtramegestionnaire	Tcowtramegestionnaire
)

func (self *Tcowtramegestionnaire) Init(mem *TMémoiregestionnaire, trameNombre uint32) bool {
	self.mem = mem
	self.trameNombre = trameNombre
	referenceOctets := trameNombre * uint32(unsafe.Sizeof(uint16(0)))
	referencePointeur := mem.Allouer_la_mémoire(referenceOctets)
	if referencePointeur == nil {
		self.refs = nil
		self.trameNombre = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referencePointeur)[:trameNombre:trameNombre]
	for i := uint32(0); i < trameNombre; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcowtramegestionnaire) Reference(trame uint32) uint16 {
	idx := trame >> 12
	if idx >= self.trameNombre || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcowtramegestionnaire) Increment(trame uint32) {
	idx := trame >> 12
	if idx >= self.trameNombre || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcowtramegestionnaire) Decrement(trame uint32) {
	idx := trame >> 12
	if idx >= self.trameNombre || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Pagination) Init(pagerépertoireélément uintptr, pageTableauélément uint32, mémoiregestionnaire *TMémoiregestionnaire) {

	Pagerépertoireélément = pagerépertoireélément
	PageTableauélément = pageTableauélément

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowtramegestionnaire.Init(mémoiregestionnaire, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressPointeur, _ := mémoiregestionnaire.Alignedmalloc(0x1000)
			if addressPointeur == nil {
				return
			}
			address := uint32(uintptr(addressPointeur))

			Ensembleunsignedinteger32ataddress(address|0x87, uint32(pagerépertoireélément)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Ensembleunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		pagerépertoireélément = pagerépertoireélément + 0x1000
	}

}
func (self *Pagination) Sharedmémoireregion() {

	pagerépertoireélément := Pagerépertoireélément
	kpagerépertoireélément := Pagerépertoireélément

	for i := uint32(1); i <= virtlen; i++ {

		pagerépertoireélément = pagerépertoireélément + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetValeur(uint32(kpagerépertoireélément) + pde*4)
			v = (v & 0xFFFFF000)
			Ensembleunsignedinteger32ataddress(v|0x87, uint32(pagerépertoireélément)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetValeur(uint32(kpagerépertoireélément) + pde*4)
			v = (v & 0xFFFFF000)
			Ensembleunsignedinteger32ataddress(v|0x87, uint32(pagerépertoireélément)+pde*4)

		}

	}
}
func (self *Pagination) Pagedéfaut(gestionnaire *TInterruptiongestionnaire) {
	interruptionhandler = poignéepaginationinterruption

	var address uintptr
	address = uintptr(unsafe.Pointer(&interruptionhandler))
	self.TInterruptionhandler.Init(0xE, uintptr(unsafe.Pointer(gestionnaire)), address)
}

var interruptionhandler func(uint32) uint32

func poignéepaginationinterruption(esp uint32) uint32 {
	if Résoudrecopiersurécriredéfaut() {
		return esp
	}
	return Poignéefatalinterruptiontrame(esp, 0x0E)
}

func CloneaddressEspacecow(sourcepagerépertoire uint32) uint32 {
	if Actifmémoiregestionnaire == nil || sourcepagerépertoire == 0 {
		return 0
	}
	destinationPointeur, _ := Actifmémoiregestionnaire.Alignedmalloc(0x1000)
	if destinationPointeur == nil {
		return 0
	}
	destinationpagerépertoire := uint32(uintptr(destinationPointeur))
	for i := uint32(0); i < 1024; i++ {
		Ensembleunsignedinteger32ataddress(0, destinationpagerépertoire+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		sourcepdeaddress := sourcepagerépertoire + pde*4
		sourcepde := GetValeur(sourcepdeaddress)
		if (sourcepde & PagePrésente) == 0 {
			continue
		}
		if issharedpde(pde) {
			Ensembleunsignedinteger32ataddress(sourcepde, destinationpagerépertoire+pde*4)
			continue
		}

		destinationptPointeur, _ := Actifmémoiregestionnaire.Alignedmalloc(0x1000)
		if destinationptPointeur == nil {
			continue
		}
		sourcept := sourcepde & Pagetrame
		destinationpt := uint32(uintptr(destinationptPointeur))
		Ensembleunsignedinteger32ataddress((destinationpt | (sourcepde & 0xFFF)), destinationpagerépertoire+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := sourcept + pte*4
			élément := GetValeur(pteaddress)
			if (élément & PagePrésente) != 0 {
				if (élément & Pagewritable) != 0 {
					élément = (élément &^ Pagewritable) | Pagecow
					Ensembleunsignedinteger32ataddress(élément, pteaddress)
					cowtramegestionnaire.Increment(élément & Pagetrame)
				} else if (élément & Pagecow) != 0 {
					cowtramegestionnaire.Increment(élément & Pagetrame)
				}
			}
			Ensembleunsignedinteger32ataddress(élément, destinationpt+pte*4)
		}
	}
	rechargercr3()
	return destinationpagerépertoire
}

func Résoudrecopiersurécriredéfaut() bool {
	if Actifmémoiregestionnaire == nil {
		return false
	}
	défautaddress := getcr2()
	répertoire_de_pages := getcr3()
	pdeaddress := répertoire_de_pages + ((défautaddress>>22)&0x3FF)*4
	pde := GetValeur(pdeaddress)
	if (pde & PagePrésente) == 0 {
		return false
	}
	pt := pde & Pagetrame
	pteaddress := pt + ((défautaddress>>12)&0x3FF)*4
	pte := GetValeur(pteaddress)
	if (pte&Pagecow) == 0 || (pte&PagePrésente) == 0 {
		return false
	}
	vieuxtrame := pte & Pagetrame
	if cowtramegestionnaire.Reference(vieuxtrame) <= 1 {
		Ensembleunsignedinteger32ataddress((pte|Pagewritable)&^Pagecow, pteaddress)
		rechargercr3()
		return true
	}

	nouveauPointeur, _ := Actifmémoiregestionnaire.Alignedmalloc(0x1000)
	if nouveauPointeur == nil {
		return false
	}
	nouveautrame := uint32(uintptr(nouveauPointeur)) & Pagetrame

	source_2 := GetOctetsdePointeur(uintptr(défautaddress&Pagetrame), 0x1000, 0x1000)
	destination_2 := GetOctetsdePointeur(uintptr(nouveautrame), 0x1000, 0x1000)
	copy(destination_2, source_2)
	cowtramegestionnaire.Decrement(vieuxtrame)
	Ensembleunsignedinteger32ataddress((nouveautrame|(pte&0xFFF)|Pagewritable)&^Pagecow, pteaddress)
	rechargercr3()
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

func rechargercr3() {
	cr3 := getcr3()
	ensemblecr3(cr3)
}

func EnsembleoctetEntrantepagerépertoire(x byte, address uint32, répertoire_de_pages uint32) {
	vieuxcr3 := getcr3()
	ensemblecr3(répertoire_de_pages)
	Ensembleoctetataddress(x, address)
	ensemblecr3(vieuxcr3)
}

func EnsembleBlocEntrantepagerépertoire(source_2 []byte, destination_2 []byte, taille uint32, répertoire_de_pages uint32) {
	if taille == 0 || répertoire_de_pages == 0 {
		return
	}
	vieuxcr3 := getcr3()
	ensemblecr3(répertoire_de_pages)
	makeIntervallePrivéwritableCourante(répertoire_de_pages, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), taille)

	for i := uint32(0); i < taille; i++ {
		destination_2[i] = source_2[i]
	}
	ensemblecr3(vieuxcr3)
}

func ZéroBlocEntrantepagerépertoire(address uint32, taille uint32, répertoire_de_pages uint32) {
	if taille == 0 || répertoire_de_pages == 0 {
		return
	}
	vieuxcr3 := getcr3()
	ensemblecr3(répertoire_de_pages)
	makeIntervallePrivéwritableCourante(répertoire_de_pages, address, taille)
	destination_2 := GetOctetsdePointeur(uintptr(address), int(taille), int(taille))
	for i := uint32(0); i < taille; i++ {
		destination_2[i] = 0
	}
	ensemblecr3(vieuxcr3)
}

func makepagePrivéwritableCourante(répertoire_de_pages uint32, virtueladdress uint32) bool {
	pde := GetValeur(répertoire_de_pages + ((virtueladdress>>22)&0x3FF)*4)
	if (pde & PagePrésente) == 0 {
		return false
	}
	pteaddress := (pde & Pagetrame) + ((virtueladdress>>12)&0x3FF)*4
	pte := GetValeur(pteaddress)
	if (pte & PagePrésente) == 0 {
		return false
	}
	if (pte & Pagecow) == 0 {
		return (pte & Pagewritable) != 0
	}
	if Actifmémoiregestionnaire == nil {
		return false
	}
	nouveauPointeur, _ := Actifmémoiregestionnaire.Alignedmalloc(0x1000)
	if nouveauPointeur == nil {
		return false
	}
	nouveautrame := uint32(uintptr(nouveauPointeur)) & Pagetrame
	source_2 := GetOctetsdePointeur(uintptr(virtueladdress&Pagetrame), 0x1000, 0x1000)
	destination_2 := GetOctetsdePointeur(uintptr(nouveautrame), 0x1000, 0x1000)
	copy(destination_2, source_2)
	cowtramegestionnaire.Decrement(pte & Pagetrame)
	Ensembleunsignedinteger32ataddress((nouveautrame|(pte&0xFFF)|Pagewritable)&^Pagecow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	rechargercr3()
	return true
}

func makeIntervallePrivéwritableCourante(répertoire_de_pages uint32, address uint32, taille uint32) bool {
	if taille == 0 {
		return true
	}
	dernière := address + taille - 1
	if dernière < address {
		return false
	}
	for page := address & Pagetrame; ; page += 0x1000 {
		if !makepagePrivéwritableCourante(répertoire_de_pages, page) {
			return false
		}
		if page == (dernière & Pagetrame) {
			break
		}
	}
	return true
}

func MakeIntervallePrivéwritable(répertoire_de_pages uint32, address uint32, taille uint32) bool {
	if répertoire_de_pages == 0 {
		return false
	}
	vieuxcr3 := getcr3()
	ensemblecr3(répertoire_de_pages)
	valider := makeIntervallePrivéwritableCourante(répertoire_de_pages, address, taille)
	ensemblecr3(vieuxcr3)
	return valider
}

func Ensembleunsignedinteger32Entrantepagerépertoire(x uint32, address uint32, répertoire_de_pages uint32) {
	if répertoire_de_pages == 0 {
		return
	}
	vieuxcr3 := getcr3()
	ensemblecr3(répertoire_de_pages)
	Ensembleunsignedinteger32ataddress(x, address)
	ensemblecr3(vieuxcr3)
}

func GetValeur(address uint32) uint32 {
	var orgValeur uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgValeur
}
func GetValeurEntrantepagerépertoire(address uint32, répertoire_de_pages uint32) uint32 {
	if répertoire_de_pages == 0 {
		return 0
	}
	vieuxcr3 := getcr3()
	ensemblecr3(répertoire_de_pages)
	v := GetValeur(address)
	ensemblecr3(vieuxcr3)
	return v
}

var v uint32 = 0

func CopierpagetrameBloc(xpagerépertoire uint32, ypagerépertoire uint32, vaddress uint32) {
	if xpagerépertoire == 0 || ypagerépertoire == 0 {
		return
	}
	vieuxcr3 := getcr3()
	ensemblecr3(xpagerépertoire)
	v = GetValeur(vaddress)
	Ensembleunsignedinteger32Entrantepagerépertoire(v, vaddress, ypagerépertoire)

	ensemblecr3(vieuxcr3)
}
