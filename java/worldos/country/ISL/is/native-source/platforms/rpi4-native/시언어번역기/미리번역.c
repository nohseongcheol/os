#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "búnt.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char gögn[16384];static unsigned lengd_VALUE,현재위치;static int upplýsingatækni_ógilt;
static unsigned Merki_Listi[512],첫째값[512],SECOND_VALUE[512],fasti_hópur,현재클래스;
static char Texti[65536];static unsigned textastærð;
typedef struct {unsigned afbrigði_Background_Intelligent_Transfer_Service,Heiti,서술값,skipun_SEQUENCE,Stærð,지역변수들,bunki_geymsla;} aðferð_færsla;
static aðferð_færsla 메소드목록[64];static unsigned 메소드개수;
static unsigned heiti_reits[64],필드서술[64],reitur_fasti[64],필드개수;
static unsigned TAKE_VALUE(unsigned vara_COUNT){if(현재위치>lengd_VALUE||vara_COUNT>lengd_VALUE-현재위치){upplýsingatækni_ógilt=1;return 0;}unsigned gögn_staða=현재위치;현재위치+=vara_COUNT;return gögn_staða;}
static unsigned bæti_gögn(void){unsigned gögn_staða=TAKE_VALUE(1);return upplýsingatækni_ógilt?0:gögn[gögn_staða];}
static unsigned 절반값(void){unsigned x_hnit=bæti_gögn();return x_hnit<<8|bæti_gögn();}
static uint32_t 가득참(void){uint32_t x_hnit=절반값();return x_hnit<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*strengur_gögn){return 순번>0&&순번<fasti_hópur&&Merki_Listi[순번]==1&&strlen(strengur_gögn)==SECOND_VALUE[순번]&&!memcmp(gögn+첫째값[순번],strengur_gögn,SECOND_VALUE[순번]);}
static int 같음(unsigned x_hnit,unsigned Y_hnit){return x_hnit>0&&x_hnit<fasti_hópur&&Y_hnit>0&&Y_hnit<fasti_hópur&&Merki_Listi[x_hnit]==1&&Merki_Listi[Y_hnit]==1&&SECOND_VALUE[x_hnit]==SECOND_VALUE[Y_hnit]&&!memcmp(gögn+첫째값[x_hnit],gögn+첫째값[Y_hnit],SECOND_VALUE[x_hnit]);}
static void 내보내기(const char*skrá_færsla_3d0c1245,...){if(upplýsingatækni_ógilt)return;va_list frumbreyta_ARRAY;va_start(frumbreyta_ARRAY,skrá_færsla_3d0c1245);int vara_COUNT=vsnprintf(Texti+textastærð,sizeof(Texti)-textastærð,skrá_færsla_3d0c1245,frumbreyta_ARRAY);va_end(frumbreyta_ARRAY);if(vara_COUNT<0||(unsigned)vara_COUNT>=sizeof(Texti)-textastærð){upplýsingatækni_ógilt=1;return;}textastærð+=vara_COUNT;}
static int 서술자(unsigned auðkenni_VALUE,int*NIÐURSTAÐA){
    if(auðkenni_VALUE<1||auðkenni_VALUE>=fasti_hópur||Merki_Listi[auðkenni_VALUE]!=1)return -1;unsigned gögn_staða=첫째값[auðkenni_VALUE],ljúka_OFFSET=gögn_staða+SECOND_VALUE[auðkenni_VALUE];if(gögn_staða>=ljúka_OFFSET||gögn[gögn_staða++]!='(')return -1;int færsla_COUNT=0;
    while(gögn_staða<ljúka_OFFSET&&gögn[gögn_staða]!=')'){
        unsigned stafkóði=gögn[gögn_staða++];while(stafkóði=='['&&gögn_staða<ljúka_OFFSET)stafkóði=gögn[gögn_staða++];
        if(stafkóði=='L'){while(gögn_staða<ljúka_OFFSET&&gögn[gögn_staða]!=';')gögn_staða++;if(gögn_staða==ljúka_OFFSET)return -1;gögn_staða++;}
        else if(stafkóði!='I'&&stafkóði!='Z'&&stafkóði!='B'&&stafkóði!='C'&&stafkóði!='S')return -1;
        if(++færsla_COUNT>16)return -1;
    }
    if(gögn_staða+1>=ljúka_OFFSET||gögn[gögn_staða++]!=')')return -1;*NIÐURSTAÐA=gögn[gögn_staða]=='V'?0:1;
    if(gögn[gögn_staða]=='J'||gögn[gögn_staða]=='D'||gögn[gögn_staða]=='F')return -1;return færsla_COUNT;
}
static void eigind(void){unsigned vara_COUNT=절반값();for(unsigned 순번=0;순번<vara_COUNT&&!upplýsingatækni_ógilt;순번++){절반값();unsigned Stærð=가득참();TAKE_VALUE(Stærð);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned ólögráða_einstaklingur_útgáfa=절반값(),útgáfa_númer=절반값();if(ólögráða_einstaklingur_útgáfa||útgáfa_númer<45||útgáfa_númer>52)return -1;
    fasti_hópur=절반값();if(fasti_hópur<1||fasti_hópur>512)return -1;
    for(unsigned 순번=1;순번<fasti_hópur&&!upplýsingatækni_ógilt;순번++){
        Merki_Listi[순번]=bæti_gögn();switch(Merki_Listi[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=fasti_hópur)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bæti_gögn();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=fasti_hópur||Merki_Listi[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=fasti_hópur||Merki_Listi[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!upplýsingatækni_ógilt;순번++){
        unsigned afbrigði_Background_Intelligent_Transfer_Service=절반값();heiti_reits[순번]=절반값();필드서술[순번]=절반값();
        if(!(afbrigði_Background_Intelligent_Transfer_Service&8))return -1;
        unsigned færsla_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<færsla_COUNT&&!upplýsingatækni_ógilt;안쪽순번++){
            unsigned Heiti=절반값(),Stærð=가득참();
            if(UNICODE_VALUE(Heiti,"ConstantValue")){if(Stærð!=2)return -1;reitur_fasti[순번]=절반값();}
            else TAKE_VALUE(Stærð);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!upplýsingatækni_ógilt;순번++){
        aðferð_færsla*Hópur_breyta_stærð=메소드목록+순번;Hópur_breyta_stærð->afbrigði_Background_Intelligent_Transfer_Service=절반값();Hópur_breyta_stærð->Heiti=절반값();Hópur_breyta_stærð->서술값=절반값();unsigned færsla_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<færsla_COUNT&&!upplýsingatækni_ógilt;안쪽순번++){
            unsigned Heiti=절반값(),Stærð=가득참(),Keyra_2=현재위치;
            if(Stærð>lengd_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(Heiti,"Code")){
                Hópur_breyta_stærð->bunki_geymsla=절반값();Hópur_breyta_stærð->지역변수들=절반값();Hópur_breyta_stærð->Stærð=가득참();Hópur_breyta_stærð->skipun_SEQUENCE=TAKE_VALUE(Hópur_breyta_stærð->Stærð);
                if(Hópur_breyta_stærð->bunki_geymsla>128||Hópur_breyta_stærð->지역변수들>128||Hópur_breyta_stærð->Stærð>8192||절반값())return -1;eigind();
            }else TAKE_VALUE(Stærð);
            if(현재위치!=Keyra_2+Stærð)return -1;
        }
        if(!UNICODE_VALUE(Hópur_breyta_stærð->Heiti,"<init>")&&(!(Hópur_breyta_stærð->afbrigði_Background_Intelligent_Transfer_Service&8)||(Hópur_breyta_stærð->afbrigði_Background_Intelligent_Transfer_Service&(0x100|0x20))||!Hópur_breyta_stærð->Stærð))return -1;
    }
    eigind();return upplýsingatækni_ógilt||현재위치!=lengd_VALUE?-1:0;
}
static void fasti_VALUE(unsigned auðkenni_VALUE){
    if(!auðkenni_VALUE||auðkenni_VALUE>=fasti_hópur){upplýsingatækni_ógilt=1;return;}
    if(Merki_Listi[auðkenni_VALUE]==3)내보내기("P(%uU);",첫째값[auðkenni_VALUE]);
    else if(Merki_Listi[auðkenni_VALUE]==8)내보내기("P((W)k%u);",auðkenni_VALUE);else upplýsingatækni_ógilt=1;
}
static void 호출(unsigned auðkenni_VALUE,int sýndar_CALL){
    if(auðkenni_VALUE<1||auðkenni_VALUE>=fasti_hópur||(Merki_Listi[auðkenni_VALUE]!=10&&Merki_Listi[auðkenni_VALUE]!=11)||첫째값[auðkenni_VALUE]<1||첫째값[auðkenni_VALUE]>=fasti_hópur||Merki_Listi[첫째값[auðkenni_VALUE]]!=7||SECOND_VALUE[auðkenni_VALUE]<1||SECOND_VALUE[auðkenni_VALUE]>=fasti_hópur||Merki_Listi[SECOND_VALUE[auðkenni_VALUE]]!=12){upplýsingatækni_ógilt=1;return;}
    unsigned eigandi_hlutur=첫째값[첫째값[auðkenni_VALUE]],Heiti=첫째값[SECOND_VALUE[auðkenni_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[auðkenni_VALUE]];int NIÐURSTAÐA=0,vara_COUNT=서술자(서술값,&NIÐURSTAÐA);if(vara_COUNT<0){upplýsingatækni_ógilt=1;return;}
    for(int 순번=vara_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(sýndar_CALL)내보내기("Q();");
    if(!sýndar_CALL&&같음(eigandi_hlutur,첫째값[현재클래스])){
        unsigned Hópur_breyta_stærð=0;for(;Hópur_breyta_stærð<메소드개수;Hópur_breyta_stærð++)if(같음(Heiti,메소드목록[Hópur_breyta_stærð].Heiti)&&같음(서술값,메소드목록[Hópur_breyta_stærð].서술값))break;
        if(Hópur_breyta_stærð==메소드개수||!(메소드목록[Hópur_breyta_stærð].afbrigði_Background_Intelligent_Transfer_Service&8)){upplýsingatækni_ógilt=1;return;}
        if(NIÐURSTAÐA)내보내기("P(");내보내기("m%u(",Hópur_breyta_stærð);for(int 순번=0;순번<vara_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(NIÐURSTAÐA?"));":" );");return;
    }
    if((sýndar_CALL&&UNICODE_VALUE(eigandi_hlutur,"java/io/PrintStream")&& (UNICODE_VALUE(Heiti,"print")||UNICODE_VALUE(Heiti,"println")))||(!sýndar_CALL&&UNICODE_VALUE(eigandi_hlutur,"Íslenska/eigin/úttak"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Heiti,"print")||UNICODE_VALUE(Heiti,"println")||UNICODE_VALUE(Heiti,"skrifa_númer"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Heiti,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Heiti,"print")||UNICODE_VALUE(Heiti,"println")||UNICODE_VALUE(Heiti,"Skrift")||UNICODE_VALUE(Heiti,"skrifa_lína"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Heiti,"print")||UNICODE_VALUE(Heiti,"Skrift")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Heiti,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!sýndar_CALL&&UNICODE_VALUE(eigandi_hlutur,"Íslenska/eigin/Skrá")){
        if(UNICODE_VALUE(Heiti,"Skrift")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Heiti,"Lestur")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    upplýsingatækni_ógilt=1;
}
static void þýða_aðferð(unsigned LOOKUP_INDEX){
    aðferð_færsla*Hópur_breyta_stærð=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Hópur_breyta_stærð->Heiti,"<init>"))return;int NIÐURSTAÐA,vara_COUNT=서술자(Hópur_breyta_stærð->서술값,&NIÐURSTAÐA);if(vara_COUNT<0){upplýsingatækni_ógilt=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<vara_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!vara_COUNT)내보내기("void");
    if((unsigned)vara_COUNT>Hópur_breyta_stærð->지역변수들){upplýsingatækni_ógilt=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Hópur_breyta_stærð->지역변수들?Hópur_breyta_stærð->지역변수들:1);for(int 순번=0;순번<vara_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=lengd_VALUE;lengd_VALUE=Hópur_breyta_stærð->skipun_SEQUENCE+Hópur_breyta_stærð->Stærð;현재위치=Hópur_breyta_stærð->skipun_SEQUENCE;
    while(현재위치<lengd_VALUE&&!upplýsingatækni_ógilt){unsigned skipun_staða=현재위치-Hópur_breyta_stærð->skipun_SEQUENCE,aðgerð_VALUE=bæti_gögn();내보내기("L%u:;",skipun_staða);
        if(aðgerð_VALUE==0){}
        else if(aðgerð_VALUE==1)내보내기("P(0);");
        else if(aðgerð_VALUE>=2&&aðgerð_VALUE<=8)내보내기("P(%uU);",aðgerð_VALUE-3);
        else if(aðgerð_VALUE==16){int VALUE=(int8_t)bæti_gögn();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(aðgerð_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(aðgerð_VALUE==18||aðgerð_VALUE==19)fasti_VALUE(aðgerð_VALUE==18?bæti_gögn():절반값());
        else if(aðgerð_VALUE==21||aðgerð_VALUE==25){unsigned 순번=bæti_gögn();if(순번>=Hópur_breyta_stærð->지역변수들)upplýsingatækni_ógilt=1;내보내기("P(v[%u]);",순번);}
        else if((aðgerð_VALUE>=26&&aðgerð_VALUE<=29)||(aðgerð_VALUE>=42&&aðgerð_VALUE<=45)){unsigned 순번=aðgerð_VALUE>=42?aðgerð_VALUE-42:aðgerð_VALUE-26;if(순번>=Hópur_breyta_stærð->지역변수들)upplýsingatækni_ógilt=1;내보내기("P(v[%u]);",순번);}
        else if(aðgerð_VALUE==54||aðgerð_VALUE==58){unsigned 순번=bæti_gögn();if(순번>=Hópur_breyta_stærð->지역변수들)upplýsingatækni_ógilt=1;내보내기("v[%u]=Q();",순번);}
        else if((aðgerð_VALUE>=59&&aðgerð_VALUE<=62)||(aðgerð_VALUE>=75&&aðgerð_VALUE<=78)){unsigned 순번=aðgerð_VALUE>=75?aðgerð_VALUE-75:aðgerð_VALUE-59;if(순번>=Hópur_breyta_stærð->지역변수들)upplýsingatækni_ógilt=1;내보내기("v[%u]=Q();",순번);}
        else if(aðgerð_VALUE==46||aðgerð_VALUE==50||aðgerð_VALUE==51||aðgerð_VALUE==52||aðgerð_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(aðgerð_VALUE==79||aðgerð_VALUE==83||aðgerð_VALUE==84||aðgerð_VALUE==85||aðgerð_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",aðgerð_VALUE==84?"(unsigned)(signed char)q":aðgerð_VALUE==85?"(unsigned short)q":aðgerð_VALUE==86?"(unsigned)(short)q":"q");
        else if(aðgerð_VALUE==87)내보내기("Q();");
        else if(aðgerð_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(aðgerð_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(aðgerð_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(aðgerð_VALUE==96||aðgerð_VALUE==100||aðgerð_VALUE==104||aðgerð_VALUE==120||aðgerð_VALUE==124||aðgerð_VALUE==126||aðgerð_VALUE==128||aðgerð_VALUE==130){const char*kóðun_VALUE=aðgerð_VALUE==96?"+":aðgerð_VALUE==100?"-":aðgerð_VALUE==104?"*":aðgerð_VALUE==120?"<<":aðgerð_VALUE==124?">>":aðgerð_VALUE==126?"&":aðgerð_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kóðun_VALUE,aðgerð_VALUE==120||aðgerð_VALUE==124?"%32":"");}
        else if(aðgerð_VALUE==108||aðgerð_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",aðgerð_VALUE==112);
        else if(aðgerð_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(aðgerð_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(aðgerð_VALUE==132){unsigned 순번=bæti_gögn();int 차이=(int8_t)bæti_gögn();if(순번>=Hópur_breyta_stærð->지역변수들)upplýsingatækni_ógilt=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(aðgerð_VALUE>=145&&aðgerð_VALUE<=147)내보내기("P((unsigned)(%s)Q());",aðgerð_VALUE==145?"signed char":aðgerð_VALUE==146?"unsigned short":"short");
        else if(aðgerð_VALUE>=153&&aðgerð_VALUE<=166){int markmið=(int)skipun_staða+(int16_t)절반값();const char*Samanburður_VALUE[]={"==","!=","<",">=",">","<="};if(markmið<0||markmið>=(int)Hópur_breyta_stærð->Stærð){upplýsingatækni_ógilt=1;break;}if(aðgerð_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Samanburður_VALUE[aðgerð_VALUE-153],markmið);else if(aðgerð_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Samanburður_VALUE[aðgerð_VALUE-159],markmið);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",aðgerð_VALUE==165?"==":"!=",markmið);}
        else if(aðgerð_VALUE==167){int markmið=(int)skipun_staða+(int16_t)절반값();if(markmið<0||markmið>=(int)Hópur_breyta_stærð->Stærð)upplýsingatækni_ógilt=1;내보내기("goto L%d;",markmið);}
        else if(aðgerð_VALUE==172||aðgerð_VALUE==176)내보내기("return Q();");else if(aðgerð_VALUE==177)내보내기("return 0;");
        else if(aðgerð_VALUE==178||aðgerð_VALUE==179){unsigned auðkenni_VALUE=절반값();if(auðkenni_VALUE<1||auðkenni_VALUE>=fasti_hópur||Merki_Listi[auðkenni_VALUE]!=9||첫째값[auðkenni_VALUE]>=fasti_hópur||SECOND_VALUE[auðkenni_VALUE]>=fasti_hópur||Merki_Listi[첫째값[auðkenni_VALUE]]!=7||Merki_Listi[SECOND_VALUE[auðkenni_VALUE]]!=12){upplýsingatækni_ógilt=1;break;}unsigned eigandi_hlutur=첫째값[첫째값[auðkenni_VALUE]],Heiti=첫째값[SECOND_VALUE[auðkenni_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[auðkenni_VALUE]];
            if(aðgerð_VALUE==178&&UNICODE_VALUE(eigandi_hlutur,"java/lang/System")&&UNICODE_VALUE(Heiti,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned skrá_færsla_3d0c1245=0;while(skrá_færsla_3d0c1245<필드개수&&(!같음(Heiti,heiti_reits[skrá_færsla_3d0c1245])||!같음(서술값,필드서술[skrá_færsla_3d0c1245])))skrá_færsla_3d0c1245++;if(!같음(eigandi_hlutur,첫째값[현재클래스])||skrá_færsla_3d0c1245==필드개수){upplýsingatækni_ógilt=1;break;}내보내기(aðgerð_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",skrá_færsla_3d0c1245);}}
        else if(aðgerð_VALUE==182||aðgerð_VALUE==184)호출(절반값(),aðgerð_VALUE==182);
        else if(aðgerð_VALUE==188){unsigned TYPE_tegund=bæti_gögn();if(TYPE_tegund!=4&&TYPE_tegund!=5&&TYPE_tegund!=8&&TYPE_tegund!=9&&TYPE_tegund!=10)upplýsingatækni_ógilt=1;내보내기("P(jarray((int)Q()));");}
        else if(aðgerð_VALUE==190)내보내기("P(jlength(Q()));");
        else if(aðgerð_VALUE==198||aðgerð_VALUE==199){int markmið=(int)skipun_staða+(int16_t)절반값();if(markmið<0||markmið>=(int)Hópur_breyta_stærð->Stærð)upplýsingatækni_ógilt=1;내보내기("if(Q()%s0)goto L%d;",aðgerð_VALUE==198?"==":"!=",markmið);}
        else upplýsingatækni_ógilt=1;
        if(upplýsingatækni_ógilt)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,aðgerð_VALUE,skipun_staða);
        내보내기("\n");
    }
    lengd_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned strengur_eining(unsigned *gögn_staða,unsigned ljúka_OFFSET){
    if(*gögn_staða>=ljúka_OFFSET){upplýsingatækni_ógilt=1;return 0;}unsigned stafkóði=gögn[(*gögn_staða)++];
    if(stafkóði<128)return stafkóði;
    unsigned vara_COUNT=stafkóði>=0xc0&&stafkóði<=0xdf?1:stafkóði>=0xe0&&stafkóði<=0xef?2:3;
    if(vara_COUNT==3||vara_COUNT>ljúka_OFFSET-*gögn_staða){upplýsingatækni_ógilt=1;return 0;}unsigned VALUE=stafkóði&((1u<<(6-vara_COUNT))-1);
    for(unsigned 순번=0;순번<vara_COUNT;순번++){unsigned Áfram_vara=gögn[(*gögn_staða)++];if((Áfram_vara&0xc0)!=0x80)upplýsingatækni_ógilt=1;VALUE=VALUE<<6|(Áfram_vara&63);}
    if((vara_COUNT==1&&VALUE<128&&VALUE!=0)||(vara_COUNT==2&&VALUE<2048))upplýsingatækni_ógilt=1;return VALUE;
}
static void strengur_fasti(unsigned auðkenni_VALUE){
    unsigned 부호없는값=첫째값[auðkenni_VALUE];if(부호없는값<1||부호없는값>=fasti_hópur||Merki_Listi[부호없는값]!=1){upplýsingatækni_ógilt=1;return;}내보내기("static const unsigned char k%u[]={",auðkenni_VALUE);
    unsigned gögn_staða=첫째값[부호없는값],ljúka_OFFSET=gögn_staða+SECOND_VALUE[부호없는값];
    while(gögn_staða<ljúka_OFFSET&&!upplýsingatækni_ógilt){unsigned stafkóði=strengur_eining(&gögn_staða,ljúka_OFFSET);
        if(stafkóði>=0xd800&&stafkóði<=0xdbff){unsigned 낮은부분=strengur_eining(&gögn_staða,ljúka_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){upplýsingatækni_ógilt=1;break;}stafkóði=0x10000+((stafkóði-0xd800)<<10)+낮은부분-0xdc00;}
        else if(stafkóði>=0xdc00&&stafkóði<=0xdfff){upplýsingatækni_ógilt=1;break;}
        if(!stafkóði){printf("jaot: embedded NUL string needs JVM mode\n");upplýsingatækni_ógilt=1;break;}
        if(stafkóði<128)내보내기("%u,",stafkóði);
        else{unsigned vara_COUNT=stafkóði<2048?2:stafkóði<65536?3:4;내보내기("%u,",(vara_COUNT==2?0xc0:vara_COUNT==3?0xe0:0xf0)|(stafkóði>>(6*(vara_COUNT-1))));for(unsigned 순번=vara_COUNT-1;순번;순번--)내보내기("%u,",0x80|((stafkóði>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Heiti){
    size_t vara_COUNT=strlen(Heiti);
    if(vara_COUNT>4&&!strcmp(Heiti+vara_COUNT-4,".jar")){
        if(꾸러미열기(Heiti)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char SLÓÐ[256];const char*færsla_aðferð=꾸러미진입클래스();vara_COUNT=strlen(færsla_aðferð);if(vara_COUNT+6>=sizeof(SLÓÐ))return 0;
        for(unsigned 순번=0;순번<vara_COUNT;순번++)SLÓÐ[순번]=færsla_aðferð[순번]=='.'?'/':færsla_aðferð[순번];strcpy(SLÓÐ+vara_COUNT,".class");int færsla_COUNT=꾸러미읽기(SLÓÐ,gögn,sizeof(gögn));if(færsla_COUNT<0)return 0;lengd_VALUE=færsla_COUNT;
    }else{intptr_t skrá_hald=사용자호출(3,(uintptr_t)Heiti,0,0,0,0,0);if(skrá_hald<0)return 0;intptr_t færsla_COUNT=사용자호출(9,skrá_hald,0,0,0,0,0);if(færsla_COUNT<0||færsla_COUNT>sizeof(gögn)){사용자호출(4,skrá_hald,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,skrá_hald,(uintptr_t)gögn,færsla_COUNT,0,0,0);사용자호출(4,skrá_hald,0,0,0,0,0);if(RECEIVED_COUNT!=færsla_COUNT)return 0;lengd_VALUE=færsla_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<fasti_hópur&&!upplýsingatækni_ógilt;순번++)if(Merki_Listi[순번]==8)strengur_fasti(순번);
    if(upplýsingatækni_ógilt)return 0;
    int færsla_P=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Heiti,"<init>")){
        int NIÐURSTAÐA,færsla_COUNT=서술자(메소드목록[순번].서술값,&NIÐURSTAÐA);if(færsla_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<færsla_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!færsla_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Heiti,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].afbrigði_Background_Intelligent_Transfer_Service&9)==9)færsla_P=순번;
        if(UNICODE_VALUE(메소드목록[순번].Heiti,"<clinit>"))초기값=순번;
    }
    if(færsla_P<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!upplýsingatækni_ógilt;순번++)þýða_aðferð(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(reitur_fasti[순번]){
        unsigned stafkóði=reitur_fasti[순번];if(stafkóði>=fasti_hópur)return 0;
        if(Merki_Listi[stafkóði]==3)내보내기("fields[%u]=%uU;",순번,첫째값[stafkóði]);else if(Merki_Listi[stafkóði]==8)내보내기("fields[%u]=(W)k%u;",순번,stafkóði);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",færsla_P);
    return upplýsingatækni_ógilt?0:Texti;
}
