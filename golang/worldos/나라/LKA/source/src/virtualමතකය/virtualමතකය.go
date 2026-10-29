/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
