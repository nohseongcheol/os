/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package виртуелноМеморија

import . "заједнички"

const (
	Kernelvirtaddress	= 3 * ГБ
	КорисникstackВеличина	= 32 * КБ
	КорисникstackГоре	= 64 * МБ
	Корисникstack		= КорисникstackГоре - КорисникstackВеличина
)

func VirtТест() {
	ВрстаТест()
}
