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
