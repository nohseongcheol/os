package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegUllançycode	uint32	= 0x23
	SegUllançydata	uint32	= 0x2B
	SegUllançygs	uint32	= 0x33
	Segtaskstate	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitlow_2	uint16
	baselow_2	uint16
	basehigh_2	uint8
	hil		uint8
	flagslimithigh	uint8
	baseveryhigh	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, hil uint8, flags_2 uint8) {

	self_2.baselow_2 = uint16(base_2 & 0xFFFF)
	self_2.basehigh_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryhigh = uint8((base_2 >> 24) & 0xFF)

	self_2.limitlow_2 = uint16(limit_2 & 0xFFFF)
	self_2.flagslimithigh = uint8((limit_2 >> 24) & 0x0F)
	self_2.flagslimithigh |= (flags_2 & 0xF0)

	self_2.hil = hil

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
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddresslow) |
		uint32(gdtdescriptor.Gdtaddresshigh)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtUlulyk+1) / Sizeof(gdtentry))
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

	ululyk_2 := (*uint16)(Pointer(&destination_3[0]))
	(*ululyk_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MÇapxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Çap(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, hil uint8, flags_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, hil, flags_2)
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
	PrivUllançy	= 3 << 5

	Segbigmode	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescMazmunlar		= 3 << 1
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
	limitlow		uint16
	baselow			uint16
	basemid			uint8
	access			uint8
	limithighandflags	uint8
	basehigh		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.access&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, access uint8, flags uint8) {
	e.limithighandflags = uint8((limit >> 16) & 0x000F)
	e.limithighandflags |= flags
	e.access = access
	e.basemid = uint8(base >> 16)
	e.basehigh = uint8(base >> 24)
	e.baselow = uint16(base & 0xFFFF)
	e.limitlow = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Poz() {
	e.limithighandflags = 0
	e.access = 0
	e.basemid = 0
	e.basehigh = 0
	e.baselow = 0
	e.limitlow = 0

}

type Gdtdescriptor struct {
	GdtUlulyk	uint16
	Gdtaddresslow	uint16
	Gdtaddresshigh	uint16
}
type Ullançydescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Limit		uint32
	Flags		uint8
}

func Settlssegment(index uint32, descriptor *Ullançydescriptor, table []Gdtentry_2) bool {
	if index < Tlsstart || index > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Flags == Udescrxonly|Udescsegnotpresent {

		table[index].Poz()
		return true
	}

	flags := uint8(Seggranbyte)
	if descriptor.Flags&Udesclimitinpages != 0 {
		flags = Seggran4kpage
	}
	access := uint8(PrivUllançy | Segnormal | Present)
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
