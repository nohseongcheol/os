#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "isigaxa.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char imininingwane[16384];static unsigned ubude_inani,현재위치;static int 잘못됨;
static unsigned Izigaba_Uhlu[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char Itekisi[65536];static unsigned ubungako_bombhalo;
typedef struct {unsigned 설정비트,Igama,서술값,umyalelo_UKULANDELANA,Ubungako,지역변수들,Isitaki_Indawo_yokugcina;} indlela_okufakwayo;
static indlela_okufakwayo 메소드목록[64];static unsigned 메소드개수;
static unsigned igama_lomkakha[64],필드서술[64],inkundla_indawana_okungaguquki[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>ubude_inani||개수>ubude_inani-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned ibhayithi_imininingwane(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:imininingwane[자료위치];}
static unsigned 절반값(void){unsigned okuxhumanisa_u_x=ibhayithi_imininingwane();return okuxhumanisa_u_x<<8|ibhayithi_imininingwane();}
static uint32_t 가득참(void){uint32_t okuxhumanisa_u_x=절반값();return okuxhumanisa_u_x<<16|절반값();}
static int IYunikhodi_inani(unsigned 순번,const char*uchunge_imininingwane){return 순번>0&&순번<상수모음&&Izigaba_Uhlu[순번]==1&&strlen(uchunge_imininingwane)==둘째값[순번]&&!memcmp(imininingwane+첫째값[순번],uchunge_imininingwane,둘째값[순번]);}
static int 같음(unsigned okuxhumanisa_u_x,unsigned 세로좌표){return okuxhumanisa_u_x>0&&okuxhumanisa_u_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&Izigaba_Uhlu[okuxhumanisa_u_x]==1&&Izigaba_Uhlu[세로좌표]==1&&둘째값[okuxhumanisa_u_x]==둘째값[세로좌표]&&!memcmp(imininingwane+첫째값[okuxhumanisa_u_x],imininingwane+첫째값[세로좌표],둘째값[okuxhumanisa_u_x]);}
static void 내보내기(const char*ifayela_okufakwayo,...){if(잘못됨)return;va_list i_agumenti_AMALUNGU_AFANAYO;va_start(i_agumenti_AMALUNGU_AFANAYO,ifayela_okufakwayo);int 개수=vsnprintf(Itekisi+ubungako_bombhalo,sizeof(Itekisi)-ubungako_bombhalo,ifayela_okufakwayo,i_agumenti_AMALUNGU_AFANAYO);va_end(i_agumenti_AMALUNGU_AFANAYO);if(개수<0||(unsigned)개수>=sizeof(Itekisi)-ubungako_bombhalo){잘못됨=1;return;}ubungako_bombhalo+=개수;}
static int 서술자(unsigned isivezi_inani,int*결과){
    if(isivezi_inani<1||isivezi_inani>=상수모음||Izigaba_Uhlu[isivezi_inani]!=1)return -1;unsigned 자료위치=첫째값[isivezi_inani],yekisa_I_ofisethi=자료위치+둘째값[isivezi_inani];if(자료위치>=yekisa_I_ofisethi||imininingwane[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<yekisa_I_ofisethi&&imininingwane[자료위치]!=')'){
        unsigned ikhodi_yohlamvu=imininingwane[자료위치++];while(ikhodi_yohlamvu=='['&&자료위치<yekisa_I_ofisethi)ikhodi_yohlamvu=imininingwane[자료위치++];
        if(ikhodi_yohlamvu=='L'){while(자료위치<yekisa_I_ofisethi&&imininingwane[자료위치]!=';')자료위치++;if(자료위치==yekisa_I_ofisethi)return -1;자료위치++;}
        else if(ikhodi_yohlamvu!='I'&&ikhodi_yohlamvu!='Z'&&ikhodi_yohlamvu!='B'&&ikhodi_yohlamvu!='C'&&ikhodi_yohlamvu!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=yekisa_I_ofisethi||imininingwane[자료위치++]!=')')return -1;*결과=imininingwane[자료위치]=='V'?0:1;
    if(imininingwane[자료위치]=='J'||imininingwane[자료위치]=='D'||imininingwane[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned Ubungako=가득참();가져오기(Ubungako);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned ingane_isibuyekezo=절반값(),판번호=절반값();if(ingane_isibuyekezo||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Izigaba_Uhlu[순번]=ibhayithi_imininingwane();switch(Izigaba_Uhlu[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=ibhayithi_imininingwane();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Izigaba_Uhlu[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Izigaba_Uhlu[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();igama_lomkakha[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Igama=절반값(),Ubungako=가득참();
            if(IYunikhodi_inani(Igama,"ConstantValue")){if(Ubungako!=2)return -1;inkundla_indawana_okungaguquki[순번]=절반값();}
            else 가져오기(Ubungako);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        indlela_okufakwayo*iqoqo_linganisa=메소드목록+순번;iqoqo_linganisa->설정비트=절반값();iqoqo_linganisa->Igama=절반값();iqoqo_linganisa->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Igama=절반값(),Ubungako=가득참(),Sebenzisa=현재위치;
            if(Ubungako>ubude_inani-현재위치)return -1;
            if(IYunikhodi_inani(Igama,"Code")){
                iqoqo_linganisa->Isitaki_Indawo_yokugcina=절반값();iqoqo_linganisa->지역변수들=절반값();iqoqo_linganisa->Ubungako=가득참();iqoqo_linganisa->umyalelo_UKULANDELANA=가져오기(iqoqo_linganisa->Ubungako);
                if(iqoqo_linganisa->Isitaki_Indawo_yokugcina>128||iqoqo_linganisa->지역변수들>128||iqoqo_linganisa->Ubungako>8192||절반값())return -1;속성들();
            }else 가져오기(Ubungako);
            if(현재위치!=Sebenzisa+Ubungako)return -1;
        }
        if(!IYunikhodi_inani(iqoqo_linganisa->Igama,"<init>")&&(!(iqoqo_linganisa->설정비트&8)||(iqoqo_linganisa->설정비트&(0x100|0x20))||!iqoqo_linganisa->Ubungako))return -1;
    }
    속성들();return 잘못됨||현재위치!=ubude_inani?-1:0;
}
static void okungaguquki_inani(unsigned isivezi_inani){
    if(!isivezi_inani||isivezi_inani>=상수모음){잘못됨=1;return;}
    if(Izigaba_Uhlu[isivezi_inani]==3)내보내기("P(%uU);",첫째값[isivezi_inani]);
    else if(Izigaba_Uhlu[isivezi_inani]==8)내보내기("P((W)k%u);",isivezi_inani);else 잘못됨=1;
}
static void 호출(unsigned isivezi_inani,int utalagu_fonela){
    if(isivezi_inani<1||isivezi_inani>=상수모음||(Izigaba_Uhlu[isivezi_inani]!=10&&Izigaba_Uhlu[isivezi_inani]!=11)||첫째값[isivezi_inani]<1||첫째값[isivezi_inani]>=상수모음||Izigaba_Uhlu[첫째값[isivezi_inani]]!=7||둘째값[isivezi_inani]<1||둘째값[isivezi_inani]>=상수모음||Izigaba_Uhlu[둘째값[isivezi_inani]]!=12){잘못됨=1;return;}
    unsigned umnikazi_into=첫째값[첫째값[isivezi_inani]],Igama=첫째값[둘째값[isivezi_inani]],서술값=둘째값[둘째값[isivezi_inani]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(utalagu_fonela)내보내기("Q();");
    if(!utalagu_fonela&&같음(umnikazi_into,첫째값[현재클래스])){
        unsigned iqoqo_linganisa=0;for(;iqoqo_linganisa<메소드개수;iqoqo_linganisa++)if(같음(Igama,메소드목록[iqoqo_linganisa].Igama)&&같음(서술값,메소드목록[iqoqo_linganisa].서술값))break;
        if(iqoqo_linganisa==메소드개수||!(메소드목록[iqoqo_linganisa].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",iqoqo_linganisa);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((utalagu_fonela&&IYunikhodi_inani(umnikazi_into,"java/io/PrintStream")&& (IYunikhodi_inani(Igama,"print")||IYunikhodi_inani(Igama,"println")))||(!utalagu_fonela&&IYunikhodi_inani(umnikazi_into,"Isi_Zulu/자체/출력"))){
        if(IYunikhodi_inani(서술값,"(I)V")&&(IYunikhodi_inani(Igama,"print")||IYunikhodi_inani(Igama,"println")||IYunikhodi_inani(Igama,"수쓰기"))){내보내기("jprint(x[0],1,%d);",IYunikhodi_inani(Igama,"print")?0:1);return;}
        if(IYunikhodi_inani(서술값,"(Ljava/lang/String;)V")&&(IYunikhodi_inani(Igama,"print")||IYunikhodi_inani(Igama,"println")||IYunikhodi_inani(Igama,"Bhala")||IYunikhodi_inani(Igama,"bhala_umugqa"))){내보내기("jprint(x[0],0,%d);",IYunikhodi_inani(Igama,"print")||IYunikhodi_inani(Igama,"Bhala")?0:1);return;}
        if(IYunikhodi_inani(서술값,"()V")&&IYunikhodi_inani(Igama,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!utalagu_fonela&&IYunikhodi_inani(umnikazi_into,"Isi_Zulu/자체/Ihele")){
        if(IYunikhodi_inani(Igama,"Bhala")&&IYunikhodi_inani(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(IYunikhodi_inani(Igama,"Funda")&&IYunikhodi_inani(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void akha_indlela(unsigned 색인){
    indlela_okufakwayo*iqoqo_linganisa=메소드목록+색인;if(IYunikhodi_inani(iqoqo_linganisa->Igama,"<init>"))return;int 결과,개수=서술자(iqoqo_linganisa->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>iqoqo_linganisa->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",iqoqo_linganisa->지역변수들?iqoqo_linganisa->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=ubude_inani;ubude_inani=iqoqo_linganisa->umyalelo_UKULANDELANA+iqoqo_linganisa->Ubungako;현재위치=iqoqo_linganisa->umyalelo_UKULANDELANA;
    while(현재위치<ubude_inani&&!잘못됨){unsigned 명령위치=현재위치-iqoqo_linganisa->umyalelo_UKULANDELANA,umsebenzi_inani_c96707fb=ibhayithi_imininingwane();내보내기("L%u:;",명령위치);
        if(umsebenzi_inani_c96707fb==0){}
        else if(umsebenzi_inani_c96707fb==1)내보내기("P(0);");
        else if(umsebenzi_inani_c96707fb>=2&&umsebenzi_inani_c96707fb<=8)내보내기("P(%uU);",umsebenzi_inani_c96707fb-3);
        else if(umsebenzi_inani_c96707fb==16){int inani=(int8_t)ibhayithi_imininingwane();내보내기("P(%uU);",(unsigned)inani);}
        else if(umsebenzi_inani_c96707fb==17){int inani=(int16_t)절반값();내보내기("P(%uU);",(unsigned)inani);}
        else if(umsebenzi_inani_c96707fb==18||umsebenzi_inani_c96707fb==19)okungaguquki_inani(umsebenzi_inani_c96707fb==18?ibhayithi_imininingwane():절반값());
        else if(umsebenzi_inani_c96707fb==21||umsebenzi_inani_c96707fb==25){unsigned 순번=ibhayithi_imininingwane();if(순번>=iqoqo_linganisa->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((umsebenzi_inani_c96707fb>=26&&umsebenzi_inani_c96707fb<=29)||(umsebenzi_inani_c96707fb>=42&&umsebenzi_inani_c96707fb<=45)){unsigned 순번=umsebenzi_inani_c96707fb>=42?umsebenzi_inani_c96707fb-42:umsebenzi_inani_c96707fb-26;if(순번>=iqoqo_linganisa->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(umsebenzi_inani_c96707fb==54||umsebenzi_inani_c96707fb==58){unsigned 순번=ibhayithi_imininingwane();if(순번>=iqoqo_linganisa->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((umsebenzi_inani_c96707fb>=59&&umsebenzi_inani_c96707fb<=62)||(umsebenzi_inani_c96707fb>=75&&umsebenzi_inani_c96707fb<=78)){unsigned 순번=umsebenzi_inani_c96707fb>=75?umsebenzi_inani_c96707fb-75:umsebenzi_inani_c96707fb-59;if(순번>=iqoqo_linganisa->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(umsebenzi_inani_c96707fb==46||umsebenzi_inani_c96707fb==50||umsebenzi_inani_c96707fb==51||umsebenzi_inani_c96707fb==52||umsebenzi_inani_c96707fb==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(umsebenzi_inani_c96707fb==79||umsebenzi_inani_c96707fb==83||umsebenzi_inani_c96707fb==84||umsebenzi_inani_c96707fb==85||umsebenzi_inani_c96707fb==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",umsebenzi_inani_c96707fb==84?"(unsigned)(signed char)q":umsebenzi_inani_c96707fb==85?"(unsigned short)q":umsebenzi_inani_c96707fb==86?"(unsigned)(short)q":"q");
        else if(umsebenzi_inani_c96707fb==87)내보내기("Q();");
        else if(umsebenzi_inani_c96707fb==89)내보내기("q=Q();P(q);P(q);");
        else if(umsebenzi_inani_c96707fb==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(umsebenzi_inani_c96707fb==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(umsebenzi_inani_c96707fb==96||umsebenzi_inani_c96707fb==100||umsebenzi_inani_c96707fb==104||umsebenzi_inani_c96707fb==120||umsebenzi_inani_c96707fb==124||umsebenzi_inani_c96707fb==126||umsebenzi_inani_c96707fb==128||umsebenzi_inani_c96707fb==130){const char*ukubhala_ngokufihla_inani=umsebenzi_inani_c96707fb==96?"+":umsebenzi_inani_c96707fb==100?"-":umsebenzi_inani_c96707fb==104?"*":umsebenzi_inani_c96707fb==120?"<<":umsebenzi_inani_c96707fb==124?">>":umsebenzi_inani_c96707fb==126?"&":umsebenzi_inani_c96707fb==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",ukubhala_ngokufihla_inani,umsebenzi_inani_c96707fb==120||umsebenzi_inani_c96707fb==124?"%32":"");}
        else if(umsebenzi_inani_c96707fb==108||umsebenzi_inani_c96707fb==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",umsebenzi_inani_c96707fb==112);
        else if(umsebenzi_inani_c96707fb==116)내보내기("P(0U-(unsigned)Q());");
        else if(umsebenzi_inani_c96707fb==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(umsebenzi_inani_c96707fb==132){unsigned 순번=ibhayithi_imininingwane();int 차이=(int8_t)ibhayithi_imininingwane();if(순번>=iqoqo_linganisa->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(umsebenzi_inani_c96707fb>=145&&umsebenzi_inani_c96707fb<=147)내보내기("P((unsigned)(%s)Q());",umsebenzi_inani_c96707fb==145?"signed char":umsebenzi_inani_c96707fb==146?"unsigned short":"short");
        else if(umsebenzi_inani_c96707fb>=153&&umsebenzi_inani_c96707fb<=166){int impokophelo=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(impokophelo<0||impokophelo>=(int)iqoqo_linganisa->Ubungako){잘못됨=1;break;}if(umsebenzi_inani_c96707fb<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[umsebenzi_inani_c96707fb-153],impokophelo);else if(umsebenzi_inani_c96707fb<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[umsebenzi_inani_c96707fb-159],impokophelo);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",umsebenzi_inani_c96707fb==165?"==":"!=",impokophelo);}
        else if(umsebenzi_inani_c96707fb==167){int impokophelo=(int)명령위치+(int16_t)절반값();if(impokophelo<0||impokophelo>=(int)iqoqo_linganisa->Ubungako)잘못됨=1;내보내기("goto L%d;",impokophelo);}
        else if(umsebenzi_inani_c96707fb==172||umsebenzi_inani_c96707fb==176)내보내기("return Q();");else if(umsebenzi_inani_c96707fb==177)내보내기("return 0;");
        else if(umsebenzi_inani_c96707fb==178||umsebenzi_inani_c96707fb==179){unsigned isivezi_inani=절반값();if(isivezi_inani<1||isivezi_inani>=상수모음||Izigaba_Uhlu[isivezi_inani]!=9||첫째값[isivezi_inani]>=상수모음||둘째값[isivezi_inani]>=상수모음||Izigaba_Uhlu[첫째값[isivezi_inani]]!=7||Izigaba_Uhlu[둘째값[isivezi_inani]]!=12){잘못됨=1;break;}unsigned umnikazi_into=첫째값[첫째값[isivezi_inani]],Igama=첫째값[둘째값[isivezi_inani]],서술값=둘째값[둘째값[isivezi_inani]];
            if(umsebenzi_inani_c96707fb==178&&IYunikhodi_inani(umnikazi_into,"java/lang/System")&&IYunikhodi_inani(Igama,"out")&&IYunikhodi_inani(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned ifayela_okufakwayo=0;while(ifayela_okufakwayo<필드개수&&(!같음(Igama,igama_lomkakha[ifayela_okufakwayo])||!같음(서술값,필드서술[ifayela_okufakwayo])))ifayela_okufakwayo++;if(!같음(umnikazi_into,첫째값[현재클래스])||ifayela_okufakwayo==필드개수){잘못됨=1;break;}내보내기(umsebenzi_inani_c96707fb==178?"P(fields[%u]);":"fields[%u]=Q();",ifayela_okufakwayo);}}
        else if(umsebenzi_inani_c96707fb==182||umsebenzi_inani_c96707fb==184)호출(절반값(),umsebenzi_inani_c96707fb==182);
        else if(umsebenzi_inani_c96707fb==188){unsigned thayipha_umunxa=ibhayithi_imininingwane();if(thayipha_umunxa!=4&&thayipha_umunxa!=5&&thayipha_umunxa!=8&&thayipha_umunxa!=9&&thayipha_umunxa!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(umsebenzi_inani_c96707fb==190)내보내기("P(jlength(Q()));");
        else if(umsebenzi_inani_c96707fb==198||umsebenzi_inani_c96707fb==199){int impokophelo=(int)명령위치+(int16_t)절반값();if(impokophelo<0||impokophelo>=(int)iqoqo_linganisa->Ubungako)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",umsebenzi_inani_c96707fb==198?"==":"!=",impokophelo);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,umsebenzi_inani_c96707fb,명령위치);
        내보내기("\n");
    }
    ubude_inani=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned uchunge_isifundo(unsigned *자료위치,unsigned yekisa_I_ofisethi){
    if(*자료위치>=yekisa_I_ofisethi){잘못됨=1;return 0;}unsigned ikhodi_yohlamvu=imininingwane[(*자료위치)++];
    if(ikhodi_yohlamvu<128)return ikhodi_yohlamvu;
    unsigned 개수=ikhodi_yohlamvu>=0xc0&&ikhodi_yohlamvu<=0xdf?1:ikhodi_yohlamvu>=0xe0&&ikhodi_yohlamvu<=0xef?2:3;
    if(개수==3||개수>yekisa_I_ofisethi-*자료위치){잘못됨=1;return 0;}unsigned inani=ikhodi_yohlamvu&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=imininingwane[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;inani=inani<<6|(다음&63);}
    if((개수==1&&inani<128&&inani!=0)||(개수==2&&inani<2048))잘못됨=1;return inani;
}
static void uchunge_okungaguquki(unsigned isivezi_inani){
    unsigned 부호없는값=첫째값[isivezi_inani];if(부호없는값<1||부호없는값>=상수모음||Izigaba_Uhlu[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",isivezi_inani);
    unsigned 자료위치=첫째값[부호없는값],yekisa_I_ofisethi=자료위치+둘째값[부호없는값];
    while(자료위치<yekisa_I_ofisethi&&!잘못됨){unsigned ikhodi_yohlamvu=uchunge_isifundo(&자료위치,yekisa_I_ofisethi);
        if(ikhodi_yohlamvu>=0xd800&&ikhodi_yohlamvu<=0xdbff){unsigned 낮은부분=uchunge_isifundo(&자료위치,yekisa_I_ofisethi);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}ikhodi_yohlamvu=0x10000+((ikhodi_yohlamvu-0xd800)<<10)+낮은부분-0xdc00;}
        else if(ikhodi_yohlamvu>=0xdc00&&ikhodi_yohlamvu<=0xdfff){잘못됨=1;break;}
        if(!ikhodi_yohlamvu){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(ikhodi_yohlamvu<128)내보내기("%u,",ikhodi_yohlamvu);
        else{unsigned 개수=ikhodi_yohlamvu<2048?2:ikhodi_yohlamvu<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(ikhodi_yohlamvu>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((ikhodi_yohlamvu>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Igama){
    size_t 개수=strlen(Igama);
    if(개수>4&&!strcmp(Igama+개수-4,".jar")){
        if(꾸러미열기(Igama)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Indlela_2[256];const char*okufakwayo_indlela=꾸러미진입클래스();개수=strlen(okufakwayo_indlela);if(개수+6>=sizeof(Indlela_2))return 0;
        for(unsigned 순번=0;순번<개수;순번++)Indlela_2[순번]=okufakwayo_indlela[순번]=='.'?'/':okufakwayo_indlela[순번];strcpy(Indlela_2+개수,".class");int 항목수=꾸러미읽기(Indlela_2,imininingwane,sizeof(imininingwane));if(항목수<0)return 0;ubude_inani=항목수;
    }else{intptr_t ifayela_isibambo=사용자호출(3,(uintptr_t)Igama,0,0,0,0,0);if(ifayela_isibambo<0)return 0;intptr_t 항목수=사용자호출(9,ifayela_isibambo,0,0,0,0,0);if(항목수<0||항목수>sizeof(imininingwane)){사용자호출(4,ifayela_isibambo,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,ifayela_isibambo,(uintptr_t)imininingwane,항목수,0,0,0);사용자호출(4,ifayela_isibambo,0,0,0,0,0);if(받은수!=항목수)return 0;ubude_inani=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Izigaba_Uhlu[순번]==8)uchunge_okungaguquki(순번);
    if(잘못됨)return 0;
    int okufakwayo_iphoyinti=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!IYunikhodi_inani(메소드목록[순번].Igama,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(IYunikhodi_inani(메소드목록[순번].Igama,"main")&&IYunikhodi_inani(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)okufakwayo_iphoyinti=순번;
        if(IYunikhodi_inani(메소드목록[순번].Igama,"<clinit>"))초기값=순번;
    }
    if(okufakwayo_iphoyinti<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)akha_indlela(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(inkundla_indawana_okungaguquki[순번]){
        unsigned ikhodi_yohlamvu=inkundla_indawana_okungaguquki[순번];if(ikhodi_yohlamvu>=상수모음)return 0;
        if(Izigaba_Uhlu[ikhodi_yohlamvu]==3)내보내기("fields[%u]=%uU;",순번,첫째값[ikhodi_yohlamvu]);else if(Izigaba_Uhlu[ikhodi_yohlamvu]==8)내보내기("fields[%u]=(W)k%u;",순번,ikhodi_yohlamvu);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",okufakwayo_iphoyinti);
    return 잘못됨?0:Itekisi;
}
