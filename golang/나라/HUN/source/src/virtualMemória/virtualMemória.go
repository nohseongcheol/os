package virtualMemória

import . "közös"

const (
	Kernelvirtaddress	= 3 * Gb
	FelhasználóstackMéret	= 32 * Kb
	FelhasználóstackFent	= 64 * Mb
	Felhasználóstack	= FelhasználóstackFent - FelhasználóstackMéret
)

func VirtTeszt() {
	TípusTeszt()
}
