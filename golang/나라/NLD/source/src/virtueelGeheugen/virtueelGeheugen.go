package virtueelGeheugen

import . "veelvoorkomend"

const (
	Kernelvirtaddress	= 3 * Gb
	GebruikerstackGrootte	= 32 * Kb
	GebruikerstackBovenaan	= 64 * Mb
	Gebruikerstack		= GebruikerstackBovenaan - GebruikerstackGrootte
)

func VirtProef() {
	SoortProef()
}
