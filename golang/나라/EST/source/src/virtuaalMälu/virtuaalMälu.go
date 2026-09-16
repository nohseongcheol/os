/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtuaalMälu

import . "üldine"

const (
	Kernelvirtaddress	= 3 * Gb
	KasutajastackSuurus	= 32 * Kb
	KasutajastackÜleval	= 64 * Mbar
	Kasutajastack		= KasutajastackÜleval - KasutajastackSuurus
)

func VirtTesti() {
	LiikTesti()
}
