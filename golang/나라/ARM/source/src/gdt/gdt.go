package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegՕգտագործողcode	uint32	= 0x23
	SegՕգտագործողdata	uint32	= 0x2B
	SegՕգտագործողgs		uint32	= 0x33
	SegtaskՎիճակ		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitՑածր_2		uint16
	baseՑածր_2		uint16
	baseԲարձր_2		uint8
	տիպ			uint8
	դրոշներlimitԲարձր	uint8
	baseveryԲարձր		uint8
}

func (ինքնուրույն_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, տիպ uint8, դրոշներ_2 uint8) {

	ինքնուրույն_2.baseՑածր_2 = uint16(base_2 & 0xFFFF)
	ինքնուրույն_2.baseԲարձր_2 = uint8((base_2 >> 16) & 0xFF)
	ինքնուրույն_2.baseveryԲարձր = uint8((base_2 >> 24) & 0xFF)

	ինքնուրույն_2.limitՑածր_2 = uint16(limit_2 & 0xFFFF)
	ինքնուրույն_2.դրոշներlimitԲարձր = uint8((limit_2 >> 24) & 0x0F)
	ինքնուրույն_2.դրոշներlimitԲարձր |= (դրոշներ_2 & 0xF0)

	ինքնուրույն_2.տիպ = տիպ

}

type TShareddescriptorԱղյուսակdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorԱղյուսակdata

type TShareddescriptorԱղյուսակ struct {
}

func (ինքնուրույն_2 *TShareddescriptorԱղյուսակ) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressՑածր) |
		uint32(gdtdescriptor.GdtaddressԲարձր)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtՉափս+1) / Sizeof(gdtentry))
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

	չափս_2 := (*uint16)(Pointer(&destination_3[0]))
	(*չափս_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MՏպելxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Տպել(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (ինքնուրույն_2 *TShareddescriptorԱղյուսակ) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, տիպ uint8, դրոշներ_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, տիպ, դրոշներ_2)
}

const (
	KcsԻնդեքս	= 1
	KdsԻնդեքս	= 2
	KgsԻնդեքս	= 3

	Kcsselector	= KcsԻնդեքս * 8
	Kdsselector	= KdsԻնդեքս * 8
	Kgsselector	= KgsԻնդեքս * 8

	Seggranbyte	= 0 << 7
	Seggran4kԷջ	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegՀամակարգ	= 0 << 4
	SegՆորմալ	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	PrivՕգտագործող	= 3 << 5

	SegbigՌեժիմ	= 1 << 6

	Ներկա	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescԲովանդակություն	= 3 << 1
	Udescrxonly		= 1 << 3
	UdesclimitՄեջpages	= 1 << 4
	UdescsegnotՆերկա	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsՍկիզբ	= 16
)

var (
	gdtԱղյուսակ	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtԱղյուսակlen	= 0
)

type Gdtentry_2 struct {
	limitՑածր		uint16
	baseՑածր		uint16
	basemid			uint8
	մուտք			uint8
	limitԲարձրandԴրոշներ	uint8
	baseԲարձր		uint8
}

func (e *Gdtentry_2) IsՆերկա() bool {
	return e.մուտք&Ներկա != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, մուտք uint8, դրոշներ uint8) {
	e.limitԲարձրandԴրոշներ = uint8((limit >> 16) & 0x000F)
	e.limitԲարձրandԴրոշներ |= դրոշներ
	e.մուտք = մուտք
	e.basemid = uint8(base >> 16)
	e.baseԲարձր = uint8(base >> 24)
	e.baseՑածր = uint16(base & 0xFFFF)
	e.limitՑածր = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Ջնջել() {
	e.limitԲարձրandԴրոշներ = 0
	e.մուտք = 0
	e.basemid = 0
	e.baseԲարձր = 0
	e.baseՑածր = 0
	e.limitՑածր = 0

}

type Gdtdescriptor struct {
	GdtՉափս		uint16
	GdtaddressՑածր	uint16
	GdtaddressԲարձր	uint16
}
type Օգտագործողdescriptor struct {
	EntryՀԱՄԱՐ	uint32
	Baseaddress	uint32
	Limit		uint32
	Դրոշներ		uint8
}

func Settlssegment(ինդեքս uint32, descriptor *Օգտագործողdescriptor, աղյուսակ []Gdtentry_2) bool {
	if ինդեքս < TlsՍկիզբ || ինդեքս > uint32(len(gdtԱղյուսակ)) {
		return false
	}

	if descriptor.Դրոշներ == Udescrxonly|UdescsegnotՆերկա {

		աղյուսակ[ինդեքս].Ջնջել()
		return true
	}

	դրոշներ := uint8(Seggranbyte)
	if descriptor.Դրոշներ&UdesclimitՄեջpages != 0 {
		դրոշներ = Seggran4kԷջ
	}
	մուտք := uint8(PrivՕգտագործող | SegՆորմալ | Ներկա)
	if descriptor.Դրոշներ&Udescrxonly != 0 {
		մուտք |= Segexec
	} else {
		մուտք |= Segw
	}
	if մուտք&SegՆորմալ != 0 {
		դրոշներ |= SegbigՌեժիմ
	}

	աղյուսակ[ինդեքս].Fill(descriptor.Baseaddress, descriptor.Limit, մուտք, դրոշներ)
	flushtlsԱղյուսակ(աղյուսակ)

	return true
}

func flushtlsԱղյուսակ(աղյուսակ []Gdtentry_2) {
	copy(gdtԱղյուսակ[TlsՍկիզբ:], աղյուսակ[TlsՍկիզբ:])
}
func FlushtlsԱղյուսակ(աղյուսակ []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsՍկիզբ:], աղյուսակ[TlsՍկիզբ:])
}
