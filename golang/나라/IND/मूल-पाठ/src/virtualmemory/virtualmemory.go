package virtualmemory

import . "common"

const (
	Kernelvirtaddress	= 3 * Gb
	Userstacksize		= 32 * Kb
	Userstackउपर		= 64 * Mb
	Userstack		= Userstackउपर - Userstacksize
)

func Virttest() {
	Typetest()
}
