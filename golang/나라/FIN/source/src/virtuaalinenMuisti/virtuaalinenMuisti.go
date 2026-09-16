/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtuaalinenMuisti

import . "yhteinen"

const (
	Kernelvirtaddress	= 3 * Gb
	KäyttäjästackKoko	= 32 * Kt
	KäyttäjästackYlhäällä	= 64 * Mt
	Käyttäjästack		= KäyttäjästackYlhäällä - KäyttäjästackKoko
)

func VirtKokeile() {
	TyyppiKokeile()
}
