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
