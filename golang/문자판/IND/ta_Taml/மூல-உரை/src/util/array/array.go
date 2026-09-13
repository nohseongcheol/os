package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Vஅளவு int
}

func (self *TArray) Add(முகவரிச்_சுட்டி uintptr) {
	nodeArray[self.Vஅளவு] = முகவரிச்_சுட்டி
	self.Vஅளவு++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(முகவரிச்_சுட்டி uintptr) int {
	i := 0
	for ; i < self.Vஅளவு; i++ {
		if முகவரிச்_சுட்டி == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Vஅளவு; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
