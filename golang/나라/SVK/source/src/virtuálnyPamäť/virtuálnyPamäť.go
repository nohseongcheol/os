/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtuálnyPamäť

import . "bežné"

const (
	Kernelvirtaddress	= 3 * Gb
	PoužívateľstackVeľkosť	= 32 * Kb
	PoužívateľstackHore	= 64 * Milibarov
	Používateľstack		= PoužívateľstackHore - PoužívateľstackVeľkosť
)

func VirtOtestovať() {
	TypOtestovať()
}
