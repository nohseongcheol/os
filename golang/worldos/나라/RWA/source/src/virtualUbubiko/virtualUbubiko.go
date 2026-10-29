/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualUbubiko

import . "common"

const (
	Kernelvirtaddress	= 3 * Gb
	UkoreshastackIngano	= 32 * Kb
	Ukoreshastacktop	= 64 * Mb
	Ukoreshastack		= Ukoreshastacktop - UkoreshastackIngano
)

func Virttest() {
	Ubwokotest()
}
