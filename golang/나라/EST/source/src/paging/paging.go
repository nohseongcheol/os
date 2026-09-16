/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "katkestus"
import . "mälumanager"
import . "util"

type LehekülgKataloogkirje_2 uintptr

const (
	LehekülgOlemas		uint32	= 0x001
	Lehekülgwritable	uint32	= 0x002
	LehekülgKasutaja	uint32	= 0x004
	LehekülgRaam		uint32	= 0xFFFFF000
	Lehekülgcow		uint32	= 0x200
)

func Määrabyteataddress(x byte, address uint32)
func Määraunsignedinteger8ataddress(x uint8, address uint32)
func Määraunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func määracr3(lehekülgKataloog uint32)
func getcr3() uint32

type Paging struct {
	TKatkestushandler
}
type TcowRaammanager struct {
	mem		*TMälumanager
	refs		[]uint16
	raamcount	uint32
}

var (
	LehekülgKataloogkirje	uintptr
	LehekülgTabelkirje	uint32
	pdelen			uint32
	virtlen			uint32
	cowRaammanager		TcowRaammanager
)

func (ise *TcowRaammanager) Init(mem *TMälumanager, raamcount uint32) bool {
	ise.mem = mem
	ise.raamcount = raamcount
	referencebaiti := raamcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceKursor := mem.Malloc(referencebaiti)
	if referenceKursor == nil {
		ise.refs = nil
		ise.raamcount = 0
		return false
	}
	ise.refs = (*[1 << 28]uint16)(referenceKursor)[:raamcount:raamcount]
	for i := uint32(0); i < raamcount; i++ {
		ise.refs[i] = 0
	}
	return true
}

func (ise *TcowRaammanager) Reference(raam uint32) uint16 {
	idx := raam >> 12
	if idx >= ise.raamcount || ise.refs == nil {
		return 0
	}
	return ise.refs[idx]
}

func (ise *TcowRaammanager) Increment(raam uint32) {
	idx := raam >> 12
	if idx >= ise.raamcount || ise.refs == nil {
		return
	}
	if ise.refs[idx] == 0 {
		ise.refs[idx] = 2
	} else {
		ise.refs[idx]++
	}
}

func (ise *TcowRaammanager) Decrement(raam uint32) {
	idx := raam >> 12
	if idx >= ise.raamcount || ise.refs == nil || ise.refs[idx] == 0 {
		return
	}
	ise.refs[idx]--
}

func (ise *Paging) Init(lehekülgKataloogkirje uintptr, lehekülgTabelkirje uint32, mälumanager *TMälumanager) {

	LehekülgKataloogkirje = lehekülgKataloogkirje
	LehekülgTabelkirje = lehekülgTabelkirje

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRaammanager.Init(mälumanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressKursor, _ := mälumanager.Alignedmalloc(0x1000)
			if addressKursor == nil {
				return
			}
			address := uint32(uintptr(addressKursor))

			Määraunsignedinteger32ataddress(address|0x87, uint32(lehekülgKataloogkirje)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Määraunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		lehekülgKataloogkirje = lehekülgKataloogkirje + 0x1000
	}

}
func (ise *Paging) SharedMäluregion() {

	lehekülgKataloogkirje := LehekülgKataloogkirje
	kLehekülgKataloogkirje := LehekülgKataloogkirje

	for i := uint32(1); i <= virtlen; i++ {

		lehekülgKataloogkirje = lehekülgKataloogkirje + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVäärtus(uint32(kLehekülgKataloogkirje) + pde*4)
			v = (v & 0xFFFFF000)
			Määraunsignedinteger32ataddress(v|0x87, uint32(lehekülgKataloogkirje)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVäärtus(uint32(kLehekülgKataloogkirje) + pde*4)
			v = (v & 0xFFFFF000)
			Määraunsignedinteger32ataddress(v|0x87, uint32(lehekülgKataloogkirje)+pde*4)

		}

	}
}
func (ise *Paging) Lehekülgfault(manager *TKatkestusmanager) {
	katkestushandler = handlepagingKatkestus

	var address uintptr
	address = uintptr(unsafe.Pointer(&katkestushandler))
	ise.TKatkestushandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var katkestushandler func(uint32) uint32

func handlepagingKatkestus(esp uint32) uint32 {
	if ResolveKopeeriSeesKirjutaminefault() {
		return esp
	}
	return HandlefatalKatkestusRaam(esp, 0x0E)
}

func CloneaddressTühikcow(aLLIKASLehekülgKataloog uint32) uint32 {
	if AktiivneMälumanager == nil || aLLIKASLehekülgKataloog == 0 {
		return 0
	}
	sihtfailKursor, _ := AktiivneMälumanager.Alignedmalloc(0x1000)
	if sihtfailKursor == nil {
		return 0
	}
	sihtfailLehekülgKataloog := uint32(uintptr(sihtfailKursor))
	for i := uint32(0); i < 1024; i++ {
		Määraunsignedinteger32ataddress(0, sihtfailLehekülgKataloog+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		aLLIKASpdeaddress := aLLIKASLehekülgKataloog + pde*4
		aLLIKASpde := GetVäärtus(aLLIKASpdeaddress)
		if (aLLIKASpde & LehekülgOlemas) == 0 {
			continue
		}
		if issharedpde(pde) {
			Määraunsignedinteger32ataddress(aLLIKASpde, sihtfailLehekülgKataloog+pde*4)
			continue
		}

		sihtfailptKursor, _ := AktiivneMälumanager.Alignedmalloc(0x1000)
		if sihtfailptKursor == nil {
			continue
		}
		aLLIKASpt := aLLIKASpde & LehekülgRaam
		sihtfailpt := uint32(uintptr(sihtfailptKursor))
		Määraunsignedinteger32ataddress((sihtfailpt | (aLLIKASpde & 0xFFF)), sihtfailLehekülgKataloog+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := aLLIKASpt + pte*4
			kirje := GetVäärtus(pteaddress)
			if (kirje & LehekülgOlemas) != 0 {
				if (kirje & Lehekülgwritable) != 0 {
					kirje = (kirje &^ Lehekülgwritable) | Lehekülgcow
					Määraunsignedinteger32ataddress(kirje, pteaddress)
					cowRaammanager.Increment(kirje & LehekülgRaam)
				} else if (kirje & Lehekülgcow) != 0 {
					cowRaammanager.Increment(kirje & LehekülgRaam)
				}
			}
			Määraunsignedinteger32ataddress(kirje, sihtfailpt+pte*4)
		}
	}
	laadiuuesticr3()
	return sihtfailLehekülgKataloog
}

func ResolveKopeeriSeesKirjutaminefault() bool {
	if AktiivneMälumanager == nil {
		return false
	}
	faultaddress := getcr2()
	lehekülgKataloog := getcr3()
	pdeaddress := lehekülgKataloog + ((faultaddress>>22)&0x3FF)*4
	pde := GetVäärtus(pdeaddress)
	if (pde & LehekülgOlemas) == 0 {
		return false
	}
	pt := pde & LehekülgRaam
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetVäärtus(pteaddress)
	if (pte&Lehekülgcow) == 0 || (pte&LehekülgOlemas) == 0 {
		return false
	}
	oldRaam := pte & LehekülgRaam
	if cowRaammanager.Reference(oldRaam) <= 1 {
		Määraunsignedinteger32ataddress((pte|Lehekülgwritable)&^Lehekülgcow, pteaddress)
		laadiuuesticr3()
		return true
	}

	uusKursor, _ := AktiivneMälumanager.Alignedmalloc(0x1000)
	if uusKursor == nil {
		return false
	}
	uusRaam := uint32(uintptr(uusKursor)) & LehekülgRaam

	aLLIKAS_2 := GetbaitifromKursor(uintptr(faultaddress&LehekülgRaam), 0x1000, 0x1000)
	sihtfail_2 := GetbaitifromKursor(uintptr(uusRaam), 0x1000, 0x1000)
	copy(sihtfail_2, aLLIKAS_2)
	cowRaammanager.Decrement(oldRaam)
	Määraunsignedinteger32ataddress((uusRaam|(pte&0xFFF)|Lehekülgwritable)&^Lehekülgcow, pteaddress)
	laadiuuesticr3()
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

func laadiuuesticr3() {
	cr3 := getcr3()
	määracr3(cr3)
}

func MäärabyteSisseLehekülgKataloog(x byte, address uint32, lehekülgKataloog uint32) {
	oldcr3 := getcr3()
	määracr3(lehekülgKataloog)
	Määrabyteataddress(x, address)
	määracr3(oldcr3)
}

func MääraKastSisseLehekülgKataloog(aLLIKAS_2 []byte, sihtfail_2 []byte, suurus uint32, lehekülgKataloog uint32) {
	if suurus == 0 || lehekülgKataloog == 0 {
		return
	}
	oldcr3 := getcr3()
	määracr3(lehekülgKataloog)
	makeVahemikPrivaatwritableKäesolev(lehekülgKataloog, uint32(uintptr(unsafe.Pointer(&sihtfail_2[0]))), suurus)

	for i := uint32(0); i < suurus; i++ {
		sihtfail_2[i] = aLLIKAS_2[i]
	}
	määracr3(oldcr3)
}

func ZeroKastSisseLehekülgKataloog(address uint32, suurus uint32, lehekülgKataloog uint32) {
	if suurus == 0 || lehekülgKataloog == 0 {
		return
	}
	oldcr3 := getcr3()
	määracr3(lehekülgKataloog)
	makeVahemikPrivaatwritableKäesolev(lehekülgKataloog, address, suurus)
	sihtfail_2 := GetbaitifromKursor(uintptr(address), int(suurus), int(suurus))
	for i := uint32(0); i < suurus; i++ {
		sihtfail_2[i] = 0
	}
	määracr3(oldcr3)
}

func makeLehekülgPrivaatwritableKäesolev(lehekülgKataloog uint32, virtuaaladdress uint32) bool {
	pde := GetVäärtus(lehekülgKataloog + ((virtuaaladdress>>22)&0x3FF)*4)
	if (pde & LehekülgOlemas) == 0 {
		return false
	}
	pteaddress := (pde & LehekülgRaam) + ((virtuaaladdress>>12)&0x3FF)*4
	pte := GetVäärtus(pteaddress)
	if (pte & LehekülgOlemas) == 0 {
		return false
	}
	if (pte & Lehekülgcow) == 0 {
		return (pte & Lehekülgwritable) != 0
	}
	if AktiivneMälumanager == nil {
		return false
	}
	uusKursor, _ := AktiivneMälumanager.Alignedmalloc(0x1000)
	if uusKursor == nil {
		return false
	}
	uusRaam := uint32(uintptr(uusKursor)) & LehekülgRaam
	aLLIKAS_2 := GetbaitifromKursor(uintptr(virtuaaladdress&LehekülgRaam), 0x1000, 0x1000)
	sihtfail_2 := GetbaitifromKursor(uintptr(uusRaam), 0x1000, 0x1000)
	copy(sihtfail_2, aLLIKAS_2)
	cowRaammanager.Decrement(pte & LehekülgRaam)
	Määraunsignedinteger32ataddress((uusRaam|(pte&0xFFF)|Lehekülgwritable)&^Lehekülgcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	laadiuuesticr3()
	return true
}

func makeVahemikPrivaatwritableKäesolev(lehekülgKataloog uint32, address uint32, suurus uint32) bool {
	if suurus == 0 {
		return true
	}
	eelmine := address + suurus - 1
	if eelmine < address {
		return false
	}
	for lehekülg := address & LehekülgRaam; ; lehekülg += 0x1000 {
		if !makeLehekülgPrivaatwritableKäesolev(lehekülgKataloog, lehekülg) {
			return false
		}
		if lehekülg == (eelmine & LehekülgRaam) {
			break
		}
	}
	return true
}

func MakeVahemikPrivaatwritable(lehekülgKataloog uint32, address uint32, suurus uint32) bool {
	if lehekülgKataloog == 0 {
		return false
	}
	oldcr3 := getcr3()
	määracr3(lehekülgKataloog)
	olgu := makeVahemikPrivaatwritableKäesolev(lehekülgKataloog, address, suurus)
	määracr3(oldcr3)
	return olgu
}

func Määraunsignedinteger32SisseLehekülgKataloog(x uint32, address uint32, lehekülgKataloog uint32) {
	if lehekülgKataloog == 0 {
		return
	}
	oldcr3 := getcr3()
	määracr3(lehekülgKataloog)
	Määraunsignedinteger32ataddress(x, address)
	määracr3(oldcr3)
}

func GetVäärtus(address uint32) uint32 {
	var orgVäärtus uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgVäärtus
}
func GetVäärtusSisseLehekülgKataloog(address uint32, lehekülgKataloog uint32) uint32 {
	if lehekülgKataloog == 0 {
		return 0
	}
	oldcr3 := getcr3()
	määracr3(lehekülgKataloog)
	v := GetVäärtus(address)
	määracr3(oldcr3)
	return v
}

var v uint32 = 0

func KopeeriLehekülgRaamKast(xLehekülgKataloog uint32, yLehekülgKataloog uint32, vaddress uint32) {
	if xLehekülgKataloog == 0 || yLehekülgKataloog == 0 {
		return
	}
	oldcr3 := getcr3()
	määracr3(xLehekülgKataloog)
	v = GetVäärtus(vaddress)
	Määraunsignedinteger32SisseLehekülgKataloog(v, vaddress, yLehekülgKataloog)

	määracr3(oldcr3)
}
