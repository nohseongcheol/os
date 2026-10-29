#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "bundel.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char gegevens[16384];static unsigned tijdsduur_WAARDE,actueel_functie;static int informatie_nietig;
static unsigned Labels_Lijst[512],첫째값[512],SECONDE_WAARDE[512],constante_pool,actueel_les;
static char tekst[65536];static unsigned Tekengrootte;
typedef struct {unsigned configuratie_BITS,Naam,서술값,instructie_REEKS,Grootte,지역변수들,stapelgeheugen;} methode_invoer;
static methode_invoer 메소드목록[64];static unsigned 메소드개수;
static unsigned veldnaam[64],필드서술[64],veld_constante[64],필드개수;
static unsigned NEMEN_WAARDE(unsigned item_AANTAL){if(actueel_functie>tijdsduur_WAARDE||item_AANTAL>tijdsduur_WAARDE-actueel_functie){informatie_nietig=1;return 0;}unsigned gegevens_functie=actueel_functie;actueel_functie+=item_AANTAL;return gegevens_functie;}
static unsigned byte_gegevens(void){unsigned gegevens_functie=NEMEN_WAARDE(1);return informatie_nietig?0:gegevens[gegevens_functie];}
static unsigned 절반값(void){unsigned x_coördinaat=byte_gegevens();return x_coördinaat<<8|byte_gegevens();}
static uint32_t 가득참(void){uint32_t x_coördinaat=절반값();return x_coördinaat<<16|절반값();}
static int UNICODE_WAARDE(unsigned 순번,const char*tekenreeks_gegevens){return 순번>0&&순번<constante_pool&&Labels_Lijst[순번]==1&&strlen(tekenreeks_gegevens)==SECONDE_WAARDE[순번]&&!memcmp(gegevens+첫째값[순번],tekenreeks_gegevens,SECONDE_WAARDE[순번]);}
static int 같음(unsigned x_coördinaat,unsigned Y_coördinaat){return x_coördinaat>0&&x_coördinaat<constante_pool&&Y_coördinaat>0&&Y_coördinaat<constante_pool&&Labels_Lijst[x_coördinaat]==1&&Labels_Lijst[Y_coördinaat]==1&&SECONDE_WAARDE[x_coördinaat]==SECONDE_WAARDE[Y_coördinaat]&&!memcmp(gegevens+첫째값[x_coördinaat],gegevens+첫째값[Y_coördinaat],SECONDE_WAARDE[x_coördinaat]);}
static void 내보내기(const char*Bestand_invoer,...){if(informatie_nietig)return;va_list argument_MATRIX;va_start(argument_MATRIX,Bestand_invoer);int item_AANTAL=vsnprintf(tekst+Tekengrootte,sizeof(tekst)-Tekengrootte,Bestand_invoer,argument_MATRIX);va_end(argument_MATRIX);if(item_AANTAL<0||(unsigned)item_AANTAL>=sizeof(tekst)-Tekengrootte){informatie_nietig=1;return;}Tekengrootte+=item_AANTAL;}
static int 서술자(unsigned id_WAARDE,int*resultaat){
    if(id_WAARDE<1||id_WAARDE>=constante_pool||Labels_Lijst[id_WAARDE]!=1)return -1;unsigned gegevens_functie=첫째값[id_WAARDE],beëindigen_VERSCHUIVING=gegevens_functie+SECONDE_WAARDE[id_WAARDE];if(gegevens_functie>=beëindigen_VERSCHUIVING||gegevens[gegevens_functie++]!='(')return -1;int invoer_AANTAL_8f7753a1=0;
    while(gegevens_functie<beëindigen_VERSCHUIVING&&gegevens[gegevens_functie]!=')'){
        unsigned codepoint=gegevens[gegevens_functie++];while(codepoint=='['&&gegevens_functie<beëindigen_VERSCHUIVING)codepoint=gegevens[gegevens_functie++];
        if(codepoint=='L'){while(gegevens_functie<beëindigen_VERSCHUIVING&&gegevens[gegevens_functie]!=';')gegevens_functie++;if(gegevens_functie==beëindigen_VERSCHUIVING)return -1;gegevens_functie++;}
        else if(codepoint!='I'&&codepoint!='Z'&&codepoint!='B'&&codepoint!='C'&&codepoint!='S')return -1;
        if(++invoer_AANTAL_8f7753a1>16)return -1;
    }
    if(gegevens_functie+1>=beëindigen_VERSCHUIVING||gegevens[gegevens_functie++]!=')')return -1;*resultaat=gegevens[gegevens_functie]=='V'?0:1;
    if(gegevens[gegevens_functie]=='J'||gegevens[gegevens_functie]=='D'||gegevens[gegevens_functie]=='F')return -1;return invoer_AANTAL_8f7753a1;
}
static void attributen(void){unsigned item_AANTAL=절반값();for(unsigned 순번=0;순번<item_AANTAL&&!informatie_nietig;순번++){절반값();unsigned Grootte=가득참();NEMEN_WAARDE(Grootte);}}
static int parseren_invoer(void){
    if(가득참()!=0xcafebabe)return -1;unsigned secundaire_versie=절반값(),versienummer=절반값();if(secundaire_versie||versienummer<45||versienummer>52)return -1;
    constante_pool=절반값();if(constante_pool<1||constante_pool>512)return -1;
    for(unsigned 순번=1;순번<constante_pool&&!informatie_nietig;순번++){
        Labels_Lijst[순번]=byte_gegevens();switch(Labels_Lijst[순번]){
        case 1:SECONDE_WAARDE[순번]=절반값();첫째값[순번]=NEMEN_WAARDE(SECONDE_WAARDE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:NEMEN_WAARDE(8);if(++순번>=constante_pool)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECONDE_WAARDE[순번]=절반값();break;
        case 15:첫째값[순번]=byte_gegevens();SECONDE_WAARDE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();actueel_les=절반값();절반값();if(actueel_les<1||actueel_les>=constante_pool||Labels_Lijst[actueel_les]!=7||첫째값[actueel_les]<1||첫째값[actueel_les]>=constante_pool||Labels_Lijst[첫째값[actueel_les]]!=1)return -1;unsigned 인터페이스목록=절반값();NEMEN_WAARDE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!informatie_nietig;순번++){
        unsigned configuratie_BITS=절반값();veldnaam[순번]=절반값();필드서술[순번]=절반값();
        if(!(configuratie_BITS&8))return -1;
        unsigned invoer_AANTAL_8f7753a1=절반값();for(unsigned 안쪽순번=0;안쪽순번<invoer_AANTAL_8f7753a1&&!informatie_nietig;안쪽순번++){
            unsigned Naam=절반값(),Grootte=가득참();
            if(UNICODE_WAARDE(Naam,"ConstantValue")){if(Grootte!=2)return -1;veld_constante[순번]=절반값();}
            else NEMEN_WAARDE(Grootte);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!informatie_nietig;순번++){
        methode_invoer*Groep_formaat_wijzigen=메소드목록+순번;Groep_formaat_wijzigen->configuratie_BITS=절반값();Groep_formaat_wijzigen->Naam=절반값();Groep_formaat_wijzigen->서술값=절반값();unsigned invoer_AANTAL_8f7753a1=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<invoer_AANTAL_8f7753a1&&!informatie_nietig;안쪽순번++){
            unsigned Naam=절반값(),Grootte=가득참(),starten=actueel_functie;
            if(Grootte>tijdsduur_WAARDE-actueel_functie)return -1;
            if(UNICODE_WAARDE(Naam,"Code")){
                Groep_formaat_wijzigen->stapelgeheugen=절반값();Groep_formaat_wijzigen->지역변수들=절반값();Groep_formaat_wijzigen->Grootte=가득참();Groep_formaat_wijzigen->instructie_REEKS=NEMEN_WAARDE(Groep_formaat_wijzigen->Grootte);
                if(Groep_formaat_wijzigen->stapelgeheugen>128||Groep_formaat_wijzigen->지역변수들>128||Groep_formaat_wijzigen->Grootte>8192||절반값())return -1;attributen();
            }else NEMEN_WAARDE(Grootte);
            if(actueel_functie!=starten+Grootte)return -1;
        }
        if(!UNICODE_WAARDE(Groep_formaat_wijzigen->Naam,"<init>")&&(!(Groep_formaat_wijzigen->configuratie_BITS&8)||(Groep_formaat_wijzigen->configuratie_BITS&(0x100|0x20))||!Groep_formaat_wijzigen->Grootte))return -1;
    }
    attributen();return informatie_nietig||actueel_functie!=tijdsduur_WAARDE?-1:0;
}
static void constante_WAARDE(unsigned id_WAARDE){
    if(!id_WAARDE||id_WAARDE>=constante_pool){informatie_nietig=1;return;}
    if(Labels_Lijst[id_WAARDE]==3)내보내기("P(%uU);",첫째값[id_WAARDE]);
    else if(Labels_Lijst[id_WAARDE]==8)내보내기("P((W)k%u);",id_WAARDE);else informatie_nietig=1;
}
static void 호출(unsigned id_WAARDE,int virtueel_Bellen){
    if(id_WAARDE<1||id_WAARDE>=constante_pool||(Labels_Lijst[id_WAARDE]!=10&&Labels_Lijst[id_WAARDE]!=11)||첫째값[id_WAARDE]<1||첫째값[id_WAARDE]>=constante_pool||Labels_Lijst[첫째값[id_WAARDE]]!=7||SECONDE_WAARDE[id_WAARDE]<1||SECONDE_WAARDE[id_WAARDE]>=constante_pool||Labels_Lijst[SECONDE_WAARDE[id_WAARDE]]!=12){informatie_nietig=1;return;}
    unsigned eigenaar_object=첫째값[첫째값[id_WAARDE]],Naam=첫째값[SECONDE_WAARDE[id_WAARDE]],서술값=SECONDE_WAARDE[SECONDE_WAARDE[id_WAARDE]];int resultaat=0,item_AANTAL=서술자(서술값,&resultaat);if(item_AANTAL<0){informatie_nietig=1;return;}
    for(int 순번=item_AANTAL;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtueel_Bellen)내보내기("Q();");
    if(!virtueel_Bellen&&같음(eigenaar_object,첫째값[actueel_les])){
        unsigned Groep_formaat_wijzigen=0;for(;Groep_formaat_wijzigen<메소드개수;Groep_formaat_wijzigen++)if(같음(Naam,메소드목록[Groep_formaat_wijzigen].Naam)&&같음(서술값,메소드목록[Groep_formaat_wijzigen].서술값))break;
        if(Groep_formaat_wijzigen==메소드개수||!(메소드목록[Groep_formaat_wijzigen].configuratie_BITS&8)){informatie_nietig=1;return;}
        if(resultaat)내보내기("P(");내보내기("m%u(",Groep_formaat_wijzigen);for(int 순번=0;순번<item_AANTAL;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(resultaat?"));":" );");return;
    }
    if((virtueel_Bellen&&UNICODE_WAARDE(eigenaar_object,"java/io/PrintStream")&& (UNICODE_WAARDE(Naam,"print")||UNICODE_WAARDE(Naam,"println")))||(!virtueel_Bellen&&UNICODE_WAARDE(eigenaar_object,"Nederlands/Eigen/tekstuitvoer"))){
        if(UNICODE_WAARDE(서술값,"(I)V")&&(UNICODE_WAARDE(Naam,"print")||UNICODE_WAARDE(Naam,"println")||UNICODE_WAARDE(Naam,"schrijven_nummer"))){내보내기("jprint(x[0],1,%d);",UNICODE_WAARDE(Naam,"print")?0:1);return;}
        if(UNICODE_WAARDE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_WAARDE(Naam,"print")||UNICODE_WAARDE(Naam,"println")||UNICODE_WAARDE(Naam,"Schrijven")||UNICODE_WAARDE(Naam,"schrijven_lijn"))){내보내기("jprint(x[0],0,%d);",UNICODE_WAARDE(Naam,"print")||UNICODE_WAARDE(Naam,"Schrijven")?0:1);return;}
        if(UNICODE_WAARDE(서술값,"()V")&&UNICODE_WAARDE(Naam,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtueel_Bellen&&UNICODE_WAARDE(eigenaar_object,"Nederlands/Eigen/bestand")){
        if(UNICODE_WAARDE(Naam,"Schrijven")&&UNICODE_WAARDE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_WAARDE(Naam,"Lezen")&&UNICODE_WAARDE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    informatie_nietig=1;
}
static void compileren_methode(unsigned ZOEKEN_INDEX){
    methode_invoer*Groep_formaat_wijzigen=메소드목록+ZOEKEN_INDEX;if(UNICODE_WAARDE(Groep_formaat_wijzigen->Naam,"<init>"))return;int resultaat,item_AANTAL=서술자(Groep_formaat_wijzigen->서술값,&resultaat);if(item_AANTAL<0){informatie_nietig=1;return;}
    내보내기("static W m%u(",ZOEKEN_INDEX);for(int 순번=0;순번<item_AANTAL;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!item_AANTAL)내보내기("void");
    if((unsigned)item_AANTAL>Groep_formaat_wijzigen->지역변수들){informatie_nietig=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Groep_formaat_wijzigen->지역변수들?Groep_formaat_wijzigen->지역변수들:1);for(int 순번=0;순번<item_AANTAL;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=tijdsduur_WAARDE;tijdsduur_WAARDE=Groep_formaat_wijzigen->instructie_REEKS+Groep_formaat_wijzigen->Grootte;actueel_functie=Groep_formaat_wijzigen->instructie_REEKS;
    while(actueel_functie<tijdsduur_WAARDE&&!informatie_nietig){unsigned opdracht_functie=actueel_functie-Groep_formaat_wijzigen->instructie_REEKS,operatie_WAARDE=byte_gegevens();내보내기("L%u:;",opdracht_functie);
        if(operatie_WAARDE==0){}
        else if(operatie_WAARDE==1)내보내기("P(0);");
        else if(operatie_WAARDE>=2&&operatie_WAARDE<=8)내보내기("P(%uU);",operatie_WAARDE-3);
        else if(operatie_WAARDE==16){int WAARDE=(int8_t)byte_gegevens();내보내기("P(%uU);",(unsigned)WAARDE);}
        else if(operatie_WAARDE==17){int WAARDE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)WAARDE);}
        else if(operatie_WAARDE==18||operatie_WAARDE==19)constante_WAARDE(operatie_WAARDE==18?byte_gegevens():절반값());
        else if(operatie_WAARDE==21||operatie_WAARDE==25){unsigned 순번=byte_gegevens();if(순번>=Groep_formaat_wijzigen->지역변수들)informatie_nietig=1;내보내기("P(v[%u]);",순번);}
        else if((operatie_WAARDE>=26&&operatie_WAARDE<=29)||(operatie_WAARDE>=42&&operatie_WAARDE<=45)){unsigned 순번=operatie_WAARDE>=42?operatie_WAARDE-42:operatie_WAARDE-26;if(순번>=Groep_formaat_wijzigen->지역변수들)informatie_nietig=1;내보내기("P(v[%u]);",순번);}
        else if(operatie_WAARDE==54||operatie_WAARDE==58){unsigned 순번=byte_gegevens();if(순번>=Groep_formaat_wijzigen->지역변수들)informatie_nietig=1;내보내기("v[%u]=Q();",순번);}
        else if((operatie_WAARDE>=59&&operatie_WAARDE<=62)||(operatie_WAARDE>=75&&operatie_WAARDE<=78)){unsigned 순번=operatie_WAARDE>=75?operatie_WAARDE-75:operatie_WAARDE-59;if(순번>=Groep_formaat_wijzigen->지역변수들)informatie_nietig=1;내보내기("v[%u]=Q();",순번);}
        else if(operatie_WAARDE==46||operatie_WAARDE==50||operatie_WAARDE==51||operatie_WAARDE==52||operatie_WAARDE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operatie_WAARDE==79||operatie_WAARDE==83||operatie_WAARDE==84||operatie_WAARDE==85||operatie_WAARDE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operatie_WAARDE==84?"(unsigned)(signed char)q":operatie_WAARDE==85?"(unsigned short)q":operatie_WAARDE==86?"(unsigned)(short)q":"q");
        else if(operatie_WAARDE==87)내보내기("Q();");
        else if(operatie_WAARDE==89)내보내기("q=Q();P(q);P(q);");
        else if(operatie_WAARDE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operatie_WAARDE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operatie_WAARDE==96||operatie_WAARDE==100||operatie_WAARDE==104||operatie_WAARDE==120||operatie_WAARDE==124||operatie_WAARDE==126||operatie_WAARDE==128||operatie_WAARDE==130){const char*Encoding_WAARDE=operatie_WAARDE==96?"+":operatie_WAARDE==100?"-":operatie_WAARDE==104?"*":operatie_WAARDE==120?"<<":operatie_WAARDE==124?">>":operatie_WAARDE==126?"&":operatie_WAARDE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",Encoding_WAARDE,operatie_WAARDE==120||operatie_WAARDE==124?"%32":"");}
        else if(operatie_WAARDE==108||operatie_WAARDE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operatie_WAARDE==112);
        else if(operatie_WAARDE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operatie_WAARDE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operatie_WAARDE==132){unsigned 순번=byte_gegevens();int 차이=(int8_t)byte_gegevens();if(순번>=Groep_formaat_wijzigen->지역변수들)informatie_nietig=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operatie_WAARDE>=145&&operatie_WAARDE<=147)내보내기("P((unsigned)(%s)Q());",operatie_WAARDE==145?"signed char":operatie_WAARDE==146?"unsigned short":"short");
        else if(operatie_WAARDE>=153&&operatie_WAARDE<=166){int doel=(int)opdracht_functie+(int16_t)절반값();const char*Vergelijking_WAARDE[]={"==","!=","<",">=",">","<="};if(doel<0||doel>=(int)Groep_formaat_wijzigen->Grootte){informatie_nietig=1;break;}if(operatie_WAARDE<159)내보내기("if((int)Q()%s0)goto L%d;",Vergelijking_WAARDE[operatie_WAARDE-153],doel);else if(operatie_WAARDE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Vergelijking_WAARDE[operatie_WAARDE-159],doel);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operatie_WAARDE==165?"==":"!=",doel);}
        else if(operatie_WAARDE==167){int doel=(int)opdracht_functie+(int16_t)절반값();if(doel<0||doel>=(int)Groep_formaat_wijzigen->Grootte)informatie_nietig=1;내보내기("goto L%d;",doel);}
        else if(operatie_WAARDE==172||operatie_WAARDE==176)내보내기("return Q();");else if(operatie_WAARDE==177)내보내기("return 0;");
        else if(operatie_WAARDE==178||operatie_WAARDE==179){unsigned id_WAARDE=절반값();if(id_WAARDE<1||id_WAARDE>=constante_pool||Labels_Lijst[id_WAARDE]!=9||첫째값[id_WAARDE]>=constante_pool||SECONDE_WAARDE[id_WAARDE]>=constante_pool||Labels_Lijst[첫째값[id_WAARDE]]!=7||Labels_Lijst[SECONDE_WAARDE[id_WAARDE]]!=12){informatie_nietig=1;break;}unsigned eigenaar_object=첫째값[첫째값[id_WAARDE]],Naam=첫째값[SECONDE_WAARDE[id_WAARDE]],서술값=SECONDE_WAARDE[SECONDE_WAARDE[id_WAARDE]];
            if(operatie_WAARDE==178&&UNICODE_WAARDE(eigenaar_object,"java/lang/System")&&UNICODE_WAARDE(Naam,"out")&&UNICODE_WAARDE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Bestand_invoer=0;while(Bestand_invoer<필드개수&&(!같음(Naam,veldnaam[Bestand_invoer])||!같음(서술값,필드서술[Bestand_invoer])))Bestand_invoer++;if(!같음(eigenaar_object,첫째값[actueel_les])||Bestand_invoer==필드개수){informatie_nietig=1;break;}내보내기(operatie_WAARDE==178?"P(fields[%u]);":"fields[%u]=Q();",Bestand_invoer);}}
        else if(operatie_WAARDE==182||operatie_WAARDE==184)호출(절반값(),operatie_WAARDE==182);
        else if(operatie_WAARDE==188){unsigned TYPE_gebied=byte_gegevens();if(TYPE_gebied!=4&&TYPE_gebied!=5&&TYPE_gebied!=8&&TYPE_gebied!=9&&TYPE_gebied!=10)informatie_nietig=1;내보내기("P(jarray((int)Q()));");}
        else if(operatie_WAARDE==190)내보내기("P(jlength(Q()));");
        else if(operatie_WAARDE==198||operatie_WAARDE==199){int doel=(int)opdracht_functie+(int16_t)절반값();if(doel<0||doel>=(int)Groep_formaat_wijzigen->Grootte)informatie_nietig=1;내보내기("if(Q()%s0)goto L%d;",operatie_WAARDE==198?"==":"!=",doel);}
        else informatie_nietig=1;
        if(informatie_nietig)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",ZOEKEN_INDEX,operatie_WAARDE,opdracht_functie);
        내보내기("\n");
    }
    tijdsduur_WAARDE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned tekenreeks_les(unsigned *gegevens_functie,unsigned beëindigen_VERSCHUIVING){
    if(*gegevens_functie>=beëindigen_VERSCHUIVING){informatie_nietig=1;return 0;}unsigned codepoint=gegevens[(*gegevens_functie)++];
    if(codepoint<128)return codepoint;
    unsigned item_AANTAL=codepoint>=0xc0&&codepoint<=0xdf?1:codepoint>=0xe0&&codepoint<=0xef?2:3;
    if(item_AANTAL==3||item_AANTAL>beëindigen_VERSCHUIVING-*gegevens_functie){informatie_nietig=1;return 0;}unsigned WAARDE=codepoint&((1u<<(6-item_AANTAL))-1);
    for(unsigned 순번=0;순번<item_AANTAL;순번++){unsigned Volgende_item=gegevens[(*gegevens_functie)++];if((Volgende_item&0xc0)!=0x80)informatie_nietig=1;WAARDE=WAARDE<<6|(Volgende_item&63);}
    if((item_AANTAL==1&&WAARDE<128&&WAARDE!=0)||(item_AANTAL==2&&WAARDE<2048))informatie_nietig=1;return WAARDE;
}
static void tekenreeks_constante(unsigned id_WAARDE){
    unsigned 부호없는값=첫째값[id_WAARDE];if(부호없는값<1||부호없는값>=constante_pool||Labels_Lijst[부호없는값]!=1){informatie_nietig=1;return;}내보내기("static const unsigned char k%u[]={",id_WAARDE);
    unsigned gegevens_functie=첫째값[부호없는값],beëindigen_VERSCHUIVING=gegevens_functie+SECONDE_WAARDE[부호없는값];
    while(gegevens_functie<beëindigen_VERSCHUIVING&&!informatie_nietig){unsigned codepoint=tekenreeks_les(&gegevens_functie,beëindigen_VERSCHUIVING);
        if(codepoint>=0xd800&&codepoint<=0xdbff){unsigned 낮은부분=tekenreeks_les(&gegevens_functie,beëindigen_VERSCHUIVING);if(낮은부분<0xdc00||낮은부분>0xdfff){informatie_nietig=1;break;}codepoint=0x10000+((codepoint-0xd800)<<10)+낮은부분-0xdc00;}
        else if(codepoint>=0xdc00&&codepoint<=0xdfff){informatie_nietig=1;break;}
        if(!codepoint){printf("jaot: embedded NUL string needs JVM mode\n");informatie_nietig=1;break;}
        if(codepoint<128)내보내기("%u,",codepoint);
        else{unsigned item_AANTAL=codepoint<2048?2:codepoint<65536?3:4;내보내기("%u,",(item_AANTAL==2?0xc0:item_AANTAL==3?0xe0:0xf0)|(codepoint>>(6*(item_AANTAL-1))));for(unsigned 순번=item_AANTAL-1;순번;순번--)내보내기("%u,",0x80|((codepoint>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Naam){
    size_t item_AANTAL=strlen(Naam);
    if(item_AANTAL>4&&!strcmp(Naam+item_AANTAL-4,".jar")){
        if(꾸러미열기(Naam)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char pad[256];const char*invoer_methode=꾸러미진입클래스();item_AANTAL=strlen(invoer_methode);if(item_AANTAL+6>=sizeof(pad))return 0;
        for(unsigned 순번=0;순번<item_AANTAL;순번++)pad[순번]=invoer_methode[순번]=='.'?'/':invoer_methode[순번];strcpy(pad+item_AANTAL,".class");int invoer_AANTAL_8f7753a1=꾸러미읽기(pad,gegevens,sizeof(gegevens));if(invoer_AANTAL_8f7753a1<0)return 0;tijdsduur_WAARDE=invoer_AANTAL_8f7753a1;
    }else{intptr_t bestandsingang=사용자호출(3,(uintptr_t)Naam,0,0,0,0,0);if(bestandsingang<0)return 0;intptr_t invoer_AANTAL_8f7753a1=사용자호출(9,bestandsingang,0,0,0,0,0);if(invoer_AANTAL_8f7753a1<0||invoer_AANTAL_8f7753a1>sizeof(gegevens)){사용자호출(4,bestandsingang,0,0,0,0,0);return 0;}intptr_t OPBRENGST_AANTAL=사용자호출(2,bestandsingang,(uintptr_t)gegevens,invoer_AANTAL_8f7753a1,0,0,0);사용자호출(4,bestandsingang,0,0,0,0,0);if(OPBRENGST_AANTAL!=invoer_AANTAL_8f7753a1)return 0;tijdsduur_WAARDE=invoer_AANTAL_8f7753a1;}
    if(parseren_invoer()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<constante_pool&&!informatie_nietig;순번++)if(Labels_Lijst[순번]==8)tekenreeks_constante(순번);
    if(informatie_nietig)return 0;
    int beginpunt=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_WAARDE(메소드목록[순번].Naam,"<init>")){
        int resultaat,invoer_AANTAL_8f7753a1=서술자(메소드목록[순번].서술값,&resultaat);if(invoer_AANTAL_8f7753a1<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<invoer_AANTAL_8f7753a1;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!invoer_AANTAL_8f7753a1)내보내기("void");내보내기(");\n");
        if(UNICODE_WAARDE(메소드목록[순번].Naam,"main")&&UNICODE_WAARDE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].configuratie_BITS&9)==9)beginpunt=순번;
        if(UNICODE_WAARDE(메소드목록[순번].Naam,"<clinit>"))초기값=순번;
    }
    if(beginpunt<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!informatie_nietig;순번++)compileren_methode(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(veld_constante[순번]){
        unsigned codepoint=veld_constante[순번];if(codepoint>=constante_pool)return 0;
        if(Labels_Lijst[codepoint]==3)내보내기("fields[%u]=%uU;",순번,첫째값[codepoint]);else if(Labels_Lijst[codepoint]==8)내보내기("fields[%u]=(W)k%u;",순번,codepoint);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",beginpunt);
    return informatie_nietig?0:tekst;
}
