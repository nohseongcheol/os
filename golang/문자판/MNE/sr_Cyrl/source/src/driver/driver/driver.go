/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Покрени()
	Поновопостави() int
	Обустави()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var бројdriver int

func (исти *TDrivermanager) Init() {
	бројdriver = 0
}

func (исти *TDrivermanager) Додајdriver(driver_2 IDriver) {
	idriver[бројdriver] = driver_2
	бројdriver++
}
func (исти *TDrivermanager) ПокрениСве() {
	for i := 0; i < бројdriver; i++ {
		idriver[i].Покрени()
	}
}
