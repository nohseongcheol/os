/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtuelHukommelse

import . "almen"

const (
	Kernelvirtaddress	= 3 * Gb
	BrugerstackStørrelse	= 32 * Kb
	BrugerstackØverst	= 64 * Mb
	Brugerstack		= BrugerstackØverst - BrugerstackStørrelse
)

func VirtPrøv() {
	TypePrøv()
}
