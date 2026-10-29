#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "beart.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char sonraí[16384];static unsigned fad_VALUE,현재위치;static int teicneolaíocht_faisnéise_neamhbhailí;
static unsigned Catagóirí_Liosta[512],첫째값[512],SECOND_VALUE[512],상수모음,현재클래스;
static char Téacs[65536];static unsigned méid_téacs;
typedef struct {unsigned 설정비트,Ainm,서술값,treoir_SEQUENCE,Méid,지역변수들,Cruach_Stóras;} modh_iontráil;
static modh_iontráil 메소드목록[64];static unsigned 메소드개수;
static unsigned ainm_réimse_98daa19b[64],필드서술[64],réimse_tairiseach[64],필드개수;
static unsigned TAKE_VALUE(unsigned mír_COUNT){if(현재위치>fad_VALUE||mír_COUNT>fad_VALUE-현재위치){teicneolaíocht_faisnéise_neamhbhailí=1;return 0;}unsigned sonraí_suíomh=현재위치;현재위치+=mír_COUNT;return sonraí_suíomh;}
static unsigned beart_sonraí(void){unsigned sonraí_suíomh=TAKE_VALUE(1);return teicneolaíocht_faisnéise_neamhbhailí?0:sonraí[sonraí_suíomh];}
static unsigned 절반값(void){unsigned x_chomhordanáid=beart_sonraí();return x_chomhordanáid<<8|beart_sonraí();}
static uint32_t 가득참(void){uint32_t x_chomhordanáid=절반값();return x_chomhordanáid<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*teaghrán_sonraí){return 순번>0&&순번<상수모음&&Catagóirí_Liosta[순번]==1&&strlen(teaghrán_sonraí)==SECOND_VALUE[순번]&&!memcmp(sonraí+첫째값[순번],teaghrán_sonraí,SECOND_VALUE[순번]);}
static int 같음(unsigned x_chomhordanáid,unsigned 세로좌표){return x_chomhordanáid>0&&x_chomhordanáid<상수모음&&세로좌표>0&&세로좌표<상수모음&&Catagóirí_Liosta[x_chomhordanáid]==1&&Catagóirí_Liosta[세로좌표]==1&&SECOND_VALUE[x_chomhordanáid]==SECOND_VALUE[세로좌표]&&!memcmp(sonraí+첫째값[x_chomhordanáid],sonraí+첫째값[세로좌표],SECOND_VALUE[x_chomhordanáid]);}
static void 내보내기(const char*comhad_iontráil,...){if(teicneolaíocht_faisnéise_neamhbhailí)return;va_list argóint_ARRAY;va_start(argóint_ARRAY,comhad_iontráil);int mír_COUNT=vsnprintf(Téacs+méid_téacs,sizeof(Téacs)-méid_téacs,comhad_iontráil,argóint_ARRAY);va_end(argóint_ARRAY);if(mír_COUNT<0||(unsigned)mír_COUNT>=sizeof(Téacs)-méid_téacs){teicneolaíocht_faisnéise_neamhbhailí=1;return;}méid_téacs+=mír_COUNT;}
static int 서술자(unsigned aitheantóir_VALUE,int*tomhas){
    if(aitheantóir_VALUE<1||aitheantóir_VALUE>=상수모음||Catagóirí_Liosta[aitheantóir_VALUE]!=1)return -1;unsigned sonraí_suíomh=첫째값[aitheantóir_VALUE],cuir_deireadh_le_OFFSET=sonraí_suíomh+SECOND_VALUE[aitheantóir_VALUE];if(sonraí_suíomh>=cuir_deireadh_le_OFFSET||sonraí[sonraí_suíomh++]!='(')return -1;int iontráil_COUNT=0;
    while(sonraí_suíomh<cuir_deireadh_le_OFFSET&&sonraí[sonraí_suíomh]!=')'){
        unsigned pointe_cóid=sonraí[sonraí_suíomh++];while(pointe_cóid=='['&&sonraí_suíomh<cuir_deireadh_le_OFFSET)pointe_cóid=sonraí[sonraí_suíomh++];
        if(pointe_cóid=='L'){while(sonraí_suíomh<cuir_deireadh_le_OFFSET&&sonraí[sonraí_suíomh]!=';')sonraí_suíomh++;if(sonraí_suíomh==cuir_deireadh_le_OFFSET)return -1;sonraí_suíomh++;}
        else if(pointe_cóid!='I'&&pointe_cóid!='Z'&&pointe_cóid!='B'&&pointe_cóid!='C'&&pointe_cóid!='S')return -1;
        if(++iontráil_COUNT>16)return -1;
    }
    if(sonraí_suíomh+1>=cuir_deireadh_le_OFFSET||sonraí[sonraí_suíomh++]!=')')return -1;*tomhas=sonraí[sonraí_suíomh]=='V'?0:1;
    if(sonraí[sonraí_suíomh]=='J'||sonraí[sonraí_suíomh]=='D'||sonraí[sonraí_suíomh]=='F')return -1;return iontráil_COUNT;
}
static void 속성들(void){unsigned mír_COUNT=절반값();for(unsigned 순번=0;순번<mír_COUNT&&!teicneolaíocht_faisnéise_neamhbhailí;순번++){절반값();unsigned Méid=가득참();TAKE_VALUE(Méid);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned mion_leagan=절반값(),uimhir_an_leagain=절반값();if(mion_leagan||uimhir_an_leagain<45||uimhir_an_leagain>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!teicneolaíocht_faisnéise_neamhbhailí;순번++){
        Catagóirí_Liosta[순번]=beart_sonraí();switch(Catagóirí_Liosta[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=beart_sonraí();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Catagóirí_Liosta[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Catagóirí_Liosta[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!teicneolaíocht_faisnéise_neamhbhailí;순번++){
        unsigned 설정비트=절반값();ainm_réimse_98daa19b[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned iontráil_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<iontráil_COUNT&&!teicneolaíocht_faisnéise_neamhbhailí;안쪽순번++){
            unsigned Ainm=절반값(),Méid=가득참();
            if(UNICODE_VALUE(Ainm,"ConstantValue")){if(Méid!=2)return -1;réimse_tairiseach[순번]=절반값();}
            else TAKE_VALUE(Méid);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!teicneolaíocht_faisnéise_neamhbhailí;순번++){
        modh_iontráil*Grúpa_socraigh_méid=메소드목록+순번;Grúpa_socraigh_méid->설정비트=절반값();Grúpa_socraigh_méid->Ainm=절반값();Grúpa_socraigh_méid->서술값=절반값();unsigned iontráil_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<iontráil_COUNT&&!teicneolaíocht_faisnéise_neamhbhailí;안쪽순번++){
            unsigned Ainm=절반값(),Méid=가득참(),Rith_2=현재위치;
            if(Méid>fad_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(Ainm,"Code")){
                Grúpa_socraigh_méid->Cruach_Stóras=절반값();Grúpa_socraigh_méid->지역변수들=절반값();Grúpa_socraigh_méid->Méid=가득참();Grúpa_socraigh_méid->treoir_SEQUENCE=TAKE_VALUE(Grúpa_socraigh_méid->Méid);
                if(Grúpa_socraigh_méid->Cruach_Stóras>128||Grúpa_socraigh_méid->지역변수들>128||Grúpa_socraigh_méid->Méid>8192||절반값())return -1;속성들();
            }else TAKE_VALUE(Méid);
            if(현재위치!=Rith_2+Méid)return -1;
        }
        if(!UNICODE_VALUE(Grúpa_socraigh_méid->Ainm,"<init>")&&(!(Grúpa_socraigh_méid->설정비트&8)||(Grúpa_socraigh_méid->설정비트&(0x100|0x20))||!Grúpa_socraigh_méid->Méid))return -1;
    }
    속성들();return teicneolaíocht_faisnéise_neamhbhailí||현재위치!=fad_VALUE?-1:0;
}
static void tairiseach_VALUE(unsigned aitheantóir_VALUE){
    if(!aitheantóir_VALUE||aitheantóir_VALUE>=상수모음){teicneolaíocht_faisnéise_neamhbhailí=1;return;}
    if(Catagóirí_Liosta[aitheantóir_VALUE]==3)내보내기("P(%uU);",첫째값[aitheantóir_VALUE]);
    else if(Catagóirí_Liosta[aitheantóir_VALUE]==8)내보내기("P((W)k%u);",aitheantóir_VALUE);else teicneolaíocht_faisnéise_neamhbhailí=1;
}
static void 호출(unsigned aitheantóir_VALUE,int fíorúil_CALL){
    if(aitheantóir_VALUE<1||aitheantóir_VALUE>=상수모음||(Catagóirí_Liosta[aitheantóir_VALUE]!=10&&Catagóirí_Liosta[aitheantóir_VALUE]!=11)||첫째값[aitheantóir_VALUE]<1||첫째값[aitheantóir_VALUE]>=상수모음||Catagóirí_Liosta[첫째값[aitheantóir_VALUE]]!=7||SECOND_VALUE[aitheantóir_VALUE]<1||SECOND_VALUE[aitheantóir_VALUE]>=상수모음||Catagóirí_Liosta[SECOND_VALUE[aitheantóir_VALUE]]!=12){teicneolaíocht_faisnéise_neamhbhailí=1;return;}
    unsigned úinéir_oibiacht=첫째값[첫째값[aitheantóir_VALUE]],Ainm=첫째값[SECOND_VALUE[aitheantóir_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[aitheantóir_VALUE]];int tomhas=0,mír_COUNT=서술자(서술값,&tomhas);if(mír_COUNT<0){teicneolaíocht_faisnéise_neamhbhailí=1;return;}
    for(int 순번=mír_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(fíorúil_CALL)내보내기("Q();");
    if(!fíorúil_CALL&&같음(úinéir_oibiacht,첫째값[현재클래스])){
        unsigned Grúpa_socraigh_méid=0;for(;Grúpa_socraigh_méid<메소드개수;Grúpa_socraigh_méid++)if(같음(Ainm,메소드목록[Grúpa_socraigh_méid].Ainm)&&같음(서술값,메소드목록[Grúpa_socraigh_méid].서술값))break;
        if(Grúpa_socraigh_méid==메소드개수||!(메소드목록[Grúpa_socraigh_méid].설정비트&8)){teicneolaíocht_faisnéise_neamhbhailí=1;return;}
        if(tomhas)내보내기("P(");내보내기("m%u(",Grúpa_socraigh_méid);for(int 순번=0;순번<mír_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(tomhas?"));":" );");return;
    }
    if((fíorúil_CALL&&UNICODE_VALUE(úinéir_oibiacht,"java/io/PrintStream")&& (UNICODE_VALUE(Ainm,"print")||UNICODE_VALUE(Ainm,"println")))||(!fíorúil_CALL&&UNICODE_VALUE(úinéir_oibiacht,"Gaeilge/자체/Aschur"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Ainm,"print")||UNICODE_VALUE(Ainm,"println")||UNICODE_VALUE(Ainm,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Ainm,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Ainm,"print")||UNICODE_VALUE(Ainm,"println")||UNICODE_VALUE(Ainm,"Scríobh")||UNICODE_VALUE(Ainm,"scríobh_líne"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Ainm,"print")||UNICODE_VALUE(Ainm,"Scríobh")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Ainm,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!fíorúil_CALL&&UNICODE_VALUE(úinéir_oibiacht,"Gaeilge/자체/Comhad")){
        if(UNICODE_VALUE(Ainm,"Scríobh")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Ainm,"Léigh")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    teicneolaíocht_faisnéise_neamhbhailí=1;
}
static void tóg_modh(unsigned LOOKUP_INDEX){
    modh_iontráil*Grúpa_socraigh_méid=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Grúpa_socraigh_méid->Ainm,"<init>"))return;int tomhas,mír_COUNT=서술자(Grúpa_socraigh_méid->서술값,&tomhas);if(mír_COUNT<0){teicneolaíocht_faisnéise_neamhbhailí=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<mír_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!mír_COUNT)내보내기("void");
    if((unsigned)mír_COUNT>Grúpa_socraigh_méid->지역변수들){teicneolaíocht_faisnéise_neamhbhailí=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grúpa_socraigh_méid->지역변수들?Grúpa_socraigh_méid->지역변수들:1);for(int 순번=0;순번<mír_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=fad_VALUE;fad_VALUE=Grúpa_socraigh_méid->treoir_SEQUENCE+Grúpa_socraigh_méid->Méid;현재위치=Grúpa_socraigh_méid->treoir_SEQUENCE;
    while(현재위치<fad_VALUE&&!teicneolaíocht_faisnéise_neamhbhailí){unsigned ordú_suíomh=현재위치-Grúpa_socraigh_méid->treoir_SEQUENCE,oibríocht_VALUE=beart_sonraí();내보내기("L%u:;",ordú_suíomh);
        if(oibríocht_VALUE==0){}
        else if(oibríocht_VALUE==1)내보내기("P(0);");
        else if(oibríocht_VALUE>=2&&oibríocht_VALUE<=8)내보내기("P(%uU);",oibríocht_VALUE-3);
        else if(oibríocht_VALUE==16){int VALUE=(int8_t)beart_sonraí();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(oibríocht_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(oibríocht_VALUE==18||oibríocht_VALUE==19)tairiseach_VALUE(oibríocht_VALUE==18?beart_sonraí():절반값());
        else if(oibríocht_VALUE==21||oibríocht_VALUE==25){unsigned 순번=beart_sonraí();if(순번>=Grúpa_socraigh_méid->지역변수들)teicneolaíocht_faisnéise_neamhbhailí=1;내보내기("P(v[%u]);",순번);}
        else if((oibríocht_VALUE>=26&&oibríocht_VALUE<=29)||(oibríocht_VALUE>=42&&oibríocht_VALUE<=45)){unsigned 순번=oibríocht_VALUE>=42?oibríocht_VALUE-42:oibríocht_VALUE-26;if(순번>=Grúpa_socraigh_méid->지역변수들)teicneolaíocht_faisnéise_neamhbhailí=1;내보내기("P(v[%u]);",순번);}
        else if(oibríocht_VALUE==54||oibríocht_VALUE==58){unsigned 순번=beart_sonraí();if(순번>=Grúpa_socraigh_méid->지역변수들)teicneolaíocht_faisnéise_neamhbhailí=1;내보내기("v[%u]=Q();",순번);}
        else if((oibríocht_VALUE>=59&&oibríocht_VALUE<=62)||(oibríocht_VALUE>=75&&oibríocht_VALUE<=78)){unsigned 순번=oibríocht_VALUE>=75?oibríocht_VALUE-75:oibríocht_VALUE-59;if(순번>=Grúpa_socraigh_méid->지역변수들)teicneolaíocht_faisnéise_neamhbhailí=1;내보내기("v[%u]=Q();",순번);}
        else if(oibríocht_VALUE==46||oibríocht_VALUE==50||oibríocht_VALUE==51||oibríocht_VALUE==52||oibríocht_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(oibríocht_VALUE==79||oibríocht_VALUE==83||oibríocht_VALUE==84||oibríocht_VALUE==85||oibríocht_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",oibríocht_VALUE==84?"(unsigned)(signed char)q":oibríocht_VALUE==85?"(unsigned short)q":oibríocht_VALUE==86?"(unsigned)(short)q":"q");
        else if(oibríocht_VALUE==87)내보내기("Q();");
        else if(oibríocht_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(oibríocht_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(oibríocht_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(oibríocht_VALUE==96||oibríocht_VALUE==100||oibríocht_VALUE==104||oibríocht_VALUE==120||oibríocht_VALUE==124||oibríocht_VALUE==126||oibríocht_VALUE==128||oibríocht_VALUE==130){const char*ionchódú_VALUE=oibríocht_VALUE==96?"+":oibríocht_VALUE==100?"-":oibríocht_VALUE==104?"*":oibríocht_VALUE==120?"<<":oibríocht_VALUE==124?">>":oibríocht_VALUE==126?"&":oibríocht_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",ionchódú_VALUE,oibríocht_VALUE==120||oibríocht_VALUE==124?"%32":"");}
        else if(oibríocht_VALUE==108||oibríocht_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",oibríocht_VALUE==112);
        else if(oibríocht_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(oibríocht_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(oibríocht_VALUE==132){unsigned 순번=beart_sonraí();int 차이=(int8_t)beart_sonraí();if(순번>=Grúpa_socraigh_méid->지역변수들)teicneolaíocht_faisnéise_neamhbhailí=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(oibríocht_VALUE>=145&&oibríocht_VALUE<=147)내보내기("P((unsigned)(%s)Q());",oibríocht_VALUE==145?"signed char":oibríocht_VALUE==146?"unsigned short":"short");
        else if(oibríocht_VALUE>=153&&oibríocht_VALUE<=166){int sprioc=(int)ordú_suíomh+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(sprioc<0||sprioc>=(int)Grúpa_socraigh_méid->Méid){teicneolaíocht_faisnéise_neamhbhailí=1;break;}if(oibríocht_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[oibríocht_VALUE-153],sprioc);else if(oibríocht_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[oibríocht_VALUE-159],sprioc);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",oibríocht_VALUE==165?"==":"!=",sprioc);}
        else if(oibríocht_VALUE==167){int sprioc=(int)ordú_suíomh+(int16_t)절반값();if(sprioc<0||sprioc>=(int)Grúpa_socraigh_méid->Méid)teicneolaíocht_faisnéise_neamhbhailí=1;내보내기("goto L%d;",sprioc);}
        else if(oibríocht_VALUE==172||oibríocht_VALUE==176)내보내기("return Q();");else if(oibríocht_VALUE==177)내보내기("return 0;");
        else if(oibríocht_VALUE==178||oibríocht_VALUE==179){unsigned aitheantóir_VALUE=절반값();if(aitheantóir_VALUE<1||aitheantóir_VALUE>=상수모음||Catagóirí_Liosta[aitheantóir_VALUE]!=9||첫째값[aitheantóir_VALUE]>=상수모음||SECOND_VALUE[aitheantóir_VALUE]>=상수모음||Catagóirí_Liosta[첫째값[aitheantóir_VALUE]]!=7||Catagóirí_Liosta[SECOND_VALUE[aitheantóir_VALUE]]!=12){teicneolaíocht_faisnéise_neamhbhailí=1;break;}unsigned úinéir_oibiacht=첫째값[첫째값[aitheantóir_VALUE]],Ainm=첫째값[SECOND_VALUE[aitheantóir_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[aitheantóir_VALUE]];
            if(oibríocht_VALUE==178&&UNICODE_VALUE(úinéir_oibiacht,"java/lang/System")&&UNICODE_VALUE(Ainm,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned comhad_iontráil=0;while(comhad_iontráil<필드개수&&(!같음(Ainm,ainm_réimse_98daa19b[comhad_iontráil])||!같음(서술값,필드서술[comhad_iontráil])))comhad_iontráil++;if(!같음(úinéir_oibiacht,첫째값[현재클래스])||comhad_iontráil==필드개수){teicneolaíocht_faisnéise_neamhbhailí=1;break;}내보내기(oibríocht_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",comhad_iontráil);}}
        else if(oibríocht_VALUE==182||oibríocht_VALUE==184)호출(절반값(),oibríocht_VALUE==182);
        else if(oibríocht_VALUE==188){unsigned TYPE_catagóir=beart_sonraí();if(TYPE_catagóir!=4&&TYPE_catagóir!=5&&TYPE_catagóir!=8&&TYPE_catagóir!=9&&TYPE_catagóir!=10)teicneolaíocht_faisnéise_neamhbhailí=1;내보내기("P(jarray((int)Q()));");}
        else if(oibríocht_VALUE==190)내보내기("P(jlength(Q()));");
        else if(oibríocht_VALUE==198||oibríocht_VALUE==199){int sprioc=(int)ordú_suíomh+(int16_t)절반값();if(sprioc<0||sprioc>=(int)Grúpa_socraigh_méid->Méid)teicneolaíocht_faisnéise_neamhbhailí=1;내보내기("if(Q()%s0)goto L%d;",oibríocht_VALUE==198?"==":"!=",sprioc);}
        else teicneolaíocht_faisnéise_neamhbhailí=1;
        if(teicneolaíocht_faisnéise_neamhbhailí)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,oibríocht_VALUE,ordú_suíomh);
        내보내기("\n");
    }
    fad_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned teaghrán_aonaid(unsigned *sonraí_suíomh,unsigned cuir_deireadh_le_OFFSET){
    if(*sonraí_suíomh>=cuir_deireadh_le_OFFSET){teicneolaíocht_faisnéise_neamhbhailí=1;return 0;}unsigned pointe_cóid=sonraí[(*sonraí_suíomh)++];
    if(pointe_cóid<128)return pointe_cóid;
    unsigned mír_COUNT=pointe_cóid>=0xc0&&pointe_cóid<=0xdf?1:pointe_cóid>=0xe0&&pointe_cóid<=0xef?2:3;
    if(mír_COUNT==3||mír_COUNT>cuir_deireadh_le_OFFSET-*sonraí_suíomh){teicneolaíocht_faisnéise_neamhbhailí=1;return 0;}unsigned VALUE=pointe_cóid&((1u<<(6-mír_COUNT))-1);
    for(unsigned 순번=0;순번<mír_COUNT;순번++){unsigned Ar_aghaidh_mír=sonraí[(*sonraí_suíomh)++];if((Ar_aghaidh_mír&0xc0)!=0x80)teicneolaíocht_faisnéise_neamhbhailí=1;VALUE=VALUE<<6|(Ar_aghaidh_mír&63);}
    if((mír_COUNT==1&&VALUE<128&&VALUE!=0)||(mír_COUNT==2&&VALUE<2048))teicneolaíocht_faisnéise_neamhbhailí=1;return VALUE;
}
static void teaghrán_tairiseach(unsigned aitheantóir_VALUE){
    unsigned 부호없는값=첫째값[aitheantóir_VALUE];if(부호없는값<1||부호없는값>=상수모음||Catagóirí_Liosta[부호없는값]!=1){teicneolaíocht_faisnéise_neamhbhailí=1;return;}내보내기("static const unsigned char k%u[]={",aitheantóir_VALUE);
    unsigned sonraí_suíomh=첫째값[부호없는값],cuir_deireadh_le_OFFSET=sonraí_suíomh+SECOND_VALUE[부호없는값];
    while(sonraí_suíomh<cuir_deireadh_le_OFFSET&&!teicneolaíocht_faisnéise_neamhbhailí){unsigned pointe_cóid=teaghrán_aonaid(&sonraí_suíomh,cuir_deireadh_le_OFFSET);
        if(pointe_cóid>=0xd800&&pointe_cóid<=0xdbff){unsigned 낮은부분=teaghrán_aonaid(&sonraí_suíomh,cuir_deireadh_le_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){teicneolaíocht_faisnéise_neamhbhailí=1;break;}pointe_cóid=0x10000+((pointe_cóid-0xd800)<<10)+낮은부분-0xdc00;}
        else if(pointe_cóid>=0xdc00&&pointe_cóid<=0xdfff){teicneolaíocht_faisnéise_neamhbhailí=1;break;}
        if(!pointe_cóid){printf("jaot: embedded NUL string needs JVM mode\n");teicneolaíocht_faisnéise_neamhbhailí=1;break;}
        if(pointe_cóid<128)내보내기("%u,",pointe_cóid);
        else{unsigned mír_COUNT=pointe_cóid<2048?2:pointe_cóid<65536?3:4;내보내기("%u,",(mír_COUNT==2?0xc0:mír_COUNT==3?0xe0:0xf0)|(pointe_cóid>>(6*(mír_COUNT-1))));for(unsigned 순번=mír_COUNT-1;순번;순번--)내보내기("%u,",0x80|((pointe_cóid>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Ainm){
    size_t mír_COUNT=strlen(Ainm);
    if(mír_COUNT>4&&!strcmp(Ainm+mír_COUNT-4,".jar")){
        if(꾸러미열기(Ainm)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char CONAIR[256];const char*iontráil_modh=꾸러미진입클래스();mír_COUNT=strlen(iontráil_modh);if(mír_COUNT+6>=sizeof(CONAIR))return 0;
        for(unsigned 순번=0;순번<mír_COUNT;순번++)CONAIR[순번]=iontráil_modh[순번]=='.'?'/':iontráil_modh[순번];strcpy(CONAIR+mír_COUNT,".class");int iontráil_COUNT=꾸러미읽기(CONAIR,sonraí,sizeof(sonraí));if(iontráil_COUNT<0)return 0;fad_VALUE=iontráil_COUNT;
    }else{intptr_t comhad_hanla=사용자호출(3,(uintptr_t)Ainm,0,0,0,0,0);if(comhad_hanla<0)return 0;intptr_t iontráil_COUNT=사용자호출(9,comhad_hanla,0,0,0,0,0);if(iontráil_COUNT<0||iontráil_COUNT>sizeof(sonraí)){사용자호출(4,comhad_hanla,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,comhad_hanla,(uintptr_t)sonraí,iontráil_COUNT,0,0,0);사용자호출(4,comhad_hanla,0,0,0,0,0);if(RECEIVED_COUNT!=iontráil_COUNT)return 0;fad_VALUE=iontráil_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!teicneolaíocht_faisnéise_neamhbhailí;순번++)if(Catagóirí_Liosta[순번]==8)teaghrán_tairiseach(순번);
    if(teicneolaíocht_faisnéise_neamhbhailí)return 0;
    int iontráil_pointe=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Ainm,"<init>")){
        int tomhas,iontráil_COUNT=서술자(메소드목록[순번].서술값,&tomhas);if(iontráil_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<iontráil_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!iontráil_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Ainm,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)iontráil_pointe=순번;
        if(UNICODE_VALUE(메소드목록[순번].Ainm,"<clinit>"))초기값=순번;
    }
    if(iontráil_pointe<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!teicneolaíocht_faisnéise_neamhbhailí;순번++)tóg_modh(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(réimse_tairiseach[순번]){
        unsigned pointe_cóid=réimse_tairiseach[순번];if(pointe_cóid>=상수모음)return 0;
        if(Catagóirí_Liosta[pointe_cóid]==3)내보내기("fields[%u]=%uU;",순번,첫째값[pointe_cóid]);else if(Catagóirí_Liosta[pointe_cóid]==8)내보내기("fields[%u]=(W)k%u;",순번,pointe_cóid);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",iontráil_pointe);
    return teicneolaíocht_faisnéise_neamhbhailí?0:Téacs;
}
