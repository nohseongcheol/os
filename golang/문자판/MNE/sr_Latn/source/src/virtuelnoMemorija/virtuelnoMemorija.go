/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtuelnoMemorija

import . "zajednički"

const (
	Kernelvirtaddress	= 3 * GB
	KorisnikstackVeličina	= 32 * KB
	KorisnikstackGore	= 64 * MB
	Korisnikstack		= KorisnikstackGore - KorisnikstackVeličina
)

func VirtTest() {
	VrstaTest()
}
