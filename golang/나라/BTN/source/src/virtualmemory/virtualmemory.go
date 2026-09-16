/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
