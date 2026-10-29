/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualmemoria

import . "común"

const (
	NúcleovirtDirección	= 3 * Gb
	UsuariostackTamaño	= 32 * Kb
	UsuariostackSuperior	= 64 * Mb
	Usuariostack		= UsuariostackSuperior - UsuariostackTamaño
)

func VirtProbar() {
	TipoProbar()
}
