/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "ometanje"
import . "memorijamanager"
import . "util"

type STRANADirektorijumunos_2 uintptr

const (
	STRANAPrisutna	uint32	= 0x001
	STRANAwritable	uint32	= 0x002
	STRANAKorisnik	uint32	= 0x004
	STRANAOkvir	uint32	= 0xFFFFF000
	STRANAcow		uint32	= 0x200
)

func Skupbyteataddress(x byte, address uint32)
func Skupunsignedinteger8ataddress(x uint8, address uint32)
func Skupunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func skupcr3(sTRANADirektorijum uint32)
func getcr3() uint32

type Paging struct {
	TOmetanjehandler
}
type TcowOkvirmanager struct {
	mem		*TMemorijamanager
	refs		[]uint16
	okvircount	uint32
}

var (
	STRANADirektorijumunos	uintptr
	STRANATabelaunos		uint32
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

func (isti *Paging) Init(sTRANADirektorijumunos uintptr, sTRANATabelaunos uint32, memorijamanager *TMemorijamanager) {

	STRANADirektorijumunos = sTRANADirektorijumunos
	STRANATabelaunos = sTRANATabelaunos

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

			Skupunsignedinteger32ataddress(address|0x87, uint32(sTRANADirektorijumunos)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Skupunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		sTRANADirektorijumunos = sTRANADirektorijumunos + 0x1000
	}

}
func (isti *Paging) SharedMemorijaregion() {

	sTRANADirektorijumunos := STRANADirektorijumunos
	kSTRANADirektorijumunos := STRANADirektorijumunos

	for i := uint32(1); i <= virtlen; i++ {

		sTRANADirektorijumunos = sTRANADirektorijumunos + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVrednost(uint32(kSTRANADirektorijumunos) + pde*4)
			v = (v & 0xFFFFF000)
			Skupunsignedinteger32ataddress(v|0x87, uint32(sTRANADirektorijumunos)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVrednost(uint32(kSTRANADirektorijumunos) + pde*4)
			v = (v & 0xFFFFF000)
			Skupunsignedinteger32ataddress(v|0x87, uint32(sTRANADirektorijumunos)+pde*4)

		}

	}
}
func (isti *Paging) STRANAfault(manager *TOmetanjemanager) {
	ometanjehandler = ručkapagingOmetanje

	var address uintptr
	address = uintptr(unsafe.Pointer(&ometanjehandler))
	isti.TOmetanjehandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var ometanjehandler func(uint32) uint32

func ručkapagingOmetanje(esp uint32) uint32 {
	if ResolveUmnožinaPišefault() {
		return esp
	}
	return RučkafatalOmetanjeOkvir(esp, 0x0E)
}

func Cloneaddressrazmakcow(izvorSTRANADirektorijum uint32) uint32 {
	if AktivnaMemorijamanager == nil || izvorSTRANADirektorijum == 0 {
		return 0
	}
	odredištePokazivač, _ := AktivnaMemorijamanager.Alignedmalloc(0x1000)
	if odredištePokazivač == nil {
		return 0
	}
	odredišteSTRANADirektorijum := uint32(uintptr(odredištePokazivač))
	for i := uint32(0); i < 1024; i++ {
		Skupunsignedinteger32ataddress(0, odredišteSTRANADirektorijum+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		izvorpdeaddress := izvorSTRANADirektorijum + pde*4
		izvorpde := GetVrednost(izvorpdeaddress)
		if (izvorpde & STRANAPrisutna) == 0 {
			continue
		}
		if issharedpde(pde) {
			Skupunsignedinteger32ataddress(izvorpde, odredišteSTRANADirektorijum+pde*4)
			continue
		}

		odredišteptPokazivač, _ := AktivnaMemorijamanager.Alignedmalloc(0x1000)
		if odredišteptPokazivač == nil {
			continue
		}
		izvorpt := izvorpde & STRANAOkvir
		odredištept := uint32(uintptr(odredišteptPokazivač))
		Skupunsignedinteger32ataddress((odredištept | (izvorpde & 0xFFF)), odredišteSTRANADirektorijum+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := izvorpt + pte*4
			unos := GetVrednost(pteaddress)
			if (unos & STRANAPrisutna) != 0 {
				if (unos & STRANAwritable) != 0 {
					unos = (unos &^ STRANAwritable) | STRANAcow
					Skupunsignedinteger32ataddress(unos, pteaddress)
					cowOkvirmanager.Increment(unos & STRANAOkvir)
				} else if (unos & STRANAcow) != 0 {
					cowOkvirmanager.Increment(unos & STRANAOkvir)
				}
			}
			Skupunsignedinteger32ataddress(unos, odredištept+pte*4)
		}
	}
	osvežicr3()
	return odredišteSTRANADirektorijum
}

func ResolveUmnožinaPišefault() bool {
	if AktivnaMemorijamanager == nil {
		return false
	}
	faultaddress := getcr2()
	sTRANADirektorijum := getcr3()
	pdeaddress := sTRANADirektorijum + ((faultaddress>>22)&0x3FF)*4
	pde := GetVrednost(pdeaddress)
	if (pde & STRANAPrisutna) == 0 {
		return false
	}
	pt := pde & STRANAOkvir
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetVrednost(pteaddress)
	if (pte&STRANAcow) == 0 || (pte&STRANAPrisutna) == 0 {
		return false
	}
	oldOkvir := pte & STRANAOkvir
	if cowOkvirmanager.Reference(oldOkvir) <= 1 {
		Skupunsignedinteger32ataddress((pte|STRANAwritable)&^STRANAcow, pteaddress)
		osvežicr3()
		return true
	}

	novaPokazivač, _ := AktivnaMemorijamanager.Alignedmalloc(0x1000)
	if novaPokazivač == nil {
		return false
	}
	novaOkvir := uint32(uintptr(novaPokazivač)) & STRANAOkvir

	izvor_2 := GetBajtovasaPokazivač(uintptr(faultaddress&STRANAOkvir), 0x1000, 0x1000)
	odredište_2 := GetBajtovasaPokazivač(uintptr(novaOkvir), 0x1000, 0x1000)
	copy(odredište_2, izvor_2)
	cowOkvirmanager.Decrement(oldOkvir)
	Skupunsignedinteger32ataddress((novaOkvir|(pte&0xFFF)|STRANAwritable)&^STRANAcow, pteaddress)
	osvežicr3()
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

func osvežicr3() {
	cr3 := getcr3()
	skupcr3(cr3)
}

func SkupbytePrimljenoSTRANADirektorijum(x byte, address uint32, sTRANADirektorijum uint32) {
	oldcr3 := getcr3()
	skupcr3(sTRANADirektorijum)
	Skupbyteataddress(x, address)
	skupcr3(oldcr3)
}

func SkupBlokPrimljenoSTRANADirektorijum(izvor_2 []byte, odredište_2 []byte, veličina uint32, sTRANADirektorijum uint32) {
	if veličina == 0 || sTRANADirektorijum == 0 {
		return
	}
	oldcr3 := getcr3()
	skupcr3(sTRANADirektorijum)
	makeOpsegPrivatnowritableTrenutno(sTRANADirektorijum, uint32(uintptr(unsafe.Pointer(&odredište_2[0]))), veličina)

	for i := uint32(0); i < veličina; i++ {
		odredište_2[i] = izvor_2[i]
	}
	skupcr3(oldcr3)
}

func ZeroBlokPrimljenoSTRANADirektorijum(address uint32, veličina uint32, sTRANADirektorijum uint32) {
	if veličina == 0 || sTRANADirektorijum == 0 {
		return
	}
	oldcr3 := getcr3()
	skupcr3(sTRANADirektorijum)
	makeOpsegPrivatnowritableTrenutno(sTRANADirektorijum, address, veličina)
	odredište_2 := GetBajtovasaPokazivač(uintptr(address), int(veličina), int(veličina))
	for i := uint32(0); i < veličina; i++ {
		odredište_2[i] = 0
	}
	skupcr3(oldcr3)
}

func makeSTRANAPrivatnowritableTrenutno(sTRANADirektorijum uint32, virtuelnoaddress uint32) bool {
	pde := GetVrednost(sTRANADirektorijum + ((virtuelnoaddress>>22)&0x3FF)*4)
	if (pde & STRANAPrisutna) == 0 {
		return false
	}
	pteaddress := (pde & STRANAOkvir) + ((virtuelnoaddress>>12)&0x3FF)*4
	pte := GetVrednost(pteaddress)
	if (pte & STRANAPrisutna) == 0 {
		return false
	}
	if (pte & STRANAcow) == 0 {
		return (pte & STRANAwritable) != 0
	}
	if AktivnaMemorijamanager == nil {
		return false
	}
	novaPokazivač, _ := AktivnaMemorijamanager.Alignedmalloc(0x1000)
	if novaPokazivač == nil {
		return false
	}
	novaOkvir := uint32(uintptr(novaPokazivač)) & STRANAOkvir
	izvor_2 := GetBajtovasaPokazivač(uintptr(virtuelnoaddress&STRANAOkvir), 0x1000, 0x1000)
	odredište_2 := GetBajtovasaPokazivač(uintptr(novaOkvir), 0x1000, 0x1000)
	copy(odredište_2, izvor_2)
	cowOkvirmanager.Decrement(pte & STRANAOkvir)
	Skupunsignedinteger32ataddress((novaOkvir|(pte&0xFFF)|STRANAwritable)&^STRANAcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	osvežicr3()
	return true
}

func makeOpsegPrivatnowritableTrenutno(sTRANADirektorijum uint32, address uint32, veličina uint32) bool {
	if veličina == 0 {
		return true
	}
	zadnja := address + veličina - 1
	if zadnja < address {
		return false
	}
	for sTRANA := address & STRANAOkvir; ; sTRANA += 0x1000 {
		if !makeSTRANAPrivatnowritableTrenutno(sTRANADirektorijum, sTRANA) {
			return false
		}
		if sTRANA == (zadnja & STRANAOkvir) {
			break
		}
	}
	return true
}

func MakeOpsegPrivatnowritable(sTRANADirektorijum uint32, address uint32, veličina uint32) bool {
	if sTRANADirektorijum == 0 {
		return false
	}
	oldcr3 := getcr3()
	skupcr3(sTRANADirektorijum)
	uredu := makeOpsegPrivatnowritableTrenutno(sTRANADirektorijum, address, veličina)
	skupcr3(oldcr3)
	return uredu
}

func Skupunsignedinteger32PrimljenoSTRANADirektorijum(x uint32, address uint32, sTRANADirektorijum uint32) {
	if sTRANADirektorijum == 0 {
		return
	}
	oldcr3 := getcr3()
	skupcr3(sTRANADirektorijum)
	Skupunsignedinteger32ataddress(x, address)
	skupcr3(oldcr3)
}

func GetVrednost(address uint32) uint32 {
	var orgVrednost uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgVrednost
}
func GetVrednostPrimljenoSTRANADirektorijum(address uint32, sTRANADirektorijum uint32) uint32 {
	if sTRANADirektorijum == 0 {
		return 0
	}
	oldcr3 := getcr3()
	skupcr3(sTRANADirektorijum)
	v := GetVrednost(address)
	skupcr3(oldcr3)
	return v
}

var v uint32 = 0

func UmnožiSTRANAOkvirBlok(xSTRANADirektorijum uint32, ySTRANADirektorijum uint32, vaddress uint32) {
	if xSTRANADirektorijum == 0 || ySTRANADirektorijum == 0 {
		return
	}
	oldcr3 := getcr3()
	skupcr3(xSTRANADirektorijum)
	v = GetVrednost(vaddress)
	Skupunsignedinteger32PrimljenoSTRANADirektorijum(v, vaddress, ySTRANADirektorijum)

	skupcr3(oldcr3)
}
