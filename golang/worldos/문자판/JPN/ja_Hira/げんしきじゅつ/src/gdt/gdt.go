/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "こんそーる"

const (
	Segちゅうかくcode	uint32	= 0x08
	Segちゅうかくでーた	uint32	= 0x10
	Segちゅうかくgs		uint32	= 0x18

	Segりようしゃcode	uint32	= 0x23
	Segりようしゃでーた	uint32	= 0x2B
	Segりようしゃgs	uint32	= 0x33
	Segたすくじょうたい	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	せいげんひくい_2		uint16
	baseひくい_2	uint16
	baseたかい_2	uint8
	かた		uint8
	ふらぐせいげんたかい		uint8
	baseveryたかい	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, せいげん_2 uint32, かた uint8, ふらぐ_2 uint8) {

	self_2.baseひくい_2 = uint16(base_2 & 0xFFFF)
	self_2.baseたかい_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryたかい = uint8((base_2 >> 24) & 0xFF)

	self_2.せいげんひくい_2 = uint16(せいげん_2 & 0xFFFF)
	self_2.ふらぐせいげんたかい = uint8((せいげん_2 >> 24) & 0x0F)
	self_2.ふらぐせいげんたかい |= (ふらぐ_2 & 0xF0)

	self_2.かた = かた

}

type TShareddescriptortableでーた struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var でーた_2 TShareddescriptortableでーた

type TShareddescriptortable struct {
}

func (self_2 *TShareddescriptortable) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddressひくい) |
		uint32(gdtdescriptor.Gdtaddressたかい)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdtさいず+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(でーた_2.segmentdescriptor[:], oldgdt)

	でーた_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	でーた_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	でーた_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	てんそうさき_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&てんそうさき_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&でーた_2)))

	さいず_2 := (*uint16)(Pointer(&てんそうさき_3[0]))
	(*さいず_2) = (uint16)((Sizeof(でーた_2)))

	gdtfunc(uintptr(Pointer(&てんそうさき_3)))

	terminal := new(Tこんそーる)
	terminal.Mいんさつxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32いんさつ(uint32(uintptr(Pointer(&でーた_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Sありdescriptor(idx int, base_2 uint32, せいげん_2 uint32, かた uint8, ふらぐ_2 uint8) {
	でーた_2.segmentdescriptor[idx].Init(base_2, せいげん_2, かた, ふらぐ_2)
}

const (
	Kcsもくじ	= 1
	Kdsもくじ	= 2
	Kgsもくじ	= 3

	Kcsselector	= Kcsもくじ * 8
	Kdsselector	= Kdsもくじ * 8
	Kgsselector	= Kgsもくじ * 8

	Seggranばいと	= 0 << 7
	Seggran4kぺーじ	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segしすてむ	= 0 << 4
	Segふつう	= 1 << 4

	Segnoexec	= 0 << 3
	Segじっこう		= 1 << 3

	Privちゅうかく	= 0 << 5
	Privりようしゃ	= 3 << 5

	Segbigもーど	= 1 << 6

	Pげんざい	= 1 << 7

	Udesc32seg		= 1 << 0
	Udescもくじ			= 3 << 1
	Udescrxせんよう		= 1 << 3
	Udescせいげんじゅしんpages		= 1 << 4
	Udescsegいんすとーるされていませんげんざい	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsかいし		= 16
)

var (
	gdttable	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdttablelen	= 0
)

type Gdtentry_2 struct {
	せいげんひくい		uint16
	baseひくい		uint16
	basemid		uint8
	あくせす		uint8
	せいげんたかいとふらぐ	uint8
	baseたかい		uint8
}

func (e *Gdtentry_2) Isげんざい() bool {
	return e.あくせす&Pげんざい != 0
}

func (e *Gdtentry_2) Fill(base uint32, せいげん uint32, あくせす uint8, ふらぐ uint8) {
	e.せいげんたかいとふらぐ = uint8((せいげん >> 16) & 0x000F)
	e.せいげんたかいとふらぐ |= ふらぐ
	e.あくせす = あくせす
	e.basemid = uint8(base >> 16)
	e.baseたかい = uint8(base >> 24)
	e.baseひくい = uint16(base & 0xFFFF)
	e.せいげんひくい = uint16(せいげん & 0x0000FFFF)
}

func (e *Gdtentry_2) Cくりあ() {
	e.せいげんたかいとふらぐ = 0
	e.あくせす = 0
	e.basemid = 0
	e.baseたかい = 0
	e.baseひくい = 0
	e.せいげんひくい = 0

}

type Gdtdescriptor struct {
	Gdtさいず		uint16
	Gdtaddressひくい	uint16
	Gdtaddressたかい	uint16
}
type Uりようしゃdescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Lせいげん		uint32
	Fふらぐ		uint8
}

func Sありtlssegment(もくじ uint32, descriptor *Uりようしゃdescriptor, table []Gdtentry_2) bool {
	if もくじ < Tlsかいし || もくじ > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Fふらぐ == Udescrxせんよう|Udescsegいんすとーるされていませんげんざい {

		table[もくじ].Cくりあ()
		return true
	}

	ふらぐ := uint8(Seggranばいと)
	if descriptor.Fふらぐ&Udescせいげんじゅしんpages != 0 {
		ふらぐ = Seggran4kぺーじ
	}
	あくせす := uint8(Privりようしゃ | Segふつう | Pげんざい)
	if descriptor.Fふらぐ&Udescrxせんよう != 0 {
		あくせす |= Segじっこう
	} else {
		あくせす |= Segw
	}
	if あくせす&Segふつう != 0 {
		ふらぐ |= Segbigもーど
	}

	table[もくじ].Fill(descriptor.Baseaddress, descriptor.Lせいげん, あくせす, ふらぐ)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdtentry_2) {
	copy(gdttable[Tlsかいし:], table[Tlsかいし:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(でーた_2.segmentdescriptor[Tlsかいし:], table[Tlsかいし:])
}
