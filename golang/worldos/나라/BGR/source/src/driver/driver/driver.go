/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Активиране()
	Възстановяване() int
	Деактивиране()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var числоdriver int

func (себеси *TDrivermanager) Init() {
	числоdriver = 0
}

func (себеси *TDrivermanager) Добавянеdriver(driver_2 IDriver) {
	idriver[числоdriver] = driver_2
	числоdriver++
}
func (себеси *TDrivermanager) АктивиранеВсички() {
	for i := 0; i < числоdriver; i++ {
		idriver[i].Активиране()
	}
}
