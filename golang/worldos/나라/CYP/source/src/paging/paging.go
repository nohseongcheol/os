/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "διακοπή"
import . "μνήμηmanager"
import . "util"

type ΣελίδαΚατάλογοςκαταχώρηση_2 uintptr

const (
	ΣελίδαΠαρούσα	uint32	= 0x001
	Σελίδαwritable	uint32	= 0x002
	ΣελίδαΧρήστης	uint32	= 0x004
	ΣελίδαΠλαίσιο	uint32	= 0xFFFFF000
	Σελίδαcow	uint32	= 0x200
)

func Σύνολοbyteataddress(x byte, address uint32)
func Σύνολοunsignedinteger8ataddress(x uint8, address uint32)
func Σύνολοunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func σύνολοcr3(σελίδαΚατάλογος uint32)
func getcr3() uint32

type Paging struct {
	TΔιακοπήhandler
}
type TcowΠλαίσιοmanager struct {
	mem		*TΜνήμηmanager
	refs		[]uint16
	πλαίσιοcount	uint32
}

var (
	ΣελίδαΚατάλογοςκαταχώρηση	uintptr
	ΣελίδαΠίνακαςκαταχώρηση		uint32
	pdelen				uint32
	virtlen				uint32
	cowΠλαίσιοmanager		TcowΠλαίσιοmanager
)

func (self *TcowΠλαίσιοmanager) Init(mem *TΜνήμηmanager, πλαίσιοcount uint32) bool {
	self.mem = mem
	self.πλαίσιοcount = πλαίσιοcount
	referencebytes := πλαίσιοcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceΔείκτης := mem.Malloc(referencebytes)
	if referenceΔείκτης == nil {
		self.refs = nil
		self.πλαίσιοcount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceΔείκτης)[:πλαίσιοcount:πλαίσιοcount]
	for i := uint32(0); i < πλαίσιοcount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TcowΠλαίσιοmanager) Reference(πλαίσιο uint32) uint16 {
	idx := πλαίσιο >> 12
	if idx >= self.πλαίσιοcount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowΠλαίσιοmanager) Increment(πλαίσιο uint32) {
	idx := πλαίσιο >> 12
	if idx >= self.πλαίσιοcount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TcowΠλαίσιοmanager) Decrement(πλαίσιο uint32) {
	idx := πλαίσιο >> 12
	if idx >= self.πλαίσιοcount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(σελίδαΚατάλογοςκαταχώρηση uintptr, σελίδαΠίνακαςκαταχώρηση uint32, μνήμηmanager *TΜνήμηmanager) {

	ΣελίδαΚατάλογοςκαταχώρηση = σελίδαΚατάλογοςκαταχώρηση
	ΣελίδαΠίνακαςκαταχώρηση = σελίδαΠίνακαςκαταχώρηση

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowΠλαίσιοmanager.Init(μνήμηmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressΔείκτης, _ := μνήμηmanager.Alignedmalloc(0x1000)
			if addressΔείκτης == nil {
				return
			}
			address := uint32(uintptr(addressΔείκτης))

			Σύνολοunsignedinteger32ataddress(address|0x87, uint32(σελίδαΚατάλογοςκαταχώρηση)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Σύνολοunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		σελίδαΚατάλογοςκαταχώρηση = σελίδαΚατάλογοςκαταχώρηση + 0x1000
	}

}
func (self *Paging) SharedΜνήμηregion() {

	σελίδαΚατάλογοςκαταχώρηση := ΣελίδαΚατάλογοςκαταχώρηση
	kΣελίδαΚατάλογοςκαταχώρηση := ΣελίδαΚατάλογοςκαταχώρηση

	for i := uint32(1); i <= virtlen; i++ {

		σελίδαΚατάλογοςκαταχώρηση = σελίδαΚατάλογοςκαταχώρηση + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetΤιμή(uint32(kΣελίδαΚατάλογοςκαταχώρηση) + pde*4)
			v = (v & 0xFFFFF000)
			Σύνολοunsignedinteger32ataddress(v|0x87, uint32(σελίδαΚατάλογοςκαταχώρηση)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetΤιμή(uint32(kΣελίδαΚατάλογοςκαταχώρηση) + pde*4)
			v = (v & 0xFFFFF000)
			Σύνολοunsignedinteger32ataddress(v|0x87, uint32(σελίδαΚατάλογοςκαταχώρηση)+pde*4)

		}

	}
}
func (self *Paging) Σελίδαfault(manager *TΔιακοπήmanager) {
	διακοπήhandler = χειρολαβήpagingΔιακοπή

	var address uintptr
	address = uintptr(unsafe.Pointer(&διακοπήhandler))
	self.TΔιακοπήhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var διακοπήhandler func(uint32) uint32

func χειρολαβήpagingΔιακοπή(esp uint32) uint32 {
	if ResolveΑντιγραφήΕνεργήΕγγραφήfault() {
		return esp
	}
	return ΧειρολαβήfatalΔιακοπήΠλαίσιο(esp, 0x0E)
}

func CloneaddressΔιάστημαcow(πηγήΣελίδαΚατάλογος uint32) uint32 {
	if ΕνεργόΜνήμηmanager == nil || πηγήΣελίδαΚατάλογος == 0 {
		return 0
	}
	προορισμόςΔείκτης, _ := ΕνεργόΜνήμηmanager.Alignedmalloc(0x1000)
	if προορισμόςΔείκτης == nil {
		return 0
	}
	προορισμόςΣελίδαΚατάλογος := uint32(uintptr(προορισμόςΔείκτης))
	for i := uint32(0); i < 1024; i++ {
		Σύνολοunsignedinteger32ataddress(0, προορισμόςΣελίδαΚατάλογος+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		πηγήpdeaddress := πηγήΣελίδαΚατάλογος + pde*4
		πηγήpde := GetΤιμή(πηγήpdeaddress)
		if (πηγήpde & ΣελίδαΠαρούσα) == 0 {
			continue
		}
		if issharedpde(pde) {
			Σύνολοunsignedinteger32ataddress(πηγήpde, προορισμόςΣελίδαΚατάλογος+pde*4)
			continue
		}

		προορισμόςptΔείκτης, _ := ΕνεργόΜνήμηmanager.Alignedmalloc(0x1000)
		if προορισμόςptΔείκτης == nil {
			continue
		}
		πηγήpt := πηγήpde & ΣελίδαΠλαίσιο
		προορισμόςpt := uint32(uintptr(προορισμόςptΔείκτης))
		Σύνολοunsignedinteger32ataddress((προορισμόςpt | (πηγήpde & 0xFFF)), προορισμόςΣελίδαΚατάλογος+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := πηγήpt + pte*4
			καταχώρηση := GetΤιμή(pteaddress)
			if (καταχώρηση & ΣελίδαΠαρούσα) != 0 {
				if (καταχώρηση & Σελίδαwritable) != 0 {
					καταχώρηση = (καταχώρηση &^ Σελίδαwritable) | Σελίδαcow
					Σύνολοunsignedinteger32ataddress(καταχώρηση, pteaddress)
					cowΠλαίσιοmanager.Increment(καταχώρηση & ΣελίδαΠλαίσιο)
				} else if (καταχώρηση & Σελίδαcow) != 0 {
					cowΠλαίσιοmanager.Increment(καταχώρηση & ΣελίδαΠλαίσιο)
				}
			}
			Σύνολοunsignedinteger32ataddress(καταχώρηση, προορισμόςpt+pte*4)
		}
	}
	επαναφόρτωσηcr3()
	return προορισμόςΣελίδαΚατάλογος
}

func ResolveΑντιγραφήΕνεργήΕγγραφήfault() bool {
	if ΕνεργόΜνήμηmanager == nil {
		return false
	}
	faultaddress := getcr2()
	σελίδαΚατάλογος := getcr3()
	pdeaddress := σελίδαΚατάλογος + ((faultaddress>>22)&0x3FF)*4
	pde := GetΤιμή(pdeaddress)
	if (pde & ΣελίδαΠαρούσα) == 0 {
		return false
	}
	pt := pde & ΣελίδαΠλαίσιο
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetΤιμή(pteaddress)
	if (pte&Σελίδαcow) == 0 || (pte&ΣελίδαΠαρούσα) == 0 {
		return false
	}
	oldΠλαίσιο := pte & ΣελίδαΠλαίσιο
	if cowΠλαίσιοmanager.Reference(oldΠλαίσιο) <= 1 {
		Σύνολοunsignedinteger32ataddress((pte|Σελίδαwritable)&^Σελίδαcow, pteaddress)
		επαναφόρτωσηcr3()
		return true
	}

	νέοΔείκτης, _ := ΕνεργόΜνήμηmanager.Alignedmalloc(0x1000)
	if νέοΔείκτης == nil {
		return false
	}
	νέοΠλαίσιο := uint32(uintptr(νέοΔείκτης)) & ΣελίδαΠλαίσιο

	πηγή_2 := GetbytesfromΔείκτης(uintptr(faultaddress&ΣελίδαΠλαίσιο), 0x1000, 0x1000)
	προορισμός_2 := GetbytesfromΔείκτης(uintptr(νέοΠλαίσιο), 0x1000, 0x1000)
	copy(προορισμός_2, πηγή_2)
	cowΠλαίσιοmanager.Decrement(oldΠλαίσιο)
	Σύνολοunsignedinteger32ataddress((νέοΠλαίσιο|(pte&0xFFF)|Σελίδαwritable)&^Σελίδαcow, pteaddress)
	επαναφόρτωσηcr3()
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

func επαναφόρτωσηcr3() {
	cr3 := getcr3()
	σύνολοcr3(cr3)
}

func ΣύνολοbyteσεΣελίδαΚατάλογος(x byte, address uint32, σελίδαΚατάλογος uint32) {
	oldcr3 := getcr3()
	σύνολοcr3(σελίδαΚατάλογος)
	Σύνολοbyteataddress(x, address)
	σύνολοcr3(oldcr3)
}

func ΣύνολοΜπλοκσεΣελίδαΚατάλογος(πηγή_2 []byte, προορισμός_2 []byte, μέγεθος uint32, σελίδαΚατάλογος uint32) {
	if μέγεθος == 0 || σελίδαΚατάλογος == 0 {
		return
	}
	oldcr3 := getcr3()
	σύνολοcr3(σελίδαΚατάλογος)
	makeΕύροςΙδιωτικόwritableΤρέχον(σελίδαΚατάλογος, uint32(uintptr(unsafe.Pointer(&προορισμός_2[0]))), μέγεθος)

	for i := uint32(0); i < μέγεθος; i++ {
		προορισμός_2[i] = πηγή_2[i]
	}
	σύνολοcr3(oldcr3)
}

func ΜηδένΜπλοκσεΣελίδαΚατάλογος(address uint32, μέγεθος uint32, σελίδαΚατάλογος uint32) {
	if μέγεθος == 0 || σελίδαΚατάλογος == 0 {
		return
	}
	oldcr3 := getcr3()
	σύνολοcr3(σελίδαΚατάλογος)
	makeΕύροςΙδιωτικόwritableΤρέχον(σελίδαΚατάλογος, address, μέγεθος)
	προορισμός_2 := GetbytesfromΔείκτης(uintptr(address), int(μέγεθος), int(μέγεθος))
	for i := uint32(0); i < μέγεθος; i++ {
		προορισμός_2[i] = 0
	}
	σύνολοcr3(oldcr3)
}

func makeΣελίδαΙδιωτικόwritableΤρέχον(σελίδαΚατάλογος uint32, εικονικήaddress uint32) bool {
	pde := GetΤιμή(σελίδαΚατάλογος + ((εικονικήaddress>>22)&0x3FF)*4)
	if (pde & ΣελίδαΠαρούσα) == 0 {
		return false
	}
	pteaddress := (pde & ΣελίδαΠλαίσιο) + ((εικονικήaddress>>12)&0x3FF)*4
	pte := GetΤιμή(pteaddress)
	if (pte & ΣελίδαΠαρούσα) == 0 {
		return false
	}
	if (pte & Σελίδαcow) == 0 {
		return (pte & Σελίδαwritable) != 0
	}
	if ΕνεργόΜνήμηmanager == nil {
		return false
	}
	νέοΔείκτης, _ := ΕνεργόΜνήμηmanager.Alignedmalloc(0x1000)
	if νέοΔείκτης == nil {
		return false
	}
	νέοΠλαίσιο := uint32(uintptr(νέοΔείκτης)) & ΣελίδαΠλαίσιο
	πηγή_2 := GetbytesfromΔείκτης(uintptr(εικονικήaddress&ΣελίδαΠλαίσιο), 0x1000, 0x1000)
	προορισμός_2 := GetbytesfromΔείκτης(uintptr(νέοΠλαίσιο), 0x1000, 0x1000)
	copy(προορισμός_2, πηγή_2)
	cowΠλαίσιοmanager.Decrement(pte & ΣελίδαΠλαίσιο)
	Σύνολοunsignedinteger32ataddress((νέοΠλαίσιο|(pte&0xFFF)|Σελίδαwritable)&^Σελίδαcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	επαναφόρτωσηcr3()
	return true
}

func makeΕύροςΙδιωτικόwritableΤρέχον(σελίδαΚατάλογος uint32, address uint32, μέγεθος uint32) bool {
	if μέγεθος == 0 {
		return true
	}
	τελευταία := address + μέγεθος - 1
	if τελευταία < address {
		return false
	}
	for σελίδα := address & ΣελίδαΠλαίσιο; ; σελίδα += 0x1000 {
		if !makeΣελίδαΙδιωτικόwritableΤρέχον(σελίδαΚατάλογος, σελίδα) {
			return false
		}
		if σελίδα == (τελευταία & ΣελίδαΠλαίσιο) {
			break
		}
	}
	return true
}

func MakeΕύροςΙδιωτικόwritable(σελίδαΚατάλογος uint32, address uint32, μέγεθος uint32) bool {
	if σελίδαΚατάλογος == 0 {
		return false
	}
	oldcr3 := getcr3()
	σύνολοcr3(σελίδαΚατάλογος)
	εντάξει := makeΕύροςΙδιωτικόwritableΤρέχον(σελίδαΚατάλογος, address, μέγεθος)
	σύνολοcr3(oldcr3)
	return εντάξει
}

func Σύνολοunsignedinteger32σεΣελίδαΚατάλογος(x uint32, address uint32, σελίδαΚατάλογος uint32) {
	if σελίδαΚατάλογος == 0 {
		return
	}
	oldcr3 := getcr3()
	σύνολοcr3(σελίδαΚατάλογος)
	Σύνολοunsignedinteger32ataddress(x, address)
	σύνολοcr3(oldcr3)
}

func GetΤιμή(address uint32) uint32 {
	var orgΤιμή uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgΤιμή
}
func GetΤιμήσεΣελίδαΚατάλογος(address uint32, σελίδαΚατάλογος uint32) uint32 {
	if σελίδαΚατάλογος == 0 {
		return 0
	}
	oldcr3 := getcr3()
	σύνολοcr3(σελίδαΚατάλογος)
	v := GetΤιμή(address)
	σύνολοcr3(oldcr3)
	return v
}

var v uint32 = 0

func ΑντιγραφήΣελίδαΠλαίσιοΜπλοκ(xΣελίδαΚατάλογος uint32, yΣελίδαΚατάλογος uint32, vaddress uint32) {
	if xΣελίδαΚατάλογος == 0 || yΣελίδαΚατάλογος == 0 {
		return
	}
	oldcr3 := getcr3()
	σύνολοcr3(xΣελίδαΚατάλογος)
	v = GetΤιμή(vaddress)
	Σύνολοunsignedinteger32σεΣελίδαΚατάλογος(v, vaddress, yΣελίδαΚατάλογος)

	σύνολοcr3(oldcr3)
}
