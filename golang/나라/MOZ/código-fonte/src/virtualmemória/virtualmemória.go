package virtualmemória

import . "comum"

const (
	NúcleovirtEndereço	= 3 * Gb
	UtilizadorstackTamanho	= 32 * Kb
	UtilizadorstackSuperior	= 64 * Mb
	Utilizadorstack		= UtilizadorstackSuperior - UtilizadorstackTamanho
)

func VirtTestar() {
	TipoTestar()
}
