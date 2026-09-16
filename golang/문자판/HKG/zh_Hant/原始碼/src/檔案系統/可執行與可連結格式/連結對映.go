/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 可執行與可連結格式

import . "unsafe"
import . "控制台"

import mem "記憶體管理器"

type L連結 struct {
	D動態		uintptr
	Previous	*L連結
	N下一個		*L連結
}
type L連結對映 struct {
	First	*L連結
	L最後	*L連結

	S大小_2	int

	mem	*mem.T記憶體管理器
}

func (self *L連結對映) Init(mem *mem.T記憶體管理器) {
	self.mem = mem
}
func (self *L連結對映) Clone() L連結對映 {
	var 連結對映 L連結對映

	連結對映.Init(self.mem)

	L連結 := self.First

	for ; L連結 != nil; L連結 = L連結.N下一個 {
		連結對映.M附加至串列尾端(L連結.D動態)
	}
	return 連結對映
}
func (self *L連結對映) M加入至串列開頭(D動態 uintptr) {
	新增連結 := (*L連結)(self.mem.M配置記憶體(uint32(Sizeof(L連結{}))))
	新增連結.D動態 = D動態
	新增連結.N下一個 = self.First
	self.First = 新增連結
	self.S大小_2++

	if self.First.N下一個 == nil {
		self.L最後 = self.First
	}
}
func (self *L連結對映) M附加至串列尾端(D動態 uintptr) {
	if D動態 == 0 {
		return
	}

	if self.S大小_2 == 0 {
		self.M加入至串列開頭(D動態)
	} else {
		新增連結 := (*L連結)(self.mem.M配置記憶體(uint32(Sizeof(L連結{}))))
		新增連結.D動態 = D動態
		新增連結.N下一個 = nil
		self.L最後.N下一個 = 新增連結
		self.L最後 = 新增連結
		self.S大小_2++
	}
}
func (self *L連結對映) P列印(x uint16, y uint16) {
	L連結 := self.First
	控制台_2 := T控制台{}
	控制台_2.M列印xy("linkmap : ", x, y)
	for ; L連結 != nil; L連結 = L連結.N下一個 {
		控制台_2.MUnsignedinteger32列印(uint32(L連結.D動態))
		控制台_2.M列印("+")

	}
}
