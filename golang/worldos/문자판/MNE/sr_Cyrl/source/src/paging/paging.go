/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "ометање"
import . "меморијаmanager"
import . "util"

type СТРАНАДиректоријумунос_2 uintptr

const (
	СТРАНАПрисутна	uint32	= 0x001
	СТРАНАwritable	uint32	= 0x002
	СТРАНАКорисник	uint32	= 0x004
	СТРАНАОквир	uint32	= 0xFFFFF000
	СТРАНАcow		uint32	= 0x200
)

func Скупbyteataddress(x byte, address uint32)
func Скупunsignedinteger8ataddress(x uint8, address uint32)
func Скупunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func скупcr3(сТРАНАДиректоријум uint32)
func getcr3() uint32

type Paging struct {
	TОметањеhandler
}
type TcowОквирmanager struct {
	mem		*TМеморијаmanager
	refs		[]uint16
	оквирcount	uint32
}

var (
	СТРАНАДиректоријумунос	uintptr
	СТРАНАТабелаунос		uint32
	pdelen			uint32
	virtlen			uint32
	cowОквирmanager		TcowОквирmanager
)

func (исти *TcowОквирmanager) Init(mem *TМеморијаmanager, оквирcount uint32) bool {
	исти.mem = mem
	исти.оквирcount = оквирcount
	referenceБајтова := оквирcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceПоказивач := mem.Malloc(referenceБајтова)
	if referenceПоказивач == nil {
		исти.refs = nil
		исти.оквирcount = 0
		return false
	}
	исти.refs = (*[1 << 28]uint16)(referenceПоказивач)[:оквирcount:оквирcount]
	for i := uint32(0); i < оквирcount; i++ {
		исти.refs[i] = 0
	}
	return true
}

func (исти *TcowОквирmanager) Reference(оквир uint32) uint16 {
	idx := оквир >> 12
	if idx >= исти.оквирcount || исти.refs == nil {
		return 0
	}
	return исти.refs[idx]
}

func (исти *TcowОквирmanager) Increment(оквир uint32) {
	idx := оквир >> 12
	if idx >= исти.оквирcount || исти.refs == nil {
		return
	}
	if исти.refs[idx] == 0 {
		исти.refs[idx] = 2
	} else {
		исти.refs[idx]++
	}
}

func (исти *TcowОквирmanager) Decrement(оквир uint32) {
	idx := оквир >> 12
	if idx >= исти.оквирcount || исти.refs == nil || исти.refs[idx] == 0 {
		return
	}
	исти.refs[idx]--
}

func (исти *Paging) Init(сТРАНАДиректоријумунос uintptr, сТРАНАТабелаунос uint32, меморијаmanager *TМеморијаmanager) {

	СТРАНАДиректоријумунос = сТРАНАДиректоријумунос
	СТРАНАТабелаунос = сТРАНАТабелаунос

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowОквирmanager.Init(меморијаmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressПоказивач, _ := меморијаmanager.Alignedmalloc(0x1000)
			if addressПоказивач == nil {
				return
			}
			address := uint32(uintptr(addressПоказивач))

			Скупunsignedinteger32ataddress(address|0x87, uint32(сТРАНАДиректоријумунос)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Скупunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		сТРАНАДиректоријумунос = сТРАНАДиректоријумунос + 0x1000
	}

}
func (исти *Paging) SharedМеморијаregion() {

	сТРАНАДиректоријумунос := СТРАНАДиректоријумунос
	kСТРАНАДиректоријумунос := СТРАНАДиректоријумунос

	for i := uint32(1); i <= virtlen; i++ {

		сТРАНАДиректоријумунос = сТРАНАДиректоријумунос + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetВредност(uint32(kСТРАНАДиректоријумунос) + pde*4)
			v = (v & 0xFFFFF000)
			Скупunsignedinteger32ataddress(v|0x87, uint32(сТРАНАДиректоријумунос)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetВредност(uint32(kСТРАНАДиректоријумунос) + pde*4)
			v = (v & 0xFFFFF000)
			Скупunsignedinteger32ataddress(v|0x87, uint32(сТРАНАДиректоријумунос)+pde*4)

		}

	}
}
func (исти *Paging) СТРАНАfault(manager *TОметањеmanager) {
	ометањеhandler = ручкаpagingОметање

	var address uintptr
	address = uintptr(unsafe.Pointer(&ометањеhandler))
	исти.TОметањеhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var ометањеhandler func(uint32) uint32

func ручкаpagingОметање(esp uint32) uint32 {
	if ResolveУмножинаПишеfault() {
		return esp
	}
	return РучкаfatalОметањеОквир(esp, 0x0E)
}

func Cloneaddressразмакcow(изворСТРАНАДиректоријум uint32) uint32 {
	if АктивнаМеморијаmanager == nil || изворСТРАНАДиректоријум == 0 {
		return 0
	}
	одредиштеПоказивач, _ := АктивнаМеморијаmanager.Alignedmalloc(0x1000)
	if одредиштеПоказивач == nil {
		return 0
	}
	одредиштеСТРАНАДиректоријум := uint32(uintptr(одредиштеПоказивач))
	for i := uint32(0); i < 1024; i++ {
		Скупunsignedinteger32ataddress(0, одредиштеСТРАНАДиректоријум+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		изворpdeaddress := изворСТРАНАДиректоријум + pde*4
		изворpde := GetВредност(изворpdeaddress)
		if (изворpde & СТРАНАПрисутна) == 0 {
			continue
		}
		if issharedpde(pde) {
			Скупunsignedinteger32ataddress(изворpde, одредиштеСТРАНАДиректоријум+pde*4)
			continue
		}

		одредиштеptПоказивач, _ := АктивнаМеморијаmanager.Alignedmalloc(0x1000)
		if одредиштеptПоказивач == nil {
			continue
		}
		изворpt := изворpde & СТРАНАОквир
		одредиштеpt := uint32(uintptr(одредиштеptПоказивач))
		Скупunsignedinteger32ataddress((одредиштеpt | (изворpde & 0xFFF)), одредиштеСТРАНАДиректоријум+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := изворpt + pte*4
			унос := GetВредност(pteaddress)
			if (унос & СТРАНАПрисутна) != 0 {
				if (унос & СТРАНАwritable) != 0 {
					унос = (унос &^ СТРАНАwritable) | СТРАНАcow
					Скупunsignedinteger32ataddress(унос, pteaddress)
					cowОквирmanager.Increment(унос & СТРАНАОквир)
				} else if (унос & СТРАНАcow) != 0 {
					cowОквирmanager.Increment(унос & СТРАНАОквир)
				}
			}
			Скупunsignedinteger32ataddress(унос, одредиштеpt+pte*4)
		}
	}
	освежиcr3()
	return одредиштеСТРАНАДиректоријум
}

func ResolveУмножинаПишеfault() bool {
	if АктивнаМеморијаmanager == nil {
		return false
	}
	faultaddress := getcr2()
	сТРАНАДиректоријум := getcr3()
	pdeaddress := сТРАНАДиректоријум + ((faultaddress>>22)&0x3FF)*4
	pde := GetВредност(pdeaddress)
	if (pde & СТРАНАПрисутна) == 0 {
		return false
	}
	pt := pde & СТРАНАОквир
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetВредност(pteaddress)
	if (pte&СТРАНАcow) == 0 || (pte&СТРАНАПрисутна) == 0 {
		return false
	}
	oldОквир := pte & СТРАНАОквир
	if cowОквирmanager.Reference(oldОквир) <= 1 {
		Скупunsignedinteger32ataddress((pte|СТРАНАwritable)&^СТРАНАcow, pteaddress)
		освежиcr3()
		return true
	}

	новаПоказивач, _ := АктивнаМеморијаmanager.Alignedmalloc(0x1000)
	if новаПоказивач == nil {
		return false
	}
	новаОквир := uint32(uintptr(новаПоказивач)) & СТРАНАОквир

	извор_2 := GetБајтовасаПоказивач(uintptr(faultaddress&СТРАНАОквир), 0x1000, 0x1000)
	одредиште_2 := GetБајтовасаПоказивач(uintptr(новаОквир), 0x1000, 0x1000)
	copy(одредиште_2, извор_2)
	cowОквирmanager.Decrement(oldОквир)
	Скупunsignedinteger32ataddress((новаОквир|(pte&0xFFF)|СТРАНАwritable)&^СТРАНАcow, pteaddress)
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

func СкупbyteПримљеноСТРАНАДиректоријум(x byte, address uint32, сТРАНАДиректоријум uint32) {
	oldcr3 := getcr3()
	скупcr3(сТРАНАДиректоријум)
	Скупbyteataddress(x, address)
	скупcr3(oldcr3)
}

func СкупБлокПримљеноСТРАНАДиректоријум(извор_2 []byte, одредиште_2 []byte, величина uint32, сТРАНАДиректоријум uint32) {
	if величина == 0 || сТРАНАДиректоријум == 0 {
		return
	}
	oldcr3 := getcr3()
	скупcr3(сТРАНАДиректоријум)
	makeОпсегПриватноwritableТренутно(сТРАНАДиректоријум, uint32(uintptr(unsafe.Pointer(&одредиште_2[0]))), величина)

	for i := uint32(0); i < величина; i++ {
		одредиште_2[i] = извор_2[i]
	}
	скупcr3(oldcr3)
}

func ZeroБлокПримљеноСТРАНАДиректоријум(address uint32, величина uint32, сТРАНАДиректоријум uint32) {
	if величина == 0 || сТРАНАДиректоријум == 0 {
		return
	}
	oldcr3 := getcr3()
	скупcr3(сТРАНАДиректоријум)
	makeОпсегПриватноwritableТренутно(сТРАНАДиректоријум, address, величина)
	одредиште_2 := GetБајтовасаПоказивач(uintptr(address), int(величина), int(величина))
	for i := uint32(0); i < величина; i++ {
		одредиште_2[i] = 0
	}
	скупcr3(oldcr3)
}

func makeСТРАНАПриватноwritableТренутно(сТРАНАДиректоријум uint32, виртуелноaddress uint32) bool {
	pde := GetВредност(сТРАНАДиректоријум + ((виртуелноaddress>>22)&0x3FF)*4)
	if (pde & СТРАНАПрисутна) == 0 {
		return false
	}
	pteaddress := (pde & СТРАНАОквир) + ((виртуелноaddress>>12)&0x3FF)*4
	pte := GetВредност(pteaddress)
	if (pte & СТРАНАПрисутна) == 0 {
		return false
	}
	if (pte & СТРАНАcow) == 0 {
		return (pte & СТРАНАwritable) != 0
	}
	if АктивнаМеморијаmanager == nil {
		return false
	}
	новаПоказивач, _ := АктивнаМеморијаmanager.Alignedmalloc(0x1000)
	if новаПоказивач == nil {
		return false
	}
	новаОквир := uint32(uintptr(новаПоказивач)) & СТРАНАОквир
	извор_2 := GetБајтовасаПоказивач(uintptr(виртуелноaddress&СТРАНАОквир), 0x1000, 0x1000)
	одредиште_2 := GetБајтовасаПоказивач(uintptr(новаОквир), 0x1000, 0x1000)
	copy(одредиште_2, извор_2)
	cowОквирmanager.Decrement(pte & СТРАНАОквир)
	Скупunsignedinteger32ataddress((новаОквир|(pte&0xFFF)|СТРАНАwritable)&^СТРАНАcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	освежиcr3()
	return true
}

func makeОпсегПриватноwritableТренутно(сТРАНАДиректоријум uint32, address uint32, величина uint32) bool {
	if величина == 0 {
		return true
	}
	задња := address + величина - 1
	if задња < address {
		return false
	}
	for сТРАНА := address & СТРАНАОквир; ; сТРАНА += 0x1000 {
		if !makeСТРАНАПриватноwritableТренутно(сТРАНАДиректоријум, сТРАНА) {
			return false
		}
		if сТРАНА == (задња & СТРАНАОквир) {
			break
		}
	}
	return true
}

func MakeОпсегПриватноwritable(сТРАНАДиректоријум uint32, address uint32, величина uint32) bool {
	if сТРАНАДиректоријум == 0 {
		return false
	}
	oldcr3 := getcr3()
	скупcr3(сТРАНАДиректоријум)
	уреду := makeОпсегПриватноwritableТренутно(сТРАНАДиректоријум, address, величина)
	скупcr3(oldcr3)
	return уреду
}

func Скупunsignedinteger32ПримљеноСТРАНАДиректоријум(x uint32, address uint32, сТРАНАДиректоријум uint32) {
	if сТРАНАДиректоријум == 0 {
		return
	}
	oldcr3 := getcr3()
	скупcr3(сТРАНАДиректоријум)
	Скупunsignedinteger32ataddress(x, address)
	скупcr3(oldcr3)
}

func GetВредност(address uint32) uint32 {
	var orgВредност uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgВредност
}
func GetВредностПримљеноСТРАНАДиректоријум(address uint32, сТРАНАДиректоријум uint32) uint32 {
	if сТРАНАДиректоријум == 0 {
		return 0
	}
	oldcr3 := getcr3()
	скупcr3(сТРАНАДиректоријум)
	v := GetВредност(address)
	скупcr3(oldcr3)
	return v
}

var v uint32 = 0

func УмножиСТРАНАОквирБлок(xСТРАНАДиректоријум uint32, yСТРАНАДиректоријум uint32, vaddress uint32) {
	if xСТРАНАДиректоријум == 0 || yСТРАНАДиректоријум == 0 {
		return
	}
	oldcr3 := getcr3()
	скупcr3(xСТРАНАДиректоријум)
	v = GetВредност(vaddress)
	Скупunsignedinteger32ПримљеноСТРАНАДиректоријум(v, vaddress, yСТРАНАДиректоријум)

	скупcr3(oldcr3)
}
