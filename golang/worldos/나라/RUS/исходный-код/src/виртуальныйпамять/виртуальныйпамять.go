/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package виртуальныйпамять

import . "общий"

const (
	Ядроvirtaddress		= 3 * ГБ
	ПользовательstackРазмер	= 32 * КБ
	ПользовательstackСверху	= 64 * МБ
	Пользовательstack	= ПользовательstackСверху - ПользовательstackРазмер
)

func VirtПроверить() {
	ТипПроверить()
}
