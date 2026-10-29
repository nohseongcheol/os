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

	SegKorisnikcode	uint32	= 0x23
	SegKorisnikdata	uint32	= 0x2B
	SegKorisnikgs	uint32	= 0x33
	Segtaskstate	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitlow_2		uint16
	baselow_2		uint16
	basehigh_2		uint8
	tip			uint8
	zastavelimithigh	uint8
	baseveryhigh		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, tip uint8, zastave_2 uint8) {

	self_2.baselow_2 = uint16(base_2 & 0xFFFF)
	self_2.basehigh_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryhigh = uint8((base_2 >> 24) & 0xFF)

	self_2.limitlow_2 = uint16(limit_2 & 0xFFFF)
	self_2.zastavelimithigh = uint8((limit_2 >> 24) & 0x0F)
	self_2.zastavelimithigh |= (zastave_2 & 0xF0)

	self_2.tip = tip

}

type TShareddescriptortabledata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptortabledata

type TShareddescriptortable struct {
}

func (self_2 *TShareddescriptortable) Init() {

	var gdtunos TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddresslow) |
		uint32(gdtdescriptor.Gdtaddresshigh)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtVeličina+1) / Sizeof(gdtunos))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	odredište_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&odredište_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	veličina_2 := (*uint16)(Pointer(&odredište_3[0]))
	(*veličina_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&odredište_3)))

	terminal := new(TConsole)
	terminal.MŠtampajxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Skupdescriptor(idx int, base_2 uint32, limit_2 uint32, tip uint8, zastave_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, tip, zastave_2)
}

const (
	KcsIndeks	= 1
	KdsIndeks	= 2
	KgsIndeks	= 3

	Kcsselector	= KcsIndeks * 8
	Kdsselector	= KdsIndeks * 8
	Kgsselector	= KgsIndeks * 8

	Seggranbyte		= 0 << 7
	Seggran4kStranica	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegSistem	= 0 << 4
	Segobičan	= 1 << 4

	Segnoexec	= 0 << 3
	Segizvršna	= 1 << 3

	Privkernel	= 0 << 5
	PrivKorisnik	= 3 << 5

	SegbigRežim	= 1 << 6

	Present	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescSadržaj			= 3 << 1
	Udescrxonly			= 1 << 3
	UdesclimitPrimljenopages	= 1 << 4
	Udescsegnotpresent		= 1 << 5
	Udescusable			= 1 << 6

	Gdtunos		= 256
	Tlsstart	= 16
)

var (
	gdttable	= [Gdtunos]Gdtunos_2{}
	gdtdescriptor	Gdtdescriptor
	gdttablelen	= 0
)

type Gdtunos_2 struct {
	limitlow		uint16
	baselow			uint16
	basemid			uint8
	access			uint8
	limithighandZastave	uint8
	basehigh		uint8
}

func (e *Gdtunos_2) Ispresent() bool {
	return e.access&Present != 0
}

func (e *Gdtunos_2) Fill(base uint32, limit uint32, access uint8, zastave uint8) {
	e.limithighandZastave = uint8((limit >> 16) & 0x000F)
	e.limithighandZastave |= zastave
	e.access = access
	e.basemid = uint8(base >> 16)
	e.basehigh = uint8(base >> 24)
	e.baselow = uint16(base & 0xFFFF)
	e.limitlow = uint16(limit & 0x0000FFFF)
}

func (e *Gdtunos_2) Obriši() {
	e.limithighandZastave = 0
	e.access = 0
	e.basemid = 0
	e.basehigh = 0
	e.baselow = 0
	e.limitlow = 0

}

type Gdtdescriptor struct {
	GdtVeličina	uint16
	Gdtaddresslow	uint16
	Gdtaddresshigh	uint16
}
type Korisnikdescriptor struct {
	UnosBroj	uint32
	Baseaddress	uint32
	Limit		uint32
	Zastave		uint8
}

func Skuptlssegment(indeks uint32, descriptor *Korisnikdescriptor, table []Gdtunos_2) bool {
	if indeks < Tlsstart || indeks > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Zastave == Udescrxonly|Udescsegnotpresent {

		table[indeks].Obriši()
		return true
	}

	zastave := uint8(Seggranbyte)
	if descriptor.Zastave&UdesclimitPrimljenopages != 0 {
		zastave = Seggran4kStranica
	}
	access := uint8(PrivKorisnik | Segobičan | Present)
	if descriptor.Zastave&Udescrxonly != 0 {
		access |= Segizvršna
	} else {
		access |= Segw
	}
	if access&Segobičan != 0 {
		zastave |= SegbigRežim
	}

	table[indeks].Fill(descriptor.Baseaddress, descriptor.Limit, access, zastave)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdtunos_2) {
	copy(gdttable[Tlsstart:], table[Tlsstart:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsstart:], table[Tlsstart:])
}
