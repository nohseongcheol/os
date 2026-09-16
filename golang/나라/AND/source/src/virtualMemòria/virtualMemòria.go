/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
