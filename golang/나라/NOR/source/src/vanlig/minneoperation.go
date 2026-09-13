package vanlig

type Minneoper struct {
}

func (selv *Minneoper) MemSett(bufferPeker uintptr, verdi byte, størrelse uint32) uintptr {
	return bufferPeker
}
func (selv *Minneoper) MemFlytt(målPeker_2 uintptr, srcptr uintptr, størrelse uint32) uintptr {
	return målPeker_2
}

func (selv *Minneoper) MemKopier(målPeker_2 uintptr, srcptr uintptr, størrelse uint32) uintptr {
	return målPeker_2
}
func (selv *Minneoper) Memcmp(målPeker_2 uintptr, srcptr uintptr, størrelse uint32) bool {
	return true
}
