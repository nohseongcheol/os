#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "grupoj.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char të_dhëna[16384];static unsigned gjatësi_VALUE,현재위치;static int teknologjia_e_informacionit_i_pavlefshëm;
static unsigned Shenjat_Listë[512],첫째값[512],SECOND_VALUE[512],konstante_kuotë,현재클래스;
static char Teksti[65536];static unsigned madhësia_e_tekstit;
typedef struct {unsigned konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond,Emër,서술값,instruksion_SEQUENCE,Madhësi,지역변수들,Stivë_hapësira_ruajtëse;} metoda_futje;
static metoda_futje 메소드목록[64];static unsigned 메소드개수;
static unsigned emri_i_fushës[64],필드서술[64],fushë_konstante[64],필드개수;
static unsigned TAKE_VALUE(unsigned njësi_COUNT){if(현재위치>gjatësi_VALUE||njësi_COUNT>gjatësi_VALUE-현재위치){teknologjia_e_informacionit_i_pavlefshëm=1;return 0;}unsigned të_dhëna_pozicioni=현재위치;현재위치+=njësi_COUNT;return të_dhëna_pozicioni;}
static unsigned bajt_të_dhëna(void){unsigned të_dhëna_pozicioni=TAKE_VALUE(1);return teknologjia_e_informacionit_i_pavlefshëm?0:të_dhëna[të_dhëna_pozicioni];}
static unsigned 절반값(void){unsigned koordinata_x=bajt_të_dhëna();return koordinata_x<<8|bajt_të_dhëna();}
static uint32_t 가득참(void){uint32_t koordinata_x=절반값();return koordinata_x<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*varg_të_dhëna){return 순번>0&&순번<konstante_kuotë&&Shenjat_Listë[순번]==1&&strlen(varg_të_dhëna)==SECOND_VALUE[순번]&&!memcmp(të_dhëna+첫째값[순번],varg_të_dhëna,SECOND_VALUE[순번]);}
static int 같음(unsigned koordinata_x,unsigned Y_koordinatë){return koordinata_x>0&&koordinata_x<konstante_kuotë&&Y_koordinatë>0&&Y_koordinatë<konstante_kuotë&&Shenjat_Listë[koordinata_x]==1&&Shenjat_Listë[Y_koordinatë]==1&&SECOND_VALUE[koordinata_x]==SECOND_VALUE[Y_koordinatë]&&!memcmp(të_dhëna+첫째값[koordinata_x],të_dhëna+첫째값[Y_koordinatë],SECOND_VALUE[koordinata_x]);}
static void 내보내기(const char*skedar_futje,...){if(teknologjia_e_informacionit_i_pavlefshëm)return;va_list argument_ARRAY;va_start(argument_ARRAY,skedar_futje);int njësi_COUNT=vsnprintf(Teksti+madhësia_e_tekstit,sizeof(Teksti)-madhësia_e_tekstit,skedar_futje,argument_ARRAY);va_end(argument_ARRAY);if(njësi_COUNT<0||(unsigned)njësi_COUNT>=sizeof(Teksti)-madhësia_e_tekstit){teknologjia_e_informacionit_i_pavlefshëm=1;return;}madhësia_e_tekstit+=njësi_COUNT;}
static int 서술자(unsigned identifikues_VALUE,int*llogaritje){
    if(identifikues_VALUE<1||identifikues_VALUE>=konstante_kuotë||Shenjat_Listë[identifikues_VALUE]!=1)return -1;unsigned të_dhëna_pozicioni=첫째값[identifikues_VALUE],mbaroj_OFFSET=të_dhëna_pozicioni+SECOND_VALUE[identifikues_VALUE];if(të_dhëna_pozicioni>=mbaroj_OFFSET||të_dhëna[të_dhëna_pozicioni++]!='(')return -1;int futje_COUNT=0;
    while(të_dhëna_pozicioni<mbaroj_OFFSET&&të_dhëna[të_dhëna_pozicioni]!=')'){
        unsigned kodi_i_karakterit=të_dhëna[të_dhëna_pozicioni++];while(kodi_i_karakterit=='['&&të_dhëna_pozicioni<mbaroj_OFFSET)kodi_i_karakterit=të_dhëna[të_dhëna_pozicioni++];
        if(kodi_i_karakterit=='L'){while(të_dhëna_pozicioni<mbaroj_OFFSET&&të_dhëna[të_dhëna_pozicioni]!=';')të_dhëna_pozicioni++;if(të_dhëna_pozicioni==mbaroj_OFFSET)return -1;të_dhëna_pozicioni++;}
        else if(kodi_i_karakterit!='I'&&kodi_i_karakterit!='Z'&&kodi_i_karakterit!='B'&&kodi_i_karakterit!='C'&&kodi_i_karakterit!='S')return -1;
        if(++futje_COUNT>16)return -1;
    }
    if(të_dhëna_pozicioni+1>=mbaroj_OFFSET||të_dhëna[të_dhëna_pozicioni++]!=')')return -1;*llogaritje=të_dhëna[të_dhëna_pozicioni]=='V'?0:1;
    if(të_dhëna[të_dhëna_pozicioni]=='J'||të_dhëna[të_dhëna_pozicioni]=='D'||të_dhëna[të_dhëna_pozicioni]=='F')return -1;return futje_COUNT;
}
static void atributet(void){unsigned njësi_COUNT=절반값();for(unsigned 순번=0;순번<njësi_COUNT&&!teknologjia_e_informacionit_i_pavlefshëm;순번++){절반값();unsigned Madhësi=가득참();TAKE_VALUE(Madhësi);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned i_mitur_version=절반값(),판번호=절반값();if(i_mitur_version||판번호<45||판번호>52)return -1;
    konstante_kuotë=절반값();if(konstante_kuotë<1||konstante_kuotë>512)return -1;
    for(unsigned 순번=1;순번<konstante_kuotë&&!teknologjia_e_informacionit_i_pavlefshëm;순번++){
        Shenjat_Listë[순번]=bajt_të_dhëna();switch(Shenjat_Listë[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstante_kuotë)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bajt_të_dhëna();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=konstante_kuotë||Shenjat_Listë[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=konstante_kuotë||Shenjat_Listë[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!teknologjia_e_informacionit_i_pavlefshëm;순번++){
        unsigned konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond=절반값();emri_i_fushës[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&8))return -1;
        unsigned futje_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<futje_COUNT&&!teknologjia_e_informacionit_i_pavlefshëm;안쪽순번++){
            unsigned Emër=절반값(),Madhësi=가득참();
            if(UNICODE_VALUE(Emër,"ConstantValue")){if(Madhësi!=2)return -1;fushë_konstante[순번]=절반값();}
            else TAKE_VALUE(Madhësi);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!teknologjia_e_informacionit_i_pavlefshëm;순번++){
        metoda_futje*grup_ndryshoj_përmasat=메소드목록+순번;grup_ndryshoj_përmasat->konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond=절반값();grup_ndryshoj_përmasat->Emër=절반값();grup_ndryshoj_përmasat->서술값=절반값();unsigned futje_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<futje_COUNT&&!teknologjia_e_informacionit_i_pavlefshëm;안쪽순번++){
            unsigned Emër=절반값(),Madhësi=가득참(),Ekzekuto=현재위치;
            if(Madhësi>gjatësi_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(Emër,"Code")){
                grup_ndryshoj_përmasat->Stivë_hapësira_ruajtëse=절반값();grup_ndryshoj_përmasat->지역변수들=절반값();grup_ndryshoj_përmasat->Madhësi=가득참();grup_ndryshoj_përmasat->instruksion_SEQUENCE=TAKE_VALUE(grup_ndryshoj_përmasat->Madhësi);
                if(grup_ndryshoj_përmasat->Stivë_hapësira_ruajtëse>128||grup_ndryshoj_përmasat->지역변수들>128||grup_ndryshoj_përmasat->Madhësi>8192||절반값())return -1;atributet();
            }else TAKE_VALUE(Madhësi);
            if(현재위치!=Ekzekuto+Madhësi)return -1;
        }
        if(!UNICODE_VALUE(grup_ndryshoj_përmasat->Emër,"<init>")&&(!(grup_ndryshoj_përmasat->konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&8)||(grup_ndryshoj_përmasat->konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&(0x100|0x20))||!grup_ndryshoj_përmasat->Madhësi))return -1;
    }
    atributet();return teknologjia_e_informacionit_i_pavlefshëm||현재위치!=gjatësi_VALUE?-1:0;
}
static void konstante_VALUE(unsigned identifikues_VALUE){
    if(!identifikues_VALUE||identifikues_VALUE>=konstante_kuotë){teknologjia_e_informacionit_i_pavlefshëm=1;return;}
    if(Shenjat_Listë[identifikues_VALUE]==3)내보내기("P(%uU);",첫째값[identifikues_VALUE]);
    else if(Shenjat_Listë[identifikues_VALUE]==8)내보내기("P((W)k%u);",identifikues_VALUE);else teknologjia_e_informacionit_i_pavlefshëm=1;
}
static void 호출(unsigned identifikues_VALUE,int virtual_CALL){
    if(identifikues_VALUE<1||identifikues_VALUE>=konstante_kuotë||(Shenjat_Listë[identifikues_VALUE]!=10&&Shenjat_Listë[identifikues_VALUE]!=11)||첫째값[identifikues_VALUE]<1||첫째값[identifikues_VALUE]>=konstante_kuotë||Shenjat_Listë[첫째값[identifikues_VALUE]]!=7||SECOND_VALUE[identifikues_VALUE]<1||SECOND_VALUE[identifikues_VALUE]>=konstante_kuotë||Shenjat_Listë[SECOND_VALUE[identifikues_VALUE]]!=12){teknologjia_e_informacionit_i_pavlefshëm=1;return;}
    unsigned pronari_objekt=첫째값[첫째값[identifikues_VALUE]],Emër=첫째값[SECOND_VALUE[identifikues_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikues_VALUE]];int llogaritje=0,njësi_COUNT=서술자(서술값,&llogaritje);if(njësi_COUNT<0){teknologjia_e_informacionit_i_pavlefshëm=1;return;}
    for(int 순번=njësi_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtual_CALL)내보내기("Q();");
    if(!virtual_CALL&&같음(pronari_objekt,첫째값[현재클래스])){
        unsigned grup_ndryshoj_përmasat=0;for(;grup_ndryshoj_përmasat<메소드개수;grup_ndryshoj_përmasat++)if(같음(Emër,메소드목록[grup_ndryshoj_përmasat].Emër)&&같음(서술값,메소드목록[grup_ndryshoj_përmasat].서술값))break;
        if(grup_ndryshoj_përmasat==메소드개수||!(메소드목록[grup_ndryshoj_përmasat].konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&8)){teknologjia_e_informacionit_i_pavlefshëm=1;return;}
        if(llogaritje)내보내기("P(");내보내기("m%u(",grup_ndryshoj_përmasat);for(int 순번=0;순번<njësi_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(llogaritje?"));":" );");return;
    }
    if((virtual_CALL&&UNICODE_VALUE(pronari_objekt,"java/io/PrintStream")&& (UNICODE_VALUE(Emër,"print")||UNICODE_VALUE(Emër,"println")))||(!virtual_CALL&&UNICODE_VALUE(pronari_objekt,"한국어/자체/출력"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Emër,"print")||UNICODE_VALUE(Emër,"println")||UNICODE_VALUE(Emër,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Emër,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Emër,"print")||UNICODE_VALUE(Emër,"println")||UNICODE_VALUE(Emër,"Shkrimi")||UNICODE_VALUE(Emër,"shkruaj_linjë"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Emër,"print")||UNICODE_VALUE(Emër,"Shkrimi")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Emër,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtual_CALL&&UNICODE_VALUE(pronari_objekt,"한국어/자체/Kartelë")){
        if(UNICODE_VALUE(Emër,"Shkrimi")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Emër,"Leximi")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    teknologjia_e_informacionit_i_pavlefshëm=1;
}
static void ndërtoj_metoda(unsigned LOOKUP_INDEX){
    metoda_futje*grup_ndryshoj_përmasat=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(grup_ndryshoj_përmasat->Emër,"<init>"))return;int llogaritje,njësi_COUNT=서술자(grup_ndryshoj_përmasat->서술값,&llogaritje);if(njësi_COUNT<0){teknologjia_e_informacionit_i_pavlefshëm=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<njësi_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!njësi_COUNT)내보내기("void");
    if((unsigned)njësi_COUNT>grup_ndryshoj_përmasat->지역변수들){teknologjia_e_informacionit_i_pavlefshëm=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",grup_ndryshoj_përmasat->지역변수들?grup_ndryshoj_përmasat->지역변수들:1);for(int 순번=0;순번<njësi_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=gjatësi_VALUE;gjatësi_VALUE=grup_ndryshoj_përmasat->instruksion_SEQUENCE+grup_ndryshoj_përmasat->Madhësi;현재위치=grup_ndryshoj_përmasat->instruksion_SEQUENCE;
    while(현재위치<gjatësi_VALUE&&!teknologjia_e_informacionit_i_pavlefshëm){unsigned komandë_pozicioni=현재위치-grup_ndryshoj_përmasat->instruksion_SEQUENCE,operim_VALUE=bajt_të_dhëna();내보내기("L%u:;",komandë_pozicioni);
        if(operim_VALUE==0){}
        else if(operim_VALUE==1)내보내기("P(0);");
        else if(operim_VALUE>=2&&operim_VALUE<=8)내보내기("P(%uU);",operim_VALUE-3);
        else if(operim_VALUE==16){int VALUE=(int8_t)bajt_të_dhëna();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operim_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operim_VALUE==18||operim_VALUE==19)konstante_VALUE(operim_VALUE==18?bajt_të_dhëna():절반값());
        else if(operim_VALUE==21||operim_VALUE==25){unsigned 순번=bajt_të_dhëna();if(순번>=grup_ndryshoj_përmasat->지역변수들)teknologjia_e_informacionit_i_pavlefshëm=1;내보내기("P(v[%u]);",순번);}
        else if((operim_VALUE>=26&&operim_VALUE<=29)||(operim_VALUE>=42&&operim_VALUE<=45)){unsigned 순번=operim_VALUE>=42?operim_VALUE-42:operim_VALUE-26;if(순번>=grup_ndryshoj_përmasat->지역변수들)teknologjia_e_informacionit_i_pavlefshëm=1;내보내기("P(v[%u]);",순번);}
        else if(operim_VALUE==54||operim_VALUE==58){unsigned 순번=bajt_të_dhëna();if(순번>=grup_ndryshoj_përmasat->지역변수들)teknologjia_e_informacionit_i_pavlefshëm=1;내보내기("v[%u]=Q();",순번);}
        else if((operim_VALUE>=59&&operim_VALUE<=62)||(operim_VALUE>=75&&operim_VALUE<=78)){unsigned 순번=operim_VALUE>=75?operim_VALUE-75:operim_VALUE-59;if(순번>=grup_ndryshoj_përmasat->지역변수들)teknologjia_e_informacionit_i_pavlefshëm=1;내보내기("v[%u]=Q();",순번);}
        else if(operim_VALUE==46||operim_VALUE==50||operim_VALUE==51||operim_VALUE==52||operim_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operim_VALUE==79||operim_VALUE==83||operim_VALUE==84||operim_VALUE==85||operim_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operim_VALUE==84?"(unsigned)(signed char)q":operim_VALUE==85?"(unsigned short)q":operim_VALUE==86?"(unsigned)(short)q":"q");
        else if(operim_VALUE==87)내보내기("Q();");
        else if(operim_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operim_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operim_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operim_VALUE==96||operim_VALUE==100||operim_VALUE==104||operim_VALUE==120||operim_VALUE==124||operim_VALUE==126||operim_VALUE==128||operim_VALUE==130){const char*enkodim_VALUE=operim_VALUE==96?"+":operim_VALUE==100?"-":operim_VALUE==104?"*":operim_VALUE==120?"<<":operim_VALUE==124?">>":operim_VALUE==126?"&":operim_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",enkodim_VALUE,operim_VALUE==120||operim_VALUE==124?"%32":"");}
        else if(operim_VALUE==108||operim_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operim_VALUE==112);
        else if(operim_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operim_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operim_VALUE==132){unsigned 순번=bajt_të_dhëna();int 차이=(int8_t)bajt_të_dhëna();if(순번>=grup_ndryshoj_përmasat->지역변수들)teknologjia_e_informacionit_i_pavlefshëm=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operim_VALUE>=145&&operim_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operim_VALUE==145?"signed char":operim_VALUE==146?"unsigned short":"short");
        else if(operim_VALUE>=153&&operim_VALUE<=166){int objektiv=(int)komandë_pozicioni+(int16_t)절반값();const char*Krahasim_VALUE[]={"==","!=","<",">=",">","<="};if(objektiv<0||objektiv>=(int)grup_ndryshoj_përmasat->Madhësi){teknologjia_e_informacionit_i_pavlefshëm=1;break;}if(operim_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Krahasim_VALUE[operim_VALUE-153],objektiv);else if(operim_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Krahasim_VALUE[operim_VALUE-159],objektiv);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operim_VALUE==165?"==":"!=",objektiv);}
        else if(operim_VALUE==167){int objektiv=(int)komandë_pozicioni+(int16_t)절반값();if(objektiv<0||objektiv>=(int)grup_ndryshoj_përmasat->Madhësi)teknologjia_e_informacionit_i_pavlefshëm=1;내보내기("goto L%d;",objektiv);}
        else if(operim_VALUE==172||operim_VALUE==176)내보내기("return Q();");else if(operim_VALUE==177)내보내기("return 0;");
        else if(operim_VALUE==178||operim_VALUE==179){unsigned identifikues_VALUE=절반값();if(identifikues_VALUE<1||identifikues_VALUE>=konstante_kuotë||Shenjat_Listë[identifikues_VALUE]!=9||첫째값[identifikues_VALUE]>=konstante_kuotë||SECOND_VALUE[identifikues_VALUE]>=konstante_kuotë||Shenjat_Listë[첫째값[identifikues_VALUE]]!=7||Shenjat_Listë[SECOND_VALUE[identifikues_VALUE]]!=12){teknologjia_e_informacionit_i_pavlefshëm=1;break;}unsigned pronari_objekt=첫째값[첫째값[identifikues_VALUE]],Emër=첫째값[SECOND_VALUE[identifikues_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikues_VALUE]];
            if(operim_VALUE==178&&UNICODE_VALUE(pronari_objekt,"java/lang/System")&&UNICODE_VALUE(Emër,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned skedar_futje=0;while(skedar_futje<필드개수&&(!같음(Emër,emri_i_fushës[skedar_futje])||!같음(서술값,필드서술[skedar_futje])))skedar_futje++;if(!같음(pronari_objekt,첫째값[현재클래스])||skedar_futje==필드개수){teknologjia_e_informacionit_i_pavlefshëm=1;break;}내보내기(operim_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",skedar_futje);}}
        else if(operim_VALUE==182||operim_VALUE==184)호출(절반값(),operim_VALUE==182);
        else if(operim_VALUE==188){unsigned TYPE_kategori=bajt_të_dhëna();if(TYPE_kategori!=4&&TYPE_kategori!=5&&TYPE_kategori!=8&&TYPE_kategori!=9&&TYPE_kategori!=10)teknologjia_e_informacionit_i_pavlefshëm=1;내보내기("P(jarray((int)Q()));");}
        else if(operim_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operim_VALUE==198||operim_VALUE==199){int objektiv=(int)komandë_pozicioni+(int16_t)절반값();if(objektiv<0||objektiv>=(int)grup_ndryshoj_përmasat->Madhësi)teknologjia_e_informacionit_i_pavlefshëm=1;내보내기("if(Q()%s0)goto L%d;",operim_VALUE==198?"==":"!=",objektiv);}
        else teknologjia_e_informacionit_i_pavlefshëm=1;
        if(teknologjia_e_informacionit_i_pavlefshëm)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operim_VALUE,komandë_pozicioni);
        내보내기("\n");
    }
    gjatësi_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned varg_mësim(unsigned *të_dhëna_pozicioni,unsigned mbaroj_OFFSET){
    if(*të_dhëna_pozicioni>=mbaroj_OFFSET){teknologjia_e_informacionit_i_pavlefshëm=1;return 0;}unsigned kodi_i_karakterit=të_dhëna[(*të_dhëna_pozicioni)++];
    if(kodi_i_karakterit<128)return kodi_i_karakterit;
    unsigned njësi_COUNT=kodi_i_karakterit>=0xc0&&kodi_i_karakterit<=0xdf?1:kodi_i_karakterit>=0xe0&&kodi_i_karakterit<=0xef?2:3;
    if(njësi_COUNT==3||njësi_COUNT>mbaroj_OFFSET-*të_dhëna_pozicioni){teknologjia_e_informacionit_i_pavlefshëm=1;return 0;}unsigned VALUE=kodi_i_karakterit&((1u<<(6-njësi_COUNT))-1);
    for(unsigned 순번=0;순번<njësi_COUNT;순번++){unsigned Tjetër_njësi=të_dhëna[(*të_dhëna_pozicioni)++];if((Tjetër_njësi&0xc0)!=0x80)teknologjia_e_informacionit_i_pavlefshëm=1;VALUE=VALUE<<6|(Tjetër_njësi&63);}
    if((njësi_COUNT==1&&VALUE<128&&VALUE!=0)||(njësi_COUNT==2&&VALUE<2048))teknologjia_e_informacionit_i_pavlefshëm=1;return VALUE;
}
static void varg_konstante(unsigned identifikues_VALUE){
    unsigned 부호없는값=첫째값[identifikues_VALUE];if(부호없는값<1||부호없는값>=konstante_kuotë||Shenjat_Listë[부호없는값]!=1){teknologjia_e_informacionit_i_pavlefshëm=1;return;}내보내기("static const unsigned char k%u[]={",identifikues_VALUE);
    unsigned të_dhëna_pozicioni=첫째값[부호없는값],mbaroj_OFFSET=të_dhëna_pozicioni+SECOND_VALUE[부호없는값];
    while(të_dhëna_pozicioni<mbaroj_OFFSET&&!teknologjia_e_informacionit_i_pavlefshëm){unsigned kodi_i_karakterit=varg_mësim(&të_dhëna_pozicioni,mbaroj_OFFSET);
        if(kodi_i_karakterit>=0xd800&&kodi_i_karakterit<=0xdbff){unsigned 낮은부분=varg_mësim(&të_dhëna_pozicioni,mbaroj_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){teknologjia_e_informacionit_i_pavlefshëm=1;break;}kodi_i_karakterit=0x10000+((kodi_i_karakterit-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kodi_i_karakterit>=0xdc00&&kodi_i_karakterit<=0xdfff){teknologjia_e_informacionit_i_pavlefshëm=1;break;}
        if(!kodi_i_karakterit){printf("jaot: embedded NUL string needs JVM mode\n");teknologjia_e_informacionit_i_pavlefshëm=1;break;}
        if(kodi_i_karakterit<128)내보내기("%u,",kodi_i_karakterit);
        else{unsigned njësi_COUNT=kodi_i_karakterit<2048?2:kodi_i_karakterit<65536?3:4;내보내기("%u,",(njësi_COUNT==2?0xc0:njësi_COUNT==3?0xe0:0xf0)|(kodi_i_karakterit>>(6*(njësi_COUNT-1))));for(unsigned 순번=njësi_COUNT-1;순번;순번--)내보내기("%u,",0x80|((kodi_i_karakterit>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Emër){
    size_t njësi_COUNT=strlen(Emër);
    if(njësi_COUNT>4&&!strcmp(Emër+njësi_COUNT-4,".jar")){
        if(꾸러미열기(Emër)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char POZICIONI[256];const char*futje_metoda=꾸러미진입클래스();njësi_COUNT=strlen(futje_metoda);if(njësi_COUNT+6>=sizeof(POZICIONI))return 0;
        for(unsigned 순번=0;순번<njësi_COUNT;순번++)POZICIONI[순번]=futje_metoda[순번]=='.'?'/':futje_metoda[순번];strcpy(POZICIONI+njësi_COUNT,".class");int futje_COUNT=꾸러미읽기(POZICIONI,të_dhëna,sizeof(të_dhëna));if(futje_COUNT<0)return 0;gjatësi_VALUE=futje_COUNT;
    }else{intptr_t skedar_dorezë=사용자호출(3,(uintptr_t)Emër,0,0,0,0,0);if(skedar_dorezë<0)return 0;intptr_t futje_COUNT=사용자호출(9,skedar_dorezë,0,0,0,0,0);if(futje_COUNT<0||futje_COUNT>sizeof(të_dhëna)){사용자호출(4,skedar_dorezë,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,skedar_dorezë,(uintptr_t)të_dhëna,futje_COUNT,0,0,0);사용자호출(4,skedar_dorezë,0,0,0,0,0);if(RECEIVED_COUNT!=futje_COUNT)return 0;gjatësi_VALUE=futje_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstante_kuotë&&!teknologjia_e_informacionit_i_pavlefshëm;순번++)if(Shenjat_Listë[순번]==8)varg_konstante(순번);
    if(teknologjia_e_informacionit_i_pavlefshëm)return 0;
    int futje_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Emër,"<init>")){
        int llogaritje,futje_COUNT=서술자(메소드목록[순번].서술값,&llogaritje);if(futje_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<futje_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!futje_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Emër,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond&9)==9)futje_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Emër,"<clinit>"))초기값=순번;
    }
    if(futje_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!teknologjia_e_informacionit_i_pavlefshëm;순번++)ndërtoj_metoda(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(fushë_konstante[순번]){
        unsigned kodi_i_karakterit=fushë_konstante[순번];if(kodi_i_karakterit>=konstante_kuotë)return 0;
        if(Shenjat_Listë[kodi_i_karakterit]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kodi_i_karakterit]);else if(Shenjat_Listë[kodi_i_karakterit]==8)내보내기("fields[%u]=(W)k%u;",순번,kodi_i_karakterit);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",futje_p);
    return teknologjia_e_informacionit_i_pavlefshëm?0:Teksti;
}
