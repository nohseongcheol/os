package virtuellSpeicher

import . "gemeinsam"

const (
	Kernvirtaddress		= 3 * Gb
	BenutzerstackGröße	= 32 * Kbit
	BenutzerstackOben	= 64 * Mbar
	Benutzerstack		= BenutzerstackOben - BenutzerstackGröße
)

func VirtTesten() {
	TypTesten()
}
