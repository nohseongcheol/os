/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "コンソール"

const (
	Seg中核code	uint32	= 0x08
	Seg中核データ	uint32	= 0x10
	Seg中核gs		uint32	= 0x18

	Seg利用者code	uint32	= 0x23
	Seg利用者データ	uint32	= 0x2B
	Seg利用者gs	uint32	= 0x33
	Segタスク状態	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	制限低い_2		uint16
	base低い_2	uint16
	base高い_2	uint8
	型		uint8
	フラグ制限高い		uint8
	basevery高い	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, 制限_2 uint32, 型 uint8, フラグ_2 uint8) {

	self_2.base低い_2 = uint16(base_2 & 0xFFFF)
	self_2.base高い_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.basevery高い = uint8((base_2 >> 24) & 0xFF)

	self_2.制限低い_2 = uint16(制限_2 & 0xFFFF)
	self_2.フラグ制限高い = uint8((制限_2 >> 24) & 0x0F)
	self_2.フラグ制限高い |= (フラグ_2 & 0xF0)

	self_2.型 = 型

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
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddress低い) |
		uint32(gdtdescriptor.Gdtaddress高い)<<16)
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

	転送先_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&転送先_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&データ_2)))

	サイズ_2 := (*uint16)(Pointer(&転送先_3[0]))
	(*サイズ_2) = (uint16)((Sizeof(データ_2)))

	gdtfunc(uintptr(Pointer(&転送先_3)))

	terminal := new(Tコンソール)
	terminal.M印刷xy("gdt:", 1, 4)
	terminal.MUnsignedinteger32印刷(uint32(uintptr(Pointer(&データ_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Sありdescriptor(idx int, base_2 uint32, 制限_2 uint32, 型 uint8, フラグ_2 uint8) {
	データ_2.segmentdescriptor[idx].Init(base_2, 制限_2, 型, フラグ_2)
}

const (
	Kcs目次	= 1
	Kds目次	= 2
	Kgs目次	= 3

	Kcsselector	= Kcs目次 * 8
	Kdsselector	= Kds目次 * 8
	Kgsselector	= Kgs目次 * 8

	Seggranバイト	= 0 << 7
	Seggran4kページ	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segシステム	= 0 << 4
	Seg普通	= 1 << 4

	Segnoexec	= 0 << 3
	Seg実行		= 1 << 3

	Priv中核	= 0 << 5
	Priv利用者	= 3 << 5

	Segbigモード	= 1 << 6

	P現在	= 1 << 7

	Udesc32seg		= 1 << 0
	Udesc目次			= 3 << 1
	Udescrx専用		= 1 << 3
	Udesc制限受信pages		= 1 << 4
	Udescsegインストールされていません現在	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tls開始		= 16
)

var (
	gdttable	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdttablelen	= 0
)

type Gdtentry_2 struct {
	制限低い		uint16
	base低い		uint16
	basemid		uint8
	アクセス		uint8
	制限高いとフラグ	uint8
	base高い		uint8
}

func (e *Gdtentry_2) Is現在() bool {
	return e.アクセス&P現在 != 0
}

func (e *Gdtentry_2) Fill(base uint32, 制限 uint32, アクセス uint8, フラグ uint8) {
	e.制限高いとフラグ = uint8((制限 >> 16) & 0x000F)
	e.制限高いとフラグ |= フラグ
	e.アクセス = アクセス
	e.basemid = uint8(base >> 16)
	e.base高い = uint8(base >> 24)
	e.base低い = uint16(base & 0xFFFF)
	e.制限低い = uint16(制限 & 0x0000FFFF)
}

func (e *Gdtentry_2) Cクリア() {
	e.制限高いとフラグ = 0
	e.アクセス = 0
	e.basemid = 0
	e.base高い = 0
	e.base低い = 0
	e.制限低い = 0

}

type Gdtdescriptor struct {
	Gdtサイズ		uint16
	Gdtaddress低い	uint16
	Gdtaddress高い	uint16
}
type U利用者descriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	L制限		uint32
	Fフラグ		uint8
}

func Sありtlssegment(目次 uint32, descriptor *U利用者descriptor, table []Gdtentry_2) bool {
	if 目次 < Tls開始 || 目次 > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Fフラグ == Udescrx専用|Udescsegインストールされていません現在 {

		table[目次].Cクリア()
		return true
	}

	フラグ := uint8(Seggranバイト)
	if descriptor.Fフラグ&Udesc制限受信pages != 0 {
		フラグ = Seggran4kページ
	}
	アクセス := uint8(Priv利用者 | Seg普通 | P現在)
	if descriptor.Fフラグ&Udescrx専用 != 0 {
		アクセス |= Seg実行
	} else {
		アクセス |= Segw
	}
	if アクセス&Seg普通 != 0 {
		フラグ |= Segbigモード
	}

	table[目次].Fill(descriptor.Baseaddress, descriptor.L制限, アクセス, フラグ)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdtentry_2) {
	copy(gdttable[Tls開始:], table[Tls開始:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(データ_2.segmentdescriptor[Tls開始:], table[Tls開始:])
}
