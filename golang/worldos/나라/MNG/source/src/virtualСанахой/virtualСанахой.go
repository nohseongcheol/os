/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualСанахой

import . "үндсэн"

const (
	Kernelvirtaddress	= 3 * Gb
	ХэрэглэгчstackХэмжээ	= 32 * Kb
	Хэрэглэгчstackдээр	= 64 * Mb
	Хэрэглэгчstack		= Хэрэглэгчstackдээр - ХэрэглэгчstackХэмжээ
)

func Virttest() {
	Төрөлtest()
}
