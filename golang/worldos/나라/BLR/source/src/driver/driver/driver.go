/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Задзейнічаць()
	Скінуць() int
	Абяздзейнічаць()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var нУМАРdriver int

func (self *TDrivermanager) Init() {
	нУМАРdriver = 0
}

func (self *TDrivermanager) Дадацьdriver(driver_2 IDriver) {
	idriver[нУМАРdriver] = driver_2
	нУМАРdriver++
}
func (self *TDrivermanager) ЗадзейнічацьУсе() {
	for i := 0; i < нУМАРdriver; i++ {
		idriver[i].Задзейнічаць()
	}
}
