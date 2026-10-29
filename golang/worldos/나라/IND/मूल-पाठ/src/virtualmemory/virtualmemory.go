/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
