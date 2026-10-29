/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package построи

import . "unsafe"
import . "console"

var nodeПострои [100]uintptr

type TПострои struct {
	Големина_2 int
}

func (само *TПострои) Додај(стрелка uintptr) {
	nodeПострои[само.Големина_2] = стрелка
	само.Големина_2++
}
func (само *TПострои) Getat(индекс int) Pointer {
	return Pointer(nodeПострои[индекс])
}
func (само *TПострои) Индексна(стрелка uintptr) int {
	i := 0
	for ; i < само.Големина_2; i++ {
		if стрелка == nodeПострои[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (само *TПострои) Печати() {
	console_2.MПечатиxy("array:", 1, 1)

	for i := 0; i < само.Големина_2; i++ {
		console_2.MUnsignedinteger32Печати(uint32(nodeПострои[i]))
		console_2.MПечати(":")
	}
}
