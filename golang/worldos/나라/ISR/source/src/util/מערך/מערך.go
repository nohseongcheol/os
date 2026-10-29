/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package מערך

import . "unsafe"
import . "console"

var צומתמערך [100]uintptr

type Tמערך struct {
	Sגודל_2 int
}

func (self *Tמערך) Aהוספה(סמן uintptr) {
	צומתמערך[self.Sגודל_2] = סמן
	self.Sגודל_2++
}
func (self *Tמערך) Getat(מפתח int) Pointer {
	return Pointer(צומתמערך[מפתח])
}
func (self *Tמערך) Iמפתחמתוך(סמן uintptr) int {
	i := 0
	for ; i < self.Sגודל_2; i++ {
		if סמן == צומתמערך[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *Tמערך) Pהדפסה() {
	console_2.Mהדפסהxy("array:", 1, 1)

	for i := 0; i < self.Sגודל_2; i++ {
		console_2.MUnsignedinteger32הדפסה(uint32(צומתמערך[i]))
		console_2.Mהדפסה(":")
	}
}
