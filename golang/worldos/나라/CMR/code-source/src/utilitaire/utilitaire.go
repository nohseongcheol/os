/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package utilitaire

import . "console"
import . "unsafe"
import . "reflect"

var utilitaireconsole TConsole = TConsole{}

func Unsignedinteger16totableau(nombre_2 uint16) [2]byte {
	var tableau [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tableau[i] = byte(nombre_2 >> (8 * i) & 0x00FF)
	}
	return tableau
}
func Unsignedinteger16totableaube(nombre_2 uint16) [2]byte {
	var tableau [2]byte
	var i uint
	for i = 0; i < 2; i++ {
		tableau[2-i] = byte(nombre_2 >> (8 * i) & 0x00FF)
	}
	return tableau
}

func Unsignedinteger32totableau(nombre_2 uint32) [4]byte {
	var tableau [4]byte
	var i uint
	for i = 0; i < 4; i++ {
		tableau[i] = byte(nombre_2 >> (8 * i) & 0x000000FF)
	}
	return tableau
}
func Unsignedinteger48totableau(nombre_2 uint64) [6]byte {
	var tableau [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tableau[i] = byte(nombre_2 >> (8 * i) & 0x00000000FF)
	}
	return tableau
}
func Unsignedinteger48totableaube(nombre_2 uint64) [6]byte {
	var tableau [6]byte
	var i uint
	for i = 0; i < 6; i++ {
		tableau[5-i] = byte(nombre_2 >> (8 * i) & 0x00000000FF)
	}
	return tableau
}
func Unsignedinteger64totableau(nombre_2 uint64) [8]byte {
	var tableau [8]byte
	var i uint
	for i = 0; i < 4; i++ {
		tableau[1-i] = byte(nombre_2 >> (8 * i) & 0x00000000000000FF)
	}
	return tableau
}
func Tableautounsignedinteger16(tableau [2]byte) uint16 {
	var nombre_2 uint16
	var i uint
	for i = 0; i < 2; i++ {
		nombre_2 = nombre_2 | (uint16(tableau[1-i]) << (8 * i))
	}
	return nombre_2
}
func Tableautounsignedinteger32(tableau [4]byte) uint32 {
	var nombre_2 uint32
	var i uint
	for i = 0; i < 4; i++ {
		nombre_2 = nombre_2 | (uint32(tableau[3-i]) << (8 * i))
	}
	return nombre_2
}
func Tableautounsignedinteger48(tableau [6]byte) uint64 {
	var nombre_2 uint64
	var i uint
	for i = 0; i < 6; i++ {
		nombre_2 = nombre_2 | (uint64(tableau[5-i]) << (8 * i))
	}
	return nombre_2

}
func Tableautounsignedinteger48be(tableau [6]byte) uint64 {
	var nombre_2 uint64
	var i uint
	for i = 0; i < 6; i++ {
		nombre_2 = nombre_2 | (uint64(tableau[i]) << (8 * i))
	}
	return nombre_2
}
func Tableautounsignedinteger64(tableau [8]byte) uint64 {
	var nombre_2 uint64
	var i uint
	for i = 0; i < 8; i++ {
		nombre_2 = nombre_2 | (uint64(tableau[7-i]) << (8 * i))
	}
	return nombre_2
}
func Unsignedinteger64r(nombre_2 uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 8; i++ {
		temporary = temporary | (uint64(nombre_2>>(8*(7-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger48r(nombre_2 uint64) uint64 {
	var temporary uint64
	var i uint
	for i = 0; i < 6; i++ {
		temporary = temporary | (uint64(nombre_2>>(8*(5-i))&0x00000000000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger32r(nombre_2 uint32) uint32 {
	var temporary uint32
	var i uint
	for i = 0; i < 4; i++ {
		temporary = temporary | (uint32(nombre_2>>(8*(3-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func Unsignedinteger16r(nombre_2 uint16) uint16 {
	var temporary uint16
	var i uint
	for i = 0; i < 2; i++ {
		temporary = temporary | (uint16(nombre_2>>(8*(1-i))&0x000000FF) << (8 * i))
	}
	return temporary
}
func ImprimerOctets(donnéesPointeur uintptr, taille int) {
	var buffer_2 [4 * 1024]byte = *(*([4 * 1024]byte))(Pointer(donnéesPointeur))
	var i int
	utilitaireconsole.MImprimer([]byte("util["))
	for i = 0; i < taille; i++ {
		utilitaireconsole.MHexadecimalImprimer(buffer_2[i])
	}
	utilitaireconsole.MImprimer([]byte("]"))
}

func ImprimerTester(paramètres ...interface{}) {
	for _, param := range paramètres {
		utilitaireconsole.MImprimer([]byte(TypeOf(param).Name()))

	}
}
func ÉgalOctets(a, b []byte) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}
func OctetstoChaîne(b []byte) string {
	bh := (*SliceHeader)(Pointer(&b))
	sh := StringHeader{bh.Data, bh.Len}
	return *(*string)(Pointer(&sh))
}
func GetunsignedintegerPointeurtableaudePointeur(référence_mémoire_2 uintptr, len int, cap int) []uintptr {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{référence_mémoire_2, len, cap}
	return *(*[]uintptr)(Pointer(&sl))
}
func Getunsignedinteger32tableaudePointeur(référence_mémoire_2 uintptr, len int, cap int) []uint32 {
	len = len * 4
	cap = cap * 4
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{référence_mémoire_2, len, cap}
	return *(*[]uint32)(Pointer(&sl))
}

func GetOctetsdePointeur(référence_mémoire_2 uintptr, len int, cap int) []byte {
	var sl = struct {
		address	uintptr
		len	int
		cap	int
	}{référence_mémoire_2, len, cap}
	return *(*[]byte)(Pointer(&sl))
}

func GetfuncPointeurdePointeur(référence_mémoire_2 uintptr) func() {
	code1Pointeur_2 := uintptr(Pointer(&référence_mémoire_2))
	return *(*func())(Pointer(&code1Pointeur_2))
}
