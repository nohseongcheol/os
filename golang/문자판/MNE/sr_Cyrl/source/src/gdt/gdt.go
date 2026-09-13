package gdt

import . "unsafe"
import "reflect"
import . "конзола"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegКорисникcode	uint32	= 0x23
	SegКорисникdata	uint32	= 0x2B
	SegКорисникgs	uint32	= 0x33
	SegЗадатакСтање	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	ограничиТихо_2		uint16
	baseТихо_2		uint16
	baseВисока_2		uint8
	врста_2			uint8
	параметриОграничиВисока	uint8
	baseveryВисока		uint8
}

func (исти_2 *TSegmentdescriptor) Init(base_2 uint32, ограничи_2 uint32, врста_2 uint8, параметри_3 uint8) {

	исти_2.baseТихо_2 = uint16(base_2 & 0xFFFF)
	исти_2.baseВисока_2 = uint8((base_2 >> 16) & 0xFF)
	исти_2.baseveryВисока = uint8((base_2 >> 24) & 0xFF)

	исти_2.ограничиТихо_2 = uint16(ограничи_2 & 0xFFFF)
	исти_2.параметриОграничиВисока = uint8((ограничи_2 >> 24) & 0x0F)
	исти_2.параметриОграничиВисока |= (параметри_3 & 0xF0)

	исти_2.врста_2 = врста_2

}

type TShareddescriptorТабелаdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorТабелаdata

type TShareddescriptorТабела struct {
}

func (исти_2 *TShareddescriptorТабела) Init() {

	var gdtунос TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressТихо) |
		uint32(gdtdescriptor.GdtaddressВисока)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtВеличина+1) / Sizeof(gdtунос))
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

	величина_2 := (*uint16)(Pointer(&одредиште_3[0]))
	(*величина_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&одредиште_3)))

	terminal := new(TКонзола)
	terminal.MШтампајxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Штампај(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (исти_2 *TShareddescriptorТабела) Скупdescriptor(idx int, base_2 uint32, ограничи_2 uint32, врста_2 uint8, параметри_3 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, ограничи_2, врста_2, параметри_3)
}

const (
	KcsПопис	= 1
	KdsПопис	= 2
	KgsПопис	= 3

	Kcsselector	= KcsПопис * 8
	Kdsselector	= KdsПопис * 8
	Kgsselector	= KgsПопис * 8

	Seggranbyte	= 0 << 7
	Seggran4kСТРАНА	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegСистем	= 0 << 4
	Segобичне	= 1 << 4

	Segnoexec	= 0 << 3
	Segизвршна	= 1 << 3

	Privkernel	= 0 << 5
	PrivКорисник	= 3 << 5

	SegbigРЕЖИМ	= 1 << 6

	Присутна	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescСадржај			= 3 << 1
	Udescrxonly			= 1 << 3
	UdescОграничиПримљеноpages	= 1 << 4
	UdescsegnotПрисутна		= 1 << 5
	Udescusable			= 1 << 6

	Gdtунос		= 256
	TlsПокрени	= 16
)

var (
	gdtТабела	= [Gdtунос]Gdtунос_2{}
	gdtdescriptor	Gdtdescriptor
	gdtТабелаlen	= 0
)

type Gdtунос_2 struct {
	ограничиТихо			uint16
	baseТихо			uint16
	basemid				uint8
	приступање			uint8
	ограничиВисокаandПараметри	uint8
	baseВисока			uint8
}

func (e *Gdtунос_2) IsПрисутна() bool {
	return e.приступање&Присутна != 0
}

func (e *Gdtунос_2) Fill(base uint32, ограничи uint32, приступање uint8, параметри uint8) {
	e.ограничиВисокаandПараметри = uint8((ограничи >> 16) & 0x000F)
	e.ограничиВисокаandПараметри |= параметри
	e.приступање = приступање
	e.basemid = uint8(base >> 16)
	e.baseВисока = uint8(base >> 24)
	e.baseТихо = uint16(base & 0xFFFF)
	e.ограничиТихо = uint16(ограничи & 0x0000FFFF)
}

func (e *Gdtунос_2) Очисти() {
	e.ограничиВисокаandПараметри = 0
	e.приступање = 0
	e.basemid = 0
	e.baseВисока = 0
	e.baseТихо = 0
	e.ограничиТихо = 0

}

type Gdtdescriptor struct {
	GdtВеличина		uint16
	GdtaddressТихо		uint16
	GdtaddressВисока	uint16
}
type Корисникdescriptor struct {
	Уносброј	uint32
	Baseaddress	uint32
	Ограничи	uint32
	Параметри	uint8
}

func Скупtlssegment(попис uint32, descriptor *Корисникdescriptor, табела []Gdtунос_2) bool {
	if попис < TlsПокрени || попис > uint32(len(gdtТабела)) {
		return false
	}

	if descriptor.Параметри == Udescrxonly|UdescsegnotПрисутна {

		табела[попис].Очисти()
		return true
	}

	параметри := uint8(Seggranbyte)
	if descriptor.Параметри&UdescОграничиПримљеноpages != 0 {
		параметри = Seggran4kСТРАНА
	}
	приступање := uint8(PrivКорисник | Segобичне | Присутна)
	if descriptor.Параметри&Udescrxonly != 0 {
		приступање |= Segизвршна
	} else {
		приступање |= Segw
	}
	if приступање&Segобичне != 0 {
		параметри |= SegbigРЕЖИМ
	}

	табела[попис].Fill(descriptor.Baseaddress, descriptor.Ограничи, приступање, параметри)
	flushtlsТабела(табела)

	return true
}

func flushtlsТабела(табела []Gdtунос_2) {
	copy(gdtТабела[TlsПокрени:], табела[TlsПокрени:])
}
func FlushtlsТабела(табела []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsПокрени:], табела[TlsПокрени:])
}
