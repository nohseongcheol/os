/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Omogoči()
	Ponastavi() int
	Onemogoči()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var številkadriver int

func (sam *TDrivermanager) Init() {
	številkadriver = 0
}

func (sam *TDrivermanager) Dodajdriver(driver_2 IDriver) {
	idriver[številkadriver] = driver_2
	številkadriver++
}
func (sam *TDrivermanager) OmogočiVse() {
	for i := 0; i < številkadriver; i++ {
		idriver[i].Omogoči()
	}
}
