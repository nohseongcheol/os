#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "ngwungwu.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char datà[16384];static unsigned ogologo_valuu,현재위치;static int 잘못됨;
static unsigned nhụbaama_ndepụta[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char SMS[65536];static unsigned ụha_ngwe;
typedef struct {unsigned 설정비트,Aha,서술값,okwunkụzi_NSOTANSO,Ụhara,지역변수들,ikpo_Nchekwa;} usoro_ndebà;
static usoro_ndebà 메소드목록[64];static unsigned 메소드개수;
static unsigned ahà_fild[64],필드서술[64],fild_ihendịgide[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>ogologo_valuu||개수>ogologo_valuu-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned baịtị_datà(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:datà[자료위치];}
static unsigned 절반값(void){unsigned ngakọrịta_x=baịtị_datà();return ngakọrịta_x<<8|baịtị_datà();}
static uint32_t 가득참(void){uint32_t ngakọrịta_x=절반값();return ngakọrịta_x<<16|절반값();}
static int Yunīkoòdù_valuu(unsigned 순번,const char*ùsòròokwū_datà){return 순번>0&&순번<상수모음&&nhụbaama_ndepụta[순번]==1&&strlen(ùsòròokwū_datà)==둘째값[순번]&&!memcmp(datà+첫째값[순번],ùsòròokwū_datà,둘째값[순번]);}
static int 같음(unsigned ngakọrịta_x,unsigned 세로좌표){return ngakọrịta_x>0&&ngakọrịta_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&nhụbaama_ndepụta[ngakọrịta_x]==1&&nhụbaama_ndepụta[세로좌표]==1&&둘째값[ngakọrịta_x]==둘째값[세로좌표]&&!memcmp(datà+첫째값[ngakọrịta_x],datà+첫째값[세로좌표],둘째값[ngakọrịta_x]);}
static void 내보내기(const char*ọbọakwụkwọ_ndebà,...){if(잘못됨)return;va_list agụment_MKPOKỌTA;va_start(agụment_MKPOKỌTA,ọbọakwụkwọ_ndebà);int 개수=vsnprintf(SMS+ụha_ngwe,sizeof(SMS)-ụha_ngwe,ọbọakwụkwọ_ndebà,agụment_MKPOKỌTA);va_end(agụment_MKPOKỌTA);if(개수<0||(unsigned)개수>=sizeof(SMS)-ụha_ngwe){잘못됨=1;return;}ụha_ngwe+=개수;}
static int 서술자(unsigned ihe_nkọwapụta_valuu,int*결과){
    if(ihe_nkọwapụta_valuu<1||ihe_nkọwapụta_valuu>=상수모음||nhụbaama_ndepụta[ihe_nkọwapụta_valuu]!=1)return -1;unsigned 자료위치=첫째값[ihe_nkọwapụta_valuu],mèdebe_Nnokwata=자료위치+둘째값[ihe_nkọwapụta_valuu];if(자료위치>=mèdebe_Nnokwata||datà[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<mèdebe_Nnokwata&&datà[자료위치]!=')'){
        unsigned koòdù_nkeakàrà=datà[자료위치++];while(koòdù_nkeakàrà=='['&&자료위치<mèdebe_Nnokwata)koòdù_nkeakàrà=datà[자료위치++];
        if(koòdù_nkeakàrà=='L'){while(자료위치<mèdebe_Nnokwata&&datà[자료위치]!=';')자료위치++;if(자료위치==mèdebe_Nnokwata)return -1;자료위치++;}
        else if(koòdù_nkeakàrà!='I'&&koòdù_nkeakàrà!='Z'&&koòdù_nkeakàrà!='B'&&koòdù_nkeakàrà!='C'&&koòdù_nkeakàrà!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=mèdebe_Nnokwata||datà[자료위치++]!=')')return -1;*결과=datà[자료위치]=='V'?0:1;
    if(datà[자료위치]=='J'||datà[자료위치]=='D'||datà[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned Ụhara=가득참();가져오기(Ụhara);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned obere_nwa_ụdị=절반값(),판번호=절반값();if(obere_nwa_ụdị||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        nhụbaama_ndepụta[순번]=baịtị_datà();switch(nhụbaama_ndepụta[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=baịtị_datà();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||nhụbaama_ndepụta[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||nhụbaama_ndepụta[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();ahà_fild[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Aha=절반값(),Ụhara=가득참();
            if(Yunīkoòdù_valuu(Aha,"ConstantValue")){if(Ụhara!=2)return -1;fild_ihendịgide[순번]=절반값();}
            else 가져오기(Ụhara);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        usoro_ndebà*otu_ụha=메소드목록+순번;otu_ụha->설정비트=절반값();otu_ụha->Aha=절반값();otu_ụha->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Aha=절반값(),Ụhara=가득참(),Bido=현재위치;
            if(Ụhara>ogologo_valuu-현재위치)return -1;
            if(Yunīkoòdù_valuu(Aha,"Code")){
                otu_ụha->ikpo_Nchekwa=절반값();otu_ụha->지역변수들=절반값();otu_ụha->Ụhara=가득참();otu_ụha->okwunkụzi_NSOTANSO=가져오기(otu_ụha->Ụhara);
                if(otu_ụha->ikpo_Nchekwa>128||otu_ụha->지역변수들>128||otu_ụha->Ụhara>8192||절반값())return -1;속성들();
            }else 가져오기(Ụhara);
            if(현재위치!=Bido+Ụhara)return -1;
        }
        if(!Yunīkoòdù_valuu(otu_ụha->Aha,"<init>")&&(!(otu_ụha->설정비트&8)||(otu_ụha->설정비트&(0x100|0x20))||!otu_ụha->Ụhara))return -1;
    }
    속성들();return 잘못됨||현재위치!=ogologo_valuu?-1:0;
}
static void ihendịgide_valuu(unsigned ihe_nkọwapụta_valuu){
    if(!ihe_nkọwapụta_valuu||ihe_nkọwapụta_valuu>=상수모음){잘못됨=1;return;}
    if(nhụbaama_ndepụta[ihe_nkọwapụta_valuu]==3)내보내기("P(%uU);",첫째값[ihe_nkọwapụta_valuu]);
    else if(nhụbaama_ndepụta[ihe_nkọwapụta_valuu]==8)내보내기("P((W)k%u);",ihe_nkọwapụta_valuu);else 잘못됨=1;
}
static void 호출(unsigned ihe_nkọwapụta_valuu,int kendìnuchè_oku){
    if(ihe_nkọwapụta_valuu<1||ihe_nkọwapụta_valuu>=상수모음||(nhụbaama_ndepụta[ihe_nkọwapụta_valuu]!=10&&nhụbaama_ndepụta[ihe_nkọwapụta_valuu]!=11)||첫째값[ihe_nkọwapụta_valuu]<1||첫째값[ihe_nkọwapụta_valuu]>=상수모음||nhụbaama_ndepụta[첫째값[ihe_nkọwapụta_valuu]]!=7||둘째값[ihe_nkọwapụta_valuu]<1||둘째값[ihe_nkọwapụta_valuu]>=상수모음||nhụbaama_ndepụta[둘째값[ihe_nkọwapụta_valuu]]!=12){잘못됨=1;return;}
    unsigned nwe_ihe=첫째값[첫째값[ihe_nkọwapụta_valuu]],Aha=첫째값[둘째값[ihe_nkọwapụta_valuu]],서술값=둘째값[둘째값[ihe_nkọwapụta_valuu]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(kendìnuchè_oku)내보내기("Q();");
    if(!kendìnuchè_oku&&같음(nwe_ihe,첫째값[현재클래스])){
        unsigned otu_ụha=0;for(;otu_ụha<메소드개수;otu_ụha++)if(같음(Aha,메소드목록[otu_ụha].Aha)&&같음(서술값,메소드목록[otu_ụha].서술값))break;
        if(otu_ụha==메소드개수||!(메소드목록[otu_ụha].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",otu_ụha);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((kendìnuchè_oku&&Yunīkoòdù_valuu(nwe_ihe,"java/io/PrintStream")&& (Yunīkoòdù_valuu(Aha,"print")||Yunīkoòdù_valuu(Aha,"println")))||(!kendìnuchè_oku&&Yunīkoòdù_valuu(nwe_ihe,"한국어/자체/출력"))){
        if(Yunīkoòdù_valuu(서술값,"(I)V")&&(Yunīkoòdù_valuu(Aha,"print")||Yunīkoòdù_valuu(Aha,"println")||Yunīkoòdù_valuu(Aha,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Yunīkoòdù_valuu(Aha,"print")?0:1);return;}
        if(Yunīkoòdù_valuu(서술값,"(Ljava/lang/String;)V")&&(Yunīkoòdù_valuu(Aha,"print")||Yunīkoòdù_valuu(Aha,"println")||Yunīkoòdù_valuu(Aha,"Chekwaa_ozi")||Yunīkoòdù_valuu(Aha,"dee_ahịrī"))){내보내기("jprint(x[0],0,%d);",Yunīkoòdù_valuu(Aha,"print")||Yunīkoòdù_valuu(Aha,"Chekwaa_ozi")?0:1);return;}
        if(Yunīkoòdù_valuu(서술값,"()V")&&Yunīkoòdù_valuu(Aha,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!kendìnuchè_oku&&Yunīkoòdù_valuu(nwe_ihe,"한국어/자체/Faịlụ")){
        if(Yunīkoòdù_valuu(Aha,"Chekwaa_ozi")&&Yunīkoòdù_valuu(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Yunīkoòdù_valuu(Aha,"Wepụta_ọzi")&&Yunīkoòdù_valuu(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void wue_usoro(unsigned 색인){
    usoro_ndebà*otu_ụha=메소드목록+색인;if(Yunīkoòdù_valuu(otu_ụha->Aha,"<init>"))return;int 결과,개수=서술자(otu_ụha->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>otu_ụha->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",otu_ụha->지역변수들?otu_ụha->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=ogologo_valuu;ogologo_valuu=otu_ụha->okwunkụzi_NSOTANSO+otu_ụha->Ụhara;현재위치=otu_ụha->okwunkụzi_NSOTANSO;
    while(현재위치<ogologo_valuu&&!잘못됨){unsigned 명령위치=현재위치-otu_ụha->okwunkụzi_NSOTANSO,àrụmọrụ_valuu=baịtị_datà();내보내기("L%u:;",명령위치);
        if(àrụmọrụ_valuu==0){}
        else if(àrụmọrụ_valuu==1)내보내기("P(0);");
        else if(àrụmọrụ_valuu>=2&&àrụmọrụ_valuu<=8)내보내기("P(%uU);",àrụmọrụ_valuu-3);
        else if(àrụmọrụ_valuu==16){int valuu=(int8_t)baịtị_datà();내보내기("P(%uU);",(unsigned)valuu);}
        else if(àrụmọrụ_valuu==17){int valuu=(int16_t)절반값();내보내기("P(%uU);",(unsigned)valuu);}
        else if(àrụmọrụ_valuu==18||àrụmọrụ_valuu==19)ihendịgide_valuu(àrụmọrụ_valuu==18?baịtị_datà():절반값());
        else if(àrụmọrụ_valuu==21||àrụmọrụ_valuu==25){unsigned 순번=baịtị_datà();if(순번>=otu_ụha->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((àrụmọrụ_valuu>=26&&àrụmọrụ_valuu<=29)||(àrụmọrụ_valuu>=42&&àrụmọrụ_valuu<=45)){unsigned 순번=àrụmọrụ_valuu>=42?àrụmọrụ_valuu-42:àrụmọrụ_valuu-26;if(순번>=otu_ụha->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(àrụmọrụ_valuu==54||àrụmọrụ_valuu==58){unsigned 순번=baịtị_datà();if(순번>=otu_ụha->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((àrụmọrụ_valuu>=59&&àrụmọrụ_valuu<=62)||(àrụmọrụ_valuu>=75&&àrụmọrụ_valuu<=78)){unsigned 순번=àrụmọrụ_valuu>=75?àrụmọrụ_valuu-75:àrụmọrụ_valuu-59;if(순번>=otu_ụha->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(àrụmọrụ_valuu==46||àrụmọrụ_valuu==50||àrụmọrụ_valuu==51||àrụmọrụ_valuu==52||àrụmọrụ_valuu==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(àrụmọrụ_valuu==79||àrụmọrụ_valuu==83||àrụmọrụ_valuu==84||àrụmọrụ_valuu==85||àrụmọrụ_valuu==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",àrụmọrụ_valuu==84?"(unsigned)(signed char)q":àrụmọrụ_valuu==85?"(unsigned short)q":àrụmọrụ_valuu==86?"(unsigned)(short)q":"q");
        else if(àrụmọrụ_valuu==87)내보내기("Q();");
        else if(àrụmọrụ_valuu==89)내보내기("q=Q();P(q);P(q);");
        else if(àrụmọrụ_valuu==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(àrụmọrụ_valuu==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(àrụmọrụ_valuu==96||àrụmọrụ_valuu==100||àrụmọrụ_valuu==104||àrụmọrụ_valuu==120||àrụmọrụ_valuu==124||àrụmọrụ_valuu==126||àrụmọrụ_valuu==128||àrụmọrụ_valuu==130){const char*ntinye_koòdù_valuu=àrụmọrụ_valuu==96?"+":àrụmọrụ_valuu==100?"-":àrụmọrụ_valuu==104?"*":àrụmọrụ_valuu==120?"<<":àrụmọrụ_valuu==124?">>":àrụmọrụ_valuu==126?"&":àrụmọrụ_valuu==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",ntinye_koòdù_valuu,àrụmọrụ_valuu==120||àrụmọrụ_valuu==124?"%32":"");}
        else if(àrụmọrụ_valuu==108||àrụmọrụ_valuu==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",àrụmọrụ_valuu==112);
        else if(àrụmọrụ_valuu==116)내보내기("P(0U-(unsigned)Q());");
        else if(àrụmọrụ_valuu==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(àrụmọrụ_valuu==132){unsigned 순번=baịtị_datà();int 차이=(int8_t)baịtị_datà();if(순번>=otu_ụha->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(àrụmọrụ_valuu>=145&&àrụmọrụ_valuu<=147)내보내기("P((unsigned)(%s)Q());",àrụmọrụ_valuu==145?"signed char":àrụmọrụ_valuu==146?"unsigned short":"short");
        else if(àrụmọrụ_valuu>=153&&àrụmọrụ_valuu<=166){int ebenlereanya=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(ebenlereanya<0||ebenlereanya>=(int)otu_ụha->Ụhara){잘못됨=1;break;}if(àrụmọrụ_valuu<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[àrụmọrụ_valuu-153],ebenlereanya);else if(àrụmọrụ_valuu<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[àrụmọrụ_valuu-159],ebenlereanya);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",àrụmọrụ_valuu==165?"==":"!=",ebenlereanya);}
        else if(àrụmọrụ_valuu==167){int ebenlereanya=(int)명령위치+(int16_t)절반값();if(ebenlereanya<0||ebenlereanya>=(int)otu_ụha->Ụhara)잘못됨=1;내보내기("goto L%d;",ebenlereanya);}
        else if(àrụmọrụ_valuu==172||àrụmọrụ_valuu==176)내보내기("return Q();");else if(àrụmọrụ_valuu==177)내보내기("return 0;");
        else if(àrụmọrụ_valuu==178||àrụmọrụ_valuu==179){unsigned ihe_nkọwapụta_valuu=절반값();if(ihe_nkọwapụta_valuu<1||ihe_nkọwapụta_valuu>=상수모음||nhụbaama_ndepụta[ihe_nkọwapụta_valuu]!=9||첫째값[ihe_nkọwapụta_valuu]>=상수모음||둘째값[ihe_nkọwapụta_valuu]>=상수모음||nhụbaama_ndepụta[첫째값[ihe_nkọwapụta_valuu]]!=7||nhụbaama_ndepụta[둘째값[ihe_nkọwapụta_valuu]]!=12){잘못됨=1;break;}unsigned nwe_ihe=첫째값[첫째값[ihe_nkọwapụta_valuu]],Aha=첫째값[둘째값[ihe_nkọwapụta_valuu]],서술값=둘째값[둘째값[ihe_nkọwapụta_valuu]];
            if(àrụmọrụ_valuu==178&&Yunīkoòdù_valuu(nwe_ihe,"java/lang/System")&&Yunīkoòdù_valuu(Aha,"out")&&Yunīkoòdù_valuu(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned ọbọakwụkwọ_ndebà=0;while(ọbọakwụkwọ_ndebà<필드개수&&(!같음(Aha,ahà_fild[ọbọakwụkwọ_ndebà])||!같음(서술값,필드서술[ọbọakwụkwọ_ndebà])))ọbọakwụkwọ_ndebà++;if(!같음(nwe_ihe,첫째값[현재클래스])||ọbọakwụkwọ_ndebà==필드개수){잘못됨=1;break;}내보내기(àrụmọrụ_valuu==178?"P(fields[%u]);":"fields[%u]=Q();",ọbọakwụkwọ_ndebà);}}
        else if(àrụmọrụ_valuu==182||àrụmọrụ_valuu==184)호출(절반값(),àrụmọrụ_valuu==182);
        else if(àrụmọrụ_valuu==188){unsigned pinye_otu=baịtị_datà();if(pinye_otu!=4&&pinye_otu!=5&&pinye_otu!=8&&pinye_otu!=9&&pinye_otu!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(àrụmọrụ_valuu==190)내보내기("P(jlength(Q()));");
        else if(àrụmọrụ_valuu==198||àrụmọrụ_valuu==199){int ebenlereanya=(int)명령위치+(int16_t)절반값();if(ebenlereanya<0||ebenlereanya>=(int)otu_ụha->Ụhara)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",àrụmọrụ_valuu==198?"==":"!=",ebenlereanya);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,àrụmọrụ_valuu,명령위치);
        내보내기("\n");
    }
    ogologo_valuu=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned ùsòròokwū_ihe_ọmụmụ(unsigned *자료위치,unsigned mèdebe_Nnokwata){
    if(*자료위치>=mèdebe_Nnokwata){잘못됨=1;return 0;}unsigned koòdù_nkeakàrà=datà[(*자료위치)++];
    if(koòdù_nkeakàrà<128)return koòdù_nkeakàrà;
    unsigned 개수=koòdù_nkeakàrà>=0xc0&&koòdù_nkeakàrà<=0xdf?1:koòdù_nkeakàrà>=0xe0&&koòdù_nkeakàrà<=0xef?2:3;
    if(개수==3||개수>mèdebe_Nnokwata-*자료위치){잘못됨=1;return 0;}unsigned valuu=koòdù_nkeakàrà&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=datà[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;valuu=valuu<<6|(다음&63);}
    if((개수==1&&valuu<128&&valuu!=0)||(개수==2&&valuu<2048))잘못됨=1;return valuu;
}
static void ùsòròokwū_ihendịgide(unsigned ihe_nkọwapụta_valuu){
    unsigned 부호없는값=첫째값[ihe_nkọwapụta_valuu];if(부호없는값<1||부호없는값>=상수모음||nhụbaama_ndepụta[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",ihe_nkọwapụta_valuu);
    unsigned 자료위치=첫째값[부호없는값],mèdebe_Nnokwata=자료위치+둘째값[부호없는값];
    while(자료위치<mèdebe_Nnokwata&&!잘못됨){unsigned koòdù_nkeakàrà=ùsòròokwū_ihe_ọmụmụ(&자료위치,mèdebe_Nnokwata);
        if(koòdù_nkeakàrà>=0xd800&&koòdù_nkeakàrà<=0xdbff){unsigned 낮은부분=ùsòròokwū_ihe_ọmụmụ(&자료위치,mèdebe_Nnokwata);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}koòdù_nkeakàrà=0x10000+((koòdù_nkeakàrà-0xd800)<<10)+낮은부분-0xdc00;}
        else if(koòdù_nkeakàrà>=0xdc00&&koòdù_nkeakàrà<=0xdfff){잘못됨=1;break;}
        if(!koòdù_nkeakàrà){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(koòdù_nkeakàrà<128)내보내기("%u,",koòdù_nkeakàrà);
        else{unsigned 개수=koòdù_nkeakàrà<2048?2:koòdù_nkeakàrà<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(koòdù_nkeakàrà>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((koòdù_nkeakàrà>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Aha){
    size_t 개수=strlen(Aha);
    if(개수>4&&!strcmp(Aha+개수-4,".jar")){
        if(꾸러미열기(Aha)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char ụzọ_ozi[256];const char*ndebà_usoro=꾸러미진입클래스();개수=strlen(ndebà_usoro);if(개수+6>=sizeof(ụzọ_ozi))return 0;
        for(unsigned 순번=0;순번<개수;순번++)ụzọ_ozi[순번]=ndebà_usoro[순번]=='.'?'/':ndebà_usoro[순번];strcpy(ụzọ_ozi+개수,".class");int 항목수=꾸러미읽기(ụzọ_ozi,datà,sizeof(datà));if(항목수<0)return 0;ogologo_valuu=항목수;
    }else{intptr_t ọbọakwụkwọ_ebenjìaka=사용자호출(3,(uintptr_t)Aha,0,0,0,0,0);if(ọbọakwụkwọ_ebenjìaka<0)return 0;intptr_t 항목수=사용자호출(9,ọbọakwụkwọ_ebenjìaka,0,0,0,0,0);if(항목수<0||항목수>sizeof(datà)){사용자호출(4,ọbọakwụkwọ_ebenjìaka,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,ọbọakwụkwọ_ebenjìaka,(uintptr_t)datà,항목수,0,0,0);사용자호출(4,ọbọakwụkwọ_ebenjìaka,0,0,0,0,0);if(받은수!=항목수)return 0;ogologo_valuu=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(nhụbaama_ndepụta[순번]==8)ùsòròokwū_ihendịgide(순번);
    if(잘못됨)return 0;
    int ndebà_akara=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Yunīkoòdù_valuu(메소드목록[순번].Aha,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Yunīkoòdù_valuu(메소드목록[순번].Aha,"main")&&Yunīkoòdù_valuu(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)ndebà_akara=순번;
        if(Yunīkoòdù_valuu(메소드목록[순번].Aha,"<clinit>"))초기값=순번;
    }
    if(ndebà_akara<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)wue_usoro(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(fild_ihendịgide[순번]){
        unsigned koòdù_nkeakàrà=fild_ihendịgide[순번];if(koòdù_nkeakàrà>=상수모음)return 0;
        if(nhụbaama_ndepụta[koòdù_nkeakàrà]==3)내보내기("fields[%u]=%uU;",순번,첫째값[koòdù_nkeakàrà]);else if(nhụbaama_ndepụta[koòdù_nkeakàrà]==8)내보내기("fields[%u]=(W)k%u;",순번,koòdù_nkeakàrà);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",ndebà_akara);
    return 잘못됨?0:SMS;
}
