package общий

type Памятьoper struct {
}

func (текущий *Памятьoper) Memуказать(bufferУказатели uintptr, значение byte, размер uint32) uintptr {
	return bufferУказатели
}
func (текущий *Памятьoper) MemПереместить(назначениеУказатели_2 uintptr, srcptr uintptr, размер uint32) uintptr {
	return назначениеУказатели_2
}

func (текущий *Памятьoper) Memкопировать(назначениеУказатели_2 uintptr, srcptr uintptr, размер uint32) uintptr {
	return назначениеУказатели_2
}
func (текущий *Памятьoper) MemNOT(назначениеУказатели_2 uintptr, srcptr uintptr, размер uint32) bool {
	return true
}
