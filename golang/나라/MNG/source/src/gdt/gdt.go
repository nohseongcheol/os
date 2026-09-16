/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "консол"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegХэрэглэгчcode	uint32	= 0x23
	SegХэрэглэгчdata	uint32	= 0x2B
	SegХэрэглэгчgs		uint32	= 0x33
	Segtaskstate		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitБага_2			uint16
	baseБага_2			uint16
	baseБүрэнцэнэглэгдсэн_2		uint8
	төрөл				uint8
	төлвүүдlimitБүрэнцэнэглэгдсэн	uint8
	baseveryБүрэнцэнэглэгдсэн	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, төрөл uint8, төлвүүд_2 uint8) {

	self_2.baseБага_2 = uint16(base_2 & 0xFFFF)
	self_2.baseБүрэнцэнэглэгдсэн_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryБүрэнцэнэглэгдсэн = uint8((base_2 >> 24) & 0xFF)

	self_2.limitБага_2 = uint16(limit_2 & 0xFFFF)
	self_2.төлвүүдlimitБүрэнцэнэглэгдсэн = uint8((limit_2 >> 24) & 0x0F)
	self_2.төлвүүдlimitБүрэнцэнэглэгдсэн |= (төлвүүд_2 & 0xF0)

	self_2.төрөл = төрөл

}

type TShareddescriptortabledata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptortabledata

type TShareddescriptortable struct {
}

func (self_2 *TShareddescriptortable) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressБага) |
		uint32(gdtdescriptor.GdtaddressБүрэнцэнэглэгдсэн)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtХэмжээ+1) / Sizeof(gdtentry))
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

	хэмжээ_2 := (*uint16)(Pointer(&destination_3[0]))
	(*хэмжээ_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TКонсол)
	terminal.MХэвлэхxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Хэвлэх(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, төрөл uint8, төлвүүд_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, төрөл, төлвүүд_2)
}

const (
	KcsҮзүүлэлт	= 1
	KdsҮзүүлэлт	= 2
	KgsҮзүүлэлт	= 3

	Kcsselector	= KcsҮзүүлэлт * 8
	Kdsselector	= KdsҮзүүлэлт * 8
	Kgsselector	= KgsҮзүүлэлт * 8

	Seggranbyte	= 0 << 7
	Seggran4kХУУДАС	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegСистем	= 0 << 4
	Segnormal	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	PrivХэрэглэгч	= 3 << 5

	SegbigГорим	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescАгуулга		= 3 << 1
	Udescrxonly		= 1 << 3
	Udesclimitinpages	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsЭхлэл	= 16
)

var (
	gdttable	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdttablelen	= 0
)

type Gdtentry_2 struct {
	limitБага				uint16
	baseБага				uint16
	basemid					uint8
	access					uint8
	limitБүрэнцэнэглэгдсэнandТөлвүүд	uint8
	baseБүрэнцэнэглэгдсэн			uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.access&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, access uint8, төлвүүд uint8) {
	e.limitБүрэнцэнэглэгдсэнandТөлвүүд = uint8((limit >> 16) & 0x000F)
	e.limitБүрэнцэнэглэгдсэнandТөлвүүд |= төлвүүд
	e.access = access
	e.basemid = uint8(base >> 16)
	e.baseБүрэнцэнэглэгдсэн = uint8(base >> 24)
	e.baseБага = uint16(base & 0xFFFF)
	e.limitБага = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Цэвэрлэх() {
	e.limitБүрэнцэнэглэгдсэнandТөлвүүд = 0
	e.access = 0
	e.basemid = 0
	e.baseБүрэнцэнэглэгдсэн = 0
	e.baseБага = 0
	e.limitБага = 0

}

type Gdtdescriptor struct {
	GdtХэмжээ			uint16
	GdtaddressБага			uint16
	GdtaddressБүрэнцэнэглэгдсэн	uint16
}
type Хэрэглэгчdescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Limit		uint32
	Төлвүүд		uint8
}

func Settlssegment(үзүүлэлт uint32, descriptor *Хэрэглэгчdescriptor, table []Gdtentry_2) bool {
	if үзүүлэлт < TlsЭхлэл || үзүүлэлт > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Төлвүүд == Udescrxonly|Udescsegnotpresent {

		table[үзүүлэлт].Цэвэрлэх()
		return true
	}

	төлвүүд := uint8(Seggranbyte)
	if descriptor.Төлвүүд&Udesclimitinpages != 0 {
		төлвүүд = Seggran4kХУУДАС
	}
	access := uint8(PrivХэрэглэгч | Segnormal | Present)
	if descriptor.Төлвүүд&Udescrxonly != 0 {
		access |= Segexec
	} else {
		access |= Segw
	}
	if access&Segnormal != 0 {
		төлвүүд |= SegbigГорим
	}

	table[үзүүлэлт].Fill(descriptor.Baseaddress, descriptor.Limit, access, төлвүүд)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdtentry_2) {
	copy(gdttable[TlsЭхлэл:], table[TlsЭхлэл:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsЭхлэл:], table[TlsЭхлэл:])
}
