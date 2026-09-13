package virtuālaAtmiņa

import . "kopējie"

const (
	Kernelvirtaddress	= 3 * Gb
	LietotājsstackIzmērs	= 32 * Kb
	LietotājsstackAugšā	= 64 * Mb
	Lietotājsstack		= LietotājsstackAugšā - LietotājsstackIzmērs
)

func VirtPārbaudīt() {
	TipsPārbaudīt()
}
