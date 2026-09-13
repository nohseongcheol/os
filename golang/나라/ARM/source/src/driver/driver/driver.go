package driver

type IDriver interface {
	Ակտիվացնել()
	Դադարեցնել() int
	Ապաակտիվացնել()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var հԱՄԱՐdriver int

func (ինքնուրույն *TDrivermanager) Init() {
	հԱՄԱՐdriver = 0
}

func (ինքնուրույն *TDrivermanager) Ավելացնելdriver(driver_2 IDriver) {
	idriver[հԱՄԱՐdriver] = driver_2
	հԱՄԱՐdriver++
}
func (ինքնուրույն *TDrivermanager) ԱկտիվացնելԲոլորը() {
	for i := 0; i < հԱՄԱՐdriver; i++ {
		idriver[i].Ակտիվացնել()
	}
}
