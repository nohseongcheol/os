/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtuellMinne

import . "gemensam"

const (
	KernelvirtAdress	= 3 * Gb
	AnvändarestackStorlek	= 32 * Kb
	AnvändarestackÖverst	= 64 * Mb
	Användarestack		= AnvändarestackÖverst - AnvändarestackStorlek
)

func VirtTesta() {
	TypTesta()
}
