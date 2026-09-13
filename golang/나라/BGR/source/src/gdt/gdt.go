package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegСобственикcode	uint32	= 0x23
	SegСобственикdata	uint32	= 0x2B
	SegСобственикgs		uint32	= 0x33
	SegЗадачаСъстояние	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	ограничениеНисък_2	uint16
	baseНисък_2		uint16
	baseВисок_2		uint8
	тип			uint8
	флаговеОграничениеВисок	uint8
	baseveryВисок		uint8
}

func (себеси_2 *TSegmentdescriptor) Init(base_2 uint32, ограничение_2 uint32, тип uint8, флагове_2 uint8) {

	себеси_2.baseНисък_2 = uint16(base_2 & 0xFFFF)
	себеси_2.baseВисок_2 = uint8((base_2 >> 16) & 0xFF)
	себеси_2.baseveryВисок = uint8((base_2 >> 24) & 0xFF)

	себеси_2.ограничениеНисък_2 = uint16(ограничение_2 & 0xFFFF)
	себеси_2.флаговеОграничениеВисок = uint8((ограничение_2 >> 24) & 0x0F)
	себеси_2.флаговеОграничениеВисок |= (флагове_2 & 0xF0)

	себеси_2.тип = тип

}

type TShareddescriptorТаблицаdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorТаблицаdata

type TShareddescriptorТаблица struct {
}

func (себеси_2 *TShareddescriptorТаблица) Init() {

	var gdtзапис TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressНисък) |
		uint32(gdtdescriptor.GdtaddressВисок)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtРазмер+1) / Sizeof(gdtзапис))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	назначение_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&назначение_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	размер_2 := (*uint16)(Pointer(&назначение_3[0]))
	(*размер_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&назначение_3)))

	terminal := new(TConsole)
	terminal.MПечатxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Печат(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (себеси_2 *TShareddescriptorТаблица) Задайdescriptor(idx int, base_2 uint32, ограничение_2 uint32, тип uint8, флагове_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, ограничение_2, тип, флагове_2)
}

const (
	KcsСъдържание	= 1
	KdsСъдържание	= 2
	KgsСъдържание	= 3

	Kcsselector	= KcsСъдържание * 8
	Kdsselector	= KdsСъдържание * 8
	Kgsselector	= KgsСъдържание * 8

	Seggranbyte		= 0 << 7
	Seggran4kСтраница	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegСистема	= 0 << 4
	SegНормален	= 1 << 4

	Segnoexec	= 0 << 3
	SegИзпълнение	= 1 << 3

	Privkernel	= 0 << 5
	PrivСобственик	= 3 << 5

	SegbigРЕЖИМ	= 1 << 6

	Налична	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescРъководство		= 3 << 1
	Udescrxonly			= 1 << 3
	UdescОграничениеВходящСтраници	= 1 << 4
	UdescsegnotНалична		= 1 << 5
	Udescusable			= 1 << 6

	Gdtзапис	= 256
	TlsСтартиране	= 16
)

var (
	gdtТаблица	= [Gdtзапис]Gdtзапис_2{}
	gdtdescriptor	Gdtdescriptor
	gdtТаблицаlen	= 0
)

type Gdtзапис_2 struct {
	ограничениеНисък		uint16
	baseНисък			uint16
	basemid				uint8
	достъп				uint8
	ограничениеВисокandФлагове	uint8
	baseВисок			uint8
}

func (e *Gdtзапис_2) IsНалична() bool {
	return e.достъп&Налична != 0
}

func (e *Gdtзапис_2) Fill(base uint32, ограничение uint32, достъп uint8, флагове uint8) {
	e.ограничениеВисокandФлагове = uint8((ограничение >> 16) & 0x000F)
	e.ограничениеВисокandФлагове |= флагове
	e.достъп = достъп
	e.basemid = uint8(base >> 16)
	e.baseВисок = uint8(base >> 24)
	e.baseНисък = uint16(base & 0xFFFF)
	e.ограничениеНисък = uint16(ограничение & 0x0000FFFF)
}

func (e *Gdtзапис_2) Изчистване() {
	e.ограничениеВисокandФлагове = 0
	e.достъп = 0
	e.basemid = 0
	e.baseВисок = 0
	e.baseНисък = 0
	e.ограничениеНисък = 0

}

type Gdtdescriptor struct {
	GdtРазмер	uint16
	GdtaddressНисък	uint16
	GdtaddressВисок	uint16
}
type Собственикdescriptor struct {
	ЗаписЧисло	uint32
	Baseaddress	uint32
	Ограничение	uint32
	Флагове		uint8
}

func Задайtlssegment(съдържание uint32, descriptor *Собственикdescriptor, таблица []Gdtзапис_2) bool {
	if съдържание < TlsСтартиране || съдържание > uint32(len(gdtТаблица)) {
		return false
	}

	if descriptor.Флагове == Udescrxonly|UdescsegnotНалична {

		таблица[съдържание].Изчистване()
		return true
	}

	флагове := uint8(Seggranbyte)
	if descriptor.Флагове&UdescОграничениеВходящСтраници != 0 {
		флагове = Seggran4kСтраница
	}
	достъп := uint8(PrivСобственик | SegНормален | Налична)
	if descriptor.Флагове&Udescrxonly != 0 {
		достъп |= SegИзпълнение
	} else {
		достъп |= Segw
	}
	if достъп&SegНормален != 0 {
		флагове |= SegbigРЕЖИМ
	}

	таблица[съдържание].Fill(descriptor.Baseaddress, descriptor.Ограничение, достъп, флагове)
	flushtlsТаблица(таблица)

	return true
}

func flushtlsТаблица(таблица []Gdtзапис_2) {
	copy(gdtТаблица[TlsСтартиране:], таблица[TlsСтартиране:])
}
func FlushtlsТаблица(таблица []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsСтартиране:], таблица[TlsСтартиране:])
}
