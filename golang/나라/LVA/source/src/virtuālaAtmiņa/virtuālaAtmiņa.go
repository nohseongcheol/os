/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
