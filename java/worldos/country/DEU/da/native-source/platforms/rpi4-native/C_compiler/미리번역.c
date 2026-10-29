#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "bundt.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned varighed_VÆRDI,aktuel_placere;static int it_ugyldig;
static unsigned Mærker_Liste[512],첫째값[512],SEKUND_VÆRDI[512],konstant_pulje,aktuel_Hold;
static char Tekst[65536];static unsigned Tekststørrelse;
typedef struct {unsigned konfiguration_BITS,Navn,서술값,명령열,Størrelse,지역변수들,Stak_Lager;} metode_post;
static metode_post 메소드목록[64];static unsigned 메소드개수;
static unsigned feltnavn[64],필드서술[64],felt_konstant[64],필드개수;
static unsigned TAG_VÆRDI(unsigned vare_TÆL){if(aktuel_placere>varighed_VÆRDI||vare_TÆL>varighed_VÆRDI-aktuel_placere){it_ugyldig=1;return 0;}unsigned data_placere=aktuel_placere;aktuel_placere+=vare_TÆL;return data_placere;}
static unsigned byte_data(void){unsigned data_placere=TAG_VÆRDI(1);return it_ugyldig?0:data[data_placere];}
static unsigned 절반값(void){unsigned X_koordinat=byte_data();return X_koordinat<<8|byte_data();}
static uint32_t 가득참(void){uint32_t X_koordinat=절반값();return X_koordinat<<16|절반값();}
static int UNICODE_VÆRDI(unsigned 순번,const char*streng_data){return 순번>0&&순번<konstant_pulje&&Mærker_Liste[순번]==1&&strlen(streng_data)==SEKUND_VÆRDI[순번]&&!memcmp(data+첫째값[순번],streng_data,SEKUND_VÆRDI[순번]);}
static int 같음(unsigned X_koordinat,unsigned Y_koordinat){return X_koordinat>0&&X_koordinat<konstant_pulje&&Y_koordinat>0&&Y_koordinat<konstant_pulje&&Mærker_Liste[X_koordinat]==1&&Mærker_Liste[Y_koordinat]==1&&SEKUND_VÆRDI[X_koordinat]==SEKUND_VÆRDI[Y_koordinat]&&!memcmp(data+첫째값[X_koordinat],data+첫째값[Y_koordinat],SEKUND_VÆRDI[X_koordinat]);}
static void 내보내기(const char*fil_post,...){if(it_ugyldig)return;va_list argument_MATRIX;va_start(argument_MATRIX,fil_post);int vare_TÆL=vsnprintf(Tekst+Tekststørrelse,sizeof(Tekst)-Tekststørrelse,fil_post,argument_MATRIX);va_end(argument_MATRIX);if(vare_TÆL<0||(unsigned)vare_TÆL>=sizeof(Tekst)-Tekststørrelse){it_ugyldig=1;return;}Tekststørrelse+=vare_TÆL;}
static int 서술자(unsigned identifikator_VÆRDI,int*KR){
    if(identifikator_VÆRDI<1||identifikator_VÆRDI>=konstant_pulje||Mærker_Liste[identifikator_VÆRDI]!=1)return -1;unsigned data_placere=첫째값[identifikator_VÆRDI],afslutte_et_opkald_FORSKYDNING=data_placere+SEKUND_VÆRDI[identifikator_VÆRDI];if(data_placere>=afslutte_et_opkald_FORSKYDNING||data[data_placere++]!='(')return -1;int post_TÆL_8f7753a1=0;
    while(data_placere<afslutte_et_opkald_FORSKYDNING&&data[data_placere]!=')'){
        unsigned tegnkode=data[data_placere++];while(tegnkode=='['&&data_placere<afslutte_et_opkald_FORSKYDNING)tegnkode=data[data_placere++];
        if(tegnkode=='L'){while(data_placere<afslutte_et_opkald_FORSKYDNING&&data[data_placere]!=';')data_placere++;if(data_placere==afslutte_et_opkald_FORSKYDNING)return -1;data_placere++;}
        else if(tegnkode!='I'&&tegnkode!='Z'&&tegnkode!='B'&&tegnkode!='C'&&tegnkode!='S')return -1;
        if(++post_TÆL_8f7753a1>16)return -1;
    }
    if(data_placere+1>=afslutte_et_opkald_FORSKYDNING||data[data_placere++]!=')')return -1;*KR=data[data_placere]=='V'?0:1;
    if(data[data_placere]=='J'||data[data_placere]=='D'||data[data_placere]=='F')return -1;return post_TÆL_8f7753a1;
}
static void egenskaber(void){unsigned vare_TÆL=절반값();for(unsigned 순번=0;순번<vare_TÆL&&!it_ugyldig;순번++){절반값();unsigned Størrelse=가득참();TAG_VÆRDI(Størrelse);}}
static int opdele_tekst_input(void){
    if(가득참()!=0xcafebabe)return -1;unsigned mindre_version=절반값(),versionsnummer=절반값();if(mindre_version||versionsnummer<45||versionsnummer>52)return -1;
    konstant_pulje=절반값();if(konstant_pulje<1||konstant_pulje>512)return -1;
    for(unsigned 순번=1;순번<konstant_pulje&&!it_ugyldig;순번++){
        Mærker_Liste[순번]=byte_data();switch(Mærker_Liste[순번]){
        case 1:SEKUND_VÆRDI[순번]=절반값();첫째값[순번]=TAG_VÆRDI(SEKUND_VÆRDI[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAG_VÆRDI(8);if(++순번>=konstant_pulje)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEKUND_VÆRDI[순번]=절반값();break;
        case 15:첫째값[순번]=byte_data();SEKUND_VÆRDI[순번]=절반값();break;default:return -1;
        }
    }
    절반값();aktuel_Hold=절반값();절반값();if(aktuel_Hold<1||aktuel_Hold>=konstant_pulje||Mærker_Liste[aktuel_Hold]!=7||첫째값[aktuel_Hold]<1||첫째값[aktuel_Hold]>=konstant_pulje||Mærker_Liste[첫째값[aktuel_Hold]]!=1)return -1;unsigned 인터페이스목록=절반값();TAG_VÆRDI(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!it_ugyldig;순번++){
        unsigned konfiguration_BITS=절반값();feltnavn[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfiguration_BITS&8))return -1;
        unsigned post_TÆL_8f7753a1=절반값();for(unsigned 안쪽순번=0;안쪽순번<post_TÆL_8f7753a1&&!it_ugyldig;안쪽순번++){
            unsigned Navn=절반값(),Størrelse=가득참();
            if(UNICODE_VÆRDI(Navn,"ConstantValue")){if(Størrelse!=2)return -1;felt_konstant[순번]=절반값();}
            else TAG_VÆRDI(Størrelse);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!it_ugyldig;순번++){
        metode_post*gruppe_tilpasse_størrelse=메소드목록+순번;gruppe_tilpasse_størrelse->konfiguration_BITS=절반값();gruppe_tilpasse_størrelse->Navn=절반값();gruppe_tilpasse_størrelse->서술값=절반값();unsigned post_TÆL_8f7753a1=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<post_TÆL_8f7753a1&&!it_ugyldig;안쪽순번++){
            unsigned Navn=절반값(),Størrelse=가득참(),Kør_2=aktuel_placere;
            if(Størrelse>varighed_VÆRDI-aktuel_placere)return -1;
            if(UNICODE_VÆRDI(Navn,"Code")){
                gruppe_tilpasse_størrelse->Stak_Lager=절반값();gruppe_tilpasse_størrelse->지역변수들=절반값();gruppe_tilpasse_størrelse->Størrelse=가득참();gruppe_tilpasse_størrelse->명령열=TAG_VÆRDI(gruppe_tilpasse_størrelse->Størrelse);
                if(gruppe_tilpasse_størrelse->Stak_Lager>128||gruppe_tilpasse_størrelse->지역변수들>128||gruppe_tilpasse_størrelse->Størrelse>8192||절반값())return -1;egenskaber();
            }else TAG_VÆRDI(Størrelse);
            if(aktuel_placere!=Kør_2+Størrelse)return -1;
        }
        if(!UNICODE_VÆRDI(gruppe_tilpasse_størrelse->Navn,"<init>")&&(!(gruppe_tilpasse_størrelse->konfiguration_BITS&8)||(gruppe_tilpasse_størrelse->konfiguration_BITS&(0x100|0x20))||!gruppe_tilpasse_størrelse->Størrelse))return -1;
    }
    egenskaber();return it_ugyldig||aktuel_placere!=varighed_VÆRDI?-1:0;
}
static void konstant_VÆRDI(unsigned identifikator_VÆRDI){
    if(!identifikator_VÆRDI||identifikator_VÆRDI>=konstant_pulje){it_ugyldig=1;return;}
    if(Mærker_Liste[identifikator_VÆRDI]==3)내보내기("P(%uU);",첫째값[identifikator_VÆRDI]);
    else if(Mærker_Liste[identifikator_VÆRDI]==8)내보내기("P((W)k%u);",identifikator_VÆRDI);else it_ugyldig=1;
}
static void 호출(unsigned identifikator_VÆRDI,int virtuel_KALD){
    if(identifikator_VÆRDI<1||identifikator_VÆRDI>=konstant_pulje||(Mærker_Liste[identifikator_VÆRDI]!=10&&Mærker_Liste[identifikator_VÆRDI]!=11)||첫째값[identifikator_VÆRDI]<1||첫째값[identifikator_VÆRDI]>=konstant_pulje||Mærker_Liste[첫째값[identifikator_VÆRDI]]!=7||SEKUND_VÆRDI[identifikator_VÆRDI]<1||SEKUND_VÆRDI[identifikator_VÆRDI]>=konstant_pulje||Mærker_Liste[SEKUND_VÆRDI[identifikator_VÆRDI]]!=12){it_ugyldig=1;return;}
    unsigned ejer_objekt=첫째값[첫째값[identifikator_VÆRDI]],Navn=첫째값[SEKUND_VÆRDI[identifikator_VÆRDI]],서술값=SEKUND_VÆRDI[SEKUND_VÆRDI[identifikator_VÆRDI]];int KR=0,vare_TÆL=서술자(서술값,&KR);if(vare_TÆL<0){it_ugyldig=1;return;}
    for(int 순번=vare_TÆL;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuel_KALD)내보내기("Q();");
    if(!virtuel_KALD&&같음(ejer_objekt,첫째값[aktuel_Hold])){
        unsigned gruppe_tilpasse_størrelse=0;for(;gruppe_tilpasse_størrelse<메소드개수;gruppe_tilpasse_størrelse++)if(같음(Navn,메소드목록[gruppe_tilpasse_størrelse].Navn)&&같음(서술값,메소드목록[gruppe_tilpasse_størrelse].서술값))break;
        if(gruppe_tilpasse_størrelse==메소드개수||!(메소드목록[gruppe_tilpasse_størrelse].konfiguration_BITS&8)){it_ugyldig=1;return;}
        if(KR)내보내기("P(");내보내기("m%u(",gruppe_tilpasse_størrelse);for(int 순번=0;순번<vare_TÆL;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(KR?"));":" );");return;
    }
    if((virtuel_KALD&&UNICODE_VÆRDI(ejer_objekt,"java/io/PrintStream")&& (UNICODE_VÆRDI(Navn,"print")||UNICODE_VÆRDI(Navn,"println")))||(!virtuel_KALD&&UNICODE_VÆRDI(ejer_objekt,"Dansk/eget/Udgang"))){
        if(UNICODE_VÆRDI(서술값,"(I)V")&&(UNICODE_VÆRDI(Navn,"print")||UNICODE_VÆRDI(Navn,"println")||UNICODE_VÆRDI(Navn,"skrive_tal"))){내보내기("jprint(x[0],1,%d);",UNICODE_VÆRDI(Navn,"print")?0:1);return;}
        if(UNICODE_VÆRDI(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VÆRDI(Navn,"print")||UNICODE_VÆRDI(Navn,"println")||UNICODE_VÆRDI(Navn,"Skrive")||UNICODE_VÆRDI(Navn,"skrive_linje"))){내보내기("jprint(x[0],0,%d);",UNICODE_VÆRDI(Navn,"print")||UNICODE_VÆRDI(Navn,"Skrive")?0:1);return;}
        if(UNICODE_VÆRDI(서술값,"()V")&&UNICODE_VÆRDI(Navn,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuel_KALD&&UNICODE_VÆRDI(ejer_objekt,"Dansk/eget/Fil")){
        if(UNICODE_VÆRDI(Navn,"Skrive")&&UNICODE_VÆRDI(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VÆRDI(Navn,"Læse")&&UNICODE_VÆRDI(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    it_ugyldig=1;
}
static void kompilere_metode(unsigned Opslag_INDEKS){
    metode_post*gruppe_tilpasse_størrelse=메소드목록+Opslag_INDEKS;if(UNICODE_VÆRDI(gruppe_tilpasse_størrelse->Navn,"<init>"))return;int KR,vare_TÆL=서술자(gruppe_tilpasse_størrelse->서술값,&KR);if(vare_TÆL<0){it_ugyldig=1;return;}
    내보내기("static W m%u(",Opslag_INDEKS);for(int 순번=0;순번<vare_TÆL;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!vare_TÆL)내보내기("void");
    if((unsigned)vare_TÆL>gruppe_tilpasse_størrelse->지역변수들){it_ugyldig=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",gruppe_tilpasse_størrelse->지역변수들?gruppe_tilpasse_størrelse->지역변수들:1);for(int 순번=0;순번<vare_TÆL;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=varighed_VÆRDI;varighed_VÆRDI=gruppe_tilpasse_størrelse->명령열+gruppe_tilpasse_størrelse->Størrelse;aktuel_placere=gruppe_tilpasse_størrelse->명령열;
    while(aktuel_placere<varighed_VÆRDI&&!it_ugyldig){unsigned kommando_placere=aktuel_placere-gruppe_tilpasse_størrelse->명령열,kirurgi_VÆRDI=byte_data();내보내기("L%u:;",kommando_placere);
        if(kirurgi_VÆRDI==0){}
        else if(kirurgi_VÆRDI==1)내보내기("P(0);");
        else if(kirurgi_VÆRDI>=2&&kirurgi_VÆRDI<=8)내보내기("P(%uU);",kirurgi_VÆRDI-3);
        else if(kirurgi_VÆRDI==16){int VÆRDI=(int8_t)byte_data();내보내기("P(%uU);",(unsigned)VÆRDI);}
        else if(kirurgi_VÆRDI==17){int VÆRDI=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VÆRDI);}
        else if(kirurgi_VÆRDI==18||kirurgi_VÆRDI==19)konstant_VÆRDI(kirurgi_VÆRDI==18?byte_data():절반값());
        else if(kirurgi_VÆRDI==21||kirurgi_VÆRDI==25){unsigned 순번=byte_data();if(순번>=gruppe_tilpasse_størrelse->지역변수들)it_ugyldig=1;내보내기("P(v[%u]);",순번);}
        else if((kirurgi_VÆRDI>=26&&kirurgi_VÆRDI<=29)||(kirurgi_VÆRDI>=42&&kirurgi_VÆRDI<=45)){unsigned 순번=kirurgi_VÆRDI>=42?kirurgi_VÆRDI-42:kirurgi_VÆRDI-26;if(순번>=gruppe_tilpasse_størrelse->지역변수들)it_ugyldig=1;내보내기("P(v[%u]);",순번);}
        else if(kirurgi_VÆRDI==54||kirurgi_VÆRDI==58){unsigned 순번=byte_data();if(순번>=gruppe_tilpasse_størrelse->지역변수들)it_ugyldig=1;내보내기("v[%u]=Q();",순번);}
        else if((kirurgi_VÆRDI>=59&&kirurgi_VÆRDI<=62)||(kirurgi_VÆRDI>=75&&kirurgi_VÆRDI<=78)){unsigned 순번=kirurgi_VÆRDI>=75?kirurgi_VÆRDI-75:kirurgi_VÆRDI-59;if(순번>=gruppe_tilpasse_størrelse->지역변수들)it_ugyldig=1;내보내기("v[%u]=Q();",순번);}
        else if(kirurgi_VÆRDI==46||kirurgi_VÆRDI==50||kirurgi_VÆRDI==51||kirurgi_VÆRDI==52||kirurgi_VÆRDI==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(kirurgi_VÆRDI==79||kirurgi_VÆRDI==83||kirurgi_VÆRDI==84||kirurgi_VÆRDI==85||kirurgi_VÆRDI==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",kirurgi_VÆRDI==84?"(unsigned)(signed char)q":kirurgi_VÆRDI==85?"(unsigned short)q":kirurgi_VÆRDI==86?"(unsigned)(short)q":"q");
        else if(kirurgi_VÆRDI==87)내보내기("Q();");
        else if(kirurgi_VÆRDI==89)내보내기("q=Q();P(q);P(q);");
        else if(kirurgi_VÆRDI==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(kirurgi_VÆRDI==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(kirurgi_VÆRDI==96||kirurgi_VÆRDI==100||kirurgi_VÆRDI==104||kirurgi_VÆRDI==120||kirurgi_VÆRDI==124||kirurgi_VÆRDI==126||kirurgi_VÆRDI==128||kirurgi_VÆRDI==130){const char*kodning_VÆRDI=kirurgi_VÆRDI==96?"+":kirurgi_VÆRDI==100?"-":kirurgi_VÆRDI==104?"*":kirurgi_VÆRDI==120?"<<":kirurgi_VÆRDI==124?">>":kirurgi_VÆRDI==126?"&":kirurgi_VÆRDI==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodning_VÆRDI,kirurgi_VÆRDI==120||kirurgi_VÆRDI==124?"%32":"");}
        else if(kirurgi_VÆRDI==108||kirurgi_VÆRDI==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",kirurgi_VÆRDI==112);
        else if(kirurgi_VÆRDI==116)내보내기("P(0U-(unsigned)Q());");
        else if(kirurgi_VÆRDI==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(kirurgi_VÆRDI==132){unsigned 순번=byte_data();int 차이=(int8_t)byte_data();if(순번>=gruppe_tilpasse_størrelse->지역변수들)it_ugyldig=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(kirurgi_VÆRDI>=145&&kirurgi_VÆRDI<=147)내보내기("P((unsigned)(%s)Q());",kirurgi_VÆRDI==145?"signed char":kirurgi_VÆRDI==146?"unsigned short":"short");
        else if(kirurgi_VÆRDI>=153&&kirurgi_VÆRDI<=166){int mål=(int)kommando_placere+(int16_t)절반값();const char*Sammenligning_VÆRDI[]={"==","!=","<",">=",">","<="};if(mål<0||mål>=(int)gruppe_tilpasse_størrelse->Størrelse){it_ugyldig=1;break;}if(kirurgi_VÆRDI<159)내보내기("if((int)Q()%s0)goto L%d;",Sammenligning_VÆRDI[kirurgi_VÆRDI-153],mål);else if(kirurgi_VÆRDI<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Sammenligning_VÆRDI[kirurgi_VÆRDI-159],mål);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",kirurgi_VÆRDI==165?"==":"!=",mål);}
        else if(kirurgi_VÆRDI==167){int mål=(int)kommando_placere+(int16_t)절반값();if(mål<0||mål>=(int)gruppe_tilpasse_størrelse->Størrelse)it_ugyldig=1;내보내기("goto L%d;",mål);}
        else if(kirurgi_VÆRDI==172||kirurgi_VÆRDI==176)내보내기("return Q();");else if(kirurgi_VÆRDI==177)내보내기("return 0;");
        else if(kirurgi_VÆRDI==178||kirurgi_VÆRDI==179){unsigned identifikator_VÆRDI=절반값();if(identifikator_VÆRDI<1||identifikator_VÆRDI>=konstant_pulje||Mærker_Liste[identifikator_VÆRDI]!=9||첫째값[identifikator_VÆRDI]>=konstant_pulje||SEKUND_VÆRDI[identifikator_VÆRDI]>=konstant_pulje||Mærker_Liste[첫째값[identifikator_VÆRDI]]!=7||Mærker_Liste[SEKUND_VÆRDI[identifikator_VÆRDI]]!=12){it_ugyldig=1;break;}unsigned ejer_objekt=첫째값[첫째값[identifikator_VÆRDI]],Navn=첫째값[SEKUND_VÆRDI[identifikator_VÆRDI]],서술값=SEKUND_VÆRDI[SEKUND_VÆRDI[identifikator_VÆRDI]];
            if(kirurgi_VÆRDI==178&&UNICODE_VÆRDI(ejer_objekt,"java/lang/System")&&UNICODE_VÆRDI(Navn,"out")&&UNICODE_VÆRDI(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fil_post=0;while(fil_post<필드개수&&(!같음(Navn,feltnavn[fil_post])||!같음(서술값,필드서술[fil_post])))fil_post++;if(!같음(ejer_objekt,첫째값[aktuel_Hold])||fil_post==필드개수){it_ugyldig=1;break;}내보내기(kirurgi_VÆRDI==178?"P(fields[%u]);":"fields[%u]=Q();",fil_post);}}
        else if(kirurgi_VÆRDI==182||kirurgi_VÆRDI==184)호출(절반값(),kirurgi_VÆRDI==182);
        else if(kirurgi_VÆRDI==188){unsigned Type_område=byte_data();if(Type_område!=4&&Type_område!=5&&Type_område!=8&&Type_område!=9&&Type_område!=10)it_ugyldig=1;내보내기("P(jarray((int)Q()));");}
        else if(kirurgi_VÆRDI==190)내보내기("P(jlength(Q()));");
        else if(kirurgi_VÆRDI==198||kirurgi_VÆRDI==199){int mål=(int)kommando_placere+(int16_t)절반값();if(mål<0||mål>=(int)gruppe_tilpasse_størrelse->Størrelse)it_ugyldig=1;내보내기("if(Q()%s0)goto L%d;",kirurgi_VÆRDI==198?"==":"!=",mål);}
        else it_ugyldig=1;
        if(it_ugyldig)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",Opslag_INDEKS,kirurgi_VÆRDI,kommando_placere);
        내보내기("\n");
    }
    varighed_VÆRDI=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned streng_enhed(unsigned *data_placere,unsigned afslutte_et_opkald_FORSKYDNING){
    if(*data_placere>=afslutte_et_opkald_FORSKYDNING){it_ugyldig=1;return 0;}unsigned tegnkode=data[(*data_placere)++];
    if(tegnkode<128)return tegnkode;
    unsigned vare_TÆL=tegnkode>=0xc0&&tegnkode<=0xdf?1:tegnkode>=0xe0&&tegnkode<=0xef?2:3;
    if(vare_TÆL==3||vare_TÆL>afslutte_et_opkald_FORSKYDNING-*data_placere){it_ugyldig=1;return 0;}unsigned VÆRDI=tegnkode&((1u<<(6-vare_TÆL))-1);
    for(unsigned 순번=0;순번<vare_TÆL;순번++){unsigned Næste_vare=data[(*data_placere)++];if((Næste_vare&0xc0)!=0x80)it_ugyldig=1;VÆRDI=VÆRDI<<6|(Næste_vare&63);}
    if((vare_TÆL==1&&VÆRDI<128&&VÆRDI!=0)||(vare_TÆL==2&&VÆRDI<2048))it_ugyldig=1;return VÆRDI;
}
static void streng_konstant(unsigned identifikator_VÆRDI){
    unsigned 부호없는값=첫째값[identifikator_VÆRDI];if(부호없는값<1||부호없는값>=konstant_pulje||Mærker_Liste[부호없는값]!=1){it_ugyldig=1;return;}내보내기("static const unsigned char k%u[]={",identifikator_VÆRDI);
    unsigned data_placere=첫째값[부호없는값],afslutte_et_opkald_FORSKYDNING=data_placere+SEKUND_VÆRDI[부호없는값];
    while(data_placere<afslutte_et_opkald_FORSKYDNING&&!it_ugyldig){unsigned tegnkode=streng_enhed(&data_placere,afslutte_et_opkald_FORSKYDNING);
        if(tegnkode>=0xd800&&tegnkode<=0xdbff){unsigned 낮은부분=streng_enhed(&data_placere,afslutte_et_opkald_FORSKYDNING);if(낮은부분<0xdc00||낮은부분>0xdfff){it_ugyldig=1;break;}tegnkode=0x10000+((tegnkode-0xd800)<<10)+낮은부분-0xdc00;}
        else if(tegnkode>=0xdc00&&tegnkode<=0xdfff){it_ugyldig=1;break;}
        if(!tegnkode){printf("jaot: embedded NUL string needs JVM mode\n");it_ugyldig=1;break;}
        if(tegnkode<128)내보내기("%u,",tegnkode);
        else{unsigned vare_TÆL=tegnkode<2048?2:tegnkode<65536?3:4;내보내기("%u,",(vare_TÆL==2?0xc0:vare_TÆL==3?0xe0:0xf0)|(tegnkode>>(6*(vare_TÆL-1))));for(unsigned 순번=vare_TÆL-1;순번;순번--)내보내기("%u,",0x80|((tegnkode>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Navn){
    size_t vare_TÆL=strlen(Navn);
    if(vare_TÆL>4&&!strcmp(Navn+vare_TÆL-4,".jar")){
        if(꾸러미열기(Navn)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Sti[256];const char*post_metode=꾸러미진입클래스();vare_TÆL=strlen(post_metode);if(vare_TÆL+6>=sizeof(Sti))return 0;
        for(unsigned 순번=0;순번<vare_TÆL;순번++)Sti[순번]=post_metode[순번]=='.'?'/':post_metode[순번];strcpy(Sti+vare_TÆL,".class");int post_TÆL_8f7753a1=꾸러미읽기(Sti,data,sizeof(data));if(post_TÆL_8f7753a1<0)return 0;varighed_VÆRDI=post_TÆL_8f7753a1;
    }else{intptr_t fil_handle=사용자호출(3,(uintptr_t)Navn,0,0,0,0,0);if(fil_handle<0)return 0;intptr_t post_TÆL_8f7753a1=사용자호출(9,fil_handle,0,0,0,0,0);if(post_TÆL_8f7753a1<0||post_TÆL_8f7753a1>sizeof(data)){사용자호출(4,fil_handle,0,0,0,0,0);return 0;}intptr_t MODTAGET_VED_UDLØB_TÆL=사용자호출(2,fil_handle,(uintptr_t)data,post_TÆL_8f7753a1,0,0,0);사용자호출(4,fil_handle,0,0,0,0,0);if(MODTAGET_VED_UDLØB_TÆL!=post_TÆL_8f7753a1)return 0;varighed_VÆRDI=post_TÆL_8f7753a1;}
    if(opdele_tekst_input()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstant_pulje&&!it_ugyldig;순번++)if(Mærker_Liste[순번]==8)streng_konstant(순번);
    if(it_ugyldig)return 0;
    int indgangspunkt=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VÆRDI(메소드목록[순번].Navn,"<init>")){
        int KR,post_TÆL_8f7753a1=서술자(메소드목록[순번].서술값,&KR);if(post_TÆL_8f7753a1<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<post_TÆL_8f7753a1;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!post_TÆL_8f7753a1)내보내기("void");내보내기(");\n");
        if(UNICODE_VÆRDI(메소드목록[순번].Navn,"main")&&UNICODE_VÆRDI(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfiguration_BITS&9)==9)indgangspunkt=순번;
        if(UNICODE_VÆRDI(메소드목록[순번].Navn,"<clinit>"))초기값=순번;
    }
    if(indgangspunkt<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!it_ugyldig;순번++)kompilere_metode(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(felt_konstant[순번]){
        unsigned tegnkode=felt_konstant[순번];if(tegnkode>=konstant_pulje)return 0;
        if(Mærker_Liste[tegnkode]==3)내보내기("fields[%u]=%uU;",순번,첫째값[tegnkode]);else if(Mærker_Liste[tegnkode]==8)내보내기("fields[%u]=(W)k%u;",순번,tegnkode);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",indgangspunkt);
    return it_ugyldig?0:Tekst;
}
