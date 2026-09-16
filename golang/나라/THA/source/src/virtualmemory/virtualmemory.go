/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualmemory

import . "common"

const (
	Kernelvirtaddress	= 3 * Gb
	Userstackขนาด		= 32 * Kb
	Userstackบน		= 64 * Mb
	Userstack		= Userstackบน - Userstackขนาด
)

func Virtทดสอบ() {
	Tประเภททดสอบ()
}
