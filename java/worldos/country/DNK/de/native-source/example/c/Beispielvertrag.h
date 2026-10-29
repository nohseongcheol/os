#ifndef SystemnahBeispielKopf
#define SystemnahBeispielKopf
#include <DateiABI.h>
#include <BildschirmABI.h>
static int textLänge(const char *Text) { int Länge=0;while(Text[Länge])Länge++;return Länge; }
static int Ausgabe(const char *Text) { int Länge=textLänge(Text);return dateiDatenSchreiben(1,Text,Länge)==Länge?0:1; }
#endif
