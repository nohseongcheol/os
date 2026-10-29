/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "консоль"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegКористувачcode	uint32	= 0x23
	SegКористувачdata	uint32	= 0x2B
	SegКористувачgs		uint32	= 0x33
	SegЗадачаСтан		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	обмеженняНизька_2	uint16
	baseНизька_2		uint16
	baseВисокий_2		uint8
	тип_2			uint8
	прапориОбмеженняВисокий	uint8
	baseveryВисокий		uint8
}

func (поточний_2 *TSegmentdescriptor) Init(base_2 uint32, обмеження_2 uint32, тип_2 uint8, прапори_2 uint8) {

	поточний_2.baseНизька_2 = uint16(base_2 & 0xFFFF)
	поточний_2.baseВисокий_2 = uint8((base_2 >> 16) & 0xFF)
	поточний_2.baseveryВисокий = uint8((base_2 >> 24) & 0xFF)

	поточний_2.обмеженняНизька_2 = uint16(обмеження_2 & 0xFFFF)
	поточний_2.прапориОбмеженняВисокий = uint8((обмеження_2 >> 24) & 0x0F)
	поточний_2.прапориОбмеженняВисокий |= (прапори_2 & 0xF0)

	поточний_2.тип_2 = тип_2

}

type TShareddescriptorТаблицяdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorТаблицяdata

type TShareddescriptorТаблиця struct {
}

func (поточний_2 *TShareddescriptorТаблиця) Init() {

	var gdtзапис TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtАдреса := uintptr(uint32(gdtdescriptor.GdtАдресаНизька) |
		uint32(gdtdescriptor.GdtАдресаВисокий)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtРозмір+1) / Sizeof(gdtзапис))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtАдреса,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	призначення_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseАдреса := (*uint32)(Pointer(&призначення_3[2]))
	(*baseАдреса) = uint32(uintptr(Pointer(&data_2)))

	розмір_2 := (*uint16)(Pointer(&призначення_3[0]))
	(*розмір_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&призначення_3)))

	terminal := new(TКонсоль)
	terminal.MДрукxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Друк(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (поточний_2 *TShareddescriptorТаблиця) Множинаdescriptor(idx int, base_2 uint32, обмеження_2 uint32, тип_2 uint8, прапори_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, обмеження_2, тип_2, прапори_2)
}

const (
	KcsІндекс	= 1
	KdsІндекс	= 2
	KgsІндекс	= 3

	Kcsselector	= KcsІндекс * 8
	Kdsselector	= KdsІндекс * 8
	Kgsselector	= KgsІндекс * 8

	Seggranbyte		= 0 << 7
	Seggran4kСторінка	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegСистема	= 0 << 4
	SegЗвичайний	= 1 << 4

	Segnoexec	= 0 << 3
	SegВиконати	= 1 << 3

	Privkernel	= 0 << 5
	PrivКористувач	= 3 << 5

	SegbigРЕЖИМ	= 1 << 6

	Присутній	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescЗміст			= 3 << 1
	Udescrxonly			= 1 << 3
	UdescОбмеженняВхіднийСторінки	= 1 << 4
	UdescsegnotПрисутній		= 1 << 5
	Udescusable			= 1 << 6

	Gdtзапис	= 256
	TlsЗапустити	= 16
)

var (
	gdtТаблиця	= [Gdtзапис]Gdtзапис_2{}
	gdtdescriptor	Gdtdescriptor
	gdtТаблицяlen	= 0
)

type Gdtзапис_2 struct {
	обмеженняНизька			uint16
	baseНизька			uint16
	basemid				uint8
	доступ				uint8
	обмеженняВисокийandПрапори	uint8
	baseВисокий			uint8
}

func (e *Gdtзапис_2) IsПрисутній() bool {
	return e.доступ&Присутній != 0
}

func (e *Gdtзапис_2) Fill(base uint32, обмеження uint32, доступ uint8, прапори uint8) {
	e.обмеженняВисокийandПрапори = uint8((обмеження >> 16) & 0x000F)
	e.обмеженняВисокийandПрапори |= прапори
	e.доступ = доступ
	e.basemid = uint8(base >> 16)
	e.baseВисокий = uint8(base >> 24)
	e.baseНизька = uint16(base & 0xFFFF)
	e.обмеженняНизька = uint16(обмеження & 0x0000FFFF)
}

func (e *Gdtзапис_2) Очистити() {
	e.обмеженняВисокийandПрапори = 0
	e.доступ = 0
	e.basemid = 0
	e.baseВисокий = 0
	e.baseНизька = 0
	e.обмеженняНизька = 0

}

type Gdtdescriptor struct {
	GdtРозмір		uint16
	GdtАдресаНизька		uint16
	GdtАдресаВисокий	uint16
}
type Користувачdescriptor struct {
	ЗаписЧисло	uint32
	BaseАдреса	uint32
	Обмеження	uint32
	Прапори		uint8
}

func Множинаtlssegment(індекс uint32, descriptor *Користувачdescriptor, таблиця []Gdtзапис_2) bool {
	if індекс < TlsЗапустити || індекс > uint32(len(gdtТаблиця)) {
		return false
	}

	if descriptor.Прапори == Udescrxonly|UdescsegnotПрисутній {

		таблиця[індекс].Очистити()
		return true
	}

	прапори := uint8(Seggranbyte)
	if descriptor.Прапори&UdescОбмеженняВхіднийСторінки != 0 {
		прапори = Seggran4kСторінка
	}
	доступ := uint8(PrivКористувач | SegЗвичайний | Присутній)
	if descriptor.Прапори&Udescrxonly != 0 {
		доступ |= SegВиконати
	} else {
		доступ |= Segw
	}
	if доступ&SegЗвичайний != 0 {
		прапори |= SegbigРЕЖИМ
	}

	таблиця[індекс].Fill(descriptor.BaseАдреса, descriptor.Обмеження, доступ, прапори)
	flushtlsТаблиця(таблиця)

	return true
}

func flushtlsТаблиця(таблиця []Gdtзапис_2) {
	copy(gdtТаблиця[TlsЗапустити:], таблиця[TlsЗапустити:])
}
func FlushtlsТаблиця(таблиця []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsЗапустити:], таблиця[TlsЗапустити:])
}
