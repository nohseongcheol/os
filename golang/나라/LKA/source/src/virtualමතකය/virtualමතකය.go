package virtualමතකය

import . "common"

const (
	Kernelvirtaddress	= 3 * Gb
	Userstacksize		= 32 * Kb
	Userstackඉහළ		= 64 * Mb
	Userstack		= Userstackඉහළ - Userstacksize
)

func Virttest() {
	Typetest()
}
