/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 実行連結形式

import . "unsafe"
import . "コンソール"

import mem "メモリ管理者"

type L連結 struct {
	D動的に		uintptr
	Previous	*L連結
	N次		*L連結
}
type L連結対応表 struct {
	First	*L連結
	L最後	*L連結

	Sサイズ_2	int

	mem	*mem.Tメモリ管理者
}

func (self *L連結対応表) Init(mem *mem.Tメモリ管理者) {
	self.mem = mem
}
func (self *L連結対応表) Clone() L連結対応表 {
	var 連結対応表 L連結対応表

	連結対応表.Init(self.mem)

	L連結 := self.First

	for ; L連結 != nil; L連結 = L連結.N次 {
		連結対応表.M末尾に追加(L連結.D動的に)
	}
	return 連結対応表
}
func (self *L連結対応表) M先頭に追加(D動的に uintptr) {
	新規連結 := (*L連結)(self.mem.M記憶領域を確保(uint32(Sizeof(L連結{}))))
	新規連結.D動的に = D動的に
	新規連結.N次 = self.First
	self.First = 新規連結
	self.Sサイズ_2++

	if self.First.N次 == nil {
		self.L最後 = self.First
	}
}
func (self *L連結対応表) M末尾に追加(D動的に uintptr) {
	if D動的に == 0 {
		return
	}

	if self.Sサイズ_2 == 0 {
		self.M先頭に追加(D動的に)
	} else {
		新規連結 := (*L連結)(self.mem.M記憶領域を確保(uint32(Sizeof(L連結{}))))
		新規連結.D動的に = D動的に
		新規連結.N次 = nil
		self.L最後.N次 = 新規連結
		self.L最後 = 新規連結
		self.Sサイズ_2++
	}
}
func (self *L連結対応表) P印刷(x uint16, y uint16) {
	L連結 := self.First
	コンソール_2 := Tコンソール{}
	コンソール_2.M印刷xy("linkmap : ", x, y)
	for ; L連結 != nil; L連結 = L連結.N次 {
		コンソール_2.MUnsignedinteger32印刷(uint32(L連結.D動的に))
		コンソール_2.M印刷("+")

	}
}
