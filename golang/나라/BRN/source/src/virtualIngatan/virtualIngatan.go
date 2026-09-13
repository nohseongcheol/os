package virtualIngatan

import . "biasa"

const (
	Kernelvirtaddress	= 3 * Gb
	PenggunastackSaiz	= 32 * Kb
	PenggunastackAtas	= 64 * Mb
	Penggunastack		= PenggunastackAtas - PenggunastackSaiz
)

func VirtUji() {
	JenisUji()
}
