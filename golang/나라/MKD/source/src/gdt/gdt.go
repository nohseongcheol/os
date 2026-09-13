package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegКорисникcode	uint32	= 0x23
	SegКорисникdata	uint32	= 0x2B
	SegКорисникgs	uint32	= 0x33
	Segtaskstate	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitlow_2		uint16
	baselow_2		uint16
	basehigh_2		uint8
	тип			uint8
	атрибутиlimithigh	uint8
	baseveryhigh		uint8
}

func (само_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, тип uint8, атрибути_2 uint8) {

	само_2.baselow_2 = uint16(base_2 & 0xFFFF)
	само_2.basehigh_2 = uint8((base_2 >> 16) & 0xFF)
	само_2.baseveryhigh = uint8((base_2 >> 24) & 0xFF)

	само_2.limitlow_2 = uint16(limit_2 & 0xFFFF)
	само_2.атрибутиlimithigh = uint8((limit_2 >> 24) & 0x0F)
	само_2.атрибутиlimithigh |= (атрибути_2 & 0xF0)

	само_2.тип = тип

}

type TShareddescriptorТабелаdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorТабелаdata

type TShareddescriptorТабела struct {
}

func (само_2 *TShareddescriptorТабела) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddresslow) |
		uint32(gdtdescriptor.Gdtaddresshigh)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtГолемина+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	одредиште_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&одредиште_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	големина_2 := (*uint16)(Pointer(&одредиште_3[0]))
	(*големина_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&одредиште_3)))

	terminal := new(TConsole)
	terminal.MПечатиxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Печати(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (само_2 *TShareddescriptorТабела) Поставиdescriptor(idx int, base_2 uint32, limit_2 uint32, тип uint8, атрибути_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, тип, атрибути_2)
}

const (
	KcsИндекс	= 1
	KdsИндекс	= 2
	KgsИндекс	= 3

	Kcsselector	= KcsИндекс * 8
	Kdsselector	= KdsИндекс * 8
	Kgsselector	= KgsИндекс * 8

	Seggranbyte		= 0 << 7
	Seggran4kСтраница	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegСистем	= 0 << 4
	SegНормално	= 1 << 4

	Segnoexec	= 0 << 3
	SegИзвршна	= 1 << 3

	Privkernel	= 0 << 5
	PrivКорисник	= 3 << 5

	SegbigРежим	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescСодржини		= 3 << 1
	Udescrxonly		= 1 << 3
	UdesclimitвоСтрани	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsПушти	= 16
)

var (
	gdtТабела	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtТабелаlen	= 0
)

type Gdtentry_2 struct {
	limitlow		uint16
	baselow			uint16
	basemid			uint8
	пристап			uint8
	limithighandАтрибути	uint8
	basehigh		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.пристап&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, пристап uint8, атрибути uint8) {
	e.limithighandАтрибути = uint8((limit >> 16) & 0x000F)
	e.limithighandАтрибути |= атрибути
	e.пристап = пристап
	e.basemid = uint8(base >> 16)
	e.basehigh = uint8(base >> 24)
	e.baselow = uint16(base & 0xFFFF)
	e.limitlow = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Исчисти() {
	e.limithighandАтрибути = 0
	e.пристап = 0
	e.basemid = 0
	e.basehigh = 0
	e.baselow = 0
	e.limitlow = 0

}

type Gdtdescriptor struct {
	GdtГолемина	uint16
	Gdtaddresslow	uint16
	Gdtaddresshigh	uint16
}
type Корисникdescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Limit		uint32
	Атрибути	uint8
}

func Поставиtlssegment(индекс uint32, descriptor *Корисникdescriptor, табела []Gdtentry_2) bool {
	if индекс < TlsПушти || индекс > uint32(len(gdtТабела)) {
		return false
	}

	if descriptor.Атрибути == Udescrxonly|Udescsegnotpresent {

		табела[индекс].Исчисти()
		return true
	}

	атрибути := uint8(Seggranbyte)
	if descriptor.Атрибути&UdesclimitвоСтрани != 0 {
		атрибути = Seggran4kСтраница
	}
	пристап := uint8(PrivКорисник | SegНормално | Present)
	if descriptor.Атрибути&Udescrxonly != 0 {
		пристап |= SegИзвршна
	} else {
		пристап |= Segw
	}
	if пристап&SegНормално != 0 {
		атрибути |= SegbigРежим
	}

	табела[индекс].Fill(descriptor.Baseaddress, descriptor.Limit, пристап, атрибути)
	flushtlsТабела(табела)

	return true
}

func flushtlsТабела(табела []Gdtentry_2) {
	copy(gdtТабела[TlsПушти:], табела[TlsПушти:])
}
func FlushtlsТабела(табела []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsПушти:], табела[TlsПушти:])
}
