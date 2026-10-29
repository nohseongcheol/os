#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "kogum.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char andmed[16384];static unsigned 길이,tähtaja_piires_ametikoht;static int infotehnoloogia_kehtetu;
static unsigned Sildid_Loend[512],첫째값[512],SECOND_VALUE[512],konstant_kaust,tähtaja_piires_tund;
static char Tekst[65536];static unsigned Teksti_suurus;
typedef struct {unsigned konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus,Nimi_2,서술값,명령열,Suurus,지역변수들,Virn_salvesti;} meetod_kirje;
static meetod_kirje 메소드목록[64];static unsigned 메소드개수;
static unsigned väljanimi[64],필드서술[64],väli_konstant[64],필드개수;
static unsigned TAKE_VALUE(unsigned kaup_COUNT){if(tähtaja_piires_ametikoht>길이||kaup_COUNT>길이-tähtaja_piires_ametikoht){infotehnoloogia_kehtetu=1;return 0;}unsigned andmed_ametikoht=tähtaja_piires_ametikoht;tähtaja_piires_ametikoht+=kaup_COUNT;return andmed_ametikoht;}
static unsigned bait_andmed(void){unsigned andmed_ametikoht=TAKE_VALUE(1);return infotehnoloogia_kehtetu?0:andmed[andmed_ametikoht];}
static unsigned 절반값(void){unsigned 가로좌표=bait_andmed();return 가로좌표<<8|bait_andmed();}
static uint32_t 가득참(void){uint32_t 가로좌표=절반값();return 가로좌표<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*string_andmed){return 순번>0&&순번<konstant_kaust&&Sildid_Loend[순번]==1&&strlen(string_andmed)==SECOND_VALUE[순번]&&!memcmp(andmed+첫째값[순번],string_andmed,SECOND_VALUE[순번]);}
static int 같음(unsigned 가로좌표,unsigned 세로좌표){return 가로좌표>0&&가로좌표<konstant_kaust&&세로좌표>0&&세로좌표<konstant_kaust&&Sildid_Loend[가로좌표]==1&&Sildid_Loend[세로좌표]==1&&SECOND_VALUE[가로좌표]==SECOND_VALUE[세로좌표]&&!memcmp(andmed+첫째값[가로좌표],andmed+첫째값[세로좌표],SECOND_VALUE[가로좌표]);}
static void 내보내기(const char*Fail_kirje,...){if(infotehnoloogia_kehtetu)return;va_list argument_ARRAY;va_start(argument_ARRAY,Fail_kirje);int kaup_COUNT=vsnprintf(Tekst+Teksti_suurus,sizeof(Tekst)-Teksti_suurus,Fail_kirje,argument_ARRAY);va_end(argument_ARRAY);if(kaup_COUNT<0||(unsigned)kaup_COUNT>=sizeof(Tekst)-Teksti_suurus){infotehnoloogia_kehtetu=1;return;}Teksti_suurus+=kaup_COUNT;}
static int 서술자(unsigned identifikaator_VALUE,int*TULEMUS){
    if(identifikaator_VALUE<1||identifikaator_VALUE>=konstant_kaust||Sildid_Loend[identifikaator_VALUE]!=1)return -1;unsigned andmed_ametikoht=첫째값[identifikaator_VALUE],lõpeta_kõne_nihe=andmed_ametikoht+SECOND_VALUE[identifikaator_VALUE];if(andmed_ametikoht>=lõpeta_kõne_nihe||andmed[andmed_ametikoht++]!='(')return -1;int kirje_COUNT=0;
    while(andmed_ametikoht<lõpeta_kõne_nihe&&andmed[andmed_ametikoht]!=')'){
        unsigned koodipunkt=andmed[andmed_ametikoht++];while(koodipunkt=='['&&andmed_ametikoht<lõpeta_kõne_nihe)koodipunkt=andmed[andmed_ametikoht++];
        if(koodipunkt=='L'){while(andmed_ametikoht<lõpeta_kõne_nihe&&andmed[andmed_ametikoht]!=';')andmed_ametikoht++;if(andmed_ametikoht==lõpeta_kõne_nihe)return -1;andmed_ametikoht++;}
        else if(koodipunkt!='I'&&koodipunkt!='Z'&&koodipunkt!='B'&&koodipunkt!='C'&&koodipunkt!='S')return -1;
        if(++kirje_COUNT>16)return -1;
    }
    if(andmed_ametikoht+1>=lõpeta_kõne_nihe||andmed[andmed_ametikoht++]!=')')return -1;*TULEMUS=andmed[andmed_ametikoht]=='V'?0:1;
    if(andmed[andmed_ametikoht]=='J'||andmed[andmed_ametikoht]=='D'||andmed[andmed_ametikoht]=='F')return -1;return kirje_COUNT;
}
static void füüsilised_andmed(void){unsigned kaup_COUNT=절반값();for(unsigned 순번=0;순번<kaup_COUNT&&!infotehnoloogia_kehtetu;순번++){절반값();unsigned Suurus=가득참();TAKE_VALUE(Suurus);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned vaheversioon=절반값(),versiooninumber=절반값();if(vaheversioon||versiooninumber<45||versiooninumber>52)return -1;
    konstant_kaust=절반값();if(konstant_kaust<1||konstant_kaust>512)return -1;
    for(unsigned 순번=1;순번<konstant_kaust&&!infotehnoloogia_kehtetu;순번++){
        Sildid_Loend[순번]=bait_andmed();switch(Sildid_Loend[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstant_kaust)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bait_andmed();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();tähtaja_piires_tund=절반값();절반값();if(tähtaja_piires_tund<1||tähtaja_piires_tund>=konstant_kaust||Sildid_Loend[tähtaja_piires_tund]!=7||첫째값[tähtaja_piires_tund]<1||첫째값[tähtaja_piires_tund]>=konstant_kaust||Sildid_Loend[첫째값[tähtaja_piires_tund]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!infotehnoloogia_kehtetu;순번++){
        unsigned konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus=절반값();väljanimi[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&8))return -1;
        unsigned kirje_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<kirje_COUNT&&!infotehnoloogia_kehtetu;안쪽순번++){
            unsigned Nimi_2=절반값(),Suurus=가득참();
            if(UNICODE_VALUE(Nimi_2,"ConstantValue")){if(Suurus!=2)return -1;väli_konstant[순번]=절반값();}
            else TAKE_VALUE(Suurus);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!infotehnoloogia_kehtetu;순번++){
        meetod_kirje*Rühm_suurust_muutma=메소드목록+순번;Rühm_suurust_muutma->konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus=절반값();Rühm_suurust_muutma->Nimi_2=절반값();Rühm_suurust_muutma->서술값=절반값();unsigned kirje_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<kirje_COUNT&&!infotehnoloogia_kehtetu;안쪽순번++){
            unsigned Nimi_2=절반값(),Suurus=가득참(),Käivita_2=tähtaja_piires_ametikoht;
            if(Suurus>길이-tähtaja_piires_ametikoht)return -1;
            if(UNICODE_VALUE(Nimi_2,"Code")){
                Rühm_suurust_muutma->Virn_salvesti=절반값();Rühm_suurust_muutma->지역변수들=절반값();Rühm_suurust_muutma->Suurus=가득참();Rühm_suurust_muutma->명령열=TAKE_VALUE(Rühm_suurust_muutma->Suurus);
                if(Rühm_suurust_muutma->Virn_salvesti>128||Rühm_suurust_muutma->지역변수들>128||Rühm_suurust_muutma->Suurus>8192||절반값())return -1;füüsilised_andmed();
            }else TAKE_VALUE(Suurus);
            if(tähtaja_piires_ametikoht!=Käivita_2+Suurus)return -1;
        }
        if(!UNICODE_VALUE(Rühm_suurust_muutma->Nimi_2,"<init>")&&(!(Rühm_suurust_muutma->konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&8)||(Rühm_suurust_muutma->konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&(0x100|0x20))||!Rühm_suurust_muutma->Suurus))return -1;
    }
    füüsilised_andmed();return infotehnoloogia_kehtetu||tähtaja_piires_ametikoht!=길이?-1:0;
}
static void konstant_VALUE(unsigned identifikaator_VALUE){
    if(!identifikaator_VALUE||identifikaator_VALUE>=konstant_kaust){infotehnoloogia_kehtetu=1;return;}
    if(Sildid_Loend[identifikaator_VALUE]==3)내보내기("P(%uU);",첫째값[identifikaator_VALUE]);
    else if(Sildid_Loend[identifikaator_VALUE]==8)내보내기("P((W)k%u);",identifikaator_VALUE);else infotehnoloogia_kehtetu=1;
}
static void 호출(unsigned identifikaator_VALUE,int 가상호출){
    if(identifikaator_VALUE<1||identifikaator_VALUE>=konstant_kaust||(Sildid_Loend[identifikaator_VALUE]!=10&&Sildid_Loend[identifikaator_VALUE]!=11)||첫째값[identifikaator_VALUE]<1||첫째값[identifikaator_VALUE]>=konstant_kaust||Sildid_Loend[첫째값[identifikaator_VALUE]]!=7||SECOND_VALUE[identifikaator_VALUE]<1||SECOND_VALUE[identifikaator_VALUE]>=konstant_kaust||Sildid_Loend[SECOND_VALUE[identifikaator_VALUE]]!=12){infotehnoloogia_kehtetu=1;return;}
    unsigned omanik_objekt=첫째값[첫째값[identifikaator_VALUE]],Nimi_2=첫째값[SECOND_VALUE[identifikaator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikaator_VALUE]];int TULEMUS=0,kaup_COUNT=서술자(서술값,&TULEMUS);if(kaup_COUNT<0){infotehnoloogia_kehtetu=1;return;}
    for(int 순번=kaup_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(가상호출)내보내기("Q();");
    if(!가상호출&&같음(omanik_objekt,첫째값[tähtaja_piires_tund])){
        unsigned Rühm_suurust_muutma=0;for(;Rühm_suurust_muutma<메소드개수;Rühm_suurust_muutma++)if(같음(Nimi_2,메소드목록[Rühm_suurust_muutma].Nimi_2)&&같음(서술값,메소드목록[Rühm_suurust_muutma].서술값))break;
        if(Rühm_suurust_muutma==메소드개수||!(메소드목록[Rühm_suurust_muutma].konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&8)){infotehnoloogia_kehtetu=1;return;}
        if(TULEMUS)내보내기("P(");내보내기("m%u(",Rühm_suurust_muutma);for(int 순번=0;순번<kaup_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(TULEMUS?"));":" );");return;
    }
    if((가상호출&&UNICODE_VALUE(omanik_objekt,"java/io/PrintStream")&& (UNICODE_VALUE(Nimi_2,"print")||UNICODE_VALUE(Nimi_2,"println")))||(!가상호출&&UNICODE_VALUE(omanik_objekt,"Eesti/oma/Väljund"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Nimi_2,"print")||UNICODE_VALUE(Nimi_2,"println")||UNICODE_VALUE(Nimi_2,"kirjutamine_number"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Nimi_2,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Nimi_2,"print")||UNICODE_VALUE(Nimi_2,"println")||UNICODE_VALUE(Nimi_2,"Kirjutamine")||UNICODE_VALUE(Nimi_2,"kirjutamine_liin"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Nimi_2,"print")||UNICODE_VALUE(Nimi_2,"Kirjutamine")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Nimi_2,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!가상호출&&UNICODE_VALUE(omanik_objekt,"Eesti/oma/Fail")){
        if(UNICODE_VALUE(Nimi_2,"Kirjutamine")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Nimi_2,"Lugemine")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    infotehnoloogia_kehtetu=1;
}
static void kompileerima_meetod(unsigned LOOKUP_INDEX){
    meetod_kirje*Rühm_suurust_muutma=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Rühm_suurust_muutma->Nimi_2,"<init>"))return;int TULEMUS,kaup_COUNT=서술자(Rühm_suurust_muutma->서술값,&TULEMUS);if(kaup_COUNT<0){infotehnoloogia_kehtetu=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<kaup_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!kaup_COUNT)내보내기("void");
    if((unsigned)kaup_COUNT>Rühm_suurust_muutma->지역변수들){infotehnoloogia_kehtetu=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Rühm_suurust_muutma->지역변수들?Rühm_suurust_muutma->지역변수들:1);for(int 순번=0;순번<kaup_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=길이;길이=Rühm_suurust_muutma->명령열+Rühm_suurust_muutma->Suurus;tähtaja_piires_ametikoht=Rühm_suurust_muutma->명령열;
    while(tähtaja_piires_ametikoht<길이&&!infotehnoloogia_kehtetu){unsigned käsk_ametikoht=tähtaja_piires_ametikoht-Rühm_suurust_muutma->명령열,lõikus_VALUE=bait_andmed();내보내기("L%u:;",käsk_ametikoht);
        if(lõikus_VALUE==0){}
        else if(lõikus_VALUE==1)내보내기("P(0);");
        else if(lõikus_VALUE>=2&&lõikus_VALUE<=8)내보내기("P(%uU);",lõikus_VALUE-3);
        else if(lõikus_VALUE==16){int VALUE=(int8_t)bait_andmed();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(lõikus_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(lõikus_VALUE==18||lõikus_VALUE==19)konstant_VALUE(lõikus_VALUE==18?bait_andmed():절반값());
        else if(lõikus_VALUE==21||lõikus_VALUE==25){unsigned 순번=bait_andmed();if(순번>=Rühm_suurust_muutma->지역변수들)infotehnoloogia_kehtetu=1;내보내기("P(v[%u]);",순번);}
        else if((lõikus_VALUE>=26&&lõikus_VALUE<=29)||(lõikus_VALUE>=42&&lõikus_VALUE<=45)){unsigned 순번=lõikus_VALUE>=42?lõikus_VALUE-42:lõikus_VALUE-26;if(순번>=Rühm_suurust_muutma->지역변수들)infotehnoloogia_kehtetu=1;내보내기("P(v[%u]);",순번);}
        else if(lõikus_VALUE==54||lõikus_VALUE==58){unsigned 순번=bait_andmed();if(순번>=Rühm_suurust_muutma->지역변수들)infotehnoloogia_kehtetu=1;내보내기("v[%u]=Q();",순번);}
        else if((lõikus_VALUE>=59&&lõikus_VALUE<=62)||(lõikus_VALUE>=75&&lõikus_VALUE<=78)){unsigned 순번=lõikus_VALUE>=75?lõikus_VALUE-75:lõikus_VALUE-59;if(순번>=Rühm_suurust_muutma->지역변수들)infotehnoloogia_kehtetu=1;내보내기("v[%u]=Q();",순번);}
        else if(lõikus_VALUE==46||lõikus_VALUE==50||lõikus_VALUE==51||lõikus_VALUE==52||lõikus_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(lõikus_VALUE==79||lõikus_VALUE==83||lõikus_VALUE==84||lõikus_VALUE==85||lõikus_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",lõikus_VALUE==84?"(unsigned)(signed char)q":lõikus_VALUE==85?"(unsigned short)q":lõikus_VALUE==86?"(unsigned)(short)q":"q");
        else if(lõikus_VALUE==87)내보내기("Q();");
        else if(lõikus_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(lõikus_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(lõikus_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(lõikus_VALUE==96||lõikus_VALUE==100||lõikus_VALUE==104||lõikus_VALUE==120||lõikus_VALUE==124||lõikus_VALUE==126||lõikus_VALUE==128||lõikus_VALUE==130){const char*kodeerimine_VALUE=lõikus_VALUE==96?"+":lõikus_VALUE==100?"-":lõikus_VALUE==104?"*":lõikus_VALUE==120?"<<":lõikus_VALUE==124?">>":lõikus_VALUE==126?"&":lõikus_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodeerimine_VALUE,lõikus_VALUE==120||lõikus_VALUE==124?"%32":"");}
        else if(lõikus_VALUE==108||lõikus_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",lõikus_VALUE==112);
        else if(lõikus_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(lõikus_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(lõikus_VALUE==132){unsigned 순번=bait_andmed();int 차이=(int8_t)bait_andmed();if(순번>=Rühm_suurust_muutma->지역변수들)infotehnoloogia_kehtetu=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(lõikus_VALUE>=145&&lõikus_VALUE<=147)내보내기("P((unsigned)(%s)Q());",lõikus_VALUE==145?"signed char":lõikus_VALUE==146?"unsigned short":"short");
        else if(lõikus_VALUE>=153&&lõikus_VALUE<=166){int siht=(int)käsk_ametikoht+(int16_t)절반값();const char*Võrdlus_VALUE[]={"==","!=","<",">=",">","<="};if(siht<0||siht>=(int)Rühm_suurust_muutma->Suurus){infotehnoloogia_kehtetu=1;break;}if(lõikus_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Võrdlus_VALUE[lõikus_VALUE-153],siht);else if(lõikus_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Võrdlus_VALUE[lõikus_VALUE-159],siht);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",lõikus_VALUE==165?"==":"!=",siht);}
        else if(lõikus_VALUE==167){int siht=(int)käsk_ametikoht+(int16_t)절반값();if(siht<0||siht>=(int)Rühm_suurust_muutma->Suurus)infotehnoloogia_kehtetu=1;내보내기("goto L%d;",siht);}
        else if(lõikus_VALUE==172||lõikus_VALUE==176)내보내기("return Q();");else if(lõikus_VALUE==177)내보내기("return 0;");
        else if(lõikus_VALUE==178||lõikus_VALUE==179){unsigned identifikaator_VALUE=절반값();if(identifikaator_VALUE<1||identifikaator_VALUE>=konstant_kaust||Sildid_Loend[identifikaator_VALUE]!=9||첫째값[identifikaator_VALUE]>=konstant_kaust||SECOND_VALUE[identifikaator_VALUE]>=konstant_kaust||Sildid_Loend[첫째값[identifikaator_VALUE]]!=7||Sildid_Loend[SECOND_VALUE[identifikaator_VALUE]]!=12){infotehnoloogia_kehtetu=1;break;}unsigned omanik_objekt=첫째값[첫째값[identifikaator_VALUE]],Nimi_2=첫째값[SECOND_VALUE[identifikaator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikaator_VALUE]];
            if(lõikus_VALUE==178&&UNICODE_VALUE(omanik_objekt,"java/lang/System")&&UNICODE_VALUE(Nimi_2,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Fail_kirje=0;while(Fail_kirje<필드개수&&(!같음(Nimi_2,väljanimi[Fail_kirje])||!같음(서술값,필드서술[Fail_kirje])))Fail_kirje++;if(!같음(omanik_objekt,첫째값[tähtaja_piires_tund])||Fail_kirje==필드개수){infotehnoloogia_kehtetu=1;break;}내보내기(lõikus_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",Fail_kirje);}}
        else if(lõikus_VALUE==182||lõikus_VALUE==184)호출(절반값(),lõikus_VALUE==182);
        else if(lõikus_VALUE==188){unsigned TYPE_ala=bait_andmed();if(TYPE_ala!=4&&TYPE_ala!=5&&TYPE_ala!=8&&TYPE_ala!=9&&TYPE_ala!=10)infotehnoloogia_kehtetu=1;내보내기("P(jarray((int)Q()));");}
        else if(lõikus_VALUE==190)내보내기("P(jlength(Q()));");
        else if(lõikus_VALUE==198||lõikus_VALUE==199){int siht=(int)käsk_ametikoht+(int16_t)절반값();if(siht<0||siht>=(int)Rühm_suurust_muutma->Suurus)infotehnoloogia_kehtetu=1;내보내기("if(Q()%s0)goto L%d;",lõikus_VALUE==198?"==":"!=",siht);}
        else infotehnoloogia_kehtetu=1;
        if(infotehnoloogia_kehtetu)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,lõikus_VALUE,käsk_ametikoht);
        내보내기("\n");
    }
    길이=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned string_ühik(unsigned *andmed_ametikoht,unsigned lõpeta_kõne_nihe){
    if(*andmed_ametikoht>=lõpeta_kõne_nihe){infotehnoloogia_kehtetu=1;return 0;}unsigned koodipunkt=andmed[(*andmed_ametikoht)++];
    if(koodipunkt<128)return koodipunkt;
    unsigned kaup_COUNT=koodipunkt>=0xc0&&koodipunkt<=0xdf?1:koodipunkt>=0xe0&&koodipunkt<=0xef?2:3;
    if(kaup_COUNT==3||kaup_COUNT>lõpeta_kõne_nihe-*andmed_ametikoht){infotehnoloogia_kehtetu=1;return 0;}unsigned VALUE=koodipunkt&((1u<<(6-kaup_COUNT))-1);
    for(unsigned 순번=0;순번<kaup_COUNT;순번++){unsigned Edasi_kaup=andmed[(*andmed_ametikoht)++];if((Edasi_kaup&0xc0)!=0x80)infotehnoloogia_kehtetu=1;VALUE=VALUE<<6|(Edasi_kaup&63);}
    if((kaup_COUNT==1&&VALUE<128&&VALUE!=0)||(kaup_COUNT==2&&VALUE<2048))infotehnoloogia_kehtetu=1;return VALUE;
}
static void string_konstant(unsigned identifikaator_VALUE){
    unsigned 부호없는값=첫째값[identifikaator_VALUE];if(부호없는값<1||부호없는값>=konstant_kaust||Sildid_Loend[부호없는값]!=1){infotehnoloogia_kehtetu=1;return;}내보내기("static const unsigned char k%u[]={",identifikaator_VALUE);
    unsigned andmed_ametikoht=첫째값[부호없는값],lõpeta_kõne_nihe=andmed_ametikoht+SECOND_VALUE[부호없는값];
    while(andmed_ametikoht<lõpeta_kõne_nihe&&!infotehnoloogia_kehtetu){unsigned koodipunkt=string_ühik(&andmed_ametikoht,lõpeta_kõne_nihe);
        if(koodipunkt>=0xd800&&koodipunkt<=0xdbff){unsigned 낮은부분=string_ühik(&andmed_ametikoht,lõpeta_kõne_nihe);if(낮은부분<0xdc00||낮은부분>0xdfff){infotehnoloogia_kehtetu=1;break;}koodipunkt=0x10000+((koodipunkt-0xd800)<<10)+낮은부분-0xdc00;}
        else if(koodipunkt>=0xdc00&&koodipunkt<=0xdfff){infotehnoloogia_kehtetu=1;break;}
        if(!koodipunkt){printf("jaot: embedded NUL string needs JVM mode\n");infotehnoloogia_kehtetu=1;break;}
        if(koodipunkt<128)내보내기("%u,",koodipunkt);
        else{unsigned kaup_COUNT=koodipunkt<2048?2:koodipunkt<65536?3:4;내보내기("%u,",(kaup_COUNT==2?0xc0:kaup_COUNT==3?0xe0:0xf0)|(koodipunkt>>(6*(kaup_COUNT-1))));for(unsigned 순번=kaup_COUNT-1;순번;순번--)내보내기("%u,",0x80|((koodipunkt>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nimi_2){
    size_t kaup_COUNT=strlen(Nimi_2);
    if(kaup_COUNT>4&&!strcmp(Nimi_2+kaup_COUNT-4,".jar")){
        if(꾸러미열기(Nimi_2)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char RADA[256];const char*kirje_meetod=꾸러미진입클래스();kaup_COUNT=strlen(kirje_meetod);if(kaup_COUNT+6>=sizeof(RADA))return 0;
        for(unsigned 순번=0;순번<kaup_COUNT;순번++)RADA[순번]=kirje_meetod[순번]=='.'?'/':kirje_meetod[순번];strcpy(RADA+kaup_COUNT,".class");int kirje_COUNT=꾸러미읽기(RADA,andmed,sizeof(andmed));if(kirje_COUNT<0)return 0;길이=kirje_COUNT;
    }else{intptr_t Fail_pide=사용자호출(3,(uintptr_t)Nimi_2,0,0,0,0,0);if(Fail_pide<0)return 0;intptr_t kirje_COUNT=사용자호출(9,Fail_pide,0,0,0,0,0);if(kirje_COUNT<0||kirje_COUNT>sizeof(andmed)){사용자호출(4,Fail_pide,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,Fail_pide,(uintptr_t)andmed,kirje_COUNT,0,0,0);사용자호출(4,Fail_pide,0,0,0,0,0);if(RECEIVED_COUNT!=kirje_COUNT)return 0;길이=kirje_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstant_kaust&&!infotehnoloogia_kehtetu;순번++)if(Sildid_Loend[순번]==8)string_konstant(순번);
    if(infotehnoloogia_kehtetu)return 0;
    int kirje_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Nimi_2,"<init>")){
        int TULEMUS,kirje_COUNT=서술자(메소드목록[순번].서술값,&TULEMUS);if(kirje_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<kirje_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!kirje_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Nimi_2,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&9)==9)kirje_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Nimi_2,"<clinit>"))초기값=순번;
    }
    if(kirje_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!infotehnoloogia_kehtetu;순번++)kompileerima_meetod(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(väli_konstant[순번]){
        unsigned koodipunkt=väli_konstant[순번];if(koodipunkt>=konstant_kaust)return 0;
        if(Sildid_Loend[koodipunkt]==3)내보내기("fields[%u]=%uU;",순번,첫째값[koodipunkt]);else if(Sildid_Loend[koodipunkt]==8)내보내기("fields[%u]=(W)k%u;",순번,koodipunkt);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",kirje_p);
    return infotehnoloogia_kehtetu?0:Tekst;
}
