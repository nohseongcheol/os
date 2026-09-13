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
