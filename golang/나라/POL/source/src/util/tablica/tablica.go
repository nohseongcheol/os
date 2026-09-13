package tablica

import . "unsafe"
import . "konsola"

var węzełTablica [100]uintptr

type TTablica struct {
	Rozmiar_2 int
}

func (bieżący *TTablica) Dodaj(odwołanie_do_adresu uintptr) {
	węzełTablica[bieżący.Rozmiar_2] = odwołanie_do_adresu
	bieżący.Rozmiar_2++
}
func (bieżący *TTablica) Getat(indeks int) Pointer {
	return Pointer(węzełTablica[indeks])
}
func (bieżący *TTablica) Indeksz(odwołanie_do_adresu uintptr) int {
	i := 0
	for ; i < bieżący.Rozmiar_2; i++ {
		if odwołanie_do_adresu == węzełTablica[i] {
			return i
		}
	}
	return -1
}

var konsola_2 = TKonsola{}

func (bieżący *TTablica) Wydrukuj() {
	konsola_2.MWydrukujxy("array:", 1, 1)

	for i := 0; i < bieżący.Rozmiar_2; i++ {
		konsola_2.MUnsignedinteger32Wydrukuj(uint32(węzełTablica[i]))
		konsola_2.MWydrukuj(":")
	}
}
