package ページ管理

import unsafe "unsafe"
import . "割込み"
import . "メモリ管理者"
import . "汎用"

type Pページディレクトリentry_2 uintptr

const (
	Pページ現在		uint32	= 0x001
	Pページwritable	uint32	= 0x002
	Pページ利用者		uint32	= 0x004
	Pページフレーム	uint32	= 0xFFFFF000
	Pページcow		uint32	= 0x200
)

func Sありバイトataddress(x byte, address uint32)
func Sありunsignedinteger8ataddress(x uint8, address uint32)
func Sありunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func ありcr3(記憶頁上位表 uint32)
func getcr3() uint32

type Pページ管理 struct {
	T割込みhandler
}
type Tcowフレーム管理者 struct {
	mem		*Tメモリ管理者
	refs		[]uint16
	フレームカウント	uint32
}

var (
	Pページディレクトリentry	uintptr
	Pページtableentry	uint32
	pdelen		uint32
	virtlen		uint32
	cowフレーム管理者	Tcowフレーム管理者
)

func (self *Tcowフレーム管理者) Init(mem *Tメモリ管理者, フレームカウント uint32) bool {
	self.mem = mem
	self.フレームカウント = フレームカウント
	referenceバイト := フレームカウント * uint32(unsafe.Sizeof(uint16(0)))
	referenceポインタ := mem.M記憶領域を確保(referenceバイト)
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

func (self *Tcowフレーム管理者) Reference(フレーム uint32) uint16 {
	idx := フレーム >> 12
	if idx >= self.フレームカウント || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcowフレーム管理者) Increment(フレーム uint32) {
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

func (self *Tcowフレーム管理者) Decrement(フレーム uint32) {
	idx := フレーム >> 12
	if idx >= self.フレームカウント || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Pページ管理) Init(ページディレクトリentry uintptr, ページtableentry uint32, メモリ管理者 *Tメモリ管理者) {

	Pページディレクトリentry = ページディレクトリentry
	Pページtableentry = ページtableentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowフレーム管理者.Init(メモリ管理者, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressポインタ, _ := メモリ管理者.Alignedmalloc(0x1000)
			if addressポインタ == nil {
				return
			}
			address := uint32(uintptr(addressポインタ))

			Sありunsignedinteger32ataddress(address|0x87, uint32(ページディレクトリentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Sありunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		ページディレクトリentry = ページディレクトリentry + 0x1000
	}

}
func (self *Pページ管理) Sharedメモリregion() {

	ページディレクトリentry := Pページディレクトリentry
	kページディレクトリentry := Pページディレクトリentry

	for i := uint32(1); i <= virtlen; i++ {

		ページディレクトリentry = ページディレクトリentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Get値(uint32(kページディレクトリentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sありunsignedinteger32ataddress(v|0x87, uint32(ページディレクトリentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Get値(uint32(kページディレクトリentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sありunsignedinteger32ataddress(v|0x87, uint32(ページディレクトリentry)+pde*4)

		}

	}
}
func (self *Pページ管理) Pページ障害(管理者 *T割込み管理者) {
	割込みhandler = 取っ手ページ管理割込み

	var address uintptr
	address = uintptr(unsafe.Pointer(&割込みhandler))
	self.T割込みhandler.Init(0xE, uintptr(unsafe.Pointer(管理者)), address)
}

var 割込みhandler func(uint32) uint32

func 取っ手ページ管理割込み(esp uint32) uint32 {
	if R解決複製時書込み障害() {
		return esp
	}
	return H取っ手fatal割込みフレーム(esp, 0x0E)
}

func Cloneaddressスペースcow(転送元ページディレクトリ uint32) uint32 {
	if A有効メモリ管理者 == nil || 転送元ページディレクトリ == 0 {
		return 0
	}
	転送先ポインタ, _ := A有効メモリ管理者.Alignedmalloc(0x1000)
	if 転送先ポインタ == nil {
		return 0
	}
	転送先ページディレクトリ := uint32(uintptr(転送先ポインタ))
	for i := uint32(0); i < 1024; i++ {
		Sありunsignedinteger32ataddress(0, 転送先ページディレクトリ+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		転送元pdeaddress := 転送元ページディレクトリ + pde*4
		転送元pde := Get値(転送元pdeaddress)
		if (転送元pde & Pページ現在) == 0 {
			continue
		}
		if issharedpde(pde) {
			Sありunsignedinteger32ataddress(転送元pde, 転送先ページディレクトリ+pde*4)
			continue
		}

		転送先ptポインタ, _ := A有効メモリ管理者.Alignedmalloc(0x1000)
		if 転送先ptポインタ == nil {
			continue
		}
		転送元pt := 転送元pde & Pページフレーム
		転送先pt := uint32(uintptr(転送先ptポインタ))
		Sありunsignedinteger32ataddress((転送先pt | (転送元pde & 0xFFF)), 転送先ページディレクトリ+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := 転送元pt + pte*4
			entry := Get値(pteaddress)
			if (entry & Pページ現在) != 0 {
				if (entry & Pページwritable) != 0 {
					entry = (entry &^ Pページwritable) | Pページcow
					Sありunsignedinteger32ataddress(entry, pteaddress)
					cowフレーム管理者.Increment(entry & Pページフレーム)
				} else if (entry & Pページcow) != 0 {
					cowフレーム管理者.Increment(entry & Pページフレーム)
				}
			}
			Sありunsignedinteger32ataddress(entry, 転送先pt+pte*4)
		}
	}
	再読み込みcr3()
	return 転送先ページディレクトリ
}

func R解決複製時書込み障害() bool {
	if A有効メモリ管理者 == nil {
		return false
	}
	障害address := getcr2()
	記憶頁上位表 := getcr3()
	pdeaddress := 記憶頁上位表 + ((障害address>>22)&0x3FF)*4
	pde := Get値(pdeaddress)
	if (pde & Pページ現在) == 0 {
		return false
	}
	pt := pde & Pページフレーム
	pteaddress := pt + ((障害address>>12)&0x3FF)*4
	pte := Get値(pteaddress)
	if (pte&Pページcow) == 0 || (pte&Pページ現在) == 0 {
		return false
	}
	oldフレーム := pte & Pページフレーム
	if cowフレーム管理者.Reference(oldフレーム) <= 1 {
		Sありunsignedinteger32ataddress((pte|Pページwritable)&^Pページcow, pteaddress)
		再読み込みcr3()
		return true
	}

	新規ポインタ, _ := A有効メモリ管理者.Alignedmalloc(0x1000)
	if 新規ポインタ == nil {
		return false
	}
	新規フレーム := uint32(uintptr(新規ポインタ)) & Pページフレーム

	転送元_2 := Getバイトからポインタ(uintptr(障害address&Pページフレーム), 0x1000, 0x1000)
	転送先_2 := Getバイトからポインタ(uintptr(新規フレーム), 0x1000, 0x1000)
	copy(転送先_2, 転送元_2)
	cowフレーム管理者.Decrement(oldフレーム)
	Sありunsignedinteger32ataddress((新規フレーム|(pte&0xFFF)|Pページwritable)&^Pページcow, pteaddress)
	再読み込みcr3()
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

func 再読み込みcr3() {
	cr3 := getcr3()
	ありcr3(cr3)
}

func Sありバイト受信ページディレクトリ(x byte, address uint32, 記憶頁上位表 uint32) {
	oldcr3 := getcr3()
	ありcr3(記憶頁上位表)
	Sありバイトataddress(x, address)
	ありcr3(oldcr3)
}

func Sありブロック受信ページディレクトリ(転送元_2 []byte, 転送先_2 []byte, サイズ uint32, 記憶頁上位表 uint32) {
	if サイズ == 0 || 記憶頁上位表 == 0 {
		return
	}
	oldcr3 := getcr3()
	ありcr3(記憶頁上位表)
	makerangeプライベートwritable現在の日時(記憶頁上位表, uint32(uintptr(unsafe.Pointer(&転送先_2[0]))), サイズ)

	for i := uint32(0); i < サイズ; i++ {
		転送先_2[i] = 転送元_2[i]
	}
	ありcr3(oldcr3)
}

func Z数値の0ブロック受信ページディレクトリ(address uint32, サイズ uint32, 記憶頁上位表 uint32) {
	if サイズ == 0 || 記憶頁上位表 == 0 {
		return
	}
	oldcr3 := getcr3()
	ありcr3(記憶頁上位表)
	makerangeプライベートwritable現在の日時(記憶頁上位表, address, サイズ)
	転送先_2 := Getバイトからポインタ(uintptr(address), int(サイズ), int(サイズ))
	for i := uint32(0); i < サイズ; i++ {
		転送先_2[i] = 0
	}
	ありcr3(oldcr3)
}

func makeページプライベートwritable現在の日時(記憶頁上位表 uint32, 仮想address uint32) bool {
	pde := Get値(記憶頁上位表 + ((仮想address>>22)&0x3FF)*4)
	if (pde & Pページ現在) == 0 {
		return false
	}
	pteaddress := (pde & Pページフレーム) + ((仮想address>>12)&0x3FF)*4
	pte := Get値(pteaddress)
	if (pte & Pページ現在) == 0 {
		return false
	}
	if (pte & Pページcow) == 0 {
		return (pte & Pページwritable) != 0
	}
	if A有効メモリ管理者 == nil {
		return false
	}
	新規ポインタ, _ := A有効メモリ管理者.Alignedmalloc(0x1000)
	if 新規ポインタ == nil {
		return false
	}
	新規フレーム := uint32(uintptr(新規ポインタ)) & Pページフレーム
	転送元_2 := Getバイトからポインタ(uintptr(仮想address&Pページフレーム), 0x1000, 0x1000)
	転送先_2 := Getバイトからポインタ(uintptr(新規フレーム), 0x1000, 0x1000)
	copy(転送先_2, 転送元_2)
	cowフレーム管理者.Decrement(pte & Pページフレーム)
	Sありunsignedinteger32ataddress((新規フレーム|(pte&0xFFF)|Pページwritable)&^Pページcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	再読み込みcr3()
	return true
}

func makerangeプライベートwritable現在の日時(記憶頁上位表 uint32, address uint32, サイズ uint32) bool {
	if サイズ == 0 {
		return true
	}
	最後 := address + サイズ - 1
	if 最後 < address {
		return false
	}
	for ページ := address & Pページフレーム; ; ページ += 0x1000 {
		if !makeページプライベートwritable現在の日時(記憶頁上位表, ページ) {
			return false
		}
		if ページ == (最後 & Pページフレーム) {
			break
		}
	}
	return true
}

func Makerangeプライベートwritable(記憶頁上位表 uint32, address uint32, サイズ uint32) bool {
	if 記憶頁上位表 == 0 {
		return false
	}
	oldcr3 := getcr3()
	ありcr3(記憶頁上位表)
	ok := makerangeプライベートwritable現在の日時(記憶頁上位表, address, サイズ)
	ありcr3(oldcr3)
	return ok
}

func Sありunsignedinteger32受信ページディレクトリ(x uint32, address uint32, 記憶頁上位表 uint32) {
	if 記憶頁上位表 == 0 {
		return
	}
	oldcr3 := getcr3()
	ありcr3(記憶頁上位表)
	Sありunsignedinteger32ataddress(x, address)
	ありcr3(oldcr3)
}

func Get値(address uint32) uint32 {
	var org値 uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return org値
}
func Get値受信ページディレクトリ(address uint32, 記憶頁上位表 uint32) uint32 {
	if 記憶頁上位表 == 0 {
		return 0
	}
	oldcr3 := getcr3()
	ありcr3(記憶頁上位表)
	v := Get値(address)
	ありcr3(oldcr3)
	return v
}

var v uint32 = 0

func C複製ページフレームブロック(xページディレクトリ uint32, yページディレクトリ uint32, vaddress uint32) {
	if xページディレクトリ == 0 || yページディレクトリ == 0 {
		return
	}
	oldcr3 := getcr3()
	ありcr3(xページディレクトリ)
	v = Get値(vaddress)
	Sありunsignedinteger32受信ページディレクトリ(v, vaddress, yページディレクトリ)

	ありcr3(oldcr3)
}
