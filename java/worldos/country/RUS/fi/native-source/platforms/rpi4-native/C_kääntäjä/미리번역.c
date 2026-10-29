#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "nippu.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned kesto_ARVO,nykyinen_toimi;static int tietojärjestelmät_pätemätön;
static unsigned Luokat_luettelo[512],첫째값[512],SEKUNNIT_ARVO[512],vakio_pooli,nykyinen_Luokka;
static char teksti[65536];static unsigned Tekstin_koko;
typedef struct {unsigned määritys_Background_Intelligent_Transfer_Service,Nimi,서술값,käsky_JONO,Koko,지역변수들,pinomuisti;} menetelmä_merkintä;
static menetelmä_merkintä 메소드목록[64];static unsigned 메소드개수;
static unsigned kentän_nimi[64],필드서술[64],kenttä_vakio[64],필드개수;
static unsigned OTA_ARVO(unsigned kohde_LASKE){if(nykyinen_toimi>kesto_ARVO||kohde_LASKE>kesto_ARVO-nykyinen_toimi){tietojärjestelmät_pätemätön=1;return 0;}unsigned data_toimi=nykyinen_toimi;nykyinen_toimi+=kohde_LASKE;return data_toimi;}
static unsigned tavu_data(void){unsigned data_toimi=OTA_ARVO(1);return tietojärjestelmät_pätemätön?0:data[data_toimi];}
static unsigned 절반값(void){unsigned x_koordinaatti=tavu_data();return x_koordinaatti<<8|tavu_data();}
static uint32_t 가득참(void){uint32_t x_koordinaatti=절반값();return x_koordinaatti<<16|절반값();}
static int UNICODE_ARVO(unsigned 순번,const char*merkkijono_data){return 순번>0&&순번<vakio_pooli&&Luokat_luettelo[순번]==1&&strlen(merkkijono_data)==SEKUNNIT_ARVO[순번]&&!memcmp(data+첫째값[순번],merkkijono_data,SEKUNNIT_ARVO[순번]);}
static int 같음(unsigned x_koordinaatti,unsigned Y_koordinaatti){return x_koordinaatti>0&&x_koordinaatti<vakio_pooli&&Y_koordinaatti>0&&Y_koordinaatti<vakio_pooli&&Luokat_luettelo[x_koordinaatti]==1&&Luokat_luettelo[Y_koordinaatti]==1&&SEKUNNIT_ARVO[x_koordinaatti]==SEKUNNIT_ARVO[Y_koordinaatti]&&!memcmp(data+첫째값[x_koordinaatti],data+첫째값[Y_koordinaatti],SEKUNNIT_ARVO[x_koordinaatti]);}
static void 내보내기(const char*Tiedosto_merkintä,...){if(tietojärjestelmät_pätemätön)return;va_list argumentti_MATRIISI;va_start(argumentti_MATRIISI,Tiedosto_merkintä);int kohde_LASKE=vsnprintf(teksti+Tekstin_koko,sizeof(teksti)-Tekstin_koko,Tiedosto_merkintä,argumentti_MATRIISI);va_end(argumentti_MATRIISI);if(kohde_LASKE<0||(unsigned)kohde_LASKE>=sizeof(teksti)-Tekstin_koko){tietojärjestelmät_pätemätön=1;return;}Tekstin_koko+=kohde_LASKE;}
static int 서술자(unsigned tunniste_ARVO,int*TULOS){
    if(tunniste_ARVO<1||tunniste_ARVO>=vakio_pooli||Luokat_luettelo[tunniste_ARVO]!=1)return -1;unsigned data_toimi=첫째값[tunniste_ARVO],lopettaa_puhelu_SIIRTYMÄ=data_toimi+SEKUNNIT_ARVO[tunniste_ARVO];if(data_toimi>=lopettaa_puhelu_SIIRTYMÄ||data[data_toimi++]!='(')return -1;int merkintä_LASKE=0;
    while(data_toimi<lopettaa_puhelu_SIIRTYMÄ&&data[data_toimi]!=')'){
        unsigned merkkikoodi=data[data_toimi++];while(merkkikoodi=='['&&data_toimi<lopettaa_puhelu_SIIRTYMÄ)merkkikoodi=data[data_toimi++];
        if(merkkikoodi=='L'){while(data_toimi<lopettaa_puhelu_SIIRTYMÄ&&data[data_toimi]!=';')data_toimi++;if(data_toimi==lopettaa_puhelu_SIIRTYMÄ)return -1;data_toimi++;}
        else if(merkkikoodi!='I'&&merkkikoodi!='Z'&&merkkikoodi!='B'&&merkkikoodi!='C'&&merkkikoodi!='S')return -1;
        if(++merkintä_LASKE>16)return -1;
    }
    if(data_toimi+1>=lopettaa_puhelu_SIIRTYMÄ||data[data_toimi++]!=')')return -1;*TULOS=data[data_toimi]=='V'?0:1;
    if(data[data_toimi]=='J'||data[data_toimi]=='D'||data[data_toimi]=='F')return -1;return merkintä_LASKE;
}
static void määritteet(void){unsigned kohde_LASKE=절반값();for(unsigned 순번=0;순번<kohde_LASKE&&!tietojärjestelmät_pätemätön;순번++){절반값();unsigned Koko=가득참();OTA_ARVO(Koko);}}
static int jäsentää_syöte(void){
    if(가득참()!=0xcafebabe)return -1;unsigned aliversio=절반값(),versionumero=절반값();if(aliversio||versionumero<45||versionumero>52)return -1;
    vakio_pooli=절반값();if(vakio_pooli<1||vakio_pooli>512)return -1;
    for(unsigned 순번=1;순번<vakio_pooli&&!tietojärjestelmät_pätemätön;순번++){
        Luokat_luettelo[순번]=tavu_data();switch(Luokat_luettelo[순번]){
        case 1:SEKUNNIT_ARVO[순번]=절반값();첫째값[순번]=OTA_ARVO(SEKUNNIT_ARVO[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:OTA_ARVO(8);if(++순번>=vakio_pooli)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEKUNNIT_ARVO[순번]=절반값();break;
        case 15:첫째값[순번]=tavu_data();SEKUNNIT_ARVO[순번]=절반값();break;default:return -1;
        }
    }
    절반값();nykyinen_Luokka=절반값();절반값();if(nykyinen_Luokka<1||nykyinen_Luokka>=vakio_pooli||Luokat_luettelo[nykyinen_Luokka]!=7||첫째값[nykyinen_Luokka]<1||첫째값[nykyinen_Luokka]>=vakio_pooli||Luokat_luettelo[첫째값[nykyinen_Luokka]]!=1)return -1;unsigned 인터페이스목록=절반값();OTA_ARVO(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!tietojärjestelmät_pätemätön;순번++){
        unsigned määritys_Background_Intelligent_Transfer_Service=절반값();kentän_nimi[순번]=절반값();필드서술[순번]=절반값();
        if(!(määritys_Background_Intelligent_Transfer_Service&8))return -1;
        unsigned merkintä_LASKE=절반값();for(unsigned 안쪽순번=0;안쪽순번<merkintä_LASKE&&!tietojärjestelmät_pätemätön;안쪽순번++){
            unsigned Nimi=절반값(),Koko=가득참();
            if(UNICODE_ARVO(Nimi,"ConstantValue")){if(Koko!=2)return -1;kenttä_vakio[순번]=절반값();}
            else OTA_ARVO(Koko);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!tietojärjestelmät_pätemätön;순번++){
        menetelmä_merkintä*Ryhmä_muuttaa_kokoa=메소드목록+순번;Ryhmä_muuttaa_kokoa->määritys_Background_Intelligent_Transfer_Service=절반값();Ryhmä_muuttaa_kokoa->Nimi=절반값();Ryhmä_muuttaa_kokoa->서술값=절반값();unsigned merkintä_LASKE=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<merkintä_LASKE&&!tietojärjestelmät_pätemätön;안쪽순번++){
            unsigned Nimi=절반값(),Koko=가득참(),Suorita_2=nykyinen_toimi;
            if(Koko>kesto_ARVO-nykyinen_toimi)return -1;
            if(UNICODE_ARVO(Nimi,"Code")){
                Ryhmä_muuttaa_kokoa->pinomuisti=절반값();Ryhmä_muuttaa_kokoa->지역변수들=절반값();Ryhmä_muuttaa_kokoa->Koko=가득참();Ryhmä_muuttaa_kokoa->käsky_JONO=OTA_ARVO(Ryhmä_muuttaa_kokoa->Koko);
                if(Ryhmä_muuttaa_kokoa->pinomuisti>128||Ryhmä_muuttaa_kokoa->지역변수들>128||Ryhmä_muuttaa_kokoa->Koko>8192||절반값())return -1;määritteet();
            }else OTA_ARVO(Koko);
            if(nykyinen_toimi!=Suorita_2+Koko)return -1;
        }
        if(!UNICODE_ARVO(Ryhmä_muuttaa_kokoa->Nimi,"<init>")&&(!(Ryhmä_muuttaa_kokoa->määritys_Background_Intelligent_Transfer_Service&8)||(Ryhmä_muuttaa_kokoa->määritys_Background_Intelligent_Transfer_Service&(0x100|0x20))||!Ryhmä_muuttaa_kokoa->Koko))return -1;
    }
    määritteet();return tietojärjestelmät_pätemätön||nykyinen_toimi!=kesto_ARVO?-1:0;
}
static void vakio_ARVO(unsigned tunniste_ARVO){
    if(!tunniste_ARVO||tunniste_ARVO>=vakio_pooli){tietojärjestelmät_pätemätön=1;return;}
    if(Luokat_luettelo[tunniste_ARVO]==3)내보내기("P(%uU);",첫째값[tunniste_ARVO]);
    else if(Luokat_luettelo[tunniste_ARVO]==8)내보내기("P((W)k%u);",tunniste_ARVO);else tietojärjestelmät_pätemätön=1;
}
static void 호출(unsigned tunniste_ARVO,int virtuaalinen_KUTSU){
    if(tunniste_ARVO<1||tunniste_ARVO>=vakio_pooli||(Luokat_luettelo[tunniste_ARVO]!=10&&Luokat_luettelo[tunniste_ARVO]!=11)||첫째값[tunniste_ARVO]<1||첫째값[tunniste_ARVO]>=vakio_pooli||Luokat_luettelo[첫째값[tunniste_ARVO]]!=7||SEKUNNIT_ARVO[tunniste_ARVO]<1||SEKUNNIT_ARVO[tunniste_ARVO]>=vakio_pooli||Luokat_luettelo[SEKUNNIT_ARVO[tunniste_ARVO]]!=12){tietojärjestelmät_pätemätön=1;return;}
    unsigned omistaja_objekti=첫째값[첫째값[tunniste_ARVO]],Nimi=첫째값[SEKUNNIT_ARVO[tunniste_ARVO]],서술값=SEKUNNIT_ARVO[SEKUNNIT_ARVO[tunniste_ARVO]];int TULOS=0,kohde_LASKE=서술자(서술값,&TULOS);if(kohde_LASKE<0){tietojärjestelmät_pätemätön=1;return;}
    for(int 순번=kohde_LASKE;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuaalinen_KUTSU)내보내기("Q();");
    if(!virtuaalinen_KUTSU&&같음(omistaja_objekti,첫째값[nykyinen_Luokka])){
        unsigned Ryhmä_muuttaa_kokoa=0;for(;Ryhmä_muuttaa_kokoa<메소드개수;Ryhmä_muuttaa_kokoa++)if(같음(Nimi,메소드목록[Ryhmä_muuttaa_kokoa].Nimi)&&같음(서술값,메소드목록[Ryhmä_muuttaa_kokoa].서술값))break;
        if(Ryhmä_muuttaa_kokoa==메소드개수||!(메소드목록[Ryhmä_muuttaa_kokoa].määritys_Background_Intelligent_Transfer_Service&8)){tietojärjestelmät_pätemätön=1;return;}
        if(TULOS)내보내기("P(");내보내기("m%u(",Ryhmä_muuttaa_kokoa);for(int 순번=0;순번<kohde_LASKE;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(TULOS?"));":" );");return;
    }
    if((virtuaalinen_KUTSU&&UNICODE_ARVO(omistaja_objekti,"java/io/PrintStream")&& (UNICODE_ARVO(Nimi,"print")||UNICODE_ARVO(Nimi,"println")))||(!virtuaalinen_KUTSU&&UNICODE_ARVO(omistaja_objekti,"suomi/oma/tulostuspaikka"))){
        if(UNICODE_ARVO(서술값,"(I)V")&&(UNICODE_ARVO(Nimi,"print")||UNICODE_ARVO(Nimi,"println")||UNICODE_ARVO(Nimi,"kirjoitus_numero"))){내보내기("jprint(x[0],1,%d);",UNICODE_ARVO(Nimi,"print")?0:1);return;}
        if(UNICODE_ARVO(서술값,"(Ljava/lang/String;)V")&&(UNICODE_ARVO(Nimi,"print")||UNICODE_ARVO(Nimi,"println")||UNICODE_ARVO(Nimi,"Kirjoitus")||UNICODE_ARVO(Nimi,"kirjoitus_rivi"))){내보내기("jprint(x[0],0,%d);",UNICODE_ARVO(Nimi,"print")||UNICODE_ARVO(Nimi,"Kirjoitus")?0:1);return;}
        if(UNICODE_ARVO(서술값,"()V")&&UNICODE_ARVO(Nimi,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuaalinen_KUTSU&&UNICODE_ARVO(omistaja_objekti,"suomi/oma/tiedoston_nimi")){
        if(UNICODE_ARVO(Nimi,"Kirjoitus")&&UNICODE_ARVO(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_ARVO(Nimi,"Luku")&&UNICODE_ARVO(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    tietojärjestelmät_pätemätön=1;
}
static void kääntää_menetelmä(unsigned HAKU_INDEKSI){
    menetelmä_merkintä*Ryhmä_muuttaa_kokoa=메소드목록+HAKU_INDEKSI;if(UNICODE_ARVO(Ryhmä_muuttaa_kokoa->Nimi,"<init>"))return;int TULOS,kohde_LASKE=서술자(Ryhmä_muuttaa_kokoa->서술값,&TULOS);if(kohde_LASKE<0){tietojärjestelmät_pätemätön=1;return;}
    내보내기("static W m%u(",HAKU_INDEKSI);for(int 순번=0;순번<kohde_LASKE;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!kohde_LASKE)내보내기("void");
    if((unsigned)kohde_LASKE>Ryhmä_muuttaa_kokoa->지역변수들){tietojärjestelmät_pätemätön=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Ryhmä_muuttaa_kokoa->지역변수들?Ryhmä_muuttaa_kokoa->지역변수들:1);for(int 순번=0;순번<kohde_LASKE;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=kesto_ARVO;kesto_ARVO=Ryhmä_muuttaa_kokoa->käsky_JONO+Ryhmä_muuttaa_kokoa->Koko;nykyinen_toimi=Ryhmä_muuttaa_kokoa->käsky_JONO;
    while(nykyinen_toimi<kesto_ARVO&&!tietojärjestelmät_pätemätön){unsigned komento_toimi=nykyinen_toimi-Ryhmä_muuttaa_kokoa->käsky_JONO,leikkaus_ARVO=tavu_data();내보내기("L%u:;",komento_toimi);
        if(leikkaus_ARVO==0){}
        else if(leikkaus_ARVO==1)내보내기("P(0);");
        else if(leikkaus_ARVO>=2&&leikkaus_ARVO<=8)내보내기("P(%uU);",leikkaus_ARVO-3);
        else if(leikkaus_ARVO==16){int ARVO=(int8_t)tavu_data();내보내기("P(%uU);",(unsigned)ARVO);}
        else if(leikkaus_ARVO==17){int ARVO=(int16_t)절반값();내보내기("P(%uU);",(unsigned)ARVO);}
        else if(leikkaus_ARVO==18||leikkaus_ARVO==19)vakio_ARVO(leikkaus_ARVO==18?tavu_data():절반값());
        else if(leikkaus_ARVO==21||leikkaus_ARVO==25){unsigned 순번=tavu_data();if(순번>=Ryhmä_muuttaa_kokoa->지역변수들)tietojärjestelmät_pätemätön=1;내보내기("P(v[%u]);",순번);}
        else if((leikkaus_ARVO>=26&&leikkaus_ARVO<=29)||(leikkaus_ARVO>=42&&leikkaus_ARVO<=45)){unsigned 순번=leikkaus_ARVO>=42?leikkaus_ARVO-42:leikkaus_ARVO-26;if(순번>=Ryhmä_muuttaa_kokoa->지역변수들)tietojärjestelmät_pätemätön=1;내보내기("P(v[%u]);",순번);}
        else if(leikkaus_ARVO==54||leikkaus_ARVO==58){unsigned 순번=tavu_data();if(순번>=Ryhmä_muuttaa_kokoa->지역변수들)tietojärjestelmät_pätemätön=1;내보내기("v[%u]=Q();",순번);}
        else if((leikkaus_ARVO>=59&&leikkaus_ARVO<=62)||(leikkaus_ARVO>=75&&leikkaus_ARVO<=78)){unsigned 순번=leikkaus_ARVO>=75?leikkaus_ARVO-75:leikkaus_ARVO-59;if(순번>=Ryhmä_muuttaa_kokoa->지역변수들)tietojärjestelmät_pätemätön=1;내보내기("v[%u]=Q();",순번);}
        else if(leikkaus_ARVO==46||leikkaus_ARVO==50||leikkaus_ARVO==51||leikkaus_ARVO==52||leikkaus_ARVO==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(leikkaus_ARVO==79||leikkaus_ARVO==83||leikkaus_ARVO==84||leikkaus_ARVO==85||leikkaus_ARVO==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",leikkaus_ARVO==84?"(unsigned)(signed char)q":leikkaus_ARVO==85?"(unsigned short)q":leikkaus_ARVO==86?"(unsigned)(short)q":"q");
        else if(leikkaus_ARVO==87)내보내기("Q();");
        else if(leikkaus_ARVO==89)내보내기("q=Q();P(q);P(q);");
        else if(leikkaus_ARVO==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(leikkaus_ARVO==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(leikkaus_ARVO==96||leikkaus_ARVO==100||leikkaus_ARVO==104||leikkaus_ARVO==120||leikkaus_ARVO==124||leikkaus_ARVO==126||leikkaus_ARVO==128||leikkaus_ARVO==130){const char*koodaus_ARVO=leikkaus_ARVO==96?"+":leikkaus_ARVO==100?"-":leikkaus_ARVO==104?"*":leikkaus_ARVO==120?"<<":leikkaus_ARVO==124?">>":leikkaus_ARVO==126?"&":leikkaus_ARVO==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",koodaus_ARVO,leikkaus_ARVO==120||leikkaus_ARVO==124?"%32":"");}
        else if(leikkaus_ARVO==108||leikkaus_ARVO==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",leikkaus_ARVO==112);
        else if(leikkaus_ARVO==116)내보내기("P(0U-(unsigned)Q());");
        else if(leikkaus_ARVO==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(leikkaus_ARVO==132){unsigned 순번=tavu_data();int 차이=(int8_t)tavu_data();if(순번>=Ryhmä_muuttaa_kokoa->지역변수들)tietojärjestelmät_pätemätön=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(leikkaus_ARVO>=145&&leikkaus_ARVO<=147)내보내기("P((unsigned)(%s)Q());",leikkaus_ARVO==145?"signed char":leikkaus_ARVO==146?"unsigned short":"short");
        else if(leikkaus_ARVO>=153&&leikkaus_ARVO<=166){int tavoite=(int)komento_toimi+(int16_t)절반값();const char*Vertailu_ARVO[]={"==","!=","<",">=",">","<="};if(tavoite<0||tavoite>=(int)Ryhmä_muuttaa_kokoa->Koko){tietojärjestelmät_pätemätön=1;break;}if(leikkaus_ARVO<159)내보내기("if((int)Q()%s0)goto L%d;",Vertailu_ARVO[leikkaus_ARVO-153],tavoite);else if(leikkaus_ARVO<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Vertailu_ARVO[leikkaus_ARVO-159],tavoite);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",leikkaus_ARVO==165?"==":"!=",tavoite);}
        else if(leikkaus_ARVO==167){int tavoite=(int)komento_toimi+(int16_t)절반값();if(tavoite<0||tavoite>=(int)Ryhmä_muuttaa_kokoa->Koko)tietojärjestelmät_pätemätön=1;내보내기("goto L%d;",tavoite);}
        else if(leikkaus_ARVO==172||leikkaus_ARVO==176)내보내기("return Q();");else if(leikkaus_ARVO==177)내보내기("return 0;");
        else if(leikkaus_ARVO==178||leikkaus_ARVO==179){unsigned tunniste_ARVO=절반값();if(tunniste_ARVO<1||tunniste_ARVO>=vakio_pooli||Luokat_luettelo[tunniste_ARVO]!=9||첫째값[tunniste_ARVO]>=vakio_pooli||SEKUNNIT_ARVO[tunniste_ARVO]>=vakio_pooli||Luokat_luettelo[첫째값[tunniste_ARVO]]!=7||Luokat_luettelo[SEKUNNIT_ARVO[tunniste_ARVO]]!=12){tietojärjestelmät_pätemätön=1;break;}unsigned omistaja_objekti=첫째값[첫째값[tunniste_ARVO]],Nimi=첫째값[SEKUNNIT_ARVO[tunniste_ARVO]],서술값=SEKUNNIT_ARVO[SEKUNNIT_ARVO[tunniste_ARVO]];
            if(leikkaus_ARVO==178&&UNICODE_ARVO(omistaja_objekti,"java/lang/System")&&UNICODE_ARVO(Nimi,"out")&&UNICODE_ARVO(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Tiedosto_merkintä=0;while(Tiedosto_merkintä<필드개수&&(!같음(Nimi,kentän_nimi[Tiedosto_merkintä])||!같음(서술값,필드서술[Tiedosto_merkintä])))Tiedosto_merkintä++;if(!같음(omistaja_objekti,첫째값[nykyinen_Luokka])||Tiedosto_merkintä==필드개수){tietojärjestelmät_pätemätön=1;break;}내보내기(leikkaus_ARVO==178?"P(fields[%u]);":"fields[%u]=Q();",Tiedosto_merkintä);}}
        else if(leikkaus_ARVO==182||leikkaus_ARVO==184)호출(절반값(),leikkaus_ARVO==182);
        else if(leikkaus_ARVO==188){unsigned TYYPPI_alue=tavu_data();if(TYYPPI_alue!=4&&TYYPPI_alue!=5&&TYYPPI_alue!=8&&TYYPPI_alue!=9&&TYYPPI_alue!=10)tietojärjestelmät_pätemätön=1;내보내기("P(jarray((int)Q()));");}
        else if(leikkaus_ARVO==190)내보내기("P(jlength(Q()));");
        else if(leikkaus_ARVO==198||leikkaus_ARVO==199){int tavoite=(int)komento_toimi+(int16_t)절반값();if(tavoite<0||tavoite>=(int)Ryhmä_muuttaa_kokoa->Koko)tietojärjestelmät_pätemätön=1;내보내기("if(Q()%s0)goto L%d;",leikkaus_ARVO==198?"==":"!=",tavoite);}
        else tietojärjestelmät_pätemätön=1;
        if(tietojärjestelmät_pätemätön)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",HAKU_INDEKSI,leikkaus_ARVO,komento_toimi);
        내보내기("\n");
    }
    kesto_ARVO=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned merkkijono_osio(unsigned *data_toimi,unsigned lopettaa_puhelu_SIIRTYMÄ){
    if(*data_toimi>=lopettaa_puhelu_SIIRTYMÄ){tietojärjestelmät_pätemätön=1;return 0;}unsigned merkkikoodi=data[(*data_toimi)++];
    if(merkkikoodi<128)return merkkikoodi;
    unsigned kohde_LASKE=merkkikoodi>=0xc0&&merkkikoodi<=0xdf?1:merkkikoodi>=0xe0&&merkkikoodi<=0xef?2:3;
    if(kohde_LASKE==3||kohde_LASKE>lopettaa_puhelu_SIIRTYMÄ-*data_toimi){tietojärjestelmät_pätemätön=1;return 0;}unsigned ARVO=merkkikoodi&((1u<<(6-kohde_LASKE))-1);
    for(unsigned 순번=0;순번<kohde_LASKE;순번++){unsigned Seuraava_kohde=data[(*data_toimi)++];if((Seuraava_kohde&0xc0)!=0x80)tietojärjestelmät_pätemätön=1;ARVO=ARVO<<6|(Seuraava_kohde&63);}
    if((kohde_LASKE==1&&ARVO<128&&ARVO!=0)||(kohde_LASKE==2&&ARVO<2048))tietojärjestelmät_pätemätön=1;return ARVO;
}
static void merkkijono_vakio(unsigned tunniste_ARVO){
    unsigned 부호없는값=첫째값[tunniste_ARVO];if(부호없는값<1||부호없는값>=vakio_pooli||Luokat_luettelo[부호없는값]!=1){tietojärjestelmät_pätemätön=1;return;}내보내기("static const unsigned char k%u[]={",tunniste_ARVO);
    unsigned data_toimi=첫째값[부호없는값],lopettaa_puhelu_SIIRTYMÄ=data_toimi+SEKUNNIT_ARVO[부호없는값];
    while(data_toimi<lopettaa_puhelu_SIIRTYMÄ&&!tietojärjestelmät_pätemätön){unsigned merkkikoodi=merkkijono_osio(&data_toimi,lopettaa_puhelu_SIIRTYMÄ);
        if(merkkikoodi>=0xd800&&merkkikoodi<=0xdbff){unsigned 낮은부분=merkkijono_osio(&data_toimi,lopettaa_puhelu_SIIRTYMÄ);if(낮은부분<0xdc00||낮은부분>0xdfff){tietojärjestelmät_pätemätön=1;break;}merkkikoodi=0x10000+((merkkikoodi-0xd800)<<10)+낮은부분-0xdc00;}
        else if(merkkikoodi>=0xdc00&&merkkikoodi<=0xdfff){tietojärjestelmät_pätemätön=1;break;}
        if(!merkkikoodi){printf("jaot: embedded NUL string needs JVM mode\n");tietojärjestelmät_pätemätön=1;break;}
        if(merkkikoodi<128)내보내기("%u,",merkkikoodi);
        else{unsigned kohde_LASKE=merkkikoodi<2048?2:merkkikoodi<65536?3:4;내보내기("%u,",(kohde_LASKE==2?0xc0:kohde_LASKE==3?0xe0:0xf0)|(merkkikoodi>>(6*(kohde_LASKE-1))));for(unsigned 순번=kohde_LASKE-1;순번;순번--)내보내기("%u,",0x80|((merkkikoodi>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nimi){
    size_t kohde_LASKE=strlen(Nimi);
    if(kohde_LASKE>4&&!strcmp(Nimi+kohde_LASKE-4,".jar")){
        if(꾸러미열기(Nimi)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char polku_2[256];const char*merkintä_menetelmä=꾸러미진입클래스();kohde_LASKE=strlen(merkintä_menetelmä);if(kohde_LASKE+6>=sizeof(polku_2))return 0;
        for(unsigned 순번=0;순번<kohde_LASKE;순번++)polku_2[순번]=merkintä_menetelmä[순번]=='.'?'/':merkintä_menetelmä[순번];strcpy(polku_2+kohde_LASKE,".class");int merkintä_LASKE=꾸러미읽기(polku_2,data,sizeof(data));if(merkintä_LASKE<0)return 0;kesto_ARVO=merkintä_LASKE;
    }else{intptr_t Tiedosto_kahva=사용자호출(3,(uintptr_t)Nimi,0,0,0,0,0);if(Tiedosto_kahva<0)return 0;intptr_t merkintä_LASKE=사용자호출(9,Tiedosto_kahva,0,0,0,0,0);if(merkintä_LASKE<0||merkintä_LASKE>sizeof(data)){사용자호출(4,Tiedosto_kahva,0,0,0,0,0);return 0;}intptr_t SAATU_HINTA_LASKE=사용자호출(2,Tiedosto_kahva,(uintptr_t)data,merkintä_LASKE,0,0,0);사용자호출(4,Tiedosto_kahva,0,0,0,0,0);if(SAATU_HINTA_LASKE!=merkintä_LASKE)return 0;kesto_ARVO=merkintä_LASKE;}
    if(jäsentää_syöte()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<vakio_pooli&&!tietojärjestelmät_pätemätön;순번++)if(Luokat_luettelo[순번]==8)merkkijono_vakio(순번);
    if(tietojärjestelmät_pätemätön)return 0;
    int aloituskohta=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_ARVO(메소드목록[순번].Nimi,"<init>")){
        int TULOS,merkintä_LASKE=서술자(메소드목록[순번].서술값,&TULOS);if(merkintä_LASKE<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<merkintä_LASKE;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!merkintä_LASKE)내보내기("void");내보내기(");\n");
        if(UNICODE_ARVO(메소드목록[순번].Nimi,"main")&&UNICODE_ARVO(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].määritys_Background_Intelligent_Transfer_Service&9)==9)aloituskohta=순번;
        if(UNICODE_ARVO(메소드목록[순번].Nimi,"<clinit>"))초기값=순번;
    }
    if(aloituskohta<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!tietojärjestelmät_pätemätön;순번++)kääntää_menetelmä(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(kenttä_vakio[순번]){
        unsigned merkkikoodi=kenttä_vakio[순번];if(merkkikoodi>=vakio_pooli)return 0;
        if(Luokat_luettelo[merkkikoodi]==3)내보내기("fields[%u]=%uU;",순번,첫째값[merkkikoodi]);else if(Luokat_luettelo[merkkikoodi]==8)내보내기("fields[%u]=(W)k%u;",순번,merkkikoodi);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",aloituskohta);
    return tietojärjestelmät_pätemätön?0:teksti;
}
