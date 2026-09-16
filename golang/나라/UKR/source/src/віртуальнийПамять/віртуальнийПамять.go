/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package віртуальнийПамять

import . "звичайний"

const (
	KernelvirtАдреса	= 3 * ГБ
	КористувачstackРозмір	= 32 * КБ
	КористувачstackЗверху	= 64 * МБ
	Користувачstack		= КористувачstackЗверху - КористувачstackРозмір
)

func VirtТест() {
	ТипТест()
}
