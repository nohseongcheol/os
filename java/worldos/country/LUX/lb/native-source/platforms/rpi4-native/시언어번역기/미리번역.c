#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "Bëndel.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char Daten[16384];static unsigned Längt_VALUE,현재위치;static int 잘못됨;
static unsigned Kategorien_Lëscht[512],첫째값[512],SECOND_VALUE[512],상수모음,현재클래스;
static char SMS[65536];static unsigned Textgréisst;
typedef struct {unsigned 설정비트,Numm,서술값,Instruktioun_SEQUENCE,d_Gréisst_veränneren,지역변수들,Stapel_Späicher;} Method_Agab;
static Method_Agab 메소드목록[64];static unsigned 메소드개수;
static unsigned Feldnumm[64],필드서술[64],Feld_Konstant[64],필드개수;
static unsigned TAKE_VALUE(unsigned Element_COUNT){if(현재위치>Längt_VALUE||Element_COUNT>Längt_VALUE-현재위치){잘못됨=1;return 0;}unsigned Daten_positionéieren=현재위치;현재위치+=Element_COUNT;return Daten_positionéieren;}
static unsigned Byte_Daten(void){unsigned Daten_positionéieren=TAKE_VALUE(1);return 잘못됨?0:Daten[Daten_positionéieren];}
static unsigned 절반값(void){unsigned X_Koordinat=Byte_Daten();return X_Koordinat<<8|Byte_Daten();}
static uint32_t 가득참(void){uint32_t X_Koordinat=절반값();return X_Koordinat<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*Zeechefolleg_Daten){return 순번>0&&순번<상수모음&&Kategorien_Lëscht[순번]==1&&strlen(Zeechefolleg_Daten)==SECOND_VALUE[순번]&&!memcmp(Daten+첫째값[순번],Zeechefolleg_Daten,SECOND_VALUE[순번]);}
static int 같음(unsigned X_Koordinat,unsigned 세로좌표){return X_Koordinat>0&&X_Koordinat<상수모음&&세로좌표>0&&세로좌표<상수모음&&Kategorien_Lëscht[X_Koordinat]==1&&Kategorien_Lëscht[세로좌표]==1&&SECOND_VALUE[X_Koordinat]==SECOND_VALUE[세로좌표]&&!memcmp(Daten+첫째값[X_Koordinat],Daten+첫째값[세로좌표],SECOND_VALUE[X_Koordinat]);}
static void 내보내기(const char*Fichier_Agab,...){if(잘못됨)return;va_list Argument_ARRAY;va_start(Argument_ARRAY,Fichier_Agab);int Element_COUNT=vsnprintf(SMS+Textgréisst,sizeof(SMS)-Textgréisst,Fichier_Agab,Argument_ARRAY);va_end(Argument_ARRAY);if(Element_COUNT<0||(unsigned)Element_COUNT>=sizeof(SMS)-Textgréisst){잘못됨=1;return;}Textgréisst+=Element_COUNT;}
static int 서술자(unsigned Identifikateur_VALUE,int*Mooss){
    if(Identifikateur_VALUE<1||Identifikateur_VALUE>=상수모음||Kategorien_Lëscht[Identifikateur_VALUE]!=1)return -1;unsigned Daten_positionéieren=첫째값[Identifikateur_VALUE],bëennegen_OFFSET=Daten_positionéieren+SECOND_VALUE[Identifikateur_VALUE];if(Daten_positionéieren>=bëennegen_OFFSET||Daten[Daten_positionéieren++]!='(')return -1;int Agab_COUNT=0;
    while(Daten_positionéieren<bëennegen_OFFSET&&Daten[Daten_positionéieren]!=')'){
        unsigned Zeechecode=Daten[Daten_positionéieren++];while(Zeechecode=='['&&Daten_positionéieren<bëennegen_OFFSET)Zeechecode=Daten[Daten_positionéieren++];
        if(Zeechecode=='L'){while(Daten_positionéieren<bëennegen_OFFSET&&Daten[Daten_positionéieren]!=';')Daten_positionéieren++;if(Daten_positionéieren==bëennegen_OFFSET)return -1;Daten_positionéieren++;}
        else if(Zeechecode!='I'&&Zeechecode!='Z'&&Zeechecode!='B'&&Zeechecode!='C'&&Zeechecode!='S')return -1;
        if(++Agab_COUNT>16)return -1;
    }
    if(Daten_positionéieren+1>=bëennegen_OFFSET||Daten[Daten_positionéieren++]!=')')return -1;*Mooss=Daten[Daten_positionéieren]=='V'?0:1;
    if(Daten[Daten_positionéieren]=='J'||Daten[Daten_positionéieren]=='D'||Daten[Daten_positionéieren]=='F')return -1;return Agab_COUNT;
}
static void 속성들(void){unsigned Element_COUNT=절반값();for(unsigned 순번=0;순번<Element_COUNT&&!잘못됨;순번++){절반값();unsigned d_Gréisst_veränneren=가득참();TAKE_VALUE(d_Gréisst_veränneren);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned Mannerjäregen_Versioun=절반값(),판번호=절반값();if(Mannerjäregen_Versioun||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++){
        Kategorien_Lëscht[순번]=Byte_Daten();switch(Kategorien_Lëscht[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=Byte_Daten();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Kategorien_Lëscht[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Kategorien_Lëscht[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!잘못됨;순번++){
        unsigned 설정비트=절반값();Feldnumm[순번]=절반값();필드서술[순번]=절반값();
        if(!(설정비트&8))return -1;
        unsigned Agab_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<Agab_COUNT&&!잘못됨;안쪽순번++){
            unsigned Numm=절반값(),d_Gréisst_veränneren=가득참();
            if(UNICODE_VALUE(Numm,"ConstantValue")){if(d_Gréisst_veränneren!=2)return -1;Feld_Konstant[순번]=절반값();}
            else TAKE_VALUE(d_Gréisst_veränneren);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++){
        Method_Agab*Grupp_d_Gréisst_veränneren=메소드목록+순번;Grupp_d_Gréisst_veränneren->설정비트=절반값();Grupp_d_Gréisst_veränneren->Numm=절반값();Grupp_d_Gréisst_veränneren->서술값=절반값();unsigned Agab_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<Agab_COUNT&&!잘못됨;안쪽순번++){
            unsigned Numm=절반값(),d_Gréisst_veränneren=가득참(),Laf=현재위치;
            if(d_Gréisst_veränneren>Längt_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(Numm,"Code")){
                Grupp_d_Gréisst_veränneren->Stapel_Späicher=절반값();Grupp_d_Gréisst_veränneren->지역변수들=절반값();Grupp_d_Gréisst_veränneren->d_Gréisst_veränneren=가득참();Grupp_d_Gréisst_veränneren->Instruktioun_SEQUENCE=TAKE_VALUE(Grupp_d_Gréisst_veränneren->d_Gréisst_veränneren);
                if(Grupp_d_Gréisst_veränneren->Stapel_Späicher>128||Grupp_d_Gréisst_veränneren->지역변수들>128||Grupp_d_Gréisst_veränneren->d_Gréisst_veränneren>8192||절반값())return -1;속성들();
            }else TAKE_VALUE(d_Gréisst_veränneren);
            if(현재위치!=Laf+d_Gréisst_veränneren)return -1;
        }
        if(!UNICODE_VALUE(Grupp_d_Gréisst_veränneren->Numm,"<init>")&&(!(Grupp_d_Gréisst_veränneren->설정비트&8)||(Grupp_d_Gréisst_veränneren->설정비트&(0x100|0x20))||!Grupp_d_Gréisst_veränneren->d_Gréisst_veränneren))return -1;
    }
    속성들();return 잘못됨||현재위치!=Längt_VALUE?-1:0;
}
static void Konstant_VALUE(unsigned Identifikateur_VALUE){
    if(!Identifikateur_VALUE||Identifikateur_VALUE>=상수모음){잘못됨=1;return;}
    if(Kategorien_Lëscht[Identifikateur_VALUE]==3)내보내기("P(%uU);",첫째값[Identifikateur_VALUE]);
    else if(Kategorien_Lëscht[Identifikateur_VALUE]==8)내보내기("P((W)k%u);",Identifikateur_VALUE);else 잘못됨=1;
}
static void 호출(unsigned Identifikateur_VALUE,int virtuell_CALL){
    if(Identifikateur_VALUE<1||Identifikateur_VALUE>=상수모음||(Kategorien_Lëscht[Identifikateur_VALUE]!=10&&Kategorien_Lëscht[Identifikateur_VALUE]!=11)||첫째값[Identifikateur_VALUE]<1||첫째값[Identifikateur_VALUE]>=상수모음||Kategorien_Lëscht[첫째값[Identifikateur_VALUE]]!=7||SECOND_VALUE[Identifikateur_VALUE]<1||SECOND_VALUE[Identifikateur_VALUE]>=상수모음||Kategorien_Lëscht[SECOND_VALUE[Identifikateur_VALUE]]!=12){잘못됨=1;return;}
    unsigned Besëtzer_Objet=첫째값[첫째값[Identifikateur_VALUE]],Numm=첫째값[SECOND_VALUE[Identifikateur_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[Identifikateur_VALUE]];int Mooss=0,Element_COUNT=서술자(서술값,&Mooss);if(Element_COUNT<0){잘못됨=1;return;}
    for(int 순번=Element_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuell_CALL)내보내기("Q();");
    if(!virtuell_CALL&&같음(Besëtzer_Objet,첫째값[현재클래스])){
        unsigned Grupp_d_Gréisst_veränneren=0;for(;Grupp_d_Gréisst_veränneren<메소드개수;Grupp_d_Gréisst_veränneren++)if(같음(Numm,메소드목록[Grupp_d_Gréisst_veränneren].Numm)&&같음(서술값,메소드목록[Grupp_d_Gréisst_veränneren].서술값))break;
        if(Grupp_d_Gréisst_veränneren==메소드개수||!(메소드목록[Grupp_d_Gréisst_veränneren].설정비트&8)){잘못됨=1;return;}
        if(Mooss)내보내기("P(");내보내기("m%u(",Grupp_d_Gréisst_veränneren);for(int 순번=0;순번<Element_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(Mooss?"));":" );");return;
    }
    if((virtuell_CALL&&UNICODE_VALUE(Besëtzer_Objet,"java/io/PrintStream")&& (UNICODE_VALUE(Numm,"print")||UNICODE_VALUE(Numm,"println")))||(!virtuell_CALL&&UNICODE_VALUE(Besëtzer_Objet,"한국어/자체/출력"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Numm,"print")||UNICODE_VALUE(Numm,"println")||UNICODE_VALUE(Numm,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Numm,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Numm,"print")||UNICODE_VALUE(Numm,"println")||UNICODE_VALUE(Numm,"schreiwen")||UNICODE_VALUE(Numm,"schreiwen_Zeil"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Numm,"print")||UNICODE_VALUE(Numm,"schreiwen")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Numm,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuell_CALL&&UNICODE_VALUE(Besëtzer_Objet,"한국어/자체/Fichier")){
        if(UNICODE_VALUE(Numm,"schreiwen")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Numm,"읽기")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    잘못됨=1;
}
static void erstellen_Method(unsigned LOOKUP_INDEX){
    Method_Agab*Grupp_d_Gréisst_veränneren=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Grupp_d_Gréisst_veränneren->Numm,"<init>"))return;int Mooss,Element_COUNT=서술자(Grupp_d_Gréisst_veränneren->서술값,&Mooss);if(Element_COUNT<0){잘못됨=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<Element_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!Element_COUNT)내보내기("void");
    if((unsigned)Element_COUNT>Grupp_d_Gréisst_veränneren->지역변수들){잘못됨=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grupp_d_Gréisst_veränneren->지역변수들?Grupp_d_Gréisst_veränneren->지역변수들:1);for(int 순번=0;순번<Element_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=Längt_VALUE;Längt_VALUE=Grupp_d_Gréisst_veränneren->Instruktioun_SEQUENCE+Grupp_d_Gréisst_veränneren->d_Gréisst_veränneren;현재위치=Grupp_d_Gréisst_veränneren->Instruktioun_SEQUENCE;
    while(현재위치<Längt_VALUE&&!잘못됨){unsigned Befeel_positionéieren=현재위치-Grupp_d_Gréisst_veränneren->Instruktioun_SEQUENCE,Operatioun_VALUE=Byte_Daten();내보내기("L%u:;",Befeel_positionéieren);
        if(Operatioun_VALUE==0){}
        else if(Operatioun_VALUE==1)내보내기("P(0);");
        else if(Operatioun_VALUE>=2&&Operatioun_VALUE<=8)내보내기("P(%uU);",Operatioun_VALUE-3);
        else if(Operatioun_VALUE==16){int VALUE=(int8_t)Byte_Daten();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(Operatioun_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(Operatioun_VALUE==18||Operatioun_VALUE==19)Konstant_VALUE(Operatioun_VALUE==18?Byte_Daten():절반값());
        else if(Operatioun_VALUE==21||Operatioun_VALUE==25){unsigned 순번=Byte_Daten();if(순번>=Grupp_d_Gréisst_veränneren->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if((Operatioun_VALUE>=26&&Operatioun_VALUE<=29)||(Operatioun_VALUE>=42&&Operatioun_VALUE<=45)){unsigned 순번=Operatioun_VALUE>=42?Operatioun_VALUE-42:Operatioun_VALUE-26;if(순번>=Grupp_d_Gréisst_veränneren->지역변수들)잘못됨=1;내보내기("P(v[%u]);",순번);}
        else if(Operatioun_VALUE==54||Operatioun_VALUE==58){unsigned 순번=Byte_Daten();if(순번>=Grupp_d_Gréisst_veränneren->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if((Operatioun_VALUE>=59&&Operatioun_VALUE<=62)||(Operatioun_VALUE>=75&&Operatioun_VALUE<=78)){unsigned 순번=Operatioun_VALUE>=75?Operatioun_VALUE-75:Operatioun_VALUE-59;if(순번>=Grupp_d_Gréisst_veränneren->지역변수들)잘못됨=1;내보내기("v[%u]=Q();",순번);}
        else if(Operatioun_VALUE==46||Operatioun_VALUE==50||Operatioun_VALUE==51||Operatioun_VALUE==52||Operatioun_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(Operatioun_VALUE==79||Operatioun_VALUE==83||Operatioun_VALUE==84||Operatioun_VALUE==85||Operatioun_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",Operatioun_VALUE==84?"(unsigned)(signed char)q":Operatioun_VALUE==85?"(unsigned short)q":Operatioun_VALUE==86?"(unsigned)(short)q":"q");
        else if(Operatioun_VALUE==87)내보내기("Q();");
        else if(Operatioun_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(Operatioun_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(Operatioun_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(Operatioun_VALUE==96||Operatioun_VALUE==100||Operatioun_VALUE==104||Operatioun_VALUE==120||Operatioun_VALUE==124||Operatioun_VALUE==126||Operatioun_VALUE==128||Operatioun_VALUE==130){const char*Codéierung_VALUE=Operatioun_VALUE==96?"+":Operatioun_VALUE==100?"-":Operatioun_VALUE==104?"*":Operatioun_VALUE==120?"<<":Operatioun_VALUE==124?">>":Operatioun_VALUE==126?"&":Operatioun_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",Codéierung_VALUE,Operatioun_VALUE==120||Operatioun_VALUE==124?"%32":"");}
        else if(Operatioun_VALUE==108||Operatioun_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",Operatioun_VALUE==112);
        else if(Operatioun_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(Operatioun_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(Operatioun_VALUE==132){unsigned 순번=Byte_Daten();int 차이=(int8_t)Byte_Daten();if(순번>=Grupp_d_Gréisst_veränneren->지역변수들)잘못됨=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(Operatioun_VALUE>=145&&Operatioun_VALUE<=147)내보내기("P((unsigned)(%s)Q());",Operatioun_VALUE==145?"signed char":Operatioun_VALUE==146?"unsigned short":"short");
        else if(Operatioun_VALUE>=153&&Operatioun_VALUE<=166){int Zil=(int)Befeel_positionéieren+(int16_t)절반값();const char*비교값[]={"==","!=","<",">=",">","<="};if(Zil<0||Zil>=(int)Grupp_d_Gréisst_veränneren->d_Gréisst_veränneren){잘못됨=1;break;}if(Operatioun_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",비교값[Operatioun_VALUE-153],Zil);else if(Operatioun_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",비교값[Operatioun_VALUE-159],Zil);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",Operatioun_VALUE==165?"==":"!=",Zil);}
        else if(Operatioun_VALUE==167){int Zil=(int)Befeel_positionéieren+(int16_t)절반값();if(Zil<0||Zil>=(int)Grupp_d_Gréisst_veränneren->d_Gréisst_veränneren)잘못됨=1;내보내기("goto L%d;",Zil);}
        else if(Operatioun_VALUE==172||Operatioun_VALUE==176)내보내기("return Q();");else if(Operatioun_VALUE==177)내보내기("return 0;");
        else if(Operatioun_VALUE==178||Operatioun_VALUE==179){unsigned Identifikateur_VALUE=절반값();if(Identifikateur_VALUE<1||Identifikateur_VALUE>=상수모음||Kategorien_Lëscht[Identifikateur_VALUE]!=9||첫째값[Identifikateur_VALUE]>=상수모음||SECOND_VALUE[Identifikateur_VALUE]>=상수모음||Kategorien_Lëscht[첫째값[Identifikateur_VALUE]]!=7||Kategorien_Lëscht[SECOND_VALUE[Identifikateur_VALUE]]!=12){잘못됨=1;break;}unsigned Besëtzer_Objet=첫째값[첫째값[Identifikateur_VALUE]],Numm=첫째값[SECOND_VALUE[Identifikateur_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[Identifikateur_VALUE]];
            if(Operatioun_VALUE==178&&UNICODE_VALUE(Besëtzer_Objet,"java/lang/System")&&UNICODE_VALUE(Numm,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Fichier_Agab=0;while(Fichier_Agab<필드개수&&(!같음(Numm,Feldnumm[Fichier_Agab])||!같음(서술값,필드서술[Fichier_Agab])))Fichier_Agab++;if(!같음(Besëtzer_Objet,첫째값[현재클래스])||Fichier_Agab==필드개수){잘못됨=1;break;}내보내기(Operatioun_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",Fichier_Agab);}}
        else if(Operatioun_VALUE==182||Operatioun_VALUE==184)호출(절반값(),Operatioun_VALUE==182);
        else if(Operatioun_VALUE==188){unsigned TYPE_Kategorie=Byte_Daten();if(TYPE_Kategorie!=4&&TYPE_Kategorie!=5&&TYPE_Kategorie!=8&&TYPE_Kategorie!=9&&TYPE_Kategorie!=10)잘못됨=1;내보내기("P(jarray((int)Q()));");}
        else if(Operatioun_VALUE==190)내보내기("P(jlength(Q()));");
        else if(Operatioun_VALUE==198||Operatioun_VALUE==199){int Zil=(int)Befeel_positionéieren+(int16_t)절반값();if(Zil<0||Zil>=(int)Grupp_d_Gréisst_veränneren->d_Gréisst_veränneren)잘못됨=1;내보내기("if(Q()%s0)goto L%d;",Operatioun_VALUE==198?"==":"!=",Zil);}
        else 잘못됨=1;
        if(잘못됨)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,Operatioun_VALUE,Befeel_positionéieren);
        내보내기("\n");
    }
    Längt_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned Zeechefolleg_Lektioun(unsigned *Daten_positionéieren,unsigned bëennegen_OFFSET){
    if(*Daten_positionéieren>=bëennegen_OFFSET){잘못됨=1;return 0;}unsigned Zeechecode=Daten[(*Daten_positionéieren)++];
    if(Zeechecode<128)return Zeechecode;
    unsigned Element_COUNT=Zeechecode>=0xc0&&Zeechecode<=0xdf?1:Zeechecode>=0xe0&&Zeechecode<=0xef?2:3;
    if(Element_COUNT==3||Element_COUNT>bëennegen_OFFSET-*Daten_positionéieren){잘못됨=1;return 0;}unsigned VALUE=Zeechecode&((1u<<(6-Element_COUNT))-1);
    for(unsigned 순번=0;순번<Element_COUNT;순번++){unsigned Weider_Element=Daten[(*Daten_positionéieren)++];if((Weider_Element&0xc0)!=0x80)잘못됨=1;VALUE=VALUE<<6|(Weider_Element&63);}
    if((Element_COUNT==1&&VALUE<128&&VALUE!=0)||(Element_COUNT==2&&VALUE<2048))잘못됨=1;return VALUE;
}
static void Zeechefolleg_Konstant(unsigned Identifikateur_VALUE){
    unsigned 부호없는값=첫째값[Identifikateur_VALUE];if(부호없는값<1||부호없는값>=상수모음||Kategorien_Lëscht[부호없는값]!=1){잘못됨=1;return;}내보내기("static const unsigned char k%u[]={",Identifikateur_VALUE);
    unsigned Daten_positionéieren=첫째값[부호없는값],bëennegen_OFFSET=Daten_positionéieren+SECOND_VALUE[부호없는값];
    while(Daten_positionéieren<bëennegen_OFFSET&&!잘못됨){unsigned Zeechecode=Zeechefolleg_Lektioun(&Daten_positionéieren,bëennegen_OFFSET);
        if(Zeechecode>=0xd800&&Zeechecode<=0xdbff){unsigned 낮은부분=Zeechefolleg_Lektioun(&Daten_positionéieren,bëennegen_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){잘못됨=1;break;}Zeechecode=0x10000+((Zeechecode-0xd800)<<10)+낮은부분-0xdc00;}
        else if(Zeechecode>=0xdc00&&Zeechecode<=0xdfff){잘못됨=1;break;}
        if(!Zeechecode){printf("jaot: embedded NUL string needs JVM mode\n");잘못됨=1;break;}
        if(Zeechecode<128)내보내기("%u,",Zeechecode);
        else{unsigned Element_COUNT=Zeechecode<2048?2:Zeechecode<65536?3:4;내보내기("%u,",(Element_COUNT==2?0xc0:Element_COUNT==3?0xe0:0xf0)|(Zeechecode>>(6*(Element_COUNT-1))));for(unsigned 순번=Element_COUNT-1;순번;순번--)내보내기("%u,",0x80|((Zeechecode>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Numm){
    size_t Element_COUNT=strlen(Numm);
    if(Element_COUNT>4&&!strcmp(Numm+Element_COUNT-4,".jar")){
        if(꾸러미열기(Numm)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Wee[256];const char*Agab_Method=꾸러미진입클래스();Element_COUNT=strlen(Agab_Method);if(Element_COUNT+6>=sizeof(Wee))return 0;
        for(unsigned 순번=0;순번<Element_COUNT;순번++)Wee[순번]=Agab_Method[순번]=='.'?'/':Agab_Method[순번];strcpy(Wee+Element_COUNT,".class");int Agab_COUNT=꾸러미읽기(Wee,Daten,sizeof(Daten));if(Agab_COUNT<0)return 0;Längt_VALUE=Agab_COUNT;
    }else{intptr_t Fichier_Handle=사용자호출(3,(uintptr_t)Numm,0,0,0,0,0);if(Fichier_Handle<0)return 0;intptr_t Agab_COUNT=사용자호출(9,Fichier_Handle,0,0,0,0,0);if(Agab_COUNT<0||Agab_COUNT>sizeof(Daten)){사용자호출(4,Fichier_Handle,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,Fichier_Handle,(uintptr_t)Daten,Agab_COUNT,0,0,0);사용자호출(4,Fichier_Handle,0,0,0,0,0);if(RECEIVED_COUNT!=Agab_COUNT)return 0;Längt_VALUE=Agab_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!잘못됨;순번++)if(Kategorien_Lëscht[순번]==8)Zeechefolleg_Konstant(순번);
    if(잘못됨)return 0;
    int Agab_Punkt=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Numm,"<init>")){
        int Mooss,Agab_COUNT=서술자(메소드목록[순번].서술값,&Mooss);if(Agab_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<Agab_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!Agab_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Numm,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].설정비트&9)==9)Agab_Punkt=순번;
        if(UNICODE_VALUE(메소드목록[순번].Numm,"<clinit>"))초기값=순번;
    }
    if(Agab_Punkt<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!잘못됨;순번++)erstellen_Method(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(Feld_Konstant[순번]){
        unsigned Zeechecode=Feld_Konstant[순번];if(Zeechecode>=상수모음)return 0;
        if(Kategorien_Lëscht[Zeechecode]==3)내보내기("fields[%u]=%uU;",순번,첫째값[Zeechecode]);else if(Kategorien_Lëscht[Zeechecode]==8)내보내기("fields[%u]=(W)k%u;",순번,Zeechecode);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",Agab_Punkt);
    return 잘못됨?0:SMS;
}
