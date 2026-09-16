/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package виртуелноМеморија

import . "вообичаено"

const (
	Kernelvirtaddress	= 3 * Gb
	КорисникstackГолемина	= 32 * Kb
	КорисникstackГоре	= 64 * Mb
	Корисникstack		= КорисникstackГоре - КорисникstackГолемина
)

func Virttest() {
	Типtest()
}
