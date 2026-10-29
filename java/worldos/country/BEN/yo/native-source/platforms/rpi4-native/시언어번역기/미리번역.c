#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "àkópọ̀.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char détà[16384];static unsigned gígùn_iye,현재위치;static int 잘못됨;
static unsigned Ìsàmì_Àtòkọ[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char SMS[65536];static unsigned ìwọn_àyọkà;
typedef struct {unsigned 설정비트,Orúkọ,서술값,ìtọ́sọ́nà_ÀTẸ̀LÉRA,Ìwọ̀n,지역변수들,kójọ_Ibi_ìpamọ́;} ìlànà_ìgbéwọlé;
static ìlànà_ìgbéwọlé 메소드목록[64];static unsigned 메소드개수;
static unsigned orúkọ_ààyè_wúnrẹ̀n[64],필드서술[64],àayè_wúnrẹ̀n_aláìṣeéyípadà[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>gígùn_iye||개수>gígùn_iye-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned báìtì_détà(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:détà[자료위치];}
static unsigned 절반값(void){unsigned ibi_ìtọ́kasí_x=báìtì_détà();return ibi_ìtọ́kasí_x<<8|báìtì_détà();}
static uint32_t 가득참(void){uint32_t ibi_ìtọ́kasí_x=절반값();return ibi_ìtọ́kasí_x<<16|절반값();}
static int Unicode_iye(unsigned 순번,const char*fọ́nrán_détà){return 순번>0&&순번<상수모음&&Ìsàmì_Àtòkọ[순번]==1&&strlen(fọ́nrán_détà)==둘째값[순번]&&!memcmp(détà+첫째값[순번],fọ́nrán_détà,둘째값[순번]);}
static int 같음(unsigned ibi_ìtọ́kasí_x,unsigned 세로좌표){return ibi_ìtọ́kasí_x>0&&ibi_ìtọ́kasí_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&Ìsàmì_Àtòkọ[ibi_ìtọ́kasí_x]==1&&Ìsàmì_Àtòkọ[세로좌표]==1&&둘째값[ibi_ìtọ́kasí_x]==둘째값[세로좌표]&&!memcmp(détà+첫째값[ibi_ìtọ́kasí_x],détà+첫째값[세로좌표],둘째값[ibi_ìtọ́kasí_x]);}
static void 내보내기(const char*fáìlì_ìgbéwọlé,...){if(잘못됨)return;va_list ágúmẹ́ntì_ÀRÉÈ;va_start(ágúmẹ́ntì_ÀRÉÈ,fáìlì_ìgbéwọlé);int 개수=vsnprintf(SMS+ìwọn_àyọkà,sizeof(SMS)-ìwọn_àyọkà,fáìlì_ìgbéwọlé,ágúmẹ́ntì_ÀRÉÈ);va_end(ágúmẹ́ntì_ÀRÉÈ);if(개수<0||(unsigned)개수>=sizeof(SMS)-ìwọn_àyọkà){잘못됨=1;return;}ìwọn_àyọkà+=개수;}
static int 서술자(unsigned Àfidámọ̀_iye,int*결과){
    if(Àfidámọ̀_iye<1||Àfidámọ̀_iye>=상수모음||Ìsàmì_Àtòkọ[Àfidámọ̀_iye]!=1)return -1;unsigned 자료위치=첫째값[Àfidámọ̀_iye],parí_Ìtayọ=자료위치+둘째값[Àfidámọ̀_iye];if(자료위치>=parí_Ìtayọ||détà[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<parí_Ìtayọ&&détà[자료위치]!=')'){
        unsigned kóòdù_ẹyọ_ọ̀rọ̀=détà[자료위치++];while(kóòdù_ẹyọ_ọ̀rọ̀=='['&&자료위치<parí_Ìtayọ)kóòdù_ẹyọ_ọ̀rọ̀=détà[자료위치++];
        if(kóòdù_ẹyọ_ọ̀rọ̀=='L'){while(자료위치<parí_Ìtayọ&&détà[자료위치]!=';')자료위치++;if(자료위치==parí_Ìtayọ)return -1;자료위치++;}
        else if(kóòdù_ẹyọ_ọ̀rọ̀!='I'&&kóòdù_ẹyọ_ọ̀rọ̀!='Z'&&kóòdù_ẹyọ_ọ̀rọ̀!='B'&&kóòdù_ẹyọ_ọ̀rọ̀!='C'&&kóòdù_ẹyọ_ọ̀rọ̀!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=parí_Ìtayọ||détà[자료위치++]!=')')return -1;*결과=détà[자료위치]=='V'?0:1;
    if(détà[자료위치]=='J'||détà[자료위치]=='D'||détà[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned Ìwọ̀n=가득참();가져오기(Ìwọ̀n);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned ọdọ́_ẹ̀yà=절반값(),판번호=절반값();if(ọdọ́_ẹ̀yà||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Ìsàmì_Àtòkọ[순번]=báìtì_détà();switch(Ìsàmì_Àtòkọ[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=báìtì_détà();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Ìsàmì_Àtòkọ[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Ìsàmì_Àtòkọ[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();orúkọ_ààyè_wúnrẹ̀n[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Orúkọ=절반값(),Ìwọ̀n=가득참();
            if(Unicode_iye(Orúkọ,"ConstantValue")){if(Ìwọ̀n!=2)return -1;àayè_wúnrẹ̀n_aláìṣeéyípadà[순번]=절반값();}
            else 가져오기(Ìwọ̀n);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        ìlànà_ìgbéwọlé*Àjọṣe_ìwọn=메소드목록+순번;Àjọṣe_ìwọn->설정비트=절반값();Àjọṣe_ìwọn->Orúkọ=절반값();Àjọṣe_ìwọn->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Orúkọ=절반값(),Ìwọ̀n=가득참(),Rọ́ọ̀nù=현재위치;
            if(Ìwọ̀n>gígùn_iye-현재위치)return -1;
            if(Unicode_iye(Orúkọ,"Code")){
                Àjọṣe_ìwọn->kójọ_Ibi_ìpamọ́=절반값();Àjọṣe_ìwọn->지역변수들=절반값();Àjọṣe_ìwọn->Ìwọ̀n=가득참();Àjọṣe_ìwọn->ìtọ́sọ́nà_ÀTẸ̀LÉRA=가져오기(Àjọṣe_ìwọn->Ìwọ̀n);
                if(Àjọṣe_ìwọn->kójọ_Ibi_ìpamọ́>128||Àjọṣe_ìwọn->지역변수들>128||Àjọṣe_ìwọn->Ìwọ̀n>8192||절반값())return -1;속성들();
            }else 가져오기(Ìwọ̀n);
            if(현재위치!=Rọ́ọ̀nù+Ìwọ̀n)return -1;
        }
        if(!Unicode_iye(Àjọṣe_ìwọn->Orúkọ,"<init>")&&(!(Àjọṣe_ìwọn->설정비트&8)||(Àjọṣe_ìwọn->설정비트&(0x100|0x20))||!Àjọṣe_ìwọn->Ìwọ̀n))return -1;
    }
    속성들();return 잘못됨||현재위치!=gígùn_iye?-1:0;
}
static void aláìṣeéyípadà_iye(unsigned Àfidámọ̀_iye){
    if(!Àfidámọ̀_iye||Àfidámọ̀_iye>=상수모음){잘못됨=1;return;}
    if(Ìsàmì_Àtòkọ[Àfidámọ̀_iye]==3)내보내기("P(%uU);",첫째값[Àfidámọ̀_iye]);
    else if(Ìsàmì_Àtòkọ[Àfidámọ̀_iye]==8)내보내기("P((W)k%u);",Àfidámọ̀_iye);else 잘못됨=1;
}
static void 호출(unsigned Àfidámọ̀_iye,int àfojúunúṣe_pè){
    if(Àfidámọ̀_iye<1||Àfidámọ̀_iye>=상수모음||(Ìsàmì_Àtòkọ[Àfidámọ̀_iye]!=10&&Ìsàmì_Àtòkọ[Àfidámọ̀_iye]!=11)||첫째값[Àfidámọ̀_iye]<1||첫째값[Àfidámọ̀_iye]>=상수모음||Ìsàmì_Àtòkọ[첫째값[Àfidámọ̀_iye]]!=7||둘째값[Àfidámọ̀_iye]<1||둘째값[Àfidámọ̀_iye]>=상수모음||Ìsàmì_Àtòkọ[둘째값[Àfidámọ̀_iye]]!=12){잘못됨=1;return;}
    unsigned Oníǹkan_nǹkan=첫째값[첫째값[Àfidámọ̀_iye]],Orúkọ=첫째값[둘째값[Àfidámọ̀_iye]],서술값=둘째값[둘째값[Àfidámọ̀_iye]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(àfojúunúṣe_pè)내보내기("Q();");
    if(!àfojúunúṣe_pè&&같음(Oníǹkan_nǹkan,첫째값[현재클래스])){
        unsigned Àjọṣe_ìwọn=0;for(;Àjọṣe_ìwọn<메소드개수;Àjọṣe_ìwọn++)if(같음(Orúkọ,메소드목록[Àjọṣe_ìwọn].Orúkọ)&&같음(서술값,메소드목록[Àjọṣe_ìwọn].서술값))break;
        if(Àjọṣe_ìwọn==메소드개수||!(메소드목록[Àjọṣe_ìwọn].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",Àjọṣe_ìwọn);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((àfojúunúṣe_pè&&Unicode_iye(Oníǹkan_nǹkan,"java/io/PrintStream")&& (Unicode_iye(Orúkọ,"print")||Unicode_iye(Orúkọ,"println")))||(!àfojúunúṣe_pè&&Unicode_iye(Oníǹkan_nǹkan,"한국어/자체/출력"))){
        if(Unicode_iye(서술값,"(I)V")&&(Unicode_iye(Orúkọ,"print")||Unicode_iye(Orúkọ,"println")||Unicode_iye(Orúkọ,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Unicode_iye(Orúkọ,"print")?0:1);return;}
        if(Unicode_iye(서술값,"(Ljava/lang/String;)V")&&(Unicode_iye(Orúkọ,"print")||Unicode_iye(Orúkọ,"println")||Unicode_iye(Orúkọ,"Kọ")||Unicode_iye(Orúkọ,"kọ_ìlà"))){내보내기("jprint(x[0],0,%d);",Unicode_iye(Orúkọ,"print")||Unicode_iye(Orúkọ,"Kọ")?0:1);return;}
        if(Unicode_iye(서술값,"()V")&&Unicode_iye(Orúkọ,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!àfojúunúṣe_pè&&Unicode_iye(Oníǹkan_nǹkan,"한국어/자체/Fáìlì")){
        if(Unicode_iye(Orúkọ,"Kọ")&&Unicode_iye(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Unicode_iye(Orúkọ,"Kàá")&&Unicode_iye(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_ìlànà(unsigned 색인){
    ìlànà_ìgbéwọlé*Àjọṣe_ìwọn=메소드목록+색인;if(Unicode_iye(Àjọṣe_ìwọn->Orúkọ,"<init>"))return;int 결과,개수=서술자(Àjọṣe_ìwọn->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>Àjọṣe_ìwọn->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Àjọṣe_ìwọn->지역변수들?Àjọṣe_ìwọn->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=gígùn_iye;gígùn_iye=Àjọṣe_ìwọn->ìtọ́sọ́nà_ÀTẸ̀LÉRA+Àjọṣe_ìwọn->Ìwọ̀n;현재위치=Àjọṣe_ìwọn->ìtọ́sọ́nà_ÀTẸ̀LÉRA;
    while(현재위치<gígùn_iye&&!잘못됨){unsigned 명령위치=현재위치-Àjọṣe_ìwọn->ìtọ́sọ́nà_ÀTẸ̀LÉRA,ìmú_ṣiṣẹ́_iye=báìtì_détà();내보내기("L%u:;",명령위치);
        if(ìmú_ṣiṣẹ́_iye==0){}
        else if(ìmú_ṣiṣẹ́_iye==1)내보내기("P(0);");
        else if(ìmú_ṣiṣẹ́_iye>=2&&ìmú_ṣiṣẹ́_iye<=8)내보내기("P(%uU);",ìmú_ṣiṣẹ́_iye-3);
        else if(ìmú_ṣiṣẹ́_iye==16){int iye=(int8_t)báìtì_détà();내보내기("P(%uU);",(unsigned)iye);}
        else if(ìmú_ṣiṣẹ́_iye==17){int iye=(int16_t)절반값();내보내기("P(%uU);",(unsigned)iye);}
        else if(ìmú_ṣiṣẹ́_iye==18||ìmú_ṣiṣẹ́_iye==19)aláìṣeéyípadà_iye(ìmú_ṣiṣẹ́_iye==18?báìtì_détà():절반값());
        else if(ìmú_ṣiṣẹ́_iye==21||ìmú_ṣiṣẹ́_iye==25){unsigned 순번=báìtì_détà();if(순번>=Àjọṣe_ìwọn->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((ìmú_ṣiṣẹ́_iye>=26&&ìmú_ṣiṣẹ́_iye<=29)||(ìmú_ṣiṣẹ́_iye>=42&&ìmú_ṣiṣẹ́_iye<=45)){unsigned 순번=ìmú_ṣiṣẹ́_iye>=42?ìmú_ṣiṣẹ́_iye-42:ìmú_ṣiṣẹ́_iye-26;if(순번>=Àjọṣe_ìwọn->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(ìmú_ṣiṣẹ́_iye==54||ìmú_ṣiṣẹ́_iye==58){unsigned 순번=báìtì_détà();if(순번>=Àjọṣe_ìwọn->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((ìmú_ṣiṣẹ́_iye>=59&&ìmú_ṣiṣẹ́_iye<=62)||(ìmú_ṣiṣẹ́_iye>=75&&ìmú_ṣiṣẹ́_iye<=78)){unsigned 순번=ìmú_ṣiṣẹ́_iye>=75?ìmú_ṣiṣẹ́_iye-75:ìmú_ṣiṣẹ́_iye-59;if(순번>=Àjọṣe_ìwọn->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(ìmú_ṣiṣẹ́_iye==46||ìmú_ṣiṣẹ́_iye==50||ìmú_ṣiṣẹ́_iye==51||ìmú_ṣiṣẹ́_iye==52||ìmú_ṣiṣẹ́_iye==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(ìmú_ṣiṣẹ́_iye==79||ìmú_ṣiṣẹ́_iye==83||ìmú_ṣiṣẹ́_iye==84||ìmú_ṣiṣẹ́_iye==85||ìmú_ṣiṣẹ́_iye==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",ìmú_ṣiṣẹ́_iye==84?"(unsigned)(signed char)q":ìmú_ṣiṣẹ́_iye==85?"(unsigned short)q":ìmú_ṣiṣẹ́_iye==86?"(unsigned)(short)q":"q");
        else if(ìmú_ṣiṣẹ́_iye==87)내보내기("Q();");
        else if(ìmú_ṣiṣẹ́_iye==89)내보내기("q=Q();P(q);P(q);");
        else if(ìmú_ṣiṣẹ́_iye==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(ìmú_ṣiṣẹ́_iye==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(ìmú_ṣiṣẹ́_iye==96||ìmú_ṣiṣẹ́_iye==100||ìmú_ṣiṣẹ́_iye==104||ìmú_ṣiṣẹ́_iye==120||ìmú_ṣiṣẹ́_iye==124||ìmú_ṣiṣẹ́_iye==126||ìmú_ṣiṣẹ́_iye==128||ìmú_ṣiṣẹ́_iye==130){const char*pípàrokò_iye=ìmú_ṣiṣẹ́_iye==96?"+":ìmú_ṣiṣẹ́_iye==100?"-":ìmú_ṣiṣẹ́_iye==104?"*":ìmú_ṣiṣẹ́_iye==120?"<<":ìmú_ṣiṣẹ́_iye==124?">>":ìmú_ṣiṣẹ́_iye==126?"&":ìmú_ṣiṣẹ́_iye==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",pípàrokò_iye,ìmú_ṣiṣẹ́_iye==120||ìmú_ṣiṣẹ́_iye==124?"%32":"");}
        else if(ìmú_ṣiṣẹ́_iye==108||ìmú_ṣiṣẹ́_iye==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",ìmú_ṣiṣẹ́_iye==112);
        else if(ìmú_ṣiṣẹ́_iye==116)내보내기("P(0U-(unsigned)Q());");
        else if(ìmú_ṣiṣẹ́_iye==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(ìmú_ṣiṣẹ́_iye==132){unsigned 순번=báìtì_détà();int 차이=(int8_t)báìtì_détà();if(순번>=Àjọṣe_ìwọn->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(ìmú_ṣiṣẹ́_iye>=145&&ìmú_ṣiṣẹ́_iye<=147)내보내기("P((unsigned)(%s)Q());",ìmú_ṣiṣẹ́_iye==145?"signed char":ìmú_ṣiṣẹ́_iye==146?"unsigned short":"short");
        else if(ìmú_ṣiṣẹ́_iye>=153&&ìmú_ṣiṣẹ́_iye<=166){int àfojúsùn=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(àfojúsùn<0||àfojúsùn>=(int)Àjọṣe_ìwọn->Ìwọ̀n){잘못됨=1;break;}if(ìmú_ṣiṣẹ́_iye<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[ìmú_ṣiṣẹ́_iye-153],àfojúsùn);else if(ìmú_ṣiṣẹ́_iye<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[ìmú_ṣiṣẹ́_iye-159],àfojúsùn);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",ìmú_ṣiṣẹ́_iye==165?"==":"!=",àfojúsùn);}
        else if(ìmú_ṣiṣẹ́_iye==167){int àfojúsùn=(int)명령위치+(int16_t)절반값();if(àfojúsùn<0||àfojúsùn>=(int)Àjọṣe_ìwọn->Ìwọ̀n)잘못됨=1;내보내기("goto L%d;",àfojúsùn);}
        else if(ìmú_ṣiṣẹ́_iye==172||ìmú_ṣiṣẹ́_iye==176)내보내기("return Q();");else if(ìmú_ṣiṣẹ́_iye==177)내보내기("return 0;");
        else if(ìmú_ṣiṣẹ́_iye==178||ìmú_ṣiṣẹ́_iye==179){unsigned Àfidámọ̀_iye=절반값();if(Àfidámọ̀_iye<1||Àfidámọ̀_iye>=상수모음||Ìsàmì_Àtòkọ[Àfidámọ̀_iye]!=9||첫째값[Àfidámọ̀_iye]>=상수모음||둘째값[Àfidámọ̀_iye]>=상수모음||Ìsàmì_Àtòkọ[첫째값[Àfidámọ̀_iye]]!=7||Ìsàmì_Àtòkọ[둘째값[Àfidámọ̀_iye]]!=12){잘못됨=1;break;}unsigned Oníǹkan_nǹkan=첫째값[첫째값[Àfidámọ̀_iye]],Orúkọ=첫째값[둘째값[Àfidámọ̀_iye]],서술값=둘째값[둘째값[Àfidámọ̀_iye]];
            if(ìmú_ṣiṣẹ́_iye==178&&Unicode_iye(Oníǹkan_nǹkan,"java/lang/System")&&Unicode_iye(Orúkọ,"out")&&Unicode_iye(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fáìlì_ìgbéwọlé=0;while(fáìlì_ìgbéwọlé<필드개수&&(!같음(Orúkọ,orúkọ_ààyè_wúnrẹ̀n[fáìlì_ìgbéwọlé])||!같음(서술값,필드서술[fáìlì_ìgbéwọlé])))fáìlì_ìgbéwọlé++;if(!같음(Oníǹkan_nǹkan,첫째값[현재클래스])||fáìlì_ìgbéwọlé==필드개수){잘못됨=1;break;}내보내기(ìmú_ṣiṣẹ́_iye==178?"P(fields[%u]);":"fields[%u]=Q();",fáìlì_ìgbéwọlé);}}
        else if(ìmú_ṣiṣẹ́_iye==182||ìmú_ṣiṣẹ́_iye==184)호출(절반값(),ìmú_ṣiṣẹ́_iye==182);
        else if(ìmú_ṣiṣẹ́_iye==188){unsigned irú_ìsọ̀rí=báìtì_détà();if(irú_ìsọ̀rí!=4&&irú_ìsọ̀rí!=5&&irú_ìsọ̀rí!=8&&irú_ìsọ̀rí!=9&&irú_ìsọ̀rí!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(ìmú_ṣiṣẹ́_iye==190)내보내기("P(jlength(Q()));");
        else if(ìmú_ṣiṣẹ́_iye==198||ìmú_ṣiṣẹ́_iye==199){int àfojúsùn=(int)명령위치+(int16_t)절반값();if(àfojúsùn<0||àfojúsùn>=(int)Àjọṣe_ìwọn->Ìwọ̀n)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",ìmú_ṣiṣẹ́_iye==198?"==":"!=",àfojúsùn);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,ìmú_ṣiṣẹ́_iye,명령위치);
        내보내기("\n");
    }
    gígùn_iye=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned fọ́nrán_ìkẹ́kọ̀ọ́(unsigned *자료위치,unsigned parí_Ìtayọ){
    if(*자료위치>=parí_Ìtayọ){잘못됨=1;return 0;}unsigned kóòdù_ẹyọ_ọ̀rọ̀=détà[(*자료위치)++];
    if(kóòdù_ẹyọ_ọ̀rọ̀<128)return kóòdù_ẹyọ_ọ̀rọ̀;
    unsigned 개수=kóòdù_ẹyọ_ọ̀rọ̀>=0xc0&&kóòdù_ẹyọ_ọ̀rọ̀<=0xdf?1:kóòdù_ẹyọ_ọ̀rọ̀>=0xe0&&kóòdù_ẹyọ_ọ̀rọ̀<=0xef?2:3;
    if(개수==3||개수>parí_Ìtayọ-*자료위치){잘못됨=1;return 0;}unsigned iye=kóòdù_ẹyọ_ọ̀rọ̀&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=détà[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;iye=iye<<6|(다음&63);}
    if((개수==1&&iye<128&&iye!=0)||(개수==2&&iye<2048))잘못됨=1;return iye;
}
static void fọ́nrán_aláìṣeéyípadà(unsigned Àfidámọ̀_iye){
    unsigned 부호없는값=첫째값[Àfidámọ̀_iye];if(부호없는값<1||부호없는값>=상수모음||Ìsàmì_Àtòkọ[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",Àfidámọ̀_iye);
    unsigned 자료위치=첫째값[부호없는값],parí_Ìtayọ=자료위치+둘째값[부호없는값];
    while(자료위치<parí_Ìtayọ&&!잘못됨){unsigned kóòdù_ẹyọ_ọ̀rọ̀=fọ́nrán_ìkẹ́kọ̀ọ́(&자료위치,parí_Ìtayọ);
        if(kóòdù_ẹyọ_ọ̀rọ̀>=0xd800&&kóòdù_ẹyọ_ọ̀rọ̀<=0xdbff){unsigned 낮은부분=fọ́nrán_ìkẹ́kọ̀ọ́(&자료위치,parí_Ìtayọ);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}kóòdù_ẹyọ_ọ̀rọ̀=0x10000+((kóòdù_ẹyọ_ọ̀rọ̀-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kóòdù_ẹyọ_ọ̀rọ̀>=0xdc00&&kóòdù_ẹyọ_ọ̀rọ̀<=0xdfff){잘못됨=1;break;}
        if(!kóòdù_ẹyọ_ọ̀rọ̀){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(kóòdù_ẹyọ_ọ̀rọ̀<128)내보내기("%u,",kóòdù_ẹyọ_ọ̀rọ̀);
        else{unsigned 개수=kóòdù_ẹyọ_ọ̀rọ̀<2048?2:kóòdù_ẹyọ_ọ̀rọ̀<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(kóòdù_ẹyọ_ọ̀rọ̀>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((kóòdù_ẹyọ_ọ̀rọ̀>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Orúkọ){
    size_t 개수=strlen(Orúkọ);
    if(개수>4&&!strcmp(Orúkọ+개수-4,".jar")){
        if(꾸러미열기(Orúkọ)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char ọ̀nà[256];const char*ìgbéwọlé_ìlànà=꾸러미진입클래스();개수=strlen(ìgbéwọlé_ìlànà);if(개수+6>=sizeof(ọ̀nà))return 0;
        for(unsigned 순번=0;순번<개수;순번++)ọ̀nà[순번]=ìgbéwọlé_ìlànà[순번]=='.'?'/':ìgbéwọlé_ìlànà[순번];strcpy(ọ̀nà+개수,".class");int 항목수=꾸러미읽기(ọ̀nà,détà,sizeof(détà));if(항목수<0)return 0;gígùn_iye=항목수;
    }else{intptr_t fáìlì_èkù=사용자호출(3,(uintptr_t)Orúkọ,0,0,0,0,0);if(fáìlì_èkù<0)return 0;intptr_t 항목수=사용자호출(9,fáìlì_èkù,0,0,0,0,0);if(항목수<0||항목수>sizeof(détà)){사용자호출(4,fáìlì_èkù,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,fáìlì_èkù,(uintptr_t)détà,항목수,0,0,0);사용자호출(4,fáìlì_èkù,0,0,0,0,0);if(받은수!=항목수)return 0;gígùn_iye=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Ìsàmì_Àtòkọ[순번]==8)fọ́nrán_aláìṣeéyípadà(순번);
    if(잘못됨)return 0;
    int ìgbéwọlé_kókó=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Unicode_iye(메소드목록[순번].Orúkọ,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Unicode_iye(메소드목록[순번].Orúkọ,"main")&&Unicode_iye(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)ìgbéwọlé_kókó=순번;
        if(Unicode_iye(메소드목록[순번].Orúkọ,"<clinit>"))초기값=순번;
    }
    if(ìgbéwọlé_kókó<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)ṣàkójọ_ìtumò_èdè_kọ̀ǹpútà_ìlànà(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(àayè_wúnrẹ̀n_aláìṣeéyípadà[순번]){
        unsigned kóòdù_ẹyọ_ọ̀rọ̀=àayè_wúnrẹ̀n_aláìṣeéyípadà[순번];if(kóòdù_ẹyọ_ọ̀rọ̀>=상수모음)return 0;
        if(Ìsàmì_Àtòkọ[kóòdù_ẹyọ_ọ̀rọ̀]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kóòdù_ẹyọ_ọ̀rọ̀]);else if(Ìsàmì_Àtòkọ[kóòdù_ẹyọ_ọ̀rọ̀]==8)내보내기("fields[%u]=(W)k%u;",순번,kóòdù_ẹyọ_ọ̀rọ̀);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",ìgbéwọlé_kókó);
    return 잘못됨?0:SMS;
}
