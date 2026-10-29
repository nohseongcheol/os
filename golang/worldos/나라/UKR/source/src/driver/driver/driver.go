/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Активувати()
	Скинути() int
	Деактивувати()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var числоdriver int

func (поточний *TDrivermanager) Init() {
	числоdriver = 0
}

func (поточний *TDrivermanager) Додатиdriver(driver_2 IDriver) {
	idriver[числоdriver] = driver_2
	числоdriver++
}
func (поточний *TDrivermanager) АктивуватиВсі() {
	for i := 0; i < числоdriver; i++ {
		idriver[i].Активувати()
	}
}
