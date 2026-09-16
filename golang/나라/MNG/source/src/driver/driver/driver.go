/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Идэвхжүүлэх()
	Суллах() int
	Идэвхигүйжүүлэх()
}

type TDriverЗохицуулагч struct {
}

var idriver [256]IDriver
var numberdriver int

func (self *TDriverЗохицуулагч) Init() {
	numberdriver = 0
}

func (self *TDriverЗохицуулагч) Нэмэхdriver(driver_2 IDriver) {
	idriver[numberdriver] = driver_2
	numberdriver++
}
func (self *TDriverЗохицуулагч) ИдэвхжүүлэхБүх() {
	for i := 0; i < numberdriver; i++ {
		idriver[i].Идэвхжүүлэх()
	}
}
