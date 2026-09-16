/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package масив

import . "unsafe"
import . "консоль"

var вузолМасив [100]uintptr

type TМасив struct {
	Розмір_2 int
}

func (поточний *TМасив) Додати(посилання_на_адресу uintptr) {
	вузолМасив[поточний.Розмір_2] = посилання_на_адресу
	поточний.Розмір_2++
}
func (поточний *TМасив) Getat(індекс int) Pointer {
	return Pointer(вузолМасив[індекс])
}
func (поточний *TМасив) Індексз(посилання_на_адресу uintptr) int {
	i := 0
	for ; i < поточний.Розмір_2; i++ {
		if посилання_на_адресу == вузолМасив[i] {
			return i
		}
	}
	return -1
}

var консоль_2 = TКонсоль{}

func (поточний *TМасив) Друк() {
	консоль_2.MДрукxy("array:", 1, 1)

	for i := 0; i < поточний.Розмір_2; i++ {
		консоль_2.MUnsignedinteger32Друк(uint32(вузолМасив[i]))
		консоль_2.MДрук(":")
	}
}
