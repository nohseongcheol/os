/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package wirtualnePamięć

import . "zwykły"

const (
	KernelvirtAdres		= 3 * Gb
	UżytkownikstackRozmiar	= 32 * Kb
	UżytkownikstackGóra	= 64 * Mbar
	Użytkownikstack		= UżytkownikstackGóra - UżytkownikstackRozmiar
)

func VirtPrzetestuj() {
	TypPrzetestuj()
}
