#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "trusgan.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char dàta[16384];static unsigned faid_VALUE,현재위치;static int 잘못됨;
static unsigned tagaichean_Liosta[512],첫째값[512],SECOND_VALUE[512],상수모음,현재클래스;
static char SMS[65536];static unsigned meud_an_teacsa;
typedef struct {unsigned 설정비트,Ainm,서술값,treòrachadh_SEQUENCE,atharraich_am_meud,지역변수들,stac_stòras;} dòigh_cur_a_steach;
static dòigh_cur_a_steach 메소드목록[64];static unsigned 메소드개수;
static unsigned ainm_raoin[64],필드서술[64],raon_cunbhalachan[64],필드개수;
static unsigned TAKE_VALUE(unsigned nì_COUNT){if(현재위치>faid_VALUE||nì_COUNT>faid_VALUE-현재위치){잘못됨=1;return 0;}unsigned dàta_suidhich=현재위치;현재위치+=nì_COUNT;return dàta_suidhich;}
static unsigned baidht_dàta(void){unsigned dàta_suidhich=TAKE_VALUE(1);return 잘못됨?0:dàta[dàta_suidhich];}
static unsigned 절반값(void){unsigned co_chomharra_x=baidht_dàta();return co_chomharra_x<<8|baidht_dàta();}
static uint32_t 가득참(void){uint32_t co_chomharra_x=절반값();return co_chomharra_x<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*sreang_dàta){return 순번>0&&순번<상수모음&&tagaichean_Liosta[순번]==1&&strlen(sreang_dàta)==SECOND_VALUE[순번]&&!memcmp(dàta+첫째값[순번],sreang_dàta,SECOND_VALUE[순번]);}
static int 같음(unsigned co_chomharra_x,unsigned 세로좌표){return co_chomharra_x>0&&co_chomharra_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&tagaichean_Liosta[co_chomharra_x]==1&&tagaichean_Liosta[세로좌표]==1&&SECOND_VALUE[co_chomharra_x]==SECOND_VALUE[세로좌표]&&!memcmp(dàta+첫째값[co_chomharra_x],dàta+첫째값[세로좌표],SECOND_VALUE[co_chomharra_x]);}
static void 내보내기(const char*faidhle_cur_a_steach,...){if(잘못됨)return;va_list argamaid_ARRAY;va_start(argamaid_ARRAY,faidhle_cur_a_steach);int nì_COUNT=vsnprintf(SMS+meud_an_teacsa,sizeof(SMS)-meud_an_teacsa,faidhle_cur_a_steach,argamaid_ARRAY);va_end(argamaid_ARRAY);if(nì_COUNT<0||(unsigned)nì_COUNT>=sizeof(SMS)-meud_an_teacsa){잘못됨=1;return;}meud_an_teacsa+=nì_COUNT;}
static int 서술자(unsigned aithnichear_VALUE,int*tomhas){
    if(aithnichear_VALUE<1||aithnichear_VALUE>=상수모음||tagaichean_Liosta[aithnichear_VALUE]!=1)return -1;unsigned dàta_suidhich=첫째값[aithnichear_VALUE],crìochnaich_OFFSET=dàta_suidhich+SECOND_VALUE[aithnichear_VALUE];if(dàta_suidhich>=crìochnaich_OFFSET||dàta[dàta_suidhich++]!='(')return -1;int cur_a_steach_COUNT=0;
    while(dàta_suidhich<crìochnaich_OFFSET&&dàta[dàta_suidhich]!=')'){
        unsigned còd_a_charactair=dàta[dàta_suidhich++];while(còd_a_charactair=='['&&dàta_suidhich<crìochnaich_OFFSET)còd_a_charactair=dàta[dàta_suidhich++];
        if(còd_a_charactair=='L'){while(dàta_suidhich<crìochnaich_OFFSET&&dàta[dàta_suidhich]!=';')dàta_suidhich++;if(dàta_suidhich==crìochnaich_OFFSET)return -1;dàta_suidhich++;}
        else if(còd_a_charactair!='I'&&còd_a_charactair!='Z'&&còd_a_charactair!='B'&&còd_a_charactair!='C'&&còd_a_charactair!='S')return -1;
        if(++cur_a_steach_COUNT>16)return -1;
    }
    if(dàta_suidhich+1>=crìochnaich_OFFSET||dàta[dàta_suidhich++]!=')')return -1;*tomhas=dàta[dàta_suidhich]=='V'?0:1;
    if(dàta[dàta_suidhich]=='J'||dàta[dàta_suidhich]=='D'||dàta[dàta_suidhich]=='F')return -1;return cur_a_steach_COUNT;
}
static void 속성들(void){unsigned nì_COUNT=절반값();for(unsigned 순번=0;순번<nì_COUNT&&!잘못됨;순번++){절반값();unsigned atharraich_am_meud=가득참();TAKE_VALUE(atharraich_am_meud);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned mion_aoiseach_tionndadh=절반값(),판번호=절반값();if(mion_aoiseach_tionndadh||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        tagaichean_Liosta[순번]=baidht_dàta();switch(tagaichean_Liosta[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=baidht_dàta();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||tagaichean_Liosta[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||tagaichean_Liosta[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();ainm_raoin[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned cur_a_steach_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<cur_a_steach_COUNT&&!잘못됨;안쪽순번++){
            unsigned Ainm=절반값(),atharraich_am_meud=가득참();
            if(UNICODE_VALUE(Ainm,"ConstantValue")){if(atharraich_am_meud!=2)return -1;raon_cunbhalachan[순번]=절반값();}
            else TAKE_VALUE(atharraich_am_meud);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        dòigh_cur_a_steach*buidheann_atharraich_am_meud=메소드목록+순번;buidheann_atharraich_am_meud->설정비트=절반값();buidheann_atharraich_am_meud->Ainm=절반값();buidheann_atharraich_am_meud->서술값=절반값();unsigned cur_a_steach_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<cur_a_steach_COUNT&&!잘못됨;안쪽순번++){
            unsigned Ainm=절반값(),atharraich_am_meud=가득참(),ruith=현재위치;
            if(atharraich_am_meud>faid_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(Ainm,"Code")){
                buidheann_atharraich_am_meud->stac_stòras=절반값();buidheann_atharraich_am_meud->지역변수들=절반값();buidheann_atharraich_am_meud->atharraich_am_meud=가득참();buidheann_atharraich_am_meud->treòrachadh_SEQUENCE=TAKE_VALUE(buidheann_atharraich_am_meud->atharraich_am_meud);
                if(buidheann_atharraich_am_meud->stac_stòras>128||buidheann_atharraich_am_meud->지역변수들>128||buidheann_atharraich_am_meud->atharraich_am_meud>8192||절반값())return -1;속성들();
            }else TAKE_VALUE(atharraich_am_meud);
            if(현재위치!=ruith+atharraich_am_meud)return -1;
        }
        if(!UNICODE_VALUE(buidheann_atharraich_am_meud->Ainm,"<init>")&&(!(buidheann_atharraich_am_meud->설정비트&8)||(buidheann_atharraich_am_meud->설정비트&(0x100|0x20))||!buidheann_atharraich_am_meud->atharraich_am_meud))return -1;
    }
    속성들();return 잘못됨||현재위치!=faid_VALUE?-1:0;
}
static void cunbhalachan_VALUE(unsigned aithnichear_VALUE){
    if(!aithnichear_VALUE||aithnichear_VALUE>=상수모음){잘못됨=1;return;}
    if(tagaichean_Liosta[aithnichear_VALUE]==3)내보내기("P(%uU);",첫째값[aithnichear_VALUE]);
    else if(tagaichean_Liosta[aithnichear_VALUE]==8)내보내기("P((W)k%u);",aithnichear_VALUE);else 잘못됨=1;
}
static void 호출(unsigned aithnichear_VALUE,int mas_fhìor_CALL){
    if(aithnichear_VALUE<1||aithnichear_VALUE>=상수모음||(tagaichean_Liosta[aithnichear_VALUE]!=10&&tagaichean_Liosta[aithnichear_VALUE]!=11)||첫째값[aithnichear_VALUE]<1||첫째값[aithnichear_VALUE]>=상수모음||tagaichean_Liosta[첫째값[aithnichear_VALUE]]!=7||SECOND_VALUE[aithnichear_VALUE]<1||SECOND_VALUE[aithnichear_VALUE]>=상수모음||tagaichean_Liosta[SECOND_VALUE[aithnichear_VALUE]]!=12){잘못됨=1;return;}
    unsigned sealbhadair_nì=첫째값[첫째값[aithnichear_VALUE]],Ainm=첫째값[SECOND_VALUE[aithnichear_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[aithnichear_VALUE]];int tomhas=0,nì_COUNT=서술자(서술값,&tomhas);if(nì_COUNT<0){잘못됨=1;return;}
    for(int 순번=nì_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(mas_fhìor_CALL)내보내기("Q();");
    if(!mas_fhìor_CALL&&같음(sealbhadair_nì,첫째값[현재클래스])){
        unsigned buidheann_atharraich_am_meud=0;for(;buidheann_atharraich_am_meud<메소드개수;buidheann_atharraich_am_meud++)if(같음(Ainm,메소드목록[buidheann_atharraich_am_meud].Ainm)&&같음(서술값,메소드목록[buidheann_atharraich_am_meud].서술값))break;
        if(buidheann_atharraich_am_meud==메소드개수||!(메소드목록[buidheann_atharraich_am_meud].설정비트&8)){잘못됨=1;return;}
        if(tomhas)내보내기("P(");내보내기("m%u(",buidheann_atharraich_am_meud);for(int 순번=0;순번<nì_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(tomhas?"));":" );");return;
    }
    if((mas_fhìor_CALL&&UNICODE_VALUE(sealbhadair_nì,"java/io/PrintStream")&& (UNICODE_VALUE(Ainm,"print")||UNICODE_VALUE(Ainm,"println")))||(!mas_fhìor_CALL&&UNICODE_VALUE(sealbhadair_nì,"한국어/자체/출력"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Ainm,"print")||UNICODE_VALUE(Ainm,"println")||UNICODE_VALUE(Ainm,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Ainm,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Ainm,"print")||UNICODE_VALUE(Ainm,"println")||UNICODE_VALUE(Ainm,"sgrìobh")||UNICODE_VALUE(Ainm,"sgrìobh_loidhne"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Ainm,"print")||UNICODE_VALUE(Ainm,"sgrìobh")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Ainm,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!mas_fhìor_CALL&&UNICODE_VALUE(sealbhadair_nì,"한국어/자체/faidhle")){
        if(UNICODE_VALUE(Ainm,"sgrìobh")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Ainm,"읽기")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void tog_dòigh(unsigned LOOKUP_INDEX){
    dòigh_cur_a_steach*buidheann_atharraich_am_meud=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(buidheann_atharraich_am_meud->Ainm,"<init>"))return;int tomhas,nì_COUNT=서술자(buidheann_atharraich_am_meud->서술값,&tomhas);if(nì_COUNT<0){잘못됨=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<nì_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!nì_COUNT)내보내기("void");
    if((unsigned)nì_COUNT>buidheann_atharraich_am_meud->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",buidheann_atharraich_am_meud->지역변수들?buidheann_atharraich_am_meud->지역변수들:1);for(int 순번=0;순번<nì_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=faid_VALUE;faid_VALUE=buidheann_atharraich_am_meud->treòrachadh_SEQUENCE+buidheann_atharraich_am_meud->atharraich_am_meud;현재위치=buidheann_atharraich_am_meud->treòrachadh_SEQUENCE;
    while(현재위치<faid_VALUE&&!잘못됨){unsigned àithne_suidhich=현재위치-buidheann_atharraich_am_meud->treòrachadh_SEQUENCE,obrachadh_VALUE=baidht_dàta();내보내기("L%u:;",àithne_suidhich);
        if(obrachadh_VALUE==0){}
        else if(obrachadh_VALUE==1)내보내기("P(0);");
        else if(obrachadh_VALUE>=2&&obrachadh_VALUE<=8)내보내기("P(%uU);",obrachadh_VALUE-3);
        else if(obrachadh_VALUE==16){int VALUE=(int8_t)baidht_dàta();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(obrachadh_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(obrachadh_VALUE==18||obrachadh_VALUE==19)cunbhalachan_VALUE(obrachadh_VALUE==18?baidht_dàta():절반값());
        else if(obrachadh_VALUE==21||obrachadh_VALUE==25){unsigned 순번=baidht_dàta();if(순번>=buidheann_atharraich_am_meud->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((obrachadh_VALUE>=26&&obrachadh_VALUE<=29)||(obrachadh_VALUE>=42&&obrachadh_VALUE<=45)){unsigned 순번=obrachadh_VALUE>=42?obrachadh_VALUE-42:obrachadh_VALUE-26;if(순번>=buidheann_atharraich_am_meud->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(obrachadh_VALUE==54||obrachadh_VALUE==58){unsigned 순번=baidht_dàta();if(순번>=buidheann_atharraich_am_meud->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((obrachadh_VALUE>=59&&obrachadh_VALUE<=62)||(obrachadh_VALUE>=75&&obrachadh_VALUE<=78)){unsigned 순번=obrachadh_VALUE>=75?obrachadh_VALUE-75:obrachadh_VALUE-59;if(순번>=buidheann_atharraich_am_meud->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(obrachadh_VALUE==46||obrachadh_VALUE==50||obrachadh_VALUE==51||obrachadh_VALUE==52||obrachadh_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(obrachadh_VALUE==79||obrachadh_VALUE==83||obrachadh_VALUE==84||obrachadh_VALUE==85||obrachadh_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",obrachadh_VALUE==84?"(unsigned)(signed char)q":obrachadh_VALUE==85?"(unsigned short)q":obrachadh_VALUE==86?"(unsigned)(short)q":"q");
        else if(obrachadh_VALUE==87)내보내기("Q();");
        else if(obrachadh_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(obrachadh_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(obrachadh_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(obrachadh_VALUE==96||obrachadh_VALUE==100||obrachadh_VALUE==104||obrachadh_VALUE==120||obrachadh_VALUE==124||obrachadh_VALUE==126||obrachadh_VALUE==128||obrachadh_VALUE==130){const char*còdachadh_VALUE=obrachadh_VALUE==96?"+":obrachadh_VALUE==100?"-":obrachadh_VALUE==104?"*":obrachadh_VALUE==120?"<<":obrachadh_VALUE==124?">>":obrachadh_VALUE==126?"&":obrachadh_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",còdachadh_VALUE,obrachadh_VALUE==120||obrachadh_VALUE==124?"%32":"");}
        else if(obrachadh_VALUE==108||obrachadh_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",obrachadh_VALUE==112);
        else if(obrachadh_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(obrachadh_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(obrachadh_VALUE==132){unsigned 순번=baidht_dàta();int 차이=(int8_t)baidht_dàta();if(순번>=buidheann_atharraich_am_meud->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(obrachadh_VALUE>=145&&obrachadh_VALUE<=147)내보내기("P((unsigned)(%s)Q());",obrachadh_VALUE==145?"signed char":obrachadh_VALUE==146?"unsigned short":"short");
        else if(obrachadh_VALUE>=153&&obrachadh_VALUE<=166){int targaid=(int)àithne_suidhich+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(targaid<0||targaid>=(int)buidheann_atharraich_am_meud->atharraich_am_meud){잘못됨=1;break;}if(obrachadh_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[obrachadh_VALUE-153],targaid);else if(obrachadh_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[obrachadh_VALUE-159],targaid);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",obrachadh_VALUE==165?"==":"!=",targaid);}
        else if(obrachadh_VALUE==167){int targaid=(int)àithne_suidhich+(int16_t)절반값();if(targaid<0||targaid>=(int)buidheann_atharraich_am_meud->atharraich_am_meud)잘못됨=1;내보내기("goto L%d;",targaid);}
        else if(obrachadh_VALUE==172||obrachadh_VALUE==176)내보내기("return Q();");else if(obrachadh_VALUE==177)내보내기("return 0;");
        else if(obrachadh_VALUE==178||obrachadh_VALUE==179){unsigned aithnichear_VALUE=절반값();if(aithnichear_VALUE<1||aithnichear_VALUE>=상수모음||tagaichean_Liosta[aithnichear_VALUE]!=9||첫째값[aithnichear_VALUE]>=상수모음||SECOND_VALUE[aithnichear_VALUE]>=상수모음||tagaichean_Liosta[첫째값[aithnichear_VALUE]]!=7||tagaichean_Liosta[SECOND_VALUE[aithnichear_VALUE]]!=12){잘못됨=1;break;}unsigned sealbhadair_nì=첫째값[첫째값[aithnichear_VALUE]],Ainm=첫째값[SECOND_VALUE[aithnichear_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[aithnichear_VALUE]];
            if(obrachadh_VALUE==178&&UNICODE_VALUE(sealbhadair_nì,"java/lang/System")&&UNICODE_VALUE(Ainm,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned faidhle_cur_a_steach=0;while(faidhle_cur_a_steach<필드개수&&(!같음(Ainm,ainm_raoin[faidhle_cur_a_steach])||!같음(서술값,필드서술[faidhle_cur_a_steach])))faidhle_cur_a_steach++;if(!같음(sealbhadair_nì,첫째값[현재클래스])||faidhle_cur_a_steach==필드개수){잘못됨=1;break;}내보내기(obrachadh_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",faidhle_cur_a_steach);}}
        else if(obrachadh_VALUE==182||obrachadh_VALUE==184)호출(절반값(),obrachadh_VALUE==182);
        else if(obrachadh_VALUE==188){unsigned TYPE_roinn_seòrsa=baidht_dàta();if(TYPE_roinn_seòrsa!=4&&TYPE_roinn_seòrsa!=5&&TYPE_roinn_seòrsa!=8&&TYPE_roinn_seòrsa!=9&&TYPE_roinn_seòrsa!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(obrachadh_VALUE==190)내보내기("P(jlength(Q()));");
        else if(obrachadh_VALUE==198||obrachadh_VALUE==199){int targaid=(int)àithne_suidhich+(int16_t)절반값();if(targaid<0||targaid>=(int)buidheann_atharraich_am_meud->atharraich_am_meud)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",obrachadh_VALUE==198?"==":"!=",targaid);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,obrachadh_VALUE,àithne_suidhich);
        내보내기("\n");
    }
    faid_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned sreang_leasan(unsigned *dàta_suidhich,unsigned crìochnaich_OFFSET){
    if(*dàta_suidhich>=crìochnaich_OFFSET){잘못됨=1;return 0;}unsigned còd_a_charactair=dàta[(*dàta_suidhich)++];
    if(còd_a_charactair<128)return còd_a_charactair;
    unsigned nì_COUNT=còd_a_charactair>=0xc0&&còd_a_charactair<=0xdf?1:còd_a_charactair>=0xe0&&còd_a_charactair<=0xef?2:3;
    if(nì_COUNT==3||nì_COUNT>crìochnaich_OFFSET-*dàta_suidhich){잘못됨=1;return 0;}unsigned VALUE=còd_a_charactair&((1u<<(6-nì_COUNT))-1);
    for(unsigned 순번=0;순번<nì_COUNT;순번++){unsigned air_adhart_nì=dàta[(*dàta_suidhich)++];if((air_adhart_nì&0xc0)!=0x80)잘못됨=1;VALUE=VALUE<<6|(air_adhart_nì&63);}
    if((nì_COUNT==1&&VALUE<128&&VALUE!=0)||(nì_COUNT==2&&VALUE<2048))잘못됨=1;return VALUE;
}
static void sreang_cunbhalachan(unsigned aithnichear_VALUE){
    unsigned 부호없는값=첫째값[aithnichear_VALUE];if(부호없는값<1||부호없는값>=상수모음||tagaichean_Liosta[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",aithnichear_VALUE);
    unsigned dàta_suidhich=첫째값[부호없는값],crìochnaich_OFFSET=dàta_suidhich+SECOND_VALUE[부호없는값];
    while(dàta_suidhich<crìochnaich_OFFSET&&!잘못됨){unsigned còd_a_charactair=sreang_leasan(&dàta_suidhich,crìochnaich_OFFSET);
        if(còd_a_charactair>=0xd800&&còd_a_charactair<=0xdbff){unsigned 낮은부분=sreang_leasan(&dàta_suidhich,crìochnaich_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}còd_a_charactair=0x10000+((còd_a_charactair-0xd800)<<10)+낮은부분-0xdc00;}
        else if(còd_a_charactair>=0xdc00&&còd_a_charactair<=0xdfff){잘못됨=1;break;}
        if(!còd_a_charactair){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(còd_a_charactair<128)내보내기("%u,",còd_a_charactair);
        else{unsigned nì_COUNT=còd_a_charactair<2048?2:còd_a_charactair<65536?3:4;내보내기("%u,",(nì_COUNT==2?0xc0:nì_COUNT==3?0xe0:0xf0)|(còd_a_charactair>>(6*(nì_COUNT-1))));for(unsigned 순번=nì_COUNT-1;순번;순번--)내보내기("%u,",0x80|((còd_a_charactair>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Ainm){
    size_t nì_COUNT=strlen(Ainm);
    if(nì_COUNT>4&&!strcmp(Ainm+nì_COUNT-4,".jar")){
        if(꾸러미열기(Ainm)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Slighe[256];const char*cur_a_steach_dòigh=꾸러미진입클래스();nì_COUNT=strlen(cur_a_steach_dòigh);if(nì_COUNT+6>=sizeof(Slighe))return 0;
        for(unsigned 순번=0;순번<nì_COUNT;순번++)Slighe[순번]=cur_a_steach_dòigh[순번]=='.'?'/':cur_a_steach_dòigh[순번];strcpy(Slighe+nì_COUNT,".class");int cur_a_steach_COUNT=꾸러미읽기(Slighe,dàta,sizeof(dàta));if(cur_a_steach_COUNT<0)return 0;faid_VALUE=cur_a_steach_COUNT;
    }else{intptr_t faidhle_làmhrachan=사용자호출(3,(uintptr_t)Ainm,0,0,0,0,0);if(faidhle_làmhrachan<0)return 0;intptr_t cur_a_steach_COUNT=사용자호출(9,faidhle_làmhrachan,0,0,0,0,0);if(cur_a_steach_COUNT<0||cur_a_steach_COUNT>sizeof(dàta)){사용자호출(4,faidhle_làmhrachan,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,faidhle_làmhrachan,(uintptr_t)dàta,cur_a_steach_COUNT,0,0,0);사용자호출(4,faidhle_làmhrachan,0,0,0,0,0);if(RECEIVED_COUNT!=cur_a_steach_COUNT)return 0;faid_VALUE=cur_a_steach_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(tagaichean_Liosta[순번]==8)sreang_cunbhalachan(순번);
    if(잘못됨)return 0;
    int cur_a_steach_puing=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Ainm,"<init>")){
        int tomhas,cur_a_steach_COUNT=서술자(메소드목록[순번].서술값,&tomhas);if(cur_a_steach_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<cur_a_steach_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!cur_a_steach_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Ainm,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)cur_a_steach_puing=순번;
        if(UNICODE_VALUE(메소드목록[순번].Ainm,"<clinit>"))초기값=순번;
    }
    if(cur_a_steach_puing<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)tog_dòigh(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(raon_cunbhalachan[순번]){
        unsigned còd_a_charactair=raon_cunbhalachan[순번];if(còd_a_charactair>=상수모음)return 0;
        if(tagaichean_Liosta[còd_a_charactair]==3)내보내기("fields[%u]=%uU;",순번,첫째값[còd_a_charactair]);else if(tagaichean_Liosta[còd_a_charactair]==8)내보내기("fields[%u]=(W)k%u;",순번,còd_a_charactair);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",cur_a_steach_puing);
    return 잘못됨?0:SMS;
}
