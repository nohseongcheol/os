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

	SegBrúkaricode	uint32	= 0x23
	SegBrúkaridata	uint32	= 0x2B
	SegBrúkarigs	uint32	= 0x33
	SegtaskStøða	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitLágur_2	uint16
	baseLágur_2	uint16
	baseHøgt_2	uint8
	typeValue	uint8
	flagslimitHøgt	uint8
	baseveryHøgt	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, typeValue uint8, flags_2 uint8) {

	self_2.baseLágur_2 = uint16(base_2 & 0xFFFF)
	self_2.baseHøgt_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryHøgt = uint8((base_2 >> 24) & 0xFF)

	self_2.limitLágur_2 = uint16(limit_2 & 0xFFFF)
	self_2.flagslimitHøgt = uint8((limit_2 >> 24) & 0x0F)
	self_2.flagslimitHøgt |= (flags_2 & 0xF0)

	self_2.typeValue = typeValue

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
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressLágur) |
		uint32(gdtdescriptor.GdtaddressHøgt)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtStødd+1) / Sizeof(gdtentry))
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

	stødd_2 := (*uint16)(Pointer(&destination_3[0]))
	(*stødd_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MPrintxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32print(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, typeValue uint8, flags_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, typeValue, flags_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4kpage	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segsystem	= 0 << 4
	Segnormal	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	PrivBrúkari	= 3 << 5

	Segbigmode	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	Udesccontents		= 3 << 1
	Udescrxonly		= 1 << 3
	Udesclimitinpages	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsstart	= 16
)

var (
	gdttable	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdttablelen	= 0
)

type Gdtentry_2 struct {
	limitLágur		uint16
	baseLágur		uint16
	basemid			uint8
	access			uint8
	limitHøgtandflags	uint8
	baseHøgt		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.access&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, access uint8, flags uint8) {
	e.limitHøgtandflags = uint8((limit >> 16) & 0x000F)
	e.limitHøgtandflags |= flags
	e.access = access
	e.basemid = uint8(base >> 16)
	e.baseHøgt = uint8(base >> 24)
	e.baseLágur = uint16(base & 0xFFFF)
	e.limitLágur = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Clear() {
	e.limitHøgtandflags = 0
	e.access = 0
	e.basemid = 0
	e.baseHøgt = 0
	e.baseLágur = 0
	e.limitLágur = 0

}

type Gdtdescriptor struct {
	GdtStødd	uint16
	GdtaddressLágur	uint16
	GdtaddressHøgt	uint16
}
type Brúkaridescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Limit		uint32
	Flags		uint8
}

func Settlssegment(index uint32, descriptor *Brúkaridescriptor, table []Gdtentry_2) bool {
	if index < Tlsstart || index > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Flags == Udescrxonly|Udescsegnotpresent {

		table[index].Clear()
		return true
	}

	flags := uint8(Seggranbyte)
	if descriptor.Flags&Udesclimitinpages != 0 {
		flags = Seggran4kpage
	}
	access := uint8(PrivBrúkari | Segnormal | Present)
	if descriptor.Flags&Udescrxonly != 0 {
		access |= Segexec
	} else {
		access |= Segw
	}
	if access&Segnormal != 0 {
		flags |= Segbigmode
	}

	table[index].Fill(descriptor.Baseaddress, descriptor.Limit, access, flags)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdtentry_2) {
	copy(gdttable[Tlsstart:], table[Tlsstart:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsstart:], table[Tlsstart:])
}
