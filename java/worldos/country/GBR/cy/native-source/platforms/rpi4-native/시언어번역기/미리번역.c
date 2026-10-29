#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "bwndel.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned hyd_VALUE,현재위치;static int technoleg_gwybodaeth_annilys;
static unsigned Tagiau_Rhestr[512],첫째값[512],SECOND_VALUE[512],cysonyn_cronfa,현재클래스;
static char Testun[65536];static unsigned maint_y_testun;
typedef struct {unsigned 설정비트,Enw,서술값,cyfarwyddyd_SEQUENCE,Maint,지역변수들,pentwr_Storio;} dull_cofnod;
static dull_cofnod 메소드목록[64];static unsigned 메소드개수;
static unsigned enw_maes_98daa19b[64],필드서술[64],maes_cysonyn[64],필드개수;
static unsigned TAKE_VALUE(unsigned eitem_COUNT){if(현재위치>hyd_VALUE||eitem_COUNT>hyd_VALUE-현재위치){technoleg_gwybodaeth_annilys=1;return 0;}unsigned data_safle=현재위치;현재위치+=eitem_COUNT;return data_safle;}
static unsigned beit_data(void){unsigned data_safle=TAKE_VALUE(1);return technoleg_gwybodaeth_annilys?0:data[data_safle];}
static unsigned 절반값(void){unsigned cyfesuryn_x=beit_data();return cyfesuryn_x<<8|beit_data();}
static uint32_t 가득참(void){uint32_t cyfesuryn_x=절반값();return cyfesuryn_x<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*testun_data){return 순번>0&&순번<cysonyn_cronfa&&Tagiau_Rhestr[순번]==1&&strlen(testun_data)==SECOND_VALUE[순번]&&!memcmp(data+첫째값[순번],testun_data,SECOND_VALUE[순번]);}
static int 같음(unsigned cyfesuryn_x,unsigned Y_cyfesuryn){return cyfesuryn_x>0&&cyfesuryn_x<cysonyn_cronfa&&Y_cyfesuryn>0&&Y_cyfesuryn<cysonyn_cronfa&&Tagiau_Rhestr[cyfesuryn_x]==1&&Tagiau_Rhestr[Y_cyfesuryn]==1&&SECOND_VALUE[cyfesuryn_x]==SECOND_VALUE[Y_cyfesuryn]&&!memcmp(data+첫째값[cyfesuryn_x],data+첫째값[Y_cyfesuryn],SECOND_VALUE[cyfesuryn_x]);}
static void 내보내기(const char*ffeil_cofnod,...){if(technoleg_gwybodaeth_annilys)return;va_list arg_ARAE;va_start(arg_ARAE,ffeil_cofnod);int eitem_COUNT=vsnprintf(Testun+maint_y_testun,sizeof(Testun)-maint_y_testun,ffeil_cofnod,arg_ARAE);va_end(arg_ARAE);if(eitem_COUNT<0||(unsigned)eitem_COUNT>=sizeof(Testun)-maint_y_testun){technoleg_gwybodaeth_annilys=1;return;}maint_y_testun+=eitem_COUNT;}
static int 서술자(unsigned dynodwr_VALUE,int*mesur){
    if(dynodwr_VALUE<1||dynodwr_VALUE>=cysonyn_cronfa||Tagiau_Rhestr[dynodwr_VALUE]!=1)return -1;unsigned data_safle=첫째값[dynodwr_VALUE],gorffen_OFFSET=data_safle+SECOND_VALUE[dynodwr_VALUE];if(data_safle>=gorffen_OFFSET||data[data_safle++]!='(')return -1;int cofnod_COUNT=0;
    while(data_safle<gorffen_OFFSET&&data[data_safle]!=')'){
        unsigned cod_nod=data[data_safle++];while(cod_nod=='['&&data_safle<gorffen_OFFSET)cod_nod=data[data_safle++];
        if(cod_nod=='L'){while(data_safle<gorffen_OFFSET&&data[data_safle]!=';')data_safle++;if(data_safle==gorffen_OFFSET)return -1;data_safle++;}
        else if(cod_nod!='I'&&cod_nod!='Z'&&cod_nod!='B'&&cod_nod!='C'&&cod_nod!='S')return -1;
        if(++cofnod_COUNT>16)return -1;
    }
    if(data_safle+1>=gorffen_OFFSET||data[data_safle++]!=')')return -1;*mesur=data[data_safle]=='V'?0:1;
    if(data[data_safle]=='J'||data[data_safle]=='D'||data[data_safle]=='F')return -1;return cofnod_COUNT;
}
static void priodoleddau(void){unsigned eitem_COUNT=절반값();for(unsigned 순번=0;순번<eitem_COUNT&&!technoleg_gwybodaeth_annilys;순번++){절반값();unsigned Maint=가득참();TAKE_VALUE(Maint);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned fersiwn_bach=절반값(),rhif_fersiwn=절반값();if(fersiwn_bach||rhif_fersiwn<45||rhif_fersiwn>52)return -1;
    cysonyn_cronfa=절반값();if(cysonyn_cronfa<1||cysonyn_cronfa>512)return -1;
    for(unsigned 순번=1;순번<cysonyn_cronfa&&!technoleg_gwybodaeth_annilys;순번++){
        Tagiau_Rhestr[순번]=beit_data();switch(Tagiau_Rhestr[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=cysonyn_cronfa)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=beit_data();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=cysonyn_cronfa||Tagiau_Rhestr[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=cysonyn_cronfa||Tagiau_Rhestr[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!technoleg_gwybodaeth_annilys;순번++){
        unsigned 설정비트=절반값();enw_maes_98daa19b[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned cofnod_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<cofnod_COUNT&&!technoleg_gwybodaeth_annilys;안쪽순번++){
            unsigned Enw=절반값(),Maint=가득참();
            if(UNICODE_VALUE(Enw,"ConstantValue")){if(Maint!=2)return -1;maes_cysonyn[순번]=절반값();}
            else TAKE_VALUE(Maint);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!technoleg_gwybodaeth_annilys;순번++){
        dull_cofnod*Grŵp_newid_maint=메소드목록+순번;Grŵp_newid_maint->설정비트=절반값();Grŵp_newid_maint->Enw=절반값();Grŵp_newid_maint->서술값=절반값();unsigned cofnod_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<cofnod_COUNT&&!technoleg_gwybodaeth_annilys;안쪽순번++){
            unsigned Enw=절반값(),Maint=가득참(),Gweithredu_2=현재위치;
            if(Maint>hyd_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(Enw,"Code")){
                Grŵp_newid_maint->pentwr_Storio=절반값();Grŵp_newid_maint->지역변수들=절반값();Grŵp_newid_maint->Maint=가득참();Grŵp_newid_maint->cyfarwyddyd_SEQUENCE=TAKE_VALUE(Grŵp_newid_maint->Maint);
                if(Grŵp_newid_maint->pentwr_Storio>128||Grŵp_newid_maint->지역변수들>128||Grŵp_newid_maint->Maint>8192||절반값())return -1;priodoleddau();
            }else TAKE_VALUE(Maint);
            if(현재위치!=Gweithredu_2+Maint)return -1;
        }
        if(!UNICODE_VALUE(Grŵp_newid_maint->Enw,"<init>")&&(!(Grŵp_newid_maint->설정비트&8)||(Grŵp_newid_maint->설정비트&(0x100|0x20))||!Grŵp_newid_maint->Maint))return -1;
    }
    priodoleddau();return technoleg_gwybodaeth_annilys||현재위치!=hyd_VALUE?-1:0;
}
static void cysonyn_VALUE(unsigned dynodwr_VALUE){
    if(!dynodwr_VALUE||dynodwr_VALUE>=cysonyn_cronfa){technoleg_gwybodaeth_annilys=1;return;}
    if(Tagiau_Rhestr[dynodwr_VALUE]==3)내보내기("P(%uU);",첫째값[dynodwr_VALUE]);
    else if(Tagiau_Rhestr[dynodwr_VALUE]==8)내보내기("P((W)k%u);",dynodwr_VALUE);else technoleg_gwybodaeth_annilys=1;
}
static void 호출(unsigned dynodwr_VALUE,int rhith_CALL){
    if(dynodwr_VALUE<1||dynodwr_VALUE>=cysonyn_cronfa||(Tagiau_Rhestr[dynodwr_VALUE]!=10&&Tagiau_Rhestr[dynodwr_VALUE]!=11)||첫째값[dynodwr_VALUE]<1||첫째값[dynodwr_VALUE]>=cysonyn_cronfa||Tagiau_Rhestr[첫째값[dynodwr_VALUE]]!=7||SECOND_VALUE[dynodwr_VALUE]<1||SECOND_VALUE[dynodwr_VALUE]>=cysonyn_cronfa||Tagiau_Rhestr[SECOND_VALUE[dynodwr_VALUE]]!=12){technoleg_gwybodaeth_annilys=1;return;}
    unsigned perchennog_gwrthrych=첫째값[첫째값[dynodwr_VALUE]],Enw=첫째값[SECOND_VALUE[dynodwr_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[dynodwr_VALUE]];int mesur=0,eitem_COUNT=서술자(서술값,&mesur);if(eitem_COUNT<0){technoleg_gwybodaeth_annilys=1;return;}
    for(int 순번=eitem_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(rhith_CALL)내보내기("Q();");
    if(!rhith_CALL&&같음(perchennog_gwrthrych,첫째값[현재클래스])){
        unsigned Grŵp_newid_maint=0;for(;Grŵp_newid_maint<메소드개수;Grŵp_newid_maint++)if(같음(Enw,메소드목록[Grŵp_newid_maint].Enw)&&같음(서술값,메소드목록[Grŵp_newid_maint].서술값))break;
        if(Grŵp_newid_maint==메소드개수||!(메소드목록[Grŵp_newid_maint].설정비트&8)){technoleg_gwybodaeth_annilys=1;return;}
        if(mesur)내보내기("P(");내보내기("m%u(",Grŵp_newid_maint);for(int 순번=0;순번<eitem_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(mesur?"));":" );");return;
    }
    if((rhith_CALL&&UNICODE_VALUE(perchennog_gwrthrych,"java/io/PrintStream")&& (UNICODE_VALUE(Enw,"print")||UNICODE_VALUE(Enw,"println")))||(!rhith_CALL&&UNICODE_VALUE(perchennog_gwrthrych,"Cymraeg/자체/Allbwn"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Enw,"print")||UNICODE_VALUE(Enw,"println")||UNICODE_VALUE(Enw,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Enw,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Enw,"print")||UNICODE_VALUE(Enw,"println")||UNICODE_VALUE(Enw,"Ysgrifennu")||UNICODE_VALUE(Enw,"ysgrifennu_llinell"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Enw,"print")||UNICODE_VALUE(Enw,"Ysgrifennu")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Enw,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!rhith_CALL&&UNICODE_VALUE(perchennog_gwrthrych,"Cymraeg/자체/Ffeil")){
        if(UNICODE_VALUE(Enw,"Ysgrifennu")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Enw,"Darllen")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    technoleg_gwybodaeth_annilys=1;
}
static void llunio_dull(unsigned LOOKUP_INDEX){
    dull_cofnod*Grŵp_newid_maint=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Grŵp_newid_maint->Enw,"<init>"))return;int mesur,eitem_COUNT=서술자(Grŵp_newid_maint->서술값,&mesur);if(eitem_COUNT<0){technoleg_gwybodaeth_annilys=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<eitem_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!eitem_COUNT)내보내기("void");
    if((unsigned)eitem_COUNT>Grŵp_newid_maint->지역변수들){technoleg_gwybodaeth_annilys=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grŵp_newid_maint->지역변수들?Grŵp_newid_maint->지역변수들:1);for(int 순번=0;순번<eitem_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=hyd_VALUE;hyd_VALUE=Grŵp_newid_maint->cyfarwyddyd_SEQUENCE+Grŵp_newid_maint->Maint;현재위치=Grŵp_newid_maint->cyfarwyddyd_SEQUENCE;
    while(현재위치<hyd_VALUE&&!technoleg_gwybodaeth_annilys){unsigned gorchymyn_safle=현재위치-Grŵp_newid_maint->cyfarwyddyd_SEQUENCE,gweithrediad_VALUE=beit_data();내보내기("L%u:;",gorchymyn_safle);
        if(gweithrediad_VALUE==0){}
        else if(gweithrediad_VALUE==1)내보내기("P(0);");
        else if(gweithrediad_VALUE>=2&&gweithrediad_VALUE<=8)내보내기("P(%uU);",gweithrediad_VALUE-3);
        else if(gweithrediad_VALUE==16){int VALUE=(int8_t)beit_data();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(gweithrediad_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(gweithrediad_VALUE==18||gweithrediad_VALUE==19)cysonyn_VALUE(gweithrediad_VALUE==18?beit_data():절반값());
        else if(gweithrediad_VALUE==21||gweithrediad_VALUE==25){unsigned 순번=beit_data();if(순번>=Grŵp_newid_maint->지역변수들)technoleg_gwybodaeth_annilys=1;내보내기("P(v[%u]);",순번);}
        else if((gweithrediad_VALUE>=26&&gweithrediad_VALUE<=29)||(gweithrediad_VALUE>=42&&gweithrediad_VALUE<=45)){unsigned 순번=gweithrediad_VALUE>=42?gweithrediad_VALUE-42:gweithrediad_VALUE-26;if(순번>=Grŵp_newid_maint->지역변수들)technoleg_gwybodaeth_annilys=1;내보내기("P(v[%u]);",순번);}
        else if(gweithrediad_VALUE==54||gweithrediad_VALUE==58){unsigned 순번=beit_data();if(순번>=Grŵp_newid_maint->지역변수들)technoleg_gwybodaeth_annilys=1;내보내기("v[%u]=Q();",순번);}
        else if((gweithrediad_VALUE>=59&&gweithrediad_VALUE<=62)||(gweithrediad_VALUE>=75&&gweithrediad_VALUE<=78)){unsigned 순번=gweithrediad_VALUE>=75?gweithrediad_VALUE-75:gweithrediad_VALUE-59;if(순번>=Grŵp_newid_maint->지역변수들)technoleg_gwybodaeth_annilys=1;내보내기("v[%u]=Q();",순번);}
        else if(gweithrediad_VALUE==46||gweithrediad_VALUE==50||gweithrediad_VALUE==51||gweithrediad_VALUE==52||gweithrediad_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(gweithrediad_VALUE==79||gweithrediad_VALUE==83||gweithrediad_VALUE==84||gweithrediad_VALUE==85||gweithrediad_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",gweithrediad_VALUE==84?"(unsigned)(signed char)q":gweithrediad_VALUE==85?"(unsigned short)q":gweithrediad_VALUE==86?"(unsigned)(short)q":"q");
        else if(gweithrediad_VALUE==87)내보내기("Q();");
        else if(gweithrediad_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(gweithrediad_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(gweithrediad_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(gweithrediad_VALUE==96||gweithrediad_VALUE==100||gweithrediad_VALUE==104||gweithrediad_VALUE==120||gweithrediad_VALUE==124||gweithrediad_VALUE==126||gweithrediad_VALUE==128||gweithrediad_VALUE==130){const char*amgodio_VALUE=gweithrediad_VALUE==96?"+":gweithrediad_VALUE==100?"-":gweithrediad_VALUE==104?"*":gweithrediad_VALUE==120?"<<":gweithrediad_VALUE==124?">>":gweithrediad_VALUE==126?"&":gweithrediad_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",amgodio_VALUE,gweithrediad_VALUE==120||gweithrediad_VALUE==124?"%32":"");}
        else if(gweithrediad_VALUE==108||gweithrediad_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",gweithrediad_VALUE==112);
        else if(gweithrediad_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(gweithrediad_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(gweithrediad_VALUE==132){unsigned 순번=beit_data();int 차이=(int8_t)beit_data();if(순번>=Grŵp_newid_maint->지역변수들)technoleg_gwybodaeth_annilys=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(gweithrediad_VALUE>=145&&gweithrediad_VALUE<=147)내보내기("P((unsigned)(%s)Q());",gweithrediad_VALUE==145?"signed char":gweithrediad_VALUE==146?"unsigned short":"short");
        else if(gweithrediad_VALUE>=153&&gweithrediad_VALUE<=166){int targed=(int)gorchymyn_safle+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(targed<0||targed>=(int)Grŵp_newid_maint->Maint){technoleg_gwybodaeth_annilys=1;break;}if(gweithrediad_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[gweithrediad_VALUE-153],targed);else if(gweithrediad_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[gweithrediad_VALUE-159],targed);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",gweithrediad_VALUE==165?"==":"!=",targed);}
        else if(gweithrediad_VALUE==167){int targed=(int)gorchymyn_safle+(int16_t)절반값();if(targed<0||targed>=(int)Grŵp_newid_maint->Maint)technoleg_gwybodaeth_annilys=1;내보내기("goto L%d;",targed);}
        else if(gweithrediad_VALUE==172||gweithrediad_VALUE==176)내보내기("return Q();");else if(gweithrediad_VALUE==177)내보내기("return 0;");
        else if(gweithrediad_VALUE==178||gweithrediad_VALUE==179){unsigned dynodwr_VALUE=절반값();if(dynodwr_VALUE<1||dynodwr_VALUE>=cysonyn_cronfa||Tagiau_Rhestr[dynodwr_VALUE]!=9||첫째값[dynodwr_VALUE]>=cysonyn_cronfa||SECOND_VALUE[dynodwr_VALUE]>=cysonyn_cronfa||Tagiau_Rhestr[첫째값[dynodwr_VALUE]]!=7||Tagiau_Rhestr[SECOND_VALUE[dynodwr_VALUE]]!=12){technoleg_gwybodaeth_annilys=1;break;}unsigned perchennog_gwrthrych=첫째값[첫째값[dynodwr_VALUE]],Enw=첫째값[SECOND_VALUE[dynodwr_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[dynodwr_VALUE]];
            if(gweithrediad_VALUE==178&&UNICODE_VALUE(perchennog_gwrthrych,"java/lang/System")&&UNICODE_VALUE(Enw,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned ffeil_cofnod=0;while(ffeil_cofnod<필드개수&&(!같음(Enw,enw_maes_98daa19b[ffeil_cofnod])||!같음(서술값,필드서술[ffeil_cofnod])))ffeil_cofnod++;if(!같음(perchennog_gwrthrych,첫째값[현재클래스])||ffeil_cofnod==필드개수){technoleg_gwybodaeth_annilys=1;break;}내보내기(gweithrediad_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",ffeil_cofnod);}}
        else if(gweithrediad_VALUE==182||gweithrediad_VALUE==184)호출(절반값(),gweithrediad_VALUE==182);
        else if(gweithrediad_VALUE==188){unsigned TYPE_ardal=beit_data();if(TYPE_ardal!=4&&TYPE_ardal!=5&&TYPE_ardal!=8&&TYPE_ardal!=9&&TYPE_ardal!=10)technoleg_gwybodaeth_annilys=1;내보내기("P(jarray((int)Q()));");}
        else if(gweithrediad_VALUE==190)내보내기("P(jlength(Q()));");
        else if(gweithrediad_VALUE==198||gweithrediad_VALUE==199){int targed=(int)gorchymyn_safle+(int16_t)절반값();if(targed<0||targed>=(int)Grŵp_newid_maint->Maint)technoleg_gwybodaeth_annilys=1;내보내기("if(Q()%s0)goto L%d;",gweithrediad_VALUE==198?"==":"!=",targed);}
        else technoleg_gwybodaeth_annilys=1;
        if(technoleg_gwybodaeth_annilys)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,gweithrediad_VALUE,gorchymyn_safle);
        내보내기("\n");
    }
    hyd_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned testun_gwers(unsigned *data_safle,unsigned gorffen_OFFSET){
    if(*data_safle>=gorffen_OFFSET){technoleg_gwybodaeth_annilys=1;return 0;}unsigned cod_nod=data[(*data_safle)++];
    if(cod_nod<128)return cod_nod;
    unsigned eitem_COUNT=cod_nod>=0xc0&&cod_nod<=0xdf?1:cod_nod>=0xe0&&cod_nod<=0xef?2:3;
    if(eitem_COUNT==3||eitem_COUNT>gorffen_OFFSET-*data_safle){technoleg_gwybodaeth_annilys=1;return 0;}unsigned VALUE=cod_nod&((1u<<(6-eitem_COUNT))-1);
    for(unsigned 순번=0;순번<eitem_COUNT;순번++){unsigned Nesaf_eitem=data[(*data_safle)++];if((Nesaf_eitem&0xc0)!=0x80)technoleg_gwybodaeth_annilys=1;VALUE=VALUE<<6|(Nesaf_eitem&63);}
    if((eitem_COUNT==1&&VALUE<128&&VALUE!=0)||(eitem_COUNT==2&&VALUE<2048))technoleg_gwybodaeth_annilys=1;return VALUE;
}
static void testun_cysonyn(unsigned dynodwr_VALUE){
    unsigned 부호없는값=첫째값[dynodwr_VALUE];if(부호없는값<1||부호없는값>=cysonyn_cronfa||Tagiau_Rhestr[부호없는값]!=1){technoleg_gwybodaeth_annilys=1;return;}내보내기("static const unsigned char k%u[]={",dynodwr_VALUE);
    unsigned data_safle=첫째값[부호없는값],gorffen_OFFSET=data_safle+SECOND_VALUE[부호없는값];
    while(data_safle<gorffen_OFFSET&&!technoleg_gwybodaeth_annilys){unsigned cod_nod=testun_gwers(&data_safle,gorffen_OFFSET);
        if(cod_nod>=0xd800&&cod_nod<=0xdbff){unsigned 낮은부분=testun_gwers(&data_safle,gorffen_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){technoleg_gwybodaeth_annilys=1;break;}cod_nod=0x10000+((cod_nod-0xd800)<<10)+낮은부분-0xdc00;}
        else if(cod_nod>=0xdc00&&cod_nod<=0xdfff){technoleg_gwybodaeth_annilys=1;break;}
        if(!cod_nod){printf("jaot: embedded NUL string needs JVM mode\n");technoleg_gwybodaeth_annilys=1;break;}
        if(cod_nod<128)내보내기("%u,",cod_nod);
        else{unsigned eitem_COUNT=cod_nod<2048?2:cod_nod<65536?3:4;내보내기("%u,",(eitem_COUNT==2?0xc0:eitem_COUNT==3?0xe0:0xf0)|(cod_nod>>(6*(eitem_COUNT-1))));for(unsigned 순번=eitem_COUNT-1;순번;순번--)내보내기("%u,",0x80|((cod_nod>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Enw){
    size_t eitem_COUNT=strlen(Enw);
    if(eitem_COUNT>4&&!strcmp(Enw+eitem_COUNT-4,".jar")){
        if(꾸러미열기(Enw)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char LLWYBR[256];const char*cofnod_dull=꾸러미진입클래스();eitem_COUNT=strlen(cofnod_dull);if(eitem_COUNT+6>=sizeof(LLWYBR))return 0;
        for(unsigned 순번=0;순번<eitem_COUNT;순번++)LLWYBR[순번]=cofnod_dull[순번]=='.'?'/':cofnod_dull[순번];strcpy(LLWYBR+eitem_COUNT,".class");int cofnod_COUNT=꾸러미읽기(LLWYBR,data,sizeof(data));if(cofnod_COUNT<0)return 0;hyd_VALUE=cofnod_COUNT;
    }else{intptr_t ffeil_dolen=사용자호출(3,(uintptr_t)Enw,0,0,0,0,0);if(ffeil_dolen<0)return 0;intptr_t cofnod_COUNT=사용자호출(9,ffeil_dolen,0,0,0,0,0);if(cofnod_COUNT<0||cofnod_COUNT>sizeof(data)){사용자호출(4,ffeil_dolen,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,ffeil_dolen,(uintptr_t)data,cofnod_COUNT,0,0,0);사용자호출(4,ffeil_dolen,0,0,0,0,0);if(RECEIVED_COUNT!=cofnod_COUNT)return 0;hyd_VALUE=cofnod_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<cysonyn_cronfa&&!technoleg_gwybodaeth_annilys;순번++)if(Tagiau_Rhestr[순번]==8)testun_cysonyn(순번);
    if(technoleg_gwybodaeth_annilys)return 0;
    int cofnod_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Enw,"<init>")){
        int mesur,cofnod_COUNT=서술자(메소드목록[순번].서술값,&mesur);if(cofnod_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<cofnod_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!cofnod_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Enw,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)cofnod_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Enw,"<clinit>"))초기값=순번;
    }
    if(cofnod_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!technoleg_gwybodaeth_annilys;순번++)llunio_dull(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(maes_cysonyn[순번]){
        unsigned cod_nod=maes_cysonyn[순번];if(cod_nod>=cysonyn_cronfa)return 0;
        if(Tagiau_Rhestr[cod_nod]==3)내보내기("fields[%u]=%uU;",순번,첫째값[cod_nod]);else if(Tagiau_Rhestr[cod_nod]==8)내보내기("fields[%u]=(W)k%u;",순번,cod_nod);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",cofnod_p);
    return technoleg_gwybodaeth_annilys?0:Testun;
}
