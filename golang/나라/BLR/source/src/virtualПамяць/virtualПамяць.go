/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
