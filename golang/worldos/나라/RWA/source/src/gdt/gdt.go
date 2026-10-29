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

	SegUkoreshacode	uint32	= 0x23
	SegUkoreshadata	uint32	= 0x2B
	SegUkoreshags	uint32	= 0x33
	Segtaskstate	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitlow_2		uint16
	baselow_2		uint16
	basehigh_2		uint8
	ubwoko_2		uint8
	amabenderalimithigh	uint8
	baseveryhigh		uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, ubwoko_2 uint8, amabendera_2 uint8) {

	self_2.baselow_2 = uint16(base_2 & 0xFFFF)
	self_2.basehigh_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryhigh = uint8((base_2 >> 24) & 0xFF)

	self_2.limitlow_2 = uint16(limit_2 & 0xFFFF)
	self_2.amabenderalimithigh = uint8((limit_2 >> 24) & 0x0F)
	self_2.amabenderalimithigh |= (amabendera_2 & 0xF0)

	self_2.ubwoko_2 = ubwoko_2

}

type TShareddescriptorImbonerahamwedata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorImbonerahamwedata

type TShareddescriptorImbonerahamwe struct {
}

func (self_2 *TShareddescriptorImbonerahamwe) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddresslow) |
		uint32(gdtdescriptor.Gdtaddresshigh)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtIngano+1) / Sizeof(gdtentry))
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

	ingano_2 := (*uint16)(Pointer(&destination_3[0]))
	(*ingano_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.MGucapaxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Gucapa(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorImbonerahamwe) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, ubwoko_2 uint8, amabendera_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, ubwoko_2, amabendera_2)
}

const (
	KcsUmubarendanga	= 1
	KdsUmubarendanga	= 2
	KgsUmubarendanga	= 3

	Kcsselector	= KcsUmubarendanga * 8
	Kdsselector	= KdsUmubarendanga * 8
	Kgsselector	= KgsUmubarendanga * 8

	Seggranbyte	= 0 << 7
	Seggran4kIpaji	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segsystem	= 0 << 4
	SegBisanzwe	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	PrivUkoresha	= 3 << 5

	SegbigUbwoko	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescIbigize		= 3 << 1
	Udescrxonly		= 1 << 3
	UdesclimitImbereAmapaji	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsstart	= 16
)

var (
	gdtImbonerahamwe	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor		Gdtdescriptor
	gdtImbonerahamwelen	= 0
)

type Gdtentry_2 struct {
	limitlow		uint16
	baselow			uint16
	basemid			uint8
	access			uint8
	limithighandAmabendera	uint8
	basehigh		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.access&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, access uint8, amabendera uint8) {
	e.limithighandAmabendera = uint8((limit >> 16) & 0x000F)
	e.limithighandAmabendera |= amabendera
	e.access = access
	e.basemid = uint8(base >> 16)
	e.basehigh = uint8(base >> 24)
	e.baselow = uint16(base & 0xFFFF)
	e.limitlow = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Gusiba() {
	e.limithighandAmabendera = 0
	e.access = 0
	e.basemid = 0
	e.basehigh = 0
	e.baselow = 0
	e.limitlow = 0

}

type Gdtdescriptor struct {
	GdtIngano	uint16
	Gdtaddresslow	uint16
	Gdtaddresshigh	uint16
}
type Ukoreshadescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Limit		uint32
	Amabendera	uint8
}

func Settlssegment(umubarendanga uint32, descriptor *Ukoreshadescriptor, imbonerahamwe_2 []Gdtentry_2) bool {
	if umubarendanga < Tlsstart || umubarendanga > uint32(len(gdtImbonerahamwe)) {
		return false
	}

	if descriptor.Amabendera == Udescrxonly|Udescsegnotpresent {

		imbonerahamwe_2[umubarendanga].Gusiba()
		return true
	}

	amabendera := uint8(Seggranbyte)
	if descriptor.Amabendera&UdesclimitImbereAmapaji != 0 {
		amabendera = Seggran4kIpaji
	}
	access := uint8(PrivUkoresha | SegBisanzwe | Present)
	if descriptor.Amabendera&Udescrxonly != 0 {
		access |= Segexec
	} else {
		access |= Segw
	}
	if access&SegBisanzwe != 0 {
		amabendera |= SegbigUbwoko
	}

	imbonerahamwe_2[umubarendanga].Fill(descriptor.Baseaddress, descriptor.Limit, access, amabendera)
	flushtlsImbonerahamwe(imbonerahamwe_2)

	return true
}

func flushtlsImbonerahamwe(imbonerahamwe_2 []Gdtentry_2) {
	copy(gdtImbonerahamwe[Tlsstart:], imbonerahamwe_2[Tlsstart:])
}
func FlushtlsImbonerahamwe(imbonerahamwe_2 []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsstart:], imbonerahamwe_2[Tlsstart:])
}
