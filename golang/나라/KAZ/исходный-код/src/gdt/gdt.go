package gdt

import . "unsafe"
import "reflect"
import . "консоль"

const (
	Segядроcode	uint32	= 0x08
	Segядроданные	uint32	= 0x10
	Segядроgs	uint32	= 0x18

	Segпользовательcode	uint32	= 0x23
	Segпользовательданные	uint32	= 0x2B
	Segпользовательgs	uint32	= 0x33
	SegзадачаСостояние	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	ограничениеНизкий_2	uint16
	baseНизкий_2		uint16
	baseВысокий_2		uint8
	тип_2			uint8
	флагиОграничениеВысокий	uint8
	baseveryВысокий		uint8
}

func (текущий_2 *TSegmentdescriptor) Init(base_2 uint32, ограничение_2 uint32, тип_2 uint8, флаги_2 uint8) {

	текущий_2.baseНизкий_2 = uint16(base_2 & 0xFFFF)
	текущий_2.baseВысокий_2 = uint8((base_2 >> 16) & 0xFF)
	текущий_2.baseveryВысокий = uint8((base_2 >> 24) & 0xFF)

	текущий_2.ограничениеНизкий_2 = uint16(ограничение_2 & 0xFFFF)
	текущий_2.флагиОграничениеВысокий = uint8((ограничение_2 >> 24) & 0x0F)
	текущий_2.флагиОграничениеВысокий |= (флаги_2 & 0xF0)

	текущий_2.тип_2 = тип_2

}

type TShareddescriptorТаблицаданные struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var данные_2 TShareddescriptorТаблицаданные

type TShareddescriptorТаблица struct {
}

func (текущий_2 *TShareddescriptorТаблица) Init() {

	var gdtзапись TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressНизкий) |
		uint32(gdtdescriptor.GdtaddressВысокий)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtРазмер+1) / Sizeof(gdtзапись))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(данные_2.segmentdescriptor[:], oldgdt)

	данные_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	данные_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	данные_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	назначение_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&назначение_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&данные_2)))

	размер_2 := (*uint16)(Pointer(&назначение_3[0]))
	(*размер_2) = (uint16)((Sizeof(данные_2)))

	gdtfunc(uintptr(Pointer(&назначение_3)))

	terminal := new(TКонсоль)
	terminal.MПечатьxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Печать(uint32(uintptr(Pointer(&данные_2.segmentdescriptor[3]))))

}
func (текущий_2 *TShareddescriptorТаблица) Указатьdescriptor(idx int, base_2 uint32, ограничение_2 uint32, тип_2 uint8, флаги_2 uint8) {
	данные_2.segmentdescriptor[idx].Init(base_2, ограничение_2, тип_2, флаги_2)
}

const (
	KcsСодержание	= 1
	KdsСодержание	= 2
	KgsСодержание	= 3

	Kcsselector	= KcsСодержание * 8
	Kdsselector	= KdsСодержание * 8
	Kgsselector	= KgsСодержание * 8

	Seggranбайт		= 0 << 7
	Seggran4kстраница	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segсистема	= 0 << 4
	Segнормальный	= 1 << 4

	Segnoexec	= 0 << 3
	SegВыполнение	= 1 << 3

	Privядро		= 0 << 5
	Privпользователь	= 3 << 5

	Segbigрежим	= 1 << 6

	Присутствует	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescСодержание			= 3 << 1
	Udescrxтолько			= 1 << 3
	UdescОграничениеИсходящийpages	= 1 << 4
	UdescsegnotПрисутствует		= 1 << 5
	Udescusable			= 1 << 6

	Gdtзапись	= 256
	TlsПуск		= 16
)

var (
	gdtТаблица	= [Gdtзапись]Gdtзапись_2{}
	gdtdescriptor	Gdtdescriptor
	gdtТаблицаlen	= 0
)

type Gdtзапись_2 struct {
	ограничениеНизкий		uint16
	baseНизкий			uint16
	basemid				uint8
	доступ				uint8
	ограничениеВысокийиФлаги	uint8
	baseВысокий			uint8
}

func (e *Gdtзапись_2) IsПрисутствует() bool {
	return e.доступ&Присутствует != 0
}

func (e *Gdtзапись_2) Fill(base uint32, ограничение uint32, доступ uint8, флаги uint8) {
	e.ограничениеВысокийиФлаги = uint8((ограничение >> 16) & 0x000F)
	e.ограничениеВысокийиФлаги |= флаги
	e.доступ = доступ
	e.basemid = uint8(base >> 16)
	e.baseВысокий = uint8(base >> 24)
	e.baseНизкий = uint16(base & 0xFFFF)
	e.ограничениеНизкий = uint16(ограничение & 0x0000FFFF)
}

func (e *Gdtзапись_2) Очистить() {
	e.ограничениеВысокийиФлаги = 0
	e.доступ = 0
	e.basemid = 0
	e.baseВысокий = 0
	e.baseНизкий = 0
	e.ограничениеНизкий = 0

}

type Gdtdescriptor struct {
	GdtРазмер		uint16
	GdtaddressНизкий	uint16
	GdtaddressВысокий	uint16
}
type Пользовательdescriptor struct {
	ЗаписьЧисло	uint32
	Baseaddress	uint32
	Ограничение	uint32
	Флаги		uint8
}

func Указатьtlssegment(содержание uint32, descriptor *Пользовательdescriptor, таблица []Gdtзапись_2) bool {
	if содержание < TlsПуск || содержание > uint32(len(gdtТаблица)) {
		return false
	}

	if descriptor.Флаги == Udescrxтолько|UdescsegnotПрисутствует {

		таблица[содержание].Очистить()
		return true
	}

	флаги := uint8(Seggranбайт)
	if descriptor.Флаги&UdescОграничениеИсходящийpages != 0 {
		флаги = Seggran4kстраница
	}
	доступ := uint8(Privпользователь | Segнормальный | Присутствует)
	if descriptor.Флаги&Udescrxтолько != 0 {
		доступ |= SegВыполнение
	} else {
		доступ |= Segw
	}
	if доступ&Segнормальный != 0 {
		флаги |= Segbigрежим
	}

	таблица[содержание].Fill(descriptor.Baseaddress, descriptor.Ограничение, доступ, флаги)
	flushtlsТаблица(таблица)

	return true
}

func flushtlsТаблица(таблица []Gdtзапись_2) {
	copy(gdtТаблица[TlsПуск:], таблица[TlsПуск:])
}
func FlushtlsТаблица(таблица []TSegmentdescriptor) {
	copy(данные_2.segmentdescriptor[TlsПуск:], таблица[TlsПуск:])
}
