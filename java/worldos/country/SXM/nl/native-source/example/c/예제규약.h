#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int tekstlengte_in_bytes(const char *tekst) { int tijdsduur_WAARDE=0;while(tekst[tijdsduur_WAARDE])tijdsduur_WAARDE++;return tijdsduur_WAARDE; }
static int tekstuitvoer(const char *tekst) { int tijdsduur_WAARDE=tekstlengte_in_bytes(tekst);return schrijven_Bestand_gegevens(1,tekst,tijdsduur_WAARDE)==tijdsduur_WAARDE?0:1; }
#endif
