package ポート

var 配置 uint16 = 1

type Tポート struct {
	portnumber uint16
}

type Tポート8bit struct {
	Tポート
	読込みカウント	uint16
	書込みカウント	uint16
}

func (self *Tポート8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.読込みカウント = 65
	self.書込みカウント = 65
}
func (self *Tポート8bit) W書込み(データ uint8) {
	Pポート送信バイト(self.portnumber, データ)
}
func (self *Tポート8bit) R読込み() uint8 {
	var 生成先 = Pポート受信バイト(self.portnumber)
	return 生成先
}
func Pポート書込みバイト(portnumber uint16, データ uint8) {
	Pポート送信バイト(portnumber, データ)
}
func Pポート読込みバイト(portnumber uint16) uint8 {
	生成先 := Pポート受信バイト(portnumber)
	return 生成先
}

type Tポート16bit struct {
	Tポート
}

func (self *Tポート16bit) Init(portnumber uint16) {
	self.Tポート.portnumber = portnumber
}
func (self *Tポート16bit) W書込み(データ uint16) {
	Pポート送信語(self.Tポート.portnumber, データ)
}
func (self *Tポート16bit) R読込み() uint16 {
	var 生成先 = Pポート受信語(self.Tポート.portnumber)
	return 生成先
}
func Pポート書込み語(portnumber uint16, データ uint16) {
	Pポート送信語(portnumber, データ)
}
func Pポート読込み語(portnumber uint16) uint16 {
	var 生成先 uint16 = Pポート受信語(portnumber)
	return 生成先
}

type Tポート32bit struct {
	Tポート
}

func (self *Tポート32bit) Init(portnumber uint16) {
	self.Tポート.portnumber = portnumber
}
func (self *Tポート32bit) W書込み(データ uint32) {
	Pポート送信dword(self.Tポート.portnumber, データ)
}
func (self *Tポート32bit) R読込み() {
	Pポート受信dword(self.Tポート.portnumber)
}
func Pポート書込みdword(portnumber uint16, データ uint32) {
	Pポート送信dword(portnumber, データ)
}
func Pポート読込みdword(portnumber uint16) uint32 {
	var 生成先 uint32 = Pポート受信dword(portnumber)
	return 生成先
}

var 読込みカウント uint16 = 65
var 書込みカウント uint16 = 66

func Pポート送信バイト(portnumber uint16, データ uint8)
func Pポート受信バイト(portnumber uint16) uint8

func Pポート送信語(portnumber uint16, データ uint16)
func Pポート受信語(portnumber uint16) uint16

func Pポート送信dword(portnumber uint16, データ uint32)
func Pポート受信dword(portnumber uint16) uint32
