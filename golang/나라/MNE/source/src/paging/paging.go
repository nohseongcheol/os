package paging

import unsafe "unsafe"
import . "ометање"
import . "memorijamanager"
import . "util"

type ListDirektorijumунос_2 uintptr

const (
	ListPrisutno	uint32	= 0x001
	Listwritable	uint32	= 0x002
	ListKorisnik	uint32	= 0x004
	ListOkvir	uint32	= 0xFFFFF000
	Listcow		uint32	= 0x200
)

func Скупbyteataddress(x byte, address uint32)
func Скупunsignedinteger8ataddress(x uint8, address uint32)
func Скупunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func скупcr3(listDirektorijum uint32)
func getcr3() uint32

type Paging struct {
	TОметањеhandler
}
type TcowOkvirmanager struct {
	mem		*TMemorijamanager
	refs		[]uint16
	okvircount	uint32
}

var (
	ListDirektorijumунос	uintptr
	ListTabelaунос		uint32
	pdelen			uint32
	virtlen			uint32
	cowOkvirmanager		TcowOkvirmanager
)

func (isti *TcowOkvirmanager) Init(mem *TMemorijamanager, okvircount uint32) bool {
	isti.mem = mem
	isti.okvircount = okvircount
	referenceBajtova := okvircount * uint32(unsafe.Sizeof(uint16(0)))
	referencePokazivač := mem.Malloc(referenceBajtova)
	if referencePokazivač == nil {
		isti.refs = nil
		isti.okvircount = 0
		return false
	}
	isti.refs = (*[1 << 28]uint16)(referencePokazivač)[:okvircount:okvircount]
	for i := uint32(0); i < okvircount; i++ {
		isti.refs[i] = 0
	}
	return true
}

func (isti *TcowOkvirmanager) Reference(okvir uint32) uint16 {
	idx := okvir >> 12
	if idx >= isti.okvircount || isti.refs == nil {
		return 0
	}
	return isti.refs[idx]
}

func (isti *TcowOkvirmanager) Increment(okvir uint32) {
	idx := okvir >> 12
	if idx >= isti.okvircount || isti.refs == nil {
		return
	}
	if isti.refs[idx] == 0 {
		isti.refs[idx] = 2
	} else {
		isti.refs[idx]++
	}
}

func (isti *TcowOkvirmanager) Decrement(okvir uint32) {
	idx := okvir >> 12
	if idx >= isti.okvircount || isti.refs == nil || isti.refs[idx] == 0 {
		return
	}
	isti.refs[idx]--
}

func (isti *Paging) Init(listDirektorijumунос uintptr, listTabelaунос uint32, memorijamanager *TMemorijamanager) {

	ListDirektorijumунос = listDirektorijumунос
	ListTabelaунос = listTabelaунос

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowOkvirmanager.Init(memorijamanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressPokazivač, _ := memorijamanager.Alignedmalloc(0x1000)
			if addressPokazivač == nil {
				return
			}
			address := uint32(uintptr(addressPokazivač))

			Скупunsignedinteger32ataddress(address|0x87, uint32(listDirektorijumунос)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Скупunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		listDirektorijumунос = listDirektorijumунос + 0x1000
	}

}
func (isti *Paging) SharedMemorijaregion() {

	listDirektorijumунос := ListDirektorijumунос
	klistDirektorijumунос := ListDirektorijumунос

	for i := uint32(1); i <= virtlen; i++ {

		listDirektorijumунос = listDirektorijumунос + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetВредност(uint32(klistDirektorijumунос) + pde*4)
			v = (v & 0xFFFFF000)
			Скупunsignedinteger32ataddress(v|0x87, uint32(listDirektorijumунос)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetВредност(uint32(klistDirektorijumунос) + pde*4)
			v = (v & 0xFFFFF000)
			Скупunsignedinteger32ataddress(v|0x87, uint32(listDirektorijumунос)+pde*4)

		}

	}
}
func (isti *Paging) Listfault(manager *TОметањеmanager) {
	ометањеhandler = ручкаpagingОметање

	var address uintptr
	address = uintptr(unsafe.Pointer(&ометањеhandler))
	isti.TОметањеhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var ометањеhandler func(uint32) uint32

func ручкаpagingОметање(esp uint32) uint32 {
	if ResolveУмножиnaupisfault() {
		return esp
	}
	return РучкаfatalОметањеOkvir(esp, 0x0E)
}

func Cloneaddressrazmakcow(izvorlistDirektorijum uint32) uint32 {
	if AktivnaMemorijamanager == nil || izvorlistDirektorijum == 0 {
		return 0
	}
	odredištePokazivač, _ := AktivnaMemorijamanager.Alignedmalloc(0x1000)
	if odredištePokazivač == nil {
		return 0
	}
	odredištelistDirektorijum := uint32(uintptr(odredištePokazivač))
	for i := uint32(0); i < 1024; i++ {
		Скупunsignedinteger32ataddress(0, odredištelistDirektorijum+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		izvorpdeaddress := izvorlistDirektorijum + pde*4
		izvorpde := GetВредност(izvorpdeaddress)
		if (izvorpde & ListPrisutno) == 0 {
			continue
		}
		if issharedpde(pde) {
			Скупunsignedinteger32ataddress(izvorpde, odredištelistDirektorijum+pde*4)
			continue
		}

		odredišteptPokazivač, _ := AktivnaMemorijamanager.Alignedmalloc(0x1000)
		if odredišteptPokazivač == nil {
			continue
		}
		izvorpt := izvorpde & ListOkvir
		odredištept := uint32(uintptr(odredišteptPokazivač))
		Скупunsignedinteger32ataddress((odredištept | (izvorpde & 0xFFF)), odredištelistDirektorijum+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := izvorpt + pte*4
			унос := GetВредност(pteaddress)
			if (унос & ListPrisutno) != 0 {
				if (унос & Listwritable) != 0 {
					унос = (унос &^ Listwritable) | Listcow
					Скупunsignedinteger32ataddress(унос, pteaddress)
					cowOkvirmanager.Increment(унос & ListOkvir)
				} else if (унос & Listcow) != 0 {
					cowOkvirmanager.Increment(унос & ListOkvir)
				}
			}
			Скупunsignedinteger32ataddress(унос, odredištept+pte*4)
		}
	}
	освежиcr3()
	return odredištelistDirektorijum
}

func ResolveУмножиnaupisfault() bool {
	if AktivnaMemorijamanager == nil {
		return false
	}
	faultaddress := getcr2()
	listDirektorijum := getcr3()
	pdeaddress := listDirektorijum + ((faultaddress>>22)&0x3FF)*4
	pde := GetВредност(pdeaddress)
	if (pde & ListPrisutno) == 0 {
		return false
	}
	pt := pde & ListOkvir
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetВредност(pteaddress)
	if (pte&Listcow) == 0 || (pte&ListPrisutno) == 0 {
		return false
	}
	oldOkvir := pte & ListOkvir
	if cowOkvirmanager.Reference(oldOkvir) <= 1 {
		Скупunsignedinteger32ataddress((pte|Listwritable)&^Listcow, pteaddress)
		освежиcr3()
		return true
	}

	новаPokazivač, _ := AktivnaMemorijamanager.Alignedmalloc(0x1000)
	if новаPokazivač == nil {
		return false
	}
	новаOkvir := uint32(uintptr(новаPokazivač)) & ListOkvir

	izvor_2 := GetBajtovasaPokazivač(uintptr(faultaddress&ListOkvir), 0x1000, 0x1000)
	odredište_2 := GetBajtovasaPokazivač(uintptr(новаOkvir), 0x1000, 0x1000)
	copy(odredište_2, izvor_2)
	cowOkvirmanager.Decrement(oldOkvir)
	Скупunsignedinteger32ataddress((новаOkvir|(pte&0xFFF)|Listwritable)&^Listcow, pteaddress)
	освежиcr3()
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

func освежиcr3() {
	cr3 := getcr3()
	скупcr3(cr3)
}

func СкупbyteПримљеноlistDirektorijum(x byte, address uint32, listDirektorijum uint32) {
	oldcr3 := getcr3()
	скупcr3(listDirektorijum)
	Скупbyteataddress(x, address)
	скупcr3(oldcr3)
}

func СкупBlokПримљеноlistDirektorijum(izvor_2 []byte, odredište_2 []byte, величина uint32, listDirektorijum uint32) {
	if величина == 0 || listDirektorijum == 0 {
		return
	}
	oldcr3 := getcr3()
	скупcr3(listDirektorijum)
	makeOpsegPrivatnowritableТренутно(listDirektorijum, uint32(uintptr(unsafe.Pointer(&odredište_2[0]))), величина)

	for i := uint32(0); i < величина; i++ {
		odredište_2[i] = izvor_2[i]
	}
	скупcr3(oldcr3)
}

func ZeroBlokПримљеноlistDirektorijum(address uint32, величина uint32, listDirektorijum uint32) {
	if величина == 0 || listDirektorijum == 0 {
		return
	}
	oldcr3 := getcr3()
	скупcr3(listDirektorijum)
	makeOpsegPrivatnowritableТренутно(listDirektorijum, address, величина)
	odredište_2 := GetBajtovasaPokazivač(uintptr(address), int(величина), int(величина))
	for i := uint32(0); i < величина; i++ {
		odredište_2[i] = 0
	}
	скупcr3(oldcr3)
}

func makelistPrivatnowritableТренутно(listDirektorijum uint32, virtuelnoaddress uint32) bool {
	pde := GetВредност(listDirektorijum + ((virtuelnoaddress>>22)&0x3FF)*4)
	if (pde & ListPrisutno) == 0 {
		return false
	}
	pteaddress := (pde & ListOkvir) + ((virtuelnoaddress>>12)&0x3FF)*4
	pte := GetВредност(pteaddress)
	if (pte & ListPrisutno) == 0 {
		return false
	}
	if (pte & Listcow) == 0 {
		return (pte & Listwritable) != 0
	}
	if AktivnaMemorijamanager == nil {
		return false
	}
	новаPokazivač, _ := AktivnaMemorijamanager.Alignedmalloc(0x1000)
	if новаPokazivač == nil {
		return false
	}
	новаOkvir := uint32(uintptr(новаPokazivač)) & ListOkvir
	izvor_2 := GetBajtovasaPokazivač(uintptr(virtuelnoaddress&ListOkvir), 0x1000, 0x1000)
	odredište_2 := GetBajtovasaPokazivač(uintptr(новаOkvir), 0x1000, 0x1000)
	copy(odredište_2, izvor_2)
	cowOkvirmanager.Decrement(pte & ListOkvir)
	Скупunsignedinteger32ataddress((новаOkvir|(pte&0xFFF)|Listwritable)&^Listcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	освежиcr3()
	return true
}

func makeOpsegPrivatnowritableТренутно(listDirektorijum uint32, address uint32, величина uint32) bool {
	if величина == 0 {
		return true
	}
	задња := address + величина - 1
	if задња < address {
		return false
	}
	for list := address & ListOkvir; ; list += 0x1000 {
		if !makelistPrivatnowritableТренутно(listDirektorijum, list) {
			return false
		}
		if list == (задња & ListOkvir) {
			break
		}
	}
	return true
}

func MakeOpsegPrivatnowritable(listDirektorijum uint32, address uint32, величина uint32) bool {
	if listDirektorijum == 0 {
		return false
	}
	oldcr3 := getcr3()
	скупcr3(listDirektorijum)
	уреду := makeOpsegPrivatnowritableТренутно(listDirektorijum, address, величина)
	скупcr3(oldcr3)
	return уреду
}

func Скупunsignedinteger32ПримљеноlistDirektorijum(x uint32, address uint32, listDirektorijum uint32) {
	if listDirektorijum == 0 {
		return
	}
	oldcr3 := getcr3()
	скупcr3(listDirektorijum)
	Скупunsignedinteger32ataddress(x, address)
	скупcr3(oldcr3)
}

func GetВредност(address uint32) uint32 {
	var orgВредност uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgВредност
}
func GetВредностПримљеноlistDirektorijum(address uint32, listDirektorijum uint32) uint32 {
	if listDirektorijum == 0 {
		return 0
	}
	oldcr3 := getcr3()
	скупcr3(listDirektorijum)
	v := GetВредност(address)
	скупcr3(oldcr3)
	return v
}

var v uint32 = 0

func УмножиlistOkvirBlok(xlistDirektorijum uint32, ylistDirektorijum uint32, vaddress uint32) {
	if xlistDirektorijum == 0 || ylistDirektorijum == 0 {
		return
	}
	oldcr3 := getcr3()
	скупcr3(xlistDirektorijum)
	v = GetВредност(vaddress)
	Скупunsignedinteger32ПримљеноlistDirektorijum(v, vaddress, ylistDirektorijum)

	скупcr3(oldcr3)
}
