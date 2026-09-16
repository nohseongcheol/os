/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualПамет

import . "честосрещани"

const (
	Kernelvirtaddress	= 3 * ГБ
	СобственикstackРазмер	= 32 * КБ
	СобственикstackГоре	= 64 * МБ
	Собственикstack		= СобственикstackГоре - СобственикstackРазмер
)

func VirtТест() {
	ТипТест()
}
