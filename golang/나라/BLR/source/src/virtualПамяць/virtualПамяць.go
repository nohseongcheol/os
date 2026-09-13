package virtualПамяць

import . "агульныязнакі"

const (
	Kernelvirtaddress	= 3 * ГБ
	КарыстальнікstackПамер	= 32 * КБ
	КарыстальнікstackЗверху	= 64 * МБ
	Карыстальнікstack	= КарыстальнікstackЗверху - КарыстальнікstackПамер
)

func VirtПраверка() {
	ТыпПраверка()
}
