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
