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
