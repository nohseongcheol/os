/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
