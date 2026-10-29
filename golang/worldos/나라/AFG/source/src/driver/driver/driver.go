/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aفعالکردن()
	Rبرگرداندنبهمقادیراولیه() int
	Dغیرفعالکردن()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var numberdriver int

func (خود *TDrivermanager) Init() {
	numberdriver = 0
}

func (خود *TDrivermanager) Aاضافهکردنdriver(driver_2 IDriver) {
	idriver[numberdriver] = driver_2
	numberdriver++
}
func (خود *TDrivermanager) Aفعالکردنهمه() {
	for i := 0; i < numberdriver; i++ {
		idriver[i].Aفعالکردن()
	}
}
