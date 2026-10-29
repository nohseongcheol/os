/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package لڑی

import . "unsafe"
import . "console"

var گرہلڑی [100]uintptr

type Tلڑی struct {
	Sحجم_2 int
}

func (self *Tلڑی) Aشاملکریں(پؤائنٹر uintptr) {
	گرہلڑی[self.Sحجم_2] = پؤائنٹر
	self.Sحجم_2++
}
func (self *Tلڑی) Getat(index int) Pointer {
	return Pointer(گرہلڑی[index])
}
func (self *Tلڑی) Indexبرائے(پؤائنٹر uintptr) int {
	i := 0
	for ; i < self.Sحجم_2; i++ {
		if پؤائنٹر == گرہلڑی[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *Tلڑی) Pچھاپیں() {
	console_2.Mچھاپیںxy("array:", 1, 1)

	for i := 0; i < self.Sحجم_2; i++ {
		console_2.MUnsignedinteger32چھاپیں(uint32(گرہلڑی[i]))
		console_2.Mچھاپیں(":")
	}
}
