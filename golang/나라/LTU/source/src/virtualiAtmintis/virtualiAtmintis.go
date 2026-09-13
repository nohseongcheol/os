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
