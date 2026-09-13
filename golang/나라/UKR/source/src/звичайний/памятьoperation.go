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
