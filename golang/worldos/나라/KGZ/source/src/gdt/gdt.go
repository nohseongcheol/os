/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegКолдонуучуcode	uint32	= 0x23
	SegКолдонуучуdata	uint32	= 0x2B
	SegКолдонуучуgs		uint32	= 0x33
	SegtaskАбал		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitlow_2		uint16
	baselow_2		uint16
	basehigh_2		uint8
	түрү			uint8
	желектериlimithigh	uint8
	baseveryhigh		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, түрү uint8, желектери_2 uint8) {

	self_2.baselow_2 = uint16(base_2 & 0xFFFF)
	self_2.basehigh_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryhigh = uint8((base_2 >> 24) & 0xFF)

	self_2.limitlow_2 = uint16(limit_2 & 0xFFFF)
	self_2.желектериlimithigh = uint8((limit_2 >> 24) & 0x0F)
	self_2.желектериlimithigh |= (желектери_2 & 0xF0)

	self_2.түрү = түрү

}

type TShareddescriptorЖадыбалdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorЖадыбалdata

type TShareddescriptorЖадыбал struct {
}

func (self_2 *TShareddescriptorЖадыбал) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddresslow) |
		uint32(gdtdescriptor.Gdtaddresshigh)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtӨлчөм+1) / Sizeof(gdtentry))
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

	өлчөм_2 := (*uint16)(Pointer(&destination_3[0]))
	(*өлчөм_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MБасмаxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Басма(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorЖадыбал) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, түрү uint8, желектери_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, түрү, желектери_2)
}

const (
	KcsМазмун	= 1
	KdsМазмун	= 2
	KgsМазмун	= 3

	Kcsselector	= KcsМазмун * 8
	Kdsselector	= KdsМазмун * 8
	Kgsselector	= KgsМазмун * 8

	Seggranbyte	= 0 << 7
	Seggran4kБАРАК	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegСистема	= 0 << 4
	SegКадимкидей	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	PrivКолдонуучу	= 3 << 5

	SegbigРежим	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescМазмун		= 3 << 1
	Udescrxonly		= 1 << 3
	UdesclimitЧоңойтууpages	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsЖүргүзүү	= 16
)

var (
	gdtЖадыбал	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtЖадыбалlen	= 0
)

type Gdtentry_2 struct {
	limitlow		uint16
	baselow			uint16
	basemid			uint8
	кирүү			uint8
	limithighandЖелектери	uint8
	basehigh		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.кирүү&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, кирүү uint8, желектери uint8) {
	e.limithighandЖелектери = uint8((limit >> 16) & 0x000F)
	e.limithighandЖелектери |= желектери
	e.кирүү = кирүү
	e.basemid = uint8(base >> 16)
	e.basehigh = uint8(base >> 24)
	e.baselow = uint16(base & 0xFFFF)
	e.limitlow = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Тзл() {
	e.limithighandЖелектери = 0
	e.кирүү = 0
	e.basemid = 0
	e.basehigh = 0
	e.baselow = 0
	e.limitlow = 0

}

type Gdtdescriptor struct {
	GdtӨлчөм	uint16
	Gdtaddresslow	uint16
	Gdtaddresshigh	uint16
}
type Колдонуучуdescriptor struct {
	EntryНОМЕР	uint32
	Baseaddress	uint32
	Limit		uint32
	Желектери	uint8
}

func Settlssegment(мазмун uint32, descriptor *Колдонуучуdescriptor, жадыбал []Gdtentry_2) bool {
	if мазмун < TlsЖүргүзүү || мазмун > uint32(len(gdtЖадыбал)) {
		return false
	}

	if descriptor.Желектери == Udescrxonly|Udescsegnotpresent {

		жадыбал[мазмун].Тзл()
		return true
	}

	желектери := uint8(Seggranbyte)
	if descriptor.Желектери&UdesclimitЧоңойтууpages != 0 {
		желектери = Seggran4kБАРАК
	}
	кирүү := uint8(PrivКолдонуучу | SegКадимкидей | Present)
	if descriptor.Желектери&Udescrxonly != 0 {
		кирүү |= Segexec
	} else {
		кирүү |= Segw
	}
	if кирүү&SegКадимкидей != 0 {
		желектери |= SegbigРежим
	}

	жадыбал[мазмун].Fill(descriptor.Baseaddress, descriptor.Limit, кирүү, желектери)
	flushtlsЖадыбал(жадыбал)

	return true
}

func flushtlsЖадыбал(жадыбал []Gdtentry_2) {
	copy(gdtЖадыбал[TlsЖүргүзүү:], жадыбал[TlsЖүргүзүү:])
}
func FlushtlsЖадыбал(жадыбал []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsЖүргүзүү:], жадыбал[TlsЖүргүзүү:])
}
