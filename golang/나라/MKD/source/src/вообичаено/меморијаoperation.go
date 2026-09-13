package вообичаено

type Меморијаoper struct {
}

func (само *Меморијаoper) Memпостави(bufferСтрелка uintptr, вредност byte, големина uint32) uintptr {
	return bufferСтрелка
}
func (само *Меморијаoper) MemПомести(одредиштеСтрелка_2 uintptr, srcptr uintptr, големина uint32) uintptr {
	return одредиштеСтрелка_2
}

func (само *Меморијаoper) MemКопирај(одредиштеСтрелка_2 uintptr, srcptr uintptr, големина uint32) uintptr {
	return одредиштеСтрелка_2
}
func (само *Меморијаoper) Memcmp(одредиштеСтрелка_2 uintptr, srcptr uintptr, големина uint32) bool {
	return true
}
