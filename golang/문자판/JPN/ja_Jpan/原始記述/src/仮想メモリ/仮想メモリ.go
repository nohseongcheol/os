package 仮想メモリ

import . "共通"

const (
	K中核virtaddress	= 3 * Gb
	U利用者stackサイズ	= 32 * Kb
	U利用者stack上	= 64 * Mミリバール
	U利用者stack	= U利用者stack上 - U利用者stackサイズ
)

func Virtテスト() {
	T型テスト()
}
