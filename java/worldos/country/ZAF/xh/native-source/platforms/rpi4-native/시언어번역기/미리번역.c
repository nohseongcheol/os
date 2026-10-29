#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "umqulu.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char iingcombolo[16384];static unsigned ubude_ixabiso,현재위치;static int 잘못됨;
static unsigned iimpawu_uludwe[512],첫째값[512],둘째값[512],상수모음,현재클래스;
static char Umbhalo[65536];static unsigned isayizi_yombhalo;
typedef struct {unsigned 설정비트,Igama,서술값,umyalelo_ULANDELELWANO,Ubukhulu,지역변수들,fumba_Ugcino;} imethodi_ufako_nkcukacha;
static imethodi_ufako_nkcukacha 메소드목록[64];static unsigned 메소드개수;
static unsigned igama_lefildi[64],필드서술[64],ifildi_engajikiyo[64],필드개수;
static unsigned 가져오기(unsigned 개수){if(현재위치>ubude_ixabiso||개수>ubude_ixabiso-현재위치){잘못됨=1;return 0;}unsigned 자료위치=현재위치;현재위치+=개수;return 자료위치;}
static unsigned ibhayithi_iingcombolo(void){unsigned 자료위치=가져오기(1);return 잘못됨?0:iingcombolo[자료위치];}
static unsigned 절반값(void){unsigned isilungelelanisi_x=ibhayithi_iingcombolo();return isilungelelanisi_x<<8|ibhayithi_iingcombolo();}
static uint32_t 가득참(void){uint32_t isilungelelanisi_x=절반값();return isilungelelanisi_x<<16|절반값();}
static int ikhowudi_efanayo_ixabiso(unsigned 순번,const char*uluhlu_lweekharektha_iingcombolo){return 순번>0&&순번<상수모음&&iimpawu_uludwe[순번]==1&&strlen(uluhlu_lweekharektha_iingcombolo)==둘째값[순번]&&!memcmp(iingcombolo+첫째값[순번],uluhlu_lweekharektha_iingcombolo,둘째값[순번]);}
static int 같음(unsigned isilungelelanisi_x,unsigned 세로좌표){return isilungelelanisi_x>0&&isilungelelanisi_x<상수모음&&세로좌표>0&&세로좌표<상수모음&&iimpawu_uludwe[isilungelelanisi_x]==1&&iimpawu_uludwe[세로좌표]==1&&둘째값[isilungelelanisi_x]==둘째값[세로좌표]&&!memcmp(iingcombolo+첫째값[isilungelelanisi_x],iingcombolo+첫째값[세로좌표],둘째값[isilungelelanisi_x]);}
static void 내보내기(const char*ifayile_ufako_nkcukacha,...){if(잘못됨)return;va_list isiniki_myalelo_ULUHLU;va_start(isiniki_myalelo_ULUHLU,ifayile_ufako_nkcukacha);int 개수=vsnprintf(Umbhalo+isayizi_yombhalo,sizeof(Umbhalo)-isayizi_yombhalo,ifayile_ufako_nkcukacha,isiniki_myalelo_ULUHLU);va_end(isiniki_myalelo_ULUHLU);if(개수<0||(unsigned)개수>=sizeof(Umbhalo)-isayizi_yombhalo){잘못됨=1;return;}isayizi_yombhalo+=개수;}
static int 서술자(unsigned isalathisi_ixabiso,int*결과){
    if(isalathisi_ixabiso<1||isalathisi_ixabiso>=상수모음||iimpawu_uludwe[isalathisi_ixabiso]!=1)return -1;unsigned 자료위치=첫째값[isalathisi_ixabiso],phela_Ukulinganisa=자료위치+둘째값[isalathisi_ixabiso];if(자료위치>=phela_Ukulinganisa||iingcombolo[자료위치++]!='(')return -1;int 항목수=0;
    while(자료위치<phela_Ukulinganisa&&iingcombolo[자료위치]!=')'){
        unsigned ikhowudi_yekharakhtha=iingcombolo[자료위치++];while(ikhowudi_yekharakhtha=='['&&자료위치<phela_Ukulinganisa)ikhowudi_yekharakhtha=iingcombolo[자료위치++];
        if(ikhowudi_yekharakhtha=='L'){while(자료위치<phela_Ukulinganisa&&iingcombolo[자료위치]!=';')자료위치++;if(자료위치==phela_Ukulinganisa)return -1;자료위치++;}
        else if(ikhowudi_yekharakhtha!='I'&&ikhowudi_yekharakhtha!='Z'&&ikhowudi_yekharakhtha!='B'&&ikhowudi_yekharakhtha!='C'&&ikhowudi_yekharakhtha!='S')return -1;
        if(++항목수>16)return -1;
    }
    if(자료위치+1>=phela_Ukulinganisa||iingcombolo[자료위치++]!=')')return -1;*결과=iingcombolo[자료위치]=='V'?0:1;
    if(iingcombolo[자료위치]=='J'||iingcombolo[자료위치]=='D'||iingcombolo[자료위치]=='F')return -1;return 항목수;
}
static void 속성들(void){unsigned 개수=절반값();for(unsigned 순번=0;순번<개수&&!잘못됨;순번++){절반값();unsigned Ubukhulu=가득참();가져오기(Ubukhulu);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned umntwana_inguqulelo=절반값(),판번호=절반값();if(umntwana_inguqulelo||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        iimpawu_uludwe[순번]=ibhayithi_iingcombolo();switch(iimpawu_uludwe[순번]){
        case 1:둘째값[순번]=절반값();첫째값[순번]=가져오기(둘째값[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:가져오기(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();둘째값[순번]=절반값();break;
        case 15:첫째값[순번]=ibhayithi_iingcombolo();둘째값[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||iimpawu_uludwe[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||iimpawu_uludwe[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();가져오기(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();igama_lefildi[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned 항목수=절반값();for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Igama=절반값(),Ubukhulu=가득참();
            if(ikhowudi_efanayo_ixabiso(Igama,"ConstantValue")){if(Ubukhulu!=2)return -1;ifildi_engajikiyo[순번]=절반값();}
            else 가져오기(Ubukhulu);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        imethodi_ufako_nkcukacha*iqela_isayizi=메소드목록+순번;iqela_isayizi->설정비트=절반값();iqela_isayizi->Igama=절반값();iqela_isayizi->서술값=절반값();unsigned 항목수=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<항목수&&!잘못됨;안쪽순번++){
            unsigned Igama=절반값(),Ubukhulu=가득참(),Phumeza=현재위치;
            if(Ubukhulu>ubude_ixabiso-현재위치)return -1;
            if(ikhowudi_efanayo_ixabiso(Igama,"Code")){
                iqela_isayizi->fumba_Ugcino=절반값();iqela_isayizi->지역변수들=절반값();iqela_isayizi->Ubukhulu=가득참();iqela_isayizi->umyalelo_ULANDELELWANO=가져오기(iqela_isayizi->Ubukhulu);
                if(iqela_isayizi->fumba_Ugcino>128||iqela_isayizi->지역변수들>128||iqela_isayizi->Ubukhulu>8192||절반값())return -1;속성들();
            }else 가져오기(Ubukhulu);
            if(현재위치!=Phumeza+Ubukhulu)return -1;
        }
        if(!ikhowudi_efanayo_ixabiso(iqela_isayizi->Igama,"<init>")&&(!(iqela_isayizi->설정비트&8)||(iqela_isayizi->설정비트&(0x100|0x20))||!iqela_isayizi->Ubukhulu))return -1;
    }
    속성들();return 잘못됨||현재위치!=ubude_ixabiso?-1:0;
}
static void engajikiyo_ixabiso(unsigned isalathisi_ixabiso){
    if(!isalathisi_ixabiso||isalathisi_ixabiso>=상수모음){잘못됨=1;return;}
    if(iimpawu_uludwe[isalathisi_ixabiso]==3)내보내기("P(%uU);",첫째값[isalathisi_ixabiso]);
    else if(iimpawu_uludwe[isalathisi_ixabiso]==8)내보내기("P((W)k%u);",isalathisi_ixabiso);else 잘못됨=1;
}
static void 호출(unsigned isalathisi_ixabiso,int enembonakalo_yenyani_fowuna){
    if(isalathisi_ixabiso<1||isalathisi_ixabiso>=상수모음||(iimpawu_uludwe[isalathisi_ixabiso]!=10&&iimpawu_uludwe[isalathisi_ixabiso]!=11)||첫째값[isalathisi_ixabiso]<1||첫째값[isalathisi_ixabiso]>=상수모음||iimpawu_uludwe[첫째값[isalathisi_ixabiso]]!=7||둘째값[isalathisi_ixabiso]<1||둘째값[isalathisi_ixabiso]>=상수모음||iimpawu_uludwe[둘째값[isalathisi_ixabiso]]!=12){잘못됨=1;return;}
    unsigned umnini_into=첫째값[첫째값[isalathisi_ixabiso]],Igama=첫째값[둘째값[isalathisi_ixabiso]],서술값=둘째값[둘째값[isalathisi_ixabiso]];int 결과=0,개수=서술자(서술값,&결과);if(개수<0){잘못됨=1;return;}
    for(int 순번=개수;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(enembonakalo_yenyani_fowuna)내보내기("Q();");
    if(!enembonakalo_yenyani_fowuna&&같음(umnini_into,첫째값[현재클래스])){
        unsigned iqela_isayizi=0;for(;iqela_isayizi<메소드개수;iqela_isayizi++)if(같음(Igama,메소드목록[iqela_isayizi].Igama)&&같음(서술값,메소드목록[iqela_isayizi].서술값))break;
        if(iqela_isayizi==메소드개수||!(메소드목록[iqela_isayizi].설정비트&8)){잘못됨=1;return;}
        if(결과)내보내기("P(");내보내기("m%u(",iqela_isayizi);for(int 순번=0;순번<개수;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(결과?"));":" );");return;
    }
    if((enembonakalo_yenyani_fowuna&&ikhowudi_efanayo_ixabiso(umnini_into,"java/io/PrintStream")&& (ikhowudi_efanayo_ixabiso(Igama,"print")||ikhowudi_efanayo_ixabiso(Igama,"println")))||(!enembonakalo_yenyani_fowuna&&ikhowudi_efanayo_ixabiso(umnini_into,"isiXhosa/자체/출력"))){
        if(ikhowudi_efanayo_ixabiso(서술값,"(I)V")&&(ikhowudi_efanayo_ixabiso(Igama,"print")||ikhowudi_efanayo_ixabiso(Igama,"println")||ikhowudi_efanayo_ixabiso(Igama,"수쓰기"))){내보내기("jprint(x[0],1,%d);",ikhowudi_efanayo_ixabiso(Igama,"print")?0:1);return;}
        if(ikhowudi_efanayo_ixabiso(서술값,"(Ljava/lang/String;)V")&&(ikhowudi_efanayo_ixabiso(Igama,"print")||ikhowudi_efanayo_ixabiso(Igama,"println")||ikhowudi_efanayo_ixabiso(Igama,"Bhala")||ikhowudi_efanayo_ixabiso(Igama,"bhala_umgca"))){내보내기("jprint(x[0],0,%d);",ikhowudi_efanayo_ixabiso(Igama,"print")||ikhowudi_efanayo_ixabiso(Igama,"Bhala")?0:1);return;}
        if(ikhowudi_efanayo_ixabiso(서술값,"()V")&&ikhowudi_efanayo_ixabiso(Igama,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!enembonakalo_yenyani_fowuna&&ikhowudi_efanayo_ixabiso(umnini_into,"isiXhosa/자체/iFayili")){
        if(ikhowudi_efanayo_ixabiso(Igama,"Bhala")&&ikhowudi_efanayo_ixabiso(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(ikhowudi_efanayo_ixabiso(Igama,"Funda")&&ikhowudi_efanayo_ixabiso(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void yakha_imethodi(unsigned 색인){
    imethodi_ufako_nkcukacha*iqela_isayizi=메소드목록+색인;if(ikhowudi_efanayo_ixabiso(iqela_isayizi->Igama,"<init>"))return;int 결과,개수=서술자(iqela_isayizi->서술값,&결과);if(개수<0){잘못됨=1;return;}
    내보내기("static W m%u(",색인);for(int 순번=0;순번<개수;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!개수)내보내기("void");
    if((unsigned)개수>iqela_isayizi->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",iqela_isayizi->지역변수들?iqela_isayizi->지역변수들:1);for(int 순번=0;순번<개수;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=ubude_ixabiso;ubude_ixabiso=iqela_isayizi->umyalelo_ULANDELELWANO+iqela_isayizi->Ubukhulu;현재위치=iqela_isayizi->umyalelo_ULANDELELWANO;
    while(현재위치<ubude_ixabiso&&!잘못됨){unsigned 명령위치=현재위치-iqela_isayizi->umyalelo_ULANDELELWANO,isibalo_ixabiso=ibhayithi_iingcombolo();내보내기("L%u:;",명령위치);
        if(isibalo_ixabiso==0){}
        else if(isibalo_ixabiso==1)내보내기("P(0);");
        else if(isibalo_ixabiso>=2&&isibalo_ixabiso<=8)내보내기("P(%uU);",isibalo_ixabiso-3);
        else if(isibalo_ixabiso==16){int ixabiso=(int8_t)ibhayithi_iingcombolo();내보내기("P(%uU);",(unsigned)ixabiso);}
        else if(isibalo_ixabiso==17){int ixabiso=(int16_t)절반값();내보내기("P(%uU);",(unsigned)ixabiso);}
        else if(isibalo_ixabiso==18||isibalo_ixabiso==19)engajikiyo_ixabiso(isibalo_ixabiso==18?ibhayithi_iingcombolo():절반값());
        else if(isibalo_ixabiso==21||isibalo_ixabiso==25){unsigned 순번=ibhayithi_iingcombolo();if(순번>=iqela_isayizi->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((isibalo_ixabiso>=26&&isibalo_ixabiso<=29)||(isibalo_ixabiso>=42&&isibalo_ixabiso<=45)){unsigned 순번=isibalo_ixabiso>=42?isibalo_ixabiso-42:isibalo_ixabiso-26;if(순번>=iqela_isayizi->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(isibalo_ixabiso==54||isibalo_ixabiso==58){unsigned 순번=ibhayithi_iingcombolo();if(순번>=iqela_isayizi->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((isibalo_ixabiso>=59&&isibalo_ixabiso<=62)||(isibalo_ixabiso>=75&&isibalo_ixabiso<=78)){unsigned 순번=isibalo_ixabiso>=75?isibalo_ixabiso-75:isibalo_ixabiso-59;if(순번>=iqela_isayizi->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(isibalo_ixabiso==46||isibalo_ixabiso==50||isibalo_ixabiso==51||isibalo_ixabiso==52||isibalo_ixabiso==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(isibalo_ixabiso==79||isibalo_ixabiso==83||isibalo_ixabiso==84||isibalo_ixabiso==85||isibalo_ixabiso==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",isibalo_ixabiso==84?"(unsigned)(signed char)q":isibalo_ixabiso==85?"(unsigned short)q":isibalo_ixabiso==86?"(unsigned)(short)q":"q");
        else if(isibalo_ixabiso==87)내보내기("Q();");
        else if(isibalo_ixabiso==89)내보내기("q=Q();P(q);P(q);");
        else if(isibalo_ixabiso==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(isibalo_ixabiso==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(isibalo_ixabiso==96||isibalo_ixabiso==100||isibalo_ixabiso==104||isibalo_ixabiso==120||isibalo_ixabiso==124||isibalo_ixabiso==126||isibalo_ixabiso==128||isibalo_ixabiso==130){const char*ujiko_nkcukacha_zibe_ziikhowudi_ixabiso=isibalo_ixabiso==96?"+":isibalo_ixabiso==100?"-":isibalo_ixabiso==104?"*":isibalo_ixabiso==120?"<<":isibalo_ixabiso==124?">>":isibalo_ixabiso==126?"&":isibalo_ixabiso==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",ujiko_nkcukacha_zibe_ziikhowudi_ixabiso,isibalo_ixabiso==120||isibalo_ixabiso==124?"%32":"");}
        else if(isibalo_ixabiso==108||isibalo_ixabiso==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",isibalo_ixabiso==112);
        else if(isibalo_ixabiso==116)내보내기("P(0U-(unsigned)Q());");
        else if(isibalo_ixabiso==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(isibalo_ixabiso==132){unsigned 순번=ibhayithi_iingcombolo();int 차이=(int8_t)ibhayithi_iingcombolo();if(순번>=iqela_isayizi->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(isibalo_ixabiso>=145&&isibalo_ixabiso<=147)내보내기("P((unsigned)(%s)Q());",isibalo_ixabiso==145?"signed char":isibalo_ixabiso==146?"unsigned short":"short");
        else if(isibalo_ixabiso>=153&&isibalo_ixabiso<=166){int ithagethi=(int)명령위치+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(ithagethi<0||ithagethi>=(int)iqela_isayizi->Ubukhulu){잘못됨=1;break;}if(isibalo_ixabiso<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[isibalo_ixabiso-153],ithagethi);else if(isibalo_ixabiso<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[isibalo_ixabiso-159],ithagethi);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",isibalo_ixabiso==165?"==":"!=",ithagethi);}
        else if(isibalo_ixabiso==167){int ithagethi=(int)명령위치+(int16_t)절반값();if(ithagethi<0||ithagethi>=(int)iqela_isayizi->Ubukhulu)잘못됨=1;내보내기("goto L%d;",ithagethi);}
        else if(isibalo_ixabiso==172||isibalo_ixabiso==176)내보내기("return Q();");else if(isibalo_ixabiso==177)내보내기("return 0;");
        else if(isibalo_ixabiso==178||isibalo_ixabiso==179){unsigned isalathisi_ixabiso=절반값();if(isalathisi_ixabiso<1||isalathisi_ixabiso>=상수모음||iimpawu_uludwe[isalathisi_ixabiso]!=9||첫째값[isalathisi_ixabiso]>=상수모음||둘째값[isalathisi_ixabiso]>=상수모음||iimpawu_uludwe[첫째값[isalathisi_ixabiso]]!=7||iimpawu_uludwe[둘째값[isalathisi_ixabiso]]!=12){잘못됨=1;break;}unsigned umnini_into=첫째값[첫째값[isalathisi_ixabiso]],Igama=첫째값[둘째값[isalathisi_ixabiso]],서술값=둘째값[둘째값[isalathisi_ixabiso]];
            if(isibalo_ixabiso==178&&ikhowudi_efanayo_ixabiso(umnini_into,"java/lang/System")&&ikhowudi_efanayo_ixabiso(Igama,"out")&&ikhowudi_efanayo_ixabiso(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned ifayile_ufako_nkcukacha=0;while(ifayile_ufako_nkcukacha<필드개수&&(!같음(Igama,igama_lefildi[ifayile_ufako_nkcukacha])||!같음(서술값,필드서술[ifayile_ufako_nkcukacha])))ifayile_ufako_nkcukacha++;if(!같음(umnini_into,첫째값[현재클래스])||ifayile_ufako_nkcukacha==필드개수){잘못됨=1;break;}내보내기(isibalo_ixabiso==178?"P(fields[%u]);":"fields[%u]=Q();",ifayile_ufako_nkcukacha);}}
        else if(isibalo_ixabiso==182||isibalo_ixabiso==184)호출(절반값(),isibalo_ixabiso==182);
        else if(isibalo_ixabiso==188){unsigned uhlobo_udidi=ibhayithi_iingcombolo();if(uhlobo_udidi!=4&&uhlobo_udidi!=5&&uhlobo_udidi!=8&&uhlobo_udidi!=9&&uhlobo_udidi!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(isibalo_ixabiso==190)내보내기("P(jlength(Q()));");
        else if(isibalo_ixabiso==198||isibalo_ixabiso==199){int ithagethi=(int)명령위치+(int16_t)절반값();if(ithagethi<0||ithagethi>=(int)iqela_isayizi->Ubukhulu)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",isibalo_ixabiso==198?"==":"!=",ithagethi);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",색인,isibalo_ixabiso,명령위치);
        내보내기("\n");
    }
    ubude_ixabiso=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned uluhlu_lweekharektha_isifundo(unsigned *자료위치,unsigned phela_Ukulinganisa){
    if(*자료위치>=phela_Ukulinganisa){잘못됨=1;return 0;}unsigned ikhowudi_yekharakhtha=iingcombolo[(*자료위치)++];
    if(ikhowudi_yekharakhtha<128)return ikhowudi_yekharakhtha;
    unsigned 개수=ikhowudi_yekharakhtha>=0xc0&&ikhowudi_yekharakhtha<=0xdf?1:ikhowudi_yekharakhtha>=0xe0&&ikhowudi_yekharakhtha<=0xef?2:3;
    if(개수==3||개수>phela_Ukulinganisa-*자료위치){잘못됨=1;return 0;}unsigned ixabiso=ikhowudi_yekharakhtha&((1u<<(6-개수))-1);
    for(unsigned 순번=0;순번<개수;순번++){unsigned 다음=iingcombolo[(*자료위치)++];if((다음&0xc0)!=0x80)잘못됨=1;ixabiso=ixabiso<<6|(다음&63);}
    if((개수==1&&ixabiso<128&&ixabiso!=0)||(개수==2&&ixabiso<2048))잘못됨=1;return ixabiso;
}
static void uluhlu_lweekharektha_engajikiyo(unsigned isalathisi_ixabiso){
    unsigned 부호없는값=첫째값[isalathisi_ixabiso];if(부호없는값<1||부호없는값>=상수모음||iimpawu_uludwe[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",isalathisi_ixabiso);
    unsigned 자료위치=첫째값[부호없는값],phela_Ukulinganisa=자료위치+둘째값[부호없는값];
    while(자료위치<phela_Ukulinganisa&&!잘못됨){unsigned ikhowudi_yekharakhtha=uluhlu_lweekharektha_isifundo(&자료위치,phela_Ukulinganisa);
        if(ikhowudi_yekharakhtha>=0xd800&&ikhowudi_yekharakhtha<=0xdbff){unsigned 낮은부분=uluhlu_lweekharektha_isifundo(&자료위치,phela_Ukulinganisa);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}ikhowudi_yekharakhtha=0x10000+((ikhowudi_yekharakhtha-0xd800)<<10)+낮은부분-0xdc00;}
        else if(ikhowudi_yekharakhtha>=0xdc00&&ikhowudi_yekharakhtha<=0xdfff){잘못됨=1;break;}
        if(!ikhowudi_yekharakhtha){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(ikhowudi_yekharakhtha<128)내보내기("%u,",ikhowudi_yekharakhtha);
        else{unsigned 개수=ikhowudi_yekharakhtha<2048?2:ikhowudi_yekharakhtha<65536?3:4;내보내기("%u,",(개수==2?0xc0:개수==3?0xe0:0xf0)|(ikhowudi_yekharakhtha>>(6*(개수-1))));for(unsigned 순번=개수-1;순번;순번--)내보내기("%u,",0x80|((ikhowudi_yekharakhtha>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Igama){
    size_t 개수=strlen(Igama);
    if(개수>4&&!strcmp(Igama+개수-4,".jar")){
        if(꾸러미열기(Igama)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char INDLELA[256];const char*ufako_nkcukacha_imethodi=꾸러미진입클래스();개수=strlen(ufako_nkcukacha_imethodi);if(개수+6>=sizeof(INDLELA))return 0;
        for(unsigned 순번=0;순번<개수;순번++)INDLELA[순번]=ufako_nkcukacha_imethodi[순번]=='.'?'/':ufako_nkcukacha_imethodi[순번];strcpy(INDLELA+개수,".class");int 항목수=꾸러미읽기(INDLELA,iingcombolo,sizeof(iingcombolo));if(항목수<0)return 0;ubude_ixabiso=항목수;
    }else{intptr_t ifayile_isibambi=사용자호출(3,(uintptr_t)Igama,0,0,0,0,0);if(ifayile_isibambi<0)return 0;intptr_t 항목수=사용자호출(9,ifayile_isibambi,0,0,0,0,0);if(항목수<0||항목수>sizeof(iingcombolo)){사용자호출(4,ifayile_isibambi,0,0,0,0,0);return 0;}intptr_t 받은수=사용자호출(2,ifayile_isibambi,(uintptr_t)iingcombolo,항목수,0,0,0);사용자호출(4,ifayile_isibambi,0,0,0,0,0);if(받은수!=항목수)return 0;ubude_ixabiso=항목수;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(iimpawu_uludwe[순번]==8)uluhlu_lweekharektha_engajikiyo(순번);
    if(잘못됨)return 0;
    int ufako_nkcukacha_inqaku=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!ikhowudi_efanayo_ixabiso(메소드목록[순번].Igama,"<init>")){
        int 결과,항목수=서술자(메소드목록[순번].서술값,&결과);if(항목수<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<항목수;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!항목수)내보내기("void");내보내기(");\n");
        if(ikhowudi_efanayo_ixabiso(메소드목록[순번].Igama,"main")&&ikhowudi_efanayo_ixabiso(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)ufako_nkcukacha_inqaku=순번;
        if(ikhowudi_efanayo_ixabiso(메소드목록[순번].Igama,"<clinit>"))초기값=순번;
    }
    if(ufako_nkcukacha_inqaku<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)yakha_imethodi(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(ifildi_engajikiyo[순번]){
        unsigned ikhowudi_yekharakhtha=ifildi_engajikiyo[순번];if(ikhowudi_yekharakhtha>=상수모음)return 0;
        if(iimpawu_uludwe[ikhowudi_yekharakhtha]==3)내보내기("fields[%u]=%uU;",순번,첫째값[ikhowudi_yekharakhtha]);else if(iimpawu_uludwe[ikhowudi_yekharakhtha]==8)내보내기("fields[%u]=(W)k%u;",순번,ikhowudi_yekharakhtha);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",ufako_nkcukacha_inqaku);
    return 잘못됨?0:Umbhalo;
}
