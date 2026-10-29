#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "dami.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char Tarin_bayani[16384];static unsigned Tsawo_Daraja,현재위치;static int kimiyar_bayanai_mara_ƙarfi;
static unsigned Nau_o_i_Jeri[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char SMS[65536];static unsigned girman_rubutu;
typedef struct {unsigned saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango,Suna,서술값,Sharadi_JERI,Girma,지역변수들,tara_Wurin_adana;} tsari_Mashigar_bayanai;
static tsari_Mashigar_bayanai 메소드목록[64];static unsigned 메소드개수;
static unsigned Sunan_fili[64],필드서술[64],Fili_Jurarre[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>Tsawo_Daraja||개수>Tsawo_Daraja-현재위치){kimiyar_bayanai_mara_ƙarfi=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned bayit_Tarin_bayani(void){unsigned 자료위치=가져오기(1);return kimiyar_bayanai_mara_ƙarfi?0:Tarin_bayani[자료위치];}
static unsigned 절반값(void){unsigned gamayyar_x=bayit_Tarin_bayani();return gamayyar_x<<8|bayit_Tarin_bayani();}
static uint32_t 가득참(void){uint32_t gamayyar_x=절반값();return gamayyar_x<<16|절반값();}
static int Ɗan_maƙalu_Daraja(unsigned 순번,const char*Zare_Tarin_bayani){return 순번>0&&순번<상수모음&&Nau_o_i_Jeri[순번]==1&&strlen(Zare_Tarin_bayani)==둘째값[순번]&&!memcmp(Tarin_bayani+첫째값[순번],Zare_Tarin_bayani,둘째값[순번]);}
static int 같음(unsigned gamayyar_x,unsigned Maɓallin_Y_Mai_tsarawa){return gamayyar_x>0&&gamayyar_x<상수모음&&Maɓallin_Y_Mai_tsarawa>0&&Maɓallin_Y_Mai_tsarawa<상수모음&&Nau_o_i_Jeri[gamayyar_x]==1&&Nau_o_i_Jeri[Maɓallin_Y_Mai_tsarawa]==1&&둘째값[gamayyar_x]==둘째값[Maɓallin_Y_Mai_tsarawa]&&!memcmp(Tarin_bayani+첫째값[gamayyar_x],Tarin_bayani+첫째값[Maɓallin_Y_Mai_tsarawa],둘째값[gamayyar_x]);}
static void 내보내기(const char*Fayil_Mashigar_bayanai,...){if(kimiyar_bayanai_mara_ƙarfi)return;va_list Tubalin_aiki_TSARI;va_start(Tubalin_aiki_TSARI,Fayil_Mashigar_bayanai);int 개수=vsnprintf(SMS+girman_rubutu,sizeof(SMS)-girman_rubutu,Fayil_Mashigar_bayanai,Tubalin_aiki_TSARI);va_end(Tubalin_aiki_TSARI);if(개수<0||(unsigned)개수>=sizeof(SMS)-girman_rubutu){kimiyar_bayanai_mara_ƙarfi=1;return;}girman_rubutu+=개수;}
static int 서술자(unsigned mai_ganewa_Daraja,int*결과){
    if(mai_ganewa_Daraja<1||mai_ganewa_Daraja>=상수모음||Nau_o_i_Jeri[mai_ganewa_Daraja]!=1)return -1;unsigned 자료위치=첫째값[mai_ganewa_Daraja],Ƙarshe_Sassautawa=자료위치+둘째값[mai_ganewa_Daraja];if(자료위치>=Ƙarshe_Sassautawa||Tarin_bayani[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<Ƙarshe_Sassautawa&&Tarin_bayani[자료위치]!=')'){
        unsigned Lambar_sirrin_harafi=Tarin_bayani[자료위치++];while(Lambar_sirrin_harafi=='['&&자료위치<Ƙarshe_Sassautawa)Lambar_sirrin_harafi=Tarin_bayani[자료위치++];
        if(Lambar_sirrin_harafi=='L'){while(자료위치<Ƙarshe_Sassautawa&&Tarin_bayani[자료위치]!=';')자료위치++;if(자료위치==Ƙarshe_Sassautawa)return -1;자료위치++;}
        else if(Lambar_sirrin_harafi!='I'&&Lambar_sirrin_harafi!='Z'&&Lambar_sirrin_harafi!='B'&&Lambar_sirrin_harafi!='C'&&Lambar_sirrin_harafi!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=Ƙarshe_Sassautawa||Tarin_bayani[자료위치++]!=')')return -1;*결과=Tarin_bayani[자료위치]=='V'?0:1;
    if(Tarin_bayani[자료위치]=='J'||Tarin_bayani[자료위치]=='D'||Tarin_bayani[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!kimiyar_bayanai_mara_ƙarfi;순번++){절반값();unsigned Girma=가득참();가져오기(Girma);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned mara_balaga_siga=절반값(),판번호=절반값();if(mara_balaga_siga||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!kimiyar_bayanai_mara_ƙarfi;순번++){
        Nau_o_i_Jeri[순번]=bayit_Tarin_bayani();switch(Nau_o_i_Jeri[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=bayit_Tarin_bayani();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Nau_o_i_Jeri[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Nau_o_i_Jeri[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!kimiyar_bayanai_mara_ƙarfi;순번++){
        unsigned saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango=절반값();Sunan_fili[순번]=절반값();필드서술[순번]=절반값();
        if(!(saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!kimiyar_bayanai_mara_ƙarfi;안쪽순번++){
            unsigned Suna=절반값(),Girma=가득참();
            if(Ɗan_maƙalu_Daraja(Suna,"ConstantValue")){if(Girma!=2)return -1;Fili_Jurarre[순번]=절반값();}
            else 가져오기(Girma);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!kimiyar_bayanai_mara_ƙarfi;순번++){
        tsari_Mashigar_bayanai*gungu_girma=메소드목록+순번;gungu_girma->saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango=절반값();gungu_girma->Suna=절반값();gungu_girma->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!kimiyar_bayanai_mara_ƙarfi;안쪽순번++){
            unsigned Suna=절반값(),Girma=가득참(),Tafiyar_da=현재위치;
            if(Girma>Tsawo_Daraja-현재위치)return -1;
            if(Ɗan_maƙalu_Daraja(Suna,"Code")){
                gungu_girma->tara_Wurin_adana=절반값();gungu_girma->지역변수들=절반값();gungu_girma->Girma=가득참();gungu_girma->Sharadi_JERI=가져오기(gungu_girma->Girma);
                if(gungu_girma->tara_Wurin_adana>128||gungu_girma->지역변수들>128||gungu_girma->Girma>8192||절반값())return -1;속성들();
            }else 가져오기(Girma);
            if(현재위치!=Tafiyar_da+Girma)return -1;
        }
        if(!Ɗan_maƙalu_Daraja(gungu_girma->Suna,"<init>")&&(!(gungu_girma->saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&8)||(gungu_girma->saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&(0x100|0x20))||!gungu_girma->Girma))return -1;
    }
    속성들();return kimiyar_bayanai_mara_ƙarfi||현재위치!=Tsawo_Daraja?-1:0;
}
static void Jurarre_Daraja(unsigned mai_ganewa_Daraja){
    if(!mai_ganewa_Daraja||mai_ganewa_Daraja>=상수모음){kimiyar_bayanai_mara_ƙarfi=1;return;}
    if(Nau_o_i_Jeri[mai_ganewa_Daraja]==3)내보내기("P(%uU);",첫째값[mai_ganewa_Daraja]);
    else if(Nau_o_i_Jeri[mai_ganewa_Daraja]==8)내보내기("P((W)k%u);",mai_ganewa_Daraja);else kimiyar_bayanai_mara_ƙarfi=1;
}
static void 호출(unsigned mai_ganewa_Daraja,int Mai_alaka_da_aikin_na_ura_na_boye_Kira){
    if(mai_ganewa_Daraja<1||mai_ganewa_Daraja>=상수모음||(Nau_o_i_Jeri[mai_ganewa_Daraja]!=10&&Nau_o_i_Jeri[mai_ganewa_Daraja]!=11)||첫째값[mai_ganewa_Daraja]<1||첫째값[mai_ganewa_Daraja]>=상수모음||Nau_o_i_Jeri[첫째값[mai_ganewa_Daraja]]!=7||둘째값[mai_ganewa_Daraja]<1||둘째값[mai_ganewa_Daraja]>=상수모음||Nau_o_i_Jeri[둘째값[mai_ganewa_Daraja]]!=12){kimiyar_bayanai_mara_ƙarfi=1;return;}
    unsigned mamallaki_abu=첫째값[첫째값[mai_ganewa_Daraja]],Suna=첫째값[둘째값[mai_ganewa_Daraja]],서술값=둘째값[둘째값[mai_ganewa_Daraja]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){kimiyar_bayanai_mara_ƙarfi=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(Mai_alaka_da_aikin_na_ura_na_boye_Kira)내보내기("Q();");
    if(!Mai_alaka_da_aikin_na_ura_na_boye_Kira&&같음(mamallaki_abu,첫째값[현재클래스])){
        unsigned gungu_girma=0;for(;gungu_girma<메소드개수;gungu_girma++)if(같음(Suna,메소드목록[gungu_girma].Suna)&&같음(서술값,메소드목록[gungu_girma].서술값))break;
        if(gungu_girma==메소드개수||!(메소드목록[gungu_girma].saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&8)){kimiyar_bayanai_mara_ƙarfi=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",gungu_girma);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((Mai_alaka_da_aikin_na_ura_na_boye_Kira&&Ɗan_maƙalu_Daraja(mamallaki_abu,"java/io/PrintStream")&& (Ɗan_maƙalu_Daraja(Suna,"print")||Ɗan_maƙalu_Daraja(Suna,"println")))||(!Mai_alaka_da_aikin_na_ura_na_boye_Kira&&Ɗan_maƙalu_Daraja(mamallaki_abu,"한국어/자체/출력"))){
        if(Ɗan_maƙalu_Daraja(서술값,"(I)V")&&(Ɗan_maƙalu_Daraja(Suna,"print")||Ɗan_maƙalu_Daraja(Suna,"println")||Ɗan_maƙalu_Daraja(Suna,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Ɗan_maƙalu_Daraja(Suna,"print")?0:1);return;}
        if(Ɗan_maƙalu_Daraja(서술값,"(Ljava/lang/String;)V")&&(Ɗan_maƙalu_Daraja(Suna,"print")||Ɗan_maƙalu_Daraja(Suna,"println")||Ɗan_maƙalu_Daraja(Suna,"Yi_Rubutu")||Ɗan_maƙalu_Daraja(Suna,"Rubuta_Layi"))){내보내기("jprint(x[0],0,%d);",Ɗan_maƙalu_Daraja(Suna,"print")||Ɗan_maƙalu_Daraja(Suna,"Yi_Rubutu")?0:1);return;}
        if(Ɗan_maƙalu_Daraja(서술값,"()V")&&Ɗan_maƙalu_Daraja(Suna,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!Mai_alaka_da_aikin_na_ura_na_boye_Kira&&Ɗan_maƙalu_Daraja(mamallaki_abu,"한국어/자체/Fayil")){
        if(Ɗan_maƙalu_Daraja(Suna,"Yi_Rubutu")&&Ɗan_maƙalu_Daraja(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Ɗan_maƙalu_Daraja(Suna,"Yi_Karatu")&&Ɗan_maƙalu_Daraja(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    kimiyar_bayanai_mara_ƙarfi=1;
}
static void Gina_tsari(unsigned 색인){
    tsari_Mashigar_bayanai*gungu_girma=메소드목록+색인;if(Ɗan_maƙalu_Daraja(gungu_girma->Suna,"<init>"))return;int 결과,개수=서술자(gungu_girma->서술값,&결과);if(개수<0){kimiyar_bayanai_mara_ƙarfi=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>gungu_girma->지역변수들){kimiyar_bayanai_mara_ƙarfi=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",gungu_girma->지역변수들?gungu_girma->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=Tsawo_Daraja;Tsawo_Daraja=gungu_girma->Sharadi_JERI+gungu_girma->Girma;현재위치=gungu_girma->Sharadi_JERI;
    while(현재위치<Tsawo_Daraja&&!kimiyar_bayanai_mara_ƙarfi){unsigned 명령위치=현재위치-gungu_girma->Sharadi_JERI,aiki_Daraja=bayit_Tarin_bayani();내보내기("L%u:;",명령위치);
        if(aiki_Daraja==0){}
        else if(aiki_Daraja==1)내보내기("P(0);");
        else if(aiki_Daraja>=2&&aiki_Daraja<=8)내보내기("P(%uU);",aiki_Daraja-3);
        else if(aiki_Daraja==16){int Daraja=(int8_t)bayit_Tarin_bayani();내보내기("P(%uU);",(unsigned)Daraja);}
        else if(aiki_Daraja==17){int Daraja=(int16_t)절반값();내보내기("P(%uU);",(unsigned)Daraja);}
        else if(aiki_Daraja==18||aiki_Daraja==19)Jurarre_Daraja(aiki_Daraja==18?bayit_Tarin_bayani():절반값());
        else if(aiki_Daraja==21||aiki_Daraja==25){unsigned 순번=bayit_Tarin_bayani();if(순번>=gungu_girma->지역변수들)kimiyar_bayanai_mara_ƙarfi=1;내보내기("P(v[%u]);",순번);}
        else if((aiki_Daraja>=26&&aiki_Daraja<=29)||(aiki_Daraja>=42&&aiki_Daraja<=45)){unsigned 순번=aiki_Daraja>=42?aiki_Daraja-42:aiki_Daraja-26;if(순번>=gungu_girma->지역변수들)kimiyar_bayanai_mara_ƙarfi=1;내보내기("P(v[%u]);",순번);}
        else if(aiki_Daraja==54||aiki_Daraja==58){unsigned 순번=bayit_Tarin_bayani();if(순번>=gungu_girma->지역변수들)kimiyar_bayanai_mara_ƙarfi=1;내보내기("v[%u]=Q();",순번);}
        else if((aiki_Daraja>=59&&aiki_Daraja<=62)||(aiki_Daraja>=75&&aiki_Daraja<=78)){unsigned 순번=aiki_Daraja>=75?aiki_Daraja-75:aiki_Daraja-59;if(순번>=gungu_girma->지역변수들)kimiyar_bayanai_mara_ƙarfi=1;내보내기("v[%u]=Q();",순번);}
        else if(aiki_Daraja==46||aiki_Daraja==50||aiki_Daraja==51||aiki_Daraja==52||aiki_Daraja==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(aiki_Daraja==79||aiki_Daraja==83||aiki_Daraja==84||aiki_Daraja==85||aiki_Daraja==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",aiki_Daraja==84?"(unsigned)(signed char)q":aiki_Daraja==85?"(unsigned short)q":aiki_Daraja==86?"(unsigned)(short)q":"q");
        else if(aiki_Daraja==87)내보내기("Q();");
        else if(aiki_Daraja==89)내보내기("q=Q();P(q);P(q);");
        else if(aiki_Daraja==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(aiki_Daraja==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(aiki_Daraja==96||aiki_Daraja==100||aiki_Daraja==104||aiki_Daraja==120||aiki_Daraja==124||aiki_Daraja==126||aiki_Daraja==128||aiki_Daraja==130){const char*Juyar_da_bayanai_zuwa_lamba_Daraja=aiki_Daraja==96?"+":aiki_Daraja==100?"-":aiki_Daraja==104?"*":aiki_Daraja==120?"<<":aiki_Daraja==124?">>":aiki_Daraja==126?"&":aiki_Daraja==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",Juyar_da_bayanai_zuwa_lamba_Daraja,aiki_Daraja==120||aiki_Daraja==124?"%32":"");}
        else if(aiki_Daraja==108||aiki_Daraja==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",aiki_Daraja==112);
        else if(aiki_Daraja==116)내보내기("P(0U-(unsigned)Q());");
        else if(aiki_Daraja==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(aiki_Daraja==132){unsigned 순번=bayit_Tarin_bayani();int 차이=(int8_t)bayit_Tarin_bayani();if(순번>=gungu_girma->지역변수들)kimiyar_bayanai_mara_ƙarfi=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(aiki_Daraja>=145&&aiki_Daraja<=147)내보내기("P((unsigned)(%s)Q());",aiki_Daraja==145?"signed char":aiki_Daraja==146?"unsigned short":"short");
        else if(aiki_Daraja>=153&&aiki_Daraja<=166){int tageti=(int)명령위치+(int16_t)절반값();const char*Kwatantawa_Daraja[]={"==","!=","<",">=",">","<="};if(tageti<0||tageti>=(int)gungu_girma->Girma){kimiyar_bayanai_mara_ƙarfi=1;break;}if(aiki_Daraja<159)내보내기("if((int)Q()%s0)goto L%d;",Kwatantawa_Daraja[aiki_Daraja-153],tageti);else if(aiki_Daraja<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Kwatantawa_Daraja[aiki_Daraja-159],tageti);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",aiki_Daraja==165?"==":"!=",tageti);}
        else if(aiki_Daraja==167){int tageti=(int)명령위치+(int16_t)절반값();if(tageti<0||tageti>=(int)gungu_girma->Girma)kimiyar_bayanai_mara_ƙarfi=1;내보내기("goto L%d;",tageti);}
        else if(aiki_Daraja==172||aiki_Daraja==176)내보내기("return Q();");else if(aiki_Daraja==177)내보내기("return 0;");
        else if(aiki_Daraja==178||aiki_Daraja==179){unsigned mai_ganewa_Daraja=절반값();if(mai_ganewa_Daraja<1||mai_ganewa_Daraja>=상수모음||Nau_o_i_Jeri[mai_ganewa_Daraja]!=9||첫째값[mai_ganewa_Daraja]>=상수모음||둘째값[mai_ganewa_Daraja]>=상수모음||Nau_o_i_Jeri[첫째값[mai_ganewa_Daraja]]!=7||Nau_o_i_Jeri[둘째값[mai_ganewa_Daraja]]!=12){kimiyar_bayanai_mara_ƙarfi=1;break;}unsigned mamallaki_abu=첫째값[첫째값[mai_ganewa_Daraja]],Suna=첫째값[둘째값[mai_ganewa_Daraja]],서술값=둘째값[둘째값[mai_ganewa_Daraja]];
            if(aiki_Daraja==178&&Ɗan_maƙalu_Daraja(mamallaki_abu,"java/lang/System")&&Ɗan_maƙalu_Daraja(Suna,"out")&&Ɗan_maƙalu_Daraja(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Fayil_Mashigar_bayanai=0;while(Fayil_Mashigar_bayanai<필드개수&&(!같음(Suna,Sunan_fili[Fayil_Mashigar_bayanai])||!같음(서술값,필드서술[Fayil_Mashigar_bayanai])))Fayil_Mashigar_bayanai++;if(!같음(mamallaki_abu,첫째값[현재클래스])||Fayil_Mashigar_bayanai==필드개수){kimiyar_bayanai_mara_ƙarfi=1;break;}내보내기(aiki_Daraja==178?"P(fields[%u]);":"fields[%u]=Q();",Fayil_Mashigar_bayanai);}}
        else if(aiki_Daraja==182||aiki_Daraja==184)호출(절반값(),aiki_Daraja==182);
        else if(aiki_Daraja==188){unsigned rubuta_ɓangare=bayit_Tarin_bayani();if(rubuta_ɓangare!=4&&rubuta_ɓangare!=5&&rubuta_ɓangare!=8&&rubuta_ɓangare!=9&&rubuta_ɓangare!=10)kimiyar_bayanai_mara_ƙarfi=1;내보내기("P(jarray((int)Q()));");}
        else if(aiki_Daraja==190)내보내기("P(jlength(Q()));");
        else if(aiki_Daraja==198||aiki_Daraja==199){int tageti=(int)명령위치+(int16_t)절반값();if(tageti<0||tageti>=(int)gungu_girma->Girma)kimiyar_bayanai_mara_ƙarfi=1;내보내기("if(Q()%s0)goto L%d;",aiki_Daraja==198?"==":"!=",tageti);}
        else kimiyar_bayanai_mara_ƙarfi=1;
        if(kimiyar_bayanai_mara_ƙarfi)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,aiki_Daraja,명령위치);
        내보내기("\n");
    }
    Tsawo_Daraja=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned Zare_darasi(unsigned *자료위치,unsigned Ƙarshe_Sassautawa){
    if(*자료위치>=Ƙarshe_Sassautawa){kimiyar_bayanai_mara_ƙarfi=1;return 0;}unsigned Lambar_sirrin_harafi=Tarin_bayani[(*자료위치)++];
    if(Lambar_sirrin_harafi<128)return Lambar_sirrin_harafi;
    unsigned 개수=Lambar_sirrin_harafi>=0xc0&&Lambar_sirrin_harafi<=0xdf?1:Lambar_sirrin_harafi>=0xe0&&Lambar_sirrin_harafi<=0xef?2:3;
    if(개수==3||개수>Ƙarshe_Sassautawa-*자료위치){kimiyar_bayanai_mara_ƙarfi=1;return 0;}unsigned Daraja=Lambar_sirrin_harafi&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=Tarin_bayani[(*자료위치)++];if((다음&0xc0)!=0x80)kimiyar_bayanai_mara_ƙarfi=1;Daraja=Daraja<<6|(다음&63);}
    if((개수==1&&Daraja<128&&Daraja!=0)||(개수==2&&Daraja<2048))kimiyar_bayanai_mara_ƙarfi=1;return Daraja;
}
static void Zare_Jurarre(unsigned mai_ganewa_Daraja){
    unsigned 부호없는값=첫째값[mai_ganewa_Daraja];if(부호없는값<1||부호없는값>=상수모음||Nau_o_i_Jeri[부호없는값]!=1){kimiyar_bayanai_mara_ƙarfi=1;return;}내보내기("static const unsigned char k%u[]={",mai_ganewa_Daraja);
    unsigned 자료위치=첫째값[부호없는값],Ƙarshe_Sassautawa=자료위치+둘째값[부호없는값];
    while(자료위치<Ƙarshe_Sassautawa&&!kimiyar_bayanai_mara_ƙarfi){unsigned Lambar_sirrin_harafi=Zare_darasi(&자료위치,Ƙarshe_Sassautawa);
        if(Lambar_sirrin_harafi>=0xd800&&Lambar_sirrin_harafi<=0xdbff){unsigned 낮은부분=Zare_darasi(&자료위치,Ƙarshe_Sassautawa);if(낮은부분<0xdc00||낮은부분>0xdfff){kimiyar_bayanai_mara_ƙarfi=1;break;}Lambar_sirrin_harafi=0x10000+((Lambar_sirrin_harafi-0xd800)<<10)+낮은부분-0xdc00;}
        else if(Lambar_sirrin_harafi>=0xdc00&&Lambar_sirrin_harafi<=0xdfff){kimiyar_bayanai_mara_ƙarfi=1;break;}
        if(!Lambar_sirrin_harafi){printf("jaot: embedded NUL string needs JVM mode\n");kimiyar_bayanai_mara_ƙarfi=1;break;}
        if(Lambar_sirrin_harafi<128)내보내기("%u,",Lambar_sirrin_harafi);
        else{unsigned 개수=Lambar_sirrin_harafi<2048?2:Lambar_sirrin_harafi<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(Lambar_sirrin_harafi>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((Lambar_sirrin_harafi>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Suna){
    size_t 개수=strlen(Suna);
    if(개수>4&&!strcmp(Suna+개수-4,".jar")){
        if(꾸러미열기(Suna)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Hanyar_shiga[256];const char*Mashigar_bayanai_tsari=꾸러미진입클래스();개수=strlen(Mashigar_bayanai_tsari);if(개수+6>=sizeof(Hanyar_shiga))return 0;
        for(unsigned 순번=0;순번<개수;순번++)Hanyar_shiga[순번]=Mashigar_bayanai_tsari[순번]=='.'?'/':Mashigar_bayanai_tsari[순번];strcpy(Hanyar_shiga+개수,".class");int 항목수=꾸러미읽기(Hanyar_shiga,Tarin_bayani,sizeof(Tarin_bayani));if(항목수<0)return 0;Tsawo_Daraja=항목수;
    }else{intptr_t Fayil_Mariki=사용자호출(3,(uintptr_t)Suna,0,0,0,0,0);if(Fayil_Mariki<0)return 0;intptr_t 항목수=사용자호출(9,Fayil_Mariki,0,0,0,0,0);if(항목수<0||항목수>sizeof(Tarin_bayani)){사용자호출(4,Fayil_Mariki,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,Fayil_Mariki,(uintptr_t)Tarin_bayani,항목수,0,0,0);사용자호출(4,Fayil_Mariki,0,0,0,0,0);if(받은수!=항목수)return 0;Tsawo_Daraja=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!kimiyar_bayanai_mara_ƙarfi;순번++)if(Nau_o_i_Jeri[순번]==8)Zare_Jurarre(순번);
    if(kimiyar_bayanai_mara_ƙarfi)return 0;
    int Mashigar_bayanai_maki=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Ɗan_maƙalu_Daraja(메소드목록[순번].Suna,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(Ɗan_maƙalu_Daraja(메소드목록[순번].Suna,"main")&&Ɗan_maƙalu_Daraja(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango&9)==9)Mashigar_bayanai_maki=순번;
        if(Ɗan_maƙalu_Daraja(메소드목록[순번].Suna,"<clinit>"))초기값=순번;
    }
    if(Mashigar_bayanai_maki<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!kimiyar_bayanai_mara_ƙarfi;순번++)Gina_tsari(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(Fili_Jurarre[순번]){
        unsigned Lambar_sirrin_harafi=Fili_Jurarre[순번];if(Lambar_sirrin_harafi>=상수모음)return 0;
        if(Nau_o_i_Jeri[Lambar_sirrin_harafi]==3)내보내기("fields[%u]=%uU;",순번,첫째값[Lambar_sirrin_harafi]);else if(Nau_o_i_Jeri[Lambar_sirrin_harafi]==8)내보내기("fields[%u]=(W)k%u;",순번,Lambar_sirrin_harafi);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",Mashigar_bayanai_maki);
    return kimiyar_bayanai_mara_ƙarfi?0:SMS;
}
