#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "pūpū.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char raraunga[16384];static unsigned roa_uara,현재위치;static int 잘못됨;
static unsigned Kāwai_Rārangi[512],첫째값[512],SECOND_uara[512],상수모음,현재클래스;
static char Ngā_kupu[65536];static unsigned rahinga_kuputuhi;
typedef struct {unsigned 설정비트,Ingoa,서술값,tohutohu_SEQUENCE,rahi,지역변수들,Huinga_Rokiroki;} aratuka_tāurunga;
static aratuka_tāurunga 메소드목록[64];static unsigned 메소드개수;
static unsigned ingoa_āpure_98daa19b[64],필드서술[64],āpure_taimau[64],필드개수;
static unsigned TAKE_uara(unsigned tuemi_COUNT){if(현재위치>roa_uara||tuemi_COUNT>roa_uara-현재위치){잘못됨=1;return 0;}unsigned raraunga_tūranga=현재위치;현재위치+=tuemi_COUNT;return raraunga_tūranga;}
static unsigned paita_raraunga(void){unsigned raraunga_tūranga=TAKE_uara(1);return 잘못됨?0:raraunga[raraunga_tūranga];}
static unsigned 절반값(void){unsigned taunga_x=paita_raraunga();return taunga_x<<8|paita_raraunga();}
static uint32_t 가득참(void){uint32_t taunga_x=절반값();return taunga_x<<16|절반값();}
static int UNICODE_uara(unsigned 순번,const char*aho_raraunga){return 순번>0&&순번<상수모음&&Kāwai_Rārangi[순번]==1&&strlen(aho_raraunga)==SECOND_uara[순번]&&!memcmp(raraunga+첫째값[순번],aho_raraunga,SECOND_uara[순번]);}
static int 같음(unsigned taunga_x,unsigned 세로좌표){return taunga_x>0&&taunga_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&Kāwai_Rārangi[taunga_x]==1&&Kāwai_Rārangi[세로좌표]==1&&SECOND_uara[taunga_x]==SECOND_uara[세로좌표]&&!memcmp(raraunga+첫째값[taunga_x],raraunga+첫째값[세로좌표],SECOND_uara[taunga_x]);}
static void 내보내기(const char*kōnae_tāurunga,...){if(잘못됨)return;va_list tohenga_HUĀNGA;va_start(tohenga_HUĀNGA,kōnae_tāurunga);int tuemi_COUNT=vsnprintf(Ngā_kupu+rahinga_kuputuhi,sizeof(Ngā_kupu)-rahinga_kuputuhi,kōnae_tāurunga,tohenga_HUĀNGA);va_end(tohenga_HUĀNGA);if(tuemi_COUNT<0||(unsigned)tuemi_COUNT>=sizeof(Ngā_kupu)-rahinga_kuputuhi){잘못됨=1;return;}rahinga_kuputuhi+=tuemi_COUNT;}
static int 서술자(unsigned pūtāutu_uara,int*mēhua){
    if(pūtāutu_uara<1||pūtāutu_uara>=상수모음||Kāwai_Rārangi[pūtāutu_uara]!=1)return -1;unsigned raraunga_tūranga=첫째값[pūtāutu_uara],mutu_OFFSET=raraunga_tūranga+SECOND_uara[pūtāutu_uara];if(raraunga_tūranga>=mutu_OFFSET||raraunga[raraunga_tūranga++]!='(')return -1;int tāurunga_COUNT=0;
    while(raraunga_tūranga<mutu_OFFSET&&raraunga[raraunga_tūranga]!=')'){
        unsigned waehere_pūāhua=raraunga[raraunga_tūranga++];while(waehere_pūāhua=='['&&raraunga_tūranga<mutu_OFFSET)waehere_pūāhua=raraunga[raraunga_tūranga++];
        if(waehere_pūāhua=='L'){while(raraunga_tūranga<mutu_OFFSET&&raraunga[raraunga_tūranga]!=';')raraunga_tūranga++;if(raraunga_tūranga==mutu_OFFSET)return -1;raraunga_tūranga++;}
        else if(waehere_pūāhua!='I'&&waehere_pūāhua!='Z'&&waehere_pūāhua!='B'&&waehere_pūāhua!='C'&&waehere_pūāhua!='S')return -1;
        if(++tāurunga_COUNT>16)return -1;
    }
    if(raraunga_tūranga+1>=mutu_OFFSET||raraunga[raraunga_tūranga++]!=')')return -1;*mēhua=raraunga[raraunga_tūranga]=='V'?0:1;
    if(raraunga[raraunga_tūranga]=='J'||raraunga[raraunga_tūranga]=='D'||raraunga[raraunga_tūranga]=='F')return -1;return tāurunga_COUNT;
}
static void 속성들(void){unsigned tuemi_COUNT=절반값();for(unsigned 순번=0;순번<tuemi_COUNT&&!잘못됨;순번++){절반값();unsigned rahi=가득참();TAKE_uara(rahi);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned tamaiti_putanga=절반값(),판번호=절반값();if(tamaiti_putanga||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Kāwai_Rārangi[순번]=paita_raraunga();switch(Kāwai_Rārangi[순번]){
        case 1:SECOND_uara[순번]=절반값();첫째값[순번]=TAKE_uara(SECOND_uara[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_uara(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_uara[순번]=절반값();break;
        case 15:첫째값[순번]=paita_raraunga();SECOND_uara[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Kāwai_Rārangi[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Kāwai_Rārangi[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_uara(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();ingoa_āpure_98daa19b[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned tāurunga_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<tāurunga_COUNT&&!잘못됨;안쪽순번++){
            unsigned Ingoa=절반값(),rahi=가득참();
            if(UNICODE_uara(Ingoa,"ConstantValue")){if(rahi!=2)return -1;āpure_taimau[순번]=절반값();}
            else TAKE_uara(rahi);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        aratuka_tāurunga*rōpū_rahi=메소드목록+순번;rōpū_rahi->설정비트=절반값();rōpū_rahi->Ingoa=절반값();rōpū_rahi->서술값=절반값();unsigned tāurunga_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<tāurunga_COUNT&&!잘못됨;안쪽순번++){
            unsigned Ingoa=절반값(),rahi=가득참(),whakahaere=현재위치;
            if(rahi>roa_uara-현재위치)return -1;
            if(UNICODE_uara(Ingoa,"Code")){
                rōpū_rahi->Huinga_Rokiroki=절반값();rōpū_rahi->지역변수들=절반값();rōpū_rahi->rahi=가득참();rōpū_rahi->tohutohu_SEQUENCE=TAKE_uara(rōpū_rahi->rahi);
                if(rōpū_rahi->Huinga_Rokiroki>128||rōpū_rahi->지역변수들>128||rōpū_rahi->rahi>8192||절반값())return -1;속성들();
            }else TAKE_uara(rahi);
            if(현재위치!=whakahaere+rahi)return -1;
        }
        if(!UNICODE_uara(rōpū_rahi->Ingoa,"<init>")&&(!(rōpū_rahi->설정비트&8)||(rōpū_rahi->설정비트&(0x100|0x20))||!rōpū_rahi->rahi))return -1;
    }
    속성들();return 잘못됨||현재위치!=roa_uara?-1:0;
}
static void taimau_uara(unsigned pūtāutu_uara){
    if(!pūtāutu_uara||pūtāutu_uara>=상수모음){잘못됨=1;return;}
    if(Kāwai_Rārangi[pūtāutu_uara]==3)내보내기("P(%uU);",첫째값[pūtāutu_uara]);
    else if(Kāwai_Rārangi[pūtāutu_uara]==8)내보내기("P((W)k%u);",pūtāutu_uara);else 잘못됨=1;
}
static void 호출(unsigned pūtāutu_uara,int mariko_CALL){
    if(pūtāutu_uara<1||pūtāutu_uara>=상수모음||(Kāwai_Rārangi[pūtāutu_uara]!=10&&Kāwai_Rārangi[pūtāutu_uara]!=11)||첫째값[pūtāutu_uara]<1||첫째값[pūtāutu_uara]>=상수모음||Kāwai_Rārangi[첫째값[pūtāutu_uara]]!=7||SECOND_uara[pūtāutu_uara]<1||SECOND_uara[pūtāutu_uara]>=상수모음||Kāwai_Rārangi[SECOND_uara[pūtāutu_uara]]!=12){잘못됨=1;return;}
    unsigned kaipupuri_ahanoa=첫째값[첫째값[pūtāutu_uara]],Ingoa=첫째값[SECOND_uara[pūtāutu_uara]],서술값=SECOND_uara[SECOND_uara[pūtāutu_uara]];int mēhua=0,tuemi_COUNT=서술자(서술값,&mēhua);if(tuemi_COUNT<0){잘못됨=1;return;}
    for(int 순번=tuemi_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(mariko_CALL)내보내기("Q();");
    if(!mariko_CALL&&같음(kaipupuri_ahanoa,첫째값[현재클래스])){
        unsigned rōpū_rahi=0;for(;rōpū_rahi<메소드개수;rōpū_rahi++)if(같음(Ingoa,메소드목록[rōpū_rahi].Ingoa)&&같음(서술값,메소드목록[rōpū_rahi].서술값))break;
        if(rōpū_rahi==메소드개수||!(메소드목록[rōpū_rahi].설정비트&8)){잘못됨=1;return;}
        if(mēhua)내보내기("P(");내보내기("m%u(",rōpū_rahi);for(int 순번=0;순번<tuemi_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(mēhua?"));":" );");return;
    }
    if((mariko_CALL&&UNICODE_uara(kaipupuri_ahanoa,"java/io/PrintStream")&& (UNICODE_uara(Ingoa,"print")||UNICODE_uara(Ingoa,"println")))||(!mariko_CALL&&UNICODE_uara(kaipupuri_ahanoa,"Reo_Māori/자체/출력"))){
        if(UNICODE_uara(서술값,"(I)V")&&(UNICODE_uara(Ingoa,"print")||UNICODE_uara(Ingoa,"println")||UNICODE_uara(Ingoa,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_uara(Ingoa,"print")?0:1);return;}
        if(UNICODE_uara(서술값,"(Ljava/lang/String;)V")&&(UNICODE_uara(Ingoa,"print")||UNICODE_uara(Ingoa,"println")||UNICODE_uara(Ingoa,"Tuhia")||UNICODE_uara(Ingoa,"tuhi_hononga"))){내보내기("jprint(x[0],0,%d);",UNICODE_uara(Ingoa,"print")||UNICODE_uara(Ingoa,"Tuhia")?0:1);return;}
        if(UNICODE_uara(서술값,"()V")&&UNICODE_uara(Ingoa,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!mariko_CALL&&UNICODE_uara(kaipupuri_ahanoa,"Reo_Māori/자체/Kōnae")){
        if(UNICODE_uara(Ingoa,"Tuhia")&&UNICODE_uara(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_uara(Ingoa,"Pānuitia")&&UNICODE_uara(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void hanga_aratuka(unsigned Rapu_INDEX){
    aratuka_tāurunga*rōpū_rahi=메소드목록+Rapu_INDEX;if(UNICODE_uara(rōpū_rahi->Ingoa,"<init>"))return;int mēhua,tuemi_COUNT=서술자(rōpū_rahi->서술값,&mēhua);if(tuemi_COUNT<0){잘못됨=1;return;}
    내보내기("static W m%u(",Rapu_INDEX);for(int 순번=0;순번<tuemi_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!tuemi_COUNT)내보내기("void");
    if((unsigned)tuemi_COUNT>rōpū_rahi->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",rōpū_rahi->지역변수들?rōpū_rahi->지역변수들:1);for(int 순번=0;순번<tuemi_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=roa_uara;roa_uara=rōpū_rahi->tohutohu_SEQUENCE+rōpū_rahi->rahi;현재위치=rōpū_rahi->tohutohu_SEQUENCE;
    while(현재위치<roa_uara&&!잘못됨){unsigned tono_tūranga=현재위치-rōpū_rahi->tohutohu_SEQUENCE,mahi_uara=paita_raraunga();내보내기("L%u:;",tono_tūranga);
        if(mahi_uara==0){}
        else if(mahi_uara==1)내보내기("P(0);");
        else if(mahi_uara>=2&&mahi_uara<=8)내보내기("P(%uU);",mahi_uara-3);
        else if(mahi_uara==16){int uara=(int8_t)paita_raraunga();내보내기("P(%uU);",(unsigned)uara);}
        else if(mahi_uara==17){int uara=(int16_t)절반값();내보내기("P(%uU);",(unsigned)uara);}
        else if(mahi_uara==18||mahi_uara==19)taimau_uara(mahi_uara==18?paita_raraunga():절반값());
        else if(mahi_uara==21||mahi_uara==25){unsigned 순번=paita_raraunga();if(순번>=rōpū_rahi->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((mahi_uara>=26&&mahi_uara<=29)||(mahi_uara>=42&&mahi_uara<=45)){unsigned 순번=mahi_uara>=42?mahi_uara-42:mahi_uara-26;if(순번>=rōpū_rahi->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(mahi_uara==54||mahi_uara==58){unsigned 순번=paita_raraunga();if(순번>=rōpū_rahi->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((mahi_uara>=59&&mahi_uara<=62)||(mahi_uara>=75&&mahi_uara<=78)){unsigned 순번=mahi_uara>=75?mahi_uara-75:mahi_uara-59;if(순번>=rōpū_rahi->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(mahi_uara==46||mahi_uara==50||mahi_uara==51||mahi_uara==52||mahi_uara==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(mahi_uara==79||mahi_uara==83||mahi_uara==84||mahi_uara==85||mahi_uara==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",mahi_uara==84?"(unsigned)(signed char)q":mahi_uara==85?"(unsigned short)q":mahi_uara==86?"(unsigned)(short)q":"q");
        else if(mahi_uara==87)내보내기("Q();");
        else if(mahi_uara==89)내보내기("q=Q();P(q);P(q);");
        else if(mahi_uara==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(mahi_uara==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(mahi_uara==96||mahi_uara==100||mahi_uara==104||mahi_uara==120||mahi_uara==124||mahi_uara==126||mahi_uara==128||mahi_uara==130){const char*whakawaehere_uara=mahi_uara==96?"+":mahi_uara==100?"-":mahi_uara==104?"*":mahi_uara==120?"<<":mahi_uara==124?">>":mahi_uara==126?"&":mahi_uara==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",whakawaehere_uara,mahi_uara==120||mahi_uara==124?"%32":"");}
        else if(mahi_uara==108||mahi_uara==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",mahi_uara==112);
        else if(mahi_uara==116)내보내기("P(0U-(unsigned)Q());");
        else if(mahi_uara==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(mahi_uara==132){unsigned 순번=paita_raraunga();int 차이=(int8_t)paita_raraunga();if(순번>=rōpū_rahi->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(mahi_uara>=145&&mahi_uara<=147)내보내기("P((unsigned)(%s)Q());",mahi_uara==145?"signed char":mahi_uara==146?"unsigned short":"short");
        else if(mahi_uara>=153&&mahi_uara<=166){int ūnga=(int)tono_tūranga+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(ūnga<0||ūnga>=(int)rōpū_rahi->rahi){잘못됨=1;break;}if(mahi_uara<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[mahi_uara-153],ūnga);else if(mahi_uara<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[mahi_uara-159],ūnga);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",mahi_uara==165?"==":"!=",ūnga);}
        else if(mahi_uara==167){int ūnga=(int)tono_tūranga+(int16_t)절반값();if(ūnga<0||ūnga>=(int)rōpū_rahi->rahi)잘못됨=1;내보내기("goto L%d;",ūnga);}
        else if(mahi_uara==172||mahi_uara==176)내보내기("return Q();");else if(mahi_uara==177)내보내기("return 0;");
        else if(mahi_uara==178||mahi_uara==179){unsigned pūtāutu_uara=절반값();if(pūtāutu_uara<1||pūtāutu_uara>=상수모음||Kāwai_Rārangi[pūtāutu_uara]!=9||첫째값[pūtāutu_uara]>=상수모음||SECOND_uara[pūtāutu_uara]>=상수모음||Kāwai_Rārangi[첫째값[pūtāutu_uara]]!=7||Kāwai_Rārangi[SECOND_uara[pūtāutu_uara]]!=12){잘못됨=1;break;}unsigned kaipupuri_ahanoa=첫째값[첫째값[pūtāutu_uara]],Ingoa=첫째값[SECOND_uara[pūtāutu_uara]],서술값=SECOND_uara[SECOND_uara[pūtāutu_uara]];
            if(mahi_uara==178&&UNICODE_uara(kaipupuri_ahanoa,"java/lang/System")&&UNICODE_uara(Ingoa,"out")&&UNICODE_uara(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned kōnae_tāurunga=0;while(kōnae_tāurunga<필드개수&&(!같음(Ingoa,ingoa_āpure_98daa19b[kōnae_tāurunga])||!같음(서술값,필드서술[kōnae_tāurunga])))kōnae_tāurunga++;if(!같음(kaipupuri_ahanoa,첫째값[현재클래스])||kōnae_tāurunga==필드개수){잘못됨=1;break;}내보내기(mahi_uara==178?"P(fields[%u]);":"fields[%u]=Q();",kōnae_tāurunga);}}
        else if(mahi_uara==182||mahi_uara==184)호출(절반값(),mahi_uara==182);
        else if(mahi_uara==188){unsigned TYPE_kāwai=paita_raraunga();if(TYPE_kāwai!=4&&TYPE_kāwai!=5&&TYPE_kāwai!=8&&TYPE_kāwai!=9&&TYPE_kāwai!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(mahi_uara==190)내보내기("P(jlength(Q()));");
        else if(mahi_uara==198||mahi_uara==199){int ūnga=(int)tono_tūranga+(int16_t)절반값();if(ūnga<0||ūnga>=(int)rōpū_rahi->rahi)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",mahi_uara==198?"==":"!=",ūnga);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",Rapu_INDEX,mahi_uara,tono_tūranga);
        내보내기("\n");
    }
    roa_uara=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned aho_ngā_wae(unsigned *raraunga_tūranga,unsigned mutu_OFFSET){
    if(*raraunga_tūranga>=mutu_OFFSET){잘못됨=1;return 0;}unsigned waehere_pūāhua=raraunga[(*raraunga_tūranga)++];
    if(waehere_pūāhua<128)return waehere_pūāhua;
    unsigned tuemi_COUNT=waehere_pūāhua>=0xc0&&waehere_pūāhua<=0xdf?1:waehere_pūāhua>=0xe0&&waehere_pūāhua<=0xef?2:3;
    if(tuemi_COUNT==3||tuemi_COUNT>mutu_OFFSET-*raraunga_tūranga){잘못됨=1;return 0;}unsigned uara=waehere_pūāhua&((1u<<(6-tuemi_COUNT))-1);
    for(unsigned 순번=0;순번<tuemi_COUNT;순번++){unsigned Panuku_tuemi=raraunga[(*raraunga_tūranga)++];if((Panuku_tuemi&0xc0)!=0x80)잘못됨=1;uara=uara<<6|(Panuku_tuemi&63);}
    if((tuemi_COUNT==1&&uara<128&&uara!=0)||(tuemi_COUNT==2&&uara<2048))잘못됨=1;return uara;
}
static void aho_taimau(unsigned pūtāutu_uara){
    unsigned 부호없는값=첫째값[pūtāutu_uara];if(부호없는값<1||부호없는값>=상수모음||Kāwai_Rārangi[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",pūtāutu_uara);
    unsigned raraunga_tūranga=첫째값[부호없는값],mutu_OFFSET=raraunga_tūranga+SECOND_uara[부호없는값];
    while(raraunga_tūranga<mutu_OFFSET&&!잘못됨){unsigned waehere_pūāhua=aho_ngā_wae(&raraunga_tūranga,mutu_OFFSET);
        if(waehere_pūāhua>=0xd800&&waehere_pūāhua<=0xdbff){unsigned 낮은부분=aho_ngā_wae(&raraunga_tūranga,mutu_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}waehere_pūāhua=0x10000+((waehere_pūāhua-0xd800)<<10)+낮은부분-0xdc00;}
        else if(waehere_pūāhua>=0xdc00&&waehere_pūāhua<=0xdfff){잘못됨=1;break;}
        if(!waehere_pūāhua){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(waehere_pūāhua<128)내보내기("%u,",waehere_pūāhua);
        else{unsigned tuemi_COUNT=waehere_pūāhua<2048?2:waehere_pūāhua<65536?3:4;내보내기("%u,",(tuemi_COUNT==2?0xc0:tuemi_COUNT==3?0xe0:0xf0)|(waehere_pūāhua>>(6*(tuemi_COUNT-1))));for(unsigned 순번=tuemi_COUNT-1;순번;순번--)내보내기("%u,",0x80|((waehere_pūāhua>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Ingoa){
    size_t tuemi_COUNT=strlen(Ingoa);
    if(tuemi_COUNT>4&&!strcmp(Ingoa+tuemi_COUNT-4,".jar")){
        if(꾸러미열기(Ingoa)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char ara[256];const char*tāurunga_aratuka=꾸러미진입클래스();tuemi_COUNT=strlen(tāurunga_aratuka);if(tuemi_COUNT+6>=sizeof(ara))return 0;
        for(unsigned 순번=0;순번<tuemi_COUNT;순번++)ara[순번]=tāurunga_aratuka[순번]=='.'?'/':tāurunga_aratuka[순번];strcpy(ara+tuemi_COUNT,".class");int tāurunga_COUNT=꾸러미읽기(ara,raraunga,sizeof(raraunga));if(tāurunga_COUNT<0)return 0;roa_uara=tāurunga_COUNT;
    }else{intptr_t kōnae_raweke=사용자호출(3,(uintptr_t)Ingoa,0,0,0,0,0);if(kōnae_raweke<0)return 0;intptr_t tāurunga_COUNT=사용자호출(9,kōnae_raweke,0,0,0,0,0);if(tāurunga_COUNT<0||tāurunga_COUNT>sizeof(raraunga)){사용자호출(4,kōnae_raweke,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,kōnae_raweke,(uintptr_t)raraunga,tāurunga_COUNT,0,0,0);사용자호출(4,kōnae_raweke,0,0,0,0,0);if(RECEIVED_COUNT!=tāurunga_COUNT)return 0;roa_uara=tāurunga_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Kāwai_Rārangi[순번]==8)aho_taimau(순번);
    if(잘못됨)return 0;
    int tāurunga_ira=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_uara(메소드목록[순번].Ingoa,"<init>")){
        int mēhua,tāurunga_COUNT=서술자(메소드목록[순번].서술값,&mēhua);if(tāurunga_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<tāurunga_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!tāurunga_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_uara(메소드목록[순번].Ingoa,"main")&&UNICODE_uara(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)tāurunga_ira=순번;
        if(UNICODE_uara(메소드목록[순번].Ingoa,"<clinit>"))초기값=순번;
    }
    if(tāurunga_ira<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)hanga_aratuka(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(āpure_taimau[순번]){
        unsigned waehere_pūāhua=āpure_taimau[순번];if(waehere_pūāhua>=상수모음)return 0;
        if(Kāwai_Rārangi[waehere_pūāhua]==3)내보내기("fields[%u]=%uU;",순번,첫째값[waehere_pūāhua]);else if(Kāwai_Rārangi[waehere_pūāhua]==8)내보내기("fields[%u]=(W)k%u;",순번,waehere_pūāhua);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",tāurunga_ira);
    return 잘못됨?0:Ngā_kupu;
}
