/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
