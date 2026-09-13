package virtualmemory

import . "common"

const (
	Kernelvirtaddress	= 3 * Gb
	Userstacksize		= 32 * Kb
	Userstacktop		= 64 * Mb
	Userstack		= Userstacktop - Userstacksize
)

func Virttest() {
	Typetest()
}
