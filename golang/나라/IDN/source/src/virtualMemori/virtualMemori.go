package virtualMemori

import . "umum"

const (
	Kernelvirtaddress	= 3 * Gb
	PenggunastackUkuran	= 32 * Kb
	PenggunastackAtas	= 64 * Mb
	Penggunastack		= PenggunastackAtas - PenggunastackUkuran
)

func VirtTes() {
	TipeTes()
}
