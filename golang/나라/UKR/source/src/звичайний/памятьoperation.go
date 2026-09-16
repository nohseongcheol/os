/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package звичайний

type Памятьoper struct {
}

func (поточний *Памятьoper) Memмножина(bufferВказівник uintptr, значення byte, розмір uint32) uintptr {
	return bufferВказівник
}
func (поточний *Памятьoper) MemПеремістити(призначенняВказівник_2 uintptr, srcptr uintptr, розмір uint32) uintptr {
	return призначенняВказівник_2
}

func (поточний *Памятьoper) MemКопіювати(призначенняВказівник_2 uintptr, srcptr uintptr, розмір uint32) uintptr {
	return призначенняВказівник_2
}
func (поточний *Памятьoper) Memcmp(призначенняВказівник_2 uintptr, srcptr uintptr, розмір uint32) bool {
	return true
}
