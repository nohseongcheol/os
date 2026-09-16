/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualArika

import . "common"

const (
	Kernelvirtaddress	= 3 * Gb
	MpampiasastackHabe	= 32 * Kb
	Mpampiasastackambony	= 64 * Mb
	Mpampiasastack		= Mpampiasastackambony - MpampiasastackHabe
)

func Virttest() {
	Karazanatest()
}
