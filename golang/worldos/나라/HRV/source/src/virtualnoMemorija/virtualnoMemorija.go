/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
