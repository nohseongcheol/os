#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "fungasha.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned urefu_thamani,현재위치;static int teknolojia_ya_maelezo_batili;
static unsigned Lebo_Orodha[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char SMS[65536];static unsigned ukubwa_matini;
typedef struct {unsigned usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma,Jina,서술값,agizo_MFUATANO,panga_ukubwa,지역변수들,Mpororo_Hifadhi;} mbinu_ingizo;
static mbinu_ingizo 메소드목록[64];static unsigned 메소드개수;
static unsigned jina_la_uga[64],필드서술[64],uga_kisobadilika[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>urefu_thamani||개수>urefu_thamani-현재위치){teknolojia_ya_maelezo_batili=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned baiti_data(void){unsigned 자료위치=가져오기(1);return teknolojia_ya_maelezo_batili?0:data[자료위치];}
static unsigned 절반값(void){unsigned jira_x=baiti_data();return jira_x<<8|baiti_data();}
static uint32_t 가득참(void){uint32_t jira_x=절반값();return jira_x<<16|절반값();}
static int Msimbosare_thamani(unsigned 순번,const char*tungo_data){return 순번>0&&순번<상수모음&&Lebo_Orodha[순번]==1&&strlen(tungo_data)==둘째값[순번]&&!memcmp(data+첫째값[순번],tungo_data,둘째값[순번]);}
static int 같음(unsigned jira_x,unsigned Kitufe_cha_Y_kiratibu){return jira_x>0&&jira_x<상수모음&&Kitufe_cha_Y_kiratibu>0&&Kitufe_cha_Y_kiratibu<상수모음&&Lebo_Orodha[jira_x]==1&&Lebo_Orodha[Kitufe_cha_Y_kiratibu]==1&&둘째값[jira_x]==둘째값[Kitufe_cha_Y_kiratibu]&&!memcmp(data+첫째값[jira_x],data+첫째값[Kitufe_cha_Y_kiratibu],둘째값[jira_x]);}
static void 내보내기(const char*faili_ingizo,...){if(teknolojia_ya_maelezo_batili)return;va_list hoja_ARRAY;va_start(hoja_ARRAY,faili_ingizo);int 개수=vsnprintf(SMS+ukubwa_matini,sizeof(SMS)-ukubwa_matini,faili_ingizo,hoja_ARRAY);va_end(hoja_ARRAY);if(개수<0||(unsigned)개수>=sizeof(SMS)-ukubwa_matini){teknolojia_ya_maelezo_batili=1;return;}ukubwa_matini+=개수;}
static int 서술자(unsigned kitambulishi_thamani,int*결과){
    if(kitambulishi_thamani<1||kitambulishi_thamani>=상수모음||Lebo_Orodha[kitambulishi_thamani]!=1)return -1;unsigned 자료위치=첫째값[kitambulishi_thamani],tamatia_Chipua=자료위치+둘째값[kitambulishi_thamani];if(자료위치>=tamatia_Chipua||data[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<tamatia_Chipua&&data[자료위치]!=')'){
        unsigned msimbo_wa_kibambo=data[자료위치++];while(msimbo_wa_kibambo=='['&&자료위치<tamatia_Chipua)msimbo_wa_kibambo=data[자료위치++];
        if(msimbo_wa_kibambo=='L'){while(자료위치<tamatia_Chipua&&data[자료위치]!=';')자료위치++;if(자료위치==tamatia_Chipua)return -1;자료위치++;}
        else if(msimbo_wa_kibambo!='I'&&msimbo_wa_kibambo!='Z'&&msimbo_wa_kibambo!='B'&&msimbo_wa_kibambo!='C'&&msimbo_wa_kibambo!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=tamatia_Chipua||data[자료위치++]!=')')return -1;*결과=data[자료위치]=='V'?0:1;
    if(data[자료위치]=='J'||data[자료위치]=='D'||data[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!teknolojia_ya_maelezo_batili;순번++){절반값();unsigned panga_ukubwa=가득참();가져오기(panga_ukubwa);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned mtoto_toleo=절반값(),판번호=절반값();if(mtoto_toleo||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!teknolojia_ya_maelezo_batili;순번++){
        Lebo_Orodha[순번]=baiti_data();switch(Lebo_Orodha[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=baiti_data();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Lebo_Orodha[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Lebo_Orodha[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!teknolojia_ya_maelezo_batili;순번++){
        unsigned usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma=절반값();jina_la_uga[순번]=절반값();필드서술[순번]=절반값();
        if(!(usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!teknolojia_ya_maelezo_batili;안쪽순번++){
            unsigned Jina=절반값(),panga_ukubwa=가득참();
            if(Msimbosare_thamani(Jina,"ConstantValue")){if(panga_ukubwa!=2)return -1;uga_kisobadilika[순번]=절반값();}
            else 가져오기(panga_ukubwa);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!teknolojia_ya_maelezo_batili;순번++){
        mbinu_ingizo*Kikundi_panga_ukubwa=메소드목록+순번;Kikundi_panga_ukubwa->usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma=절반값();Kikundi_panga_ukubwa->Jina=절반값();Kikundi_panga_ukubwa->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!teknolojia_ya_maelezo_batili;안쪽순번++){
            unsigned Jina=절반값(),panga_ukubwa=가득참(),endesha=현재위치;
            if(panga_ukubwa>urefu_thamani-현재위치)return -1;
            if(Msimbosare_thamani(Jina,"Code")){
                Kikundi_panga_ukubwa->Mpororo_Hifadhi=절반값();Kikundi_panga_ukubwa->지역변수들=절반값();Kikundi_panga_ukubwa->panga_ukubwa=가득참();Kikundi_panga_ukubwa->agizo_MFUATANO=가져오기(Kikundi_panga_ukubwa->panga_ukubwa);
                if(Kikundi_panga_ukubwa->Mpororo_Hifadhi>128||Kikundi_panga_ukubwa->지역변수들>128||Kikundi_panga_ukubwa->panga_ukubwa>8192||절반값())return -1;속성들();
            }else 가져오기(panga_ukubwa);
            if(현재위치!=endesha+panga_ukubwa)return -1;
        }
        if(!Msimbosare_thamani(Kikundi_panga_ukubwa->Jina,"<init>")&&(!(Kikundi_panga_ukubwa->usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&8)||(Kikundi_panga_ukubwa->usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&(0x100|0x20))||!Kikundi_panga_ukubwa->panga_ukubwa))return -1;
    }
    속성들();return teknolojia_ya_maelezo_batili||현재위치!=urefu_thamani?-1:0;
}
static void kisobadilika_thamani(unsigned kitambulishi_thamani){
    if(!kitambulishi_thamani||kitambulishi_thamani>=상수모음){teknolojia_ya_maelezo_batili=1;return;}
    if(Lebo_Orodha[kitambulishi_thamani]==3)내보내기("P(%uU);",첫째값[kitambulishi_thamani]);
    else if(Lebo_Orodha[kitambulishi_thamani]==8)내보내기("P((W)k%u);",kitambulishi_thamani);else teknolojia_ya_maelezo_batili=1;
}
static void 호출(unsigned kitambulishi_thamani,int pepe_ita){
    if(kitambulishi_thamani<1||kitambulishi_thamani>=상수모음||(Lebo_Orodha[kitambulishi_thamani]!=10&&Lebo_Orodha[kitambulishi_thamani]!=11)||첫째값[kitambulishi_thamani]<1||첫째값[kitambulishi_thamani]>=상수모음||Lebo_Orodha[첫째값[kitambulishi_thamani]]!=7||둘째값[kitambulishi_thamani]<1||둘째값[kitambulishi_thamani]>=상수모음||Lebo_Orodha[둘째값[kitambulishi_thamani]]!=12){teknolojia_ya_maelezo_batili=1;return;}
    unsigned mmiliki_kipengee=첫째값[첫째값[kitambulishi_thamani]],Jina=첫째값[둘째값[kitambulishi_thamani]],서술값=둘째값[둘째값[kitambulishi_thamani]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){teknolojia_ya_maelezo_batili=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(pepe_ita)내보내기("Q();");
    if(!pepe_ita&&같음(mmiliki_kipengee,첫째값[현재클래스])){
        unsigned Kikundi_panga_ukubwa=0;for(;Kikundi_panga_ukubwa<메소드개수;Kikundi_panga_ukubwa++)if(같음(Jina,메소드목록[Kikundi_panga_ukubwa].Jina)&&같음(서술값,메소드목록[Kikundi_panga_ukubwa].서술값))break;
        if(Kikundi_panga_ukubwa==메소드개수||!(메소드목록[Kikundi_panga_ukubwa].usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&8)){teknolojia_ya_maelezo_batili=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",Kikundi_panga_ukubwa);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((pepe_ita&&Msimbosare_thamani(mmiliki_kipengee,"java/io/PrintStream")&& (Msimbosare_thamani(Jina,"print")||Msimbosare_thamani(Jina,"println")))||(!pepe_ita&&Msimbosare_thamani(mmiliki_kipengee,"한국어/자체/출력"))){
        if(Msimbosare_thamani(서술값,"(I)V")&&(Msimbosare_thamani(Jina,"print")||Msimbosare_thamani(Jina,"println")||Msimbosare_thamani(Jina,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Msimbosare_thamani(Jina,"print")?0:1);return;}
        if(Msimbosare_thamani(서술값,"(Ljava/lang/String;)V")&&(Msimbosare_thamani(Jina,"print")||Msimbosare_thamani(Jina,"println")||Msimbosare_thamani(Jina,"andika")||Msimbosare_thamani(Jina,"andika_laini"))){내보내기("jprint(x[0],0,%d);",Msimbosare_thamani(Jina,"print")||Msimbosare_thamani(Jina,"andika")?0:1);return;}
        if(Msimbosare_thamani(서술값,"()V")&&Msimbosare_thamani(Jina,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!pepe_ita&&Msimbosare_thamani(mmiliki_kipengee,"한국어/자체/faili")){
        if(Msimbosare_thamani(Jina,"andika")&&Msimbosare_thamani(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Msimbosare_thamani(Jina,"읽기")&&Msimbosare_thamani(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    teknolojia_ya_maelezo_batili=1;
}
static void jenga_mbinu(unsigned 색인){
    mbinu_ingizo*Kikundi_panga_ukubwa=메소드목록+색인;if(Msimbosare_thamani(Kikundi_panga_ukubwa->Jina,"<init>"))return;int 결과,개수=서술자(Kikundi_panga_ukubwa->서술값,&결과);if(개수<0){teknolojia_ya_maelezo_batili=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>Kikundi_panga_ukubwa->지역변수들){teknolojia_ya_maelezo_batili=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Kikundi_panga_ukubwa->지역변수들?Kikundi_panga_ukubwa->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=urefu_thamani;urefu_thamani=Kikundi_panga_ukubwa->agizo_MFUATANO+Kikundi_panga_ukubwa->panga_ukubwa;현재위치=Kikundi_panga_ukubwa->agizo_MFUATANO;
    while(현재위치<urefu_thamani&&!teknolojia_ya_maelezo_batili){unsigned 명령위치=현재위치-Kikundi_panga_ukubwa->agizo_MFUATANO,upasuaji_thamani=baiti_data();내보내기("L%u:;",명령위치);
        if(upasuaji_thamani==0){}
        else if(upasuaji_thamani==1)내보내기("P(0);");
        else if(upasuaji_thamani>=2&&upasuaji_thamani<=8)내보내기("P(%uU);",upasuaji_thamani-3);
        else if(upasuaji_thamani==16){int thamani=(int8_t)baiti_data();내보내기("P(%uU);",(unsigned)thamani);}
        else if(upasuaji_thamani==17){int thamani=(int16_t)절반값();내보내기("P(%uU);",(unsigned)thamani);}
        else if(upasuaji_thamani==18||upasuaji_thamani==19)kisobadilika_thamani(upasuaji_thamani==18?baiti_data():절반값());
        else if(upasuaji_thamani==21||upasuaji_thamani==25){unsigned 순번=baiti_data();if(순번>=Kikundi_panga_ukubwa->지역변수들)teknolojia_ya_maelezo_batili=1;내보내기("P(v[%u]);",순번);}
        else if((upasuaji_thamani>=26&&upasuaji_thamani<=29)||(upasuaji_thamani>=42&&upasuaji_thamani<=45)){unsigned 순번=upasuaji_thamani>=42?upasuaji_thamani-42:upasuaji_thamani-26;if(순번>=Kikundi_panga_ukubwa->지역변수들)teknolojia_ya_maelezo_batili=1;내보내기("P(v[%u]);",순번);}
        else if(upasuaji_thamani==54||upasuaji_thamani==58){unsigned 순번=baiti_data();if(순번>=Kikundi_panga_ukubwa->지역변수들)teknolojia_ya_maelezo_batili=1;내보내기("v[%u]=Q();",순번);}
        else if((upasuaji_thamani>=59&&upasuaji_thamani<=62)||(upasuaji_thamani>=75&&upasuaji_thamani<=78)){unsigned 순번=upasuaji_thamani>=75?upasuaji_thamani-75:upasuaji_thamani-59;if(순번>=Kikundi_panga_ukubwa->지역변수들)teknolojia_ya_maelezo_batili=1;내보내기("v[%u]=Q();",순번);}
        else if(upasuaji_thamani==46||upasuaji_thamani==50||upasuaji_thamani==51||upasuaji_thamani==52||upasuaji_thamani==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(upasuaji_thamani==79||upasuaji_thamani==83||upasuaji_thamani==84||upasuaji_thamani==85||upasuaji_thamani==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",upasuaji_thamani==84?"(unsigned)(signed char)q":upasuaji_thamani==85?"(unsigned short)q":upasuaji_thamani==86?"(unsigned)(short)q":"q");
        else if(upasuaji_thamani==87)내보내기("Q();");
        else if(upasuaji_thamani==89)내보내기("q=Q();P(q);P(q);");
        else if(upasuaji_thamani==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(upasuaji_thamani==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(upasuaji_thamani==96||upasuaji_thamani==100||upasuaji_thamani==104||upasuaji_thamani==120||upasuaji_thamani==124||upasuaji_thamani==126||upasuaji_thamani==128||upasuaji_thamani==130){const char*usimbaji_thamani=upasuaji_thamani==96?"+":upasuaji_thamani==100?"-":upasuaji_thamani==104?"*":upasuaji_thamani==120?"<<":upasuaji_thamani==124?">>":upasuaji_thamani==126?"&":upasuaji_thamani==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",usimbaji_thamani,upasuaji_thamani==120||upasuaji_thamani==124?"%32":"");}
        else if(upasuaji_thamani==108||upasuaji_thamani==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",upasuaji_thamani==112);
        else if(upasuaji_thamani==116)내보내기("P(0U-(unsigned)Q());");
        else if(upasuaji_thamani==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(upasuaji_thamani==132){unsigned 순번=baiti_data();int 차이=(int8_t)baiti_data();if(순번>=Kikundi_panga_ukubwa->지역변수들)teknolojia_ya_maelezo_batili=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(upasuaji_thamani>=145&&upasuaji_thamani<=147)내보내기("P((unsigned)(%s)Q());",upasuaji_thamani==145?"signed char":upasuaji_thamani==146?"unsigned short":"short");
        else if(upasuaji_thamani>=153&&upasuaji_thamani<=166){int lengo=(int)명령위치+(int16_t)절반값();const char*Kulinganisha_thamani[]={"==","!=","<",">=",">","<="};if(lengo<0||lengo>=(int)Kikundi_panga_ukubwa->panga_ukubwa){teknolojia_ya_maelezo_batili=1;break;}if(upasuaji_thamani<159)내보내기("if((int)Q()%s0)goto L%d;",Kulinganisha_thamani[upasuaji_thamani-153],lengo);else if(upasuaji_thamani<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Kulinganisha_thamani[upasuaji_thamani-159],lengo);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",upasuaji_thamani==165?"==":"!=",lengo);}
        else if(upasuaji_thamani==167){int lengo=(int)명령위치+(int16_t)절반값();if(lengo<0||lengo>=(int)Kikundi_panga_ukubwa->panga_ukubwa)teknolojia_ya_maelezo_batili=1;내보내기("goto L%d;",lengo);}
        else if(upasuaji_thamani==172||upasuaji_thamani==176)내보내기("return Q();");else if(upasuaji_thamani==177)내보내기("return 0;");
        else if(upasuaji_thamani==178||upasuaji_thamani==179){unsigned kitambulishi_thamani=절반값();if(kitambulishi_thamani<1||kitambulishi_thamani>=상수모음||Lebo_Orodha[kitambulishi_thamani]!=9||첫째값[kitambulishi_thamani]>=상수모음||둘째값[kitambulishi_thamani]>=상수모음||Lebo_Orodha[첫째값[kitambulishi_thamani]]!=7||Lebo_Orodha[둘째값[kitambulishi_thamani]]!=12){teknolojia_ya_maelezo_batili=1;break;}unsigned mmiliki_kipengee=첫째값[첫째값[kitambulishi_thamani]],Jina=첫째값[둘째값[kitambulishi_thamani]],서술값=둘째값[둘째값[kitambulishi_thamani]];
            if(upasuaji_thamani==178&&Msimbosare_thamani(mmiliki_kipengee,"java/lang/System")&&Msimbosare_thamani(Jina,"out")&&Msimbosare_thamani(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned faili_ingizo=0;while(faili_ingizo<필드개수&&(!같음(Jina,jina_la_uga[faili_ingizo])||!같음(서술값,필드서술[faili_ingizo])))faili_ingizo++;if(!같음(mmiliki_kipengee,첫째값[현재클래스])||faili_ingizo==필드개수){teknolojia_ya_maelezo_batili=1;break;}내보내기(upasuaji_thamani==178?"P(fields[%u]);":"fields[%u]=Q();",faili_ingizo);}}
        else if(upasuaji_thamani==182||upasuaji_thamani==184)호출(절반값(),upasuaji_thamani==182);
        else if(upasuaji_thamani==188){unsigned aina_kategoria=baiti_data();if(aina_kategoria!=4&&aina_kategoria!=5&&aina_kategoria!=8&&aina_kategoria!=9&&aina_kategoria!=10)teknolojia_ya_maelezo_batili=1;내보내기("P(jarray((int)Q()));");}
        else if(upasuaji_thamani==190)내보내기("P(jlength(Q()));");
        else if(upasuaji_thamani==198||upasuaji_thamani==199){int lengo=(int)명령위치+(int16_t)절반값();if(lengo<0||lengo>=(int)Kikundi_panga_ukubwa->panga_ukubwa)teknolojia_ya_maelezo_batili=1;내보내기("if(Q()%s0)goto L%d;",upasuaji_thamani==198?"==":"!=",lengo);}
        else teknolojia_ya_maelezo_batili=1;
        if(teknolojia_ya_maelezo_batili)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,upasuaji_thamani,명령위치);
        내보내기("\n");
    }
    urefu_thamani=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned tungo_funzo(unsigned *자료위치,unsigned tamatia_Chipua){
    if(*자료위치>=tamatia_Chipua){teknolojia_ya_maelezo_batili=1;return 0;}unsigned msimbo_wa_kibambo=data[(*자료위치)++];
    if(msimbo_wa_kibambo<128)return msimbo_wa_kibambo;
    unsigned 개수=msimbo_wa_kibambo>=0xc0&&msimbo_wa_kibambo<=0xdf?1:msimbo_wa_kibambo>=0xe0&&msimbo_wa_kibambo<=0xef?2:3;
    if(개수==3||개수>tamatia_Chipua-*자료위치){teknolojia_ya_maelezo_batili=1;return 0;}unsigned thamani=msimbo_wa_kibambo&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=data[(*자료위치)++];if((다음&0xc0)!=0x80)teknolojia_ya_maelezo_batili=1;thamani=thamani<<6|(다음&63);}
    if((개수==1&&thamani<128&&thamani!=0)||(개수==2&&thamani<2048))teknolojia_ya_maelezo_batili=1;return thamani;
}
static void tungo_kisobadilika(unsigned kitambulishi_thamani){
    unsigned 부호없는값=첫째값[kitambulishi_thamani];if(부호없는값<1||부호없는값>=상수모음||Lebo_Orodha[부호없는값]!=1){teknolojia_ya_maelezo_batili=1;return;}내보내기("static const unsigned char k%u[]={",kitambulishi_thamani);
    unsigned 자료위치=첫째값[부호없는값],tamatia_Chipua=자료위치+둘째값[부호없는값];
    while(자료위치<tamatia_Chipua&&!teknolojia_ya_maelezo_batili){unsigned msimbo_wa_kibambo=tungo_funzo(&자료위치,tamatia_Chipua);
        if(msimbo_wa_kibambo>=0xd800&&msimbo_wa_kibambo<=0xdbff){unsigned 낮은부분=tungo_funzo(&자료위치,tamatia_Chipua);if(낮은부분<0xdc00||낮은부분>0xdfff){teknolojia_ya_maelezo_batili=1;break;}msimbo_wa_kibambo=0x10000+((msimbo_wa_kibambo-0xd800)<<10)+낮은부분-0xdc00;}
        else if(msimbo_wa_kibambo>=0xdc00&&msimbo_wa_kibambo<=0xdfff){teknolojia_ya_maelezo_batili=1;break;}
        if(!msimbo_wa_kibambo){printf("jaot: embedded NUL string needs JVM mode\n");teknolojia_ya_maelezo_batili=1;break;}
        if(msimbo_wa_kibambo<128)내보내기("%u,",msimbo_wa_kibambo);
        else{unsigned 개수=msimbo_wa_kibambo<2048?2:msimbo_wa_kibambo<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(msimbo_wa_kibambo>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((msimbo_wa_kibambo>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Jina){
    size_t 개수=strlen(Jina);
    if(개수>4&&!strcmp(Jina+개수-4,".jar")){
        if(꾸러미열기(Jina)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char njia[256];const char*ingizo_mbinu=꾸러미진입클래스();개수=strlen(ingizo_mbinu);if(개수+6>=sizeof(njia))return 0;
        for(unsigned 순번=0;순번<개수;순번++)njia[순번]=ingizo_mbinu[순번]=='.'?'/':ingizo_mbinu[순번];strcpy(njia+개수,".class");int 항목수=꾸러미읽기(njia,data,sizeof(data));if(항목수<0)return 0;urefu_thamani=항목수;
    }else{intptr_t faili_kishiko=사용자호출(3,(uintptr_t)Jina,0,0,0,0,0);if(faili_kishiko<0)return 0;intptr_t 항목수=사용자호출(9,faili_kishiko,0,0,0,0,0);if(항목수<0||항목수>sizeof(data)){사용자호출(4,faili_kishiko,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,faili_kishiko,(uintptr_t)data,항목수,0,0,0);사용자호출(4,faili_kishiko,0,0,0,0,0);if(받은수!=항목수)return 0;urefu_thamani=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!teknolojia_ya_maelezo_batili;순번++)if(Lebo_Orodha[순번]==8)tungo_kisobadilika(순번);
    if(teknolojia_ya_maelezo_batili)return 0;
    int ingizo_pointi=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Msimbosare_thamani(메소드목록[순번].Jina,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Msimbosare_thamani(메소드목록[순번].Jina,"main")&&Msimbosare_thamani(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma&9)==9)ingizo_pointi=순번;
        if(Msimbosare_thamani(메소드목록[순번].Jina,"<clinit>"))초기값=순번;
    }
    if(ingizo_pointi<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!teknolojia_ya_maelezo_batili;순번++)jenga_mbinu(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(uga_kisobadilika[순번]){
        unsigned msimbo_wa_kibambo=uga_kisobadilika[순번];if(msimbo_wa_kibambo>=상수모음)return 0;
        if(Lebo_Orodha[msimbo_wa_kibambo]==3)내보내기("fields[%u]=%uU;",순번,첫째값[msimbo_wa_kibambo]);else if(Lebo_Orodha[msimbo_wa_kibambo]==8)내보내기("fields[%u]=(W)k%u;",순번,msimbo_wa_kibambo);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",ingizo_pointi);
    return teknolojia_ya_maelezo_batili?0:SMS;
}
