#include "../benennung/maschineBindenNamen.h"
#include "aufrufen.h"
extern int main(int,char **);
static char argumentDatenfeld[8][256];
int benutzerStarten(int unbenutzt){
    (void)unbenutzt;char *argumentListe[9];int argumenteAnzahl=benutzerAufrufen(15,UINTPTR_MAX,0,0,0,0,0);
    if(argumenteAnzahl<0||argumenteAnzahl>8)return 126;
    for(int ordnungszahlIndex=0;ordnungszahlIndex<argumenteAnzahl;ordnungszahlIndex++){if(benutzerAufrufen(15,ordnungszahlIndex,(uintptr_t)argumentDatenfeld[ordnungszahlIndex],256,0,0,0)<0)return 126;argumentListe[ordnungszahlIndex]=argumentDatenfeld[ordnungszahlIndex];}argumentListe[argumenteAnzahl]=0;
    return main(argumenteAnzahl,argumentListe);
}
void *memset(void*datenPosition,int zeichenKode,size_t elementeintragAnzahl){unsigned char*zielDaten=datenPosition;while(elementeintragAnzahl--)*zielDaten++=zeichenKode;return datenPosition;}
void *memcpy(void*zielDaten,const void*zeichenketteDaten,size_t elementeintragAnzahl){unsigned char*ersterWert=zielDaten;const unsigned char*zweiterWert=zeichenketteDaten;while(elementeintragAnzahl--)*ersterWert++=*zweiterWert++;return zielDaten;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned waagerechteKoordinateKoordinate,unsigned senkrechteKoordinateKoordinate,unsigned breiteWert,unsigned höheWert,unsigned bildpunktFarbe){return bildschirmRechteck(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,breiteWert,höheWert,bildpunktFarbe);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return benutzerAufrufen(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return fürBildschirmTasteWarten();}
int rechteckZeichnen(unsigned waagerechtPosition,unsigned senkrechtPosition,unsigned breiteWert,unsigned höheWert,unsigned bildpunktFarbe){return pk_rectangle(waagerechtPosition,senkrechtPosition,breiteWert,höheWert,bildpunktFarbe);}
unsigned millisekunden(void){return pk_ticks_ms();}
int fürZeichnungWarten(void){return pk_graphics_wait();}
int bildschirmBreite(void){return bildschirmBreiteLesen();}
int bildschirmHöhe(void){return bildschirmHöheLesen();}
