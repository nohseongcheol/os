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
