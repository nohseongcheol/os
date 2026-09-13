package virtualmemory

import . "умумӣ"

const (
	Kernelvirtaddress		= 3 * Gb
	Истифодакунандаstacksize	= 32 * Kb
	ИстифодакунандаstackБоло	= 64 * Mb
	Истифодакунандаstack		= ИстифодакунандаstackБоло - Истифодакунандаstacksize
)

func Virttest() {
	Typetest()
}
