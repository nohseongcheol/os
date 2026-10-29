/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualmemory

import . "умумӣ"

const (
	Kernelvirtaddress		= 3 * Gb
	Истифодакунандаstacksize	= 32 * Kb
	ИстифодакунандаstackБоло	= 64 * Mb
	Истифодакунандаstack		= ИстифодакунандаstackБоло - Истифодакунандаstacksize
)

func Virttest() {
	Typetest()
}
