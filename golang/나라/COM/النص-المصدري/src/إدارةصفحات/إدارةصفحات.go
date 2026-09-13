package إدارةصفحات

import unsafe "unsafe"
import . "مقاطعة"
import . "ذاكرةمدير"
import . "أداة"

type Pصفحةدليلentry_2 uintptr

const (
	Pصفحةالحالي	uint32	= 0x001
	Pصفحةwritable	uint32	= 0x002
	Pصفحةمستخدم	uint32	= 0x004
	Pصفحةإطار	uint32	= 0xFFFFF000
	Pصفحةcow	uint32	= 0x200
)

func Sتحديدبايتataddress(x byte, address uint32)
func Sتحديدunsignedinteger8ataddress(x uint8, address uint32)
func Sتحديدunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func تحديدcr3(دليل_الصفحات uint32)
func getcr3() uint32

type Pإدارةصفحات struct {
	Tمقاطعةhandler
}
type Tcowإطارمدير struct {
	mem		*Tذاكرةمدير
	refs		[]uint16
	إطارcount	uint32
}

var (
	Pصفحةدليلentry	uintptr
	Pصفحةجدولentry	uint32
	pdelen		uint32
	virtlen		uint32
	cowإطارمدير	Tcowإطارمدير
)

func (نفسه *Tcowإطارمدير) Init(mem *Tذاكرةمدير, إطارcount uint32) bool {
	نفسه.mem = mem
	نفسه.إطارcount = إطارcount
	referenceبايت := إطارcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceالمؤشر := mem.Mتخصيص_الذاكرة(referenceبايت)
	if referenceالمؤشر == nil {
		نفسه.refs = nil
		نفسه.إطارcount = 0
		return false
	}
	نفسه.refs = (*[1 << 28]uint16)(referenceالمؤشر)[:إطارcount:إطارcount]
	for i := uint32(0); i < إطارcount; i++ {
		نفسه.refs[i] = 0
	}
	return true
}

func (نفسه *Tcowإطارمدير) Reference(إطار uint32) uint16 {
	idx := إطار >> 12
	if idx >= نفسه.إطارcount || نفسه.refs == nil {
		return 0
	}
	return نفسه.refs[idx]
}

func (نفسه *Tcowإطارمدير) Increment(إطار uint32) {
	idx := إطار >> 12
	if idx >= نفسه.إطارcount || نفسه.refs == nil {
		return
	}
	if نفسه.refs[idx] == 0 {
		نفسه.refs[idx] = 2
	} else {
		نفسه.refs[idx]++
	}
}

func (نفسه *Tcowإطارمدير) Decrement(إطار uint32) {
	idx := إطار >> 12
	if idx >= نفسه.إطارcount || نفسه.refs == nil || نفسه.refs[idx] == 0 {
		return
	}
	نفسه.refs[idx]--
}

func (نفسه *Pإدارةصفحات) Init(صفحةدليلentry uintptr, صفحةجدولentry uint32, ذاكرةمدير *Tذاكرةمدير) {

	Pصفحةدليلentry = صفحةدليلentry
	Pصفحةجدولentry = صفحةجدولentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowإطارمدير.Init(ذاكرةمدير, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressالمؤشر, _ := ذاكرةمدير.Alignedmalloc(0x1000)
			if addressالمؤشر == nil {
				return
			}
			address := uint32(uintptr(addressالمؤشر))

			Sتحديدunsignedinteger32ataddress(address|0x87, uint32(صفحةدليلentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Sتحديدunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		صفحةدليلentry = صفحةدليلentry + 0x1000
	}

}
func (نفسه *Pإدارةصفحات) Sharedذاكرةregion() {

	صفحةدليلentry := Pصفحةدليلentry
	kصفحةدليلentry := Pصفحةدليلentry

	for i := uint32(1); i <= virtlen; i++ {

		صفحةدليلentry = صفحةدليلentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Getالقيمة(uint32(kصفحةدليلentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sتحديدunsignedinteger32ataddress(v|0x87, uint32(صفحةدليلentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getالقيمة(uint32(kصفحةدليلentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sتحديدunsignedinteger32ataddress(v|0x87, uint32(صفحةدليلentry)+pde*4)

		}

	}
}
func (نفسه *Pإدارةصفحات) Pصفحةخلل(مدير *Tمقاطعةمدير) {
	مقاطعةhandler = التعاملإدارةصفحاتمقاطعة

	var address uintptr
	address = uintptr(unsafe.Pointer(&مقاطعةhandler))
	نفسه.Tمقاطعةhandler.Init(0xE, uintptr(unsafe.Pointer(مدير)), address)
}

var مقاطعةhandler func(uint32) uint32

func التعاملإدارةصفحاتمقاطعة(esp uint32) uint32 {
	if Rحلنسخعندكتابةخلل() {
		return esp
	}
	return Hالتعاملfatalمقاطعةإطار(esp, 0x0E)
}

func Cloneaddressspacecow(المصدرصفحةدليل uint32) uint32 {
	if Aنشطذاكرةمدير == nil || المصدرصفحةدليل == 0 {
		return 0
	}
	المقصدالمؤشر, _ := Aنشطذاكرةمدير.Alignedmalloc(0x1000)
	if المقصدالمؤشر == nil {
		return 0
	}
	المقصدصفحةدليل := uint32(uintptr(المقصدالمؤشر))
	for i := uint32(0); i < 1024; i++ {
		Sتحديدunsignedinteger32ataddress(0, المقصدصفحةدليل+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		المصدرpdeaddress := المصدرصفحةدليل + pde*4
		المصدرpde := Getالقيمة(المصدرpdeaddress)
		if (المصدرpde & Pصفحةالحالي) == 0 {
			continue
		}
		if issharedpde(pde) {
			Sتحديدunsignedinteger32ataddress(المصدرpde, المقصدصفحةدليل+pde*4)
			continue
		}

		المقصدptالمؤشر, _ := Aنشطذاكرةمدير.Alignedmalloc(0x1000)
		if المقصدptالمؤشر == nil {
			continue
		}
		المصدرpt := المصدرpde & Pصفحةإطار
		المقصدpt := uint32(uintptr(المقصدptالمؤشر))
		Sتحديدunsignedinteger32ataddress((المقصدpt | (المصدرpde & 0xFFF)), المقصدصفحةدليل+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := المصدرpt + pte*4
			entry := Getالقيمة(pteaddress)
			if (entry & Pصفحةالحالي) != 0 {
				if (entry & Pصفحةwritable) != 0 {
					entry = (entry &^ Pصفحةwritable) | Pصفحةcow
					Sتحديدunsignedinteger32ataddress(entry, pteaddress)
					cowإطارمدير.Increment(entry & Pصفحةإطار)
				} else if (entry & Pصفحةcow) != 0 {
					cowإطارمدير.Increment(entry & Pصفحةإطار)
				}
			}
			Sتحديدunsignedinteger32ataddress(entry, المقصدpt+pte*4)
		}
	}
	أعدالتحميلcr3()
	return المقصدصفحةدليل
}

func Rحلنسخعندكتابةخلل() bool {
	if Aنشطذاكرةمدير == nil {
		return false
	}
	خللaddress := getcr2()
	دليل_الصفحات := getcr3()
	pdeaddress := دليل_الصفحات + ((خللaddress>>22)&0x3FF)*4
	pde := Getالقيمة(pdeaddress)
	if (pde & Pصفحةالحالي) == 0 {
		return false
	}
	pt := pde & Pصفحةإطار
	pteaddress := pt + ((خللaddress>>12)&0x3FF)*4
	pte := Getالقيمة(pteaddress)
	if (pte&Pصفحةcow) == 0 || (pte&Pصفحةالحالي) == 0 {
		return false
	}
	oldإطار := pte & Pصفحةإطار
	if cowإطارمدير.Reference(oldإطار) <= 1 {
		Sتحديدunsignedinteger32ataddress((pte|Pصفحةwritable)&^Pصفحةcow, pteaddress)
		أعدالتحميلcr3()
		return true
	}

	جديدالمؤشر, _ := Aنشطذاكرةمدير.Alignedmalloc(0x1000)
	if جديدالمؤشر == nil {
		return false
	}
	جديدإطار := uint32(uintptr(جديدالمؤشر)) & Pصفحةإطار

	المصدر_2 := Getبايتfromالمؤشر(uintptr(خللaddress&Pصفحةإطار), 0x1000, 0x1000)
	المقصد_2 := Getبايتfromالمؤشر(uintptr(جديدإطار), 0x1000, 0x1000)
	copy(المقصد_2, المصدر_2)
	cowإطارمدير.Decrement(oldإطار)
	Sتحديدunsignedinteger32ataddress((جديدإطار|(pte&0xFFF)|Pصفحةwritable)&^Pصفحةcow, pteaddress)
	أعدالتحميلcr3()
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

func أعدالتحميلcr3() {
	cr3 := getcr3()
	تحديدcr3(cr3)
}

func Sتحديدبايتداخلصفحةدليل(x byte, address uint32, دليل_الصفحات uint32) {
	oldcr3 := getcr3()
	تحديدcr3(دليل_الصفحات)
	Sتحديدبايتataddress(x, address)
	تحديدcr3(oldcr3)
}

func Sتحديدحظرداخلصفحةدليل(المصدر_2 []byte, المقصد_2 []byte, الحجم uint32, دليل_الصفحات uint32) {
	if الحجم == 0 || دليل_الصفحات == 0 {
		return
	}
	oldcr3 := getcr3()
	تحديدcr3(دليل_الصفحات)
	makeمدىprivatewritableالحالي(دليل_الصفحات, uint32(uintptr(unsafe.Pointer(&المقصد_2[0]))), الحجم)

	for i := uint32(0); i < الحجم; i++ {
		المقصد_2[i] = المصدر_2[i]
	}
	تحديدcr3(oldcr3)
}

func Zeroحظرداخلصفحةدليل(address uint32, الحجم uint32, دليل_الصفحات uint32) {
	if الحجم == 0 || دليل_الصفحات == 0 {
		return
	}
	oldcr3 := getcr3()
	تحديدcr3(دليل_الصفحات)
	makeمدىprivatewritableالحالي(دليل_الصفحات, address, الحجم)
	المقصد_2 := Getبايتfromالمؤشر(uintptr(address), int(الحجم), int(الحجم))
	for i := uint32(0); i < الحجم; i++ {
		المقصد_2[i] = 0
	}
	تحديدcr3(oldcr3)
}

func makeصفحةprivatewritableالحالي(دليل_الصفحات uint32, افتراضيaddress uint32) bool {
	pde := Getالقيمة(دليل_الصفحات + ((افتراضيaddress>>22)&0x3FF)*4)
	if (pde & Pصفحةالحالي) == 0 {
		return false
	}
	pteaddress := (pde & Pصفحةإطار) + ((افتراضيaddress>>12)&0x3FF)*4
	pte := Getالقيمة(pteaddress)
	if (pte & Pصفحةالحالي) == 0 {
		return false
	}
	if (pte & Pصفحةcow) == 0 {
		return (pte & Pصفحةwritable) != 0
	}
	if Aنشطذاكرةمدير == nil {
		return false
	}
	جديدالمؤشر, _ := Aنشطذاكرةمدير.Alignedmalloc(0x1000)
	if جديدالمؤشر == nil {
		return false
	}
	جديدإطار := uint32(uintptr(جديدالمؤشر)) & Pصفحةإطار
	المصدر_2 := Getبايتfromالمؤشر(uintptr(افتراضيaddress&Pصفحةإطار), 0x1000, 0x1000)
	المقصد_2 := Getبايتfromالمؤشر(uintptr(جديدإطار), 0x1000, 0x1000)
	copy(المقصد_2, المصدر_2)
	cowإطارمدير.Decrement(pte & Pصفحةإطار)
	Sتحديدunsignedinteger32ataddress((جديدإطار|(pte&0xFFF)|Pصفحةwritable)&^Pصفحةcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	أعدالتحميلcr3()
	return true
}

func makeمدىprivatewritableالحالي(دليل_الصفحات uint32, address uint32, الحجم uint32) bool {
	if الحجم == 0 {
		return true
	}
	الأخير := address + الحجم - 1
	if الأخير < address {
		return false
	}
	for صفحة := address & Pصفحةإطار; ; صفحة += 0x1000 {
		if !makeصفحةprivatewritableالحالي(دليل_الصفحات, صفحة) {
			return false
		}
		if صفحة == (الأخير & Pصفحةإطار) {
			break
		}
	}
	return true
}

func Makeمدىprivatewritable(دليل_الصفحات uint32, address uint32, الحجم uint32) bool {
	if دليل_الصفحات == 0 {
		return false
	}
	oldcr3 := getcr3()
	تحديدcr3(دليل_الصفحات)
	موافق := makeمدىprivatewritableالحالي(دليل_الصفحات, address, الحجم)
	تحديدcr3(oldcr3)
	return موافق
}

func Sتحديدunsignedinteger32داخلصفحةدليل(x uint32, address uint32, دليل_الصفحات uint32) {
	if دليل_الصفحات == 0 {
		return
	}
	oldcr3 := getcr3()
	تحديدcr3(دليل_الصفحات)
	Sتحديدunsignedinteger32ataddress(x, address)
	تحديدcr3(oldcr3)
}

func Getالقيمة(address uint32) uint32 {
	var orgالقيمة uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgالقيمة
}
func Getالقيمةداخلصفحةدليل(address uint32, دليل_الصفحات uint32) uint32 {
	if دليل_الصفحات == 0 {
		return 0
	}
	oldcr3 := getcr3()
	تحديدcr3(دليل_الصفحات)
	v := Getالقيمة(address)
	تحديدcr3(oldcr3)
	return v
}

var v uint32 = 0

func Cنسخصفحةإطارحظر(xصفحةدليل uint32, yصفحةدليل uint32, vaddress uint32) {
	if xصفحةدليل == 0 || yصفحةدليل == 0 {
		return
	}
	oldcr3 := getcr3()
	تحديدcr3(xصفحةدليل)
	v = Getالقيمة(vaddress)
	Sتحديدunsignedinteger32داخلصفحةدليل(v, vaddress, yصفحةدليل)

	تحديدcr3(oldcr3)
}
