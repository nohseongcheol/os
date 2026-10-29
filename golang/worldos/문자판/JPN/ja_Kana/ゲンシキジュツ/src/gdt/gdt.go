/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "コンソール"

const (
	Segチュウカクcode	uint32	= 0x08
	Segチュウカクデータ	uint32	= 0x10
	Segチュウカクgs		uint32	= 0x18

	Segリヨウシャcode	uint32	= 0x23
	Segリヨウシャデータ	uint32	= 0x2B
	Segリヨウシャgs	uint32	= 0x33
	Segタスクジョウタイ	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	セイゲンヒクイ_2		uint16
	baseヒクイ_2	uint16
	baseタカイ_2	uint8
	カタ		uint8
	フラグセイゲンタカイ		uint8
	baseveryタカイ	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, セイゲン_2 uint32, カタ uint8, フラグ_2 uint8) {

	self_2.baseヒクイ_2 = uint16(base_2 & 0xFFFF)
	self_2.baseタカイ_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryタカイ = uint8((base_2 >> 24) & 0xFF)

	self_2.セイゲンヒクイ_2 = uint16(セイゲン_2 & 0xFFFF)
	self_2.フラグセイゲンタカイ = uint8((セイゲン_2 >> 24) & 0x0F)
	self_2.フラグセイゲンタカイ |= (フラグ_2 & 0xF0)

	self_2.カタ = カタ

}

type TShareddescriptortableデータ struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var データ_2 TShareddescriptortableデータ

type TShareddescriptortable struct {
}

func (self_2 *TShareddescriptortable) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddressヒクイ) |
		uint32(gdtdescriptor.Gdtaddressタカイ)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdtサイズ+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(データ_2.segmentdescriptor[:], oldgdt)

	データ_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	データ_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	データ_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	テンソウサキ_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&テンソウサキ_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&データ_2)))

	サイズ_2 := (*uint16)(Pointer(&テンソウサキ_3[0]))
	(*サイズ_2) = (uint16)((Sizeof(データ_2)))

	gdtfunc(uintptr(Pointer(&テンソウサキ_3)))

	terminal := new(Tコンソール)
	terminal.Mインサツxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32インサツ(uint32(uintptr(Pointer(&データ_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Sアリdescriptor(idx int, base_2 uint32, セイゲン_2 uint32, カタ uint8, フラグ_2 uint8) {
	データ_2.segmentdescriptor[idx].Init(base_2, セイゲン_2, カタ, フラグ_2)
}

const (
	Kcsモクジ	= 1
	Kdsモクジ	= 2
	Kgsモクジ	= 3

	Kcsselector	= Kcsモクジ * 8
	Kdsselector	= Kdsモクジ * 8
	Kgsselector	= Kgsモクジ * 8

	Seggranバイト	= 0 << 7
	Seggran4kページ	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segシステム	= 0 << 4
	Segフツウ	= 1 << 4

	Segnoexec	= 0 << 3
	Segジッコウ		= 1 << 3

	Privチュウカク	= 0 << 5
	Privリヨウシャ	= 3 << 5

	Segbigモード	= 1 << 6

	Pゲンザイ	= 1 << 7

	Udesc32seg		= 1 << 0
	Udescモクジ			= 3 << 1
	Udescrxセンヨウ		= 1 << 3
	Udescセイゲンジュシンpages		= 1 << 4
	Udescsegインストールサレテイマセンゲンザイ	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsカイシ		= 16
)

var (
	gdttable	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdttablelen	= 0
)

type Gdtentry_2 struct {
	セイゲンヒクイ		uint16
	baseヒクイ		uint16
	basemid		uint8
	アクセス		uint8
	セイゲンタカイトフラグ	uint8
	baseタカイ		uint8
}

func (e *Gdtentry_2) Isゲンザイ() bool {
	return e.アクセス&Pゲンザイ != 0
}

func (e *Gdtentry_2) Fill(base uint32, セイゲン uint32, アクセス uint8, フラグ uint8) {
	e.セイゲンタカイトフラグ = uint8((セイゲン >> 16) & 0x000F)
	e.セイゲンタカイトフラグ |= フラグ
	e.アクセス = アクセス
	e.basemid = uint8(base >> 16)
	e.baseタカイ = uint8(base >> 24)
	e.baseヒクイ = uint16(base & 0xFFFF)
	e.セイゲンヒクイ = uint16(セイゲン & 0x0000FFFF)
}

func (e *Gdtentry_2) Cクリア() {
	e.セイゲンタカイトフラグ = 0
	e.アクセス = 0
	e.basemid = 0
	e.baseタカイ = 0
	e.baseヒクイ = 0
	e.セイゲンヒクイ = 0

}

type Gdtdescriptor struct {
	Gdtサイズ		uint16
	Gdtaddressヒクイ	uint16
	Gdtaddressタカイ	uint16
}
type Uリヨウシャdescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Lセイゲン		uint32
	Fフラグ		uint8
}

func Sアリtlssegment(モクジ uint32, descriptor *Uリヨウシャdescriptor, table []Gdtentry_2) bool {
	if モクジ < Tlsカイシ || モクジ > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Fフラグ == Udescrxセンヨウ|Udescsegインストールサレテイマセンゲンザイ {

		table[モクジ].Cクリア()
		return true
	}

	フラグ := uint8(Seggranバイト)
	if descriptor.Fフラグ&Udescセイゲンジュシンpages != 0 {
		フラグ = Seggran4kページ
	}
	アクセス := uint8(Privリヨウシャ | Segフツウ | Pゲンザイ)
	if descriptor.Fフラグ&Udescrxセンヨウ != 0 {
		アクセス |= Segジッコウ
	} else {
		アクセス |= Segw
	}
	if アクセス&Segフツウ != 0 {
		フラグ |= Segbigモード
	}

	table[モクジ].Fill(descriptor.Baseaddress, descriptor.Lセイゲン, アクセス, フラグ)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdtentry_2) {
	copy(gdttable[Tlsカイシ:], table[Tlsカイシ:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(データ_2.segmentdescriptor[Tlsカイシ:], table[Tlsカイシ:])
}
