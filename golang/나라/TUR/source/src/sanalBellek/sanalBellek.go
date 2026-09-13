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
