#include "../명명/기계연결이름.h"
#include "호출.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *C_output(size_t *);
extern const char *자바미리번역원문(const char *);
typedef struct { unsigned char identificatore_VALORE[16];uint16_t TIPO_area,computer_TIPO;uint32_t numero_di_versione;uint64_t punto_di_ingresso,app_Intestazione_SCARTO,intestazione_della_sezione_SCARTO;uint32_t configurazione_BITS;uint16_t Dimensione,app_Intestazione_ridimensionare,app_Intestazione_CONTA_NUMERI,intestazione_della_sezione_ridimensionare,intestazione_della_sezione_CONTA_NUMERI,sezione_nome_tabella; } Intestazione_VALORE;
typedef struct {uint32_t TIPO_area,configurazione_BITS;uint64_t SCARTO_VALORE,e_mail,fisico_e_mail,파일영역크기,기억영역크기,allineare_limite;} segmento_VALORE;
static unsigned char foto[16384];
static int pubblicare_voce(const char *Nome){
    size_t articolo_CONTA_NUMERI;const unsigned char*원본자료=C_output(&articolo_CONTA_NUMERI);if(articolo_CONTA_NUMERI<sizeof(Intestazione_VALORE))return -1;
    Intestazione_VALORE eseguibile_Intestazione;memcpy(&eseguibile_Intestazione,원본자료,sizeof(eseguibile_Intestazione));
    if(eseguibile_Intestazione.TIPO_area!=2||eseguibile_Intestazione.computer_TIPO!=183||eseguibile_Intestazione.app_Intestazione_ridimensionare!=sizeof(segmento_VALORE)||!eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI||eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI>16||eseguibile_Intestazione.app_Intestazione_SCARTO>articolo_CONTA_NUMERI||eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI*sizeof(segmento_VALORE)>articolo_CONTA_NUMERI-eseguibile_Intestazione.app_Intestazione_SCARTO)return -1;
    eseguibile_Intestazione.app_Intestazione_SCARTO=sizeof(eseguibile_Intestazione);eseguibile_Intestazione.intestazione_della_sezione_SCARTO=eseguibile_Intestazione.intestazione_della_sezione_CONTA_NUMERI=eseguibile_Intestazione.intestazione_della_sezione_ridimensionare=eseguibile_Intestazione.sezione_nome_tabella=0;memcpy(foto,&eseguibile_Intestazione,sizeof(eseguibile_Intestazione));
    size_t 부가정보=sizeof(eseguibile_Intestazione)+eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI*sizeof(segmento_VALORE),Avanti_articolo=4096;unsigned char pagina_elenco[3072]={0};int valido_punto_di_ingresso=0;
    for(unsigned 순번=0;순번<eseguibile_Intestazione.app_Intestazione_CONTA_NUMERI;순번++){
        segmento_VALORE dati_funzione;Intestazione_VALORE 원본;memcpy(&원본,원본자료,sizeof(원본));memcpy(&dati_funzione,원본자료+원본.app_Intestazione_SCARTO+순번*sizeof(dati_funzione),sizeof(dati_funzione));
        if(dati_funzione.SCARTO_VALORE>articolo_CONTA_NUMERI||dati_funzione.파일영역크기>articolo_CONTA_NUMERI-dati_funzione.SCARTO_VALORE||dati_funzione.파일영역크기>dati_funzione.기억영역크기)return -1;
        if(dati_funzione.TIPO_area==1){
            if((dati_funzione.configurazione_BITS&~7u)||!(dati_funzione.configurazione_BITS&4)||(dati_funzione.configurazione_BITS&3)==3||dati_funzione.e_mail<0x02000000||dati_funzione.e_mail>0x02c00000||dati_funzione.기억영역크기>0x02c00000-dati_funzione.e_mail)return -1;
            if((dati_funzione.configurazione_BITS&1)&&eseguibile_Intestazione.punto_di_ingresso>=dati_funzione.e_mail&&eseguibile_Intestazione.punto_di_ingresso-dati_funzione.e_mail<dati_funzione.파일영역크기&&!(eseguibile_Intestazione.punto_di_ingresso&3))valido_punto_di_ingresso=1;
            size_t 선행값=dati_funzione.e_mail&4095,바이트들=dati_funzione.파일영역크기?선행값+dati_funzione.파일영역크기:0;
            if(Avanti_articolo>sizeof(foto)||바이트들>sizeof(foto)-Avanti_articolo){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(Avanti_articolo+바이트들),(unsigned)sizeof(foto));return -1;}
            if(바이트들)memcpy(foto+Avanti_articolo+선행값,원본자료+dati_funzione.SCARTO_VALORE,dati_funzione.파일영역크기);
            dati_funzione.e_mail-=선행값;dati_funzione.fisico_e_mail=dati_funzione.e_mail;dati_funzione.기억영역크기+=선행값;dati_funzione.파일영역크기=바이트들;dati_funzione.SCARTO_VALORE=Avanti_articolo;dati_funzione.allineare_limite=4096;
            for(uint64_t pagina_VALORE=dati_funzione.e_mail;pagina_VALORE<dati_funzione.e_mail+dati_funzione.기억영역크기;pagina_VALORE+=4096){unsigned CERCA_INDICE=(pagina_VALORE-0x02000000)/4096;if(CERCA_INDICE>=sizeof(pagina_elenco)||pagina_elenco[CERCA_INDICE]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}pagina_elenco[CERCA_INDICE]=1;}
            Avanti_articolo+=(바이트들+4095)&~(size_t)4095;
        }else if(dati_funzione.TIPO_area==4){if(dati_funzione.파일영역크기>4096-부가정보)return -1;memcpy(foto+부가정보,원본자료+dati_funzione.SCARTO_VALORE,dati_funzione.파일영역크기);dati_funzione.SCARTO_VALORE=부가정보;부가정보+=dati_funzione.파일영역크기;}
        else if(dati_funzione.TIPO_area!=0&&dati_funzione.TIPO_area!=6&&dati_funzione.TIPO_area!=0x6474e551)return -1;
        memcpy(foto+eseguibile_Intestazione.app_Intestazione_SCARTO+순번*sizeof(dati_funzione),&dati_funzione,sizeof(dati_funzione));
    }
    if(!valido_punto_di_ingresso)return -1;
    intptr_t handle_di_file=사용자호출(3,(uintptr_t)Nome,577,0600,0,0,0);if(handle_di_file<0){printf("cc: cannot create output file, error %d\n",(int)handle_di_file);return -1;}
    intptr_t 쓴수=사용자호출(1,handle_di_file,(uintptr_t)foto,Avanti_articolo,0,0,0);사용자호출(4,handle_di_file,0,0,0,0,0);return 쓴수==(intptr_t)Avanti_articolo?0:-1;
}
int START_USER_app(int metodo_MODA){
    char input[256],선택항목[256],output[256]="a.elf";
    int 인수개수=사용자호출(15,UINTPTR_MAX,0,0,0,0,0);
    if(인수개수!=1&&인수개수!=3){printf(metodo_MODA?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(사용자호출(15,0,(uintptr_t)input,sizeof(input),0,0,0)<0)return 2;
    if(인수개수==1&&(!strcmp(input,"--version")||!strcmp(input,"-version"))){printf(metodo_MODA?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(인수개수==3){사용자호출(15,1,(uintptr_t)선택항목,sizeof(선택항목),0,0,0);if(strcmp(선택항목,"-o")||사용자호출(15,2,(uintptr_t)output,sizeof(output),0,0,0)<0)return 2;}
    if(!strcmp(input,output)){printf("cc: input and output must differ\n");return 2;}
    TCCState*stringa_dati=tcc_new();if(!stringa_dati)return 1;
    tcc_undefine_symbol(stringa_dati,"__linux__");tcc_undefine_symbol(stringa_dati,"__linux");tcc_undefine_symbol(stringa_dati,"linux");
    tcc_undefine_symbol(stringa_dati,"__unix__");tcc_undefine_symbol(stringa_dati,"__unix");tcc_undefine_symbol(stringa_dati,"unix");
    tcc_undefine_symbol(stringa_dati,"__STDC_HOSTED__");tcc_define_symbol(stringa_dati,"__STDC_HOSTED__","0");tcc_define_symbol(stringa_dati,"__JKOROS__","1");
    tcc_set_options(stringa_dati,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(stringa_dati,"/sdk/include");
    int 반환값=tcc_set_output_type(stringa_dati,TCC_OUTPUT_EXE);
    if(!반환값){if(metodo_MODA){const char*원본자료=자바미리번역원문(input);반환값=원본자료?tcc_compile_string(stringa_dati,원본자료):-1;}else 반환값=tcc_add_file(stringa_dati,input);}
    if(!반환값)반환값=tcc_add_file(stringa_dati,"/sdk/lib/start.o");
    if(!반환값)반환값=tcc_add_file(stringa_dati,"/sdk/lib/crt.o");
    if(!반환값&&metodo_MODA)반환값=tcc_add_file(stringa_dati,"/sdk/lib/aot-runtime.o");
    if(!반환값)반환값=tcc_add_file(stringa_dati,"/sdk/lib/libposix-kor-user.a");
    if(!반환값)반환값=tcc_output_file(stringa_dati,"/@cc-output");
    if(!반환값)반환값=pubblicare_voce(output);
    tcc_delete(stringa_dati);
    if(반환값){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(metodo_MODA?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",output);return 0;
}
