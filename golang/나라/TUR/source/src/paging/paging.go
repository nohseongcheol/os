package paging

import unsafe "unsafe"
import . "kesme"
import . "bellekmanager"
import . "util"

type SayfaDizingirdi_2 uintptr

const (
	SayfaMevcut	uint32	= 0x001
	Sayfawritable	uint32	= 0x002
	SayfaKullanıcı	uint32	= 0x004
	SayfaÇerçeve	uint32	= 0xFFFFF000
	Sayfacow	uint32	= 0x200
)

func Ayarlabyteataddress(x byte, address uint32)
func Ayarlaunsignedinteger8ataddress(x uint8, address uint32)
func Ayarlaunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func ayarlacr3(sayfa_dizini uint32)
func getcr3() uint32

type Paging struct {
	TKesmehandler
}
type TcowÇerçevemanager struct {
	mem		*TBellekmanager
	refs		[]uint16
	çerçevecount	uint32
}

var (
	SayfaDizingirdi		uintptr
	SayfaTablogirdi		uint32
	pdelen			uint32
	virtlen			uint32
	cowÇerçevemanager	TcowÇerçevemanager
)

func (self *TcowÇerçevemanager) Init(mem *TBellekmanager, çerçevecount uint32) bool {
	self.mem = mem
	self.çerçevecount = çerçevecount
	referenceBayt := çerçevecount * uint32(unsafe.Sizeof(uint16(0)))
	referenceBelirteç := mem.Bellek_ayır(referenceBayt)
	if referenceBelirteç == nil {
		self.refs = nil
		self.çerçevecount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceBelirteç)[:çerçevecount:çerçevecount]
	for i := uint32(0); i < çerçevecount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TcowÇerçevemanager) Reference(çerçeve uint32) uint16 {
	idx := çerçeve >> 12
	if idx >= self.çerçevecount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowÇerçevemanager) Increment(çerçeve uint32) {
	idx := çerçeve >> 12
	if idx >= self.çerçevecount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TcowÇerçevemanager) Decrement(çerçeve uint32) {
	idx := çerçeve >> 12
	if idx >= self.çerçevecount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(sayfaDizingirdi uintptr, sayfaTablogirdi uint32, bellekmanager *TBellekmanager) {

	SayfaDizingirdi = sayfaDizingirdi
	SayfaTablogirdi = sayfaTablogirdi

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowÇerçevemanager.Init(bellekmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressBelirteç, _ := bellekmanager.Alignedmalloc(0x1000)
			if addressBelirteç == nil {
				return
			}
			address := uint32(uintptr(addressBelirteç))

			Ayarlaunsignedinteger32ataddress(address|0x87, uint32(sayfaDizingirdi)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Ayarlaunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		sayfaDizingirdi = sayfaDizingirdi + 0x1000
	}

}
func (self *Paging) SharedBellekregion() {

	sayfaDizingirdi := SayfaDizingirdi
	kSayfaDizingirdi := SayfaDizingirdi

	for i := uint32(1); i <= virtlen; i++ {

		sayfaDizingirdi = sayfaDizingirdi + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetDeğer(uint32(kSayfaDizingirdi) + pde*4)
			v = (v & 0xFFFFF000)
			Ayarlaunsignedinteger32ataddress(v|0x87, uint32(sayfaDizingirdi)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetDeğer(uint32(kSayfaDizingirdi) + pde*4)
			v = (v & 0xFFFFF000)
			Ayarlaunsignedinteger32ataddress(v|0x87, uint32(sayfaDizingirdi)+pde*4)

		}

	}
}
func (self *Paging) Sayfafault(manager *TKesmemanager) {
	kesmehandler = handlepagingKesme

	var address uintptr
	address = uintptr(unsafe.Pointer(&kesmehandler))
	self.TKesmehandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var kesmehandler func(uint32) uint32

func handlepagingKesme(esp uint32) uint32 {
	if ResolveKopyalaAçıkYazmafault() {
		return esp
	}
	return HandlefatalKesmeÇerçeve(esp, 0x0E)
}

func CloneaddressBoşlukcow(kaynakSayfaDizin uint32) uint32 {
	if AktifBellekmanager == nil || kaynakSayfaDizin == 0 {
		return 0
	}
	hedefBelirteç, _ := AktifBellekmanager.Alignedmalloc(0x1000)
	if hedefBelirteç == nil {
		return 0
	}
	hedefSayfaDizin := uint32(uintptr(hedefBelirteç))
	for i := uint32(0); i < 1024; i++ {
		Ayarlaunsignedinteger32ataddress(0, hedefSayfaDizin+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		kaynakpdeaddress := kaynakSayfaDizin + pde*4
		kaynakpde := GetDeğer(kaynakpdeaddress)
		if (kaynakpde & SayfaMevcut) == 0 {
			continue
		}
		if issharedpde(pde) {
			Ayarlaunsignedinteger32ataddress(kaynakpde, hedefSayfaDizin+pde*4)
			continue
		}

		hedefptBelirteç, _ := AktifBellekmanager.Alignedmalloc(0x1000)
		if hedefptBelirteç == nil {
			continue
		}
		kaynakpt := kaynakpde & SayfaÇerçeve
		hedefpt := uint32(uintptr(hedefptBelirteç))
		Ayarlaunsignedinteger32ataddress((hedefpt | (kaynakpde & 0xFFF)), hedefSayfaDizin+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := kaynakpt + pte*4
			girdi := GetDeğer(pteaddress)
			if (girdi & SayfaMevcut) != 0 {
				if (girdi & Sayfawritable) != 0 {
					girdi = (girdi &^ Sayfawritable) | Sayfacow
					Ayarlaunsignedinteger32ataddress(girdi, pteaddress)
					cowÇerçevemanager.Increment(girdi & SayfaÇerçeve)
				} else if (girdi & Sayfacow) != 0 {
					cowÇerçevemanager.Increment(girdi & SayfaÇerçeve)
				}
			}
			Ayarlaunsignedinteger32ataddress(girdi, hedefpt+pte*4)
		}
	}
	yenidenYüklecr3()
	return hedefSayfaDizin
}

func ResolveKopyalaAçıkYazmafault() bool {
	if AktifBellekmanager == nil {
		return false
	}
	faultaddress := getcr2()
	sayfa_dizini := getcr3()
	pdeaddress := sayfa_dizini + ((faultaddress>>22)&0x3FF)*4
	pde := GetDeğer(pdeaddress)
	if (pde & SayfaMevcut) == 0 {
		return false
	}
	pt := pde & SayfaÇerçeve
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetDeğer(pteaddress)
	if (pte&Sayfacow) == 0 || (pte&SayfaMevcut) == 0 {
		return false
	}
	oldÇerçeve := pte & SayfaÇerçeve
	if cowÇerçevemanager.Reference(oldÇerçeve) <= 1 {
		Ayarlaunsignedinteger32ataddress((pte|Sayfawritable)&^Sayfacow, pteaddress)
		yenidenYüklecr3()
		return true
	}

	yeniBelirteç, _ := AktifBellekmanager.Alignedmalloc(0x1000)
	if yeniBelirteç == nil {
		return false
	}
	yeniÇerçeve := uint32(uintptr(yeniBelirteç)) & SayfaÇerçeve

	kaynak_2 := GetBaytfromBelirteç(uintptr(faultaddress&SayfaÇerçeve), 0x1000, 0x1000)
	hedef_2 := GetBaytfromBelirteç(uintptr(yeniÇerçeve), 0x1000, 0x1000)
	copy(hedef_2, kaynak_2)
	cowÇerçevemanager.Decrement(oldÇerçeve)
	Ayarlaunsignedinteger32ataddress((yeniÇerçeve|(pte&0xFFF)|Sayfawritable)&^Sayfacow, pteaddress)
	yenidenYüklecr3()
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

func yenidenYüklecr3() {
	cr3 := getcr3()
	ayarlacr3(cr3)
}

func AyarlabyteGelenSayfaDizin(x byte, address uint32, sayfa_dizini uint32) {
	oldcr3 := getcr3()
	ayarlacr3(sayfa_dizini)
	Ayarlabyteataddress(x, address)
	ayarlacr3(oldcr3)
}

func AyarlaBlokGelenSayfaDizin(kaynak_2 []byte, hedef_2 []byte, boyut uint32, sayfa_dizini uint32) {
	if boyut == 0 || sayfa_dizini == 0 {
		return
	}
	oldcr3 := getcr3()
	ayarlacr3(sayfa_dizini)
	makeAralıkGizliÖzelwritableŞuan(sayfa_dizini, uint32(uintptr(unsafe.Pointer(&hedef_2[0]))), boyut)

	for i := uint32(0); i < boyut; i++ {
		hedef_2[i] = kaynak_2[i]
	}
	ayarlacr3(oldcr3)
}

func SıfırBlokGelenSayfaDizin(address uint32, boyut uint32, sayfa_dizini uint32) {
	if boyut == 0 || sayfa_dizini == 0 {
		return
	}
	oldcr3 := getcr3()
	ayarlacr3(sayfa_dizini)
	makeAralıkGizliÖzelwritableŞuan(sayfa_dizini, address, boyut)
	hedef_2 := GetBaytfromBelirteç(uintptr(address), int(boyut), int(boyut))
	for i := uint32(0); i < boyut; i++ {
		hedef_2[i] = 0
	}
	ayarlacr3(oldcr3)
}

func makeSayfaGizliÖzelwritableŞuan(sayfa_dizini uint32, sanaladdress uint32) bool {
	pde := GetDeğer(sayfa_dizini + ((sanaladdress>>22)&0x3FF)*4)
	if (pde & SayfaMevcut) == 0 {
		return false
	}
	pteaddress := (pde & SayfaÇerçeve) + ((sanaladdress>>12)&0x3FF)*4
	pte := GetDeğer(pteaddress)
	if (pte & SayfaMevcut) == 0 {
		return false
	}
	if (pte & Sayfacow) == 0 {
		return (pte & Sayfawritable) != 0
	}
	if AktifBellekmanager == nil {
		return false
	}
	yeniBelirteç, _ := AktifBellekmanager.Alignedmalloc(0x1000)
	if yeniBelirteç == nil {
		return false
	}
	yeniÇerçeve := uint32(uintptr(yeniBelirteç)) & SayfaÇerçeve
	kaynak_2 := GetBaytfromBelirteç(uintptr(sanaladdress&SayfaÇerçeve), 0x1000, 0x1000)
	hedef_2 := GetBaytfromBelirteç(uintptr(yeniÇerçeve), 0x1000, 0x1000)
	copy(hedef_2, kaynak_2)
	cowÇerçevemanager.Decrement(pte & SayfaÇerçeve)
	Ayarlaunsignedinteger32ataddress((yeniÇerçeve|(pte&0xFFF)|Sayfawritable)&^Sayfacow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	yenidenYüklecr3()
	return true
}

func makeAralıkGizliÖzelwritableŞuan(sayfa_dizini uint32, address uint32, boyut uint32) bool {
	if boyut == 0 {
		return true
	}
	son_2 := address + boyut - 1
	if son_2 < address {
		return false
	}
	for sayfa := address & SayfaÇerçeve; ; sayfa += 0x1000 {
		if !makeSayfaGizliÖzelwritableŞuan(sayfa_dizini, sayfa) {
			return false
		}
		if sayfa == (son_2 & SayfaÇerçeve) {
			break
		}
	}
	return true
}

func MakeAralıkGizliÖzelwritable(sayfa_dizini uint32, address uint32, boyut uint32) bool {
	if sayfa_dizini == 0 {
		return false
	}
	oldcr3 := getcr3()
	ayarlacr3(sayfa_dizini)
	tamam := makeAralıkGizliÖzelwritableŞuan(sayfa_dizini, address, boyut)
	ayarlacr3(oldcr3)
	return tamam
}

func Ayarlaunsignedinteger32GelenSayfaDizin(x uint32, address uint32, sayfa_dizini uint32) {
	if sayfa_dizini == 0 {
		return
	}
	oldcr3 := getcr3()
	ayarlacr3(sayfa_dizini)
	Ayarlaunsignedinteger32ataddress(x, address)
	ayarlacr3(oldcr3)
}

func GetDeğer(address uint32) uint32 {
	var orgDeğer uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgDeğer
}
func GetDeğerGelenSayfaDizin(address uint32, sayfa_dizini uint32) uint32 {
	if sayfa_dizini == 0 {
		return 0
	}
	oldcr3 := getcr3()
	ayarlacr3(sayfa_dizini)
	v := GetDeğer(address)
	ayarlacr3(oldcr3)
	return v
}

var v uint32 = 0

func KopyalaSayfaÇerçeveBlok(xSayfaDizin uint32, ySayfaDizin uint32, vaddress uint32) {
	if xSayfaDizin == 0 || ySayfaDizin == 0 {
		return
	}
	oldcr3 := getcr3()
	ayarlacr3(xSayfaDizin)
	v = GetDeğer(vaddress)
	Ayarlaunsignedinteger32GelenSayfaDizin(v, vaddress, ySayfaDizin)

	ayarlacr3(oldcr3)
}
