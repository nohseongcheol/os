/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ポート

var ハイチ uint16 = 1

type Tポート struct {
	portnumber uint16
}

type Tポート8bit struct {
	Tポート
	ヨミコミカウント	uint16
	カキコミカウント	uint16
}

func (self *Tポート8bit) Init(portnumber uint16) {
	self.portnumber = portnumber
	self.ヨミコミカウント = 65
	self.カキコミカウント = 65
}
func (self *Tポート8bit) Wカキコミ(データ uint8) {
	Pポートソウシンバイト(self.portnumber, データ)
}
func (self *Tポート8bit) Rヨミコミ() uint8 {
	var セイセイサキ = Pポートジュシンバイト(self.portnumber)
	return セイセイサキ
}
func Pポートカキコミバイト(portnumber uint16, データ uint8) {
	Pポートソウシンバイト(portnumber, データ)
}
func Pポートヨミコミバイト(portnumber uint16) uint8 {
	セイセイサキ := Pポートジュシンバイト(portnumber)
	return セイセイサキ
}

type Tポート16bit struct {
	Tポート
}

func (self *Tポート16bit) Init(portnumber uint16) {
	self.Tポート.portnumber = portnumber
}
func (self *Tポート16bit) Wカキコミ(データ uint16) {
	Pポートソウシンゴ(self.Tポート.portnumber, データ)
}
func (self *Tポート16bit) Rヨミコミ() uint16 {
	var セイセイサキ = Pポートジュシンゴ(self.Tポート.portnumber)
	return セイセイサキ
}
func Pポートカキコミゴ(portnumber uint16, データ uint16) {
	Pポートソウシンゴ(portnumber, データ)
}
func Pポートヨミコミゴ(portnumber uint16) uint16 {
	var セイセイサキ uint16 = Pポートジュシンゴ(portnumber)
	return セイセイサキ
}

type Tポート32bit struct {
	Tポート
}

func (self *Tポート32bit) Init(portnumber uint16) {
	self.Tポート.portnumber = portnumber
}
func (self *Tポート32bit) Wカキコミ(データ uint32) {
	Pポートソウシンdword(self.Tポート.portnumber, データ)
}
func (self *Tポート32bit) Rヨミコミ() {
	Pポートジュシンdword(self.Tポート.portnumber)
}
func Pポートカキコミdword(portnumber uint16, データ uint32) {
	Pポートソウシンdword(portnumber, データ)
}
func Pポートヨミコミdword(portnumber uint16) uint32 {
	var セイセイサキ uint32 = Pポートジュシンdword(portnumber)
	return セイセイサキ
}

var ヨミコミカウント uint16 = 65
var カキコミカウント uint16 = 66

func Pポートソウシンバイト(portnumber uint16, データ uint8)
func Pポートジュシンバイト(portnumber uint16) uint8

func Pポートソウシンゴ(portnumber uint16, データ uint16)
func Pポートジュシンゴ(portnumber uint16) uint16

func Pポートソウシンdword(portnumber uint16, データ uint32)
func Pポートジュシンdword(portnumber uint16) uint32
