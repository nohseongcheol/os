package paging

import unsafe "unsafe"
import . "פסק"
import . "זיכרוןmanager"
import . "util"

type Pעמודספרייהentry_2 uintptr

const (
	Pעמודנוכח	uint32	= 0x001
	Pעמודwritable	uint32	= 0x002
	Pעמודמשתמש	uint32	= 0x004
	Pעמודframe	uint32	= 0xFFFFF000
	Pעמודcow	uint32	= 0x200
)

func Sקבעbyteataddress(x byte, address uint32)
func Sקבעunsignedinteger8ataddress(x uint8, address uint32)
func Sקבעunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func קבעcr3(עמודספרייה uint32)
func getcr3() uint32

type Paging struct {
	Tפסקhandler
}
type Tcowframemanager struct {
	mem		*Tזיכרוןmanager
	refs		[]uint16
	framecount	uint32
}

var (
	Pעמודספרייהentry	uintptr
	Pעמודtableentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowframemanager		Tcowframemanager
)

func (self *Tcowframemanager) Init(mem *Tזיכרוןmanager, framecount uint32) bool {
	self.mem = mem
	self.framecount = framecount
	referenceבתים := framecount * uint32(unsafe.Sizeof(uint16(0)))
	referenceסמן := mem.Malloc(referenceבתים)
	if referenceסמן == nil {
		self.refs = nil
		self.framecount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceסמן)[:framecount:framecount]
	for i := uint32(0); i < framecount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcowframemanager) Reference(frame uint32) uint16 {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcowframemanager) Increment(frame uint32) {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcowframemanager) Decrement(frame uint32) {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(עמודספרייהentry uintptr, עמודtableentry uint32, זיכרוןmanager *Tזיכרוןmanager) {

	Pעמודספרייהentry = עמודספרייהentry
	Pעמודtableentry = עמודtableentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframemanager.Init(זיכרוןmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressסמן, _ := זיכרוןmanager.Alignedmalloc(0x1000)
			if addressסמן == nil {
				return
			}
			address := uint32(uintptr(addressסמן))

			Sקבעunsignedinteger32ataddress(address|0x87, uint32(עמודספרייהentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Sקבעunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		עמודספרייהentry = עמודספרייהentry + 0x1000
	}

}
func (self *Paging) Sharedזיכרוןregion() {

	עמודספרייהentry := Pעמודספרייהentry
	kעמודספרייהentry := Pעמודספרייהentry

	for i := uint32(1); i <= virtlen; i++ {

		עמודספרייהentry = עמודספרייהentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Getערך(uint32(kעמודספרייהentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sקבעunsignedinteger32ataddress(v|0x87, uint32(עמודספרייהentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getערך(uint32(kעמודספרייהentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sקבעunsignedinteger32ataddress(v|0x87, uint32(עמודספרייהentry)+pde*4)

		}

	}
}
func (self *Paging) Pעמודfault(manager *Tפסקmanager) {
	פסקhandler = ידיתpagingפסק

	var address uintptr
	address = uintptr(unsafe.Pointer(&פסקhandler))
	self.Tפסקhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var פסקhandler func(uint32) uint32

func ידיתpagingפסק(esp uint32) uint32 {
	if Resolveהעתקפעילכתיבהfault() {
		return esp
	}
	return Hידיתfatalפסקframe(esp, 0x0E)
}

func Cloneaddressרווחcow(מקורעמודספרייה uint32) uint32 {
	if Aפעילזיכרוןmanager == nil || מקורעמודספרייה == 0 {
		return 0
	}
	יעדסמן, _ := Aפעילזיכרוןmanager.Alignedmalloc(0x1000)
	if יעדסמן == nil {
		return 0
	}
	יעדעמודספרייה := uint32(uintptr(יעדסמן))
	for i := uint32(0); i < 1024; i++ {
		Sקבעunsignedinteger32ataddress(0, יעדעמודספרייה+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		מקורpdeaddress := מקורעמודספרייה + pde*4
		מקורpde := Getערך(מקורpdeaddress)
		if (מקורpde & Pעמודנוכח) == 0 {
			continue
		}
		if issharedpde(pde) {
			Sקבעunsignedinteger32ataddress(מקורpde, יעדעמודספרייה+pde*4)
			continue
		}

		יעדptסמן, _ := Aפעילזיכרוןmanager.Alignedmalloc(0x1000)
		if יעדptסמן == nil {
			continue
		}
		מקורpt := מקורpde & Pעמודframe
		יעדpt := uint32(uintptr(יעדptסמן))
		Sקבעunsignedinteger32ataddress((יעדpt | (מקורpde & 0xFFF)), יעדעמודספרייה+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := מקורpt + pte*4
			entry := Getערך(pteaddress)
			if (entry & Pעמודנוכח) != 0 {
				if (entry & Pעמודwritable) != 0 {
					entry = (entry &^ Pעמודwritable) | Pעמודcow
					Sקבעunsignedinteger32ataddress(entry, pteaddress)
					cowframemanager.Increment(entry & Pעמודframe)
				} else if (entry & Pעמודcow) != 0 {
					cowframemanager.Increment(entry & Pעמודframe)
				}
			}
			Sקבעunsignedinteger32ataddress(entry, יעדpt+pte*4)
		}
	}
	טעןמחדשcr3()
	return יעדעמודספרייה
}

func Resolveהעתקפעילכתיבהfault() bool {
	if Aפעילזיכרוןmanager == nil {
		return false
	}
	faultaddress := getcr2()
	עמודספרייה := getcr3()
	pdeaddress := עמודספרייה + ((faultaddress>>22)&0x3FF)*4
	pde := Getערך(pdeaddress)
	if (pde & Pעמודנוכח) == 0 {
		return false
	}
	pt := pde & Pעמודframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := Getערך(pteaddress)
	if (pte&Pעמודcow) == 0 || (pte&Pעמודנוכח) == 0 {
		return false
	}
	oldframe := pte & Pעמודframe
	if cowframemanager.Reference(oldframe) <= 1 {
		Sקבעunsignedinteger32ataddress((pte|Pעמודwritable)&^Pעמודcow, pteaddress)
		טעןמחדשcr3()
		return true
	}

	חדשסמן, _ := Aפעילזיכרוןmanager.Alignedmalloc(0x1000)
	if חדשסמן == nil {
		return false
	}
	חדשframe := uint32(uintptr(חדשסמן)) & Pעמודframe

	מקור_2 := Getבתיםfromסמן(uintptr(faultaddress&Pעמודframe), 0x1000, 0x1000)
	יעד_2 := Getבתיםfromסמן(uintptr(חדשframe), 0x1000, 0x1000)
	copy(יעד_2, מקור_2)
	cowframemanager.Decrement(oldframe)
	Sקבעunsignedinteger32ataddress((חדשframe|(pte&0xFFF)|Pעמודwritable)&^Pעמודcow, pteaddress)
	טעןמחדשcr3()
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

func טעןמחדשcr3() {
	cr3 := getcr3()
	קבעcr3(cr3)
}

func Sקבעbyteנכנסעמודספרייה(x byte, address uint32, עמודספרייה uint32) {
	oldcr3 := getcr3()
	קבעcr3(עמודספרייה)
	Sקבעbyteataddress(x, address)
	קבעcr3(oldcr3)
}

func Sקבעבלוקנכנסעמודספרייה(מקור_2 []byte, יעד_2 []byte, גודל uint32, עמודספרייה uint32) {
	if גודל == 0 || עמודספרייה == 0 {
		return
	}
	oldcr3 := getcr3()
	קבעcr3(עמודספרייה)
	makerangeפרטיwritableנוכחי(עמודספרייה, uint32(uintptr(unsafe.Pointer(&יעד_2[0]))), גודל)

	for i := uint32(0); i < גודל; i++ {
		יעד_2[i] = מקור_2[i]
	}
	קבעcr3(oldcr3)
}

func Zeroבלוקנכנסעמודספרייה(address uint32, גודל uint32, עמודספרייה uint32) {
	if גודל == 0 || עמודספרייה == 0 {
		return
	}
	oldcr3 := getcr3()
	קבעcr3(עמודספרייה)
	makerangeפרטיwritableנוכחי(עמודספרייה, address, גודל)
	יעד_2 := Getבתיםfromסמן(uintptr(address), int(גודל), int(גודל))
	for i := uint32(0); i < גודל; i++ {
		יעד_2[i] = 0
	}
	קבעcr3(oldcr3)
}

func makeעמודפרטיwritableנוכחי(עמודספרייה uint32, וירטואליaddress uint32) bool {
	pde := Getערך(עמודספרייה + ((וירטואליaddress>>22)&0x3FF)*4)
	if (pde & Pעמודנוכח) == 0 {
		return false
	}
	pteaddress := (pde & Pעמודframe) + ((וירטואליaddress>>12)&0x3FF)*4
	pte := Getערך(pteaddress)
	if (pte & Pעמודנוכח) == 0 {
		return false
	}
	if (pte & Pעמודcow) == 0 {
		return (pte & Pעמודwritable) != 0
	}
	if Aפעילזיכרוןmanager == nil {
		return false
	}
	חדשסמן, _ := Aפעילזיכרוןmanager.Alignedmalloc(0x1000)
	if חדשסמן == nil {
		return false
	}
	חדשframe := uint32(uintptr(חדשסמן)) & Pעמודframe
	מקור_2 := Getבתיםfromסמן(uintptr(וירטואליaddress&Pעמודframe), 0x1000, 0x1000)
	יעד_2 := Getבתיםfromסמן(uintptr(חדשframe), 0x1000, 0x1000)
	copy(יעד_2, מקור_2)
	cowframemanager.Decrement(pte & Pעמודframe)
	Sקבעunsignedinteger32ataddress((חדשframe|(pte&0xFFF)|Pעמודwritable)&^Pעמודcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	טעןמחדשcr3()
	return true
}

func makerangeפרטיwritableנוכחי(עמודספרייה uint32, address uint32, גודל uint32) bool {
	if גודל == 0 {
		return true
	}
	אחרון := address + גודל - 1
	if אחרון < address {
		return false
	}
	for עמוד := address & Pעמודframe; ; עמוד += 0x1000 {
		if !makeעמודפרטיwritableנוכחי(עמודספרייה, עמוד) {
			return false
		}
		if עמוד == (אחרון & Pעמודframe) {
			break
		}
	}
	return true
}

func Makerangeפרטיwritable(עמודספרייה uint32, address uint32, גודל uint32) bool {
	if עמודספרייה == 0 {
		return false
	}
	oldcr3 := getcr3()
	קבעcr3(עמודספרייה)
	אישור := makerangeפרטיwritableנוכחי(עמודספרייה, address, גודל)
	קבעcr3(oldcr3)
	return אישור
}

func Sקבעunsignedinteger32נכנסעמודספרייה(x uint32, address uint32, עמודספרייה uint32) {
	if עמודספרייה == 0 {
		return
	}
	oldcr3 := getcr3()
	קבעcr3(עמודספרייה)
	Sקבעunsignedinteger32ataddress(x, address)
	קבעcr3(oldcr3)
}

func Getערך(address uint32) uint32 {
	var orgערך uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgערך
}
func Getערךנכנסעמודספרייה(address uint32, עמודספרייה uint32) uint32 {
	if עמודספרייה == 0 {
		return 0
	}
	oldcr3 := getcr3()
	קבעcr3(עמודספרייה)
	v := Getערך(address)
	קבעcr3(oldcr3)
	return v
}

var v uint32 = 0

func Cהעתקעמודframeבלוק(xעמודספרייה uint32, yעמודספרייה uint32, vaddress uint32) {
	if xעמודספרייה == 0 || yעמודספרייה == 0 {
		return
	}
	oldcr3 := getcr3()
	קבעcr3(xעמודספרייה)
	v = Getערך(vaddress)
	Sקבעunsignedinteger32נכנסעמודספרייה(v, vaddress, yעמודספרייה)

	קבעcr3(oldcr3)
}
