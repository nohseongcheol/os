/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtualiAtmintis

import . "bendrinis"

const (
	Kernelvirtaddress	= 3 * Gb
	NaudotojasstackDydis	= 32 * Kb
	NaudotojasstackViršuje	= 64 * Mb
	Naudotojasstack		= NaudotojasstackViršuje - NaudotojasstackDydis
)

func VirtTestas() {
	TipasTestas()
}
