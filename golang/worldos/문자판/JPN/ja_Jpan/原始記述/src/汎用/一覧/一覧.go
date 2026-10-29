/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 一覧

import . "unsafe"
import . "コンソール"
import mem "メモリ管理者"

type T連結要素 struct {
	番地参照		uintptr
	previous	*T連結要素
	次		*T連結要素
}

type Linked一覧 struct {
	head	*T連結要素
	tail	*T連結要素
	Sサイズ_2	int

	mem	*mem.Tメモリ管理者
}

func (self *Linked一覧) Init(mem *mem.Tメモリ管理者) {
	self.head = nil
	self.tail = nil
	self.Sサイズ_2 = 0

	self.mem = mem
}
func (self *Linked一覧) M先頭に追加(番地参照 uintptr) {
	新規ノード := (*T連結要素)(self.mem.M記憶領域を確保(uint32(Sizeof(T連結要素{}))))
	if 新規ノード == nil {
		return
	}
	新規ノード.番地参照 = 番地参照
	新規ノード.previous = nil
	新規ノード.次 = self.head
	if self.head != nil {
		self.head.previous = 新規ノード
	}
	self.head = 新規ノード
	self.Sサイズ_2++

	if self.head.次 == nil {
		self.tail = self.head
	}

}
func (self *Linked一覧) M末尾に追加(番地参照 uintptr) {
	if self.Sサイズ_2 == 0 {
		self.M先頭に追加(番地参照)
	} else {
		新規ノード := (*T連結要素)(self.mem.M記憶領域を確保(uint32(Sizeof(T連結要素{}))))
		if 新規ノード == nil {
			return
		}
		新規ノード.番地参照 = 番地参照
		新規ノード.previous = self.tail
		新規ノード.次 = nil
		self.tail.次 = 新規ノード
		self.tail = 新規ノード
		self.Sサイズ_2++
	}
}
func (self *Linked一覧) M指定位置に挿入(目次 int, 番地参照 uintptr) {
	if 目次 == 0 {
		self.M先頭に追加(番地参照)
	} else {
		previousノード := self.Getノードat(目次 - 1)
		次ノード := previousノード.次
		新規ノード := (*T連結要素)(self.mem.M記憶領域を確保(uint32(Sizeof(T連結要素{}))))
		if 新規ノード == nil {
			return
		}
		新規ノード.番地参照 = 番地参照

		previousノード.次 = 新規ノード
		新規ノード.previous = previousノード
		新規ノード.次 = 次ノード
		if 次ノード != nil {
			次ノード.previous = 新規ノード
		}

		self.Sサイズ_2++

		if 新規ノード.次 == nil {
			self.tail = 新規ノード
		}
	}
}
func (self *Linked一覧) Getノードat(目次 int) *T連結要素 {
	if 目次 < 0 || 目次 >= self.Sサイズ_2 {
		return nil
	}
	var x *T連結要素 = self.head
	for i := 0; i < 目次; i++ {
		x = x.次
	}
	return x
}

func (self *Linked一覧) Sありノードat(目次 int, 番地参照 uintptr) {
	var x *T連結要素 = self.head
	for i := 0; i < 目次; i++ {
		x = x.次
	}
	if x != nil {
		x.番地参照 = 番地参照
	}
}
func (self *Linked一覧) Getat(目次 int) Pointer {
	連結要素 := self.Getノードat(目次)
	if 連結要素 == nil {
		return nil
	}
	var 番地参照 uintptr = 連結要素.番地参照
	return Pointer(番地参照)
}
func (self *Linked一覧) I目次of(番地参照 uintptr) int {
	var n *T連結要素 = self.head
	i := 0
	for ; i < self.Sサイズ_2; i++ {
		if 番地参照 == n.番地参照 {
			return i
		}
		n = n.次
	}
	return -1
}
func (self *Linked一覧) R削除(番地参照 uintptr) {
	目次 := self.I目次of(番地参照)
	if 目次 < 0 {
		return
	}
	self.R削除at(目次)
}
func (self *Linked一覧) R削除at(目次 int) {
	if 目次 < 0 || 目次 >= self.Sサイズ_2 {
		return
	}
	連結要素 := self.Getノードat(目次)
	if 連結要素 == nil {
		return
	}
	if 連結要素.previous != nil {
		連結要素.previous.次 = 連結要素.次
	} else {
		self.head = 連結要素.次
	}
	if 連結要素.次 != nil {
		連結要素.次.previous = 連結要素.previous
	} else {
		self.tail = 連結要素.previous
	}
	self.Sサイズ_2 = self.Sサイズ_2 - 1

	if self.mem != nil {
		self.mem.F空き(Pointer(連結要素))
	}
}

var コンソール_2 = Tコンソール{}

func (self *Linked一覧) P印刷() {
	コンソール_2.M印刷xy("LinkedList:", 1, 1)
	コンソール_2.MUnsignedinteger32印刷(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Sサイズ_2; i++ {
		連結要素 := (*T連結要素)(self.Getat(i))
		コンソール_2.MUnsignedinteger32印刷(uint32(連結要素.番地参照))
		コンソール_2.M印刷(":")
	}
}
