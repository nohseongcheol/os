package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegКарыстальнікcode	uint32	= 0x23
	SegКарыстальнікdata	uint32	= 0x2B
	SegКарыстальнікgs	uint32	= 0x33
	SegЗадачаСтан		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	абмежавацьНізкі_2	uint16
	baseНізкі_2		uint16
	baseВысокі_2		uint8
	тып			uint8
	сцяжкіАбмежавацьВысокі	uint8
	baseveryВысокі		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, абмежаваць_2 uint32, тып uint8, сцяжкі_2 uint8) {

	self_2.baseНізкі_2 = uint16(base_2 & 0xFFFF)
	self_2.baseВысокі_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryВысокі = uint8((base_2 >> 24) & 0xFF)

	self_2.абмежавацьНізкі_2 = uint16(абмежаваць_2 & 0xFFFF)
	self_2.сцяжкіАбмежавацьВысокі = uint8((абмежаваць_2 >> 24) & 0x0F)
	self_2.сцяжкіАбмежавацьВысокі |= (сцяжкі_2 & 0xF0)

	self_2.тып = тып

}

type TShareddescriptorТабліцаdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorТабліцаdata

type TShareddescriptorТабліца struct {
}

func (self_2 *TShareddescriptorТабліца) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressНізкі) |
		uint32(gdtdescriptor.GdtaddressВысокі)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtПамер+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destination_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&destination_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	памер_2 := (*uint16)(Pointer(&destination_3[0]))
	(*памер_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MДрукавацьxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Друкаваць(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorТабліца) Вызначанаdescriptor(idx int, base_2 uint32, абмежаваць_2 uint32, тып uint8, сцяжкі_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, абмежаваць_2, тып, сцяжкі_2)
}

const (
	KcsЗмест	= 1
	KdsЗмест	= 2
	KgsЗмест	= 3

	Kcsselector	= KcsЗмест * 8
	Kdsselector	= KdsЗмест * 8
	Kgsselector	= KgsЗмест * 8

	Seggranbyte		= 0 << 7
	Seggran4kСтаронка	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegСістэма	= 0 << 4
	SegЗвычайны	= 1 << 4

	Segnoexec	= 0 << 3
	SegВыкананне	= 1 << 3

	Privkernel		= 0 << 5
	PrivКарыстальнік	= 3 << 5

	SegbigРЭЖЫМ	= 1 << 6

	Прысутнічае	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescЗмест		= 3 << 1
	Udescrxonly		= 1 << 3
	UdescАбмежавацьуpages	= 1 << 4
	UdescsegnotПрысутнічае	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsУключыць	= 16
)

var (
	gdtТабліца	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtТабліцаlen	= 0
)

type Gdtentry_2 struct {
	абмежавацьНізкі			uint16
	baseНізкі			uint16
	basemid				uint8
	доступ				uint8
	абмежавацьВысокіandСцяжкі	uint8
	baseВысокі			uint8
}

func (e *Gdtentry_2) IsПрысутнічае() bool {
	return e.доступ&Прысутнічае != 0
}

func (e *Gdtentry_2) Fill(base uint32, абмежаваць uint32, доступ uint8, сцяжкі uint8) {
	e.абмежавацьВысокіandСцяжкі = uint8((абмежаваць >> 16) & 0x000F)
	e.абмежавацьВысокіandСцяжкі |= сцяжкі
	e.доступ = доступ
	e.basemid = uint8(base >> 16)
	e.baseВысокі = uint8(base >> 24)
	e.baseНізкі = uint16(base & 0xFFFF)
	e.абмежавацьНізкі = uint16(абмежаваць & 0x0000FFFF)
}

func (e *Gdtentry_2) Ачысціць() {
	e.абмежавацьВысокіandСцяжкі = 0
	e.доступ = 0
	e.basemid = 0
	e.baseВысокі = 0
	e.baseНізкі = 0
	e.абмежавацьНізкі = 0

}

type Gdtdescriptor struct {
	GdtПамер		uint16
	GdtaddressНізкі		uint16
	GdtaddressВысокі	uint16
}
type Карыстальнікdescriptor struct {
	EntryНУМАР	uint32
	Baseaddress	uint32
	Абмежаваць	uint32
	Сцяжкі		uint8
}

func Вызначанаtlssegment(змест uint32, descriptor *Карыстальнікdescriptor, табліца []Gdtentry_2) bool {
	if змест < TlsУключыць || змест > uint32(len(gdtТабліца)) {
		return false
	}

	if descriptor.Сцяжкі == Udescrxonly|UdescsegnotПрысутнічае {

		табліца[змест].Ачысціць()
		return true
	}

	сцяжкі := uint8(Seggranbyte)
	if descriptor.Сцяжкі&UdescАбмежавацьуpages != 0 {
		сцяжкі = Seggran4kСтаронка
	}
	доступ := uint8(PrivКарыстальнік | SegЗвычайны | Прысутнічае)
	if descriptor.Сцяжкі&Udescrxonly != 0 {
		доступ |= SegВыкананне
	} else {
		доступ |= Segw
	}
	if доступ&SegЗвычайны != 0 {
		сцяжкі |= SegbigРЭЖЫМ
	}

	табліца[змест].Fill(descriptor.Baseaddress, descriptor.Абмежаваць, доступ, сцяжкі)
	flushtlsТабліца(табліца)

	return true
}

func flushtlsТабліца(табліца []Gdtentry_2) {
	copy(gdtТабліца[TlsУключыць:], табліца[TlsУключыць:])
}
func FlushtlsТабліца(табліца []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsУключыць:], табліца[TlsУключыць:])
}
