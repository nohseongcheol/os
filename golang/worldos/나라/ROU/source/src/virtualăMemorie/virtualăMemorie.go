/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualăMemorie

import . "comun"

const (
	Kernelvirtaddress	= 3 * Gb
	UtilizatorstackMărime	= 32 * Kb
	UtilizatorstackSus	= 64 * Mb
	Utilizatorstack		= UtilizatorstackSus - UtilizatorstackMărime
)

func VirtTestează() {
	TipTestează()
}
