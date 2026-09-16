/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
