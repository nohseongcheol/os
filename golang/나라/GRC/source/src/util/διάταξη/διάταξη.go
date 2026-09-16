/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package διάταξη

import . "unsafe"
import . "console"

var κόμβοςΔιάταξη [100]uintptr

type TΔιάταξη struct {
	Μέγεθος_2 int
}

func (self *TΔιάταξη) Προσθήκη(δείκτης uintptr) {
	κόμβοςΔιάταξη[self.Μέγεθος_2] = δείκτης
	self.Μέγεθος_2++
}
func (self *TΔιάταξη) Getat(κατάλογος int) Pointer {
	return Pointer(κόμβοςΔιάταξη[κατάλογος])
}
func (self *TΔιάταξη) Κατάλογοςαπό(δείκτης uintptr) int {
	i := 0
	for ; i < self.Μέγεθος_2; i++ {
		if δείκτης == κόμβοςΔιάταξη[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TΔιάταξη) Εκτύπωση() {
	console_2.MΕκτύπωσηxy("array:", 1, 1)

	for i := 0; i < self.Μέγεθος_2; i++ {
		console_2.MUnsignedinteger32Εκτύπωση(uint32(κόμβοςΔιάταξη[i]))
		console_2.MΕκτύπωση(":")
	}
}
