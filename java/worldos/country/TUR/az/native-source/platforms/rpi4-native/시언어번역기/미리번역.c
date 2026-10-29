#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "paket.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char verilənlər[16384];static unsigned uzunluq_VALUE,현재위치;static int 잘못됨;
static unsigned Teqlər_Siyahı[512],첫째값[512],SECOND_VALUE[512],sabit_aylıq_cəmi_dəqiqə,현재클래스;
static char Mətn[65536];static unsigned mətnin_ölçüsü;
typedef struct {unsigned konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti,Ad,서술값,təlimat_SEQUENCE,Böyüklük,지역변수들,Yığın_Yaddaş;} metod_daxiletmə;
static metod_daxiletmə 메소드목록[64];static unsigned 메소드개수;
static unsigned sahənin_adı[64],필드서술[64],sahə_sabit[64],필드개수;
static unsigned TAKE_VALUE(unsigned element_COUNT){if(현재위치>uzunluq_VALUE||element_COUNT>uzunluq_VALUE-현재위치){잘못됨=1;return 0;}unsigned verilənlər_yerinə_qoymaq=현재위치;현재위치+=element_COUNT;return verilənlər_yerinə_qoymaq;}
static unsigned bayt_verilənlər(void){unsigned verilənlər_yerinə_qoymaq=TAKE_VALUE(1);return 잘못됨?0:verilənlər[verilənlər_yerinə_qoymaq];}
static unsigned 절반값(void){unsigned x_koordinatı=bayt_verilənlər();return x_koordinatı<<8|bayt_verilənlər();}
static uint32_t 가득참(void){uint32_t x_koordinatı=절반값();return x_koordinatı<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*sətir_verilənlər){return 순번>0&&순번<sabit_aylıq_cəmi_dəqiqə&&Teqlər_Siyahı[순번]==1&&strlen(sətir_verilənlər)==SECOND_VALUE[순번]&&!memcmp(verilənlər+첫째값[순번],sətir_verilənlər,SECOND_VALUE[순번]);}
static int 같음(unsigned x_koordinatı,unsigned Y_koordinat){return x_koordinatı>0&&x_koordinatı<sabit_aylıq_cəmi_dəqiqə&&Y_koordinat>0&&Y_koordinat<sabit_aylıq_cəmi_dəqiqə&&Teqlər_Siyahı[x_koordinatı]==1&&Teqlər_Siyahı[Y_koordinat]==1&&SECOND_VALUE[x_koordinatı]==SECOND_VALUE[Y_koordinat]&&!memcmp(verilənlər+첫째값[x_koordinatı],verilənlər+첫째값[Y_koordinat],SECOND_VALUE[x_koordinatı]);}
static void 내보내기(const char*fayl_daxiletmə,...){if(잘못됨)return;va_list arqument_ARRAY;va_start(arqument_ARRAY,fayl_daxiletmə);int element_COUNT=vsnprintf(Mətn+mətnin_ölçüsü,sizeof(Mətn)-mətnin_ölçüsü,fayl_daxiletmə,arqument_ARRAY);va_end(arqument_ARRAY);if(element_COUNT<0||(unsigned)element_COUNT>=sizeof(Mətn)-mətnin_ölçüsü){잘못됨=1;return;}mətnin_ölçüsü+=element_COUNT;}
static int 서술자(unsigned identifikator_VALUE,int*ölçü){
    if(identifikator_VALUE<1||identifikator_VALUE>=sabit_aylıq_cəmi_dəqiqə||Teqlər_Siyahı[identifikator_VALUE]!=1)return -1;unsigned verilənlər_yerinə_qoymaq=첫째값[identifikator_VALUE],bitirmək_OFFSET=verilənlər_yerinə_qoymaq+SECOND_VALUE[identifikator_VALUE];if(verilənlər_yerinə_qoymaq>=bitirmək_OFFSET||verilənlər[verilənlər_yerinə_qoymaq++]!='(')return -1;int daxiletmə_COUNT=0;
    while(verilənlər_yerinə_qoymaq<bitirmək_OFFSET&&verilənlər[verilənlər_yerinə_qoymaq]!=')'){
        unsigned simvol_kodu=verilənlər[verilənlər_yerinə_qoymaq++];while(simvol_kodu=='['&&verilənlər_yerinə_qoymaq<bitirmək_OFFSET)simvol_kodu=verilənlər[verilənlər_yerinə_qoymaq++];
        if(simvol_kodu=='L'){while(verilənlər_yerinə_qoymaq<bitirmək_OFFSET&&verilənlər[verilənlər_yerinə_qoymaq]!=';')verilənlər_yerinə_qoymaq++;if(verilənlər_yerinə_qoymaq==bitirmək_OFFSET)return -1;verilənlər_yerinə_qoymaq++;}
        else if(simvol_kodu!='I'&&simvol_kodu!='Z'&&simvol_kodu!='B'&&simvol_kodu!='C'&&simvol_kodu!='S')return -1;
        if(++daxiletmə_COUNT>16)return -1;
    }
    if(verilənlər_yerinə_qoymaq+1>=bitirmək_OFFSET||verilənlər[verilənlər_yerinə_qoymaq++]!=')')return -1;*ölçü=verilənlər[verilənlər_yerinə_qoymaq]=='V'?0:1;
    if(verilənlər[verilənlər_yerinə_qoymaq]=='J'||verilənlər[verilənlər_yerinə_qoymaq]=='D'||verilənlər[verilənlər_yerinə_qoymaq]=='F')return -1;return daxiletmə_COUNT;
}
static void atributlar(void){unsigned element_COUNT=절반값();for(unsigned 순번=0;순번<element_COUNT&&!잘못됨;순번++){절반값();unsigned Böyüklük=가득참();TAKE_VALUE(Böyüklük);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned kiçik_versiya=절반값(),versiya_nömrəsi=절반값();if(kiçik_versiya||versiya_nömrəsi<45||versiya_nömrəsi>52)return -1;
    sabit_aylıq_cəmi_dəqiqə=절반값();if(sabit_aylıq_cəmi_dəqiqə<1||sabit_aylıq_cəmi_dəqiqə>512)return -1;
    for(unsigned 순번=1;순번<sabit_aylıq_cəmi_dəqiqə&&!잘못됨;순번++){
        Teqlər_Siyahı[순번]=bayt_verilənlər();switch(Teqlər_Siyahı[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=sabit_aylıq_cəmi_dəqiqə)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bayt_verilənlər();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=sabit_aylıq_cəmi_dəqiqə||Teqlər_Siyahı[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=sabit_aylıq_cəmi_dəqiqə||Teqlər_Siyahı[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti=절반값();sahənin_adı[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&8))return -1;
        unsigned daxiletmə_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<daxiletmə_COUNT&&!잘못됨;안쪽순번++){
            unsigned Ad=절반값(),Böyüklük=가득참();
            if(UNICODE_VALUE(Ad,"ConstantValue")){if(Böyüklük!=2)return -1;sahə_sabit[순번]=절반값();}
            else TAKE_VALUE(Böyüklük);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        metod_daxiletmə*Qrup_ölçünü_dəyişmək=메소드목록+순번;Qrup_ölçünü_dəyişmək->konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti=절반값();Qrup_ölçünü_dəyişmək->Ad=절반값();Qrup_ölçünü_dəyişmək->서술값=절반값();unsigned daxiletmə_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<daxiletmə_COUNT&&!잘못됨;안쪽순번++){
            unsigned Ad=절반값(),Böyüklük=가득참(),İcra_Et=현재위치;
            if(Böyüklük>uzunluq_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(Ad,"Code")){
                Qrup_ölçünü_dəyişmək->Yığın_Yaddaş=절반값();Qrup_ölçünü_dəyişmək->지역변수들=절반값();Qrup_ölçünü_dəyişmək->Böyüklük=가득참();Qrup_ölçünü_dəyişmək->təlimat_SEQUENCE=TAKE_VALUE(Qrup_ölçünü_dəyişmək->Böyüklük);
                if(Qrup_ölçünü_dəyişmək->Yığın_Yaddaş>128||Qrup_ölçünü_dəyişmək->지역변수들>128||Qrup_ölçünü_dəyişmək->Böyüklük>8192||절반값())return -1;atributlar();
            }else TAKE_VALUE(Böyüklük);
            if(현재위치!=İcra_Et+Böyüklük)return -1;
        }
        if(!UNICODE_VALUE(Qrup_ölçünü_dəyişmək->Ad,"<init>")&&(!(Qrup_ölçünü_dəyişmək->konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&8)||(Qrup_ölçünü_dəyişmək->konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&(0x100|0x20))||!Qrup_ölçünü_dəyişmək->Böyüklük))return -1;
    }
    atributlar();return 잘못됨||현재위치!=uzunluq_VALUE?-1:0;
}
static void sabit_VALUE(unsigned identifikator_VALUE){
    if(!identifikator_VALUE||identifikator_VALUE>=sabit_aylıq_cəmi_dəqiqə){잘못됨=1;return;}
    if(Teqlər_Siyahı[identifikator_VALUE]==3)내보내기("P(%uU);",첫째값[identifikator_VALUE]);
    else if(Teqlər_Siyahı[identifikator_VALUE]==8)내보내기("P((W)k%u);",identifikator_VALUE);else 잘못됨=1;
}
static void 호출(unsigned identifikator_VALUE,int virtual_CALL){
    if(identifikator_VALUE<1||identifikator_VALUE>=sabit_aylıq_cəmi_dəqiqə||(Teqlər_Siyahı[identifikator_VALUE]!=10&&Teqlər_Siyahı[identifikator_VALUE]!=11)||첫째값[identifikator_VALUE]<1||첫째값[identifikator_VALUE]>=sabit_aylıq_cəmi_dəqiqə||Teqlər_Siyahı[첫째값[identifikator_VALUE]]!=7||SECOND_VALUE[identifikator_VALUE]<1||SECOND_VALUE[identifikator_VALUE]>=sabit_aylıq_cəmi_dəqiqə||Teqlər_Siyahı[SECOND_VALUE[identifikator_VALUE]]!=12){잘못됨=1;return;}
    unsigned sahib_obyekt=첫째값[첫째값[identifikator_VALUE]],Ad=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];int ölçü=0,element_COUNT=서술자(서술값,&ölçü);if(element_COUNT<0){잘못됨=1;return;}
    for(int 순번=element_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtual_CALL)내보내기("Q();");
    if(!virtual_CALL&&같음(sahib_obyekt,첫째값[현재클래스])){
        unsigned Qrup_ölçünü_dəyişmək=0;for(;Qrup_ölçünü_dəyişmək<메소드개수;Qrup_ölçünü_dəyişmək++)if(같음(Ad,메소드목록[Qrup_ölçünü_dəyişmək].Ad)&&같음(서술값,메소드목록[Qrup_ölçünü_dəyişmək].서술값))break;
        if(Qrup_ölçünü_dəyişmək==메소드개수||!(메소드목록[Qrup_ölçünü_dəyişmək].konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&8)){잘못됨=1;return;}
        if(ölçü)내보내기("P(");내보내기("m%u(",Qrup_ölçünü_dəyişmək);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(ölçü?"));":" );");return;
    }
    if((virtual_CALL&&UNICODE_VALUE(sahib_obyekt,"java/io/PrintStream")&& (UNICODE_VALUE(Ad,"print")||UNICODE_VALUE(Ad,"println")))||(!virtual_CALL&&UNICODE_VALUE(sahib_obyekt,"한국어/자체/출력"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Ad,"print")||UNICODE_VALUE(Ad,"println")||UNICODE_VALUE(Ad,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Ad,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Ad,"print")||UNICODE_VALUE(Ad,"println")||UNICODE_VALUE(Ad,"Yazma")||UNICODE_VALUE(Ad,"yazmaq_xətt"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Ad,"print")||UNICODE_VALUE(Ad,"Yazma")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Ad,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtual_CALL&&UNICODE_VALUE(sahib_obyekt,"한국어/자체/FAYL")){
        if(UNICODE_VALUE(Ad,"Yazma")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Ad,"Oxuma")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void qurmaq_metod(unsigned LOOKUP_INDEX){
    metod_daxiletmə*Qrup_ölçünü_dəyişmək=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Qrup_ölçünü_dəyişmək->Ad,"<init>"))return;int ölçü,element_COUNT=서술자(Qrup_ölçünü_dəyişmək->서술값,&ölçü);if(element_COUNT<0){잘못됨=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!element_COUNT)내보내기("void");
    if((unsigned)element_COUNT>Qrup_ölçünü_dəyişmək->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Qrup_ölçünü_dəyişmək->지역변수들?Qrup_ölçünü_dəyişmək->지역변수들:1);for(int 순번=0;순번<element_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=uzunluq_VALUE;uzunluq_VALUE=Qrup_ölçünü_dəyişmək->təlimat_SEQUENCE+Qrup_ölçünü_dəyişmək->Böyüklük;현재위치=Qrup_ölçünü_dəyişmək->təlimat_SEQUENCE;
    while(현재위치<uzunluq_VALUE&&!잘못됨){unsigned əmr_yerinə_qoymaq=현재위치-Qrup_ölçünü_dəyişmək->təlimat_SEQUENCE,əməliyyat_VALUE=bayt_verilənlər();내보내기("L%u:;",əmr_yerinə_qoymaq);
        if(əməliyyat_VALUE==0){}
        else if(əməliyyat_VALUE==1)내보내기("P(0);");
        else if(əməliyyat_VALUE>=2&&əməliyyat_VALUE<=8)내보내기("P(%uU);",əməliyyat_VALUE-3);
        else if(əməliyyat_VALUE==16){int VALUE=(int8_t)bayt_verilənlər();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(əməliyyat_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(əməliyyat_VALUE==18||əməliyyat_VALUE==19)sabit_VALUE(əməliyyat_VALUE==18?bayt_verilənlər():절반값());
        else if(əməliyyat_VALUE==21||əməliyyat_VALUE==25){unsigned 순번=bayt_verilənlər();if(순번>=Qrup_ölçünü_dəyişmək->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((əməliyyat_VALUE>=26&&əməliyyat_VALUE<=29)||(əməliyyat_VALUE>=42&&əməliyyat_VALUE<=45)){unsigned 순번=əməliyyat_VALUE>=42?əməliyyat_VALUE-42:əməliyyat_VALUE-26;if(순번>=Qrup_ölçünü_dəyişmək->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(əməliyyat_VALUE==54||əməliyyat_VALUE==58){unsigned 순번=bayt_verilənlər();if(순번>=Qrup_ölçünü_dəyişmək->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((əməliyyat_VALUE>=59&&əməliyyat_VALUE<=62)||(əməliyyat_VALUE>=75&&əməliyyat_VALUE<=78)){unsigned 순번=əməliyyat_VALUE>=75?əməliyyat_VALUE-75:əməliyyat_VALUE-59;if(순번>=Qrup_ölçünü_dəyişmək->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(əməliyyat_VALUE==46||əməliyyat_VALUE==50||əməliyyat_VALUE==51||əməliyyat_VALUE==52||əməliyyat_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(əməliyyat_VALUE==79||əməliyyat_VALUE==83||əməliyyat_VALUE==84||əməliyyat_VALUE==85||əməliyyat_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",əməliyyat_VALUE==84?"(unsigned)(signed char)q":əməliyyat_VALUE==85?"(unsigned short)q":əməliyyat_VALUE==86?"(unsigned)(short)q":"q");
        else if(əməliyyat_VALUE==87)내보내기("Q();");
        else if(əməliyyat_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(əməliyyat_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(əməliyyat_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(əməliyyat_VALUE==96||əməliyyat_VALUE==100||əməliyyat_VALUE==104||əməliyyat_VALUE==120||əməliyyat_VALUE==124||əməliyyat_VALUE==126||əməliyyat_VALUE==128||əməliyyat_VALUE==130){const char*kodlaşdırma_VALUE=əməliyyat_VALUE==96?"+":əməliyyat_VALUE==100?"-":əməliyyat_VALUE==104?"*":əməliyyat_VALUE==120?"<<":əməliyyat_VALUE==124?">>":əməliyyat_VALUE==126?"&":əməliyyat_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodlaşdırma_VALUE,əməliyyat_VALUE==120||əməliyyat_VALUE==124?"%32":"");}
        else if(əməliyyat_VALUE==108||əməliyyat_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",əməliyyat_VALUE==112);
        else if(əməliyyat_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(əməliyyat_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(əməliyyat_VALUE==132){unsigned 순번=bayt_verilənlər();int 차이=(int8_t)bayt_verilənlər();if(순번>=Qrup_ölçünü_dəyişmək->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(əməliyyat_VALUE>=145&&əməliyyat_VALUE<=147)내보내기("P((unsigned)(%s)Q());",əməliyyat_VALUE==145?"signed char":əməliyyat_VALUE==146?"unsigned short":"short");
        else if(əməliyyat_VALUE>=153&&əməliyyat_VALUE<=166){int hədəf=(int)əmr_yerinə_qoymaq+(int16_t)절반값();const char*Müqayisə_VALUE[]={"==","!=","<",">=",">","<="};if(hədəf<0||hədəf>=(int)Qrup_ölçünü_dəyişmək->Böyüklük){잘못됨=1;break;}if(əməliyyat_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Müqayisə_VALUE[əməliyyat_VALUE-153],hədəf);else if(əməliyyat_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Müqayisə_VALUE[əməliyyat_VALUE-159],hədəf);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",əməliyyat_VALUE==165?"==":"!=",hədəf);}
        else if(əməliyyat_VALUE==167){int hədəf=(int)əmr_yerinə_qoymaq+(int16_t)절반값();if(hədəf<0||hədəf>=(int)Qrup_ölçünü_dəyişmək->Böyüklük)잘못됨=1;내보내기("goto L%d;",hədəf);}
        else if(əməliyyat_VALUE==172||əməliyyat_VALUE==176)내보내기("return Q();");else if(əməliyyat_VALUE==177)내보내기("return 0;");
        else if(əməliyyat_VALUE==178||əməliyyat_VALUE==179){unsigned identifikator_VALUE=절반값();if(identifikator_VALUE<1||identifikator_VALUE>=sabit_aylıq_cəmi_dəqiqə||Teqlər_Siyahı[identifikator_VALUE]!=9||첫째값[identifikator_VALUE]>=sabit_aylıq_cəmi_dəqiqə||SECOND_VALUE[identifikator_VALUE]>=sabit_aylıq_cəmi_dəqiqə||Teqlər_Siyahı[첫째값[identifikator_VALUE]]!=7||Teqlər_Siyahı[SECOND_VALUE[identifikator_VALUE]]!=12){잘못됨=1;break;}unsigned sahib_obyekt=첫째값[첫째값[identifikator_VALUE]],Ad=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];
            if(əməliyyat_VALUE==178&&UNICODE_VALUE(sahib_obyekt,"java/lang/System")&&UNICODE_VALUE(Ad,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fayl_daxiletmə=0;while(fayl_daxiletmə<필드개수&&(!같음(Ad,sahənin_adı[fayl_daxiletmə])||!같음(서술값,필드서술[fayl_daxiletmə])))fayl_daxiletmə++;if(!같음(sahib_obyekt,첫째값[현재클래스])||fayl_daxiletmə==필드개수){잘못됨=1;break;}내보내기(əməliyyat_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",fayl_daxiletmə);}}
        else if(əməliyyat_VALUE==182||əməliyyat_VALUE==184)호출(절반값(),əməliyyat_VALUE==182);
        else if(əməliyyat_VALUE==188){unsigned TYPE_sahə=bayt_verilənlər();if(TYPE_sahə!=4&&TYPE_sahə!=5&&TYPE_sahə!=8&&TYPE_sahə!=9&&TYPE_sahə!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(əməliyyat_VALUE==190)내보내기("P(jlength(Q()));");
        else if(əməliyyat_VALUE==198||əməliyyat_VALUE==199){int hədəf=(int)əmr_yerinə_qoymaq+(int16_t)절반값();if(hədəf<0||hədəf>=(int)Qrup_ölçünü_dəyişmək->Böyüklük)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",əməliyyat_VALUE==198?"==":"!=",hədəf);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,əməliyyat_VALUE,əmr_yerinə_qoymaq);
        내보내기("\n");
    }
    uzunluq_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned sətir_dərs(unsigned *verilənlər_yerinə_qoymaq,unsigned bitirmək_OFFSET){
    if(*verilənlər_yerinə_qoymaq>=bitirmək_OFFSET){잘못됨=1;return 0;}unsigned simvol_kodu=verilənlər[(*verilənlər_yerinə_qoymaq)++];
    if(simvol_kodu<128)return simvol_kodu;
    unsigned element_COUNT=simvol_kodu>=0xc0&&simvol_kodu<=0xdf?1:simvol_kodu>=0xe0&&simvol_kodu<=0xef?2:3;
    if(element_COUNT==3||element_COUNT>bitirmək_OFFSET-*verilənlər_yerinə_qoymaq){잘못됨=1;return 0;}unsigned VALUE=simvol_kodu&((1u<<(6-element_COUNT))-1);
    for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned Sonrakı_element=verilənlər[(*verilənlər_yerinə_qoymaq)++];if((Sonrakı_element&0xc0)!=0x80)잘못됨=1;VALUE=VALUE<<6|(Sonrakı_element&63);}
    if((element_COUNT==1&&VALUE<128&&VALUE!=0)||(element_COUNT==2&&VALUE<2048))잘못됨=1;return VALUE;
}
static void sətir_sabit(unsigned identifikator_VALUE){
    unsigned 부호없는값=첫째값[identifikator_VALUE];if(부호없는값<1||부호없는값>=sabit_aylıq_cəmi_dəqiqə||Teqlər_Siyahı[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",identifikator_VALUE);
    unsigned verilənlər_yerinə_qoymaq=첫째값[부호없는값],bitirmək_OFFSET=verilənlər_yerinə_qoymaq+SECOND_VALUE[부호없는값];
    while(verilənlər_yerinə_qoymaq<bitirmək_OFFSET&&!잘못됨){unsigned simvol_kodu=sətir_dərs(&verilənlər_yerinə_qoymaq,bitirmək_OFFSET);
        if(simvol_kodu>=0xd800&&simvol_kodu<=0xdbff){unsigned 낮은부분=sətir_dərs(&verilənlər_yerinə_qoymaq,bitirmək_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}simvol_kodu=0x10000+((simvol_kodu-0xd800)<<10)+낮은부분-0xdc00;}
        else if(simvol_kodu>=0xdc00&&simvol_kodu<=0xdfff){잘못됨=1;break;}
        if(!simvol_kodu){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(simvol_kodu<128)내보내기("%u,",simvol_kodu);
        else{unsigned element_COUNT=simvol_kodu<2048?2:simvol_kodu<65536?3:4;내보내기("%u,",(element_COUNT==2?0xc0:element_COUNT==3?0xe0:0xf0)|(simvol_kodu>>(6*(element_COUNT-1))));for(unsigned 순번=element_COUNT-1;순번;순번--)내보내기("%u,",0x80|((simvol_kodu>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Ad){
    size_t element_COUNT=strlen(Ad);
    if(element_COUNT>4&&!strcmp(Ad+element_COUNT-4,".jar")){
        if(꾸러미열기(Ad)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Cığır[256];const char*daxiletmə_metod=꾸러미진입클래스();element_COUNT=strlen(daxiletmə_metod);if(element_COUNT+6>=sizeof(Cığır))return 0;
        for(unsigned 순번=0;순번<element_COUNT;순번++)Cığır[순번]=daxiletmə_metod[순번]=='.'?'/':daxiletmə_metod[순번];strcpy(Cığır+element_COUNT,".class");int daxiletmə_COUNT=꾸러미읽기(Cığır,verilənlər,sizeof(verilənlər));if(daxiletmə_COUNT<0)return 0;uzunluq_VALUE=daxiletmə_COUNT;
    }else{intptr_t fayl_tutacaq=사용자호출(3,(uintptr_t)Ad,0,0,0,0,0);if(fayl_tutacaq<0)return 0;intptr_t daxiletmə_COUNT=사용자호출(9,fayl_tutacaq,0,0,0,0,0);if(daxiletmə_COUNT<0||daxiletmə_COUNT>sizeof(verilənlər)){사용자호출(4,fayl_tutacaq,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,fayl_tutacaq,(uintptr_t)verilənlər,daxiletmə_COUNT,0,0,0);사용자호출(4,fayl_tutacaq,0,0,0,0,0);if(RECEIVED_COUNT!=daxiletmə_COUNT)return 0;uzunluq_VALUE=daxiletmə_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<sabit_aylıq_cəmi_dəqiqə&&!잘못됨;순번++)if(Teqlər_Siyahı[순번]==8)sətir_sabit(순번);
    if(잘못됨)return 0;
    int daxiletmə_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Ad,"<init>")){
        int ölçü,daxiletmə_COUNT=서술자(메소드목록[순번].서술값,&ölçü);if(daxiletmə_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<daxiletmə_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!daxiletmə_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Ad,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti&9)==9)daxiletmə_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Ad,"<clinit>"))초기값=순번;
    }
    if(daxiletmə_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)qurmaq_metod(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(sahə_sabit[순번]){
        unsigned simvol_kodu=sahə_sabit[순번];if(simvol_kodu>=sabit_aylıq_cəmi_dəqiqə)return 0;
        if(Teqlər_Siyahı[simvol_kodu]==3)내보내기("fields[%u]=%uU;",순번,첫째값[simvol_kodu]);else if(Teqlər_Siyahı[simvol_kodu]==8)내보내기("fields[%u]=(W)k%u;",순번,simvol_kodu);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",daxiletmə_p);
    return 잘못됨?0:Mətn;
}
