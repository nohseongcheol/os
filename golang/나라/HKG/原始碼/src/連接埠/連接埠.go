package 連接埠

var 位置 uint16 = 1

type T連接埠 struct {
	portnumber uint16
}

type T連接埠8bit struct {
	T連接埠
	讀取計數	uint16
	寫入計數	uint16
}

func (self *T連接埠8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.讀取計數 = 65
	self.寫入計數 = 65
}
func (self *T連接埠8bit) W寫入(資料 uint8) {
	P連接埠出位元組(self.portnumber, 資料)
}
func (self *T連接埠8bit) R讀取() uint8 {
	var 結果 = P連接埠進位元組(self.portnumber)
	return 結果
}
func P連接埠寫入位元組(portnumber uint16, 資料 uint8) {
	P連接埠出位元組(portnumber, 資料)
}
func P連接埠讀取位元組(portnumber uint16) uint8 {
	結果 := P連接埠進位元組(portnumber)
	return 結果
}

type T連接埠16bit struct {
	T連接埠
}

func (self *T連接埠16bit) Init(portnumber uint16) {
	self.T連接埠.portnumber = portnumber
}
func (self *T連接埠16bit) W寫入(資料 uint16) {
	P連接埠出字(self.T連接埠.portnumber, 資料)
}
func (self *T連接埠16bit) R讀取() uint16 {
	var 結果 = P連接埠進字(self.T連接埠.portnumber)
	return 結果
}
func P連接埠寫入字(portnumber uint16, 資料 uint16) {
	P連接埠出字(portnumber, 資料)
}
func P連接埠讀取字(portnumber uint16) uint16 {
	var 結果 uint16 = P連接埠進字(portnumber)
	return 結果
}

type T連接埠32bit struct {
	T連接埠
}

func (self *T連接埠32bit) Init(portnumber uint16) {
	self.T連接埠.portnumber = portnumber
}
func (self *T連接埠32bit) W寫入(資料 uint32) {
	P連接埠出dword(self.T連接埠.portnumber, 資料)
}
func (self *T連接埠32bit) R讀取() {
	P連接埠進dword(self.T連接埠.portnumber)
}
func P連接埠寫入dword(portnumber uint16, 資料 uint32) {
	P連接埠出dword(portnumber, 資料)
}
func P連接埠讀取dword(portnumber uint16) uint32 {
	var 結果 uint32 = P連接埠進dword(portnumber)
	return 結果
}

var 讀取計數 uint16 = 65
var 寫入計數 uint16 = 66

func P連接埠出位元組(portnumber uint16, 資料 uint8)
func P連接埠進位元組(portnumber uint16) uint8

func P連接埠出字(portnumber uint16, 資料 uint16)
func P連接埠進字(portnumber uint16) uint16

func P連接埠出dword(portnumber uint16, 資料 uint32)
func P連接埠進dword(portnumber uint16) uint32
