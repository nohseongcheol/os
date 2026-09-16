/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package common

type Mیادداشتoper struct {
}

func (self *Mیادداشتoper) Memسیٹ(bufferپؤائنٹر uintptr, قدر byte, حجم uint32) uintptr {
	return bufferپؤائنٹر
}
func (self *Mیادداشتoper) Memمنتقلکریں(destinationپؤائنٹر_2 uintptr, srcptr uintptr, حجم uint32) uintptr {
	return destinationپؤائنٹر_2
}

func (self *Mیادداشتoper) Memکاپی(destinationپؤائنٹر_2 uintptr, srcptr uintptr, حجم uint32) uintptr {
	return destinationپؤائنٹر_2
}
func (self *Mیادداشتoper) Memcmp(destinationپؤائنٹر_2 uintptr, srcptr uintptr, حجم uint32) bool {
	return true
}
