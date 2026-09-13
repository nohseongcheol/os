package 虛擬記憶體

import . "通用"

const (
	K核心virtaddress	= 3 * Gb
	U使用者stack大小	= 32 * K千位元KB
	U使用者stack上	= 64 * M毫巴
	U使用者stack	= U使用者stack上 - U使用者stack大小
)

func Virt測試() {
	T類型測試()
}
