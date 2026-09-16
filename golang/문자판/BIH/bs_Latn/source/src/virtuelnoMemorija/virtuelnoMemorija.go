/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
