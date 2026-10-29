/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Bật()
	Đặtlại() int
	Tắt()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var sỐdriver int

func (mình *TDrivermanager) Init() {
	sỐdriver = 0
}

func (mình *TDrivermanager) Thêmdriver(driver_2 IDriver) {
	idriver[sỐdriver] = driver_2
	sỐdriver++
}
func (mình *TDrivermanager) BậtTấtcả() {
	for i := 0; i < sỐdriver; i++ {
		idriver[i].Bật()
	}
}
