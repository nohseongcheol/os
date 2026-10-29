/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package sanalBellek

import . "genel"

const (
	Kernelvirtaddress	= 3 * Gb
	KullanıcıstackBoyut	= 32 * Kb
	KullanıcıstackÜst	= 64 * Mb
	Kullanıcıstack		= KullanıcıstackÜst - KullanıcıstackBoyut
)

func VirtDene() {
	TürDene()
}
