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
