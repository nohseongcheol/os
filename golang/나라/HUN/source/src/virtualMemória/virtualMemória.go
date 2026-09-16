/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
