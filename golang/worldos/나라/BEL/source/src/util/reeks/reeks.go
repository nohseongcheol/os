/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package reeks

import . "unsafe"
import . "console"

var systeemnaamReeks [100]uintptr

type TReeks struct {
	Grootte_2 int
}

func (zelf *TReeks) Toevoegen(adresverwijzing uintptr) {
	systeemnaamReeks[zelf.Grootte_2] = adresverwijzing
	zelf.Grootte_2++
}
func (zelf *TReeks) Getat(index int) Pointer {
	return Pointer(systeemnaamReeks[index])
}
func (zelf *TReeks) Indexvan(adresverwijzing uintptr) int {
	i := 0
	for ; i < zelf.Grootte_2; i++ {
		if adresverwijzing == systeemnaamReeks[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (zelf *TReeks) Afdrukken() {
	console_2.MAfdrukkenxy("array:", 1, 1)

	for i := 0; i < zelf.Grootte_2; i++ {
		console_2.MUnsignedinteger32Afdrukken(uint32(systeemnaamReeks[i]))
		console_2.MAfdrukken(":")
	}
}
