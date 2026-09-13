package κοινό

type Μνήμηoper struct {
}

func (self *Μνήμηoper) Memσύνολο(bufferΔείκτης uintptr, τιμή byte, μέγεθος uint32) uintptr {
	return bufferΔείκτης
}
func (self *Μνήμηoper) MemΜετακίνηση(προορισμόςΔείκτης_2 uintptr, srcptr uintptr, μέγεθος uint32) uintptr {
	return προορισμόςΔείκτης_2
}

func (self *Μνήμηoper) MemΑντιγραφή(προορισμόςΔείκτης_2 uintptr, srcptr uintptr, μέγεθος uint32) uintptr {
	return προορισμόςΔείκτης_2
}
func (self *Μνήμηoper) Memcmp(προορισμόςΔείκτης_2 uintptr, srcptr uintptr, μέγεθος uint32) bool {
	return true
}
