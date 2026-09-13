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
