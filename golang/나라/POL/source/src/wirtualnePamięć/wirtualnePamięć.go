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
