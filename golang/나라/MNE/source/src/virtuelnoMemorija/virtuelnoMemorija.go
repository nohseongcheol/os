package virtuelnoMemorija

import . "заједнички"

const (
	Kernelvirtaddress	= 3 * ГБ
	KorisnikstackВеличина	= 32 * КБ
	KorisnikstackГоре	= 64 * МБ
	Korisnikstack		= KorisnikstackГоре - KorisnikstackВеличина
)

func VirtТест() {
	ВрстаТест()
}
