package низ

import . "unsafe"
import . "конзола"

var чворНиз [100]uintptr

type TНиз struct {
	Величина_2 int
}

func (isti *TНиз) Додај(pokazivač uintptr) {
	чворНиз[isti.Величина_2] = pokazivač
	isti.Величина_2++
}
func (isti *TНиз) Getat(popis int) Pointer {
	return Pointer(чворНиз[popis])
}
func (isti *TНиз) Popisod(pokazivač uintptr) int {
	i := 0
	for ; i < isti.Величина_2; i++ {
		if pokazivač == чворНиз[i] {
			return i
		}
	}
	return -1
}

var конзола_2 = TКонзола{}

func (isti *TНиз) Štampaj() {
	конзола_2.MŠtampajxy("array:", 1, 1)

	for i := 0; i < isti.Величина_2; i++ {
		конзола_2.MUnsignedinteger32Štampaj(uint32(чворНиз[i]))
		конзола_2.MŠtampaj(":")
	}
}
