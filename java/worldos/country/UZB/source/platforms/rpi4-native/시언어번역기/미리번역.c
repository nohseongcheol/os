#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "to_plam.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char ma_lumotlar[16384];static unsigned uzunlik_VALUE,현재위치;static int 잘못됨;
static unsigned Teglar_Ro_yxat[512],첫째값[512],SECOND_VALUE[512],konstanta_pul,현재클래스;
static char Matn[65536];static unsigned matn_o_lchami;
typedef struct {unsigned tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati,Nomi,서술값,qo_llanma_SEQUENCE,Hajmi,지역변수들,Stack_Xotira;} uslub_kiritish;
static uslub_kiritish 메소드목록[64];static unsigned 메소드개수;
static unsigned maydon_nomi[64],필드서술[64],ma_lumotlar_maydoni_konstanta[64],필드개수;
static unsigned TAKE_VALUE(unsigned element_COUNT){if(현재위치>uzunlik_VALUE||element_COUNT>uzunlik_VALUE-현재위치){잘못됨=1;return 0;}unsigned ma_lumotlar_holat=현재위치;현재위치+=element_COUNT;return ma_lumotlar_holat;}
static unsigned bayt_ma_lumotlar(void){unsigned ma_lumotlar_holat=TAKE_VALUE(1);return 잘못됨?0:ma_lumotlar[ma_lumotlar_holat];}
static unsigned 절반값(void){unsigned x_koordinata=bayt_ma_lumotlar();return x_koordinata<<8|bayt_ma_lumotlar();}
static uint32_t 가득참(void){uint32_t x_koordinata=절반값();return x_koordinata<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*satr_ma_lumotlar){return 순번>0&&순번<konstanta_pul&&Teglar_Ro_yxat[순번]==1&&strlen(satr_ma_lumotlar)==SECOND_VALUE[순번]&&!memcmp(ma_lumotlar+첫째값[순번],satr_ma_lumotlar,SECOND_VALUE[순번]);}
static int 같음(unsigned x_koordinata,unsigned Y_tugmasi_koordinat){return x_koordinata>0&&x_koordinata<konstanta_pul&&Y_tugmasi_koordinat>0&&Y_tugmasi_koordinat<konstanta_pul&&Teglar_Ro_yxat[x_koordinata]==1&&Teglar_Ro_yxat[Y_tugmasi_koordinat]==1&&SECOND_VALUE[x_koordinata]==SECOND_VALUE[Y_tugmasi_koordinat]&&!memcmp(ma_lumotlar+첫째값[x_koordinata],ma_lumotlar+첫째값[Y_tugmasi_koordinat],SECOND_VALUE[x_koordinata]);}
static void 내보내기(const char*fayl_kiritish,...){if(잘못됨)return;va_list dalil_ARRAY;va_start(dalil_ARRAY,fayl_kiritish);int element_COUNT=vsnprintf(Matn+matn_o_lchami,sizeof(Matn)-matn_o_lchami,fayl_kiritish,dalil_ARRAY);va_end(dalil_ARRAY);if(element_COUNT<0||(unsigned)element_COUNT>=sizeof(Matn)-matn_o_lchami){잘못됨=1;return;}matn_o_lchami+=element_COUNT;}
static int 서술자(unsigned identifikator_VALUE,int*o_lchov){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_pul||Teglar_Ro_yxat[identifikator_VALUE]!=1)return -1;unsigned ma_lumotlar_holat=첫째값[identifikator_VALUE],to_xtatmoq_OFFSET=ma_lumotlar_holat+SECOND_VALUE[identifikator_VALUE];if(ma_lumotlar_holat>=to_xtatmoq_OFFSET||ma_lumotlar[ma_lumotlar_holat++]!='(')return -1;int kiritish_COUNT=0;
    while(ma_lumotlar_holat<to_xtatmoq_OFFSET&&ma_lumotlar[ma_lumotlar_holat]!=')'){
        unsigned belgi_kodi=ma_lumotlar[ma_lumotlar_holat++];while(belgi_kodi=='['&&ma_lumotlar_holat<to_xtatmoq_OFFSET)belgi_kodi=ma_lumotlar[ma_lumotlar_holat++];
        if(belgi_kodi=='L'){while(ma_lumotlar_holat<to_xtatmoq_OFFSET&&ma_lumotlar[ma_lumotlar_holat]!=';')ma_lumotlar_holat++;if(ma_lumotlar_holat==to_xtatmoq_OFFSET)return -1;ma_lumotlar_holat++;}
        else if(belgi_kodi!='I'&&belgi_kodi!='Z'&&belgi_kodi!='B'&&belgi_kodi!='C'&&belgi_kodi!='S')return -1;
        if(++kiritish_COUNT>16)return -1;
    }
    if(ma_lumotlar_holat+1>=to_xtatmoq_OFFSET||ma_lumotlar[ma_lumotlar_holat++]!=')')return -1;*o_lchov=ma_lumotlar[ma_lumotlar_holat]=='V'?0:1;
    if(ma_lumotlar[ma_lumotlar_holat]=='J'||ma_lumotlar[ma_lumotlar_holat]=='D'||ma_lumotlar[ma_lumotlar_holat]=='F')return -1;return kiritish_COUNT;
}
static void 속성들(void){unsigned element_COUNT=절반값();for(unsigned 순번=0;순번<element_COUNT&&!잘못됨;순번++){절반값();unsigned Hajmi=가득참();TAKE_VALUE(Hajmi);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned voyaga_yetmagan_versiya=절반값(),판번호=절반값();if(voyaga_yetmagan_versiya||판번호<45||판번호>52)return -1;
    konstanta_pul=절반값();if(konstanta_pul<1||konstanta_pul>512)return -1;
    for(unsigned 순번=1;순번<konstanta_pul&&!잘못됨;순번++){
        Teglar_Ro_yxat[순번]=bayt_ma_lumotlar();switch(Teglar_Ro_yxat[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstanta_pul)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bayt_ma_lumotlar();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=konstanta_pul||Teglar_Ro_yxat[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=konstanta_pul||Teglar_Ro_yxat[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati=절반값();maydon_nomi[순번]=절반값();필드서술[순번]=절반값();
        if(!(tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&8))return -1;
        unsigned kiritish_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<kiritish_COUNT&&!잘못됨;안쪽순번++){
            unsigned Nomi=절반값(),Hajmi=가득참();
            if(UNICODE_VALUE(Nomi,"ConstantValue")){if(Hajmi!=2)return -1;ma_lumotlar_maydoni_konstanta[순번]=절반값();}
            else TAKE_VALUE(Hajmi);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        uslub_kiritish*Guruh_o_lcham=메소드목록+순번;Guruh_o_lcham->tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati=절반값();Guruh_o_lcham->Nomi=절반값();Guruh_o_lcham->서술값=절반값();unsigned kiritish_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<kiritish_COUNT&&!잘못됨;안쪽순번++){
            unsigned Nomi=절반값(),Hajmi=가득참(),Bajarish=현재위치;
            if(Hajmi>uzunlik_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(Nomi,"Code")){
                Guruh_o_lcham->Stack_Xotira=절반값();Guruh_o_lcham->지역변수들=절반값();Guruh_o_lcham->Hajmi=가득참();Guruh_o_lcham->qo_llanma_SEQUENCE=TAKE_VALUE(Guruh_o_lcham->Hajmi);
                if(Guruh_o_lcham->Stack_Xotira>128||Guruh_o_lcham->지역변수들>128||Guruh_o_lcham->Hajmi>8192||절반값())return -1;속성들();
            }else TAKE_VALUE(Hajmi);
            if(현재위치!=Bajarish+Hajmi)return -1;
        }
        if(!UNICODE_VALUE(Guruh_o_lcham->Nomi,"<init>")&&(!(Guruh_o_lcham->tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&8)||(Guruh_o_lcham->tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&(0x100|0x20))||!Guruh_o_lcham->Hajmi))return -1;
    }
    속성들();return 잘못됨||현재위치!=uzunlik_VALUE?-1:0;
}
static void konstanta_VALUE(unsigned identifikator_VALUE){
    if(!identifikator_VALUE||identifikator_VALUE>=konstanta_pul){잘못됨=1;return;}
    if(Teglar_Ro_yxat[identifikator_VALUE]==3)내보내기("P(%uU);",첫째값[identifikator_VALUE]);
    else if(Teglar_Ro_yxat[identifikator_VALUE]==8)내보내기("P((W)k%u);",identifikator_VALUE);else 잘못됨=1;
}
static void 호출(unsigned identifikator_VALUE,int virtual_CALL){
    if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_pul||(Teglar_Ro_yxat[identifikator_VALUE]!=10&&Teglar_Ro_yxat[identifikator_VALUE]!=11)||첫째값[identifikator_VALUE]<1||첫째값[identifikator_VALUE]>=konstanta_pul||Teglar_Ro_yxat[첫째값[identifikator_VALUE]]!=7||SECOND_VALUE[identifikator_VALUE]<1||SECOND_VALUE[identifikator_VALUE]>=konstanta_pul||Teglar_Ro_yxat[SECOND_VALUE[identifikator_VALUE]]!=12){잘못됨=1;return;}
    unsigned egasi_obyekt=첫째값[첫째값[identifikator_VALUE]],Nomi=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];int o_lchov=0,element_COUNT=서술자(서술값,&o_lchov);if(element_COUNT<0){잘못됨=1;return;}
    for(int 순번=element_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtual_CALL)내보내기("Q();");
    if(!virtual_CALL&&같음(egasi_obyekt,첫째값[현재클래스])){
        unsigned Guruh_o_lcham=0;for(;Guruh_o_lcham<메소드개수;Guruh_o_lcham++)if(같음(Nomi,메소드목록[Guruh_o_lcham].Nomi)&&같음(서술값,메소드목록[Guruh_o_lcham].서술값))break;
        if(Guruh_o_lcham==메소드개수||!(메소드목록[Guruh_o_lcham].tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&8)){잘못됨=1;return;}
        if(o_lchov)내보내기("P(");내보내기("m%u(",Guruh_o_lcham);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(o_lchov?"));":" );");return;
    }
    if((virtual_CALL&&UNICODE_VALUE(egasi_obyekt,"java/io/PrintStream")&& (UNICODE_VALUE(Nomi,"print")||UNICODE_VALUE(Nomi,"println")))||(!virtual_CALL&&UNICODE_VALUE(egasi_obyekt,"한국어/자체/출력"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Nomi,"print")||UNICODE_VALUE(Nomi,"println")||UNICODE_VALUE(Nomi,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Nomi,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Nomi,"print")||UNICODE_VALUE(Nomi,"println")||UNICODE_VALUE(Nomi,"Yozish")||UNICODE_VALUE(Nomi,"yozmoq_satr"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Nomi,"print")||UNICODE_VALUE(Nomi,"Yozish")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Nomi,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtual_CALL&&UNICODE_VALUE(egasi_obyekt,"한국어/자체/Fayl")){
        if(UNICODE_VALUE(Nomi,"Yozish")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Nomi,"Oʻqish")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void yig_moq_uslub(unsigned LOOKUP_INDEX){
    uslub_kiritish*Guruh_o_lcham=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Guruh_o_lcham->Nomi,"<init>"))return;int o_lchov,element_COUNT=서술자(Guruh_o_lcham->서술값,&o_lchov);if(element_COUNT<0){잘못됨=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<element_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!element_COUNT)내보내기("void");
    if((unsigned)element_COUNT>Guruh_o_lcham->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Guruh_o_lcham->지역변수들?Guruh_o_lcham->지역변수들:1);for(int 순번=0;순번<element_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=uzunlik_VALUE;uzunlik_VALUE=Guruh_o_lcham->qo_llanma_SEQUENCE+Guruh_o_lcham->Hajmi;현재위치=Guruh_o_lcham->qo_llanma_SEQUENCE;
    while(현재위치<uzunlik_VALUE&&!잘못됨){unsigned buyruq_holat=현재위치-Guruh_o_lcham->qo_llanma_SEQUENCE,jarrohlik_VALUE=bayt_ma_lumotlar();내보내기("L%u:;",buyruq_holat);
        if(jarrohlik_VALUE==0){}
        else if(jarrohlik_VALUE==1)내보내기("P(0);");
        else if(jarrohlik_VALUE>=2&&jarrohlik_VALUE<=8)내보내기("P(%uU);",jarrohlik_VALUE-3);
        else if(jarrohlik_VALUE==16){int VALUE=(int8_t)bayt_ma_lumotlar();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(jarrohlik_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(jarrohlik_VALUE==18||jarrohlik_VALUE==19)konstanta_VALUE(jarrohlik_VALUE==18?bayt_ma_lumotlar():절반값());
        else if(jarrohlik_VALUE==21||jarrohlik_VALUE==25){unsigned 순번=bayt_ma_lumotlar();if(순번>=Guruh_o_lcham->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((jarrohlik_VALUE>=26&&jarrohlik_VALUE<=29)||(jarrohlik_VALUE>=42&&jarrohlik_VALUE<=45)){unsigned 순번=jarrohlik_VALUE>=42?jarrohlik_VALUE-42:jarrohlik_VALUE-26;if(순번>=Guruh_o_lcham->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(jarrohlik_VALUE==54||jarrohlik_VALUE==58){unsigned 순번=bayt_ma_lumotlar();if(순번>=Guruh_o_lcham->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((jarrohlik_VALUE>=59&&jarrohlik_VALUE<=62)||(jarrohlik_VALUE>=75&&jarrohlik_VALUE<=78)){unsigned 순번=jarrohlik_VALUE>=75?jarrohlik_VALUE-75:jarrohlik_VALUE-59;if(순번>=Guruh_o_lcham->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(jarrohlik_VALUE==46||jarrohlik_VALUE==50||jarrohlik_VALUE==51||jarrohlik_VALUE==52||jarrohlik_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(jarrohlik_VALUE==79||jarrohlik_VALUE==83||jarrohlik_VALUE==84||jarrohlik_VALUE==85||jarrohlik_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",jarrohlik_VALUE==84?"(unsigned)(signed char)q":jarrohlik_VALUE==85?"(unsigned short)q":jarrohlik_VALUE==86?"(unsigned)(short)q":"q");
        else if(jarrohlik_VALUE==87)내보내기("Q();");
        else if(jarrohlik_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(jarrohlik_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(jarrohlik_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(jarrohlik_VALUE==96||jarrohlik_VALUE==100||jarrohlik_VALUE==104||jarrohlik_VALUE==120||jarrohlik_VALUE==124||jarrohlik_VALUE==126||jarrohlik_VALUE==128||jarrohlik_VALUE==130){const char*kodlash_VALUE=jarrohlik_VALUE==96?"+":jarrohlik_VALUE==100?"-":jarrohlik_VALUE==104?"*":jarrohlik_VALUE==120?"<<":jarrohlik_VALUE==124?">>":jarrohlik_VALUE==126?"&":jarrohlik_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodlash_VALUE,jarrohlik_VALUE==120||jarrohlik_VALUE==124?"%32":"");}
        else if(jarrohlik_VALUE==108||jarrohlik_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",jarrohlik_VALUE==112);
        else if(jarrohlik_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(jarrohlik_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(jarrohlik_VALUE==132){unsigned 순번=bayt_ma_lumotlar();int 차이=(int8_t)bayt_ma_lumotlar();if(순번>=Guruh_o_lcham->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(jarrohlik_VALUE>=145&&jarrohlik_VALUE<=147)내보내기("P((unsigned)(%s)Q());",jarrohlik_VALUE==145?"signed char":jarrohlik_VALUE==146?"unsigned short":"short");
        else if(jarrohlik_VALUE>=153&&jarrohlik_VALUE<=166){int nishon=(int)buyruq_holat+(int16_t)절반값();const char*Taqqoslama_VALUE[]={"==","!=","<",">=",">","<="};if(nishon<0||nishon>=(int)Guruh_o_lcham->Hajmi){잘못됨=1;break;}if(jarrohlik_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Taqqoslama_VALUE[jarrohlik_VALUE-153],nishon);else if(jarrohlik_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Taqqoslama_VALUE[jarrohlik_VALUE-159],nishon);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",jarrohlik_VALUE==165?"==":"!=",nishon);}
        else if(jarrohlik_VALUE==167){int nishon=(int)buyruq_holat+(int16_t)절반값();if(nishon<0||nishon>=(int)Guruh_o_lcham->Hajmi)잘못됨=1;내보내기("goto L%d;",nishon);}
        else if(jarrohlik_VALUE==172||jarrohlik_VALUE==176)내보내기("return Q();");else if(jarrohlik_VALUE==177)내보내기("return 0;");
        else if(jarrohlik_VALUE==178||jarrohlik_VALUE==179){unsigned identifikator_VALUE=절반값();if(identifikator_VALUE<1||identifikator_VALUE>=konstanta_pul||Teglar_Ro_yxat[identifikator_VALUE]!=9||첫째값[identifikator_VALUE]>=konstanta_pul||SECOND_VALUE[identifikator_VALUE]>=konstanta_pul||Teglar_Ro_yxat[첫째값[identifikator_VALUE]]!=7||Teglar_Ro_yxat[SECOND_VALUE[identifikator_VALUE]]!=12){잘못됨=1;break;}unsigned egasi_obyekt=첫째값[첫째값[identifikator_VALUE]],Nomi=첫째값[SECOND_VALUE[identifikator_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[identifikator_VALUE]];
            if(jarrohlik_VALUE==178&&UNICODE_VALUE(egasi_obyekt,"java/lang/System")&&UNICODE_VALUE(Nomi,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fayl_kiritish=0;while(fayl_kiritish<필드개수&&(!같음(Nomi,maydon_nomi[fayl_kiritish])||!같음(서술값,필드서술[fayl_kiritish])))fayl_kiritish++;if(!같음(egasi_obyekt,첫째값[현재클래스])||fayl_kiritish==필드개수){잘못됨=1;break;}내보내기(jarrohlik_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",fayl_kiritish);}}
        else if(jarrohlik_VALUE==182||jarrohlik_VALUE==184)호출(절반값(),jarrohlik_VALUE==182);
        else if(jarrohlik_VALUE==188){unsigned TYPE_toifa=bayt_ma_lumotlar();if(TYPE_toifa!=4&&TYPE_toifa!=5&&TYPE_toifa!=8&&TYPE_toifa!=9&&TYPE_toifa!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(jarrohlik_VALUE==190)내보내기("P(jlength(Q()));");
        else if(jarrohlik_VALUE==198||jarrohlik_VALUE==199){int nishon=(int)buyruq_holat+(int16_t)절반값();if(nishon<0||nishon>=(int)Guruh_o_lcham->Hajmi)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",jarrohlik_VALUE==198?"==":"!=",nishon);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,jarrohlik_VALUE,buyruq_holat);
        내보내기("\n");
    }
    uzunlik_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned satr_dars(unsigned *ma_lumotlar_holat,unsigned to_xtatmoq_OFFSET){
    if(*ma_lumotlar_holat>=to_xtatmoq_OFFSET){잘못됨=1;return 0;}unsigned belgi_kodi=ma_lumotlar[(*ma_lumotlar_holat)++];
    if(belgi_kodi<128)return belgi_kodi;
    unsigned element_COUNT=belgi_kodi>=0xc0&&belgi_kodi<=0xdf?1:belgi_kodi>=0xe0&&belgi_kodi<=0xef?2:3;
    if(element_COUNT==3||element_COUNT>to_xtatmoq_OFFSET-*ma_lumotlar_holat){잘못됨=1;return 0;}unsigned VALUE=belgi_kodi&((1u<<(6-element_COUNT))-1);
    for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned Keyingi_element=ma_lumotlar[(*ma_lumotlar_holat)++];if((Keyingi_element&0xc0)!=0x80)잘못됨=1;VALUE=VALUE<<6|(Keyingi_element&63);}
    if((element_COUNT==1&&VALUE<128&&VALUE!=0)||(element_COUNT==2&&VALUE<2048))잘못됨=1;return VALUE;
}
static void satr_konstanta(unsigned identifikator_VALUE){
    unsigned 부호없는값=첫째값[identifikator_VALUE];if(부호없는값<1||부호없는값>=konstanta_pul||Teglar_Ro_yxat[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",identifikator_VALUE);
    unsigned ma_lumotlar_holat=첫째값[부호없는값],to_xtatmoq_OFFSET=ma_lumotlar_holat+SECOND_VALUE[부호없는값];
    while(ma_lumotlar_holat<to_xtatmoq_OFFSET&&!잘못됨){unsigned belgi_kodi=satr_dars(&ma_lumotlar_holat,to_xtatmoq_OFFSET);
        if(belgi_kodi>=0xd800&&belgi_kodi<=0xdbff){unsigned 낮은부분=satr_dars(&ma_lumotlar_holat,to_xtatmoq_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}belgi_kodi=0x10000+((belgi_kodi-0xd800)<<10)+낮은부분-0xdc00;}
        else if(belgi_kodi>=0xdc00&&belgi_kodi<=0xdfff){잘못됨=1;break;}
        if(!belgi_kodi){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(belgi_kodi<128)내보내기("%u,",belgi_kodi);
        else{unsigned element_COUNT=belgi_kodi<2048?2:belgi_kodi<65536?3:4;내보내기("%u,",(element_COUNT==2?0xc0:element_COUNT==3?0xe0:0xf0)|(belgi_kodi>>(6*(element_COUNT-1))));for(unsigned 순번=element_COUNT-1;순번;순번--)내보내기("%u,",0x80|((belgi_kodi>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nomi){
    size_t element_COUNT=strlen(Nomi);
    if(element_COUNT>4&&!strcmp(Nomi+element_COUNT-4,".jar")){
        if(꾸러미열기(Nomi)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char yo_l[256];const char*kiritish_uslub=꾸러미진입클래스();element_COUNT=strlen(kiritish_uslub);if(element_COUNT+6>=sizeof(yo_l))return 0;
        for(unsigned 순번=0;순번<element_COUNT;순번++)yo_l[순번]=kiritish_uslub[순번]=='.'?'/':kiritish_uslub[순번];strcpy(yo_l+element_COUNT,".class");int kiritish_COUNT=꾸러미읽기(yo_l,ma_lumotlar,sizeof(ma_lumotlar));if(kiritish_COUNT<0)return 0;uzunlik_VALUE=kiritish_COUNT;
    }else{intptr_t fayl_deskriptor=사용자호출(3,(uintptr_t)Nomi,0,0,0,0,0);if(fayl_deskriptor<0)return 0;intptr_t kiritish_COUNT=사용자호출(9,fayl_deskriptor,0,0,0,0,0);if(kiritish_COUNT<0||kiritish_COUNT>sizeof(ma_lumotlar)){사용자호출(4,fayl_deskriptor,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,fayl_deskriptor,(uintptr_t)ma_lumotlar,kiritish_COUNT,0,0,0);사용자호출(4,fayl_deskriptor,0,0,0,0,0);if(RECEIVED_COUNT!=kiritish_COUNT)return 0;uzunlik_VALUE=kiritish_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstanta_pul&&!잘못됨;순번++)if(Teglar_Ro_yxat[순번]==8)satr_konstanta(순번);
    if(잘못됨)return 0;
    int kiritish_nuqta=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Nomi,"<init>")){
        int o_lchov,kiritish_COUNT=서술자(메소드목록[순번].서술값,&o_lchov);if(kiritish_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<kiritish_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!kiritish_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Nomi,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati&9)==9)kiritish_nuqta=순번;
        if(UNICODE_VALUE(메소드목록[순번].Nomi,"<clinit>"))초기값=순번;
    }
    if(kiritish_nuqta<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)yig_moq_uslub(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(ma_lumotlar_maydoni_konstanta[순번]){
        unsigned belgi_kodi=ma_lumotlar_maydoni_konstanta[순번];if(belgi_kodi>=konstanta_pul)return 0;
        if(Teglar_Ro_yxat[belgi_kodi]==3)내보내기("fields[%u]=%uU;",순번,첫째값[belgi_kodi]);else if(Teglar_Ro_yxat[belgi_kodi]==8)내보내기("fields[%u]=(W)k%u;",순번,belgi_kodi);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",kiritish_nuqta);
    return 잘못됨?0:Matn;
}
