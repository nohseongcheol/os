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
