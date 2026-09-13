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
