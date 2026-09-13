package virtuellMinne

import . "vanlig"

const (
	Kernelvirtaddress	= 3 * Gb
	BrukerstackStørrelse	= 32 * Kb
	BrukerstackOppe		= 64 * Mb
	Brukerstack		= BrukerstackOppe - BrukerstackStørrelse
)

func Virttest() {
	Filtypetest()
}
