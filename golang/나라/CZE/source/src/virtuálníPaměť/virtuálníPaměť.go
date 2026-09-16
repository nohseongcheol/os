/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtuálníPaměť

import . "běžné"

const (
	KernelvirtAdresa	= 3 * Gb
	UživatelstackVelikost	= 32 * Kb
	UživatelstackNahoře	= 64 * Mb
	Uživatelstack		= UživatelstackNahoře - UživatelstackVelikost
)

func VirtOtestovat() {
	TypOtestovat()
}
