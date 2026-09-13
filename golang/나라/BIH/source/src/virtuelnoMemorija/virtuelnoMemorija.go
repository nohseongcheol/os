package virtuelnoMemorija

import . "zajednički"

const (
	Kernelvirtaddress	= 3 * Gb
	KorisnikstackVeličina	= 32 * Kb
	Korisnikstacknavrh	= 64 * Mb
	Korisnikstack		= Korisnikstacknavrh - KorisnikstackVeličina
)

func Virttest() {
	Tiptest()
}
