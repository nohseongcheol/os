/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "prekinitev"
import . "pomnilnikmanager"
import . "util"

type StranMapavnos_2 uintptr

const (
	StranPrisotnost	uint32	= 0x001
	Stranwritable	uint32	= 0x002
	StranUporabnik	uint32	= 0x004
	StranOkvir	uint32	= 0xFFFFF000
	Strancow	uint32	= 0x200
)

func Množicabyteataddress(x byte, address uint32)
func Množicaunsignedinteger8ataddress(x uint8, address uint32)
func Množicaunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func množicacr3(stranMapa uint32)
func getcr3() uint32

type Paging struct {
	TPrekinitevhandler
}
type TcowOkvirmanager struct {
	mem		*TPomnilnikmanager
	refs		[]uint16
	okvircount	uint32
}

var (
	StranMapavnos		uintptr
	StranPreglednicavnos	uint32
	pdelen			uint32
	virtlen			uint32
	cowOkvirmanager		TcowOkvirmanager
)

func (sam *TcowOkvirmanager) Init(mem *TPomnilnikmanager, okvircount uint32) bool {
	sam.mem = mem
	sam.okvircount = okvircount
	referenceBajtov := okvircount * uint32(unsafe.Sizeof(uint16(0)))
	referenceKazalnik := mem.Malloc(referenceBajtov)
	if referenceKazalnik == nil {
		sam.refs = nil
		sam.okvircount = 0
		return false
	}
	sam.refs = (*[1 << 28]uint16)(referenceKazalnik)[:okvircount:okvircount]
	for i := uint32(0); i < okvircount; i++ {
		sam.refs[i] = 0
	}
	return true
}

func (sam *TcowOkvirmanager) Reference(okvir uint32) uint16 {
	idx := okvir >> 12
	if idx >= sam.okvircount || sam.refs == nil {
		return 0
	}
	return sam.refs[idx]
}

func (sam *TcowOkvirmanager) Increment(okvir uint32) {
	idx := okvir >> 12
	if idx >= sam.okvircount || sam.refs == nil {
		return
	}
	if sam.refs[idx] == 0 {
		sam.refs[idx] = 2
	} else {
		sam.refs[idx]++
	}
}

func (sam *TcowOkvirmanager) Decrement(okvir uint32) {
	idx := okvir >> 12
	if idx >= sam.okvircount || sam.refs == nil || sam.refs[idx] == 0 {
		return
	}
	sam.refs[idx]--
}

func (sam *Paging) Init(stranMapavnos uintptr, stranPreglednicavnos uint32, pomnilnikmanager *TPomnilnikmanager) {

	StranMapavnos = stranMapavnos
	StranPreglednicavnos = stranPreglednicavnos

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowOkvirmanager.Init(pomnilnikmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressKazalnik, _ := pomnilnikmanager.Alignedmalloc(0x1000)
			if addressKazalnik == nil {
				return
			}
			address := uint32(uintptr(addressKazalnik))

			Množicaunsignedinteger32ataddress(address|0x87, uint32(stranMapavnos)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Množicaunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		stranMapavnos = stranMapavnos + 0x1000
	}

}
func (sam *Paging) SharedPomnilnikregion() {

	stranMapavnos := StranMapavnos
	kStranMapavnos := StranMapavnos

	for i := uint32(1); i <= virtlen; i++ {

		stranMapavnos = stranMapavnos + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVrednost(uint32(kStranMapavnos) + pde*4)
			v = (v & 0xFFFFF000)
			Množicaunsignedinteger32ataddress(v|0x87, uint32(stranMapavnos)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVrednost(uint32(kStranMapavnos) + pde*4)
			v = (v & 0xFFFFF000)
			Množicaunsignedinteger32ataddress(v|0x87, uint32(stranMapavnos)+pde*4)

		}

	}
}
func (sam *Paging) Stranfault(manager *TPrekinitevmanager) {
	prekinitevhandler = ročicapagingPrekinitev

	var address uintptr
	address = uintptr(unsafe.Pointer(&prekinitevhandler))
	sam.TPrekinitevhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var prekinitevhandler func(uint32) uint32

func ročicapagingPrekinitev(esp uint32) uint32 {
	if ResolveKopirajVključenoPisanjefault() {
		return esp
	}
	return RočicafatalPrekinitevOkvir(esp, 0x0E)
}

func CloneaddressPresledekcow(virStranMapa uint32) uint32 {
	if DejavenPomnilnikmanager == nil || virStranMapa == 0 {
		return 0
	}
	ciljKazalnik, _ := DejavenPomnilnikmanager.Alignedmalloc(0x1000)
	if ciljKazalnik == nil {
		return 0
	}
	ciljStranMapa := uint32(uintptr(ciljKazalnik))
	for i := uint32(0); i < 1024; i++ {
		Množicaunsignedinteger32ataddress(0, ciljStranMapa+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		virpdeaddress := virStranMapa + pde*4
		virpde := GetVrednost(virpdeaddress)
		if (virpde & StranPrisotnost) == 0 {
			continue
		}
		if issharedpde(pde) {
			Množicaunsignedinteger32ataddress(virpde, ciljStranMapa+pde*4)
			continue
		}

		ciljptKazalnik, _ := DejavenPomnilnikmanager.Alignedmalloc(0x1000)
		if ciljptKazalnik == nil {
			continue
		}
		virpt := virpde & StranOkvir
		ciljpt := uint32(uintptr(ciljptKazalnik))
		Množicaunsignedinteger32ataddress((ciljpt | (virpde & 0xFFF)), ciljStranMapa+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := virpt + pte*4
			vnos := GetVrednost(pteaddress)
			if (vnos & StranPrisotnost) != 0 {
				if (vnos & Stranwritable) != 0 {
					vnos = (vnos &^ Stranwritable) | Strancow
					Množicaunsignedinteger32ataddress(vnos, pteaddress)
					cowOkvirmanager.Increment(vnos & StranOkvir)
				} else if (vnos & Strancow) != 0 {
					cowOkvirmanager.Increment(vnos & StranOkvir)
				}
			}
			Množicaunsignedinteger32ataddress(vnos, ciljpt+pte*4)
		}
	}
	ponovnonaložicr3()
	return ciljStranMapa
}

func ResolveKopirajVključenoPisanjefault() bool {
	if DejavenPomnilnikmanager == nil {
		return false
	}
	faultaddress := getcr2()
	stranMapa := getcr3()
	pdeaddress := stranMapa + ((faultaddress>>22)&0x3FF)*4
	pde := GetVrednost(pdeaddress)
	if (pde & StranPrisotnost) == 0 {
		return false
	}
	pt := pde & StranOkvir
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetVrednost(pteaddress)
	if (pte&Strancow) == 0 || (pte&StranPrisotnost) == 0 {
		return false
	}
	oldOkvir := pte & StranOkvir
	if cowOkvirmanager.Reference(oldOkvir) <= 1 {
		Množicaunsignedinteger32ataddress((pte|Stranwritable)&^Strancow, pteaddress)
		ponovnonaložicr3()
		return true
	}

	novaKazalnik, _ := DejavenPomnilnikmanager.Alignedmalloc(0x1000)
	if novaKazalnik == nil {
		return false
	}
	novaOkvir := uint32(uintptr(novaKazalnik)) & StranOkvir

	vir_2 := GetBajtovfromKazalnik(uintptr(faultaddress&StranOkvir), 0x1000, 0x1000)
	cilj_2 := GetBajtovfromKazalnik(uintptr(novaOkvir), 0x1000, 0x1000)
	copy(cilj_2, vir_2)
	cowOkvirmanager.Decrement(oldOkvir)
	Množicaunsignedinteger32ataddress((novaOkvir|(pte&0xFFF)|Stranwritable)&^Strancow, pteaddress)
	ponovnonaložicr3()
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

func ponovnonaložicr3() {
	cr3 := getcr3()
	množicacr3(cr3)
}

func MnožicabyteVhodnoStranMapa(x byte, address uint32, stranMapa uint32) {
	oldcr3 := getcr3()
	množicacr3(stranMapa)
	Množicabyteataddress(x, address)
	množicacr3(oldcr3)
}

func MnožicaBlokVhodnoStranMapa(vir_2 []byte, cilj_2 []byte, velikost uint32, stranMapa uint32) {
	if velikost == 0 || stranMapa == 0 {
		return
	}
	oldcr3 := getcr3()
	množicacr3(stranMapa)
	makeObmočjeZasebnowritablecurrent(stranMapa, uint32(uintptr(unsafe.Pointer(&cilj_2[0]))), velikost)

	for i := uint32(0); i < velikost; i++ {
		cilj_2[i] = vir_2[i]
	}
	množicacr3(oldcr3)
}

func ZeroBlokVhodnoStranMapa(address uint32, velikost uint32, stranMapa uint32) {
	if velikost == 0 || stranMapa == 0 {
		return
	}
	oldcr3 := getcr3()
	množicacr3(stranMapa)
	makeObmočjeZasebnowritablecurrent(stranMapa, address, velikost)
	cilj_2 := GetBajtovfromKazalnik(uintptr(address), int(velikost), int(velikost))
	for i := uint32(0); i < velikost; i++ {
		cilj_2[i] = 0
	}
	množicacr3(oldcr3)
}

func makeStranZasebnowritablecurrent(stranMapa uint32, navideznoaddress uint32) bool {
	pde := GetVrednost(stranMapa + ((navideznoaddress>>22)&0x3FF)*4)
	if (pde & StranPrisotnost) == 0 {
		return false
	}
	pteaddress := (pde & StranOkvir) + ((navideznoaddress>>12)&0x3FF)*4
	pte := GetVrednost(pteaddress)
	if (pte & StranPrisotnost) == 0 {
		return false
	}
	if (pte & Strancow) == 0 {
		return (pte & Stranwritable) != 0
	}
	if DejavenPomnilnikmanager == nil {
		return false
	}
	novaKazalnik, _ := DejavenPomnilnikmanager.Alignedmalloc(0x1000)
	if novaKazalnik == nil {
		return false
	}
	novaOkvir := uint32(uintptr(novaKazalnik)) & StranOkvir
	vir_2 := GetBajtovfromKazalnik(uintptr(navideznoaddress&StranOkvir), 0x1000, 0x1000)
	cilj_2 := GetBajtovfromKazalnik(uintptr(novaOkvir), 0x1000, 0x1000)
	copy(cilj_2, vir_2)
	cowOkvirmanager.Decrement(pte & StranOkvir)
	Množicaunsignedinteger32ataddress((novaOkvir|(pte&0xFFF)|Stranwritable)&^Strancow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	ponovnonaložicr3()
	return true
}

func makeObmočjeZasebnowritablecurrent(stranMapa uint32, address uint32, velikost uint32) bool {
	if velikost == 0 {
		return true
	}
	zadnji := address + velikost - 1
	if zadnji < address {
		return false
	}
	for stran := address & StranOkvir; ; stran += 0x1000 {
		if !makeStranZasebnowritablecurrent(stranMapa, stran) {
			return false
		}
		if stran == (zadnji & StranOkvir) {
			break
		}
	}
	return true
}

func MakeObmočjeZasebnowritable(stranMapa uint32, address uint32, velikost uint32) bool {
	if stranMapa == 0 {
		return false
	}
	oldcr3 := getcr3()
	množicacr3(stranMapa)
	vredu := makeObmočjeZasebnowritablecurrent(stranMapa, address, velikost)
	množicacr3(oldcr3)
	return vredu
}

func Množicaunsignedinteger32VhodnoStranMapa(x uint32, address uint32, stranMapa uint32) {
	if stranMapa == 0 {
		return
	}
	oldcr3 := getcr3()
	množicacr3(stranMapa)
	Množicaunsignedinteger32ataddress(x, address)
	množicacr3(oldcr3)
}

func GetVrednost(address uint32) uint32 {
	var orgVrednost uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgVrednost
}
func GetVrednostVhodnoStranMapa(address uint32, stranMapa uint32) uint32 {
	if stranMapa == 0 {
		return 0
	}
	oldcr3 := getcr3()
	množicacr3(stranMapa)
	v := GetVrednost(address)
	množicacr3(oldcr3)
	return v
}

var v uint32 = 0

func KopirajStranOkvirBlok(xStranMapa uint32, yStranMapa uint32, vaddress uint32) {
	if xStranMapa == 0 || yStranMapa == 0 {
		return
	}
	oldcr3 := getcr3()
	množicacr3(xStranMapa)
	v = GetVrednost(vaddress)
	Množicaunsignedinteger32VhodnoStranMapa(v, vaddress, yStranMapa)

	množicacr3(oldcr3)
}
