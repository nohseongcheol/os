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
