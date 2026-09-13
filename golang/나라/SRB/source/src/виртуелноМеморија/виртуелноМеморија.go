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
