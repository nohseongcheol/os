#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "bunt.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned längd_värde,aktuellt_placera;static int informationsteknik_ogiltig;
static unsigned Taggar_ange[512],첫째값[512],SEKUND_värde[512],konstant_pool,aktuellt_Kurs;
static char text[65536];static unsigned Textstorlek;
typedef struct {unsigned konfiguration_BITS,Namn,서술값,instruktion_SEKVENS,Storlek,지역변수들,stackminne;} metod_post;
static metod_post 메소드목록[64];static unsigned 메소드개수;
static unsigned fältnamn[64],필드서술[64],fält_konstant[64],필드개수;
static unsigned TA_värde(unsigned objekt_ANTAL){if(aktuellt_placera>längd_värde||objekt_ANTAL>längd_värde-aktuellt_placera){informationsteknik_ogiltig=1;return 0;}unsigned data_placera=aktuellt_placera;aktuellt_placera+=objekt_ANTAL;return data_placera;}
static unsigned byte_data(void){unsigned data_placera=TA_värde(1);return informationsteknik_ogiltig?0:data[data_placera];}
static unsigned 절반값(void){unsigned x_koordinat=byte_data();return x_koordinat<<8|byte_data();}
static uint32_t 가득참(void){uint32_t x_koordinat=절반값();return x_koordinat<<16|절반값();}
static int UNICODE_värde(unsigned 순번,const char*sträng_data){return 순번>0&&순번<konstant_pool&&Taggar_ange[순번]==1&&strlen(sträng_data)==SEKUND_värde[순번]&&!memcmp(data+첫째값[순번],sträng_data,SEKUND_värde[순번]);}
static int 같음(unsigned x_koordinat,unsigned Y_koordinat){return x_koordinat>0&&x_koordinat<konstant_pool&&Y_koordinat>0&&Y_koordinat<konstant_pool&&Taggar_ange[x_koordinat]==1&&Taggar_ange[Y_koordinat]==1&&SEKUND_värde[x_koordinat]==SEKUND_värde[Y_koordinat]&&!memcmp(data+첫째값[x_koordinat],data+첫째값[Y_koordinat],SEKUND_värde[x_koordinat]);}
static void 내보내기(const char*fil_post,...){if(informationsteknik_ogiltig)return;va_list argument_MATRIS;va_start(argument_MATRIS,fil_post);int objekt_ANTAL=vsnprintf(text+Textstorlek,sizeof(text)-Textstorlek,fil_post,argument_MATRIS);va_end(argument_MATRIS);if(objekt_ANTAL<0||(unsigned)objekt_ANTAL>=sizeof(text)-Textstorlek){informationsteknik_ogiltig=1;return;}Textstorlek+=objekt_ANTAL;}
static int 서술자(unsigned identifierare_värde,int*RESULTAT){
    if(identifierare_värde<1||identifierare_värde>=konstant_pool||Taggar_ange[identifierare_värde]!=1)return -1;unsigned data_placera=첫째값[identifierare_värde],avsluta_FÖRSKJUTNING=data_placera+SEKUND_värde[identifierare_värde];if(data_placera>=avsluta_FÖRSKJUTNING||data[data_placera++]!='(')return -1;int post_ANTAL=0;
    while(data_placera<avsluta_FÖRSKJUTNING&&data[data_placera]!=')'){
        unsigned kodpunkt=data[data_placera++];while(kodpunkt=='['&&data_placera<avsluta_FÖRSKJUTNING)kodpunkt=data[data_placera++];
        if(kodpunkt=='L'){while(data_placera<avsluta_FÖRSKJUTNING&&data[data_placera]!=';')data_placera++;if(data_placera==avsluta_FÖRSKJUTNING)return -1;data_placera++;}
        else if(kodpunkt!='I'&&kodpunkt!='Z'&&kodpunkt!='B'&&kodpunkt!='C'&&kodpunkt!='S')return -1;
        if(++post_ANTAL>16)return -1;
    }
    if(data_placera+1>=avsluta_FÖRSKJUTNING||data[data_placera++]!=')')return -1;*RESULTAT=data[data_placera]=='V'?0:1;
    if(data[data_placera]=='J'||data[data_placera]=='D'||data[data_placera]=='F')return -1;return post_ANTAL;
}
static void personlig_information(void){unsigned objekt_ANTAL=절반값();for(unsigned 순번=0;순번<objekt_ANTAL&&!informationsteknik_ogiltig;순번++){절반값();unsigned Storlek=가득참();TA_värde(Storlek);}}
static int parsa_indata(void){
    if(가득참()!=0xcafebabe)return -1;unsigned lägre_version=절반값(),versionsnummer=절반값();if(lägre_version||versionsnummer<45||versionsnummer>52)return -1;
    konstant_pool=절반값();if(konstant_pool<1||konstant_pool>512)return -1;
    for(unsigned 순번=1;순번<konstant_pool&&!informationsteknik_ogiltig;순번++){
        Taggar_ange[순번]=byte_data();switch(Taggar_ange[순번]){
        case 1:SEKUND_värde[순번]=절반값();첫째값[순번]=TA_värde(SEKUND_värde[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TA_värde(8);if(++순번>=konstant_pool)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEKUND_värde[순번]=절반값();break;
        case 15:첫째값[순번]=byte_data();SEKUND_värde[순번]=절반값();break;default:return -1;
        }
    }
    절반값();aktuellt_Kurs=절반값();절반값();if(aktuellt_Kurs<1||aktuellt_Kurs>=konstant_pool||Taggar_ange[aktuellt_Kurs]!=7||첫째값[aktuellt_Kurs]<1||첫째값[aktuellt_Kurs]>=konstant_pool||Taggar_ange[첫째값[aktuellt_Kurs]]!=1)return -1;unsigned 인터페이스목록=절반값();TA_värde(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informationsteknik_ogiltig;순번++){
        unsigned konfiguration_BITS=절반값();fältnamn[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfiguration_BITS&8))return -1;
        unsigned post_ANTAL=절반값();for(unsigned 안쪽순번=0;안쪽순번<post_ANTAL&&!informationsteknik_ogiltig;안쪽순번++){
            unsigned Namn=절반값(),Storlek=가득참();
            if(UNICODE_värde(Namn,"ConstantValue")){if(Storlek!=2)return -1;fält_konstant[순번]=절반값();}
            else TA_värde(Storlek);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informationsteknik_ogiltig;순번++){
        metod_post*grupp_storlek=메소드목록+순번;grupp_storlek->konfiguration_BITS=절반값();grupp_storlek->Namn=절반값();grupp_storlek->서술값=절반값();unsigned post_ANTAL=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<post_ANTAL&&!informationsteknik_ogiltig;안쪽순번++){
            unsigned Namn=절반값(),Storlek=가득참(),Kör=aktuellt_placera;
            if(Storlek>längd_värde-aktuellt_placera)return -1;
            if(UNICODE_värde(Namn,"Code")){
                grupp_storlek->stackminne=절반값();grupp_storlek->지역변수들=절반값();grupp_storlek->Storlek=가득참();grupp_storlek->instruktion_SEKVENS=TA_värde(grupp_storlek->Storlek);
                if(grupp_storlek->stackminne>128||grupp_storlek->지역변수들>128||grupp_storlek->Storlek>8192||절반값())return -1;personlig_information();
            }else TA_värde(Storlek);
            if(aktuellt_placera!=Kör+Storlek)return -1;
        }
        if(!UNICODE_värde(grupp_storlek->Namn,"<init>")&&(!(grupp_storlek->konfiguration_BITS&8)||(grupp_storlek->konfiguration_BITS&(0x100|0x20))||!grupp_storlek->Storlek))return -1;
    }
    personlig_information();return informationsteknik_ogiltig||aktuellt_placera!=längd_värde?-1:0;
}
static void konstant_värde(unsigned identifierare_värde){
    if(!identifierare_värde||identifierare_värde>=konstant_pool){informationsteknik_ogiltig=1;return;}
    if(Taggar_ange[identifierare_värde]==3)내보내기("P(%uU);",첫째값[identifierare_värde]);
    else if(Taggar_ange[identifierare_värde]==8)내보내기("P((W)k%u);",identifierare_värde);else informationsteknik_ogiltig=1;
}
static void 호출(unsigned identifierare_värde,int virtuell_ring){
    if(identifierare_värde<1||identifierare_värde>=konstant_pool||(Taggar_ange[identifierare_värde]!=10&&Taggar_ange[identifierare_värde]!=11)||첫째값[identifierare_värde]<1||첫째값[identifierare_värde]>=konstant_pool||Taggar_ange[첫째값[identifierare_värde]]!=7||SEKUND_värde[identifierare_värde]<1||SEKUND_värde[identifierare_värde]>=konstant_pool||Taggar_ange[SEKUND_värde[identifierare_värde]]!=12){informationsteknik_ogiltig=1;return;}
    unsigned ägare_objekt=첫째값[첫째값[identifierare_värde]],Namn=첫째값[SEKUND_värde[identifierare_värde]],서술값=SEKUND_värde[SEKUND_värde[identifierare_värde]];int RESULTAT=0,objekt_ANTAL=서술자(서술값,&RESULTAT);if(objekt_ANTAL<0){informationsteknik_ogiltig=1;return;}
    for(int 순번=objekt_ANTAL;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuell_ring)내보내기("Q();");
    if(!virtuell_ring&&같음(ägare_objekt,첫째값[aktuellt_Kurs])){
        unsigned grupp_storlek=0;for(;grupp_storlek<메소드개수;grupp_storlek++)if(같음(Namn,메소드목록[grupp_storlek].Namn)&&같음(서술값,메소드목록[grupp_storlek].서술값))break;
        if(grupp_storlek==메소드개수||!(메소드목록[grupp_storlek].konfiguration_BITS&8)){informationsteknik_ogiltig=1;return;}
        if(RESULTAT)내보내기("P(");내보내기("m%u(",grupp_storlek);for(int 순번=0;순번<objekt_ANTAL;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(RESULTAT?"));":" );");return;
    }
    if((virtuell_ring&&UNICODE_värde(ägare_objekt,"java/io/PrintStream")&& (UNICODE_värde(Namn,"print")||UNICODE_värde(Namn,"println")))||(!virtuell_ring&&UNICODE_värde(ägare_objekt,"Svenska/eget/utmatningsposition"))){
        if(UNICODE_värde(서술값,"(I)V")&&(UNICODE_värde(Namn,"print")||UNICODE_värde(Namn,"println")||UNICODE_värde(Namn,"skriva_nummer"))){내보내기("jprint(x[0],1,%d);",UNICODE_värde(Namn,"print")?0:1);return;}
        if(UNICODE_värde(서술값,"(Ljava/lang/String;)V")&&(UNICODE_värde(Namn,"print")||UNICODE_värde(Namn,"println")||UNICODE_värde(Namn,"Skriv")||UNICODE_värde(Namn,"skriva_rad"))){내보내기("jprint(x[0],0,%d);",UNICODE_värde(Namn,"print")||UNICODE_värde(Namn,"Skriv")?0:1);return;}
        if(UNICODE_värde(서술값,"()V")&&UNICODE_värde(Namn,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuell_ring&&UNICODE_värde(ägare_objekt,"Svenska/eget/filnamn")){
        if(UNICODE_värde(Namn,"Skriv")&&UNICODE_värde(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_värde(Namn,"Läs")&&UNICODE_värde(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informationsteknik_ogiltig=1;
}
static void kompilera_metod(unsigned LETAUPP_INDEX){
    metod_post*grupp_storlek=메소드목록+LETAUPP_INDEX;if(UNICODE_värde(grupp_storlek->Namn,"<init>"))return;int RESULTAT,objekt_ANTAL=서술자(grupp_storlek->서술값,&RESULTAT);if(objekt_ANTAL<0){informationsteknik_ogiltig=1;return;}
    내보내기("static W m%u(",LETAUPP_INDEX);for(int 순번=0;순번<objekt_ANTAL;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!objekt_ANTAL)내보내기("void");
    if((unsigned)objekt_ANTAL>grupp_storlek->지역변수들){informationsteknik_ogiltig=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",grupp_storlek->지역변수들?grupp_storlek->지역변수들:1);for(int 순번=0;순번<objekt_ANTAL;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=längd_värde;längd_värde=grupp_storlek->instruktion_SEKVENS+grupp_storlek->Storlek;aktuellt_placera=grupp_storlek->instruktion_SEKVENS;
    while(aktuellt_placera<längd_värde&&!informationsteknik_ogiltig){unsigned kommando_placera=aktuellt_placera-grupp_storlek->instruktion_SEKVENS,åtgärd_värde=byte_data();내보내기("L%u:;",kommando_placera);
        if(åtgärd_värde==0){}
        else if(åtgärd_värde==1)내보내기("P(0);");
        else if(åtgärd_värde>=2&&åtgärd_värde<=8)내보내기("P(%uU);",åtgärd_värde-3);
        else if(åtgärd_värde==16){int värde=(int8_t)byte_data();내보내기("P(%uU);",(unsigned)värde);}
        else if(åtgärd_värde==17){int värde=(int16_t)절반값();내보내기("P(%uU);",(unsigned)värde);}
        else if(åtgärd_värde==18||åtgärd_värde==19)konstant_värde(åtgärd_värde==18?byte_data():절반값());
        else if(åtgärd_värde==21||åtgärd_värde==25){unsigned 순번=byte_data();if(순번>=grupp_storlek->지역변수들)informationsteknik_ogiltig=1;내보내기("P(v[%u]);",순번);}
        else if((åtgärd_värde>=26&&åtgärd_värde<=29)||(åtgärd_värde>=42&&åtgärd_värde<=45)){unsigned 순번=åtgärd_värde>=42?åtgärd_värde-42:åtgärd_värde-26;if(순번>=grupp_storlek->지역변수들)informationsteknik_ogiltig=1;내보내기("P(v[%u]);",순번);}
        else if(åtgärd_värde==54||åtgärd_värde==58){unsigned 순번=byte_data();if(순번>=grupp_storlek->지역변수들)informationsteknik_ogiltig=1;내보내기("v[%u]=Q();",순번);}
        else if((åtgärd_värde>=59&&åtgärd_värde<=62)||(åtgärd_värde>=75&&åtgärd_värde<=78)){unsigned 순번=åtgärd_värde>=75?åtgärd_värde-75:åtgärd_värde-59;if(순번>=grupp_storlek->지역변수들)informationsteknik_ogiltig=1;내보내기("v[%u]=Q();",순번);}
        else if(åtgärd_värde==46||åtgärd_värde==50||åtgärd_värde==51||åtgärd_värde==52||åtgärd_värde==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(åtgärd_värde==79||åtgärd_värde==83||åtgärd_värde==84||åtgärd_värde==85||åtgärd_värde==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",åtgärd_värde==84?"(unsigned)(signed char)q":åtgärd_värde==85?"(unsigned short)q":åtgärd_värde==86?"(unsigned)(short)q":"q");
        else if(åtgärd_värde==87)내보내기("Q();");
        else if(åtgärd_värde==89)내보내기("q=Q();P(q);P(q);");
        else if(åtgärd_värde==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(åtgärd_värde==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(åtgärd_värde==96||åtgärd_värde==100||åtgärd_värde==104||åtgärd_värde==120||åtgärd_värde==124||åtgärd_värde==126||åtgärd_värde==128||åtgärd_värde==130){const char*kodning_värde=åtgärd_värde==96?"+":åtgärd_värde==100?"-":åtgärd_värde==104?"*":åtgärd_värde==120?"<<":åtgärd_värde==124?">>":åtgärd_värde==126?"&":åtgärd_värde==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodning_värde,åtgärd_värde==120||åtgärd_värde==124?"%32":"");}
        else if(åtgärd_värde==108||åtgärd_värde==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",åtgärd_värde==112);
        else if(åtgärd_värde==116)내보내기("P(0U-(unsigned)Q());");
        else if(åtgärd_värde==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(åtgärd_värde==132){unsigned 순번=byte_data();int 차이=(int8_t)byte_data();if(순번>=grupp_storlek->지역변수들)informationsteknik_ogiltig=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(åtgärd_värde>=145&&åtgärd_värde<=147)내보내기("P((unsigned)(%s)Q());",åtgärd_värde==145?"signed char":åtgärd_värde==146?"unsigned short":"short");
        else if(åtgärd_värde>=153&&åtgärd_värde<=166){int mål=(int)kommando_placera+(int16_t)절반값();const char*Jämförelse_värde[]={"==","!=","<",">=",">","<="};if(mål<0||mål>=(int)grupp_storlek->Storlek){informationsteknik_ogiltig=1;break;}if(åtgärd_värde<159)내보내기("if((int)Q()%s0)goto L%d;",Jämförelse_värde[åtgärd_värde-153],mål);else if(åtgärd_värde<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Jämförelse_värde[åtgärd_värde-159],mål);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",åtgärd_värde==165?"==":"!=",mål);}
        else if(åtgärd_värde==167){int mål=(int)kommando_placera+(int16_t)절반값();if(mål<0||mål>=(int)grupp_storlek->Storlek)informationsteknik_ogiltig=1;내보내기("goto L%d;",mål);}
        else if(åtgärd_värde==172||åtgärd_värde==176)내보내기("return Q();");else if(åtgärd_värde==177)내보내기("return 0;");
        else if(åtgärd_värde==178||åtgärd_värde==179){unsigned identifierare_värde=절반값();if(identifierare_värde<1||identifierare_värde>=konstant_pool||Taggar_ange[identifierare_värde]!=9||첫째값[identifierare_värde]>=konstant_pool||SEKUND_värde[identifierare_värde]>=konstant_pool||Taggar_ange[첫째값[identifierare_värde]]!=7||Taggar_ange[SEKUND_värde[identifierare_värde]]!=12){informationsteknik_ogiltig=1;break;}unsigned ägare_objekt=첫째값[첫째값[identifierare_värde]],Namn=첫째값[SEKUND_värde[identifierare_värde]],서술값=SEKUND_värde[SEKUND_värde[identifierare_värde]];
            if(åtgärd_värde==178&&UNICODE_värde(ägare_objekt,"java/lang/System")&&UNICODE_värde(Namn,"out")&&UNICODE_värde(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fil_post=0;while(fil_post<필드개수&&(!같음(Namn,fältnamn[fil_post])||!같음(서술값,필드서술[fil_post])))fil_post++;if(!같음(ägare_objekt,첫째값[aktuellt_Kurs])||fil_post==필드개수){informationsteknik_ogiltig=1;break;}내보내기(åtgärd_värde==178?"P(fields[%u]);":"fields[%u]=Q();",fil_post);}}
        else if(åtgärd_värde==182||åtgärd_värde==184)호출(절반값(),åtgärd_värde==182);
        else if(åtgärd_värde==188){unsigned Typ_område=byte_data();if(Typ_område!=4&&Typ_område!=5&&Typ_område!=8&&Typ_område!=9&&Typ_område!=10)informationsteknik_ogiltig=1;내보내기("P(jarray((int)Q()));");}
        else if(åtgärd_värde==190)내보내기("P(jlength(Q()));");
        else if(åtgärd_värde==198||åtgärd_värde==199){int mål=(int)kommando_placera+(int16_t)절반값();if(mål<0||mål>=(int)grupp_storlek->Storlek)informationsteknik_ogiltig=1;내보내기("if(Q()%s0)goto L%d;",åtgärd_värde==198?"==":"!=",mål);}
        else informationsteknik_ogiltig=1;
        if(informationsteknik_ogiltig)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LETAUPP_INDEX,åtgärd_värde,kommando_placera);
        내보내기("\n");
    }
    längd_värde=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned sträng_enhet(unsigned *data_placera,unsigned avsluta_FÖRSKJUTNING){
    if(*data_placera>=avsluta_FÖRSKJUTNING){informationsteknik_ogiltig=1;return 0;}unsigned kodpunkt=data[(*data_placera)++];
    if(kodpunkt<128)return kodpunkt;
    unsigned objekt_ANTAL=kodpunkt>=0xc0&&kodpunkt<=0xdf?1:kodpunkt>=0xe0&&kodpunkt<=0xef?2:3;
    if(objekt_ANTAL==3||objekt_ANTAL>avsluta_FÖRSKJUTNING-*data_placera){informationsteknik_ogiltig=1;return 0;}unsigned värde=kodpunkt&((1u<<(6-objekt_ANTAL))-1);
    for(unsigned 순번=0;순번<objekt_ANTAL;순번++){unsigned Nästa_objekt=data[(*data_placera)++];if((Nästa_objekt&0xc0)!=0x80)informationsteknik_ogiltig=1;värde=värde<<6|(Nästa_objekt&63);}
    if((objekt_ANTAL==1&&värde<128&&värde!=0)||(objekt_ANTAL==2&&värde<2048))informationsteknik_ogiltig=1;return värde;
}
static void sträng_konstant(unsigned identifierare_värde){
    unsigned 부호없는값=첫째값[identifierare_värde];if(부호없는값<1||부호없는값>=konstant_pool||Taggar_ange[부호없는값]!=1){informationsteknik_ogiltig=1;return;}내보내기("static const unsigned char k%u[]={",identifierare_värde);
    unsigned data_placera=첫째값[부호없는값],avsluta_FÖRSKJUTNING=data_placera+SEKUND_värde[부호없는값];
    while(data_placera<avsluta_FÖRSKJUTNING&&!informationsteknik_ogiltig){unsigned kodpunkt=sträng_enhet(&data_placera,avsluta_FÖRSKJUTNING);
        if(kodpunkt>=0xd800&&kodpunkt<=0xdbff){unsigned 낮은부분=sträng_enhet(&data_placera,avsluta_FÖRSKJUTNING);if(낮은부분<0xdc00||낮은부분>0xdfff){informationsteknik_ogiltig=1;break;}kodpunkt=0x10000+((kodpunkt-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kodpunkt>=0xdc00&&kodpunkt<=0xdfff){informationsteknik_ogiltig=1;break;}
        if(!kodpunkt){printf("jaot: embedded NUL string needs JVM mode\n");informationsteknik_ogiltig=1;break;}
        if(kodpunkt<128)내보내기("%u,",kodpunkt);
        else{unsigned objekt_ANTAL=kodpunkt<2048?2:kodpunkt<65536?3:4;내보내기("%u,",(objekt_ANTAL==2?0xc0:objekt_ANTAL==3?0xe0:0xf0)|(kodpunkt>>(6*(objekt_ANTAL-1))));for(unsigned 순번=objekt_ANTAL-1;순번;순번--)내보내기("%u,",0x80|((kodpunkt>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Namn){
    size_t objekt_ANTAL=strlen(Namn);
    if(objekt_ANTAL>4&&!strcmp(Namn+objekt_ANTAL-4,".jar")){
        if(꾸러미열기(Namn)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char sökväg_2[256];const char*post_metod=꾸러미진입클래스();objekt_ANTAL=strlen(post_metod);if(objekt_ANTAL+6>=sizeof(sökväg_2))return 0;
        for(unsigned 순번=0;순번<objekt_ANTAL;순번++)sökväg_2[순번]=post_metod[순번]=='.'?'/':post_metod[순번];strcpy(sökväg_2+objekt_ANTAL,".class");int post_ANTAL=꾸러미읽기(sökväg_2,data,sizeof(data));if(post_ANTAL<0)return 0;längd_värde=post_ANTAL;
    }else{intptr_t filreferens=사용자호출(3,(uintptr_t)Namn,0,0,0,0,0);if(filreferens<0)return 0;intptr_t post_ANTAL=사용자호출(9,filreferens,0,0,0,0,0);if(post_ANTAL<0||post_ANTAL>sizeof(data)){사용자호출(4,filreferens,0,0,0,0,0);return 0;}intptr_t BELOPP_ANTAL=사용자호출(2,filreferens,(uintptr_t)data,post_ANTAL,0,0,0);사용자호출(4,filreferens,0,0,0,0,0);if(BELOPP_ANTAL!=post_ANTAL)return 0;längd_värde=post_ANTAL;}
    if(parsa_indata()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstant_pool&&!informationsteknik_ogiltig;순번++)if(Taggar_ange[순번]==8)sträng_konstant(순번);
    if(informationsteknik_ogiltig)return 0;
    int startpunkt=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_värde(메소드목록[순번].Namn,"<init>")){
        int RESULTAT,post_ANTAL=서술자(메소드목록[순번].서술값,&RESULTAT);if(post_ANTAL<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<post_ANTAL;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!post_ANTAL)내보내기("void");내보내기(");\n");
        if(UNICODE_värde(메소드목록[순번].Namn,"main")&&UNICODE_värde(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfiguration_BITS&9)==9)startpunkt=순번;
        if(UNICODE_värde(메소드목록[순번].Namn,"<clinit>"))초기값=순번;
    }
    if(startpunkt<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informationsteknik_ogiltig;순번++)kompilera_metod(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(fält_konstant[순번]){
        unsigned kodpunkt=fält_konstant[순번];if(kodpunkt>=konstant_pool)return 0;
        if(Taggar_ange[kodpunkt]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kodpunkt]);else if(Taggar_ange[kodpunkt]==8)내보내기("fields[%u]=(W)k%u;",순번,kodpunkt);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",startpunkt);
    return informationsteknik_ogiltig?0:text;
}
