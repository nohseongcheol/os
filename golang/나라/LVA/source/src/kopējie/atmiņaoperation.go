package kopējie

type Atmiņaoper struct {
}

func (pats *Atmiņaoper) Memkopa(bufferKursors uintptr, vērtība byte, izmērs uint32) uintptr {
	return bufferKursors
}
func (pats *Atmiņaoper) MemPārvietot(mērķisKursors_2 uintptr, srcptr uintptr, izmērs uint32) uintptr {
	return mērķisKursors_2
}

func (pats *Atmiņaoper) MemKopēt(mērķisKursors_2 uintptr, srcptr uintptr, izmērs uint32) uintptr {
	return mērķisKursors_2
}
func (pats *Atmiņaoper) Memcmp(mērķisKursors_2 uintptr, srcptr uintptr, izmērs uint32) bool {
	return true
}
