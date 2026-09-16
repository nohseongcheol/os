/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package virtuelmémoire

import . "commun"

const (
	Noyauvirtaddress	= 3 * Go
	UtilisateurstackTaille	= 32 * Ko
	UtilisateurstackHaut	= 64 * Mo
	Utilisateurstack	= UtilisateurstackHaut - UtilisateurstackTaille
)

func VirtTester() {
	TypeTester()
}
