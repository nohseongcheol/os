/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ページカンリ

import unsafe "unsafe"
import . "ワリコミ"
import . "メモリカンリシャ"
import . "ハンヨウ"

type Pページディレクトリentry_2 uintptr

const (
	Pページゲンザイ		uint32	= 0x001
	Pページwritable	uint32	= 0x002
	Pページリヨウシャ		uint32	= 0x004
	Pページフレーム	uint32	= 0xFFFFF000
	Pページcow		uint32	= 0x200
)

func Sアリバイトataddress(x byte, address uint32)
func Sアリunsignedinteger8ataddress(x uint8, address uint32)
func Sアリunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func アリcr3(キオクページジョウイオモテ uint32)
func getcr3() uint32

type Pページカンリ struct {
	Tワリコミhandler
}
type Tcowフレームカンリシャ struct {
	mem		*Tメモリカンリシャ
	refs		[]uint16
	フレームカウント	uint32
}

var (
	Pページディレクトリentry	uintptr
	Pページtableentry	uint32
	pdelen		uint32
	virtlen		uint32
	cowフレームカンリシャ	Tcowフレームカンリシャ
)

func (self *Tcowフレームカンリシャ) Init(mem *Tメモリカンリシャ, フレームカウント uint32) bool {
	self.mem = mem
	self.フレームカウント = フレームカウント
	referenceバイト := フレームカウント * uint32(unsafe.Sizeof(uint16(0)))
	referenceポインタ := mem.Mキオクリョウイキヲカクホ(referenceバイト)
	if referenceポインタ == nil {
		self.refs = nil
		self.フレームカウント = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceポインタ)[:フレームカウント:フレームカウント]
	for i := uint32(0); i < フレームカウント; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcowフレームカンリシャ) Reference(フレーム uint32) uint16 {
	idx := フレーム >> 12
	if idx >= self.フレームカウント || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcowフレームカンリシャ) Increment(フレーム uint32) {
	idx := フレーム >> 12
	if idx >= self.フレームカウント || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcowフレームカンリシャ) Decrement(フレーム uint32) {
	idx := フレーム >> 12
	if idx >= self.フレームカウント || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Pページカンリ) Init(ページディレクトリentry uintptr, ページtableentry uint32, メモリカンリシャ *Tメモリカンリシャ) {

	Pページディレクトリentry = ページディレクトリentry
	Pページtableentry = ページtableentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowフレームカンリシャ.Init(メモリカンリシャ, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressポインタ, _ := メモリカンリシャ.Alignedmalloc(0x1000)
			if addressポインタ == nil {
				return
			}
			address := uint32(uintptr(addressポインタ))

			Sアリunsignedinteger32ataddress(address|0x87, uint32(ページディレクトリentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Sアリunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		ページディレクトリentry = ページディレクトリentry + 0x1000
	}

}
func (self *Pページカンリ) Sharedメモリregion() {

	ページディレクトリentry := Pページディレクトリentry
	kページディレクトリentry := Pページディレクトリentry

	for i := uint32(1); i <= virtlen; i++ {

		ページディレクトリentry = ページディレクトリentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Getアタイ(uint32(kページディレクトリentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sアリunsignedinteger32ataddress(v|0x87, uint32(ページディレクトリentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getアタイ(uint32(kページディレクトリentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sアリunsignedinteger32ataddress(v|0x87, uint32(ページディレクトリentry)+pde*4)

		}

	}
}
func (self *Pページカンリ) Pページショウガイ(カンリシャ *Tワリコミカンリシャ) {
	ワリコミhandler = トッテページカンリワリコミ

	var address uintptr
	address = uintptr(unsafe.Pointer(&ワリコミhandler))
	self.Tワリコミhandler.Init(0xE, uintptr(unsafe.Pointer(カンリシャ)), address)
}

var ワリコミhandler func(uint32) uint32

func トッテページカンリワリコミ(esp uint32) uint32 {
	if Rカイケツフクセイトキカキコミショウガイ() {
		return esp
	}
	return Hトッテfatalワリコミフレーム(esp, 0x0E)
}

func Cloneaddressスペースcow(テンソウモトページディレクトリ uint32) uint32 {
	if Aユウコウメモリカンリシャ == nil || テンソウモトページディレクトリ == 0 {
		return 0
	}
	テンソウサキポインタ, _ := Aユウコウメモリカンリシャ.Alignedmalloc(0x1000)
	if テンソウサキポインタ == nil {
		return 0
	}
	テンソウサキページディレクトリ := uint32(uintptr(テンソウサキポインタ))
	for i := uint32(0); i < 1024; i++ {
		Sアリunsignedinteger32ataddress(0, テンソウサキページディレクトリ+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		テンソウモトpdeaddress := テンソウモトページディレクトリ + pde*4
		テンソウモトpde := Getアタイ(テンソウモトpdeaddress)
		if (テンソウモトpde & Pページゲンザイ) == 0 {
			continue
		}
		if issharedpde(pde) {
			Sアリunsignedinteger32ataddress(テンソウモトpde, テンソウサキページディレクトリ+pde*4)
			continue
		}

		テンソウサキptポインタ, _ := Aユウコウメモリカンリシャ.Alignedmalloc(0x1000)
		if テンソウサキptポインタ == nil {
			continue
		}
		テンソウモトpt := テンソウモトpde & Pページフレーム
		テンソウサキpt := uint32(uintptr(テンソウサキptポインタ))
		Sアリunsignedinteger32ataddress((テンソウサキpt | (テンソウモトpde & 0xFFF)), テンソウサキページディレクトリ+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := テンソウモトpt + pte*4
			entry := Getアタイ(pteaddress)
			if (entry & Pページゲンザイ) != 0 {
				if (entry & Pページwritable) != 0 {
					entry = (entry &^ Pページwritable) | Pページcow
					Sアリunsignedinteger32ataddress(entry, pteaddress)
					cowフレームカンリシャ.Increment(entry & Pページフレーム)
				} else if (entry & Pページcow) != 0 {
					cowフレームカンリシャ.Increment(entry & Pページフレーム)
				}
			}
			Sアリunsignedinteger32ataddress(entry, テンソウサキpt+pte*4)
		}
	}
	サイドクミコミcr3()
	return テンソウサキページディレクトリ
}

func Rカイケツフクセイトキカキコミショウガイ() bool {
	if Aユウコウメモリカンリシャ == nil {
		return false
	}
	ショウガイaddress := getcr2()
	キオクページジョウイオモテ := getcr3()
	pdeaddress := キオクページジョウイオモテ + ((ショウガイaddress>>22)&0x3FF)*4
	pde := Getアタイ(pdeaddress)
	if (pde & Pページゲンザイ) == 0 {
		return false
	}
	pt := pde & Pページフレーム
	pteaddress := pt + ((ショウガイaddress>>12)&0x3FF)*4
	pte := Getアタイ(pteaddress)
	if (pte&Pページcow) == 0 || (pte&Pページゲンザイ) == 0 {
		return false
	}
	oldフレーム := pte & Pページフレーム
	if cowフレームカンリシャ.Reference(oldフレーム) <= 1 {
		Sアリunsignedinteger32ataddress((pte|Pページwritable)&^Pページcow, pteaddress)
		サイドクミコミcr3()
		return true
	}

	シンキポインタ, _ := Aユウコウメモリカンリシャ.Alignedmalloc(0x1000)
	if シンキポインタ == nil {
		return false
	}
	シンキフレーム := uint32(uintptr(シンキポインタ)) & Pページフレーム

	テンソウモト_2 := Getバイトカラポインタ(uintptr(ショウガイaddress&Pページフレーム), 0x1000, 0x1000)
	テンソウサキ_2 := Getバイトカラポインタ(uintptr(シンキフレーム), 0x1000, 0x1000)
	copy(テンソウサキ_2, テンソウモト_2)
	cowフレームカンリシャ.Decrement(oldフレーム)
	Sアリunsignedinteger32ataddress((シンキフレーム|(pte&0xFFF)|Pページwritable)&^Pページcow, pteaddress)
	サイドクミコミcr3()
	return true
}

func issharedpde(pde uint32) bool {
	if pde < 12 {
		return true
	}
	if pde >= 16 && pde < 20 {
		return true
	}
	return false
}

func サイドクミコミcr3() {
	cr3 := getcr3()
	アリcr3(cr3)
}

func Sアリバイトジュシンページディレクトリ(x byte, address uint32, キオクページジョウイオモテ uint32) {
	oldcr3 := getcr3()
	アリcr3(キオクページジョウイオモテ)
	Sアリバイトataddress(x, address)
	アリcr3(oldcr3)
}

func Sアリブロックジュシンページディレクトリ(テンソウモト_2 []byte, テンソウサキ_2 []byte, サイズ uint32, キオクページジョウイオモテ uint32) {
	if サイズ == 0 || キオクページジョウイオモテ == 0 {
		return
	}
	oldcr3 := getcr3()
	アリcr3(キオクページジョウイオモテ)
	makerangeプライベートwritableゲンザイノニチジ(キオクページジョウイオモテ, uint32(uintptr(unsafe.Pointer(&テンソウサキ_2[0]))), サイズ)

	for i := uint32(0); i < サイズ; i++ {
		テンソウサキ_2[i] = テンソウモト_2[i]
	}
	アリcr3(oldcr3)
}

func Zスウチノ0ブロックジュシンページディレクトリ(address uint32, サイズ uint32, キオクページジョウイオモテ uint32) {
	if サイズ == 0 || キオクページジョウイオモテ == 0 {
		return
	}
	oldcr3 := getcr3()
	アリcr3(キオクページジョウイオモテ)
	makerangeプライベートwritableゲンザイノニチジ(キオクページジョウイオモテ, address, サイズ)
	テンソウサキ_2 := Getバイトカラポインタ(uintptr(address), int(サイズ), int(サイズ))
	for i := uint32(0); i < サイズ; i++ {
		テンソウサキ_2[i] = 0
	}
	アリcr3(oldcr3)
}

func makeページプライベートwritableゲンザイノニチジ(キオクページジョウイオモテ uint32, カソウaddress uint32) bool {
	pde := Getアタイ(キオクページジョウイオモテ + ((カソウaddress>>22)&0x3FF)*4)
	if (pde & Pページゲンザイ) == 0 {
		return false
	}
	pteaddress := (pde & Pページフレーム) + ((カソウaddress>>12)&0x3FF)*4
	pte := Getアタイ(pteaddress)
	if (pte & Pページゲンザイ) == 0 {
		return false
	}
	if (pte & Pページcow) == 0 {
		return (pte & Pページwritable) != 0
	}
	if Aユウコウメモリカンリシャ == nil {
		return false
	}
	シンキポインタ, _ := Aユウコウメモリカンリシャ.Alignedmalloc(0x1000)
	if シンキポインタ == nil {
		return false
	}
	シンキフレーム := uint32(uintptr(シンキポインタ)) & Pページフレーム
	テンソウモト_2 := Getバイトカラポインタ(uintptr(カソウaddress&Pページフレーム), 0x1000, 0x1000)
	テンソウサキ_2 := Getバイトカラポインタ(uintptr(シンキフレーム), 0x1000, 0x1000)
	copy(テンソウサキ_2, テンソウモト_2)
	cowフレームカンリシャ.Decrement(pte & Pページフレーム)
	Sアリunsignedinteger32ataddress((シンキフレーム|(pte&0xFFF)|Pページwritable)&^Pページcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	サイドクミコミcr3()
	return true
}

func makerangeプライベートwritableゲンザイノニチジ(キオクページジョウイオモテ uint32, address uint32, サイズ uint32) bool {
	if サイズ == 0 {
		return true
	}
	サイゴ := address + サイズ - 1
	if サイゴ < address {
		return false
	}
	for ページ := address & Pページフレーム; ; ページ += 0x1000 {
		if !makeページプライベートwritableゲンザイノニチジ(キオクページジョウイオモテ, ページ) {
			return false
		}
		if ページ == (サイゴ & Pページフレーム) {
			break
		}
	}
	return true
}

func Makerangeプライベートwritable(キオクページジョウイオモテ uint32, address uint32, サイズ uint32) bool {
	if キオクページジョウイオモテ == 0 {
		return false
	}
	oldcr3 := getcr3()
	アリcr3(キオクページジョウイオモテ)
	ok := makerangeプライベートwritableゲンザイノニチジ(キオクページジョウイオモテ, address, サイズ)
	アリcr3(oldcr3)
	return ok
}

func Sアリunsignedinteger32ジュシンページディレクトリ(x uint32, address uint32, キオクページジョウイオモテ uint32) {
	if キオクページジョウイオモテ == 0 {
		return
	}
	oldcr3 := getcr3()
	アリcr3(キオクページジョウイオモテ)
	Sアリunsignedinteger32ataddress(x, address)
	アリcr3(oldcr3)
}

func Getアタイ(address uint32) uint32 {
	var orgアタイ uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgアタイ
}
func Getアタイジュシンページディレクトリ(address uint32, キオクページジョウイオモテ uint32) uint32 {
	if キオクページジョウイオモテ == 0 {
		return 0
	}
	oldcr3 := getcr3()
	アリcr3(キオクページジョウイオモテ)
	v := Getアタイ(address)
	アリcr3(oldcr3)
	return v
}

var v uint32 = 0

func Cフクセイページフレームブロック(xページディレクトリ uint32, yページディレクトリ uint32, vaddress uint32) {
	if xページディレクトリ == 0 || yページディレクトリ == 0 {
		return
	}
	oldcr3 := getcr3()
	アリcr3(xページディレクトリ)
	v = Getアタイ(vaddress)
	Sアリunsignedinteger32ジュシンページディレクトリ(v, vaddress, yページディレクトリ)

	アリcr3(oldcr3)
}
