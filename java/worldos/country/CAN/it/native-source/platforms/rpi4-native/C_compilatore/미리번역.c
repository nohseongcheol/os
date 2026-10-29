#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "aggregare.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char dati[16384];static unsigned durata_VALORE,Regolari_funzione;static int reparto_IT_non_valida;
static unsigned Categorie_elenco[512],첫째값[512],SECONDO_VALORE[512],costante_pool,Regolari_Corso;
static char testo[65536];static unsigned Dimensioni_del_testo;
typedef struct {unsigned configurazione_BITS,Nome,descrittore_dati,istruzione_SEQUENZA,Dimensione,지역변수들,memoria_a_pila;} metodo_voce;
static metodo_voce 메소드목록[64];static unsigned 메소드개수;
static unsigned nome_campo_98daa19b[64],campo_descrittore[64],campo_costante[64],필드개수;
static unsigned INCLUDI_VALORE(unsigned articolo_CONTA_NUMERI){if(Regolari_funzione>durata_VALORE||articolo_CONTA_NUMERI>durata_VALORE-Regolari_funzione){reparto_IT_non_valida=1;return 0;}unsigned dati_funzione=Regolari_funzione;Regolari_funzione+=articolo_CONTA_NUMERI;return dati_funzione;}
static unsigned byte_dati(void){unsigned dati_funzione=INCLUDI_VALORE(1);return reparto_IT_non_valida?0:dati[dati_funzione];}
static unsigned 절반값(void){unsigned coordinata_x=byte_dati();return coordinata_x<<8|byte_dati();}
static uint32_t 가득참(void){uint32_t coordinata_x=절반값();return coordinata_x<<16|절반값();}
static int UNICODE_VALORE(unsigned 순번,const char*stringa_dati){return 순번>0&&순번<costante_pool&&Categorie_elenco[순번]==1&&strlen(stringa_dati)==SECONDO_VALORE[순번]&&!memcmp(dati+첫째값[순번],stringa_dati,SECONDO_VALORE[순번]);}
static int 같음(unsigned coordinata_x,unsigned Y_coordinata){return coordinata_x>0&&coordinata_x<costante_pool&&Y_coordinata>0&&Y_coordinata<costante_pool&&Categorie_elenco[coordinata_x]==1&&Categorie_elenco[Y_coordinata]==1&&SECONDO_VALORE[coordinata_x]==SECONDO_VALORE[Y_coordinata]&&!memcmp(dati+첫째값[coordinata_x],dati+첫째값[Y_coordinata],SECONDO_VALORE[coordinata_x]);}
static void 내보내기(const char*File_voce,...){if(reparto_IT_non_valida)return;va_list argomento_array;va_start(argomento_array,File_voce);int articolo_CONTA_NUMERI=vsnprintf(testo+Dimensioni_del_testo,sizeof(testo)-Dimensioni_del_testo,File_voce,argomento_array);va_end(argomento_array);if(articolo_CONTA_NUMERI<0||(unsigned)articolo_CONTA_NUMERI>=sizeof(testo)-Dimensioni_del_testo){reparto_IT_non_valida=1;return;}Dimensioni_del_testo+=articolo_CONTA_NUMERI;}
static int descrittore_voce(unsigned identificatore_VALORE,int*risultato){
    if(identificatore_VALORE<1||identificatore_VALORE>=costante_pool||Categorie_elenco[identificatore_VALORE]!=1)return -1;unsigned dati_funzione=첫째값[identificatore_VALORE],chiudere_SCARTO=dati_funzione+SECONDO_VALORE[identificatore_VALORE];if(dati_funzione>=chiudere_SCARTO||dati[dati_funzione++]!='(')return -1;int voce_CONTA_NUMERI=0;
    while(dati_funzione<chiudere_SCARTO&&dati[dati_funzione]!=')'){
        unsigned punto_di_codice=dati[dati_funzione++];while(punto_di_codice=='['&&dati_funzione<chiudere_SCARTO)punto_di_codice=dati[dati_funzione++];
        if(punto_di_codice=='L'){while(dati_funzione<chiudere_SCARTO&&dati[dati_funzione]!=';')dati_funzione++;if(dati_funzione==chiudere_SCARTO)return -1;dati_funzione++;}
        else if(punto_di_codice!='I'&&punto_di_codice!='Z'&&punto_di_codice!='B'&&punto_di_codice!='C'&&punto_di_codice!='S')return -1;
        if(++voce_CONTA_NUMERI>16)return -1;
    }
    if(dati_funzione+1>=chiudere_SCARTO||dati[dati_funzione++]!=')')return -1;*risultato=dati[dati_funzione]=='V'?0:1;
    if(dati[dati_funzione]=='J'||dati[dati_funzione]=='D'||dati[dati_funzione]=='F')return -1;return voce_CONTA_NUMERI;
}
static void attributi(void){unsigned articolo_CONTA_NUMERI=절반값();for(unsigned 순번=0;순번<articolo_CONTA_NUMERI&&!reparto_IT_non_valida;순번++){절반값();unsigned Dimensione=가득참();INCLUDI_VALORE(Dimensione);}}
static int analizzare_input(void){
    if(가득참()!=0xcafebabe)return -1;unsigned versione_secondaria=절반값(),numero_di_versione=절반값();if(versione_secondaria||numero_di_versione<45||numero_di_versione>52)return -1;
    costante_pool=절반값();if(costante_pool<1||costante_pool>512)return -1;
    for(unsigned 순번=1;순번<costante_pool&&!reparto_IT_non_valida;순번++){
        Categorie_elenco[순번]=byte_dati();switch(Categorie_elenco[순번]){
        case 1:SECONDO_VALORE[순번]=절반값();첫째값[순번]=INCLUDI_VALORE(SECONDO_VALORE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:INCLUDI_VALORE(8);if(++순번>=costante_pool)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECONDO_VALORE[순번]=절반값();break;
        case 15:첫째값[순번]=byte_dati();SECONDO_VALORE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();Regolari_Corso=절반값();절반값();if(Regolari_Corso<1||Regolari_Corso>=costante_pool||Categorie_elenco[Regolari_Corso]!=7||첫째값[Regolari_Corso]<1||첫째값[Regolari_Corso]>=costante_pool||Categorie_elenco[첫째값[Regolari_Corso]]!=1)return -1;unsigned 인터페이스목록=절반값();INCLUDI_VALORE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!reparto_IT_non_valida;순번++){
        unsigned configurazione_BITS=절반값();nome_campo_98daa19b[순번]=절반값();campo_descrittore[순번]=절반값();
        if(!(configurazione_BITS&8))return -1;
        unsigned voce_CONTA_NUMERI=절반값();for(unsigned 안쪽순번=0;안쪽순번<voce_CONTA_NUMERI&&!reparto_IT_non_valida;안쪽순번++){
            unsigned Nome=절반값(),Dimensione=가득참();
            if(UNICODE_VALORE(Nome,"ConstantValue")){if(Dimensione!=2)return -1;campo_costante[순번]=절반값();}
            else INCLUDI_VALORE(Dimensione);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!reparto_IT_non_valida;순번++){
        metodo_voce*gruppo_ridimensionare=메소드목록+순번;gruppo_ridimensionare->configurazione_BITS=절반값();gruppo_ridimensionare->Nome=절반값();gruppo_ridimensionare->descrittore_dati=절반값();unsigned voce_CONTA_NUMERI=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<voce_CONTA_NUMERI&&!reparto_IT_non_valida;안쪽순번++){
            unsigned Nome=절반값(),Dimensione=가득참(),avvia=Regolari_funzione;
            if(Dimensione>durata_VALORE-Regolari_funzione)return -1;
            if(UNICODE_VALORE(Nome,"Code")){
                gruppo_ridimensionare->memoria_a_pila=절반값();gruppo_ridimensionare->지역변수들=절반값();gruppo_ridimensionare->Dimensione=가득참();gruppo_ridimensionare->istruzione_SEQUENZA=INCLUDI_VALORE(gruppo_ridimensionare->Dimensione);
                if(gruppo_ridimensionare->memoria_a_pila>128||gruppo_ridimensionare->지역변수들>128||gruppo_ridimensionare->Dimensione>8192||절반값())return -1;attributi();
            }else INCLUDI_VALORE(Dimensione);
            if(Regolari_funzione!=avvia+Dimensione)return -1;
        }
        if(!UNICODE_VALORE(gruppo_ridimensionare->Nome,"<init>")&&(!(gruppo_ridimensionare->configurazione_BITS&8)||(gruppo_ridimensionare->configurazione_BITS&(0x100|0x20))||!gruppo_ridimensionare->Dimensione))return -1;
    }
    attributi();return reparto_IT_non_valida||Regolari_funzione!=durata_VALORE?-1:0;
}
static void costante_VALORE(unsigned identificatore_VALORE){
    if(!identificatore_VALORE||identificatore_VALORE>=costante_pool){reparto_IT_non_valida=1;return;}
    if(Categorie_elenco[identificatore_VALORE]==3)내보내기("P(%uU);",첫째값[identificatore_VALORE]);
    else if(Categorie_elenco[identificatore_VALORE]==8)내보내기("P((W)k%u);",identificatore_VALORE);else reparto_IT_non_valida=1;
}
static void 호출(unsigned identificatore_VALORE,int virtuale_Chiama){
    if(identificatore_VALORE<1||identificatore_VALORE>=costante_pool||(Categorie_elenco[identificatore_VALORE]!=10&&Categorie_elenco[identificatore_VALORE]!=11)||첫째값[identificatore_VALORE]<1||첫째값[identificatore_VALORE]>=costante_pool||Categorie_elenco[첫째값[identificatore_VALORE]]!=7||SECONDO_VALORE[identificatore_VALORE]<1||SECONDO_VALORE[identificatore_VALORE]>=costante_pool||Categorie_elenco[SECONDO_VALORE[identificatore_VALORE]]!=12){reparto_IT_non_valida=1;return;}
    unsigned proprietario_oggetto=첫째값[첫째값[identificatore_VALORE]],Nome=첫째값[SECONDO_VALORE[identificatore_VALORE]],descrittore_dati=SECONDO_VALORE[SECONDO_VALORE[identificatore_VALORE]];int risultato=0,articolo_CONTA_NUMERI=descrittore_voce(descrittore_dati,&risultato);if(articolo_CONTA_NUMERI<0){reparto_IT_non_valida=1;return;}
    for(int 순번=articolo_CONTA_NUMERI;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtuale_Chiama)내보내기("Q();");
    if(!virtuale_Chiama&&같음(proprietario_oggetto,첫째값[Regolari_Corso])){
        unsigned gruppo_ridimensionare=0;for(;gruppo_ridimensionare<메소드개수;gruppo_ridimensionare++)if(같음(Nome,메소드목록[gruppo_ridimensionare].Nome)&&같음(descrittore_dati,메소드목록[gruppo_ridimensionare].descrittore_dati))break;
        if(gruppo_ridimensionare==메소드개수||!(메소드목록[gruppo_ridimensionare].configurazione_BITS&8)){reparto_IT_non_valida=1;return;}
        if(risultato)내보내기("P(");내보내기("m%u(",gruppo_ridimensionare);for(int 순번=0;순번<articolo_CONTA_NUMERI;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(risultato?"));":" );");return;
    }
    if((virtuale_Chiama&&UNICODE_VALORE(proprietario_oggetto,"java/io/PrintStream")&& (UNICODE_VALORE(Nome,"print")||UNICODE_VALORE(Nome,"println")))||(!virtuale_Chiama&&UNICODE_VALORE(proprietario_oggetto,"Italiano/nativo/uscitaTesto"))){
        if(UNICODE_VALORE(descrittore_dati,"(I)V")&&(UNICODE_VALORE(Nome,"print")||UNICODE_VALORE(Nome,"println")||UNICODE_VALORE(Nome,"scrivere_numero"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALORE(Nome,"print")?0:1);return;}
        if(UNICODE_VALORE(descrittore_dati,"(Ljava/lang/String;)V")&&(UNICODE_VALORE(Nome,"print")||UNICODE_VALORE(Nome,"println")||UNICODE_VALORE(Nome,"Scrittura")||UNICODE_VALORE(Nome,"scrivere_riga"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALORE(Nome,"print")||UNICODE_VALORE(Nome,"Scrittura")?0:1);return;}
        if(UNICODE_VALORE(descrittore_dati,"()V")&&UNICODE_VALORE(Nome,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtuale_Chiama&&UNICODE_VALORE(proprietario_oggetto,"Italiano/nativo/file")){
        if(UNICODE_VALORE(Nome,"Scrittura")&&UNICODE_VALORE(descrittore_dati,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALORE(Nome,"Lettura")&&UNICODE_VALORE(descrittore_dati,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    reparto_IT_non_valida=1;
}
static void compilare_metodo(unsigned CERCA_INDICE){
    metodo_voce*gruppo_ridimensionare=메소드목록+CERCA_INDICE;if(UNICODE_VALORE(gruppo_ridimensionare->Nome,"<init>"))return;int risultato,articolo_CONTA_NUMERI=descrittore_voce(gruppo_ridimensionare->descrittore_dati,&risultato);if(articolo_CONTA_NUMERI<0){reparto_IT_non_valida=1;return;}
    내보내기("static W m%u(",CERCA_INDICE);for(int 순번=0;순번<articolo_CONTA_NUMERI;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!articolo_CONTA_NUMERI)내보내기("void");
    if((unsigned)articolo_CONTA_NUMERI>gruppo_ridimensionare->지역변수들){reparto_IT_non_valida=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",gruppo_ridimensionare->지역변수들?gruppo_ridimensionare->지역변수들:1);for(int 순번=0;순번<articolo_CONTA_NUMERI;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=durata_VALORE;durata_VALORE=gruppo_ridimensionare->istruzione_SEQUENZA+gruppo_ridimensionare->Dimensione;Regolari_funzione=gruppo_ridimensionare->istruzione_SEQUENZA;
    while(Regolari_funzione<durata_VALORE&&!reparto_IT_non_valida){unsigned comando_funzione=Regolari_funzione-gruppo_ridimensionare->istruzione_SEQUENZA,operazione_VALORE=byte_dati();내보내기("L%u:;",comando_funzione);
        if(operazione_VALORE==0){}
        else if(operazione_VALORE==1)내보내기("P(0);");
        else if(operazione_VALORE>=2&&operazione_VALORE<=8)내보내기("P(%uU);",operazione_VALORE-3);
        else if(operazione_VALORE==16){int VALORE=(int8_t)byte_dati();내보내기("P(%uU);",(unsigned)VALORE);}
        else if(operazione_VALORE==17){int VALORE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALORE);}
        else if(operazione_VALORE==18||operazione_VALORE==19)costante_VALORE(operazione_VALORE==18?byte_dati():절반값());
        else if(operazione_VALORE==21||operazione_VALORE==25){unsigned 순번=byte_dati();if(순번>=gruppo_ridimensionare->지역변수들)reparto_IT_non_valida=1;내보내기("P(v[%u]);",순번);}
        else if((operazione_VALORE>=26&&operazione_VALORE<=29)||(operazione_VALORE>=42&&operazione_VALORE<=45)){unsigned 순번=operazione_VALORE>=42?operazione_VALORE-42:operazione_VALORE-26;if(순번>=gruppo_ridimensionare->지역변수들)reparto_IT_non_valida=1;내보내기("P(v[%u]);",순번);}
        else if(operazione_VALORE==54||operazione_VALORE==58){unsigned 순번=byte_dati();if(순번>=gruppo_ridimensionare->지역변수들)reparto_IT_non_valida=1;내보내기("v[%u]=Q();",순번);}
        else if((operazione_VALORE>=59&&operazione_VALORE<=62)||(operazione_VALORE>=75&&operazione_VALORE<=78)){unsigned 순번=operazione_VALORE>=75?operazione_VALORE-75:operazione_VALORE-59;if(순번>=gruppo_ridimensionare->지역변수들)reparto_IT_non_valida=1;내보내기("v[%u]=Q();",순번);}
        else if(operazione_VALORE==46||operazione_VALORE==50||operazione_VALORE==51||operazione_VALORE==52||operazione_VALORE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operazione_VALORE==79||operazione_VALORE==83||operazione_VALORE==84||operazione_VALORE==85||operazione_VALORE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operazione_VALORE==84?"(unsigned)(signed char)q":operazione_VALORE==85?"(unsigned short)q":operazione_VALORE==86?"(unsigned)(short)q":"q");
        else if(operazione_VALORE==87)내보내기("Q();");
        else if(operazione_VALORE==89)내보내기("q=Q();P(q);P(q);");
        else if(operazione_VALORE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operazione_VALORE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operazione_VALORE==96||operazione_VALORE==100||operazione_VALORE==104||operazione_VALORE==120||operazione_VALORE==124||operazione_VALORE==126||operazione_VALORE==128||operazione_VALORE==130){const char*Codifica_VALORE=operazione_VALORE==96?"+":operazione_VALORE==100?"-":operazione_VALORE==104?"*":operazione_VALORE==120?"<<":operazione_VALORE==124?">>":operazione_VALORE==126?"&":operazione_VALORE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",Codifica_VALORE,operazione_VALORE==120||operazione_VALORE==124?"%32":"");}
        else if(operazione_VALORE==108||operazione_VALORE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operazione_VALORE==112);
        else if(operazione_VALORE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operazione_VALORE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operazione_VALORE==132){unsigned 순번=byte_dati();int 차이=(int8_t)byte_dati();if(순번>=gruppo_ridimensionare->지역변수들)reparto_IT_non_valida=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operazione_VALORE>=145&&operazione_VALORE<=147)내보내기("P((unsigned)(%s)Q());",operazione_VALORE==145?"signed char":operazione_VALORE==146?"unsigned short":"short");
        else if(operazione_VALORE>=153&&operazione_VALORE<=166){int target=(int)comando_funzione+(int16_t)절반값();const char*Confronto_VALORE[]={"==","!=","<",">=",">","<="};if(target<0||target>=(int)gruppo_ridimensionare->Dimensione){reparto_IT_non_valida=1;break;}if(operazione_VALORE<159)내보내기("if((int)Q()%s0)goto L%d;",Confronto_VALORE[operazione_VALORE-153],target);else if(operazione_VALORE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Confronto_VALORE[operazione_VALORE-159],target);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operazione_VALORE==165?"==":"!=",target);}
        else if(operazione_VALORE==167){int target=(int)comando_funzione+(int16_t)절반값();if(target<0||target>=(int)gruppo_ridimensionare->Dimensione)reparto_IT_non_valida=1;내보내기("goto L%d;",target);}
        else if(operazione_VALORE==172||operazione_VALORE==176)내보내기("return Q();");else if(operazione_VALORE==177)내보내기("return 0;");
        else if(operazione_VALORE==178||operazione_VALORE==179){unsigned identificatore_VALORE=절반값();if(identificatore_VALORE<1||identificatore_VALORE>=costante_pool||Categorie_elenco[identificatore_VALORE]!=9||첫째값[identificatore_VALORE]>=costante_pool||SECONDO_VALORE[identificatore_VALORE]>=costante_pool||Categorie_elenco[첫째값[identificatore_VALORE]]!=7||Categorie_elenco[SECONDO_VALORE[identificatore_VALORE]]!=12){reparto_IT_non_valida=1;break;}unsigned proprietario_oggetto=첫째값[첫째값[identificatore_VALORE]],Nome=첫째값[SECONDO_VALORE[identificatore_VALORE]],descrittore_dati=SECONDO_VALORE[SECONDO_VALORE[identificatore_VALORE]];
            if(operazione_VALORE==178&&UNICODE_VALORE(proprietario_oggetto,"java/lang/System")&&UNICODE_VALORE(Nome,"out")&&UNICODE_VALORE(descrittore_dati,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned File_voce=0;while(File_voce<필드개수&&(!같음(Nome,nome_campo_98daa19b[File_voce])||!같음(descrittore_dati,campo_descrittore[File_voce])))File_voce++;if(!같음(proprietario_oggetto,첫째값[Regolari_Corso])||File_voce==필드개수){reparto_IT_non_valida=1;break;}내보내기(operazione_VALORE==178?"P(fields[%u]);":"fields[%u]=Q();",File_voce);}}
        else if(operazione_VALORE==182||operazione_VALORE==184)호출(절반값(),operazione_VALORE==182);
        else if(operazione_VALORE==188){unsigned TIPO_area=byte_dati();if(TIPO_area!=4&&TIPO_area!=5&&TIPO_area!=8&&TIPO_area!=9&&TIPO_area!=10)reparto_IT_non_valida=1;내보내기("P(jarray((int)Q()));");}
        else if(operazione_VALORE==190)내보내기("P(jlength(Q()));");
        else if(operazione_VALORE==198||operazione_VALORE==199){int target=(int)comando_funzione+(int16_t)절반값();if(target<0||target>=(int)gruppo_ridimensionare->Dimensione)reparto_IT_non_valida=1;내보내기("if(Q()%s0)goto L%d;",operazione_VALORE==198?"==":"!=",target);}
        else reparto_IT_non_valida=1;
        if(reparto_IT_non_valida)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",CERCA_INDICE,operazione_VALORE,comando_funzione);
        내보내기("\n");
    }
    durata_VALORE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned stringa_unità(unsigned *dati_funzione,unsigned chiudere_SCARTO){
    if(*dati_funzione>=chiudere_SCARTO){reparto_IT_non_valida=1;return 0;}unsigned punto_di_codice=dati[(*dati_funzione)++];
    if(punto_di_codice<128)return punto_di_codice;
    unsigned articolo_CONTA_NUMERI=punto_di_codice>=0xc0&&punto_di_codice<=0xdf?1:punto_di_codice>=0xe0&&punto_di_codice<=0xef?2:3;
    if(articolo_CONTA_NUMERI==3||articolo_CONTA_NUMERI>chiudere_SCARTO-*dati_funzione){reparto_IT_non_valida=1;return 0;}unsigned VALORE=punto_di_codice&((1u<<(6-articolo_CONTA_NUMERI))-1);
    for(unsigned 순번=0;순번<articolo_CONTA_NUMERI;순번++){unsigned Avanti_articolo=dati[(*dati_funzione)++];if((Avanti_articolo&0xc0)!=0x80)reparto_IT_non_valida=1;VALORE=VALORE<<6|(Avanti_articolo&63);}
    if((articolo_CONTA_NUMERI==1&&VALORE<128&&VALORE!=0)||(articolo_CONTA_NUMERI==2&&VALORE<2048))reparto_IT_non_valida=1;return VALORE;
}
static void stringa_costante(unsigned identificatore_VALORE){
    unsigned 부호없는값=첫째값[identificatore_VALORE];if(부호없는값<1||부호없는값>=costante_pool||Categorie_elenco[부호없는값]!=1){reparto_IT_non_valida=1;return;}내보내기("static const unsigned char k%u[]={",identificatore_VALORE);
    unsigned dati_funzione=첫째값[부호없는값],chiudere_SCARTO=dati_funzione+SECONDO_VALORE[부호없는값];
    while(dati_funzione<chiudere_SCARTO&&!reparto_IT_non_valida){unsigned punto_di_codice=stringa_unità(&dati_funzione,chiudere_SCARTO);
        if(punto_di_codice>=0xd800&&punto_di_codice<=0xdbff){unsigned 낮은부분=stringa_unità(&dati_funzione,chiudere_SCARTO);if(낮은부분<0xdc00||낮은부분>0xdfff){reparto_IT_non_valida=1;break;}punto_di_codice=0x10000+((punto_di_codice-0xd800)<<10)+낮은부분-0xdc00;}
        else if(punto_di_codice>=0xdc00&&punto_di_codice<=0xdfff){reparto_IT_non_valida=1;break;}
        if(!punto_di_codice){printf("jaot: embedded NUL string needs JVM mode\n");reparto_IT_non_valida=1;break;}
        if(punto_di_codice<128)내보내기("%u,",punto_di_codice);
        else{unsigned articolo_CONTA_NUMERI=punto_di_codice<2048?2:punto_di_codice<65536?3:4;내보내기("%u,",(articolo_CONTA_NUMERI==2?0xc0:articolo_CONTA_NUMERI==3?0xe0:0xf0)|(punto_di_codice>>(6*(articolo_CONTA_NUMERI-1))));for(unsigned 순번=articolo_CONTA_NUMERI-1;순번;순번--)내보내기("%u,",0x80|((punto_di_codice>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nome){
    size_t articolo_CONTA_NUMERI=strlen(Nome);
    if(articolo_CONTA_NUMERI>4&&!strcmp(Nome+articolo_CONTA_NUMERI-4,".jar")){
        if(꾸러미열기(Nome)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char percorso[256];const char*voce_metodo=꾸러미진입클래스();articolo_CONTA_NUMERI=strlen(voce_metodo);if(articolo_CONTA_NUMERI+6>=sizeof(percorso))return 0;
        for(unsigned 순번=0;순번<articolo_CONTA_NUMERI;순번++)percorso[순번]=voce_metodo[순번]=='.'?'/':voce_metodo[순번];strcpy(percorso+articolo_CONTA_NUMERI,".class");int voce_CONTA_NUMERI=꾸러미읽기(percorso,dati,sizeof(dati));if(voce_CONTA_NUMERI<0)return 0;durata_VALORE=voce_CONTA_NUMERI;
    }else{intptr_t handle_di_file=사용자호출(3,(uintptr_t)Nome,0,0,0,0,0);if(handle_di_file<0)return 0;intptr_t voce_CONTA_NUMERI=사용자호출(9,handle_di_file,0,0,0,0,0);if(voce_CONTA_NUMERI<0||voce_CONTA_NUMERI>sizeof(dati)){사용자호출(4,handle_di_file,0,0,0,0,0);return 0;}intptr_t RICEV_SCAD_CONTA_NUMERI=사용자호출(2,handle_di_file,(uintptr_t)dati,voce_CONTA_NUMERI,0,0,0);사용자호출(4,handle_di_file,0,0,0,0,0);if(RICEV_SCAD_CONTA_NUMERI!=voce_CONTA_NUMERI)return 0;durata_VALORE=voce_CONTA_NUMERI;}
    if(analizzare_input()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<costante_pool&&!reparto_IT_non_valida;순번++)if(Categorie_elenco[순번]==8)stringa_costante(순번);
    if(reparto_IT_non_valida)return 0;
    int punto_di_ingresso=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALORE(메소드목록[순번].Nome,"<init>")){
        int risultato,voce_CONTA_NUMERI=descrittore_voce(메소드목록[순번].descrittore_dati,&risultato);if(voce_CONTA_NUMERI<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<voce_CONTA_NUMERI;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!voce_CONTA_NUMERI)내보내기("void");내보내기(");\n");
        if(UNICODE_VALORE(메소드목록[순번].Nome,"main")&&UNICODE_VALORE(메소드목록[순번].descrittore_dati,"([Ljava/lang/String;)V")&&(메소드목록[순번].configurazione_BITS&9)==9)punto_di_ingresso=순번;
        if(UNICODE_VALORE(메소드목록[순번].Nome,"<clinit>"))초기값=순번;
    }
    if(punto_di_ingresso<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!reparto_IT_non_valida;순번++)compilare_metodo(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(campo_costante[순번]){
        unsigned punto_di_codice=campo_costante[순번];if(punto_di_codice>=costante_pool)return 0;
        if(Categorie_elenco[punto_di_codice]==3)내보내기("fields[%u]=%uU;",순번,첫째값[punto_di_codice]);else if(Categorie_elenco[punto_di_codice]==8)내보내기("fields[%u]=(W)k%u;",순번,punto_di_codice);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",punto_di_ingresso);
    return reparto_IT_non_valida?0:testo;
}
