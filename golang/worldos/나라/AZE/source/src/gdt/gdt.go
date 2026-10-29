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

	Segİstifadəçicode	uint32	= 0x23
	Segİstifadəçidata	uint32	= 0x2B
	Segİstifadəçigs		uint32	= 0x33
	Segtaskstate		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitAlçaq_2		uint16
	baseAlçaq_2		uint16
	basehigh_2		uint8
	növ			uint8
	bayraqlarlimithigh	uint8
	baseveryhigh		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, növ uint8, bayraqlar_2 uint8) {

	self_2.baseAlçaq_2 = uint16(base_2 & 0xFFFF)
	self_2.basehigh_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryhigh = uint8((base_2 >> 24) & 0xFF)

	self_2.limitAlçaq_2 = uint16(limit_2 & 0xFFFF)
	self_2.bayraqlarlimithigh = uint8((limit_2 >> 24) & 0x0F)
	self_2.bayraqlarlimithigh |= (bayraqlar_2 & 0xF0)

	self_2.növ = növ

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
	oldgdtaddress := uintptr(uint32(gdtdescriptor.GdtaddressAlçaq) |
		uint32(gdtdescriptor.Gdtaddresshigh)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtBöyüklük+1) / Sizeof(gdtentry))
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

	böyüklük_2 := (*uint16)(Pointer(&destination_3[0]))
	(*böyüklük_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MÇapEtxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32ÇapEt(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, növ uint8, bayraqlar_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, növ, bayraqlar_2)
}

const (
	Kcsindex	= 1
	Kdsindex	= 2
	Kgsindex	= 3

	Kcsselector	= Kcsindex * 8
	Kdsselector	= Kdsindex * 8
	Kgsselector	= Kgsindex * 8

	Seggranbyte	= 0 << 7
	Seggran4kSəhifə	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segsystem	= 0 << 4
	Segnormal	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	Privİstifadəçi	= 3 << 5

	SegbigMod	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescMəzmun		= 3 << 1
	Udescrxonly		= 1 << 3
	UdesclimitinSəhifələr	= 1 << 4
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
	limitAlçaq		uint16
	baseAlçaq		uint16
	basemid			uint8
	access			uint8
	limithighandBayraqlar	uint8
	basehigh		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.access&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, access uint8, bayraqlar uint8) {
	e.limithighandBayraqlar = uint8((limit >> 16) & 0x000F)
	e.limithighandBayraqlar |= bayraqlar
	e.access = access
	e.basemid = uint8(base >> 16)
	e.basehigh = uint8(base >> 24)
	e.baseAlçaq = uint16(base & 0xFFFF)
	e.limitAlçaq = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Təmizlə() {
	e.limithighandBayraqlar = 0
	e.access = 0
	e.basemid = 0
	e.basehigh = 0
	e.baseAlçaq = 0
	e.limitAlçaq = 0

}

type Gdtdescriptor struct {
	GdtBöyüklük	uint16
	GdtaddressAlçaq	uint16
	Gdtaddresshigh	uint16
}
type İstifadəçidescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Limit		uint32
	Bayraqlar	uint8
}

func Settlssegment(index uint32, descriptor *İstifadəçidescriptor, table []Gdtentry_2) bool {
	if index < Tlsstart || index > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Bayraqlar == Udescrxonly|Udescsegnotpresent {

		table[index].Təmizlə()
		return true
	}

	bayraqlar := uint8(Seggranbyte)
	if descriptor.Bayraqlar&UdesclimitinSəhifələr != 0 {
		bayraqlar = Seggran4kSəhifə
	}
	access := uint8(Privİstifadəçi | Segnormal | Present)
	if descriptor.Bayraqlar&Udescrxonly != 0 {
		access |= Segexec
	} else {
		access |= Segw
	}
	if access&Segnormal != 0 {
		bayraqlar |= SegbigMod
	}

	table[index].Fill(descriptor.Baseaddress, descriptor.Limit, access, bayraqlar)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdtentry_2) {
	copy(gdttable[Tlsstart:], table[Tlsstart:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsstart:], table[Tlsstart:])
}
