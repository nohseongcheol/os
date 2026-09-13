package gdt

import . "unsafe"
import "reflect"
import . "konsolë"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegPërdoruesicode	uint32	= 0x23
	SegPërdoruesidata	uint32	= 0x2B
	SegPërdoruesigs		uint32	= 0x33
	SegProcesGjendje	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	kufiUlët_2		uint16
	baseUlët_2		uint16
	baseLartë_2		uint8
	lloji			uint8
	flamurkaKufiLartë	uint8
	baseveryLartë		uint8
}

func (vetvetja_2 *TSegmentdescriptor) Init(base_2 uint32, kufi_2 uint32, lloji uint8, flamurka_2 uint8) {

	vetvetja_2.baseUlët_2 = uint16(base_2 & 0xFFFF)
	vetvetja_2.baseLartë_2 = uint8((base_2 >> 16) & 0xFF)
	vetvetja_2.baseveryLartë = uint8((base_2 >> 24) & 0xFF)

	vetvetja_2.kufiUlët_2 = uint16(kufi_2 & 0xFFFF)
	vetvetja_2.flamurkaKufiLartë = uint8((kufi_2 >> 24) & 0x0F)
	vetvetja_2.flamurkaKufiLartë |= (flamurka_2 & 0xF0)

	vetvetja_2.lloji = lloji

}

type TShareddescriptorTabeladata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorTabeladata

type TShareddescriptorTabela struct {
}

func (vetvetja_2 *TShareddescriptorTabela) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressUlët) |
		uint32(gdtdescriptor.GdtaddressLartë)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtMadhësia+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destinacioni_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&destinacioni_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	madhësia_2 := (*uint16)(Pointer(&destinacioni_3[0]))
	(*madhësia_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destinacioni_3)))

	terminal := new(TKonsolë)
	terminal.MPrintoxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Printo(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (vetvetja_2 *TShareddescriptorTabela) Caktonidescriptor(idx int, base_2 uint32, kufi_2 uint32, lloji uint8, flamurka_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, kufi_2, lloji, flamurka_2)
}

const (
	KcsTreguesi	= 1
	KdsTreguesi	= 2
	KgsTreguesi	= 3

	Kcsselector	= KcsTreguesi * 8
	Kdsselector	= KdsTreguesi * 8
	Kgsselector	= KgsTreguesi * 8

	Seggranbyte	= 0 << 7
	Seggran4kfaqe	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistemi	= 0 << 4
	SegNormale	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	PrivPërdoruesi	= 3 << 5

	Segbigmënyrë	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescPërmbajtja		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescKufiZmadhoFaqe	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsFillo	= 16
)

var (
	gdtTabela	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTabelalen	= 0
)

type Gdtentry_2 struct {
	kufiUlët		uint16
	baseUlët		uint16
	basemid			uint8
	futja			uint8
	kufiLartëandFlamurka	uint8
	baseLartë		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.futja&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, kufi uint32, futja uint8, flamurka uint8) {
	e.kufiLartëandFlamurka = uint8((kufi >> 16) & 0x000F)
	e.kufiLartëandFlamurka |= flamurka
	e.futja = futja
	e.basemid = uint8(base >> 16)
	e.baseLartë = uint8(base >> 24)
	e.baseUlët = uint16(base & 0xFFFF)
	e.kufiUlët = uint16(kufi & 0x0000FFFF)
}

func (e *Gdtentry_2) Pastro() {
	e.kufiLartëandFlamurka = 0
	e.futja = 0
	e.basemid = 0
	e.baseLartë = 0
	e.baseUlët = 0
	e.kufiUlët = 0

}

type Gdtdescriptor struct {
	GdtMadhësia	uint16
	GdtaddressUlët	uint16
	GdtaddressLartë	uint16
}
type Përdoruesidescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Kufi		uint32
	Flamurka	uint8
}

func Caktonitlssegment(treguesi uint32, descriptor *Përdoruesidescriptor, tabela []Gdtentry_2) bool {
	if treguesi < TlsFillo || treguesi > uint32(len(gdtTabela)) {
		return false
	}

	if descriptor.Flamurka == Udescrxonly|Udescsegnotpresent {

		tabela[treguesi].Pastro()
		return true
	}

	flamurka := uint8(Seggranbyte)
	if descriptor.Flamurka&UdescKufiZmadhoFaqe != 0 {
		flamurka = Seggran4kfaqe
	}
	futja := uint8(PrivPërdoruesi | SegNormale | Present)
	if descriptor.Flamurka&Udescrxonly != 0 {
		futja |= Segexec
	} else {
		futja |= Segw
	}
	if futja&SegNormale != 0 {
		flamurka |= Segbigmënyrë
	}

	tabela[treguesi].Fill(descriptor.Baseaddress, descriptor.Kufi, futja, flamurka)
	flushtlsTabela(tabela)

	return true
}

func flushtlsTabela(tabela []Gdtentry_2) {
	copy(gdtTabela[TlsFillo:], tabela[TlsFillo:])
}
func FlushtlsTabela(tabela []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsFillo:], tabela[TlsFillo:])
}
