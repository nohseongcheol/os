package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegFoydalanuvchicode	uint32	= 0x23
	SegFoydalanuvchidata	uint32	= 0x2B
	SegFoydalanuvchigs	uint32	= 0x33
	Segtaskstate		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitPast_2		uint16
	basePast_2		uint16
	baseYuqori_2		uint8
	turi			uint8
	bayroqlarlimitYuqori	uint8
	baseveryYuqori		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, turi uint8, bayroqlar_2 uint8) {

	self_2.basePast_2 = uint16(base_2 & 0xFFFF)
	self_2.baseYuqori_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryYuqori = uint8((base_2 >> 24) & 0xFF)

	self_2.limitPast_2 = uint16(limit_2 & 0xFFFF)
	self_2.bayroqlarlimitYuqori = uint8((limit_2 >> 24) & 0x0F)
	self_2.bayroqlarlimitYuqori |= (bayroqlar_2 & 0xF0)

	self_2.turi = turi

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
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressPast) |
		uint32(gdtdescriptor.GdtaddressYuqori)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtHajmi+1) / Sizeof(gdtentry))
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

	hajmi_2 := (*uint16)(Pointer(&destination_3[0]))
	(*hajmi_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MChopetishxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Chopetish(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, turi uint8, bayroqlar_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, turi, bayroqlar_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4kSAHIFA	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegTizim	= 0 << 4
	SegOʻrtacha	= 1 << 4

	Segnoexec	= 0 << 3
	SegBajarish	= 1 << 3

	Privkernel		= 0 << 5
	PrivFoydalanuvchi	= 3 << 5

	SegbigRejim	= 1 << 6

	Present	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescTarkibi			= 3 << 1
	Udescrxonly			= 1 << 3
	UdesclimitYaqinlashtirishpages	= 1 << 4
	Udescsegnotpresent		= 1 << 5
	Udescusable			= 1 << 6

	Gdtentry	= 256
	TlsBoshlash	= 16
)

var (
	gdttable	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdttablelen	= 0
)

type Gdtentry_2 struct {
	limitPast		uint16
	basePast		uint16
	basemid			uint8
	ruxsat			uint8
	limitYuqoriandBayroqlar	uint8
	baseYuqori		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.ruxsat&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, ruxsat uint8, bayroqlar uint8) {
	e.limitYuqoriandBayroqlar = uint8((limit >> 16) & 0x000F)
	e.limitYuqoriandBayroqlar |= bayroqlar
	e.ruxsat = ruxsat
	e.basemid = uint8(base >> 16)
	e.baseYuqori = uint8(base >> 24)
	e.basePast = uint16(base & 0xFFFF)
	e.limitPast = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Tozalash() {
	e.limitYuqoriandBayroqlar = 0
	e.ruxsat = 0
	e.basemid = 0
	e.baseYuqori = 0
	e.basePast = 0
	e.limitPast = 0

}

type Gdtdescriptor struct {
	GdtHajmi		uint16
	GdtaddressPast		uint16
	GdtaddressYuqori	uint16
}
type Foydalanuvchidescriptor struct {
	EntryRAQAM	uint32
	Baseaddress	uint32
	Limit		uint32
	Bayroqlar	uint8
}

func Settlssegment(index uint32, descriptor *Foydalanuvchidescriptor, table []Gdtentry_2) bool {
	if index < TlsBoshlash || index > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Bayroqlar == Udescrxonly|Udescsegnotpresent {

		table[index].Tozalash()
		return true
	}

	bayroqlar := uint8(Seggranbyte)
	if descriptor.Bayroqlar&UdesclimitYaqinlashtirishpages != 0 {
		bayroqlar = Seggran4kSAHIFA
	}
	ruxsat := uint8(PrivFoydalanuvchi | SegOʻrtacha | Present)
	if descriptor.Bayroqlar&Udescrxonly != 0 {
		ruxsat |= SegBajarish
	} else {
		ruxsat |= Segw
	}
	if ruxsat&SegOʻrtacha != 0 {
		bayroqlar |= SegbigRejim
	}

	table[index].Fill(descriptor.Baseaddress, descriptor.Limit, ruxsat, bayroqlar)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdtentry_2) {
	copy(gdttable[TlsBoshlash:], table[TlsBoshlash:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsBoshlash:], table[TlsBoshlash:])
}
