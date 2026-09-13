package низ

import . "unsafe"
import . "конзола"

var чворНиз [100]uintptr

type TНиз struct {
	Величина_2 int
}

func (исти *TНиз) Додај(показивач uintptr) {
	чворНиз[исти.Величина_2] = показивач
	исти.Величина_2++
}
func (исти *TНиз) Getat(попис int) Pointer {
	return Pointer(чворНиз[попис])
}
func (исти *TНиз) Пописод(показивач uintptr) int {
	i := 0
	for ; i < исти.Величина_2; i++ {
		if показивач == чворНиз[i] {
			return i
		}
	}
	return -1
}

var конзола_2 = TКонзола{}

func (исти *TНиз) Штампај() {
	конзола_2.MШтампајxy("array:", 1, 1)

	for i := 0; i < исти.Величина_2; i++ {
		конзола_2.MUnsignedinteger32Штампај(uint32(чворНиз[i]))
		конзола_2.MШтампај(":")
	}
}
