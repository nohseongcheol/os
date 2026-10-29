/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "ընդհատել"
import . "հիշողությունmanager"
import . "util"

type Էջֆայլապանակentry_2 uintptr

const (
	ԷջՆերկա		uint32	= 0x001
	Էջwritable	uint32	= 0x002
	ԷջՕգտագործող	uint32	= 0x004
	ԷջՇրջանակ	uint32	= 0xFFFFF000
	Էջcow		uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(էջֆայլապանակ uint32)
func getcr3() uint32

type Paging struct {
	TԸնդհատելhandler
}
type TcowՇրջանակmanager struct {
	mem		*TՀիշողությունmanager
	refs		[]uint16
	շրջանակcount	uint32
}

var (
	Էջֆայլապանակentry	uintptr
	ԷջԱղյուսակentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowՇրջանակmanager	TcowՇրջանակmanager
)

func (ինքնուրույն *TcowՇրջանակmanager) Init(mem *TՀիշողությունmanager, շրջանակcount uint32) bool {
	ինքնուրույն.mem = mem
	ինքնուրույն.շրջանակcount = շրջանակcount
	referenceԲայթեր := շրջանակcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceՑուցիչ := mem.Malloc(referenceԲայթեր)
	if referenceՑուցիչ == nil {
		ինքնուրույն.refs = nil
		ինքնուրույն.շրջանակcount = 0
		return false
	}
	ինքնուրույն.refs = (*[1 << 28]uint16)(referenceՑուցիչ)[:շրջանակcount:շրջանակcount]
	for i := uint32(0); i < շրջանակcount; i++ {
		ինքնուրույն.refs[i] = 0
	}
	return true
}

func (ինքնուրույն *TcowՇրջանակmanager) Reference(շրջանակ uint32) uint16 {
	idx := շրջանակ >> 12
	if idx >= ինքնուրույն.շրջանակcount || ինքնուրույն.refs == nil {
		return 0
	}
	return ինքնուրույն.refs[idx]
}

func (ինքնուրույն *TcowՇրջանակmanager) Increment(շրջանակ uint32) {
	idx := շրջանակ >> 12
	if idx >= ինքնուրույն.շրջանակcount || ինքնուրույն.refs == nil {
		return
	}
	if ինքնուրույն.refs[idx] == 0 {
		ինքնուրույն.refs[idx] = 2
	} else {
		ինքնուրույն.refs[idx]++
	}
}

func (ինքնուրույն *TcowՇրջանակmanager) Decrement(շրջանակ uint32) {
	idx := շրջանակ >> 12
	if idx >= ինքնուրույն.շրջանակcount || ինքնուրույն.refs == nil || ինքնուրույն.refs[idx] == 0 {
		return
	}
	ինքնուրույն.refs[idx]--
}

func (ինքնուրույն *Paging) Init(էջֆայլապանակentry uintptr, էջԱղյուսակentry uint32, հիշողությունmanager *TՀիշողությունmanager) {

	Էջֆայլապանակentry = էջֆայլապանակentry
	ԷջԱղյուսակentry = էջԱղյուսակentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowՇրջանակmanager.Init(հիշողությունmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressՑուցիչ, _ := հիշողությունmanager.Alignedmalloc(0x1000)
			if addressՑուցիչ == nil {
				return
			}
			address := uint32(uintptr(addressՑուցիչ))

			Setunsignedinteger32ataddress(address|0x87, uint32(էջֆայլապանակentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		էջֆայլապանակentry = էջֆայլապանակentry + 0x1000
	}

}
func (ինքնուրույն *Paging) SharedՀիշողությունregion() {

	էջֆայլապանակentry := Էջֆայլապանակentry
	kԷջֆայլապանակentry := Էջֆայլապանակentry

	for i := uint32(1); i <= virtlen; i++ {

		էջֆայլապանակentry = էջֆայլապանակentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetԱրժեք(uint32(kԷջֆայլապանակentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(էջֆայլապանակentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetԱրժեք(uint32(kԷջֆայլապանակentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(էջֆայլապանակentry)+pde*4)

		}

	}
}
func (ինքնուրույն *Paging) Էջfault(manager *TԸնդհատելmanager) {
	ընդհատելhandler = handlepagingԸնդհատել

	var address uintptr
	address = uintptr(unsafe.Pointer(&ընդհատելhandler))
	ինքնուրույն.TԸնդհատելhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var ընդհատելhandler func(uint32) uint32

func handlepagingԸնդհատել(esp uint32) uint32 {
	if ResolveՊատճենելՄիացնելԳրելfault() {
		return esp
	}
	return HandlefatalԸնդհատելՇրջանակ(esp, 0x0E)
}

func CloneaddressԲացատcow(աղբյուրԷջֆայլապանակ uint32) uint32 {
	if ԱկտիվՀիշողությունmanager == nil || աղբյուրԷջֆայլապանակ == 0 {
		return 0
	}
	destinationՑուցիչ, _ := ԱկտիվՀիշողությունmanager.Alignedmalloc(0x1000)
	if destinationՑուցիչ == nil {
		return 0
	}
	destinationԷջֆայլապանակ := uint32(uintptr(destinationՑուցիչ))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationԷջֆայլապանակ+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		աղբյուրpdeaddress := աղբյուրԷջֆայլապանակ + pde*4
		աղբյուրpde := GetԱրժեք(աղբյուրpdeaddress)
		if (աղբյուրpde & ԷջՆերկա) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(աղբյուրpde, destinationԷջֆայլապանակ+pde*4)
			continue
		}

		destinationptՑուցիչ, _ := ԱկտիվՀիշողությունmanager.Alignedmalloc(0x1000)
		if destinationptՑուցիչ == nil {
			continue
		}
		աղբյուրpt := աղբյուրpde & ԷջՇրջանակ
		destinationpt := uint32(uintptr(destinationptՑուցիչ))
		Setunsignedinteger32ataddress((destinationpt | (աղբյուրpde & 0xFFF)), destinationԷջֆայլապանակ+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := աղբյուրpt + pte*4
			entry := GetԱրժեք(pteaddress)
			if (entry & ԷջՆերկա) != 0 {
				if (entry & Էջwritable) != 0 {
					entry = (entry &^ Էջwritable) | Էջcow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowՇրջանակmanager.Increment(entry & ԷջՇրջանակ)
				} else if (entry & Էջcow) != 0 {
					cowՇրջանակmanager.Increment(entry & ԷջՇրջանակ)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	վերբեռնելcr3()
	return destinationԷջֆայլապանակ
}

func ResolveՊատճենելՄիացնելԳրելfault() bool {
	if ԱկտիվՀիշողությունmanager == nil {
		return false
	}
	faultaddress := getcr2()
	էջֆայլապանակ := getcr3()
	pdeaddress := էջֆայլապանակ + ((faultaddress>>22)&0x3FF)*4
	pde := GetԱրժեք(pdeaddress)
	if (pde & ԷջՆերկա) == 0 {
		return false
	}
	pt := pde & ԷջՇրջանակ
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetԱրժեք(pteaddress)
	if (pte&Էջcow) == 0 || (pte&ԷջՆերկա) == 0 {
		return false
	}
	oldՇրջանակ := pte & ԷջՇրջանակ
	if cowՇրջանակmanager.Reference(oldՇրջանակ) <= 1 {
		Setunsignedinteger32ataddress((pte|Էջwritable)&^Էջcow, pteaddress)
		վերբեռնելcr3()
		return true
	}

	նորՑուցիչ, _ := ԱկտիվՀիշողությունmanager.Alignedmalloc(0x1000)
	if նորՑուցիչ == nil {
		return false
	}
	նորՇրջանակ := uint32(uintptr(նորՑուցիչ)) & ԷջՇրջանակ

	աղբյուր_2 := GetԲայթերիցՑուցիչ(uintptr(faultaddress&ԷջՇրջանակ), 0x1000, 0x1000)
	destination_2 := GetԲայթերիցՑուցիչ(uintptr(նորՇրջանակ), 0x1000, 0x1000)
	copy(destination_2, աղբյուր_2)
	cowՇրջանակmanager.Decrement(oldՇրջանակ)
	Setunsignedinteger32ataddress((նորՇրջանակ|(pte&0xFFF)|Էջwritable)&^Էջcow, pteaddress)
	վերբեռնելcr3()
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

func վերբեռնելcr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func SetbyteՄեջԷջֆայլապանակ(x byte, address uint32, էջֆայլապանակ uint32) {
	oldcr3 := getcr3()
	setcr3(էջֆայլապանակ)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func SetԱրգելափակելՄեջԷջֆայլապանակ(աղբյուր_2 []byte, destination_2 []byte, չափս uint32, էջֆայլապանակ uint32) {
	if չափս == 0 || էջֆայլապանակ == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(էջֆայլապանակ)
	makeՄիջակայքprivatewritablecurrent(էջֆայլապանակ, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), չափս)

	for i := uint32(0); i < չափս; i++ {
		destination_2[i] = աղբյուր_2[i]
	}
	setcr3(oldcr3)
}

func ZeroԱրգելափակելՄեջԷջֆայլապանակ(address uint32, չափս uint32, էջֆայլապանակ uint32) {
	if չափս == 0 || էջֆայլապանակ == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(էջֆայլապանակ)
	makeՄիջակայքprivatewritablecurrent(էջֆայլապանակ, address, չափս)
	destination_2 := GetԲայթերիցՑուցիչ(uintptr(address), int(չափս), int(չափս))
	for i := uint32(0); i < չափս; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makeԷջprivatewritablecurrent(էջֆայլապանակ uint32, virtualaddress uint32) bool {
	pde := GetԱրժեք(էջֆայլապանակ + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & ԷջՆերկա) == 0 {
		return false
	}
	pteaddress := (pde & ԷջՇրջանակ) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetԱրժեք(pteaddress)
	if (pte & ԷջՆերկա) == 0 {
		return false
	}
	if (pte & Էջcow) == 0 {
		return (pte & Էջwritable) != 0
	}
	if ԱկտիվՀիշողությունmanager == nil {
		return false
	}
	նորՑուցիչ, _ := ԱկտիվՀիշողությունmanager.Alignedmalloc(0x1000)
	if նորՑուցիչ == nil {
		return false
	}
	նորՇրջանակ := uint32(uintptr(նորՑուցիչ)) & ԷջՇրջանակ
	աղբյուր_2 := GetԲայթերիցՑուցիչ(uintptr(virtualaddress&ԷջՇրջանակ), 0x1000, 0x1000)
	destination_2 := GetԲայթերիցՑուցիչ(uintptr(նորՇրջանակ), 0x1000, 0x1000)
	copy(destination_2, աղբյուր_2)
	cowՇրջանակmanager.Decrement(pte & ԷջՇրջանակ)
	Setunsignedinteger32ataddress((նորՇրջանակ|(pte&0xFFF)|Էջwritable)&^Էջcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	վերբեռնելcr3()
	return true
}

func makeՄիջակայքprivatewritablecurrent(էջֆայլապանակ uint32, address uint32, չափս uint32) bool {
	if չափս == 0 {
		return true
	}
	վերջին := address + չափս - 1
	if վերջին < address {
		return false
	}
	for էջ := address & ԷջՇրջանակ; ; էջ += 0x1000 {
		if !makeԷջprivatewritablecurrent(էջֆայլապանակ, էջ) {
			return false
		}
		if էջ == (վերջին & ԷջՇրջանակ) {
			break
		}
	}
	return true
}

func MakeՄիջակայքprivatewritable(էջֆայլապանակ uint32, address uint32, չափս uint32) bool {
	if էջֆայլապանակ == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(էջֆայլապանակ)
	ok := makeՄիջակայքprivatewritablecurrent(էջֆայլապանակ, address, չափս)
	setcr3(oldcr3)
	return ok
}

func Setunsignedinteger32ՄեջԷջֆայլապանակ(x uint32, address uint32, էջֆայլապանակ uint32) {
	if էջֆայլապանակ == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(էջֆայլապանակ)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func GetԱրժեք(address uint32) uint32 {
	var orgԱրժեք uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgԱրժեք
}
func GetԱրժեքՄեջԷջֆայլապանակ(address uint32, էջֆայլապանակ uint32) uint32 {
	if էջֆայլապանակ == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(էջֆայլապանակ)
	v := GetԱրժեք(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func ՊատճենելԷջՇրջանակԱրգելափակել(xԷջֆայլապանակ uint32, yԷջֆայլապանակ uint32, vaddress uint32) {
	if xԷջֆայլապանակ == 0 || yԷջֆայլապանակ == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xԷջֆայլապանակ)
	v = GetԱրժեք(vaddress)
	Setunsignedinteger32ՄեջԷջֆայլապանակ(v, vaddress, yԷջֆայլապանակ)

	setcr3(oldcr3)
}
