#include "../benennung/maschineBindenNamen.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Netzwerkstapel.h"
extern int32_t javaRücklaufnetzNetzbuchse(int32_t,int32_t,int32_t), javaRücklaufnetzZuordnen(int32_t,int32_t,int32_t);
extern int32_t javaRücklaufnetzSenden(int32_t,int32_t,int32_t,int32_t), javaRücklaufnetzEmpfangsvorgang(int32_t,int32_t);
extern int32_t javaRücklaufnetzPort(int32_t), javaRücklaufnetzAdresse(int32_t), javaRücklaufnetzGegenstelle(int32_t), javaRücklaufnetzSchließen(int32_t);
extern int32_t javaNetzAblegen(int32_t,int32_t),javaNetzHolen(int32_t);
extern int32_t javaRücklaufstromErstellen(void),javaRücklaufstromZuordnen(int32_t,int32_t,int32_t),javaRücklaufstromLauschen(int32_t,int32_t);
extern int32_t javaRücklaufstromVerbinden(int32_t,int32_t,int32_t),javaRücklaufstromAnnehmen(int32_t),javaRücklaufstromLesen(int32_t,int32_t),javaRücklaufstromSchreiben(int32_t,int32_t);
extern int32_t javaRücklaufstromPort(int32_t),javaRücklaufstromGegenstelle(int32_t),javaRücklaufstromSchließen(int32_t);
static int externeBindung[24];
static int beliebigAdresse[24], doppeltLauscher[24], uDPExternGegenstelle[8], gebundenAdresse[8];
static int externNummer(int dateiKennwert) { return dateiKennwert>=32 && dateiKennwert<56 ? externeBindung[dateiKennwert-32]-1 : -1; }
static int einsetzenText(int dateiKennwert,int typKategorie) {
    if(dateiKennwert<32||dateiKennwert>=56)return -9;int vorherigElementeintrag=externNummer(dateiKennwert);if(vorherigElementeintrag>=0)return vorherigElementeintrag;
    int elementeintragAnzahl=netzbuchseEndpunktErstellen(typKategorie);if(elementeintragAnzahl>=0)externeBindung[dateiKennwert-32]=elementeintragAnzahl+1;return elementeintragAnzahl;
}
int32_t javaNetzNetzbuchse(int32_t ersterWert,int32_t zweiterWert,int32_t zeichenKode){return javaRücklaufnetzNetzbuchse(ersterWert,zweiterWert,zeichenKode);}
int32_t javaNetzZuordnen(int32_t dateiKennwert,int32_t InternetAdresse,int32_t portNummer){
    if(InternetAdresse==0x7f000001)return javaRücklaufnetzZuordnen(dateiKennwert,InternetAdresse,portNummer);
    if(InternetAdresse!=0&&InternetAdresse!=netzwerkZustandLesen(0,0))return -99;
    int zurückgegebenWert=javaRücklaufnetzZuordnen(dateiKennwert,0,portNummer);if(zurückgegebenWert<0)return zurückgegebenWert;
    int elementeintragAnzahl=einsetzenText(dateiKennwert,2);if(elementeintragAnzahl<0)return elementeintragAnzahl;zurückgegebenWert=netzZuordnen(elementeintragAnzahl,netzwerkZustandLesen(0,0),javaRücklaufnetzPort(dateiKennwert));if(!zurückgegebenWert)gebundenAdresse[dateiKennwert-32]=InternetAdresse;return zurückgegebenWert;
}
int32_t javaNetzSenden(int32_t dateiKennwert,int32_t InternetAdresse,int32_t portNummer,int32_t größe){
    if(InternetAdresse==0x7f000001)return javaRücklaufnetzSenden(dateiKennwert,InternetAdresse,portNummer,größe);
    if(größe<0||größe>512)return -90;if(portNummer<1||portNummer>65535)return -22;
    if(javaRücklaufnetzPort(dateiKennwert)<0)return -9;
    if(javaRücklaufnetzAdresse(dateiKennwert)==0x7f000001)return -101;
    int elementeintragAnzahl=externNummer(dateiKennwert);if(elementeintragAnzahl<0){int zurückgegebenWert=0;if(javaRücklaufnetzPort(dateiKennwert)==0)zurückgegebenWert=javaRücklaufnetzZuordnen(dateiKennwert,0,0);if(zurückgegebenWert<0)return zurückgegebenWert;elementeintragAnzahl=einsetzenText(dateiKennwert,2);if(elementeintragAnzahl<0)return elementeintragAnzahl;zurückgegebenWert=netzZuordnen(elementeintragAnzahl,netzwerkZustandLesen(0,0),javaRücklaufnetzPort(dateiKennwert));if(zurückgegebenWert<0)return zurückgegebenWert;}
    unsigned char Daten[512];for(int ordnungszahlIndex=0;ordnungszahlIndex<größe;ordnungszahlIndex++)Daten[ordnungszahlIndex]=javaNetzHolen(ordnungszahlIndex);return datagrammSenden(elementeintragAnzahl,Daten,größe,InternetAdresse,portNummer);
}
int32_t javaNetzEmpfangsvorgang(int32_t dateiKennwert,int32_t größe){
    int elementeintragAnzahl=externNummer(dateiKennwert);if(elementeintragAnzahl<0)return javaRücklaufnetzEmpfangsvorgang(dateiKennwert,größe);if(größe<0||größe>512)return -22;
    int lokal=javaRücklaufnetzEmpfangsvorgang(dateiKennwert,größe);if(lokal!=-11){uDPExternGegenstelle[dateiKennwert-32]=0;return lokal;}
    unsigned char Daten[512];int zurückgegebenWert=datagrammEmpfangen(elementeintragAnzahl,Daten,größe);if(zurückgegebenWert>=0)uDPExternGegenstelle[dateiKennwert-32]=1;for(int ordnungszahlIndex=0;ordnungszahlIndex<zurückgegebenWert;ordnungszahlIndex++)javaNetzAblegen(ordnungszahlIndex,Daten[ordnungszahlIndex]);return zurückgegebenWert;
}
int32_t javaNetzPort(int32_t dateiKennwert){int elementeintragAnzahl=externNummer(dateiKennwert);return elementeintragAnzahl<0?javaRücklaufnetzPort(dateiKennwert):(int32_t)netzwerkPortNummer(elementeintragAnzahl);}
int32_t javaNetzAdresse(int32_t dateiKennwert){return externNummer(dateiKennwert)<0?javaRücklaufnetzAdresse(dateiKennwert):gebundenAdresse[dateiKennwert-32];}
int32_t javaNetzGegenstelle(int32_t dateiKennwert){int elementeintragAnzahl=externNummer(dateiKennwert);return elementeintragAnzahl<0||!uDPExternGegenstelle[dateiKennwert-32]?javaRücklaufnetzGegenstelle(dateiKennwert):(int32_t)gegenstellePortNummer(elementeintragAnzahl);}
int32_t javaNetzEntfernt(int32_t dateiKennwert){int elementeintragAnzahl=externNummer(dateiKennwert);return elementeintragAnzahl<0||!uDPExternGegenstelle[dateiKennwert-32]?0x7f000001:(int32_t)netzGegenstelleAdresse(elementeintragAnzahl);}
int32_t javaNetzSchließen(int32_t dateiKennwert){int elementeintragAnzahl=externNummer(dateiKennwert);if(elementeintragAnzahl>=0){netzwerkSchließen(elementeintragAnzahl);externeBindung[dateiKennwert-32]=0;}if(dateiKennwert>=32&&dateiKennwert<40)uDPExternGegenstelle[dateiKennwert-32]=gebundenAdresse[dateiKennwert-32]=0;return javaRücklaufnetzSchließen(dateiKennwert);}
int32_t javaDatenstromErstellen(void){return javaRücklaufstromErstellen();}
int32_t javaDatenstromZuordnen(int32_t dateiKennwert,int32_t InternetAdresse,int32_t portNummer){
    if(InternetAdresse==0||InternetAdresse==0x7f000001){int zurückgegebenWert=javaRücklaufstromZuordnen(dateiKennwert,InternetAdresse,portNummer);if(!zurückgegebenWert)beliebigAdresse[dateiKennwert-32]=InternetAdresse==0;return zurückgegebenWert;}
    if(InternetAdresse!=netzwerkZustandLesen(0,0))return -99;int zurückgegebenWert=javaRücklaufstromZuordnen(dateiKennwert,0,portNummer);if(zurückgegebenWert<0)return zurückgegebenWert;
    int elementeintragAnzahl=einsetzenText(dateiKennwert,1);return elementeintragAnzahl<0?elementeintragAnzahl:netzZuordnen(elementeintragAnzahl,InternetAdresse,javaRücklaufstromPort(dateiKennwert));
}
int32_t javaDatenstromLauschen(int32_t dateiKennwert,int32_t wartebestand){
    int elementeintragAnzahl=externNummer(dateiKennwert);if(elementeintragAnzahl<0){int zurückgegebenWert=javaRücklaufstromLauschen(dateiKennwert,wartebestand);if(zurückgegebenWert<0||!beliebigAdresse[dateiKennwert-32])return zurückgegebenWert;
        elementeintragAnzahl=einsetzenText(dateiKennwert,1);if(elementeintragAnzahl<0)return elementeintragAnzahl;zurückgegebenWert=netzZuordnen(elementeintragAnzahl,netzwerkZustandLesen(0,0),javaRücklaufstromPort(dateiKennwert));if(zurückgegebenWert<0)return zurückgegebenWert;doppeltLauscher[dateiKennwert-32]=1;
    }return wartebestand<1?-22:netzLauschen(elementeintragAnzahl);
}
int32_t javaDatenstromVerbinden(int32_t dateiKennwert,int32_t InternetAdresse,int32_t portNummer){
    if(InternetAdresse==0x7f000001 && externNummer(dateiKennwert)<0)return javaRücklaufstromVerbinden(dateiKennwert,InternetAdresse,portNummer);
    if(javaRücklaufstromPort(dateiKennwert)<0)return -9;int elementeintragAnzahl=einsetzenText(dateiKennwert,1);return elementeintragAnzahl<0?elementeintragAnzahl:netzVerbinden(elementeintragAnzahl,InternetAdresse,portNummer);
}
int32_t javaDatenstromAnnehmen(int32_t dateiKennwert){
    int elementeintragAnzahl=externNummer(dateiKennwert);if(elementeintragAnzahl<0)return javaRücklaufstromAnnehmen(dateiKennwert);
    if(doppeltLauscher[dateiKennwert-32]){int lokal=javaRücklaufstromAnnehmen(dateiKennwert);if(lokal!=-11)return lokal;}
    int gegenstelleWert=netzAnnehmen(elementeintragAnzahl);if(gegenstelleWert<0)return gegenstelleWert;
    int zielobjektWert=javaRücklaufstromErstellen();if(zielobjektWert<0){netzwerkSchließen(gegenstelleWert);return zielobjektWert;}externeBindung[zielobjektWert-32]=gegenstelleWert+1;return zielobjektWert;
}
int32_t javaDatenstromLesen(int32_t dateiKennwert,int32_t größe){
    int elementeintragAnzahl=externNummer(dateiKennwert);if(elementeintragAnzahl<0)return javaRücklaufstromLesen(dateiKennwert,größe);if(größe<0||größe>512)return -22;
    unsigned char Daten[512];int zurückgegebenWert=netzLesen(elementeintragAnzahl,Daten,größe);for(int ordnungszahlIndex=0;ordnungszahlIndex<zurückgegebenWert;ordnungszahlIndex++)javaNetzAblegen(ordnungszahlIndex,Daten[ordnungszahlIndex]);return zurückgegebenWert;
}
int32_t javaDatenstromSchreiben(int32_t dateiKennwert,int32_t größe){
    int elementeintragAnzahl=externNummer(dateiKennwert);if(elementeintragAnzahl<0)return javaRücklaufstromSchreiben(dateiKennwert,größe);if(größe<0||größe>512)return -22;
    unsigned char Daten[512];for(int ordnungszahlIndex=0;ordnungszahlIndex<größe;ordnungszahlIndex++)Daten[ordnungszahlIndex]=javaNetzHolen(ordnungszahlIndex);return netzSchreiben(elementeintragAnzahl,Daten,größe);
}
int32_t javaDatenstromPort(int32_t dateiKennwert){int elementeintragAnzahl=externNummer(dateiKennwert);return elementeintragAnzahl<0?javaRücklaufstromPort(dateiKennwert):(int32_t)netzwerkPortNummer(elementeintragAnzahl);}
int32_t javaDatenstromGegenstelle(int32_t dateiKennwert){int elementeintragAnzahl=externNummer(dateiKennwert);return elementeintragAnzahl<0?javaRücklaufstromGegenstelle(dateiKennwert):(int32_t)gegenstellePortNummer(elementeintragAnzahl);}
int32_t javaDatenstromAdresse(int32_t dateiKennwert){return externNummer(dateiKennwert)<0?0x7f000001:doppeltLauscher[dateiKennwert-32]?0:netzwerkZustandLesen(0,0);}
int32_t javaDatenstromSchließen(int32_t dateiKennwert){int elementeintragAnzahl=externNummer(dateiKennwert);if(elementeintragAnzahl>=0){netzwerkSchließen(elementeintragAnzahl);externeBindung[dateiKennwert-32]=0;}if(dateiKennwert>=40&&dateiKennwert<56)beliebigAdresse[dateiKennwert-32]=doppeltLauscher[dateiKennwert-32]=0;return javaRücklaufstromSchließen(dateiKennwert);}
