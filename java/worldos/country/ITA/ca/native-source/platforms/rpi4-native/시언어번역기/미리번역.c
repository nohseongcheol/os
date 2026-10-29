#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "paquet.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char dades[16384];static unsigned durada_VALOR,현재위치;static int tecnologies_de_la_informació_invàlid;
static unsigned Etiquetes_Llista[512],첫째값[512],SEGON_VALOR[512],상수모음,현재클래스;
static char SMS[65536];static unsigned Mida_del_text;
typedef struct {unsigned configuració_Servei_de_transferència_intel_ligent_en_segon_terme,Nom,서술값,instrucció_SEQÜÈNCIA,Mida,지역변수들,Pila_Emmagatzematge;} 메소드;
static 메소드 메소드목록[64];static unsigned 메소드개수;
static unsigned camp_nom[64],필드서술[64],필드상수[64],필드개수;
static unsigned PREN_VALOR(unsigned element_COMPT){if(현재위치>durada_VALOR||element_COMPT>durada_VALOR-현재위치){tecnologies_de_la_informació_invàlid=1;return 0;}unsigned dades_càrrec=현재위치;현재위치+=element_COMPT;return dades_càrrec;}
static unsigned byte_dades(void){unsigned dades_càrrec=PREN_VALOR(1);return tecnologies_de_la_informació_invàlid?0:dades[dades_càrrec];}
static unsigned 절반값(void){unsigned X_coordenada=byte_dades();return X_coordenada<<8|byte_dades();}
static uint32_t 가득참(void){uint32_t X_coordenada=절반값();return X_coordenada<<16|절반값();}
static int UNICODE_VALOR(unsigned 순번,const char*cadena_dades){return 순번>0&&순번<상수모음&&Etiquetes_Llista[순번]==1&&strlen(cadena_dades)==SEGON_VALOR[순번]&&!memcmp(dades+첫째값[순번],cadena_dades,SEGON_VALOR[순번]);}
static int 같음(unsigned X_coordenada,unsigned Y_coordenada){return X_coordenada>0&&X_coordenada<상수모음&&Y_coordenada>0&&Y_coordenada<상수모음&&Etiquetes_Llista[X_coordenada]==1&&Etiquetes_Llista[Y_coordenada]==1&&SEGON_VALOR[X_coordenada]==SEGON_VALOR[Y_coordenada]&&!memcmp(dades+첫째값[X_coordenada],dades+첫째값[Y_coordenada],SEGON_VALOR[X_coordenada]);}
static void 내보내기(const char*arxiu_introducció,...){if(tecnologies_de_la_informació_invàlid)return;va_list arg_MATRIU;va_start(arg_MATRIU,arxiu_introducció);int element_COMPT=vsnprintf(SMS+Mida_del_text,sizeof(SMS)-Mida_del_text,arxiu_introducció,arg_MATRIU);va_end(arg_MATRIU);if(element_COMPT<0||(unsigned)element_COMPT>=sizeof(SMS)-Mida_del_text){tecnologies_de_la_informació_invàlid=1;return;}Mida_del_text+=element_COMPT;}
static int 서술자(unsigned identificador_VALOR,int*RESULTAT){
    if(identificador_VALOR<1||identificador_VALOR>=상수모음||Etiquetes_Llista[identificador_VALOR]!=1)return -1;unsigned dades_càrrec=첫째값[identificador_VALOR],finalitzar_DESPLAÇAMENT=dades_càrrec+SEGON_VALOR[identificador_VALOR];if(dades_càrrec>=finalitzar_DESPLAÇAMENT||dades[dades_càrrec++]!='(')return -1;int introducció_COMPT=0;
    while(dades_càrrec<finalitzar_DESPLAÇAMENT&&dades[dades_càrrec]!=')'){
        unsigned codi_de_caràcter=dades[dades_càrrec++];while(codi_de_caràcter=='['&&dades_càrrec<finalitzar_DESPLAÇAMENT)codi_de_caràcter=dades[dades_càrrec++];
        if(codi_de_caràcter=='L'){while(dades_càrrec<finalitzar_DESPLAÇAMENT&&dades[dades_càrrec]!=';')dades_càrrec++;if(dades_càrrec==finalitzar_DESPLAÇAMENT)return -1;dades_càrrec++;}
        else if(codi_de_caràcter!='I'&&codi_de_caràcter!='Z'&&codi_de_caràcter!='B'&&codi_de_caràcter!='C'&&codi_de_caràcter!='S')return -1;
        if(++introducció_COMPT>16)return -1;
    }
    if(dades_càrrec+1>=finalitzar_DESPLAÇAMENT||dades[dades_càrrec++]!=')')return -1;*RESULTAT=dades[dades_càrrec]=='V'?0:1;
    if(dades[dades_càrrec]=='J'||dades[dades_càrrec]=='D'||dades[dades_càrrec]=='F')return -1;return introducció_COMPT;
}
static void atributs(void){unsigned element_COMPT=절반값();for(unsigned 순번=0;순번<element_COMPT&&!tecnologies_de_la_informació_invàlid;순번++){절반값();unsigned Mida=가득참();PREN_VALOR(Mida);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned menor_d_edat_versió=절반값(),판번호=절반값();if(menor_d_edat_versió||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!tecnologies_de_la_informació_invàlid;순번++){
        Etiquetes_Llista[순번]=byte_dades();switch(Etiquetes_Llista[순번]){
        case 1:SEGON_VALOR[순번]=절반값();첫째값[순번]=PREN_VALOR(SEGON_VALOR[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:PREN_VALOR(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEGON_VALOR[순번]=절반값();break;
        case 15:첫째값[순번]=byte_dades();SEGON_VALOR[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Etiquetes_Llista[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Etiquetes_Llista[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();PREN_VALOR(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!tecnologies_de_la_informació_invàlid;순번++){
        unsigned configuració_Servei_de_transferència_intel_ligent_en_segon_terme=절반값();camp_nom[순번]=절반값();필드서술[순번]=절반값();
        if(!(configuració_Servei_de_transferència_intel_ligent_en_segon_terme&8))return -1;
        unsigned introducció_COMPT=절반값();for(unsigned 안쪽순번=0;안쪽순번<introducció_COMPT&&!tecnologies_de_la_informació_invàlid;안쪽순번++){
            unsigned Nom=절반값(),Mida=가득참();
            if(UNICODE_VALOR(Nom,"ConstantValue")){if(Mida!=2)return -1;필드상수[순번]=절반값();}
            else PREN_VALOR(Mida);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!tecnologies_de_la_informació_invàlid;순번++){
        메소드*Grup_canviar_la_mida=메소드목록+순번;Grup_canviar_la_mida->configuració_Servei_de_transferència_intel_ligent_en_segon_terme=절반값();Grup_canviar_la_mida->Nom=절반값();Grup_canviar_la_mida->서술값=절반값();unsigned introducció_COMPT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<introducció_COMPT&&!tecnologies_de_la_informació_invàlid;안쪽순번++){
            unsigned Nom=절반값(),Mida=가득참(),Executa_2=현재위치;
            if(Mida>durada_VALOR-현재위치)return -1;
            if(UNICODE_VALOR(Nom,"Code")){
                Grup_canviar_la_mida->Pila_Emmagatzematge=절반값();Grup_canviar_la_mida->지역변수들=절반값();Grup_canviar_la_mida->Mida=가득참();Grup_canviar_la_mida->instrucció_SEQÜÈNCIA=PREN_VALOR(Grup_canviar_la_mida->Mida);
                if(Grup_canviar_la_mida->Pila_Emmagatzematge>128||Grup_canviar_la_mida->지역변수들>128||Grup_canviar_la_mida->Mida>8192||절반값())return -1;atributs();
            }else PREN_VALOR(Mida);
            if(현재위치!=Executa_2+Mida)return -1;
        }
        if(!UNICODE_VALOR(Grup_canviar_la_mida->Nom,"<init>")&&(!(Grup_canviar_la_mida->configuració_Servei_de_transferència_intel_ligent_en_segon_terme&8)||(Grup_canviar_la_mida->configuració_Servei_de_transferència_intel_ligent_en_segon_terme&(0x100|0x20))||!Grup_canviar_la_mida->Mida))return -1;
    }
    atributs();return tecnologies_de_la_informació_invàlid||현재위치!=durada_VALOR?-1:0;
}
static void 상수(unsigned identificador_VALOR){
    if(!identificador_VALOR||identificador_VALOR>=상수모음){tecnologies_de_la_informació_invàlid=1;return;}
    if(Etiquetes_Llista[identificador_VALOR]==3)내보내기("P(%uU);",첫째값[identificador_VALOR]);
    else if(Etiquetes_Llista[identificador_VALOR]==8)내보내기("P((W)k%u);",identificador_VALOR);else tecnologies_de_la_informació_invàlid=1;
}
static void 호출(unsigned identificador_VALOR,int virtual_CRIDA){
    if(identificador_VALOR<1||identificador_VALOR>=상수모음||(Etiquetes_Llista[identificador_VALOR]!=10&&Etiquetes_Llista[identificador_VALOR]!=11)||첫째값[identificador_VALOR]<1||첫째값[identificador_VALOR]>=상수모음||Etiquetes_Llista[첫째값[identificador_VALOR]]!=7||SEGON_VALOR[identificador_VALOR]<1||SEGON_VALOR[identificador_VALOR]>=상수모음||Etiquetes_Llista[SEGON_VALOR[identificador_VALOR]]!=12){tecnologies_de_la_informació_invàlid=1;return;}
    unsigned propietari_objecte=첫째값[첫째값[identificador_VALOR]],Nom=첫째값[SEGON_VALOR[identificador_VALOR]],서술값=SEGON_VALOR[SEGON_VALOR[identificador_VALOR]];int RESULTAT=0,element_COMPT=서술자(서술값,&RESULTAT);if(element_COMPT<0){tecnologies_de_la_informació_invàlid=1;return;}
    for(int 순번=element_COMPT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtual_CRIDA)내보내기("Q();");
    if(!virtual_CRIDA&&같음(propietari_objecte,첫째값[현재클래스])){
        unsigned Grup_canviar_la_mida=0;for(;Grup_canviar_la_mida<메소드개수;Grup_canviar_la_mida++)if(같음(Nom,메소드목록[Grup_canviar_la_mida].Nom)&&같음(서술값,메소드목록[Grup_canviar_la_mida].서술값))break;
        if(Grup_canviar_la_mida==메소드개수||!(메소드목록[Grup_canviar_la_mida].configuració_Servei_de_transferència_intel_ligent_en_segon_terme&8)){tecnologies_de_la_informació_invàlid=1;return;}
        if(RESULTAT)내보내기("P(");내보내기("m%u(",Grup_canviar_la_mida);for(int 순번=0;순번<element_COMPT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(RESULTAT?"));":" );");return;
    }
    if((virtual_CRIDA&&UNICODE_VALOR(propietari_objecte,"java/io/PrintStream")&& (UNICODE_VALOR(Nom,"print")||UNICODE_VALOR(Nom,"println")))||(!virtual_CRIDA&&UNICODE_VALOR(propietari_objecte,"Català/propi/Sortida"))){
        if(UNICODE_VALOR(서술값,"(I)V")&&(UNICODE_VALOR(Nom,"print")||UNICODE_VALOR(Nom,"println")||UNICODE_VALOR(Nom,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALOR(Nom,"print")?0:1);return;}
        if(UNICODE_VALOR(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALOR(Nom,"print")||UNICODE_VALOR(Nom,"println")||UNICODE_VALOR(Nom,"Escriptura")||UNICODE_VALOR(Nom,"escriure_línia"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALOR(Nom,"print")||UNICODE_VALOR(Nom,"Escriptura")?0:1);return;}
        if(UNICODE_VALOR(서술값,"()V")&&UNICODE_VALOR(Nom,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtual_CRIDA&&UNICODE_VALOR(propietari_objecte,"Català/propi/Fitxer")){
        if(UNICODE_VALOR(Nom,"Escriptura")&&UNICODE_VALOR(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALOR(Nom,"Lectura")&&UNICODE_VALOR(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    tecnologies_de_la_informació_invàlid=1;
}
static void 메소드번역(unsigned Cerca_INDEX){
    메소드*Grup_canviar_la_mida=메소드목록+Cerca_INDEX;if(UNICODE_VALOR(Grup_canviar_la_mida->Nom,"<init>"))return;int RESULTAT,element_COMPT=서술자(Grup_canviar_la_mida->서술값,&RESULTAT);if(element_COMPT<0){tecnologies_de_la_informació_invàlid=1;return;}
    내보내기("static W m%u(",Cerca_INDEX);for(int 순번=0;순번<element_COMPT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!element_COMPT)내보내기("void");
    if((unsigned)element_COMPT>Grup_canviar_la_mida->지역변수들){tecnologies_de_la_informació_invàlid=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grup_canviar_la_mida->지역변수들?Grup_canviar_la_mida->지역변수들:1);for(int 순번=0;순번<element_COMPT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=durada_VALOR;durada_VALOR=Grup_canviar_la_mida->instrucció_SEQÜÈNCIA+Grup_canviar_la_mida->Mida;현재위치=Grup_canviar_la_mida->instrucció_SEQÜÈNCIA;
    while(현재위치<durada_VALOR&&!tecnologies_de_la_informació_invàlid){unsigned ordre_càrrec=현재위치-Grup_canviar_la_mida->instrucció_SEQÜÈNCIA,cirurgia_VALOR=byte_dades();내보내기("L%u:;",ordre_càrrec);
        if(cirurgia_VALOR==0){}
        else if(cirurgia_VALOR==1)내보내기("P(0);");
        else if(cirurgia_VALOR>=2&&cirurgia_VALOR<=8)내보내기("P(%uU);",cirurgia_VALOR-3);
        else if(cirurgia_VALOR==16){int VALOR=(int8_t)byte_dades();내보내기("P(%uU);",(unsigned)VALOR);}
        else if(cirurgia_VALOR==17){int VALOR=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALOR);}
        else if(cirurgia_VALOR==18||cirurgia_VALOR==19)상수(cirurgia_VALOR==18?byte_dades():절반값());
        else if(cirurgia_VALOR==21||cirurgia_VALOR==25){unsigned 순번=byte_dades();if(순번>=Grup_canviar_la_mida->지역변수들)tecnologies_de_la_informació_invàlid=1;내보내기("P(v[%u]);",순번);}
        else if((cirurgia_VALOR>=26&&cirurgia_VALOR<=29)||(cirurgia_VALOR>=42&&cirurgia_VALOR<=45)){unsigned 순번=cirurgia_VALOR>=42?cirurgia_VALOR-42:cirurgia_VALOR-26;if(순번>=Grup_canviar_la_mida->지역변수들)tecnologies_de_la_informació_invàlid=1;내보내기("P(v[%u]);",순번);}
        else if(cirurgia_VALOR==54||cirurgia_VALOR==58){unsigned 순번=byte_dades();if(순번>=Grup_canviar_la_mida->지역변수들)tecnologies_de_la_informació_invàlid=1;내보내기("v[%u]=Q();",순번);}
        else if((cirurgia_VALOR>=59&&cirurgia_VALOR<=62)||(cirurgia_VALOR>=75&&cirurgia_VALOR<=78)){unsigned 순번=cirurgia_VALOR>=75?cirurgia_VALOR-75:cirurgia_VALOR-59;if(순번>=Grup_canviar_la_mida->지역변수들)tecnologies_de_la_informació_invàlid=1;내보내기("v[%u]=Q();",순번);}
        else if(cirurgia_VALOR==46||cirurgia_VALOR==50||cirurgia_VALOR==51||cirurgia_VALOR==52||cirurgia_VALOR==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(cirurgia_VALOR==79||cirurgia_VALOR==83||cirurgia_VALOR==84||cirurgia_VALOR==85||cirurgia_VALOR==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",cirurgia_VALOR==84?"(unsigned)(signed char)q":cirurgia_VALOR==85?"(unsigned short)q":cirurgia_VALOR==86?"(unsigned)(short)q":"q");
        else if(cirurgia_VALOR==87)내보내기("Q();");
        else if(cirurgia_VALOR==89)내보내기("q=Q();P(q);P(q);");
        else if(cirurgia_VALOR==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(cirurgia_VALOR==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(cirurgia_VALOR==96||cirurgia_VALOR==100||cirurgia_VALOR==104||cirurgia_VALOR==120||cirurgia_VALOR==124||cirurgia_VALOR==126||cirurgia_VALOR==128||cirurgia_VALOR==130){const char*codificació_VALOR=cirurgia_VALOR==96?"+":cirurgia_VALOR==100?"-":cirurgia_VALOR==104?"*":cirurgia_VALOR==120?"<<":cirurgia_VALOR==124?">>":cirurgia_VALOR==126?"&":cirurgia_VALOR==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",codificació_VALOR,cirurgia_VALOR==120||cirurgia_VALOR==124?"%32":"");}
        else if(cirurgia_VALOR==108||cirurgia_VALOR==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",cirurgia_VALOR==112);
        else if(cirurgia_VALOR==116)내보내기("P(0U-(unsigned)Q());");
        else if(cirurgia_VALOR==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(cirurgia_VALOR==132){unsigned 순번=byte_dades();int 차이=(int8_t)byte_dades();if(순번>=Grup_canviar_la_mida->지역변수들)tecnologies_de_la_informació_invàlid=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(cirurgia_VALOR>=145&&cirurgia_VALOR<=147)내보내기("P((unsigned)(%s)Q());",cirurgia_VALOR==145?"signed char":cirurgia_VALOR==146?"unsigned short":"short");
        else if(cirurgia_VALOR>=153&&cirurgia_VALOR<=166){int objectiu=(int)ordre_càrrec+(int16_t)절반값();const char*Comparació_VALOR[]={"==","!=","<",">=",">","<="};if(objectiu<0||objectiu>=(int)Grup_canviar_la_mida->Mida){tecnologies_de_la_informació_invàlid=1;break;}if(cirurgia_VALOR<159)내보내기("if((int)Q()%s0)goto L%d;",Comparació_VALOR[cirurgia_VALOR-153],objectiu);else if(cirurgia_VALOR<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Comparació_VALOR[cirurgia_VALOR-159],objectiu);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",cirurgia_VALOR==165?"==":"!=",objectiu);}
        else if(cirurgia_VALOR==167){int objectiu=(int)ordre_càrrec+(int16_t)절반값();if(objectiu<0||objectiu>=(int)Grup_canviar_la_mida->Mida)tecnologies_de_la_informació_invàlid=1;내보내기("goto L%d;",objectiu);}
        else if(cirurgia_VALOR==172||cirurgia_VALOR==176)내보내기("return Q();");else if(cirurgia_VALOR==177)내보내기("return 0;");
        else if(cirurgia_VALOR==178||cirurgia_VALOR==179){unsigned identificador_VALOR=절반값();if(identificador_VALOR<1||identificador_VALOR>=상수모음||Etiquetes_Llista[identificador_VALOR]!=9||첫째값[identificador_VALOR]>=상수모음||SEGON_VALOR[identificador_VALOR]>=상수모음||Etiquetes_Llista[첫째값[identificador_VALOR]]!=7||Etiquetes_Llista[SEGON_VALOR[identificador_VALOR]]!=12){tecnologies_de_la_informació_invàlid=1;break;}unsigned propietari_objecte=첫째값[첫째값[identificador_VALOR]],Nom=첫째값[SEGON_VALOR[identificador_VALOR]],서술값=SEGON_VALOR[SEGON_VALOR[identificador_VALOR]];
            if(cirurgia_VALOR==178&&UNICODE_VALOR(propietari_objecte,"java/lang/System")&&UNICODE_VALOR(Nom,"out")&&UNICODE_VALOR(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned arxiu_introducció=0;while(arxiu_introducció<필드개수&&(!같음(Nom,camp_nom[arxiu_introducció])||!같음(서술값,필드서술[arxiu_introducció])))arxiu_introducció++;if(!같음(propietari_objecte,첫째값[현재클래스])||arxiu_introducció==필드개수){tecnologies_de_la_informació_invàlid=1;break;}내보내기(cirurgia_VALOR==178?"P(fields[%u]);":"fields[%u]=Q();",arxiu_introducció);}}
        else if(cirurgia_VALOR==182||cirurgia_VALOR==184)호출(절반값(),cirurgia_VALOR==182);
        else if(cirurgia_VALOR==188){unsigned TIPUS_Categoria=byte_dades();if(TIPUS_Categoria!=4&&TIPUS_Categoria!=5&&TIPUS_Categoria!=8&&TIPUS_Categoria!=9&&TIPUS_Categoria!=10)tecnologies_de_la_informació_invàlid=1;내보내기("P(jarray((int)Q()));");}
        else if(cirurgia_VALOR==190)내보내기("P(jlength(Q()));");
        else if(cirurgia_VALOR==198||cirurgia_VALOR==199){int objectiu=(int)ordre_càrrec+(int16_t)절반값();if(objectiu<0||objectiu>=(int)Grup_canviar_la_mida->Mida)tecnologies_de_la_informació_invàlid=1;내보내기("if(Q()%s0)goto L%d;",cirurgia_VALOR==198?"==":"!=",objectiu);}
        else tecnologies_de_la_informació_invàlid=1;
        if(tecnologies_de_la_informació_invàlid)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",Cerca_INDEX,cirurgia_VALOR,ordre_càrrec);
        내보내기("\n");
    }
    durada_VALOR=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned cadena_lliçó(unsigned *dades_càrrec,unsigned finalitzar_DESPLAÇAMENT){
    if(*dades_càrrec>=finalitzar_DESPLAÇAMENT){tecnologies_de_la_informació_invàlid=1;return 0;}unsigned codi_de_caràcter=dades[(*dades_càrrec)++];
    if(codi_de_caràcter<128)return codi_de_caràcter;
    unsigned element_COMPT=codi_de_caràcter>=0xc0&&codi_de_caràcter<=0xdf?1:codi_de_caràcter>=0xe0&&codi_de_caràcter<=0xef?2:3;
    if(element_COMPT==3||element_COMPT>finalitzar_DESPLAÇAMENT-*dades_càrrec){tecnologies_de_la_informació_invàlid=1;return 0;}unsigned VALOR=codi_de_caràcter&((1u<<(6-element_COMPT))-1);
    for(unsigned 순번=0;순번<element_COMPT;순번++){unsigned Següent_element=dades[(*dades_càrrec)++];if((Següent_element&0xc0)!=0x80)tecnologies_de_la_informació_invàlid=1;VALOR=VALOR<<6|(Següent_element&63);}
    if((element_COMPT==1&&VALOR<128&&VALOR!=0)||(element_COMPT==2&&VALOR<2048))tecnologies_de_la_informació_invàlid=1;return VALOR;
}
static void 문자열상수(unsigned identificador_VALOR){
    unsigned 부호없는값=첫째값[identificador_VALOR];if(부호없는값<1||부호없는값>=상수모음||Etiquetes_Llista[부호없는값]!=1){tecnologies_de_la_informació_invàlid=1;return;}내보내기("static const unsigned char k%u[]={",identificador_VALOR);
    unsigned dades_càrrec=첫째값[부호없는값],finalitzar_DESPLAÇAMENT=dades_càrrec+SEGON_VALOR[부호없는값];
    while(dades_càrrec<finalitzar_DESPLAÇAMENT&&!tecnologies_de_la_informació_invàlid){unsigned codi_de_caràcter=cadena_lliçó(&dades_càrrec,finalitzar_DESPLAÇAMENT);
        if(codi_de_caràcter>=0xd800&&codi_de_caràcter<=0xdbff){unsigned 낮은부분=cadena_lliçó(&dades_càrrec,finalitzar_DESPLAÇAMENT);if(낮은부분<0xdc00||낮은부분>0xdfff){tecnologies_de_la_informació_invàlid=1;break;}codi_de_caràcter=0x10000+((codi_de_caràcter-0xd800)<<10)+낮은부분-0xdc00;}
        else if(codi_de_caràcter>=0xdc00&&codi_de_caràcter<=0xdfff){tecnologies_de_la_informació_invàlid=1;break;}
        if(!codi_de_caràcter){printf("jaot: embedded NUL string needs JVM mode\n");tecnologies_de_la_informació_invàlid=1;break;}
        if(codi_de_caràcter<128)내보내기("%u,",codi_de_caràcter);
        else{unsigned element_COMPT=codi_de_caràcter<2048?2:codi_de_caràcter<65536?3:4;내보내기("%u,",(element_COMPT==2?0xc0:element_COMPT==3?0xe0:0xf0)|(codi_de_caràcter>>(6*(element_COMPT-1))));for(unsigned 순번=element_COMPT-1;순번;순번--)내보내기("%u,",0x80|((codi_de_caràcter>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nom){
    size_t element_COMPT=strlen(Nom);
    if(element_COMPT>4&&!strcmp(Nom+element_COMPT-4,".jar")){
        if(꾸러미열기(Nom)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char Camí[256];const char*진입함수=꾸러미진입클래스();element_COMPT=strlen(진입함수);if(element_COMPT+6>=sizeof(Camí))return 0;
        for(unsigned 순번=0;순번<element_COMPT;순번++)Camí[순번]=진입함수[순번]=='.'?'/':진입함수[순번];strcpy(Camí+element_COMPT,".class");int introducció_COMPT=꾸러미읽기(Camí,dades,sizeof(dades));if(introducció_COMPT<0)return 0;durada_VALOR=introducció_COMPT;
    }else{intptr_t arxiu_control_7f4cdfd5=사용자호출(3,(uintptr_t)Nom,0,0,0,0,0);if(arxiu_control_7f4cdfd5<0)return 0;intptr_t introducció_COMPT=사용자호출(9,arxiu_control_7f4cdfd5,0,0,0,0,0);if(introducció_COMPT<0||introducció_COMPT>sizeof(dades)){사용자호출(4,arxiu_control_7f4cdfd5,0,0,0,0,0);return 0;}intptr_t CANTIDAD_RECIBIDA_COMPT=사용자호출(2,arxiu_control_7f4cdfd5,(uintptr_t)dades,introducció_COMPT,0,0,0);사용자호출(4,arxiu_control_7f4cdfd5,0,0,0,0,0);if(CANTIDAD_RECIBIDA_COMPT!=introducció_COMPT)return 0;durada_VALOR=introducció_COMPT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!tecnologies_de_la_informació_invàlid;순번++)if(Etiquetes_Llista[순번]==8)문자열상수(순번);
    if(tecnologies_de_la_informació_invàlid)return 0;
    int introducció_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALOR(메소드목록[순번].Nom,"<init>")){
        int RESULTAT,introducció_COMPT=서술자(메소드목록[순번].서술값,&RESULTAT);if(introducció_COMPT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<introducció_COMPT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!introducció_COMPT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALOR(메소드목록[순번].Nom,"main")&&UNICODE_VALOR(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].configuració_Servei_de_transferència_intel_ligent_en_segon_terme&9)==9)introducció_p=순번;
        if(UNICODE_VALOR(메소드목록[순번].Nom,"<clinit>"))초기값=순번;
    }
    if(introducció_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!tecnologies_de_la_informació_invàlid;순번++)메소드번역(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(필드상수[순번]){
        unsigned codi_de_caràcter=필드상수[순번];if(codi_de_caràcter>=상수모음)return 0;
        if(Etiquetes_Llista[codi_de_caràcter]==3)내보내기("fields[%u]=%uU;",순번,첫째값[codi_de_caràcter]);else if(Etiquetes_Llista[codi_de_caràcter]==8)내보내기("fields[%u]=(W)k%u;",순번,codi_de_caràcter);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",introducció_p);
    return tecnologies_de_la_informació_invàlid?0:SMS;
}
