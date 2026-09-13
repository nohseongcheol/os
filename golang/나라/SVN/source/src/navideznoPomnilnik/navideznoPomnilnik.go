package navideznoPomnilnik

import . "skupno"

const (
	Kernelvirtaddress	= 3 * Gb
	UporabnikstackVelikost	= 32 * Kb
	UporabnikstackVrh	= 64 * Mb
	Uporabnikstack		= UporabnikstackVrh - UporabnikstackVelikost
)

func VirtPreizkus() {
	VrstaPreizkus()
}
