package virtualnoMemorija

import . "uobičajeno"

const (
	Kernelvirtaddress	= 3 * Gb
	KorisnikstackVeličina	= 32 * Kb
	KorisnikstackVrh	= 64 * Mbar
	Korisnikstack		= KorisnikstackVrh - KorisnikstackVeličina
)

func VirtProvjeri() {
	VrstaProvjeri()
}
