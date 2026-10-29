#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "bunt.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned lengde_VERDI,betalt_plassere;static int informasjonssystemer_ugyldig;
static unsigned Merker_Liste[512],첫째값[512],SEKUND_VERDI[512],konstant_pulje,betalt_time;
static char Tekst[65536];static unsigned Tekststørrelse;
typedef struct {unsigned konfigurasjon_BITS,Navn,서술값,명령열,Størrelse,지역변수들,stakk_lager;} metode_oppføring;
static metode_oppføring 메소드목록[64];static unsigned 메소드개수;
static unsigned feltnavn[64],필드서술[64],felt_konstant[64],필드개수;
static unsigned TA_VERDI(unsigned vare_ANTALL){if(betalt_plassere>lengde_VERDI||vare_ANTALL>lengde_VERDI-betalt_plassere){informasjonssystemer_ugyldig=1;return 0;}unsigned data_plassere=betalt_plassere;betalt_plassere+=vare_ANTALL;return data_plassere;}
static unsigned byte_data(void){unsigned data_plassere=TA_VERDI(1);return informasjonssystemer_ugyldig?0:data[data_plassere];}
static unsigned 절반값(void){unsigned x_koordinat=byte_data();return x_koordinat<<8|byte_data();}
static uint32_t 가득참(void){uint32_t x_koordinat=절반값();return x_koordinat<<16|절반값();}
static int UNICODE_VERDI(unsigned 순번,const char*streng_data){return 순번>0&&순번<konstant_pulje&&Merker_Liste[순번]==1&&strlen(streng_data)==SEKUND_VERDI[순번]&&!memcmp(data+첫째값[순번],streng_data,SEKUND_VERDI[순번]);}
static int 같음(unsigned x_koordinat,unsigned Y_koordinat){return x_koordinat>0&&x_koordinat<konstant_pulje&&Y_koordinat>0&&Y_koordinat<konstant_pulje&&Merker_Liste[x_koordinat]==1&&Merker_Liste[Y_koordinat]==1&&SEKUND_VERDI[x_koordinat]==SEKUND_VERDI[Y_koordinat]&&!memcmp(data+첫째값[x_koordinat],data+첫째값[Y_koordinat],SEKUND_VERDI[x_koordinat]);}
static void 내보내기(const char*Fil_oppføring,...){if(informasjonssystemer_ugyldig)return;va_list argument_MATRISE;va_start(argument_MATRISE,Fil_oppføring);int vare_ANTALL=vsnprintf(Tekst+Tekststørrelse,sizeof(Tekst)-Tekststørrelse,Fil_oppføring,argument_MATRISE);va_end(argument_MATRISE);if(vare_ANTALL<0||(unsigned)vare_ANTALL>=sizeof(Tekst)-Tekststørrelse){informasjonssystemer_ugyldig=1;return;}Tekststørrelse+=vare_ANTALL;}
static int 서술자(unsigned identifikator_VERDI,int*KR){
    if(identifikator_VERDI<1||identifikator_VERDI>=konstant_pulje||Merker_Liste[identifikator_VERDI]!=1)return -1;unsigned data_plassere=첫째값[identifikator_VERDI],avslutte_en_samtale_FORSKYVNING=data_plassere+SEKUND_VERDI[identifikator_VERDI];if(data_plassere>=avslutte_en_samtale_FORSKYVNING||data[data_plassere++]!='(')return -1;int oppføring_ANTALL=0;
    while(data_plassere<avslutte_en_samtale_FORSKYVNING&&data[data_plassere]!=')'){
        unsigned tegnkode=data[data_plassere++];while(tegnkode=='['&&data_plassere<avslutte_en_samtale_FORSKYVNING)tegnkode=data[data_plassere++];
        if(tegnkode=='L'){while(data_plassere<avslutte_en_samtale_FORSKYVNING&&data[data_plassere]!=';')data_plassere++;if(data_plassere==avslutte_en_samtale_FORSKYVNING)return -1;data_plassere++;}
        else if(tegnkode!='I'&&tegnkode!='Z'&&tegnkode!='B'&&tegnkode!='C'&&tegnkode!='S')return -1;
        if(++oppføring_ANTALL>16)return -1;
    }
    if(data_plassere+1>=avslutte_en_samtale_FORSKYVNING||data[data_plassere++]!=')')return -1;*KR=data[data_plassere]=='V'?0:1;
    if(data[data_plassere]=='J'||data[data_plassere]=='D'||data[data_plassere]=='F')return -1;return oppføring_ANTALL;
}
static void attributter(void){unsigned vare_ANTALL=절반값();for(unsigned 순번=0;순번<vare_ANTALL&&!informasjonssystemer_ugyldig;순번++){절반값();unsigned Størrelse=가득참();TA_VERDI(Størrelse);}}
static int dele_opp_inndata(void){
    if(가득참()!=0xcafebabe)return -1;unsigned underordnet_versjon=절반값(),versjonsnummer=절반값();if(underordnet_versjon||versjonsnummer<45||versjonsnummer>52)return -1;
    konstant_pulje=절반값();if(konstant_pulje<1||konstant_pulje>512)return -1;
    for(unsigned 순번=1;순번<konstant_pulje&&!informasjonssystemer_ugyldig;순번++){
        Merker_Liste[순번]=byte_data();switch(Merker_Liste[순번]){
        case 1:SEKUND_VERDI[순번]=절반값();첫째값[순번]=TA_VERDI(SEKUND_VERDI[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TA_VERDI(8);if(++순번>=konstant_pulje)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEKUND_VERDI[순번]=절반값();break;
        case 15:첫째값[순번]=byte_data();SEKUND_VERDI[순번]=절반값();break;default:return -1;
        }
    }
    절반값();betalt_time=절반값();절반값();if(betalt_time<1||betalt_time>=konstant_pulje||Merker_Liste[betalt_time]!=7||첫째값[betalt_time]<1||첫째값[betalt_time]>=konstant_pulje||Merker_Liste[첫째값[betalt_time]]!=1)return -1;unsigned 인터페이스목록=절반값();TA_VERDI(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informasjonssystemer_ugyldig;순번++){
        unsigned konfigurasjon_BITS=절반값();feltnavn[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfigurasjon_BITS&8))return -1;
        unsigned oppføring_ANTALL=절반값();for(unsigned 안쪽순번=0;안쪽순번<oppføring_ANTALL&&!informasjonssystemer_ugyldig;안쪽순번++){
            unsigned Navn=절반값(),Størrelse=가득참();
            if(UNICODE_VERDI(Navn,"ConstantValue")){if(Størrelse!=2)return -1;felt_konstant[순번]=절반값();}
            else TA_VERDI(Størrelse);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informasjonssystemer_ugyldig;순번++){
        metode_oppføring*gruppe_skalere=메소드목록+순번;gruppe_skalere->konfigurasjon_BITS=절반값();gruppe_skalere->Navn=절반값();gruppe_skalere->서술값=절반값();unsigned oppføring_ANTALL=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<oppføring_ANTALL&&!informasjonssystemer_ugyldig;안쪽순번++){
            unsigned Navn=절반값(),Størrelse=가득참(),Kjør_2=betalt_plassere;
            if(Størrelse>lengde_VERDI-betalt_plassere)return -1;
            if(UNICODE_VERDI(Navn,"Code")){
                gruppe_skalere->stakk_lager=절반값();gruppe_skalere->지역변수들=절반값();gruppe_skalere->Størrelse=가득참();gruppe_skalere->명령열=TA_VERDI(gruppe_skalere->Størrelse);
                if(gruppe_skalere->stakk_lager>128||gruppe_skalere->지역변수들>128||gruppe_skalere->Størrelse>8192||절반값())return -1;attributter();
            }else TA_VERDI(Størrelse);
            if(betalt_plassere!=Kjør_2+Størrelse)return -1;
        }
        if(!UNICODE_VERDI(gruppe_skalere->Navn,"<init>")&&(!(gruppe_skalere->konfigurasjon_BITS&8)||(gruppe_skalere->konfigurasjon_BITS&(0x100|0x20))||!gruppe_skalere->Størrelse))return -1;
    }
    attributter();return informasjonssystemer_ugyldig||betalt_plassere!=lengde_VERDI?-1:0;
}
static void konstant_VERDI(unsigned identifikator_VERDI){
    if(!identifikator_VERDI||identifikator_VERDI>=konstant_pulje){informasjonssystemer_ugyldig=1;return;}
    if(Merker_Liste[identifikator_VERDI]==3)내보내기("P(%uU);",첫째값[identifikator_VERDI]);
    else if(Merker_Liste[identifikator_VERDI]==8)내보내기("P((W)k%u);",identifikator_VERDI);else informasjonssystemer_ugyldig=1;
}
static void 호출(unsigned identifikator_VERDI,int virtuell_Ring){
    if(identifikator_VERDI<1||identifikator_VERDI>=konstant_pulje||(Merker_Liste[identifikator_VERDI]!=10&&Merker_Liste[identifikator_VERDI]!=11)||첫째값[identifikator_VERDI]<1||첫째값[identifikator_VERDI]>=konstant_pulje||Merker_Liste[첫째값[identifikator_VERDI]]!=7||SEKUND_VERDI[identifikator_VERDI]<1||SEKUND_VERDI[identifikator_VERDI]>=konstant_pulje||Merker_Liste[SEKUND_VERDI[identifikator_VERDI]]!=12){informasjonssystemer_ugyldig=1;return;}
    unsigned eier_objekt=첫째값[첫째값[identifikator_VERDI]],Navn=첫째값[SEKUND_VERDI[identifikator_VERDI]],서술값=SEKUND_VERDI[SEKUND_VERDI[identifikator_VERDI]];int KR=0,vare_ANTALL=서술자(서술값,&KR);if(vare_ANTALL<0){informasjonssystemer_ugyldig=1;return;}
    for(int 순번=vare_ANTALL;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuell_Ring)내보내기("Q();");
    if(!virtuell_Ring&&같음(eier_objekt,첫째값[betalt_time])){
        unsigned gruppe_skalere=0;for(;gruppe_skalere<메소드개수;gruppe_skalere++)if(같음(Navn,메소드목록[gruppe_skalere].Navn)&&같음(서술값,메소드목록[gruppe_skalere].서술값))break;
        if(gruppe_skalere==메소드개수||!(메소드목록[gruppe_skalere].konfigurasjon_BITS&8)){informasjonssystemer_ugyldig=1;return;}
        if(KR)내보내기("P(");내보내기("m%u(",gruppe_skalere);for(int 순번=0;순번<vare_ANTALL;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(KR?"));":" );");return;
    }
    if((virtuell_Ring&&UNICODE_VERDI(eier_objekt,"java/io/PrintStream")&& (UNICODE_VERDI(Navn,"print")||UNICODE_VERDI(Navn,"println")))||(!virtuell_Ring&&UNICODE_VERDI(eier_objekt,"norsk/eget/Utgang"))){
        if(UNICODE_VERDI(서술값,"(I)V")&&(UNICODE_VERDI(Navn,"print")||UNICODE_VERDI(Navn,"println")||UNICODE_VERDI(Navn,"skrive_nummer"))){내보내기("jprint(x[0],1,%d);",UNICODE_VERDI(Navn,"print")?0:1);return;}
        if(UNICODE_VERDI(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VERDI(Navn,"print")||UNICODE_VERDI(Navn,"println")||UNICODE_VERDI(Navn,"Skriv")||UNICODE_VERDI(Navn,"skrive_linje"))){내보내기("jprint(x[0],0,%d);",UNICODE_VERDI(Navn,"print")||UNICODE_VERDI(Navn,"Skriv")?0:1);return;}
        if(UNICODE_VERDI(서술값,"()V")&&UNICODE_VERDI(Navn,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuell_Ring&&UNICODE_VERDI(eier_objekt,"norsk/eget/Fil")){
        if(UNICODE_VERDI(Navn,"Skriv")&&UNICODE_VERDI(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VERDI(Navn,"Les")&&UNICODE_VERDI(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informasjonssystemer_ugyldig=1;
}
static void kompilere_metode(unsigned Oppslag_INDEKS){
    metode_oppføring*gruppe_skalere=메소드목록+Oppslag_INDEKS;if(UNICODE_VERDI(gruppe_skalere->Navn,"<init>"))return;int KR,vare_ANTALL=서술자(gruppe_skalere->서술값,&KR);if(vare_ANTALL<0){informasjonssystemer_ugyldig=1;return;}
    내보내기("static W m%u(",Oppslag_INDEKS);for(int 순번=0;순번<vare_ANTALL;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!vare_ANTALL)내보내기("void");
    if((unsigned)vare_ANTALL>gruppe_skalere->지역변수들){informasjonssystemer_ugyldig=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",gruppe_skalere->지역변수들?gruppe_skalere->지역변수들:1);for(int 순번=0;순번<vare_ANTALL;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=lengde_VERDI;lengde_VERDI=gruppe_skalere->명령열+gruppe_skalere->Størrelse;betalt_plassere=gruppe_skalere->명령열;
    while(betalt_plassere<lengde_VERDI&&!informasjonssystemer_ugyldig){unsigned kommando_plassere=betalt_plassere-gruppe_skalere->명령열,operasjon_VERDI=byte_data();내보내기("L%u:;",kommando_plassere);
        if(operasjon_VERDI==0){}
        else if(operasjon_VERDI==1)내보내기("P(0);");
        else if(operasjon_VERDI>=2&&operasjon_VERDI<=8)내보내기("P(%uU);",operasjon_VERDI-3);
        else if(operasjon_VERDI==16){int VERDI=(int8_t)byte_data();내보내기("P(%uU);",(unsigned)VERDI);}
        else if(operasjon_VERDI==17){int VERDI=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VERDI);}
        else if(operasjon_VERDI==18||operasjon_VERDI==19)konstant_VERDI(operasjon_VERDI==18?byte_data():절반값());
        else if(operasjon_VERDI==21||operasjon_VERDI==25){unsigned 순번=byte_data();if(순번>=gruppe_skalere->지역변수들)informasjonssystemer_ugyldig=1;내보내기("P(v[%u]);",순번);}
        else if((operasjon_VERDI>=26&&operasjon_VERDI<=29)||(operasjon_VERDI>=42&&operasjon_VERDI<=45)){unsigned 순번=operasjon_VERDI>=42?operasjon_VERDI-42:operasjon_VERDI-26;if(순번>=gruppe_skalere->지역변수들)informasjonssystemer_ugyldig=1;내보내기("P(v[%u]);",순번);}
        else if(operasjon_VERDI==54||operasjon_VERDI==58){unsigned 순번=byte_data();if(순번>=gruppe_skalere->지역변수들)informasjonssystemer_ugyldig=1;내보내기("v[%u]=Q();",순번);}
        else if((operasjon_VERDI>=59&&operasjon_VERDI<=62)||(operasjon_VERDI>=75&&operasjon_VERDI<=78)){unsigned 순번=operasjon_VERDI>=75?operasjon_VERDI-75:operasjon_VERDI-59;if(순번>=gruppe_skalere->지역변수들)informasjonssystemer_ugyldig=1;내보내기("v[%u]=Q();",순번);}
        else if(operasjon_VERDI==46||operasjon_VERDI==50||operasjon_VERDI==51||operasjon_VERDI==52||operasjon_VERDI==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operasjon_VERDI==79||operasjon_VERDI==83||operasjon_VERDI==84||operasjon_VERDI==85||operasjon_VERDI==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operasjon_VERDI==84?"(unsigned)(signed char)q":operasjon_VERDI==85?"(unsigned short)q":operasjon_VERDI==86?"(unsigned)(short)q":"q");
        else if(operasjon_VERDI==87)내보내기("Q();");
        else if(operasjon_VERDI==89)내보내기("q=Q();P(q);P(q);");
        else if(operasjon_VERDI==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operasjon_VERDI==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operasjon_VERDI==96||operasjon_VERDI==100||operasjon_VERDI==104||operasjon_VERDI==120||operasjon_VERDI==124||operasjon_VERDI==126||operasjon_VERDI==128||operasjon_VERDI==130){const char*koding_VERDI=operasjon_VERDI==96?"+":operasjon_VERDI==100?"-":operasjon_VERDI==104?"*":operasjon_VERDI==120?"<<":operasjon_VERDI==124?">>":operasjon_VERDI==126?"&":operasjon_VERDI==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",koding_VERDI,operasjon_VERDI==120||operasjon_VERDI==124?"%32":"");}
        else if(operasjon_VERDI==108||operasjon_VERDI==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operasjon_VERDI==112);
        else if(operasjon_VERDI==116)내보내기("P(0U-(unsigned)Q());");
        else if(operasjon_VERDI==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operasjon_VERDI==132){unsigned 순번=byte_data();int 차이=(int8_t)byte_data();if(순번>=gruppe_skalere->지역변수들)informasjonssystemer_ugyldig=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operasjon_VERDI>=145&&operasjon_VERDI<=147)내보내기("P((unsigned)(%s)Q());",operasjon_VERDI==145?"signed char":operasjon_VERDI==146?"unsigned short":"short");
        else if(operasjon_VERDI>=153&&operasjon_VERDI<=166){int mål=(int)kommando_plassere+(int16_t)절반값();const char*Sammenligning_VERDI[]={"==","!=","<",">=",">","<="};if(mål<0||mål>=(int)gruppe_skalere->Størrelse){informasjonssystemer_ugyldig=1;break;}if(operasjon_VERDI<159)내보내기("if((int)Q()%s0)goto L%d;",Sammenligning_VERDI[operasjon_VERDI-153],mål);else if(operasjon_VERDI<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Sammenligning_VERDI[operasjon_VERDI-159],mål);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operasjon_VERDI==165?"==":"!=",mål);}
        else if(operasjon_VERDI==167){int mål=(int)kommando_plassere+(int16_t)절반값();if(mål<0||mål>=(int)gruppe_skalere->Størrelse)informasjonssystemer_ugyldig=1;내보내기("goto L%d;",mål);}
        else if(operasjon_VERDI==172||operasjon_VERDI==176)내보내기("return Q();");else if(operasjon_VERDI==177)내보내기("return 0;");
        else if(operasjon_VERDI==178||operasjon_VERDI==179){unsigned identifikator_VERDI=절반값();if(identifikator_VERDI<1||identifikator_VERDI>=konstant_pulje||Merker_Liste[identifikator_VERDI]!=9||첫째값[identifikator_VERDI]>=konstant_pulje||SEKUND_VERDI[identifikator_VERDI]>=konstant_pulje||Merker_Liste[첫째값[identifikator_VERDI]]!=7||Merker_Liste[SEKUND_VERDI[identifikator_VERDI]]!=12){informasjonssystemer_ugyldig=1;break;}unsigned eier_objekt=첫째값[첫째값[identifikator_VERDI]],Navn=첫째값[SEKUND_VERDI[identifikator_VERDI]],서술값=SEKUND_VERDI[SEKUND_VERDI[identifikator_VERDI]];
            if(operasjon_VERDI==178&&UNICODE_VERDI(eier_objekt,"java/lang/System")&&UNICODE_VERDI(Navn,"out")&&UNICODE_VERDI(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Fil_oppføring=0;while(Fil_oppføring<필드개수&&(!같음(Navn,feltnavn[Fil_oppføring])||!같음(서술값,필드서술[Fil_oppføring])))Fil_oppføring++;if(!같음(eier_objekt,첫째값[betalt_time])||Fil_oppføring==필드개수){informasjonssystemer_ugyldig=1;break;}내보내기(operasjon_VERDI==178?"P(fields[%u]);":"fields[%u]=Q();",Fil_oppføring);}}
        else if(operasjon_VERDI==182||operasjon_VERDI==184)호출(절반값(),operasjon_VERDI==182);
        else if(operasjon_VERDI==188){unsigned Type_område=byte_data();if(Type_område!=4&&Type_område!=5&&Type_område!=8&&Type_område!=9&&Type_område!=10)informasjonssystemer_ugyldig=1;내보내기("P(jarray((int)Q()));");}
        else if(operasjon_VERDI==190)내보내기("P(jlength(Q()));");
        else if(operasjon_VERDI==198||operasjon_VERDI==199){int mål=(int)kommando_plassere+(int16_t)절반값();if(mål<0||mål>=(int)gruppe_skalere->Størrelse)informasjonssystemer_ugyldig=1;내보내기("if(Q()%s0)goto L%d;",operasjon_VERDI==198?"==":"!=",mål);}
        else informasjonssystemer_ugyldig=1;
        if(informasjonssystemer_ugyldig)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",Oppslag_INDEKS,operasjon_VERDI,kommando_plassere);
        내보내기("\n");
    }
    lengde_VERDI=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned streng_enhet(unsigned *data_plassere,unsigned avslutte_en_samtale_FORSKYVNING){
    if(*data_plassere>=avslutte_en_samtale_FORSKYVNING){informasjonssystemer_ugyldig=1;return 0;}unsigned tegnkode=data[(*data_plassere)++];
    if(tegnkode<128)return tegnkode;
    unsigned vare_ANTALL=tegnkode>=0xc0&&tegnkode<=0xdf?1:tegnkode>=0xe0&&tegnkode<=0xef?2:3;
    if(vare_ANTALL==3||vare_ANTALL>avslutte_en_samtale_FORSKYVNING-*data_plassere){informasjonssystemer_ugyldig=1;return 0;}unsigned VERDI=tegnkode&((1u<<(6-vare_ANTALL))-1);
    for(unsigned 순번=0;순번<vare_ANTALL;순번++){unsigned Neste_vare=data[(*data_plassere)++];if((Neste_vare&0xc0)!=0x80)informasjonssystemer_ugyldig=1;VERDI=VERDI<<6|(Neste_vare&63);}
    if((vare_ANTALL==1&&VERDI<128&&VERDI!=0)||(vare_ANTALL==2&&VERDI<2048))informasjonssystemer_ugyldig=1;return VERDI;
}
static void streng_konstant(unsigned identifikator_VERDI){
    unsigned 부호없는값=첫째값[identifikator_VERDI];if(부호없는값<1||부호없는값>=konstant_pulje||Merker_Liste[부호없는값]!=1){informasjonssystemer_ugyldig=1;return;}내보내기("static const unsigned char k%u[]={",identifikator_VERDI);
    unsigned data_plassere=첫째값[부호없는값],avslutte_en_samtale_FORSKYVNING=data_plassere+SEKUND_VERDI[부호없는값];
    while(data_plassere<avslutte_en_samtale_FORSKYVNING&&!informasjonssystemer_ugyldig){unsigned tegnkode=streng_enhet(&data_plassere,avslutte_en_samtale_FORSKYVNING);
        if(tegnkode>=0xd800&&tegnkode<=0xdbff){unsigned 낮은부분=streng_enhet(&data_plassere,avslutte_en_samtale_FORSKYVNING);if(낮은부분<0xdc00||낮은부분>0xdfff){informasjonssystemer_ugyldig=1;break;}tegnkode=0x10000+((tegnkode-0xd800)<<10)+낮은부분-0xdc00;}
        else if(tegnkode>=0xdc00&&tegnkode<=0xdfff){informasjonssystemer_ugyldig=1;break;}
        if(!tegnkode){printf("jaot: embedded NUL string needs JVM mode\n");informasjonssystemer_ugyldig=1;break;}
        if(tegnkode<128)내보내기("%u,",tegnkode);
        else{unsigned vare_ANTALL=tegnkode<2048?2:tegnkode<65536?3:4;내보내기("%u,",(vare_ANTALL==2?0xc0:vare_ANTALL==3?0xe0:0xf0)|(tegnkode>>(6*(vare_ANTALL-1))));for(unsigned 순번=vare_ANTALL-1;순번;순번--)내보내기("%u,",0x80|((tegnkode>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Navn){
    size_t vare_ANTALL=strlen(Navn);
    if(vare_ANTALL>4&&!strcmp(Navn+vare_ANTALL-4,".jar")){
        if(꾸러미열기(Navn)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Sti[256];const char*oppføring_metode=꾸러미진입클래스();vare_ANTALL=strlen(oppføring_metode);if(vare_ANTALL+6>=sizeof(Sti))return 0;
        for(unsigned 순번=0;순번<vare_ANTALL;순번++)Sti[순번]=oppføring_metode[순번]=='.'?'/':oppføring_metode[순번];strcpy(Sti+vare_ANTALL,".class");int oppføring_ANTALL=꾸러미읽기(Sti,data,sizeof(data));if(oppføring_ANTALL<0)return 0;lengde_VERDI=oppføring_ANTALL;
    }else{intptr_t Fil_håndtak=사용자호출(3,(uintptr_t)Navn,0,0,0,0,0);if(Fil_håndtak<0)return 0;intptr_t oppføring_ANTALL=사용자호출(9,Fil_håndtak,0,0,0,0,0);if(oppføring_ANTALL<0||oppføring_ANTALL>sizeof(data)){사용자호출(4,Fil_håndtak,0,0,0,0,0);return 0;}intptr_t MOTTATT_AVKAST_ANTALL=사용자호출(2,Fil_håndtak,(uintptr_t)data,oppføring_ANTALL,0,0,0);사용자호출(4,Fil_håndtak,0,0,0,0,0);if(MOTTATT_AVKAST_ANTALL!=oppføring_ANTALL)return 0;lengde_VERDI=oppføring_ANTALL;}
    if(dele_opp_inndata()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstant_pulje&&!informasjonssystemer_ugyldig;순번++)if(Merker_Liste[순번]==8)streng_konstant(순번);
    if(informasjonssystemer_ugyldig)return 0;
    int inngangspunkt=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VERDI(메소드목록[순번].Navn,"<init>")){
        int KR,oppføring_ANTALL=서술자(메소드목록[순번].서술값,&KR);if(oppføring_ANTALL<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<oppføring_ANTALL;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!oppføring_ANTALL)내보내기("void");내보내기(");\n");
        if(UNICODE_VERDI(메소드목록[순번].Navn,"main")&&UNICODE_VERDI(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigurasjon_BITS&9)==9)inngangspunkt=순번;
        if(UNICODE_VERDI(메소드목록[순번].Navn,"<clinit>"))초기값=순번;
    }
    if(inngangspunkt<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informasjonssystemer_ugyldig;순번++)kompilere_metode(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(felt_konstant[순번]){
        unsigned tegnkode=felt_konstant[순번];if(tegnkode>=konstant_pulje)return 0;
        if(Merker_Liste[tegnkode]==3)내보내기("fields[%u]=%uU;",순번,첫째값[tegnkode]);else if(Merker_Liste[tegnkode]==8)내보내기("fields[%u]=(W)k%u;",순번,tegnkode);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",inngangspunkt);
    return informasjonssystemer_ugyldig?0:Tekst;
}
