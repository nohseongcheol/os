/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aგააქტიურება()
	Rგანულება() int
	Dდეაქტივაცია()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var რიცხვიdriver int

func (self *TDrivermanager) Init() {
	რიცხვიdriver = 0
}

func (self *TDrivermanager) Aდამატებაdriver(driver_2 IDriver) {
	idriver[რიცხვიdriver] = driver_2
	რიცხვიdriver++
}
func (self *TDrivermanager) Aგააქტიურებაყველა() {
	for i := 0; i < რიცხვიdriver; i++ {
		idriver[i].Aგააქტიურება()
	}
}
