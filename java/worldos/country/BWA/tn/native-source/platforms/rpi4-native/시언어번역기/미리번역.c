#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "ngatanngwe.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char tshedimosetso[16384];static unsigned boleele_Boleng,현재위치;static int 잘못됨;
static unsigned Ditlhopha_lenaane[512],첫째값[512],둘째값[512],상수모음,ga_jaana_mofuta;
static char SMS[65536];static unsigned bogolo_jwa_ditlhaka;
typedef struct {unsigned 설정비트,leina,서술값,taelo_TATELANO,lekanya,지역변수들,kokoanyodinepe_Polokelo;} mokgwa_tsenyo;
static mokgwa_tsenyo 메소드목록[64];static unsigned 메소드개수;
static unsigned leina_la_lefelo[64],필드서술[64],lefelo_tlhomameng[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>boleele_Boleng||개수>boleele_Boleng-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned baete_tshedimosetso(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:tshedimosetso[자료위치];}
static unsigned 절반값(void){unsigned kgokagano_ya_x=baete_tshedimosetso();return kgokagano_ya_x<<8|baete_tshedimosetso();}
static uint32_t 가득참(void){uint32_t kgokagano_ya_x=절반값();return kgokagano_ya_x<<16|절반값();}
static int Unicode_Boleng(unsigned 순번,const char*dikwalwa_tshedimosetso){return 순번>0&&순번<상수모음&&Ditlhopha_lenaane[순번]==1&&strlen(dikwalwa_tshedimosetso)==둘째값[순번]&&!memcmp(tshedimosetso+첫째값[순번],dikwalwa_tshedimosetso,둘째값[순번]);}
static int 같음(unsigned kgokagano_ya_x,unsigned 세로좌표){return kgokagano_ya_x>0&&kgokagano_ya_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&Ditlhopha_lenaane[kgokagano_ya_x]==1&&Ditlhopha_lenaane[세로좌표]==1&&둘째값[kgokagano_ya_x]==둘째값[세로좌표]&&!memcmp(tshedimosetso+첫째값[kgokagano_ya_x],tshedimosetso+첫째값[세로좌표],둘째값[kgokagano_ya_x]);}
static void 내보내기(const char*faele_tsenyo,...){if(잘못됨)return;va_list Thulaganyo_setlhopha;va_start(Thulaganyo_setlhopha,faele_tsenyo);int 개수=vsnprintf(SMS+bogolo_jwa_ditlhaka,sizeof(SMS)-bogolo_jwa_ditlhaka,faele_tsenyo,Thulaganyo_setlhopha);va_end(Thulaganyo_setlhopha);if(개수<0||(unsigned)개수>=sizeof(SMS)-bogolo_jwa_ditlhaka){잘못됨=1;return;}bogolo_jwa_ditlhaka+=개수;}
static int 서술자(unsigned setlhaodi_Boleng,int*결과){
    if(setlhaodi_Boleng<1||setlhaodi_Boleng>=상수모음||Ditlhopha_lenaane[setlhaodi_Boleng]!=1)return -1;unsigned 자료위치=첫째값[setlhaodi_Boleng],kgaola_Baya_ka_Tekatekanyo=자료위치+둘째값[setlhaodi_Boleng];if(자료위치>=kgaola_Baya_ka_Tekatekanyo||tshedimosetso[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<kgaola_Baya_ka_Tekatekanyo&&tshedimosetso[자료위치]!=')'){
        unsigned khoutuletshwao=tshedimosetso[자료위치++];while(khoutuletshwao=='['&&자료위치<kgaola_Baya_ka_Tekatekanyo)khoutuletshwao=tshedimosetso[자료위치++];
        if(khoutuletshwao=='L'){while(자료위치<kgaola_Baya_ka_Tekatekanyo&&tshedimosetso[자료위치]!=';')자료위치++;if(자료위치==kgaola_Baya_ka_Tekatekanyo)return -1;자료위치++;}
        else if(khoutuletshwao!='I'&&khoutuletshwao!='Z'&&khoutuletshwao!='B'&&khoutuletshwao!='C'&&khoutuletshwao!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=kgaola_Baya_ka_Tekatekanyo||tshedimosetso[자료위치++]!=')')return -1;*결과=tshedimosetso[자료위치]=='V'?0:1;
    if(tshedimosetso[자료위치]=='J'||tshedimosetso[자료위치]=='D'||tshedimosetso[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned lekanya=가득참();가져오기(lekanya);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned ngwana_kgaolo=절반값(),판번호=절반값();if(ngwana_kgaolo||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Ditlhopha_lenaane[순번]=baete_tshedimosetso();switch(Ditlhopha_lenaane[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=baete_tshedimosetso();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();ga_jaana_mofuta=절반값();절반값();if(ga_jaana_mofuta<1||ga_jaana_mofuta>=상수모음||Ditlhopha_lenaane[ga_jaana_mofuta]!=7||첫째값[ga_jaana_mofuta]<1||첫째값[ga_jaana_mofuta]>=상수모음||Ditlhopha_lenaane[첫째값[ga_jaana_mofuta]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();leina_la_lefelo[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned leina=절반값(),lekanya=가득참();
            if(Unicode_Boleng(leina,"ConstantValue")){if(lekanya!=2)return -1;lefelo_tlhomameng[순번]=절반값();}
            else 가져오기(lekanya);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        mokgwa_tsenyo*setlhopha_lekanya=메소드목록+순번;setlhopha_lekanya->설정비트=절반값();setlhopha_lekanya->leina=절반값();setlhopha_lekanya->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned leina=절반값(),lekanya=가득참(),dirisa=현재위치;
            if(lekanya>boleele_Boleng-현재위치)return -1;
            if(Unicode_Boleng(leina,"Code")){
                setlhopha_lekanya->kokoanyodinepe_Polokelo=절반값();setlhopha_lekanya->지역변수들=절반값();setlhopha_lekanya->lekanya=가득참();setlhopha_lekanya->taelo_TATELANO=가져오기(setlhopha_lekanya->lekanya);
                if(setlhopha_lekanya->kokoanyodinepe_Polokelo>128||setlhopha_lekanya->지역변수들>128||setlhopha_lekanya->lekanya>8192||절반값())return -1;속성들();
            }else 가져오기(lekanya);
            if(현재위치!=dirisa+lekanya)return -1;
        }
        if(!Unicode_Boleng(setlhopha_lekanya->leina,"<init>")&&(!(setlhopha_lekanya->설정비트&8)||(setlhopha_lekanya->설정비트&(0x100|0x20))||!setlhopha_lekanya->lekanya))return -1;
    }
    속성들();return 잘못됨||현재위치!=boleele_Boleng?-1:0;
}
static void tlhomameng_Boleng(unsigned setlhaodi_Boleng){
    if(!setlhaodi_Boleng||setlhaodi_Boleng>=상수모음){잘못됨=1;return;}
    if(Ditlhopha_lenaane[setlhaodi_Boleng]==3)내보내기("P(%uU);",첫째값[setlhaodi_Boleng]);
    else if(Ditlhopha_lenaane[setlhaodi_Boleng]==8)내보내기("P((W)k%u);",setlhaodi_Boleng);else 잘못됨=1;
}
static void 호출(unsigned setlhaodi_Boleng,int seka_letsa){
    if(setlhaodi_Boleng<1||setlhaodi_Boleng>=상수모음||(Ditlhopha_lenaane[setlhaodi_Boleng]!=10&&Ditlhopha_lenaane[setlhaodi_Boleng]!=11)||첫째값[setlhaodi_Boleng]<1||첫째값[setlhaodi_Boleng]>=상수모음||Ditlhopha_lenaane[첫째값[setlhaodi_Boleng]]!=7||둘째값[setlhaodi_Boleng]<1||둘째값[setlhaodi_Boleng]>=상수모음||Ditlhopha_lenaane[둘째값[setlhaodi_Boleng]]!=12){잘못됨=1;return;}
    unsigned mong_selwana=첫째값[첫째값[setlhaodi_Boleng]],leina=첫째값[둘째값[setlhaodi_Boleng]],서술값=둘째값[둘째값[setlhaodi_Boleng]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(seka_letsa)내보내기("Q();");
    if(!seka_letsa&&같음(mong_selwana,첫째값[ga_jaana_mofuta])){
        unsigned setlhopha_lekanya=0;for(;setlhopha_lekanya<메소드개수;setlhopha_lekanya++)if(같음(leina,메소드목록[setlhopha_lekanya].leina)&&같음(서술값,메소드목록[setlhopha_lekanya].서술값))break;
        if(setlhopha_lekanya==메소드개수||!(메소드목록[setlhopha_lekanya].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",setlhopha_lekanya);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((seka_letsa&&Unicode_Boleng(mong_selwana,"java/io/PrintStream")&& (Unicode_Boleng(leina,"print")||Unicode_Boleng(leina,"println")))||(!seka_letsa&&Unicode_Boleng(mong_selwana,"한국어/자체/출력"))){
        if(Unicode_Boleng(서술값,"(I)V")&&(Unicode_Boleng(leina,"print")||Unicode_Boleng(leina,"println")||Unicode_Boleng(leina,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Unicode_Boleng(leina,"print")?0:1);return;}
        if(Unicode_Boleng(서술값,"(Ljava/lang/String;)V")&&(Unicode_Boleng(leina,"print")||Unicode_Boleng(leina,"println")||Unicode_Boleng(leina,"kwala")||Unicode_Boleng(leina,"kwala_Mola"))){내보내기("jprint(x[0],0,%d);",Unicode_Boleng(leina,"print")||Unicode_Boleng(leina,"kwala")?0:1);return;}
        if(Unicode_Boleng(서술값,"()V")&&Unicode_Boleng(leina,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!seka_letsa&&Unicode_Boleng(mong_selwana,"한국어/자체/faele")){
        if(Unicode_Boleng(leina,"kwala")&&Unicode_Boleng(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Unicode_Boleng(leina,"읽기")&&Unicode_Boleng(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void aga_mokgwa(unsigned 색인){
    mokgwa_tsenyo*setlhopha_lekanya=메소드목록+색인;if(Unicode_Boleng(setlhopha_lekanya->leina,"<init>"))return;int 결과,개수=서술자(setlhopha_lekanya->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>setlhopha_lekanya->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",setlhopha_lekanya->지역변수들?setlhopha_lekanya->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=boleele_Boleng;boleele_Boleng=setlhopha_lekanya->taelo_TATELANO+setlhopha_lekanya->lekanya;현재위치=setlhopha_lekanya->taelo_TATELANO;
    while(현재위치<boleele_Boleng&&!잘못됨){unsigned 명령위치=현재위치-setlhopha_lekanya->taelo_TATELANO,tiro_Boleng=baete_tshedimosetso();내보내기("L%u:;",명령위치);
        if(tiro_Boleng==0){}
        else if(tiro_Boleng==1)내보내기("P(0);");
        else if(tiro_Boleng>=2&&tiro_Boleng<=8)내보내기("P(%uU);",tiro_Boleng-3);
        else if(tiro_Boleng==16){int Boleng=(int8_t)baete_tshedimosetso();내보내기("P(%uU);",(unsigned)Boleng);}
        else if(tiro_Boleng==17){int Boleng=(int16_t)절반값();내보내기("P(%uU);",(unsigned)Boleng);}
        else if(tiro_Boleng==18||tiro_Boleng==19)tlhomameng_Boleng(tiro_Boleng==18?baete_tshedimosetso():절반값());
        else if(tiro_Boleng==21||tiro_Boleng==25){unsigned 순번=baete_tshedimosetso();if(순번>=setlhopha_lekanya->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((tiro_Boleng>=26&&tiro_Boleng<=29)||(tiro_Boleng>=42&&tiro_Boleng<=45)){unsigned 순번=tiro_Boleng>=42?tiro_Boleng-42:tiro_Boleng-26;if(순번>=setlhopha_lekanya->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(tiro_Boleng==54||tiro_Boleng==58){unsigned 순번=baete_tshedimosetso();if(순번>=setlhopha_lekanya->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((tiro_Boleng>=59&&tiro_Boleng<=62)||(tiro_Boleng>=75&&tiro_Boleng<=78)){unsigned 순번=tiro_Boleng>=75?tiro_Boleng-75:tiro_Boleng-59;if(순번>=setlhopha_lekanya->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(tiro_Boleng==46||tiro_Boleng==50||tiro_Boleng==51||tiro_Boleng==52||tiro_Boleng==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(tiro_Boleng==79||tiro_Boleng==83||tiro_Boleng==84||tiro_Boleng==85||tiro_Boleng==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",tiro_Boleng==84?"(unsigned)(signed char)q":tiro_Boleng==85?"(unsigned short)q":tiro_Boleng==86?"(unsigned)(short)q":"q");
        else if(tiro_Boleng==87)내보내기("Q();");
        else if(tiro_Boleng==89)내보내기("q=Q();P(q);P(q);");
        else if(tiro_Boleng==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(tiro_Boleng==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(tiro_Boleng==96||tiro_Boleng==100||tiro_Boleng==104||tiro_Boleng==120||tiro_Boleng==124||tiro_Boleng==126||tiro_Boleng==128||tiro_Boleng==130){const char*khoutufatso_Boleng=tiro_Boleng==96?"+":tiro_Boleng==100?"-":tiro_Boleng==104?"*":tiro_Boleng==120?"<<":tiro_Boleng==124?">>":tiro_Boleng==126?"&":tiro_Boleng==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",khoutufatso_Boleng,tiro_Boleng==120||tiro_Boleng==124?"%32":"");}
        else if(tiro_Boleng==108||tiro_Boleng==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",tiro_Boleng==112);
        else if(tiro_Boleng==116)내보내기("P(0U-(unsigned)Q());");
        else if(tiro_Boleng==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(tiro_Boleng==132){unsigned 순번=baete_tshedimosetso();int 차이=(int8_t)baete_tshedimosetso();if(순번>=setlhopha_lekanya->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(tiro_Boleng>=145&&tiro_Boleng<=147)내보내기("P((unsigned)(%s)Q());",tiro_Boleng==145?"signed char":tiro_Boleng==146?"unsigned short":"short");
        else if(tiro_Boleng>=153&&tiro_Boleng<=166){int setotwa=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(setotwa<0||setotwa>=(int)setlhopha_lekanya->lekanya){잘못됨=1;break;}if(tiro_Boleng<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[tiro_Boleng-153],setotwa);else if(tiro_Boleng<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[tiro_Boleng-159],setotwa);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",tiro_Boleng==165?"==":"!=",setotwa);}
        else if(tiro_Boleng==167){int setotwa=(int)명령위치+(int16_t)절반값();if(setotwa<0||setotwa>=(int)setlhopha_lekanya->lekanya)잘못됨=1;내보내기("goto L%d;",setotwa);}
        else if(tiro_Boleng==172||tiro_Boleng==176)내보내기("return Q();");else if(tiro_Boleng==177)내보내기("return 0;");
        else if(tiro_Boleng==178||tiro_Boleng==179){unsigned setlhaodi_Boleng=절반값();if(setlhaodi_Boleng<1||setlhaodi_Boleng>=상수모음||Ditlhopha_lenaane[setlhaodi_Boleng]!=9||첫째값[setlhaodi_Boleng]>=상수모음||둘째값[setlhaodi_Boleng]>=상수모음||Ditlhopha_lenaane[첫째값[setlhaodi_Boleng]]!=7||Ditlhopha_lenaane[둘째값[setlhaodi_Boleng]]!=12){잘못됨=1;break;}unsigned mong_selwana=첫째값[첫째값[setlhaodi_Boleng]],leina=첫째값[둘째값[setlhaodi_Boleng]],서술값=둘째값[둘째값[setlhaodi_Boleng]];
            if(tiro_Boleng==178&&Unicode_Boleng(mong_selwana,"java/lang/System")&&Unicode_Boleng(leina,"out")&&Unicode_Boleng(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned faele_tsenyo=0;while(faele_tsenyo<필드개수&&(!같음(leina,leina_la_lefelo[faele_tsenyo])||!같음(서술값,필드서술[faele_tsenyo])))faele_tsenyo++;if(!같음(mong_selwana,첫째값[ga_jaana_mofuta])||faele_tsenyo==필드개수){잘못됨=1;break;}내보내기(tiro_Boleng==178?"P(fields[%u]);":"fields[%u]=Q();",faele_tsenyo);}}
        else if(tiro_Boleng==182||tiro_Boleng==184)호출(절반값(),tiro_Boleng==182);
        else if(tiro_Boleng==188){unsigned tlanya_setlhopha=baete_tshedimosetso();if(tlanya_setlhopha!=4&&tlanya_setlhopha!=5&&tlanya_setlhopha!=8&&tlanya_setlhopha!=9&&tlanya_setlhopha!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(tiro_Boleng==190)내보내기("P(jlength(Q()));");
        else if(tiro_Boleng==198||tiro_Boleng==199){int setotwa=(int)명령위치+(int16_t)절반값();if(setotwa<0||setotwa>=(int)setlhopha_lekanya->lekanya)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",tiro_Boleng==198?"==":"!=",setotwa);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,tiro_Boleng,명령위치);
        내보내기("\n");
    }
    boleele_Boleng=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned dikwalwa_thuto(unsigned *자료위치,unsigned kgaola_Baya_ka_Tekatekanyo){
    if(*자료위치>=kgaola_Baya_ka_Tekatekanyo){잘못됨=1;return 0;}unsigned khoutuletshwao=tshedimosetso[(*자료위치)++];
    if(khoutuletshwao<128)return khoutuletshwao;
    unsigned 개수=khoutuletshwao>=0xc0&&khoutuletshwao<=0xdf?1:khoutuletshwao>=0xe0&&khoutuletshwao<=0xef?2:3;
    if(개수==3||개수>kgaola_Baya_ka_Tekatekanyo-*자료위치){잘못됨=1;return 0;}unsigned Boleng=khoutuletshwao&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=tshedimosetso[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;Boleng=Boleng<<6|(다음&63);}
    if((개수==1&&Boleng<128&&Boleng!=0)||(개수==2&&Boleng<2048))잘못됨=1;return Boleng;
}
static void dikwalwa_tlhomameng(unsigned setlhaodi_Boleng){
    unsigned 부호없는값=첫째값[setlhaodi_Boleng];if(부호없는값<1||부호없는값>=상수모음||Ditlhopha_lenaane[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",setlhaodi_Boleng);
    unsigned 자료위치=첫째값[부호없는값],kgaola_Baya_ka_Tekatekanyo=자료위치+둘째값[부호없는값];
    while(자료위치<kgaola_Baya_ka_Tekatekanyo&&!잘못됨){unsigned khoutuletshwao=dikwalwa_thuto(&자료위치,kgaola_Baya_ka_Tekatekanyo);
        if(khoutuletshwao>=0xd800&&khoutuletshwao<=0xdbff){unsigned 낮은부분=dikwalwa_thuto(&자료위치,kgaola_Baya_ka_Tekatekanyo);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}khoutuletshwao=0x10000+((khoutuletshwao-0xd800)<<10)+낮은부분-0xdc00;}
        else if(khoutuletshwao>=0xdc00&&khoutuletshwao<=0xdfff){잘못됨=1;break;}
        if(!khoutuletshwao){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(khoutuletshwao<128)내보내기("%u,",khoutuletshwao);
        else{unsigned 개수=khoutuletshwao<2048?2:khoutuletshwao<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(khoutuletshwao>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((khoutuletshwao>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*leina){
    size_t 개수=strlen(leina);
    if(개수>4&&!strcmp(leina+개수-4,".jar")){
        if(꾸러미열기(leina)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char tsela[256];const char*tsenyo_mokgwa=꾸러미진입클래스();개수=strlen(tsenyo_mokgwa);if(개수+6>=sizeof(tsela))return 0;
        for(unsigned 순번=0;순번<개수;순번++)tsela[순번]=tsenyo_mokgwa[순번]=='.'?'/':tsenyo_mokgwa[순번];strcpy(tsela+개수,".class");int 항목수=꾸러미읽기(tsela,tshedimosetso,sizeof(tshedimosetso));if(항목수<0)return 0;boleele_Boleng=항목수;
    }else{intptr_t faele_mokgwakamogelo=사용자호출(3,(uintptr_t)leina,0,0,0,0,0);if(faele_mokgwakamogelo<0)return 0;intptr_t 항목수=사용자호출(9,faele_mokgwakamogelo,0,0,0,0,0);if(항목수<0||항목수>sizeof(tshedimosetso)){사용자호출(4,faele_mokgwakamogelo,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,faele_mokgwakamogelo,(uintptr_t)tshedimosetso,항목수,0,0,0);사용자호출(4,faele_mokgwakamogelo,0,0,0,0,0);if(받은수!=항목수)return 0;boleele_Boleng=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Ditlhopha_lenaane[순번]==8)dikwalwa_tlhomameng(순번);
    if(잘못됨)return 0;
    int tsenyo_ntlha=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Unicode_Boleng(메소드목록[순번].leina,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Unicode_Boleng(메소드목록[순번].leina,"main")&&Unicode_Boleng(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)tsenyo_ntlha=순번;
        if(Unicode_Boleng(메소드목록[순번].leina,"<clinit>"))초기값=순번;
    }
    if(tsenyo_ntlha<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)aga_mokgwa(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(lefelo_tlhomameng[순번]){
        unsigned khoutuletshwao=lefelo_tlhomameng[순번];if(khoutuletshwao>=상수모음)return 0;
        if(Ditlhopha_lenaane[khoutuletshwao]==3)내보내기("fields[%u]=%uU;",순번,첫째값[khoutuletshwao]);else if(Ditlhopha_lenaane[khoutuletshwao]==8)내보내기("fields[%u]=(W)k%u;",순번,khoutuletshwao);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",tsenyo_ntlha);
    return 잘못됨?0:SMS;
}
