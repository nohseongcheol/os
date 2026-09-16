/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupt"
import . "حافظهmanager"
import . "util"

type Pصفحهشاخهentry_2 uintptr

const (
	Pصفحهpresent	uint32	= 0x001
	Pصفحهwritable	uint32	= 0x002
	Pصفحهکاربر	uint32	= 0x004
	Pصفحهچارچوب	uint32	= 0xFFFFF000
	Pصفحهcow	uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(صفحهشاخه uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type Tcowچارچوبmanager struct {
	mem		*Tحافظهmanager
	refs		[]uint16
	چارچوبcount	uint32
}

var (
	Pصفحهشاخهentry		uintptr
	Pصفحهجدولentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowچارچوبmanager	Tcowچارچوبmanager
)

func (خود *Tcowچارچوبmanager) Init(mem *Tحافظهmanager, چارچوبcount uint32) bool {
	خود.mem = mem
	خود.چارچوبcount = چارچوبcount
	referenceبایت := چارچوبcount * uint32(unsafe.Sizeof(uint16(0)))
	referencepointer := mem.Malloc(referenceبایت)
	if referencepointer == nil {
		خود.refs = nil
		خود.چارچوبcount = 0
		return false
	}
	خود.refs = (*[1 << 28]uint16)(referencepointer)[:چارچوبcount:چارچوبcount]
	for i := uint32(0); i < چارچوبcount; i++ {
		خود.refs[i] = 0
	}
	return true
}

func (خود *Tcowچارچوبmanager) Reference(چارچوب uint32) uint16 {
	idx := چارچوب >> 12
	if idx >= خود.چارچوبcount || خود.refs == nil {
		return 0
	}
	return خود.refs[idx]
}

func (خود *Tcowچارچوبmanager) Increment(چارچوب uint32) {
	idx := چارچوب >> 12
	if idx >= خود.چارچوبcount || خود.refs == nil {
		return
	}
	if خود.refs[idx] == 0 {
		خود.refs[idx] = 2
	} else {
		خود.refs[idx]++
	}
}

func (خود *Tcowچارچوبmanager) Decrement(چارچوب uint32) {
	idx := چارچوب >> 12
	if idx >= خود.چارچوبcount || خود.refs == nil || خود.refs[idx] == 0 {
		return
	}
	خود.refs[idx]--
}

func (خود *Paging) Init(صفحهشاخهentry uintptr, صفحهجدولentry uint32, حافظهmanager *Tحافظهmanager) {

	Pصفحهشاخهentry = صفحهشاخهentry
	Pصفحهجدولentry = صفحهجدولentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowچارچوبmanager.Init(حافظهmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addresspointer, _ := حافظهmanager.Alignedmalloc(0x1000)
			if addresspointer == nil {
				return
			}
			address := uint32(uintptr(addresspointer))

			Setunsignedinteger32ataddress(address|0x87, uint32(صفحهشاخهentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		صفحهشاخهentry = صفحهشاخهentry + 0x1000
	}

}
func (خود *Paging) Sharedحافظهregion() {

	صفحهشاخهentry := Pصفحهشاخهentry
	kصفحهشاخهentry := Pصفحهشاخهentry

	for i := uint32(1); i <= virtlen; i++ {

		صفحهشاخهentry = صفحهشاخهentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Getمقدار(uint32(kصفحهشاخهentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(صفحهشاخهentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getمقدار(uint32(kصفحهشاخهentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(صفحهشاخهentry)+pde*4)

		}

	}
}
func (خود *Paging) Pصفحهfault(manager *TInterruptmanager) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	خود.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if Resolveکپیروشننوشتنfault() {
		return esp
	}
	return Handlefatalinterruptچارچوب(esp, 0x0E)
}

func Cloneaddressفاصلهcow(مبدأصفحهشاخه uint32) uint32 {
	if Aفعالحافظهmanager == nil || مبدأصفحهشاخه == 0 {
		return 0
	}
	مقصدpointer, _ := Aفعالحافظهmanager.Alignedmalloc(0x1000)
	if مقصدpointer == nil {
		return 0
	}
	مقصدصفحهشاخه := uint32(uintptr(مقصدpointer))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, مقصدصفحهشاخه+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		مبدأpdeaddress := مبدأصفحهشاخه + pde*4
		مبدأpde := Getمقدار(مبدأpdeaddress)
		if (مبدأpde & Pصفحهpresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(مبدأpde, مقصدصفحهشاخه+pde*4)
			continue
		}

		مقصدptpointer, _ := Aفعالحافظهmanager.Alignedmalloc(0x1000)
		if مقصدptpointer == nil {
			continue
		}
		مبدأpt := مبدأpde & Pصفحهچارچوب
		مقصدpt := uint32(uintptr(مقصدptpointer))
		Setunsignedinteger32ataddress((مقصدpt | (مبدأpde & 0xFFF)), مقصدصفحهشاخه+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := مبدأpt + pte*4
			entry := Getمقدار(pteaddress)
			if (entry & Pصفحهpresent) != 0 {
				if (entry & Pصفحهwritable) != 0 {
					entry = (entry &^ Pصفحهwritable) | Pصفحهcow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowچارچوبmanager.Increment(entry & Pصفحهچارچوب)
				} else if (entry & Pصفحهcow) != 0 {
					cowچارچوبmanager.Increment(entry & Pصفحهچارچوب)
				}
			}
			Setunsignedinteger32ataddress(entry, مقصدpt+pte*4)
		}
	}
	بازخوانیcr3()
	return مقصدصفحهشاخه
}

func Resolveکپیروشننوشتنfault() bool {
	if Aفعالحافظهmanager == nil {
		return false
	}
	faultaddress := getcr2()
	صفحهشاخه := getcr3()
	pdeaddress := صفحهشاخه + ((faultaddress>>22)&0x3FF)*4
	pde := Getمقدار(pdeaddress)
	if (pde & Pصفحهpresent) == 0 {
		return false
	}
	pt := pde & Pصفحهچارچوب
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := Getمقدار(pteaddress)
	if (pte&Pصفحهcow) == 0 || (pte&Pصفحهpresent) == 0 {
		return false
	}
	oldچارچوب := pte & Pصفحهچارچوب
	if cowچارچوبmanager.Reference(oldچارچوب) <= 1 {
		Setunsignedinteger32ataddress((pte|Pصفحهwritable)&^Pصفحهcow, pteaddress)
		بازخوانیcr3()
		return true
	}

	جدیدpointer, _ := Aفعالحافظهmanager.Alignedmalloc(0x1000)
	if جدیدpointer == nil {
		return false
	}
	جدیدچارچوب := uint32(uintptr(جدیدpointer)) & Pصفحهچارچوب

	مبدأ_2 := Getبایتfrompointer(uintptr(faultaddress&Pصفحهچارچوب), 0x1000, 0x1000)
	مقصد_2 := Getبایتfrompointer(uintptr(جدیدچارچوب), 0x1000, 0x1000)
	copy(مقصد_2, مبدأ_2)
	cowچارچوبmanager.Decrement(oldچارچوب)
	Setunsignedinteger32ataddress((جدیدچارچوب|(pte&0xFFF)|Pصفحهwritable)&^Pصفحهcow, pteaddress)
	بازخوانیcr3()
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

func بازخوانیcr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func Setbyteداخلصفحهشاخه(x byte, address uint32, صفحهشاخه uint32) {
	oldcr3 := getcr3()
	setcr3(صفحهشاخه)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func Setقطعهداخلصفحهشاخه(مبدأ_2 []byte, مقصد_2 []byte, اندازه uint32, صفحهشاخه uint32) {
	if اندازه == 0 || صفحهشاخه == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(صفحهشاخه)
	makeمحدودهخصوصیwritablecurrent(صفحهشاخه, uint32(uintptr(unsafe.Pointer(&مقصد_2[0]))), اندازه)

	for i := uint32(0); i < اندازه; i++ {
		مقصد_2[i] = مبدأ_2[i]
	}
	setcr3(oldcr3)
}

func Zeroقطعهداخلصفحهشاخه(address uint32, اندازه uint32, صفحهشاخه uint32) {
	if اندازه == 0 || صفحهشاخه == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(صفحهشاخه)
	makeمحدودهخصوصیwritablecurrent(صفحهشاخه, address, اندازه)
	مقصد_2 := Getبایتfrompointer(uintptr(address), int(اندازه), int(اندازه))
	for i := uint32(0); i < اندازه; i++ {
		مقصد_2[i] = 0
	}
	setcr3(oldcr3)
}

func makeصفحهخصوصیwritablecurrent(صفحهشاخه uint32, مجازیaddress uint32) bool {
	pde := Getمقدار(صفحهشاخه + ((مجازیaddress>>22)&0x3FF)*4)
	if (pde & Pصفحهpresent) == 0 {
		return false
	}
	pteaddress := (pde & Pصفحهچارچوب) + ((مجازیaddress>>12)&0x3FF)*4
	pte := Getمقدار(pteaddress)
	if (pte & Pصفحهpresent) == 0 {
		return false
	}
	if (pte & Pصفحهcow) == 0 {
		return (pte & Pصفحهwritable) != 0
	}
	if Aفعالحافظهmanager == nil {
		return false
	}
	جدیدpointer, _ := Aفعالحافظهmanager.Alignedmalloc(0x1000)
	if جدیدpointer == nil {
		return false
	}
	جدیدچارچوب := uint32(uintptr(جدیدpointer)) & Pصفحهچارچوب
	مبدأ_2 := Getبایتfrompointer(uintptr(مجازیaddress&Pصفحهچارچوب), 0x1000, 0x1000)
	مقصد_2 := Getبایتfrompointer(uintptr(جدیدچارچوب), 0x1000, 0x1000)
	copy(مقصد_2, مبدأ_2)
	cowچارچوبmanager.Decrement(pte & Pصفحهچارچوب)
	Setunsignedinteger32ataddress((جدیدچارچوب|(pte&0xFFF)|Pصفحهwritable)&^Pصفحهcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	بازخوانیcr3()
	return true
}

func makeمحدودهخصوصیwritablecurrent(صفحهشاخه uint32, address uint32, اندازه uint32) bool {
	if اندازه == 0 {
		return true
	}
	آخرین := address + اندازه - 1
	if آخرین < address {
		return false
	}
	for صفحه := address & Pصفحهچارچوب; ; صفحه += 0x1000 {
		if !makeصفحهخصوصیwritablecurrent(صفحهشاخه, صفحه) {
			return false
		}
		if صفحه == (آخرین & Pصفحهچارچوب) {
			break
		}
	}
	return true
}

func Makeمحدودهخصوصیwritable(صفحهشاخه uint32, address uint32, اندازه uint32) bool {
	if صفحهشاخه == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(صفحهشاخه)
	تأیید := makeمحدودهخصوصیwritablecurrent(صفحهشاخه, address, اندازه)
	setcr3(oldcr3)
	return تأیید
}

func Setunsignedinteger32داخلصفحهشاخه(x uint32, address uint32, صفحهشاخه uint32) {
	if صفحهشاخه == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(صفحهشاخه)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func Getمقدار(address uint32) uint32 {
	var orgمقدار uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgمقدار
}
func Getمقدارداخلصفحهشاخه(address uint32, صفحهشاخه uint32) uint32 {
	if صفحهشاخه == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(صفحهشاخه)
	v := Getمقدار(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func Cکپیصفحهچارچوبقطعه(xصفحهشاخه uint32, yصفحهشاخه uint32, vaddress uint32) {
	if xصفحهشاخه == 0 || yصفحهشاخه == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xصفحهشاخه)
	v = Getمقدار(vaddress)
	Setunsignedinteger32داخلصفحهشاخه(v, vaddress, yصفحهشاخه)

	setcr3(oldcr3)
}
