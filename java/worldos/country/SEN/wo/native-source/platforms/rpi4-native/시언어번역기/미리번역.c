#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "takku_xéewël.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char mbir[16384];static unsigned diir_xëyma,현재위치;static int 잘못됨;
static unsigned Tag_yi_lim[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char Tekst[65536];static unsigned dayo_mbind;
typedef struct {unsigned 설정비트,tur_253d1510,서술값,ndigal_SEQUENCE,tolluwaay,지역변수들,Tegalo_Dencukaay;} doxalin_dugal_xabaar;
static doxalin_dugal_xabaar 메소드목록[64];static unsigned 메소드개수;
static unsigned turu_tool[64],필드서술[64],barabu_denc_ab_joxe_Lees_dul_soppi[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>diir_xëyma||개수>diir_xëyma-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned okte_mbir(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:mbir[자료위치];}
static unsigned 절반값(void){unsigned rëddu_iks_yi=okte_mbir();return rëddu_iks_yi<<8|okte_mbir();}
static uint32_t 가득참(void){uint32_t rëddu_iks_yi=절반값();return rëddu_iks_yi<<16|절반값();}
static int Unicode_xëyma(unsigned 순번,const char*araf_yu_bennoo_mbir){return 순번>0&&순번<상수모음&&Tag_yi_lim[순번]==1&&strlen(araf_yu_bennoo_mbir)==둘째값[순번]&&!memcmp(mbir+첫째값[순번],araf_yu_bennoo_mbir,둘째값[순번]);}
static int 같음(unsigned rëddu_iks_yi,unsigned 세로좌표){return rëddu_iks_yi>0&&rëddu_iks_yi<상수모음&&세로좌표>0&&세로좌표<상수모음&&Tag_yi_lim[rëddu_iks_yi]==1&&Tag_yi_lim[세로좌표]==1&&둘째값[rëddu_iks_yi]==둘째값[세로좌표]&&!memcmp(mbir+첫째값[rëddu_iks_yi],mbir+첫째값[세로좌표],둘째값[rëddu_iks_yi]);}
static void 내보내기(const char*bara_denc_dugal_xabaar,...){if(잘못됨)return;va_list Tegtal_TABLO;va_start(Tegtal_TABLO,bara_denc_dugal_xabaar);int 개수=vsnprintf(Tekst+dayo_mbind,sizeof(Tekst)-dayo_mbind,bara_denc_dugal_xabaar,Tegtal_TABLO);va_end(Tegtal_TABLO);if(개수<0||(unsigned)개수>=sizeof(Tekst)-dayo_mbind){잘못됨=1;return;}dayo_mbind+=개수;}
static int 서술자(unsigned raññeekaay_xëyma,int*결과){
    if(raññeekaay_xëyma<1||raññeekaay_xëyma>=상수모음||Tag_yi_lim[raññeekaay_xëyma]!=1)return -1;unsigned 자료위치=첫째값[raññeekaay_xëyma],jeexal_Randal=자료위치+둘째값[raññeekaay_xëyma];if(자료위치>=jeexal_Randal||mbir[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<jeexal_Randal&&mbir[자료위치]!=')'){
        unsigned kotu_araf=mbir[자료위치++];while(kotu_araf=='['&&자료위치<jeexal_Randal)kotu_araf=mbir[자료위치++];
        if(kotu_araf=='L'){while(자료위치<jeexal_Randal&&mbir[자료위치]!=';')자료위치++;if(자료위치==jeexal_Randal)return -1;자료위치++;}
        else if(kotu_araf!='I'&&kotu_araf!='Z'&&kotu_araf!='B'&&kotu_araf!='C'&&kotu_araf!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=jeexal_Randal||mbir[자료위치++]!=')')return -1;*결과=mbir[자료위치]=='V'?0:1;
    if(mbir[자료위치]=='J'||mbir[자료위치]=='D'||mbir[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned tolluwaay=가득참();가져오기(tolluwaay);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned xale_taalif=절반값(),판번호=절반값();if(xale_taalif||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Tag_yi_lim[순번]=okte_mbir();switch(Tag_yi_lim[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=okte_mbir();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Tag_yi_lim[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Tag_yi_lim[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();turu_tool[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned tur_253d1510=절반값(),tolluwaay=가득참();
            if(Unicode_xëyma(tur_253d1510,"ConstantValue")){if(tolluwaay!=2)return -1;barabu_denc_ab_joxe_Lees_dul_soppi[순번]=절반값();}
            else 가져오기(tolluwaay);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        doxalin_dugal_xabaar*mboolo_tolluwaay=메소드목록+순번;mboolo_tolluwaay->설정비트=절반값();mboolo_tolluwaay->tur_253d1510=절반값();mboolo_tolluwaay->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned tur_253d1510=절반값(),tolluwaay=가득참(),daw=현재위치;
            if(tolluwaay>diir_xëyma-현재위치)return -1;
            if(Unicode_xëyma(tur_253d1510,"Code")){
                mboolo_tolluwaay->Tegalo_Dencukaay=절반값();mboolo_tolluwaay->지역변수들=절반값();mboolo_tolluwaay->tolluwaay=가득참();mboolo_tolluwaay->ndigal_SEQUENCE=가져오기(mboolo_tolluwaay->tolluwaay);
                if(mboolo_tolluwaay->Tegalo_Dencukaay>128||mboolo_tolluwaay->지역변수들>128||mboolo_tolluwaay->tolluwaay>8192||절반값())return -1;속성들();
            }else 가져오기(tolluwaay);
            if(현재위치!=daw+tolluwaay)return -1;
        }
        if(!Unicode_xëyma(mboolo_tolluwaay->tur_253d1510,"<init>")&&(!(mboolo_tolluwaay->설정비트&8)||(mboolo_tolluwaay->설정비트&(0x100|0x20))||!mboolo_tolluwaay->tolluwaay))return -1;
    }
    속성들();return 잘못됨||현재위치!=diir_xëyma?-1:0;
}
static void Lees_dul_soppi_xëyma(unsigned raññeekaay_xëyma){
    if(!raññeekaay_xëyma||raññeekaay_xëyma>=상수모음){잘못됨=1;return;}
    if(Tag_yi_lim[raññeekaay_xëyma]==3)내보내기("P(%uU);",첫째값[raññeekaay_xëyma]);
    else if(Tag_yi_lim[raññeekaay_xëyma]==8)내보내기("P((W)k%u);",raññeekaay_xëyma);else 잘못됨=1;
}
static void 호출(unsigned raññeekaay_xëyma,int luy_feeñ_te_jëmmadi_Wuute){
    if(raññeekaay_xëyma<1||raññeekaay_xëyma>=상수모음||(Tag_yi_lim[raññeekaay_xëyma]!=10&&Tag_yi_lim[raññeekaay_xëyma]!=11)||첫째값[raññeekaay_xëyma]<1||첫째값[raññeekaay_xëyma]>=상수모음||Tag_yi_lim[첫째값[raññeekaay_xëyma]]!=7||둘째값[raññeekaay_xëyma]<1||둘째값[raññeekaay_xëyma]>=상수모음||Tag_yi_lim[둘째값[raññeekaay_xëyma]]!=12){잘못됨=1;return;}
    unsigned boroom_yëf=첫째값[첫째값[raññeekaay_xëyma]],tur_253d1510=첫째값[둘째값[raññeekaay_xëyma]],서술값=둘째값[둘째값[raññeekaay_xëyma]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(luy_feeñ_te_jëmmadi_Wuute)내보내기("Q();");
    if(!luy_feeñ_te_jëmmadi_Wuute&&같음(boroom_yëf,첫째값[현재클래스])){
        unsigned mboolo_tolluwaay=0;for(;mboolo_tolluwaay<메소드개수;mboolo_tolluwaay++)if(같음(tur_253d1510,메소드목록[mboolo_tolluwaay].tur_253d1510)&&같음(서술값,메소드목록[mboolo_tolluwaay].서술값))break;
        if(mboolo_tolluwaay==메소드개수||!(메소드목록[mboolo_tolluwaay].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",mboolo_tolluwaay);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((luy_feeñ_te_jëmmadi_Wuute&&Unicode_xëyma(boroom_yëf,"java/io/PrintStream")&& (Unicode_xëyma(tur_253d1510,"print")||Unicode_xëyma(tur_253d1510,"println")))||(!luy_feeñ_te_jëmmadi_Wuute&&Unicode_xëyma(boroom_yëf,"한국어/자체/출력"))){
        if(Unicode_xëyma(서술값,"(I)V")&&(Unicode_xëyma(tur_253d1510,"print")||Unicode_xëyma(tur_253d1510,"println")||Unicode_xëyma(tur_253d1510,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Unicode_xëyma(tur_253d1510,"print")?0:1);return;}
        if(Unicode_xëyma(서술값,"(Ljava/lang/String;)V")&&(Unicode_xëyma(tur_253d1510,"print")||Unicode_xëyma(tur_253d1510,"println")||Unicode_xëyma(tur_253d1510,"biir")||Unicode_xëyma(tur_253d1510,"biir_buum"))){내보내기("jprint(x[0],0,%d);",Unicode_xëyma(tur_253d1510,"print")||Unicode_xëyma(tur_253d1510,"biir")?0:1);return;}
        if(Unicode_xëyma(서술값,"()V")&&Unicode_xëyma(tur_253d1510,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!luy_feeñ_te_jëmmadi_Wuute&&Unicode_xëyma(boroom_yëf,"한국어/자체/bara_denc")){
        if(Unicode_xëyma(tur_253d1510,"biir")&&Unicode_xëyma(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Unicode_xëyma(tur_253d1510,"읽기")&&Unicode_xëyma(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void tabax_doxalin(unsigned 색인){
    doxalin_dugal_xabaar*mboolo_tolluwaay=메소드목록+색인;if(Unicode_xëyma(mboolo_tolluwaay->tur_253d1510,"<init>"))return;int 결과,개수=서술자(mboolo_tolluwaay->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>mboolo_tolluwaay->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",mboolo_tolluwaay->지역변수들?mboolo_tolluwaay->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=diir_xëyma;diir_xëyma=mboolo_tolluwaay->ndigal_SEQUENCE+mboolo_tolluwaay->tolluwaay;현재위치=mboolo_tolluwaay->ndigal_SEQUENCE;
    while(현재위치<diir_xëyma&&!잘못됨){unsigned 명령위치=현재위치-mboolo_tolluwaay->ndigal_SEQUENCE,sëfu_xayma_xëyma=okte_mbir();내보내기("L%u:;",명령위치);
        if(sëfu_xayma_xëyma==0){}
        else if(sëfu_xayma_xëyma==1)내보내기("P(0);");
        else if(sëfu_xayma_xëyma>=2&&sëfu_xayma_xëyma<=8)내보내기("P(%uU);",sëfu_xayma_xëyma-3);
        else if(sëfu_xayma_xëyma==16){int xëyma=(int8_t)okte_mbir();내보내기("P(%uU);",(unsigned)xëyma);}
        else if(sëfu_xayma_xëyma==17){int xëyma=(int16_t)절반값();내보내기("P(%uU);",(unsigned)xëyma);}
        else if(sëfu_xayma_xëyma==18||sëfu_xayma_xëyma==19)Lees_dul_soppi_xëyma(sëfu_xayma_xëyma==18?okte_mbir():절반값());
        else if(sëfu_xayma_xëyma==21||sëfu_xayma_xëyma==25){unsigned 순번=okte_mbir();if(순번>=mboolo_tolluwaay->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((sëfu_xayma_xëyma>=26&&sëfu_xayma_xëyma<=29)||(sëfu_xayma_xëyma>=42&&sëfu_xayma_xëyma<=45)){unsigned 순번=sëfu_xayma_xëyma>=42?sëfu_xayma_xëyma-42:sëfu_xayma_xëyma-26;if(순번>=mboolo_tolluwaay->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(sëfu_xayma_xëyma==54||sëfu_xayma_xëyma==58){unsigned 순번=okte_mbir();if(순번>=mboolo_tolluwaay->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((sëfu_xayma_xëyma>=59&&sëfu_xayma_xëyma<=62)||(sëfu_xayma_xëyma>=75&&sëfu_xayma_xëyma<=78)){unsigned 순번=sëfu_xayma_xëyma>=75?sëfu_xayma_xëyma-75:sëfu_xayma_xëyma-59;if(순번>=mboolo_tolluwaay->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(sëfu_xayma_xëyma==46||sëfu_xayma_xëyma==50||sëfu_xayma_xëyma==51||sëfu_xayma_xëyma==52||sëfu_xayma_xëyma==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(sëfu_xayma_xëyma==79||sëfu_xayma_xëyma==83||sëfu_xayma_xëyma==84||sëfu_xayma_xëyma==85||sëfu_xayma_xëyma==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",sëfu_xayma_xëyma==84?"(unsigned)(signed char)q":sëfu_xayma_xëyma==85?"(unsigned short)q":sëfu_xayma_xëyma==86?"(unsigned)(short)q":"q");
        else if(sëfu_xayma_xëyma==87)내보내기("Q();");
        else if(sëfu_xayma_xëyma==89)내보내기("q=Q();P(q);P(q);");
        else if(sëfu_xayma_xëyma==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(sëfu_xayma_xëyma==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(sëfu_xayma_xëyma==96||sëfu_xayma_xëyma==100||sëfu_xayma_xëyma==104||sëfu_xayma_xëyma==120||sëfu_xayma_xëyma==124||sëfu_xayma_xëyma==126||sëfu_xayma_xëyma==128||sëfu_xayma_xëyma==130){const char*nëbbin_ci_lim_xëyma=sëfu_xayma_xëyma==96?"+":sëfu_xayma_xëyma==100?"-":sëfu_xayma_xëyma==104?"*":sëfu_xayma_xëyma==120?"<<":sëfu_xayma_xëyma==124?">>":sëfu_xayma_xëyma==126?"&":sëfu_xayma_xëyma==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",nëbbin_ci_lim_xëyma,sëfu_xayma_xëyma==120||sëfu_xayma_xëyma==124?"%32":"");}
        else if(sëfu_xayma_xëyma==108||sëfu_xayma_xëyma==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",sëfu_xayma_xëyma==112);
        else if(sëfu_xayma_xëyma==116)내보내기("P(0U-(unsigned)Q());");
        else if(sëfu_xayma_xëyma==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(sëfu_xayma_xëyma==132){unsigned 순번=okte_mbir();int 차이=(int8_t)okte_mbir();if(순번>=mboolo_tolluwaay->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(sëfu_xayma_xëyma>=145&&sëfu_xayma_xëyma<=147)내보내기("P((unsigned)(%s)Q());",sëfu_xayma_xëyma==145?"signed char":sëfu_xayma_xëyma==146?"unsigned short":"short");
        else if(sëfu_xayma_xëyma>=153&&sëfu_xayma_xëyma<=166){int luñu_name=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(luñu_name<0||luñu_name>=(int)mboolo_tolluwaay->tolluwaay){잘못됨=1;break;}if(sëfu_xayma_xëyma<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[sëfu_xayma_xëyma-153],luñu_name);else if(sëfu_xayma_xëyma<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[sëfu_xayma_xëyma-159],luñu_name);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",sëfu_xayma_xëyma==165?"==":"!=",luñu_name);}
        else if(sëfu_xayma_xëyma==167){int luñu_name=(int)명령위치+(int16_t)절반값();if(luñu_name<0||luñu_name>=(int)mboolo_tolluwaay->tolluwaay)잘못됨=1;내보내기("goto L%d;",luñu_name);}
        else if(sëfu_xayma_xëyma==172||sëfu_xayma_xëyma==176)내보내기("return Q();");else if(sëfu_xayma_xëyma==177)내보내기("return 0;");
        else if(sëfu_xayma_xëyma==178||sëfu_xayma_xëyma==179){unsigned raññeekaay_xëyma=절반값();if(raññeekaay_xëyma<1||raññeekaay_xëyma>=상수모음||Tag_yi_lim[raññeekaay_xëyma]!=9||첫째값[raññeekaay_xëyma]>=상수모음||둘째값[raññeekaay_xëyma]>=상수모음||Tag_yi_lim[첫째값[raññeekaay_xëyma]]!=7||Tag_yi_lim[둘째값[raññeekaay_xëyma]]!=12){잘못됨=1;break;}unsigned boroom_yëf=첫째값[첫째값[raññeekaay_xëyma]],tur_253d1510=첫째값[둘째값[raññeekaay_xëyma]],서술값=둘째값[둘째값[raññeekaay_xëyma]];
            if(sëfu_xayma_xëyma==178&&Unicode_xëyma(boroom_yëf,"java/lang/System")&&Unicode_xëyma(tur_253d1510,"out")&&Unicode_xëyma(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned bara_denc_dugal_xabaar=0;while(bara_denc_dugal_xabaar<필드개수&&(!같음(tur_253d1510,turu_tool[bara_denc_dugal_xabaar])||!같음(서술값,필드서술[bara_denc_dugal_xabaar])))bara_denc_dugal_xabaar++;if(!같음(boroom_yëf,첫째값[현재클래스])||bara_denc_dugal_xabaar==필드개수){잘못됨=1;break;}내보내기(sëfu_xayma_xëyma==178?"P(fields[%u]);":"fields[%u]=Q();",bara_denc_dugal_xabaar);}}
        else if(sëfu_xayma_xëyma==182||sëfu_xayma_xëyma==184)호출(절반값(),sëfu_xayma_xëyma==182);
        else if(sëfu_xayma_xëyma==188){unsigned xeet_ngiir=okte_mbir();if(xeet_ngiir!=4&&xeet_ngiir!=5&&xeet_ngiir!=8&&xeet_ngiir!=9&&xeet_ngiir!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(sëfu_xayma_xëyma==190)내보내기("P(jlength(Q()));");
        else if(sëfu_xayma_xëyma==198||sëfu_xayma_xëyma==199){int luñu_name=(int)명령위치+(int16_t)절반값();if(luñu_name<0||luñu_name>=(int)mboolo_tolluwaay->tolluwaay)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",sëfu_xayma_xëyma==198?"==":"!=",luñu_name);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,sëfu_xayma_xëyma,명령위치);
        내보내기("\n");
    }
    diir_xëyma=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned araf_yu_bennoo_sa(unsigned *자료위치,unsigned jeexal_Randal){
    if(*자료위치>=jeexal_Randal){잘못됨=1;return 0;}unsigned kotu_araf=mbir[(*자료위치)++];
    if(kotu_araf<128)return kotu_araf;
    unsigned 개수=kotu_araf>=0xc0&&kotu_araf<=0xdf?1:kotu_araf>=0xe0&&kotu_araf<=0xef?2:3;
    if(개수==3||개수>jeexal_Randal-*자료위치){잘못됨=1;return 0;}unsigned xëyma=kotu_araf&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=mbir[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;xëyma=xëyma<<6|(다음&63);}
    if((개수==1&&xëyma<128&&xëyma!=0)||(개수==2&&xëyma<2048))잘못됨=1;return xëyma;
}
static void araf_yu_bennoo_Lees_dul_soppi(unsigned raññeekaay_xëyma){
    unsigned 부호없는값=첫째값[raññeekaay_xëyma];if(부호없는값<1||부호없는값>=상수모음||Tag_yi_lim[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",raññeekaay_xëyma);
    unsigned 자료위치=첫째값[부호없는값],jeexal_Randal=자료위치+둘째값[부호없는값];
    while(자료위치<jeexal_Randal&&!잘못됨){unsigned kotu_araf=araf_yu_bennoo_sa(&자료위치,jeexal_Randal);
        if(kotu_araf>=0xd800&&kotu_araf<=0xdbff){unsigned 낮은부분=araf_yu_bennoo_sa(&자료위치,jeexal_Randal);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}kotu_araf=0x10000+((kotu_araf-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kotu_araf>=0xdc00&&kotu_araf<=0xdfff){잘못됨=1;break;}
        if(!kotu_araf){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(kotu_araf<128)내보내기("%u,",kotu_araf);
        else{unsigned 개수=kotu_araf<2048?2:kotu_araf<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(kotu_araf>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((kotu_araf>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*tur_253d1510){
    size_t 개수=strlen(tur_253d1510);
    if(개수>4&&!strcmp(tur_253d1510+개수-4,".jar")){
        if(꾸러미열기(tur_253d1510)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Yoonu_jëmale[256];const char*dugal_xabaar_doxalin=꾸러미진입클래스();개수=strlen(dugal_xabaar_doxalin);if(개수+6>=sizeof(Yoonu_jëmale))return 0;
        for(unsigned 순번=0;순번<개수;순번++)Yoonu_jëmale[순번]=dugal_xabaar_doxalin[순번]=='.'?'/':dugal_xabaar_doxalin[순번];strcpy(Yoonu_jëmale+개수,".class");int 항목수=꾸러미읽기(Yoonu_jëmale,mbir,sizeof(mbir));if(항목수<0)return 0;diir_xëyma=항목수;
    }else{intptr_t bara_denc_yombal=사용자호출(3,(uintptr_t)tur_253d1510,0,0,0,0,0);if(bara_denc_yombal<0)return 0;intptr_t 항목수=사용자호출(9,bara_denc_yombal,0,0,0,0,0);if(항목수<0||항목수>sizeof(mbir)){사용자호출(4,bara_denc_yombal,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,bara_denc_yombal,(uintptr_t)mbir,항목수,0,0,0);사용자호출(4,bara_denc_yombal,0,0,0,0,0);if(받은수!=항목수)return 0;diir_xëyma=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Tag_yi_lim[순번]==8)araf_yu_bennoo_Lees_dul_soppi(순번);
    if(잘못됨)return 0;
    int dugal_xabaar_Tomb=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Unicode_xëyma(메소드목록[순번].tur_253d1510,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Unicode_xëyma(메소드목록[순번].tur_253d1510,"main")&&Unicode_xëyma(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)dugal_xabaar_Tomb=순번;
        if(Unicode_xëyma(메소드목록[순번].tur_253d1510,"<clinit>"))초기값=순번;
    }
    if(dugal_xabaar_Tomb<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)tabax_doxalin(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(barabu_denc_ab_joxe_Lees_dul_soppi[순번]){
        unsigned kotu_araf=barabu_denc_ab_joxe_Lees_dul_soppi[순번];if(kotu_araf>=상수모음)return 0;
        if(Tag_yi_lim[kotu_araf]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kotu_araf]);else if(Tag_yi_lim[kotu_araf]==8)내보내기("fields[%u]=(W)k%u;",순번,kotu_araf);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",dugal_xabaar_Tomb);
    return 잘못됨?0:Tekst;
}
