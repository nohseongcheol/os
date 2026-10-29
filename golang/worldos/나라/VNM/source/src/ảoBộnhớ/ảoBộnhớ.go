/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ảoBộnhớ

import . "chung"

const (
	Kernelvirtaddress	= 3 * Gb
	NgườidùngstackCỡ	= 32 * Kb
	NgườidùngstackTrên	= 64 * Mb
	Ngườidùngstack		= NgườidùngstackTrên - NgườidùngstackCỡ
)

func VirtThử() {
	KiểuThử()
}
