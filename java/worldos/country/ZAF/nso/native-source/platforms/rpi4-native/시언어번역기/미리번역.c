#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "sehlopha.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned botelele_boleng,현재위치;static int 잘못됨;
static unsigned magoro_Lenaneo[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char Sengwalwa[65536];static unsigned bogolo_bja_sengwalwa;
typedef struct {unsigned 설정비트,Leina,서술값,taelo_TATELANO,Bogolo,지역변수들,kgoboko_Bobolokelo;} mokgwa_go_tsenya_tshedimošo;
static mokgwa_go_tsenya_tshedimošo 메소드목록[64];static unsigned 메소드개수;
static unsigned leina_la_sekgobangwalo[64],필드서술[64],lefelwana_ya_go_se_fetoge[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>botelele_boleng||개수>botelele_boleng-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned paete_data(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:data[자료위치];}
static unsigned 절반값(void){unsigned kamano_ya_x=paete_data();return kamano_ya_x<<8|paete_data();}
static uint32_t 가득참(void){uint32_t kamano_ya_x=절반값();return kamano_ya_x<<16|절반값();}
static int Yunikhoute_boleng(unsigned 순번,const char*molokoloko_data){return 순번>0&&순번<상수모음&&magoro_Lenaneo[순번]==1&&strlen(molokoloko_data)==둘째값[순번]&&!memcmp(data+첫째값[순번],molokoloko_data,둘째값[순번]);}
static int 같음(unsigned kamano_ya_x,unsigned 세로좌표){return kamano_ya_x>0&&kamano_ya_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&magoro_Lenaneo[kamano_ya_x]==1&&magoro_Lenaneo[세로좌표]==1&&둘째값[kamano_ya_x]==둘째값[세로좌표]&&!memcmp(data+첫째값[kamano_ya_x],data+첫째값[세로좌표],둘째값[kamano_ya_x]);}
static void 내보내기(const char*faele_go_tsenya_tshedimošo,...){if(잘못됨)return;va_list akumente_arei;va_start(akumente_arei,faele_go_tsenya_tshedimošo);int 개수=vsnprintf(Sengwalwa+bogolo_bja_sengwalwa,sizeof(Sengwalwa)-bogolo_bja_sengwalwa,faele_go_tsenya_tshedimošo,akumente_arei);va_end(akumente_arei);if(개수<0||(unsigned)개수>=sizeof(Sengwalwa)-bogolo_bja_sengwalwa){잘못됨=1;return;}bogolo_bja_sengwalwa+=개수;}
static int 서술자(unsigned sešupi_boleng,int*결과){
    if(sešupi_boleng<1||sešupi_boleng>=상수모음||magoro_Lenaneo[sešupi_boleng]!=1)return -1;unsigned 자료위치=첫째값[sešupi_boleng],fetša_E_Šetšego=자료위치+둘째값[sešupi_boleng];if(자료위치>=fetša_E_Šetšego||data[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<fetša_E_Šetšego&&data[자료위치]!=')'){
        unsigned khouto_ya_tlhaka=data[자료위치++];while(khouto_ya_tlhaka=='['&&자료위치<fetša_E_Šetšego)khouto_ya_tlhaka=data[자료위치++];
        if(khouto_ya_tlhaka=='L'){while(자료위치<fetša_E_Šetšego&&data[자료위치]!=';')자료위치++;if(자료위치==fetša_E_Šetšego)return -1;자료위치++;}
        else if(khouto_ya_tlhaka!='I'&&khouto_ya_tlhaka!='Z'&&khouto_ya_tlhaka!='B'&&khouto_ya_tlhaka!='C'&&khouto_ya_tlhaka!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=fetša_E_Šetšego||data[자료위치++]!=')')return -1;*결과=data[자료위치]=='V'?0:1;
    if(data[자료위치]=='J'||data[자료위치]=='D'||data[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned Bogolo=가득참();가져오기(Bogolo);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned ngwana_bešene=절반값(),판번호=절반값();if(ngwana_bešene||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        magoro_Lenaneo[순번]=paete_data();switch(magoro_Lenaneo[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=paete_data();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||magoro_Lenaneo[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||magoro_Lenaneo[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();leina_la_sekgobangwalo[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Leina=절반값(),Bogolo=가득참();
            if(Yunikhoute_boleng(Leina,"ConstantValue")){if(Bogolo!=2)return -1;lefelwana_ya_go_se_fetoge[순번]=절반값();}
            else 가져오기(Bogolo);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        mokgwa_go_tsenya_tshedimošo*sehlopha_bogolo=메소드목록+순번;sehlopha_bogolo->설정비트=절반값();sehlopha_bogolo->Leina=절반값();sehlopha_bogolo->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Leina=절반값(),Bogolo=가득참(),Diriša=현재위치;
            if(Bogolo>botelele_boleng-현재위치)return -1;
            if(Yunikhoute_boleng(Leina,"Code")){
                sehlopha_bogolo->kgoboko_Bobolokelo=절반값();sehlopha_bogolo->지역변수들=절반값();sehlopha_bogolo->Bogolo=가득참();sehlopha_bogolo->taelo_TATELANO=가져오기(sehlopha_bogolo->Bogolo);
                if(sehlopha_bogolo->kgoboko_Bobolokelo>128||sehlopha_bogolo->지역변수들>128||sehlopha_bogolo->Bogolo>8192||절반값())return -1;속성들();
            }else 가져오기(Bogolo);
            if(현재위치!=Diriša+Bogolo)return -1;
        }
        if(!Yunikhoute_boleng(sehlopha_bogolo->Leina,"<init>")&&(!(sehlopha_bogolo->설정비트&8)||(sehlopha_bogolo->설정비트&(0x100|0x20))||!sehlopha_bogolo->Bogolo))return -1;
    }
    속성들();return 잘못됨||현재위치!=botelele_boleng?-1:0;
}
static void ya_go_se_fetoge_boleng(unsigned sešupi_boleng){
    if(!sešupi_boleng||sešupi_boleng>=상수모음){잘못됨=1;return;}
    if(magoro_Lenaneo[sešupi_boleng]==3)내보내기("P(%uU);",첫째값[sešupi_boleng]);
    else if(magoro_Lenaneo[sešupi_boleng]==8)내보내기("P((W)k%u);",sešupi_boleng);else 잘못됨=1;
}
static void 호출(unsigned sešupi_boleng,int sethalwa_founa){
    if(sešupi_boleng<1||sešupi_boleng>=상수모음||(magoro_Lenaneo[sešupi_boleng]!=10&&magoro_Lenaneo[sešupi_boleng]!=11)||첫째값[sešupi_boleng]<1||첫째값[sešupi_boleng]>=상수모음||magoro_Lenaneo[첫째값[sešupi_boleng]]!=7||둘째값[sešupi_boleng]<1||둘째값[sešupi_boleng]>=상수모음||magoro_Lenaneo[둘째값[sešupi_boleng]]!=12){잘못됨=1;return;}
    unsigned mong_selo=첫째값[첫째값[sešupi_boleng]],Leina=첫째값[둘째값[sešupi_boleng]],서술값=둘째값[둘째값[sešupi_boleng]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(sethalwa_founa)내보내기("Q();");
    if(!sethalwa_founa&&같음(mong_selo,첫째값[현재클래스])){
        unsigned sehlopha_bogolo=0;for(;sehlopha_bogolo<메소드개수;sehlopha_bogolo++)if(같음(Leina,메소드목록[sehlopha_bogolo].Leina)&&같음(서술값,메소드목록[sehlopha_bogolo].서술값))break;
        if(sehlopha_bogolo==메소드개수||!(메소드목록[sehlopha_bogolo].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",sehlopha_bogolo);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((sethalwa_founa&&Yunikhoute_boleng(mong_selo,"java/io/PrintStream")&& (Yunikhoute_boleng(Leina,"print")||Yunikhoute_boleng(Leina,"println")))||(!sethalwa_founa&&Yunikhoute_boleng(mong_selo,"한국어/자체/출력"))){
        if(Yunikhoute_boleng(서술값,"(I)V")&&(Yunikhoute_boleng(Leina,"print")||Yunikhoute_boleng(Leina,"println")||Yunikhoute_boleng(Leina,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Yunikhoute_boleng(Leina,"print")?0:1);return;}
        if(Yunikhoute_boleng(서술값,"(Ljava/lang/String;)V")&&(Yunikhoute_boleng(Leina,"print")||Yunikhoute_boleng(Leina,"println")||Yunikhoute_boleng(Leina,"Ngwala")||Yunikhoute_boleng(Leina,"ngwala_mothaladi"))){내보내기("jprint(x[0],0,%d);",Yunikhoute_boleng(Leina,"print")||Yunikhoute_boleng(Leina,"Ngwala")?0:1);return;}
        if(Yunikhoute_boleng(서술값,"()V")&&Yunikhoute_boleng(Leina,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!sethalwa_founa&&Yunikhoute_boleng(mong_selo,"한국어/자체/Faele")){
        if(Yunikhoute_boleng(Leina,"Ngwala")&&Yunikhoute_boleng(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Yunikhoute_boleng(Leina,"Bala")&&Yunikhoute_boleng(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void aga_mokgwa(unsigned 색인){
    mokgwa_go_tsenya_tshedimošo*sehlopha_bogolo=메소드목록+색인;if(Yunikhoute_boleng(sehlopha_bogolo->Leina,"<init>"))return;int 결과,개수=서술자(sehlopha_bogolo->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>sehlopha_bogolo->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",sehlopha_bogolo->지역변수들?sehlopha_bogolo->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=botelele_boleng;botelele_boleng=sehlopha_bogolo->taelo_TATELANO+sehlopha_bogolo->Bogolo;현재위치=sehlopha_bogolo->taelo_TATELANO;
    while(현재위치<botelele_boleng&&!잘못됨){unsigned 명령위치=현재위치-sehlopha_bogolo->taelo_TATELANO,tiro_boleng=paete_data();내보내기("L%u:;",명령위치);
        if(tiro_boleng==0){}
        else if(tiro_boleng==1)내보내기("P(0);");
        else if(tiro_boleng>=2&&tiro_boleng<=8)내보내기("P(%uU);",tiro_boleng-3);
        else if(tiro_boleng==16){int boleng=(int8_t)paete_data();내보내기("P(%uU);",(unsigned)boleng);}
        else if(tiro_boleng==17){int boleng=(int16_t)절반값();내보내기("P(%uU);",(unsigned)boleng);}
        else if(tiro_boleng==18||tiro_boleng==19)ya_go_se_fetoge_boleng(tiro_boleng==18?paete_data():절반값());
        else if(tiro_boleng==21||tiro_boleng==25){unsigned 순번=paete_data();if(순번>=sehlopha_bogolo->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((tiro_boleng>=26&&tiro_boleng<=29)||(tiro_boleng>=42&&tiro_boleng<=45)){unsigned 순번=tiro_boleng>=42?tiro_boleng-42:tiro_boleng-26;if(순번>=sehlopha_bogolo->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(tiro_boleng==54||tiro_boleng==58){unsigned 순번=paete_data();if(순번>=sehlopha_bogolo->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((tiro_boleng>=59&&tiro_boleng<=62)||(tiro_boleng>=75&&tiro_boleng<=78)){unsigned 순번=tiro_boleng>=75?tiro_boleng-75:tiro_boleng-59;if(순번>=sehlopha_bogolo->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(tiro_boleng==46||tiro_boleng==50||tiro_boleng==51||tiro_boleng==52||tiro_boleng==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(tiro_boleng==79||tiro_boleng==83||tiro_boleng==84||tiro_boleng==85||tiro_boleng==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",tiro_boleng==84?"(unsigned)(signed char)q":tiro_boleng==85?"(unsigned short)q":tiro_boleng==86?"(unsigned)(short)q":"q");
        else if(tiro_boleng==87)내보내기("Q();");
        else if(tiro_boleng==89)내보내기("q=Q();P(q);P(q);");
        else if(tiro_boleng==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(tiro_boleng==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(tiro_boleng==96||tiro_boleng==100||tiro_boleng==104||tiro_boleng==120||tiro_boleng==124||tiro_boleng==126||tiro_boleng==128||tiro_boleng==130){const char*go_enkhouta_boleng=tiro_boleng==96?"+":tiro_boleng==100?"-":tiro_boleng==104?"*":tiro_boleng==120?"<<":tiro_boleng==124?">>":tiro_boleng==126?"&":tiro_boleng==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",go_enkhouta_boleng,tiro_boleng==120||tiro_boleng==124?"%32":"");}
        else if(tiro_boleng==108||tiro_boleng==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",tiro_boleng==112);
        else if(tiro_boleng==116)내보내기("P(0U-(unsigned)Q());");
        else if(tiro_boleng==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(tiro_boleng==132){unsigned 순번=paete_data();int 차이=(int8_t)paete_data();if(순번>=sehlopha_bogolo->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(tiro_boleng>=145&&tiro_boleng<=147)내보내기("P((unsigned)(%s)Q());",tiro_boleng==145?"signed char":tiro_boleng==146?"unsigned short":"short");
        else if(tiro_boleng>=153&&tiro_boleng<=166){int nepo=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(nepo<0||nepo>=(int)sehlopha_bogolo->Bogolo){잘못됨=1;break;}if(tiro_boleng<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[tiro_boleng-153],nepo);else if(tiro_boleng<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[tiro_boleng-159],nepo);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",tiro_boleng==165?"==":"!=",nepo);}
        else if(tiro_boleng==167){int nepo=(int)명령위치+(int16_t)절반값();if(nepo<0||nepo>=(int)sehlopha_bogolo->Bogolo)잘못됨=1;내보내기("goto L%d;",nepo);}
        else if(tiro_boleng==172||tiro_boleng==176)내보내기("return Q();");else if(tiro_boleng==177)내보내기("return 0;");
        else if(tiro_boleng==178||tiro_boleng==179){unsigned sešupi_boleng=절반값();if(sešupi_boleng<1||sešupi_boleng>=상수모음||magoro_Lenaneo[sešupi_boleng]!=9||첫째값[sešupi_boleng]>=상수모음||둘째값[sešupi_boleng]>=상수모음||magoro_Lenaneo[첫째값[sešupi_boleng]]!=7||magoro_Lenaneo[둘째값[sešupi_boleng]]!=12){잘못됨=1;break;}unsigned mong_selo=첫째값[첫째값[sešupi_boleng]],Leina=첫째값[둘째값[sešupi_boleng]],서술값=둘째값[둘째값[sešupi_boleng]];
            if(tiro_boleng==178&&Yunikhoute_boleng(mong_selo,"java/lang/System")&&Yunikhoute_boleng(Leina,"out")&&Yunikhoute_boleng(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned faele_go_tsenya_tshedimošo=0;while(faele_go_tsenya_tshedimošo<필드개수&&(!같음(Leina,leina_la_sekgobangwalo[faele_go_tsenya_tshedimošo])||!같음(서술값,필드서술[faele_go_tsenya_tshedimošo])))faele_go_tsenya_tshedimošo++;if(!같음(mong_selo,첫째값[현재클래스])||faele_go_tsenya_tshedimošo==필드개수){잘못됨=1;break;}내보내기(tiro_boleng==178?"P(fields[%u]);":"fields[%u]=Q();",faele_go_tsenya_tshedimošo);}}
        else if(tiro_boleng==182||tiro_boleng==184)호출(절반값(),tiro_boleng==182);
        else if(tiro_boleng==188){unsigned thaepa_legoro=paete_data();if(thaepa_legoro!=4&&thaepa_legoro!=5&&thaepa_legoro!=8&&thaepa_legoro!=9&&thaepa_legoro!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(tiro_boleng==190)내보내기("P(jlength(Q()));");
        else if(tiro_boleng==198||tiro_boleng==199){int nepo=(int)명령위치+(int16_t)절반값();if(nepo<0||nepo>=(int)sehlopha_bogolo->Bogolo)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",tiro_boleng==198?"==":"!=",nepo);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,tiro_boleng,명령위치);
        내보내기("\n");
    }
    botelele_boleng=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned molokoloko_thutišo(unsigned *자료위치,unsigned fetša_E_Šetšego){
    if(*자료위치>=fetša_E_Šetšego){잘못됨=1;return 0;}unsigned khouto_ya_tlhaka=data[(*자료위치)++];
    if(khouto_ya_tlhaka<128)return khouto_ya_tlhaka;
    unsigned 개수=khouto_ya_tlhaka>=0xc0&&khouto_ya_tlhaka<=0xdf?1:khouto_ya_tlhaka>=0xe0&&khouto_ya_tlhaka<=0xef?2:3;
    if(개수==3||개수>fetša_E_Šetšego-*자료위치){잘못됨=1;return 0;}unsigned boleng=khouto_ya_tlhaka&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=data[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;boleng=boleng<<6|(다음&63);}
    if((개수==1&&boleng<128&&boleng!=0)||(개수==2&&boleng<2048))잘못됨=1;return boleng;
}
static void molokoloko_ya_go_se_fetoge(unsigned sešupi_boleng){
    unsigned 부호없는값=첫째값[sešupi_boleng];if(부호없는값<1||부호없는값>=상수모음||magoro_Lenaneo[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",sešupi_boleng);
    unsigned 자료위치=첫째값[부호없는값],fetša_E_Šetšego=자료위치+둘째값[부호없는값];
    while(자료위치<fetša_E_Šetšego&&!잘못됨){unsigned khouto_ya_tlhaka=molokoloko_thutišo(&자료위치,fetša_E_Šetšego);
        if(khouto_ya_tlhaka>=0xd800&&khouto_ya_tlhaka<=0xdbff){unsigned 낮은부분=molokoloko_thutišo(&자료위치,fetša_E_Šetšego);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}khouto_ya_tlhaka=0x10000+((khouto_ya_tlhaka-0xd800)<<10)+낮은부분-0xdc00;}
        else if(khouto_ya_tlhaka>=0xdc00&&khouto_ya_tlhaka<=0xdfff){잘못됨=1;break;}
        if(!khouto_ya_tlhaka){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(khouto_ya_tlhaka<128)내보내기("%u,",khouto_ya_tlhaka);
        else{unsigned 개수=khouto_ya_tlhaka<2048?2:khouto_ya_tlhaka<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(khouto_ya_tlhaka>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((khouto_ya_tlhaka>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Leina){
    size_t 개수=strlen(Leina);
    if(개수>4&&!strcmp(Leina+개수-4,".jar")){
        if(꾸러미열기(Leina)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Tsejana[256];const char*go_tsenya_tshedimošo_mokgwa=꾸러미진입클래스();개수=strlen(go_tsenya_tshedimošo_mokgwa);if(개수+6>=sizeof(Tsejana))return 0;
        for(unsigned 순번=0;순번<개수;순번++)Tsejana[순번]=go_tsenya_tshedimošo_mokgwa[순번]=='.'?'/':go_tsenya_tshedimošo_mokgwa[순번];strcpy(Tsejana+개수,".class");int 항목수=꾸러미읽기(Tsejana,data,sizeof(data));if(항목수<0)return 0;botelele_boleng=항목수;
    }else{intptr_t faele_tshwaro=사용자호출(3,(uintptr_t)Leina,0,0,0,0,0);if(faele_tshwaro<0)return 0;intptr_t 항목수=사용자호출(9,faele_tshwaro,0,0,0,0,0);if(항목수<0||항목수>sizeof(data)){사용자호출(4,faele_tshwaro,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,faele_tshwaro,(uintptr_t)data,항목수,0,0,0);사용자호출(4,faele_tshwaro,0,0,0,0,0);if(받은수!=항목수)return 0;botelele_boleng=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(magoro_Lenaneo[순번]==8)molokoloko_ya_go_se_fetoge(순번);
    if(잘못됨)return 0;
    int go_tsenya_tshedimošo_ntlha=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Yunikhoute_boleng(메소드목록[순번].Leina,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Yunikhoute_boleng(메소드목록[순번].Leina,"main")&&Yunikhoute_boleng(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)go_tsenya_tshedimošo_ntlha=순번;
        if(Yunikhoute_boleng(메소드목록[순번].Leina,"<clinit>"))초기값=순번;
    }
    if(go_tsenya_tshedimošo_ntlha<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)aga_mokgwa(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(lefelwana_ya_go_se_fetoge[순번]){
        unsigned khouto_ya_tlhaka=lefelwana_ya_go_se_fetoge[순번];if(khouto_ya_tlhaka>=상수모음)return 0;
        if(magoro_Lenaneo[khouto_ya_tlhaka]==3)내보내기("fields[%u]=%uU;",순번,첫째값[khouto_ya_tlhaka]);else if(magoro_Lenaneo[khouto_ya_tlhaka]==8)내보내기("fields[%u]=(W)k%u;",순번,khouto_ya_tlhaka);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",go_tsenya_tshedimošo_ntlha);
    return 잘못됨?0:Sengwalwa;
}
