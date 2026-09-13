package paging

import unsafe "unsafe"
import . "pārtraukums"
import . "atmiņamanager"
import . "util"

type LapaMapeieraksts_2 uintptr

const (
	LapaKlātesošs	uint32	= 0x001
	Lapawritable	uint32	= 0x002
	LapaLietotājs	uint32	= 0x004
	LapaIetvars	uint32	= 0xFFFFF000
	Lapacow		uint32	= 0x200
)

func Kopabyteataddress(x byte, address uint32)
func Kopaunsignedinteger8ataddress(x uint8, address uint32)
func Kopaunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func kopacr3(lapaMape uint32)
func getcr3() uint32

type Paging struct {
	TPārtraukumshandler
}
type TcowIetvarsmanager struct {
	mem		*TAtmiņamanager
	refs		[]uint16
	ietvarscount	uint32
}

var (
	LapaMapeieraksts	uintptr
	LapaTabulaieraksts	uint32
	pdelen			uint32
	virtlen			uint32
	cowIetvarsmanager	TcowIetvarsmanager
)

func (pats *TcowIetvarsmanager) Init(mem *TAtmiņamanager, ietvarscount uint32) bool {
	pats.mem = mem
	pats.ietvarscount = ietvarscount
	referenceBaiti := ietvarscount * uint32(unsafe.Sizeof(uint16(0)))
	referenceKursors := mem.Malloc(referenceBaiti)
	if referenceKursors == nil {
		pats.refs = nil
		pats.ietvarscount = 0
		return false
	}
	pats.refs = (*[1 << 28]uint16)(referenceKursors)[:ietvarscount:ietvarscount]
	for i := uint32(0); i < ietvarscount; i++ {
		pats.refs[i] = 0
	}
	return true
}

func (pats *TcowIetvarsmanager) Reference(ietvars uint32) uint16 {
	idx := ietvars >> 12
	if idx >= pats.ietvarscount || pats.refs == nil {
		return 0
	}
	return pats.refs[idx]
}

func (pats *TcowIetvarsmanager) Increment(ietvars uint32) {
	idx := ietvars >> 12
	if idx >= pats.ietvarscount || pats.refs == nil {
		return
	}
	if pats.refs[idx] == 0 {
		pats.refs[idx] = 2
	} else {
		pats.refs[idx]++
	}
}

func (pats *TcowIetvarsmanager) Decrement(ietvars uint32) {
	idx := ietvars >> 12
	if idx >= pats.ietvarscount || pats.refs == nil || pats.refs[idx] == 0 {
		return
	}
	pats.refs[idx]--
}

func (pats *Paging) Init(lapaMapeieraksts uintptr, lapaTabulaieraksts uint32, atmiņamanager *TAtmiņamanager) {

	LapaMapeieraksts = lapaMapeieraksts
	LapaTabulaieraksts = lapaTabulaieraksts

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowIetvarsmanager.Init(atmiņamanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressKursors, _ := atmiņamanager.Alignedmalloc(0x1000)
			if addressKursors == nil {
				return
			}
			address := uint32(uintptr(addressKursors))

			Kopaunsignedinteger32ataddress(address|0x87, uint32(lapaMapeieraksts)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Kopaunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		lapaMapeieraksts = lapaMapeieraksts + 0x1000
	}

}
func (pats *Paging) SharedAtmiņaregion() {

	lapaMapeieraksts := LapaMapeieraksts
	kLapaMapeieraksts := LapaMapeieraksts

	for i := uint32(1); i <= virtlen; i++ {

		lapaMapeieraksts = lapaMapeieraksts + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVērtība(uint32(kLapaMapeieraksts) + pde*4)
			v = (v & 0xFFFFF000)
			Kopaunsignedinteger32ataddress(v|0x87, uint32(lapaMapeieraksts)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVērtība(uint32(kLapaMapeieraksts) + pde*4)
			v = (v & 0xFFFFF000)
			Kopaunsignedinteger32ataddress(v|0x87, uint32(lapaMapeieraksts)+pde*4)

		}

	}
}
func (pats *Paging) Lapafault(manager *TPārtraukumsmanager) {
	pārtraukumshandler = handlepagingPārtraukums

	var address uintptr
	address = uintptr(unsafe.Pointer(&pārtraukumshandler))
	pats.TPārtraukumshandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var pārtraukumshandler func(uint32) uint32

func handlepagingPārtraukums(esp uint32) uint32 {
	if ResolveKopētIeslēgtsRakstītfault() {
		return esp
	}
	return HandlefatalPārtraukumsIetvars(esp, 0x0E)
}

func Cloneaddressspacecow(avotsLapaMape uint32) uint32 {
	if AktīvsAtmiņamanager == nil || avotsLapaMape == 0 {
		return 0
	}
	mērķisKursors, _ := AktīvsAtmiņamanager.Alignedmalloc(0x1000)
	if mērķisKursors == nil {
		return 0
	}
	mērķisLapaMape := uint32(uintptr(mērķisKursors))
	for i := uint32(0); i < 1024; i++ {
		Kopaunsignedinteger32ataddress(0, mērķisLapaMape+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		avotspdeaddress := avotsLapaMape + pde*4
		avotspde := GetVērtība(avotspdeaddress)
		if (avotspde & LapaKlātesošs) == 0 {
			continue
		}
		if issharedpde(pde) {
			Kopaunsignedinteger32ataddress(avotspde, mērķisLapaMape+pde*4)
			continue
		}

		mērķisptKursors, _ := AktīvsAtmiņamanager.Alignedmalloc(0x1000)
		if mērķisptKursors == nil {
			continue
		}
		avotspt := avotspde & LapaIetvars
		mērķispt := uint32(uintptr(mērķisptKursors))
		Kopaunsignedinteger32ataddress((mērķispt | (avotspde & 0xFFF)), mērķisLapaMape+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := avotspt + pte*4
			ieraksts := GetVērtība(pteaddress)
			if (ieraksts & LapaKlātesošs) != 0 {
				if (ieraksts & Lapawritable) != 0 {
					ieraksts = (ieraksts &^ Lapawritable) | Lapacow
					Kopaunsignedinteger32ataddress(ieraksts, pteaddress)
					cowIetvarsmanager.Increment(ieraksts & LapaIetvars)
				} else if (ieraksts & Lapacow) != 0 {
					cowIetvarsmanager.Increment(ieraksts & LapaIetvars)
				}
			}
			Kopaunsignedinteger32ataddress(ieraksts, mērķispt+pte*4)
		}
	}
	pārlādētcr3()
	return mērķisLapaMape
}

func ResolveKopētIeslēgtsRakstītfault() bool {
	if AktīvsAtmiņamanager == nil {
		return false
	}
	faultaddress := getcr2()
	lapaMape := getcr3()
	pdeaddress := lapaMape + ((faultaddress>>22)&0x3FF)*4
	pde := GetVērtība(pdeaddress)
	if (pde & LapaKlātesošs) == 0 {
		return false
	}
	pt := pde & LapaIetvars
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetVērtība(pteaddress)
	if (pte&Lapacow) == 0 || (pte&LapaKlātesošs) == 0 {
		return false
	}
	oldIetvars := pte & LapaIetvars
	if cowIetvarsmanager.Reference(oldIetvars) <= 1 {
		Kopaunsignedinteger32ataddress((pte|Lapawritable)&^Lapacow, pteaddress)
		pārlādētcr3()
		return true
	}

	jaunsKursors, _ := AktīvsAtmiņamanager.Alignedmalloc(0x1000)
	if jaunsKursors == nil {
		return false
	}
	jaunsIetvars := uint32(uintptr(jaunsKursors)) & LapaIetvars

	avots_2 := GetBaitifromKursors(uintptr(faultaddress&LapaIetvars), 0x1000, 0x1000)
	mērķis_2 := GetBaitifromKursors(uintptr(jaunsIetvars), 0x1000, 0x1000)
	copy(mērķis_2, avots_2)
	cowIetvarsmanager.Decrement(oldIetvars)
	Kopaunsignedinteger32ataddress((jaunsIetvars|(pte&0xFFF)|Lapawritable)&^Lapacow, pteaddress)
	pārlādētcr3()
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

func pārlādētcr3() {
	cr3 := getcr3()
	kopacr3(cr3)
}

func KopabyteIenākošāLapaMape(x byte, address uint32, lapaMape uint32) {
	oldcr3 := getcr3()
	kopacr3(lapaMape)
	Kopabyteataddress(x, address)
	kopacr3(oldcr3)
}

func KopaBloksIenākošāLapaMape(avots_2 []byte, mērķis_2 []byte, izmērs uint32, lapaMape uint32) {
	if izmērs == 0 || lapaMape == 0 {
		return
	}
	oldcr3 := getcr3()
	kopacr3(lapaMape)
	makeApgabalsPrivātswritablePašreizējais(lapaMape, uint32(uintptr(unsafe.Pointer(&mērķis_2[0]))), izmērs)

	for i := uint32(0); i < izmērs; i++ {
		mērķis_2[i] = avots_2[i]
	}
	kopacr3(oldcr3)
}

func ZeroBloksIenākošāLapaMape(address uint32, izmērs uint32, lapaMape uint32) {
	if izmērs == 0 || lapaMape == 0 {
		return
	}
	oldcr3 := getcr3()
	kopacr3(lapaMape)
	makeApgabalsPrivātswritablePašreizējais(lapaMape, address, izmērs)
	mērķis_2 := GetBaitifromKursors(uintptr(address), int(izmērs), int(izmērs))
	for i := uint32(0); i < izmērs; i++ {
		mērķis_2[i] = 0
	}
	kopacr3(oldcr3)
}

func makeLapaPrivātswritablePašreizējais(lapaMape uint32, virtuālaaddress uint32) bool {
	pde := GetVērtība(lapaMape + ((virtuālaaddress>>22)&0x3FF)*4)
	if (pde & LapaKlātesošs) == 0 {
		return false
	}
	pteaddress := (pde & LapaIetvars) + ((virtuālaaddress>>12)&0x3FF)*4
	pte := GetVērtība(pteaddress)
	if (pte & LapaKlātesošs) == 0 {
		return false
	}
	if (pte & Lapacow) == 0 {
		return (pte & Lapawritable) != 0
	}
	if AktīvsAtmiņamanager == nil {
		return false
	}
	jaunsKursors, _ := AktīvsAtmiņamanager.Alignedmalloc(0x1000)
	if jaunsKursors == nil {
		return false
	}
	jaunsIetvars := uint32(uintptr(jaunsKursors)) & LapaIetvars
	avots_2 := GetBaitifromKursors(uintptr(virtuālaaddress&LapaIetvars), 0x1000, 0x1000)
	mērķis_2 := GetBaitifromKursors(uintptr(jaunsIetvars), 0x1000, 0x1000)
	copy(mērķis_2, avots_2)
	cowIetvarsmanager.Decrement(pte & LapaIetvars)
	Kopaunsignedinteger32ataddress((jaunsIetvars|(pte&0xFFF)|Lapawritable)&^Lapacow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	pārlādētcr3()
	return true
}

func makeApgabalsPrivātswritablePašreizējais(lapaMape uint32, address uint32, izmērs uint32) bool {
	if izmērs == 0 {
		return true
	}
	pēdējais := address + izmērs - 1
	if pēdējais < address {
		return false
	}
	for lapa := address & LapaIetvars; ; lapa += 0x1000 {
		if !makeLapaPrivātswritablePašreizējais(lapaMape, lapa) {
			return false
		}
		if lapa == (pēdējais & LapaIetvars) {
			break
		}
	}
	return true
}

func MakeApgabalsPrivātswritable(lapaMape uint32, address uint32, izmērs uint32) bool {
	if lapaMape == 0 {
		return false
	}
	oldcr3 := getcr3()
	kopacr3(lapaMape)
	labi := makeApgabalsPrivātswritablePašreizējais(lapaMape, address, izmērs)
	kopacr3(oldcr3)
	return labi
}

func Kopaunsignedinteger32IenākošāLapaMape(x uint32, address uint32, lapaMape uint32) {
	if lapaMape == 0 {
		return
	}
	oldcr3 := getcr3()
	kopacr3(lapaMape)
	Kopaunsignedinteger32ataddress(x, address)
	kopacr3(oldcr3)
}

func GetVērtība(address uint32) uint32 {
	var orgVērtība uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgVērtība
}
func GetVērtībaIenākošāLapaMape(address uint32, lapaMape uint32) uint32 {
	if lapaMape == 0 {
		return 0
	}
	oldcr3 := getcr3()
	kopacr3(lapaMape)
	v := GetVērtība(address)
	kopacr3(oldcr3)
	return v
}

var v uint32 = 0

func KopētLapaIetvarsBloks(xLapaMape uint32, yLapaMape uint32, vaddress uint32) {
	if xLapaMape == 0 || yLapaMape == 0 {
		return
	}
	oldcr3 := getcr3()
	kopacr3(xLapaMape)
	v = GetVērtība(vaddress)
	Kopaunsignedinteger32IenākošāLapaMape(v, vaddress, yLapaMape)

	kopacr3(oldcr3)
}
