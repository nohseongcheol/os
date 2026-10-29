/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
