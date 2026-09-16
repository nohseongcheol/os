/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
