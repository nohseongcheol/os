package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Vਆਕਾਰ int
}

func (self *TArray) Add(ਪਤੇ_ਦਾ_ਹਵਾਲਾ uintptr) {
	nodeArray[self.Vਆਕਾਰ] = ਪਤੇ_ਦਾ_ਹਵਾਲਾ
	self.Vਆਕਾਰ++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(ਪਤੇ_ਦਾ_ਹਵਾਲਾ uintptr) int {
	i := 0
	for ; i < self.Vਆਕਾਰ; i++ {
		if ਪਤੇ_ਦਾ_ਹਵਾਲਾ == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Vਆਕਾਰ; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
