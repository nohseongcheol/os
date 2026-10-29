#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "köteg.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char adat[16384];static unsigned hossz_ÉRTÉK,aktuális_pozíció;static int informatikai_részleg_alaptalan;
static unsigned Címkék_Lista[512],첫째값[512],MPERC_ÉRTÉK[512],állandó_gyűjtő,aktuális_tanóra;
static char Szöveg[65536];static unsigned Szövegméret;
typedef struct {unsigned konfiguráció_BITS,Név,서술값,명령열,Méret,지역변수들,Sor_tár;} metódus_bejegyzés;
static metódus_bejegyzés 메소드목록[64];static unsigned 메소드개수;
static unsigned mezőnév[64],필드서술[64],mező_állandó[64],필드개수;
static unsigned ÁTHELYEZ_ÉRTÉK(unsigned cikk_DARAB){if(aktuális_pozíció>hossz_ÉRTÉK||cikk_DARAB>hossz_ÉRTÉK-aktuális_pozíció){informatikai_részleg_alaptalan=1;return 0;}unsigned adat_pozíció=aktuális_pozíció;aktuális_pozíció+=cikk_DARAB;return adat_pozíció;}
static unsigned bájt_adat(void){unsigned adat_pozíció=ÁTHELYEZ_ÉRTÉK(1);return informatikai_részleg_alaptalan?0:adat[adat_pozíció];}
static unsigned 절반값(void){unsigned x_koordináta=bájt_adat();return x_koordináta<<8|bájt_adat();}
static uint32_t 가득참(void){uint32_t x_koordináta=절반값();return x_koordináta<<16|절반값();}
static int UNICODE_ÉRTÉK(unsigned 순번,const char*sztring_adat){return 순번>0&&순번<állandó_gyűjtő&&Címkék_Lista[순번]==1&&strlen(sztring_adat)==MPERC_ÉRTÉK[순번]&&!memcmp(adat+첫째값[순번],sztring_adat,MPERC_ÉRTÉK[순번]);}
static int 같음(unsigned x_koordináta,unsigned Y_koordináta){return x_koordináta>0&&x_koordináta<állandó_gyűjtő&&Y_koordináta>0&&Y_koordináta<állandó_gyűjtő&&Címkék_Lista[x_koordináta]==1&&Címkék_Lista[Y_koordináta]==1&&MPERC_ÉRTÉK[x_koordináta]==MPERC_ÉRTÉK[Y_koordináta]&&!memcmp(adat+첫째값[x_koordináta],adat+첫째값[Y_koordináta],MPERC_ÉRTÉK[x_koordináta]);}
static void 내보내기(const char*Fájl_bejegyzés,...){if(informatikai_részleg_alaptalan)return;va_list argumentum_TÖMB;va_start(argumentum_TÖMB,Fájl_bejegyzés);int cikk_DARAB=vsnprintf(Szöveg+Szövegméret,sizeof(Szöveg)-Szövegméret,Fájl_bejegyzés,argumentum_TÖMB);va_end(argumentum_TÖMB);if(cikk_DARAB<0||(unsigned)cikk_DARAB>=sizeof(Szöveg)-Szövegméret){informatikai_részleg_alaptalan=1;return;}Szövegméret+=cikk_DARAB;}
static int 서술자(unsigned azonosító_ÉRTÉK,int*KR){
    if(azonosító_ÉRTÉK<1||azonosító_ÉRTÉK>=állandó_gyűjtő||Címkék_Lista[azonosító_ÉRTÉK]!=1)return -1;unsigned adat_pozíció=첫째값[azonosító_ÉRTÉK],megszüntet_Ofszet=adat_pozíció+MPERC_ÉRTÉK[azonosító_ÉRTÉK];if(adat_pozíció>=megszüntet_Ofszet||adat[adat_pozíció++]!='(')return -1;int bejegyzés_DARAB=0;
    while(adat_pozíció<megszüntet_Ofszet&&adat[adat_pozíció]!=')'){
        unsigned kódpont=adat[adat_pozíció++];while(kódpont=='['&&adat_pozíció<megszüntet_Ofszet)kódpont=adat[adat_pozíció++];
        if(kódpont=='L'){while(adat_pozíció<megszüntet_Ofszet&&adat[adat_pozíció]!=';')adat_pozíció++;if(adat_pozíció==megszüntet_Ofszet)return -1;adat_pozíció++;}
        else if(kódpont!='I'&&kódpont!='Z'&&kódpont!='B'&&kódpont!='C'&&kódpont!='S')return -1;
        if(++bejegyzés_DARAB>16)return -1;
    }
    if(adat_pozíció+1>=megszüntet_Ofszet||adat[adat_pozíció++]!=')')return -1;*KR=adat[adat_pozíció]=='V'?0:1;
    if(adat[adat_pozíció]=='J'||adat[adat_pozíció]=='D'||adat[adat_pozíció]=='F')return -1;return bejegyzés_DARAB;
}
static void attribútumok(void){unsigned cikk_DARAB=절반값();for(unsigned 순번=0;순번<cikk_DARAB&&!informatikai_részleg_alaptalan;순번++){절반값();unsigned Méret=가득참();ÁTHELYEZ_ÉRTÉK(Méret);}}
static int elemez_bevitel(void){
    if(가득참()!=0xcafebabe)return -1;unsigned alverzió=절반값(),verziószám=절반값();if(alverzió||verziószám<45||verziószám>52)return -1;
    állandó_gyűjtő=절반값();if(állandó_gyűjtő<1||állandó_gyűjtő>512)return -1;
    for(unsigned 순번=1;순번<állandó_gyűjtő&&!informatikai_részleg_alaptalan;순번++){
        Címkék_Lista[순번]=bájt_adat();switch(Címkék_Lista[순번]){
        case 1:MPERC_ÉRTÉK[순번]=절반값();첫째값[순번]=ÁTHELYEZ_ÉRTÉK(MPERC_ÉRTÉK[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:ÁTHELYEZ_ÉRTÉK(8);if(++순번>=állandó_gyűjtő)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();MPERC_ÉRTÉK[순번]=절반값();break;
        case 15:첫째값[순번]=bájt_adat();MPERC_ÉRTÉK[순번]=절반값();break;default:return -1;
        }
    }
    절반값();aktuális_tanóra=절반값();절반값();if(aktuális_tanóra<1||aktuális_tanóra>=állandó_gyűjtő||Címkék_Lista[aktuális_tanóra]!=7||첫째값[aktuális_tanóra]<1||첫째값[aktuális_tanóra]>=állandó_gyűjtő||Címkék_Lista[첫째값[aktuális_tanóra]]!=1)return -1;unsigned 인터페이스목록=절반값();ÁTHELYEZ_ÉRTÉK(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informatikai_részleg_alaptalan;순번++){
        unsigned konfiguráció_BITS=절반값();mezőnév[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfiguráció_BITS&8))return -1;
        unsigned bejegyzés_DARAB=절반값();for(unsigned 안쪽순번=0;안쪽순번<bejegyzés_DARAB&&!informatikai_részleg_alaptalan;안쪽순번++){
            unsigned Név=절반값(),Méret=가득참();
            if(UNICODE_ÉRTÉK(Név,"ConstantValue")){if(Méret!=2)return -1;mező_állandó[순번]=절반값();}
            else ÁTHELYEZ_ÉRTÉK(Méret);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informatikai_részleg_alaptalan;순번++){
        metódus_bejegyzés*Csoport_méretez=메소드목록+순번;Csoport_méretez->konfiguráció_BITS=절반값();Csoport_méretez->Név=절반값();Csoport_méretez->서술값=절반값();unsigned bejegyzés_DARAB=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<bejegyzés_DARAB&&!informatikai_részleg_alaptalan;안쪽순번++){
            unsigned Név=절반값(),Méret=가득참(),Futtatás=aktuális_pozíció;
            if(Méret>hossz_ÉRTÉK-aktuális_pozíció)return -1;
            if(UNICODE_ÉRTÉK(Név,"Code")){
                Csoport_méretez->Sor_tár=절반값();Csoport_méretez->지역변수들=절반값();Csoport_méretez->Méret=가득참();Csoport_méretez->명령열=ÁTHELYEZ_ÉRTÉK(Csoport_méretez->Méret);
                if(Csoport_méretez->Sor_tár>128||Csoport_méretez->지역변수들>128||Csoport_méretez->Méret>8192||절반값())return -1;attribútumok();
            }else ÁTHELYEZ_ÉRTÉK(Méret);
            if(aktuális_pozíció!=Futtatás+Méret)return -1;
        }
        if(!UNICODE_ÉRTÉK(Csoport_méretez->Név,"<init>")&&(!(Csoport_méretez->konfiguráció_BITS&8)||(Csoport_méretez->konfiguráció_BITS&(0x100|0x20))||!Csoport_méretez->Méret))return -1;
    }
    attribútumok();return informatikai_részleg_alaptalan||aktuális_pozíció!=hossz_ÉRTÉK?-1:0;
}
static void állandó_ÉRTÉK(unsigned azonosító_ÉRTÉK){
    if(!azonosító_ÉRTÉK||azonosító_ÉRTÉK>=állandó_gyűjtő){informatikai_részleg_alaptalan=1;return;}
    if(Címkék_Lista[azonosító_ÉRTÉK]==3)내보내기("P(%uU);",첫째값[azonosító_ÉRTÉK]);
    else if(Címkék_Lista[azonosító_ÉRTÉK]==8)내보내기("P((W)k%u);",azonosító_ÉRTÉK);else informatikai_részleg_alaptalan=1;
}
static void 호출(unsigned azonosító_ÉRTÉK,int virtuális_hív){
    if(azonosító_ÉRTÉK<1||azonosító_ÉRTÉK>=állandó_gyűjtő||(Címkék_Lista[azonosító_ÉRTÉK]!=10&&Címkék_Lista[azonosító_ÉRTÉK]!=11)||첫째값[azonosító_ÉRTÉK]<1||첫째값[azonosító_ÉRTÉK]>=állandó_gyűjtő||Címkék_Lista[첫째값[azonosító_ÉRTÉK]]!=7||MPERC_ÉRTÉK[azonosító_ÉRTÉK]<1||MPERC_ÉRTÉK[azonosító_ÉRTÉK]>=állandó_gyűjtő||Címkék_Lista[MPERC_ÉRTÉK[azonosító_ÉRTÉK]]!=12){informatikai_részleg_alaptalan=1;return;}
    unsigned tulajdonos_objektum=첫째값[첫째값[azonosító_ÉRTÉK]],Név=첫째값[MPERC_ÉRTÉK[azonosító_ÉRTÉK]],서술값=MPERC_ÉRTÉK[MPERC_ÉRTÉK[azonosító_ÉRTÉK]];int KR=0,cikk_DARAB=서술자(서술값,&KR);if(cikk_DARAB<0){informatikai_részleg_alaptalan=1;return;}
    for(int 순번=cikk_DARAB;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuális_hív)내보내기("Q();");
    if(!virtuális_hív&&같음(tulajdonos_objektum,첫째값[aktuális_tanóra])){
        unsigned Csoport_méretez=0;for(;Csoport_méretez<메소드개수;Csoport_méretez++)if(같음(Név,메소드목록[Csoport_méretez].Név)&&같음(서술값,메소드목록[Csoport_méretez].서술값))break;
        if(Csoport_méretez==메소드개수||!(메소드목록[Csoport_méretez].konfiguráció_BITS&8)){informatikai_részleg_alaptalan=1;return;}
        if(KR)내보내기("P(");내보내기("m%u(",Csoport_méretez);for(int 순번=0;순번<cikk_DARAB;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(KR?"));":" );");return;
    }
    if((virtuális_hív&&UNICODE_ÉRTÉK(tulajdonos_objektum,"java/io/PrintStream")&& (UNICODE_ÉRTÉK(Név,"print")||UNICODE_ÉRTÉK(Név,"println")))||(!virtuális_hív&&UNICODE_ÉRTÉK(tulajdonos_objektum,"magyar/saját/Kimenet"))){
        if(UNICODE_ÉRTÉK(서술값,"(I)V")&&(UNICODE_ÉRTÉK(Név,"print")||UNICODE_ÉRTÉK(Név,"println")||UNICODE_ÉRTÉK(Név,"ír_szám"))){내보내기("jprint(x[0],1,%d);",UNICODE_ÉRTÉK(Név,"print")?0:1);return;}
        if(UNICODE_ÉRTÉK(서술값,"(Ljava/lang/String;)V")&&(UNICODE_ÉRTÉK(Név,"print")||UNICODE_ÉRTÉK(Név,"println")||UNICODE_ÉRTÉK(Név,"Írás")||UNICODE_ÉRTÉK(Név,"ír_sor"))){내보내기("jprint(x[0],0,%d);",UNICODE_ÉRTÉK(Név,"print")||UNICODE_ÉRTÉK(Név,"Írás")?0:1);return;}
        if(UNICODE_ÉRTÉK(서술값,"()V")&&UNICODE_ÉRTÉK(Név,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuális_hív&&UNICODE_ÉRTÉK(tulajdonos_objektum,"magyar/saját/Fájl")){
        if(UNICODE_ÉRTÉK(Név,"Írás")&&UNICODE_ÉRTÉK(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_ÉRTÉK(Név,"Olvasás")&&UNICODE_ÉRTÉK(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informatikai_részleg_alaptalan=1;
}
static void épít_metódus(unsigned KERES_INDEX){
    metódus_bejegyzés*Csoport_méretez=메소드목록+KERES_INDEX;if(UNICODE_ÉRTÉK(Csoport_méretez->Név,"<init>"))return;int KR,cikk_DARAB=서술자(Csoport_méretez->서술값,&KR);if(cikk_DARAB<0){informatikai_részleg_alaptalan=1;return;}
    내보내기("static W m%u(",KERES_INDEX);for(int 순번=0;순번<cikk_DARAB;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!cikk_DARAB)내보내기("void");
    if((unsigned)cikk_DARAB>Csoport_méretez->지역변수들){informatikai_részleg_alaptalan=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Csoport_méretez->지역변수들?Csoport_méretez->지역변수들:1);for(int 순번=0;순번<cikk_DARAB;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=hossz_ÉRTÉK;hossz_ÉRTÉK=Csoport_méretez->명령열+Csoport_méretez->Méret;aktuális_pozíció=Csoport_méretez->명령열;
    while(aktuális_pozíció<hossz_ÉRTÉK&&!informatikai_részleg_alaptalan){unsigned parancs_pozíció=aktuális_pozíció-Csoport_méretez->명령열,műtét_ÉRTÉK=bájt_adat();내보내기("L%u:;",parancs_pozíció);
        if(műtét_ÉRTÉK==0){}
        else if(műtét_ÉRTÉK==1)내보내기("P(0);");
        else if(műtét_ÉRTÉK>=2&&műtét_ÉRTÉK<=8)내보내기("P(%uU);",műtét_ÉRTÉK-3);
        else if(műtét_ÉRTÉK==16){int ÉRTÉK=(int8_t)bájt_adat();내보내기("P(%uU);",(unsigned)ÉRTÉK);}
        else if(műtét_ÉRTÉK==17){int ÉRTÉK=(int16_t)절반값();내보내기("P(%uU);",(unsigned)ÉRTÉK);}
        else if(műtét_ÉRTÉK==18||műtét_ÉRTÉK==19)állandó_ÉRTÉK(műtét_ÉRTÉK==18?bájt_adat():절반값());
        else if(műtét_ÉRTÉK==21||műtét_ÉRTÉK==25){unsigned 순번=bájt_adat();if(순번>=Csoport_méretez->지역변수들)informatikai_részleg_alaptalan=1;내보내기("P(v[%u]);",순번);}
        else if((műtét_ÉRTÉK>=26&&műtét_ÉRTÉK<=29)||(műtét_ÉRTÉK>=42&&műtét_ÉRTÉK<=45)){unsigned 순번=műtét_ÉRTÉK>=42?műtét_ÉRTÉK-42:műtét_ÉRTÉK-26;if(순번>=Csoport_méretez->지역변수들)informatikai_részleg_alaptalan=1;내보내기("P(v[%u]);",순번);}
        else if(műtét_ÉRTÉK==54||műtét_ÉRTÉK==58){unsigned 순번=bájt_adat();if(순번>=Csoport_méretez->지역변수들)informatikai_részleg_alaptalan=1;내보내기("v[%u]=Q();",순번);}
        else if((műtét_ÉRTÉK>=59&&műtét_ÉRTÉK<=62)||(műtét_ÉRTÉK>=75&&műtét_ÉRTÉK<=78)){unsigned 순번=műtét_ÉRTÉK>=75?műtét_ÉRTÉK-75:műtét_ÉRTÉK-59;if(순번>=Csoport_méretez->지역변수들)informatikai_részleg_alaptalan=1;내보내기("v[%u]=Q();",순번);}
        else if(műtét_ÉRTÉK==46||műtét_ÉRTÉK==50||műtét_ÉRTÉK==51||műtét_ÉRTÉK==52||műtét_ÉRTÉK==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(műtét_ÉRTÉK==79||műtét_ÉRTÉK==83||műtét_ÉRTÉK==84||műtét_ÉRTÉK==85||műtét_ÉRTÉK==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",műtét_ÉRTÉK==84?"(unsigned)(signed char)q":műtét_ÉRTÉK==85?"(unsigned short)q":műtét_ÉRTÉK==86?"(unsigned)(short)q":"q");
        else if(műtét_ÉRTÉK==87)내보내기("Q();");
        else if(műtét_ÉRTÉK==89)내보내기("q=Q();P(q);P(q);");
        else if(műtét_ÉRTÉK==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(műtét_ÉRTÉK==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(műtét_ÉRTÉK==96||műtét_ÉRTÉK==100||műtét_ÉRTÉK==104||műtét_ÉRTÉK==120||műtét_ÉRTÉK==124||műtét_ÉRTÉK==126||műtét_ÉRTÉK==128||műtét_ÉRTÉK==130){const char*kódolás_ÉRTÉK=műtét_ÉRTÉK==96?"+":műtét_ÉRTÉK==100?"-":műtét_ÉRTÉK==104?"*":műtét_ÉRTÉK==120?"<<":műtét_ÉRTÉK==124?">>":műtét_ÉRTÉK==126?"&":műtét_ÉRTÉK==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kódolás_ÉRTÉK,műtét_ÉRTÉK==120||műtét_ÉRTÉK==124?"%32":"");}
        else if(műtét_ÉRTÉK==108||műtét_ÉRTÉK==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",műtét_ÉRTÉK==112);
        else if(műtét_ÉRTÉK==116)내보내기("P(0U-(unsigned)Q());");
        else if(műtét_ÉRTÉK==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(műtét_ÉRTÉK==132){unsigned 순번=bájt_adat();int 차이=(int8_t)bájt_adat();if(순번>=Csoport_méretez->지역변수들)informatikai_részleg_alaptalan=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(műtét_ÉRTÉK>=145&&műtét_ÉRTÉK<=147)내보내기("P((unsigned)(%s)Q());",műtét_ÉRTÉK==145?"signed char":műtét_ÉRTÉK==146?"unsigned short":"short");
        else if(műtét_ÉRTÉK>=153&&műtét_ÉRTÉK<=166){int cél=(int)parancs_pozíció+(int16_t)절반값();const char*Összehasonlítás_ÉRTÉK[]={"==","!=","<",">=",">","<="};if(cél<0||cél>=(int)Csoport_méretez->Méret){informatikai_részleg_alaptalan=1;break;}if(műtét_ÉRTÉK<159)내보내기("if((int)Q()%s0)goto L%d;",Összehasonlítás_ÉRTÉK[műtét_ÉRTÉK-153],cél);else if(műtét_ÉRTÉK<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Összehasonlítás_ÉRTÉK[műtét_ÉRTÉK-159],cél);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",műtét_ÉRTÉK==165?"==":"!=",cél);}
        else if(műtét_ÉRTÉK==167){int cél=(int)parancs_pozíció+(int16_t)절반값();if(cél<0||cél>=(int)Csoport_méretez->Méret)informatikai_részleg_alaptalan=1;내보내기("goto L%d;",cél);}
        else if(műtét_ÉRTÉK==172||műtét_ÉRTÉK==176)내보내기("return Q();");else if(műtét_ÉRTÉK==177)내보내기("return 0;");
        else if(műtét_ÉRTÉK==178||műtét_ÉRTÉK==179){unsigned azonosító_ÉRTÉK=절반값();if(azonosító_ÉRTÉK<1||azonosító_ÉRTÉK>=állandó_gyűjtő||Címkék_Lista[azonosító_ÉRTÉK]!=9||첫째값[azonosító_ÉRTÉK]>=állandó_gyűjtő||MPERC_ÉRTÉK[azonosító_ÉRTÉK]>=állandó_gyűjtő||Címkék_Lista[첫째값[azonosító_ÉRTÉK]]!=7||Címkék_Lista[MPERC_ÉRTÉK[azonosító_ÉRTÉK]]!=12){informatikai_részleg_alaptalan=1;break;}unsigned tulajdonos_objektum=첫째값[첫째값[azonosító_ÉRTÉK]],Név=첫째값[MPERC_ÉRTÉK[azonosító_ÉRTÉK]],서술값=MPERC_ÉRTÉK[MPERC_ÉRTÉK[azonosító_ÉRTÉK]];
            if(műtét_ÉRTÉK==178&&UNICODE_ÉRTÉK(tulajdonos_objektum,"java/lang/System")&&UNICODE_ÉRTÉK(Név,"out")&&UNICODE_ÉRTÉK(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Fájl_bejegyzés=0;while(Fájl_bejegyzés<필드개수&&(!같음(Név,mezőnév[Fájl_bejegyzés])||!같음(서술값,필드서술[Fájl_bejegyzés])))Fájl_bejegyzés++;if(!같음(tulajdonos_objektum,첫째값[aktuális_tanóra])||Fájl_bejegyzés==필드개수){informatikai_részleg_alaptalan=1;break;}내보내기(műtét_ÉRTÉK==178?"P(fields[%u]);":"fields[%u]=Q();",Fájl_bejegyzés);}}
        else if(műtét_ÉRTÉK==182||műtét_ÉRTÉK==184)호출(절반값(),műtét_ÉRTÉK==182);
        else if(műtét_ÉRTÉK==188){unsigned beír_terület=bájt_adat();if(beír_terület!=4&&beír_terület!=5&&beír_terület!=8&&beír_terület!=9&&beír_terület!=10)informatikai_részleg_alaptalan=1;내보내기("P(jarray((int)Q()));");}
        else if(műtét_ÉRTÉK==190)내보내기("P(jlength(Q()));");
        else if(műtét_ÉRTÉK==198||műtét_ÉRTÉK==199){int cél=(int)parancs_pozíció+(int16_t)절반값();if(cél<0||cél>=(int)Csoport_méretez->Méret)informatikai_részleg_alaptalan=1;내보내기("if(Q()%s0)goto L%d;",műtét_ÉRTÉK==198?"==":"!=",cél);}
        else informatikai_részleg_alaptalan=1;
        if(informatikai_részleg_alaptalan)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",KERES_INDEX,műtét_ÉRTÉK,parancs_pozíció);
        내보내기("\n");
    }
    hossz_ÉRTÉK=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned sztring_lecke(unsigned *adat_pozíció,unsigned megszüntet_Ofszet){
    if(*adat_pozíció>=megszüntet_Ofszet){informatikai_részleg_alaptalan=1;return 0;}unsigned kódpont=adat[(*adat_pozíció)++];
    if(kódpont<128)return kódpont;
    unsigned cikk_DARAB=kódpont>=0xc0&&kódpont<=0xdf?1:kódpont>=0xe0&&kódpont<=0xef?2:3;
    if(cikk_DARAB==3||cikk_DARAB>megszüntet_Ofszet-*adat_pozíció){informatikai_részleg_alaptalan=1;return 0;}unsigned ÉRTÉK=kódpont&((1u<<(6-cikk_DARAB))-1);
    for(unsigned 순번=0;순번<cikk_DARAB;순번++){unsigned Tovább_cikk=adat[(*adat_pozíció)++];if((Tovább_cikk&0xc0)!=0x80)informatikai_részleg_alaptalan=1;ÉRTÉK=ÉRTÉK<<6|(Tovább_cikk&63);}
    if((cikk_DARAB==1&&ÉRTÉK<128&&ÉRTÉK!=0)||(cikk_DARAB==2&&ÉRTÉK<2048))informatikai_részleg_alaptalan=1;return ÉRTÉK;
}
static void sztring_állandó(unsigned azonosító_ÉRTÉK){
    unsigned 부호없는값=첫째값[azonosító_ÉRTÉK];if(부호없는값<1||부호없는값>=állandó_gyűjtő||Címkék_Lista[부호없는값]!=1){informatikai_részleg_alaptalan=1;return;}내보내기("static const unsigned char k%u[]={",azonosító_ÉRTÉK);
    unsigned adat_pozíció=첫째값[부호없는값],megszüntet_Ofszet=adat_pozíció+MPERC_ÉRTÉK[부호없는값];
    while(adat_pozíció<megszüntet_Ofszet&&!informatikai_részleg_alaptalan){unsigned kódpont=sztring_lecke(&adat_pozíció,megszüntet_Ofszet);
        if(kódpont>=0xd800&&kódpont<=0xdbff){unsigned 낮은부분=sztring_lecke(&adat_pozíció,megszüntet_Ofszet);if(낮은부분<0xdc00||낮은부분>0xdfff){informatikai_részleg_alaptalan=1;break;}kódpont=0x10000+((kódpont-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kódpont>=0xdc00&&kódpont<=0xdfff){informatikai_részleg_alaptalan=1;break;}
        if(!kódpont){printf("jaot: embedded NUL string needs JVM mode\n");informatikai_részleg_alaptalan=1;break;}
        if(kódpont<128)내보내기("%u,",kódpont);
        else{unsigned cikk_DARAB=kódpont<2048?2:kódpont<65536?3:4;내보내기("%u,",(cikk_DARAB==2?0xc0:cikk_DARAB==3?0xe0:0xf0)|(kódpont>>(6*(cikk_DARAB-1))));for(unsigned 순번=cikk_DARAB-1;순번;순번--)내보내기("%u,",0x80|((kódpont>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Név){
    size_t cikk_DARAB=strlen(Név);
    if(cikk_DARAB>4&&!strcmp(Név+cikk_DARAB-4,".jar")){
        if(꾸러미열기(Név)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char ÚTVONAL[256];const char*bejegyzés_metódus=꾸러미진입클래스();cikk_DARAB=strlen(bejegyzés_metódus);if(cikk_DARAB+6>=sizeof(ÚTVONAL))return 0;
        for(unsigned 순번=0;순번<cikk_DARAB;순번++)ÚTVONAL[순번]=bejegyzés_metódus[순번]=='.'?'/':bejegyzés_metódus[순번];strcpy(ÚTVONAL+cikk_DARAB,".class");int bejegyzés_DARAB=꾸러미읽기(ÚTVONAL,adat,sizeof(adat));if(bejegyzés_DARAB<0)return 0;hossz_ÉRTÉK=bejegyzés_DARAB;
    }else{intptr_t fájlleíró=사용자호출(3,(uintptr_t)Név,0,0,0,0,0);if(fájlleíró<0)return 0;intptr_t bejegyzés_DARAB=사용자호출(9,fájlleíró,0,0,0,0,0);if(bejegyzés_DARAB<0||bejegyzés_DARAB>sizeof(adat)){사용자호출(4,fájlleíró,0,0,0,0,0);return 0;}intptr_t KAPOTT_DARAB=사용자호출(2,fájlleíró,(uintptr_t)adat,bejegyzés_DARAB,0,0,0);사용자호출(4,fájlleíró,0,0,0,0,0);if(KAPOTT_DARAB!=bejegyzés_DARAB)return 0;hossz_ÉRTÉK=bejegyzés_DARAB;}
    if(elemez_bevitel()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<állandó_gyűjtő&&!informatikai_részleg_alaptalan;순번++)if(Címkék_Lista[순번]==8)sztring_állandó(순번);
    if(informatikai_részleg_alaptalan)return 0;
    int belépési_pont=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_ÉRTÉK(메소드목록[순번].Név,"<init>")){
        int KR,bejegyzés_DARAB=서술자(메소드목록[순번].서술값,&KR);if(bejegyzés_DARAB<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<bejegyzés_DARAB;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!bejegyzés_DARAB)내보내기("void");내보내기(");\n");
        if(UNICODE_ÉRTÉK(메소드목록[순번].Név,"main")&&UNICODE_ÉRTÉK(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfiguráció_BITS&9)==9)belépési_pont=순번;
        if(UNICODE_ÉRTÉK(메소드목록[순번].Név,"<clinit>"))초기값=순번;
    }
    if(belépési_pont<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informatikai_részleg_alaptalan;순번++)épít_metódus(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(mező_állandó[순번]){
        unsigned kódpont=mező_állandó[순번];if(kódpont>=állandó_gyűjtő)return 0;
        if(Címkék_Lista[kódpont]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kódpont]);else if(Címkék_Lista[kódpont]==8)내보내기("fields[%u]=(W)k%u;",순번,kódpont);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",belépési_pont);
    return informatikai_részleg_alaptalan?0:Szöveg;
}
