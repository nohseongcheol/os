package נפוצים

type Mזיכרוןoper struct {
}

func (self *Mזיכרוןoper) Memקבע(bufferסמן uintptr, ערך byte, גודל uint32) uintptr {
	return bufferסמן
}
func (self *Mזיכרוןoper) Memהזז(יעדסמן_2 uintptr, srcptr uintptr, גודל uint32) uintptr {
	return יעדסמן_2
}

func (self *Mזיכרוןoper) Memהעתק(יעדסמן_2 uintptr, srcptr uintptr, גודל uint32) uintptr {
	return יעדסמן_2
}
func (self *Mזיכרוןoper) Memcmp(יעדסמן_2 uintptr, srcptr uintptr, גודל uint32) bool {
	return true
}
