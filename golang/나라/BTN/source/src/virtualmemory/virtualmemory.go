package virtualmemory

import . "common"

const (
	Kernelvirtaddress	= 3 * Gb
	Userstackཚད		= 32 * Kb
	Userstacktop		= 64 * Mb
	Userstack		= Userstacktop - Userstackཚད
)

func Virttest() {
	Typetest()
}
