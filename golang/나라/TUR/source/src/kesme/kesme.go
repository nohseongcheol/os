package Kesme

import . "unsafe"
import . "reflect"

import . "bağlantıNoktası"
import . "gdt"
import . "multitasking"
import . "konsol"

func kesmeignore()

func kesmeexceptionhandler()
func kesmeexceptionhandler0x00()
func kesmeexceptionhandler0x01()
func kesmeexceptionhandler0x02()
func kesmeexceptionhandler0x03()
func kesmeexceptionhandler0x04()
func kesmeexceptionhandler0x05()
func kesmeexceptionhandler0x06()
func kesmeexceptionhandler0x07()
func kesmeexceptionhandler0x08()
func kesmeexceptionhandler0x09()
func kesmeexceptionhandler0x0a()
func kesmeexceptionhandler0x0b()
func kesmeexceptionhandler0x0c()
func kesmeexceptionhandler0x0d()
func kesmeexceptionhandler0x0e()
func kesmeexceptionhandler0x0f()
func kesmeexceptionhandler0x10()
func kesmeexceptionhandler0x11()
func kesmeexceptionhandler0x12()
func kesmeexceptionhandler0x13()

func kesmerequesthandler0x00()
func kesmerequesthandler0x01()
func kesmerequesthandler0x02()
func kesmerequesthandler0x03()
func kesmerequesthandler0x04()
func kesmerequesthandler0x05()
func kesmerequesthandler0x06()
func kesmerequesthandler0x07()
func kesmerequesthandler0x08()
func kesmerequesthandler0x09()
func kesmerequesthandler0x0a()
func kesmerequesthandler0x0b()
func kesmerequesthandler0x0c()
func kesmerequesthandler0x0d()
func kesmerequesthandler0x0e()
func kesmerequesthandler0x0f()

func kesmerequesthandler0x80()
func kesmerequesthandler0x81()
func kesmerequesthandler0x82()

func DeneYazdır(konum uint8, data uint8)
func ayarlads(dssegment uint32)
func ayarlags(gssegment uint32)
func kesmeÇıkloop()

type TKesmehandler struct {
	KesmeSayı	uint8
	Kesmemanager	uintptr
}
type IKesmehandler interface {
	HandleKesme(uint32) uint32
}

func YeniKesmehandler(Kesmemanager uintptr, KesmeSayı uint8) *TKesmehandler {
	kesmehandler_2 := new(TKesmehandler)
	kesmehandler_2.KesmeSayı = KesmeSayı
	kesmehandler_2.Kesmemanager = Kesmemanager
	return kesmehandler_2

}

var handler_2 [256]uintptr

func (self *TKesmehandler) Init(KesmeSayı uint8, Kesmemanager uintptr, funcaddress uintptr) {

	handler_2[KesmeSayı] = funcaddress

	self.KesmeSayı = KesmeSayı
	self.Kesmemanager = Kesmemanager

}
func (self *TKesmehandler) AyarlahandleKesmefuction(KesmeSayı uint32, address uintptr) {
	handler_2[KesmeSayı] = address
}
func (self *TKesmehandler) YokEt() {
	selfuintptr := uintptr(Pointer(self))
	Kesmemanager := (*TKesmemanager)(Pointer(self.Kesmemanager))
	if selfuintptr == Kesmemanager.Gethandler(self.KesmeSayı) {
		Kesmemanager.Ayarlahandler(0, self.KesmeSayı)
	}

}
func (self *TKesmehandler) AyarlaKesmemanager(Kesmemanager uintptr) {
}
func (self *TKesmehandler) AyarlaKesmeSayı(KesmeSayı uint8) {
	self.KesmeSayı = KesmeSayı
}
func (self *TKesmehandler) HandleKesme(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konsol_2 := TKonsol{}
	konsol_2.MYazdır(buffer)
	return esp
}
func HandleKesme1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konsol_2 := TKonsol{}
	konsol_2.MYazdır(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TKesmedescriptorTabloBelirteç struct {
}

var idtdata [256 * 8]uint8
var AktifKesmemanager uintptr = 0

const kesmeHataAyıkla = false

type TKesmemanager struct {
	handler_2	[256]uintptr

	donanımKesmeoffset	uint16

	görevmanager	*TGörevmanager
}

var PrimarypicKomutGirdiÇıktıBağlantıNoktası uint16 = 0x20
var PrimarypicdataGirdiÇıktıBağlantıNoktası uint16 = 0x21
var SecondarypicKomutGirdiÇıktıBağlantıNoktası uint16 = 0xA0
var SecondarypicdataGirdiÇıktıBağlantıNoktası uint16 = 0xA1

func (self *TKesmemanager) Init(donanımKesmeoffset uint16, geneldescriptorTablo *TShareddescriptorTablo, görevmanager *TGörevmanager) {

	self.görevmanager = görevmanager

	self.donanımKesmeoffset = donanımKesmeoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtKesmegate uint8 = 0xE
	address = uint32(ValueOf(kesmeignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(kesmeexceptionhandler0x0f).Pointer())
		self.KesmedescriptorTablogirdiayarla(i, codesegment, address, 0, IdtKesmegate)
	}

	address = uint32(ValueOf(kesmeexceptionhandler0x00).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x00, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x01).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x01, codesegment, address, 0, IdtKesmegate)
	address = uint32(ValueOf(kesmeexceptionhandler0x02).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x02, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x03).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x03, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x04).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x04, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x05).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x05, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x06).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x06, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x07).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x07, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x08).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x08, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x09).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x09, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x0a).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x0A, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x0b).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x0B, codesegment, address, 0, IdtKesmegate)
	address = uint32(ValueOf(kesmeexceptionhandler0x0c).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x0C, codesegment, address, 0, IdtKesmegate)
	address = uint32(ValueOf(kesmeexceptionhandler0x0d).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x0D, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x0e).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x0E, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x0f).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x0F, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x10).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x10, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x11).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x11, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x12).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x12, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmeexceptionhandler0x13).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x13, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x00).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x20, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x01).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x21, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x02).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x22, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x03).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x23, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x04).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x24, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x05).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x25, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x06).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x26, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x07).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x27, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x08).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x28, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x09).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x29, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x0a).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x2A, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x0b).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x2B, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x0c).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x2C, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x0d).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x2D, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x0e).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x2E, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x0f).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x2F, codesegment, address, 0, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x80).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x80, codesegment, address, 3, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x81).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x81, codesegment, address, 3, IdtKesmegate)

	address = uint32(ValueOf(kesmerequesthandler0x82).Pointer())
	self.KesmedescriptorTablogirdiayarla(0x82, codesegment, address, 3, IdtKesmegate)

	BağlantıNoktasıYazmabyte(PrimarypicKomutGirdiÇıktıBağlantıNoktası, 0x11)
	BağlantıNoktasıYazmabyte(SecondarypicKomutGirdiÇıktıBağlantıNoktası, 0x11)

	BağlantıNoktasıYazmabyte(PrimarypicdataGirdiÇıktıBağlantıNoktası, 0x20)
	BağlantıNoktasıYazmabyte(SecondarypicdataGirdiÇıktıBağlantıNoktası, 0x28)

	BağlantıNoktasıYazmabyte(PrimarypicdataGirdiÇıktıBağlantıNoktası, 0x04)
	BağlantıNoktasıYazmabyte(SecondarypicdataGirdiÇıktıBağlantıNoktası, 0x02)

	BağlantıNoktasıYazmabyte(PrimarypicdataGirdiÇıktıBağlantıNoktası, 0x01)
	BağlantıNoktasıYazmabyte(SecondarypicdataGirdiÇıktıBağlantıNoktası, 0x01)

	BağlantıNoktasıYazmabyte(PrimarypicdataGirdiÇıktıBağlantıNoktası, 0xF8)
	BağlantıNoktasıYazmabyte(SecondarypicdataGirdiÇıktıBağlantıNoktası, 0xEF)

	idtBelirteç := [6]uint8{0, 0, 0, 0, 0, 0}
	boyut := (*uint16)(Pointer(&idtBelirteç[0]))
	(*boyut) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtBelirteç[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtBelirteç)))
}
func Lidt(lidtaddr uintptr)

func (self *TKesmemanager) KesmedescriptorTablogirdiayarla(kesme int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTür uint8) {

	handleraddressDüşükbit := (*uint16)(Pointer(&idtdata[kesme*8+0]))
	(*handleraddressDüşükbit) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[kesme*8+2]))
	(*gdtcodesegmentselector) = codesegment

	rezerve := (*uint8)(Pointer(&idtdata[kesme*8+4]))
	(*rezerve) = 0

	var IdtdescriptorMevcut uint8 = 0x80
	erişim := (*uint8)(Pointer(&idtdata[kesme*8+5]))
	(*erişim) = (IdtdescriptorMevcut | DescriptorTür | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressYüksekbit := (*uint16)(Pointer(&idtdata[kesme*8+6]))
	(*handleraddressYüksekbit) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TKesmemanager) Ayarlahandler(handler uintptr, KesmeSayı uint8) {
	handler_2[KesmeSayı] = handler
}
func (self *TKesmemanager) Gethandler(KesmeSayı uint8) uintptr {
	return handler_2[KesmeSayı]
}
func (self *TKesmemanager) DohandleKesme(kesme uint8, esp uint32) uint32 {

	if kesmeHataAyıkla {
		konsol_2.MYazdırxy("[esp:", 1, 20)
		konsol_2.MUnsignedinteger32Yazdır(uint32(kesme))
		konsol_2.MYazdır(":")
		konsol_2.MUnsignedinteger32Yazdır(esp)
	}
	handlerÇalıştır := false
	if handler_2[kesme] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[kesme])))
		esp = myfunction(esp)
		handlerÇalıştır = true

	}

	if !handlerÇalıştır && kesme == uint8(self.donanımKesmeoffset) && self.görevmanager != nil {
		esp = uint32(uintptr(Pointer(self.görevmanager.Schedule((*TcpuDurum)(Pointer(uintptr(esp)))))))

	}
	if !handlerÇalıştır && kesme == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if kesme <= 0x1F {
	}
	if 0x20 <= kesme && kesme < 0x30 {
		if 0x28 <= kesme {
			BağlantıNoktasıYazmabyte(SecondarypicKomutGirdiÇıktıBağlantıNoktası, 0x20)
		}
		BağlantıNoktasıYazmabyte(PrimarypicKomutGirdiÇıktıBağlantıNoktası, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func ayarlacr3(address uint32)

var konsol_2 TKonsol = TKonsol{}

func HandleKesme(esp uint32, kesme uint32) uint32 {

	if kesmeHataAyıkla && kesme != 0x80 && kesme != 0x20 {
		konsol_2.MYazdırxy("[esp:", 1, 21)
		konsol_2.MUnsignedinteger32Yazdır(uint32(kesme))
		konsol_2.MYazdır(":")
		konsol_2.MUnsignedinteger32Yazdır(esp)
	}

	if AktifKesmemanager != 0 {
		p := (*TKesmemanager)(Pointer(AktifKesmemanager))
		esp = p.DohandleKesme(uint8(kesme), esp)
		return esp
	}
	if handler_2[kesme] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[kesme])))
		esp = myfunction(esp)
	}
	if kesme == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= kesme && kesme < 0x30 {
		if 0x28 <= kesme {
			BağlantıNoktasıYazmabyte(SecondarypicKomutGirdiÇıktıBağlantıNoktası, 0x20)
		}
		BağlantıNoktasıYazmabyte(PrimarypicKomutGirdiÇıktıBağlantıNoktası, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	mİB := (*TcpuDurum)(Pointer(uintptr(esp)))
	if mİB.Eax == 1 || mİB.Eax == 252 {
		mİB.Eip = uint32(ValueOf(kesmeÇıkloop).Pointer())
		mİB.Cs = Segkernelcode
		mİB.Ds = Segkerneldata
		mİB.Es = Segkerneldata
		mİB.Fs = Segkerneldata
		mİB.Gs = Segkernelgs
		mİB.Ss = Segkerneldata
		mİB.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasHatacode(kesme uint32) bool {
	switch kesme {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionİsim(kesme uint32) string {
	switch kesme {
	case 0x00:
		return "#DE divide error"
	case 0x06:
		return "#UD invalid opcode"
	case 0x08:
		return "#DF double fault"
	case 0x0A:
		return "#TS invalid TSS"
	case 0x0B:
		return "#NP segment not present"
	case 0x0C:
		return "#SS stack fault"
	case 0x0D:
		return "#GP general protection"
	case 0x0E:
		return "#PF page fault"
	case 0x11:
		return "#AC alignment check"
	}
	return "#EX exception"
}

func exceptionÇerçeveDeğer(çerçeve uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(çerçeve + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func yazdırSayfafaultBilgi(hata uint32) {
	MEmergencyGünlükKatar(" pf=[")
	if (hata & 0x01) != 0 {
		MEmergencyGünlükKatar("protection")
	} else {
		MEmergencyGünlükKatar("not-present")
	}
	if (hata & 0x02) != 0 {
		MEmergencyGünlükKatar(",write")
	} else {
		MEmergencyGünlükKatar(",read")
	}
	if (hata & 0x04) != 0 {
		MEmergencyGünlükKatar(",user")
	} else {
		MEmergencyGünlükKatar(",kernel")
	}
	if (hata & 0x08) != 0 {
		MEmergencyGünlükKatar(",reserved-bit")
	}
	if (hata & 0x10) != 0 {
		MEmergencyGünlükKatar(",instruction-fetch")
	}
	MEmergencyGünlükKatar("]")
}

func yazdırexceptionselectorBilgi(hata uint32) {
	MEmergencyGünlükKatar(" selector=")
	MEmergencyGünlükunsignedinteger32(hata & 0xFFFFFFF8)
	MEmergencyGünlükKatar(" index=")
	MEmergencyGünlükunsignedinteger32(hata >> 3)
	MEmergencyGünlükKatar(" table=")
	if (hata & 0x02) != 0 {
		MEmergencyGünlükKatar("IDT")
	} else if (hata & 0x04) != 0 {
		MEmergencyGünlükKatar("LDT")
	} else {
		MEmergencyGünlükKatar("GDT")
	}
	MEmergencyGünlükKatar(" ext=")
	MEmergencyGünlükunsignedinteger32(hata & 0x01)
}

func Handleexception(esp uint32, kesme uint32) uint32 {
	MEmergencyGünlükKatar("\nEXCEPTION vec=")
	MEmergencyGünlükhexadecimal8(uint8(kesme))
	MEmergencyGünlükKatar(" ")
	MEmergencyGünlükKatar(exceptionİsim(kesme))
	MEmergencyGünlükKatar(" frame=")
	MEmergencyGünlükunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyGünlükKatar(" invalid-frame")
		if exceptionhasHatacode(kesme) {
			MEmergencyGünlükKatar(" raw-error-or-bad-esp=")
			MEmergencyGünlükunsignedinteger32(esp)
			yazdırexceptionselectorBilgi(esp)
		}
		MEmergencyGünlükKatar("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var hata uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasHatacode(kesme) {
		hata = exceptionÇerçeveDeğer(esp, 0)
		eipoffset = 4
	}
	eip := exceptionÇerçeveDeğer(esp, eipoffset)
	cs := exceptionÇerçeveDeğer(esp, eipoffset+4)
	eflags := exceptionÇerçeveDeğer(esp, eipoffset+8)

	MEmergencyGünlükKatar(" err=")
	MEmergencyGünlükunsignedinteger32(hata)
	MEmergencyGünlükKatar(" eip=")
	MEmergencyGünlükunsignedinteger32(eip)
	MEmergencyGünlükKatar(" cs=")
	MEmergencyGünlükunsignedinteger32(cs)
	MEmergencyGünlükKatar(" eflags=")
	MEmergencyGünlükunsignedinteger32(eflags)
	MEmergencyGünlükKatar(" cr0=")
	MEmergencyGünlükunsignedinteger32(exceptioncr0())
	MEmergencyGünlükKatar(" cr3=")
	MEmergencyGünlükunsignedinteger32(exceptioncr3())

	if kesme == 0x0E {
		MEmergencyGünlükKatar(" cr2=")
		MEmergencyGünlükunsignedinteger32(exceptioncr2())
		yazdırSayfafaultBilgi(hata)
	}

	if (cs & 0x03) != 0 {
		MEmergencyGünlükKatar(" useresp=")
		MEmergencyGünlükunsignedinteger32(exceptionÇerçeveDeğer(esp, eipoffset+12))
		MEmergencyGünlükKatar(" ss=")
		MEmergencyGünlükunsignedinteger32(exceptionÇerçeveDeğer(esp, eipoffset+16))
	}

	if exceptionhasHatacode(kesme) {
		yazdırexceptionselectorBilgi(hata)
	}
	MEmergencyGünlükKatar("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltSonrafatalexception()

func HandlefatalKesmeÇerçeve(kaydedildiesp uint32, kesme uint32) uint32 {
	Handleexception(kaydedildiesp+52, kesme)
	haltSonrafatalexception()
	return kaydedildiesp
}

func KesmeAktif()
func (self *TKesmemanager) Aktif() {
	if AktifKesmemanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	AktifKesmemanager = address
	KesmeAktif()
}
func Kesmedeactive()
func (self *TKesmemanager) Deactive() {
	AktifKesmemanager = 0
	Kesmedeactive()
}

func MyhandleKesme(kesme uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konsol_2 := TKonsol{}
	konsol_2.MYazdır(buffer)
	return esp
}
func MyDene(kesme uint8, esp uint32)

func UnhandleKesme() {
	buffer := []byte("unhandle interrupt\n")
	konsol_2 := TKonsol{}
	konsol_2.MYazdır(buffer)
}

func kesmehandler_2(kesme uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konsol_2 := TKonsol{}
	konsol_2.MYazdır(buffer)
	konsol_2.MHexadecimalYazdır(0x40)
	return esp
}
func yazdıresp(esp uint32) {
	konsol_2 := TKonsol{}
	konsol_2.MUnsignedinteger32Yazdırxy(esp, 20, 21)
}
func gettls() uint32
func Yazdırtls() {

}
