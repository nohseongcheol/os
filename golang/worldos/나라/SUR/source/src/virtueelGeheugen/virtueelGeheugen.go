/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
