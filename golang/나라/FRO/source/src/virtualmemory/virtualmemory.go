/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualmemory

import . "common"

const (
	Kernelvirtaddress	= 3 * Gb
	BrúkaristackStødd	= 32 * Kb
	BrúkaristackToppur	= 64 * Mb
	Brúkaristack		= BrúkaristackToppur - BrúkaristackStødd
)

func Virttest() {
	Typetest()
}
