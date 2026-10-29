/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Активирај()
	Ресетирај() int
	Деактивирај()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var numberdriver int

func (само *TDrivermanager) Init() {
	numberdriver = 0
}

func (само *TDrivermanager) Додајdriver(driver_2 IDriver) {
	idriver[numberdriver] = driver_2
	numberdriver++
}
func (само *TDrivermanager) АктивирајСѐ() {
	for i := 0; i < numberdriver; i++ {
		idriver[i].Активирај()
	}
}
