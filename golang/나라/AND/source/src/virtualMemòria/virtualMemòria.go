package virtualMemòria

import . "comú"

const (
	KernelvirtAdreça	= 3 * Gb
	UsuaristackMida		= 32 * Kb
	UsuaristackAdalt	= 64 * Mb
	Usuaristack		= UsuaristackAdalt - UsuaristackMida
)

func VirtProva() {
	TipusProva()
}
