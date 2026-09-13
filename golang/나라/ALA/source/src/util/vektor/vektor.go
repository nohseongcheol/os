package vektor

import . "unsafe"
import . "konsol"

var nodVektor [100]uintptr

type TVektor struct {
	Storlek_2 int
}

func (själv *TVektor) Läggtill(adressreferens uintptr) {
	nodVektor[själv.Storlek_2] = adressreferens
	själv.Storlek_2++
}
func (själv *TVektor) Getat(index int) Pointer {
	return Pointer(nodVektor[index])
}
func (själv *TVektor) Indexav(adressreferens uintptr) int {
	i := 0
	for ; i < själv.Storlek_2; i++ {
		if adressreferens == nodVektor[i] {
			return i
		}
	}
	return -1
}

var konsol_2 = TKonsol{}

func (själv *TVektor) Skrivut() {
	konsol_2.MSkrivutxy("array:", 1, 1)

	for i := 0; i < själv.Storlek_2; i++ {
		konsol_2.MUnsignedinteger32Skrivut(uint32(nodVektor[i]))
		konsol_2.MSkrivut(":")
	}
}
