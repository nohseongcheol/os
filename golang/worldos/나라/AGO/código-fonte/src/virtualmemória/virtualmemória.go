/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
