/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Editor_capacidade 16384
static unsigned char Texto[Editor_capacidade],desfacer_datos[Editor_capacidade],복사자료[Editor_capacidade],medida_datos[1024];
static int duración_VALOR,ÍNDICE_VALOR,맨위,왼쪽,변경됨,Inserir,desfacer_duración,위쪽,desfacer_Modificacións,되돌림있음,copiar_duración,사용량,COLUMNAS=68,FILA_CONTAR=19;
static char Ficheiro_introdución_nome[64],Orde[128],Busca_introdución[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned pendente_Chave;
static int axuda_Categoría,Estado_IMAXE,Estado_cola;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)medida_datos,사용량,0,0,0);사용량=0;}}
static void byte_datos(unsigned código_de_carácter){if(Estado_IMAXE){if((código_de_carácter&192)!=128){Estado_cola+=código_de_carácter>=196?2:1;}if(Estado_cola>=COLUMNAS)return;}if(사용량==(int)sizeof(medida_datos))출력비우기();medida_datos[사용량++]=código_de_carácter;}
static void 글내보내기(const char *cadea_datos){while(*cadea_datos)byte_datos((unsigned char)*cadea_datos++);}
static void 수치(unsigned elemento_CONTAR){char SEGUNDO_VALOR[12];int 순번=0;do{SEGUNDO_VALOR[순번++]='0'+elemento_CONTAR%10;elemento_CONTAR/=10;}while(elemento_CONTAR);while(순번)byte_datos(SEGUNDO_VALOR[--순번]);}
static void mover_VALOR(int FILA_cargo,int COLUMNA_cargo){글내보내기("\033[");수치(FILA_cargo);byte_datos(';');수치(COLUMNA_cargo);byte_datos('H');}
static int 이전항목(int datos_cargo){if(datos_cargo){datos_cargo--;while(datos_cargo>0&&(Texto[datos_cargo]&192)==128)datos_cargo--;}return datos_cargo;}
static int Seguinte_elemento(int datos_cargo){if(datos_cargo<duración_VALOR){datos_cargo++;while(datos_cargo<duración_VALOR&&(Texto[datos_cargo]&192)==128)datos_cargo++;}return datos_cargo;}
static int Executar_2(int datos_cargo){while(datos_cargo>0&&Texto[datos_cargo-1]!='\n')datos_cargo--;return datos_cargo;}
static int finalizar_DESPRAZAMENTO(int datos_cargo){while(datos_cargo<duración_VALOR&&Texto[datos_cargo]!='\n')datos_cargo++;return datos_cargo;}
static int 너비(unsigned código_de_carácter){return código_de_carácter>=196?2:1;}
static int COLUMNA(int datos_cargo){int código_de_carácter=0;for(int 순번=Executar_2(datos_cargo);순번<datos_cargo;순번=Seguinte_elemento(순번))código_de_carácter+=Texto[순번]=='\t'?4-código_de_carácter%4:너비(Texto[순번]);return código_de_carácter;}
static void punto_de_verificación(void){for(int 순번=0;순번<duración_VALOR;순번++)desfacer_datos[순번]=Texto[순번];desfacer_duración=duración_VALOR;위쪽=ÍNDICE_VALOR;desfacer_Modificacións=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){punto_de_verificación();for(int 순번=도착위치;순번<duración_VALOR;순번++)Texto[출발위치+순번-도착위치]=Texto[순번];duración_VALOR-=도착위치-출발위치;ÍNDICE_VALOR=출발위치;변경됨=1;}
static int Anexar_VALOR(const unsigned char *cadea_datos,int elemento_CONTAR){if(elemento_CONTAR>Editor_capacidade-duración_VALOR){알림문="File full (16384 bytes)";return 0;}punto_de_verificación();for(int 순번=duración_VALOR-1;순번>=ÍNDICE_VALOR;순번--)Texto[순번+elemento_CONTAR]=Texto[순번];for(int 순번=0;순번<elemento_CONTAR;순번++)Texto[ÍNDICE_VALOR+순번]=cadea_datos[순번];duración_VALOR+=elemento_CONTAR;ÍNDICE_VALOR+=elemento_CONTAR;변경됨=1;return 1;}
static void Vertical(int 차이){int COLUMNA_cargo=COLUMNA(ÍNDICE_VALOR),datos_cargo=Executar_2(ÍNDICE_VALOR);if(차이<0){if(!datos_cargo)return;datos_cargo=Executar_2(datos_cargo-1);}else{datos_cargo=finalizar_DESPRAZAMENTO(datos_cargo);if(datos_cargo==duración_VALOR)return;datos_cargo++;}int código_de_carácter=0;while(datos_cargo<duración_VALOR&&Texto[datos_cargo]!='\n'&&código_de_carácter<COLUMNA_cargo){código_de_carácter+=Texto[datos_cargo]=='\t'?4-código_de_carácter%4:너비(Texto[datos_cargo]);datos_cargo=Seguinte_elemento(datos_cargo);}ÍNDICE_VALOR=datos_cargo;}
static void 화면그리기(void){
    if(ÍNDICE_VALOR>duración_VALOR)ÍNDICE_VALOR=duración_VALOR;if(맨위>ÍNDICE_VALOR)맨위=Executar_2(ÍNDICE_VALOR);맨위=Executar_2(맨위);
    int FILA_cargo=0;for(int 순번=맨위;순번<ÍNDICE_VALOR;순번++)if(Texto[순번]=='\n')FILA_cargo++;
    while(FILA_cargo>=FILA_CONTAR-1){맨위=finalizar_DESPRAZAMENTO(맨위);if(맨위<duración_VALOR)맨위++;FILA_cargo--;}
    int COLUMNA_cargo=COLUMNA(ÍNDICE_VALOR);if(COLUMNA_cargo<왼쪽)왼쪽=COLUMNA_cargo;if(COLUMNA_cargo-왼쪽>=COLUMNAS-1)왼쪽=COLUMNA_cargo-COLUMNAS+2;
    글내보내기("\033[?25l");int datos_cargo=맨위;
    for(int 반환값=0;반환값<FILA_CONTAR-1;반환값++){
        mover_VALOR(반환값+1,1);글내보내기("\033[0m\033[2K");int código_de_carácter=0,그려진상태=0;
        if(datos_cargo>=duración_VALOR&&반환값>FILA_cargo){글내보내기("\033[90m~\033[0m");continue;}
        while(datos_cargo<duración_VALOR&&Texto[datos_cargo]!='\n'){
            int Seguinte_DESPRAZAMENTO=Seguinte_elemento(datos_cargo),너비값=Texto[datos_cargo]=='\t'?4-código_de_carácter%4:너비(Texto[datos_cargo]);
            if(código_de_carácter>=왼쪽&&código_de_carácter-왼쪽+너비값<COLUMNAS){
                if(Texto[datos_cargo]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_datos(' ');}else if(Texto[datos_cargo]<32||Texto[datos_cargo]==127){byte_datos('?');}else for(int 안쪽순번=datos_cargo;안쪽순번<Seguinte_DESPRAZAMENTO;안쪽순번++)byte_datos(Texto[안쪽순번]);그려진상태+=너비값;
            }código_de_carácter+=너비값;datos_cargo=Seguinte_DESPRAZAMENTO;
        }
        (void)그려진상태;if(datos_cargo<duración_VALOR)datos_cargo++;
    }
    mover_VALOR(FILA_CONTAR,1);글내보내기("\033[7m\033[2K");Estado_IMAXE=1;Estado_cola=0;글내보내기(Inserir?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Ficheiro_introdución_nome[이름바이트수]&&이름바이트수<30)byte_datos(Ficheiro_introdución_nome[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Liña=1;for(int 순번=0;순번<ÍNDICE_VALOR;순번++)if(Texto[순번]=='\n')Liña++;수치(Liña);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int elemento_CONTAR=0;글내보내기(" | ");while(알림문[elemento_CONTAR]&&elemento_CONTAR<20)byte_datos(알림문[elemento_CONTAR++]);}
    Estado_IMAXE=0;글내보내기("\033[0m");mover_VALOR(FILA_cargo+1,COLUMNA_cargo-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(pendente_Chave){int 셋째순번=pendente_Chave;pendente_Chave=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Tamaño=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNAS!=(int)(Tamaño&65535)||FILA_CONTAR!=(int)(Tamaño>>16)){
            COLUMNAS=Tamaño&65535;FILA_CONTAR=Tamaño>>16;화면그리기();
            if(axuda_Categoría){mover_VALOR(FILA_CONTAR,1);글내보내기("\033[0m\033[2K");byte_datos(axuda_Categoría);글내보내기(Orde);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned ao_corrente_cargo=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-ao_corrente_cargo<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){pendente_Chave=셋째순번;return 27;}
    int elemento_CONTAR=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){elemento_CONTAR=elemento_CONTAR*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return elemento_CONTAR==3?1007:elemento_CONTAR==5?1008:elemento_CONTAR==6?1009:elemento_CONTAR==1?1005:elemento_CONTAR==4?1006:27;return 27;}return 27;
}
static int Store_VALOR(void){
    int Ficheiro_agarradoira=abrir_Ficheiro(Ficheiro_introdución_nome,de_lectura_e_escrita|없으면만들기|내용비우기,0600);if(Ficheiro_agarradoira<0){알림문="Cannot open for save";return 0;}
    intptr_t elemento_CONTAR=escribir_Ficheiro_datos(Ficheiro_agarradoira,Texto,duración_VALOR);peche_Ficheiro(Ficheiro_agarradoira);if(elemento_CONTAR!=duración_VALOR){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEGUNDO_VALOR){while(*첫째값&&*첫째값==*SEGUNDO_VALOR){첫째값++;SEGUNDO_VALOR++;}return *첫째값==*SEGUNDO_VALOR;}
static void Busca_Seguinte(void){int elemento_CONTAR=0;while(Busca_introdución[elemento_CONTAR])elemento_CONTAR++;if(!elemento_CONTAR){알림문="No search pattern";return;}for(int 순번=1;순번<=duración_VALOR;순번++){int datos_cargo=(ÍNDICE_VALOR+순번)%(duración_VALOR?duración_VALOR:1),안쪽순번=0;while(안쪽순번<elemento_CONTAR&&datos_cargo+안쪽순번<duración_VALOR&&Texto[datos_cargo+안쪽순번]==(unsigned char)Busca_introdución[안쪽순번])안쪽순번++;if(안쪽순번==elemento_CONTAR){ÍNDICE_VALOR=datos_cargo;알림문="Match";return;}}알림문="Pattern not found";}
static int avisar(int Categoría_VALOR){
    int elemento_CONTAR=0;Orde[0]=0;
    for(;;){mover_VALOR(FILA_CONTAR,1);글내보내기("\033[0m\033[2K");byte_datos(Categoría_VALOR);글내보내기(Orde);출력비우기();axuda_Categoría=Categoría_VALOR;int 셋째순번=누름값();axuda_Categoría=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(elemento_CONTAR){elemento_CONTAR--;while(elemento_CONTAR>0&&((unsigned char)Orde[elemento_CONTAR]&192)==128)elemento_CONTAR--;Orde[elemento_CONTAR]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&elemento_CONTAR<120){Orde[elemento_CONTAR++]=셋째순번;Orde[elemento_CONTAR]=0;}
    }
    if(Categoría_VALOR=='/'){for(int 순번=0;순번<=elemento_CONTAR;순번++)Busca_introdución[순번]=Orde[순번];Busca_Seguinte();return 0;}
    if(같은지(Orde,"q!"))return 1;
    if(같은지(Orde,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Orde,"wq")||같은지(Orde,"x"))return Store_VALOR();
    if(같은지(Orde,"w")){Store_VALOR();return 0;}
    if(Orde[0]=='w'&&Orde[1]==' '){int 순번=2;while(Orde[순번]==' ')순번++;int Tamaño=elemento_CONTAR-순번;if(Tamaño<1||Tamaño>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Tamaño;안쪽순번++)Ficheiro_introdución_nome[안쪽순번]=Orde[순번+안쪽순번];Ficheiro_introdución_nome[Tamaño]=0;Store_VALOR();return 0;}
    int Liña=0;for(int 순번=0;순번<elemento_CONTAR;순번++){if(Orde[순번]<'0'||Orde[순번]>'9'){Liña=0;break;}Liña=Liña*10+Orde[순번]-'0';if(Liña>16384){Liña=0;break;}}
    if(Liña){ÍNDICE_VALOR=0;while(--Liña&&ÍNDICE_VALOR<duración_VALOR){ÍNDICE_VALOR=finalizar_DESPRAZAMENTO(ÍNDICE_VALOR);if(ÍNDICE_VALOR<duración_VALOR)ÍNDICE_VALOR++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int START_usuario_apl(int 무시값){
    (void)무시값;if(usuario_argumento_CONTAR()!=1||usuario_argumento(0,Ficheiro_introdución_nome,sizeof(Ficheiro_introdución_nome))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Ficheiro_agarradoira=abrir_Ficheiro(Ficheiro_introdución_nome,só_de_lectura_VALOR,0);
    if(Ficheiro_agarradoira>=0){int elemento_CONTAR=파일크기(Ficheiro_agarradoira);if(elemento_CONTAR<0||elemento_CONTAR>Editor_capacidade){peche_Ficheiro(Ficheiro_agarradoira);return 1;}duración_VALOR=파일자료읽기(Ficheiro_agarradoira,Texto,elemento_CONTAR);peche_Ficheiro(Ficheiro_agarradoira);if(duración_VALOR!=elemento_CONTAR)return 1;for(int 순번=0;순번<duración_VALOR;순번++)if(!Texto[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(número_de_erro!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNAS=흐린색&65535;FILA_CONTAR=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,saír_apl_55b3a1cd=0;
    while(!saír_apl_55b3a1cd){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Vertical(-1);continue;}if(셋째순번==1002){Vertical(1);continue;}if(셋째순번==1003){ÍNDICE_VALOR=Seguinte_elemento(ÍNDICE_VALOR);continue;}if(셋째순번==1004){ÍNDICE_VALOR=이전항목(ÍNDICE_VALOR);continue;}
        if(셋째순번==1005){ÍNDICE_VALOR=Executar_2(ÍNDICE_VALOR);continue;}if(셋째순번==1006){ÍNDICE_VALOR=finalizar_DESPRAZAMENTO(ÍNDICE_VALOR);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<FILA_CONTAR-2;순번++)Vertical(셋째순번==1008?-1:1);continue;}
        if(Inserir){
            if(셋째순번==27||셋째순번==3){Inserir=0;continue;}
            if(셋째순번==127||셋째순번==8){if(ÍNDICE_VALOR)바이트지우기(이전항목(ÍNDICE_VALOR),ÍNDICE_VALOR);continue;}
            if(셋째순번==1007){if(ÍNDICE_VALOR<duración_VALOR)바이트지우기(ÍNDICE_VALOR,Seguinte_elemento(ÍNDICE_VALOR));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEGUNDO_VALOR[4];SEGUNDO_VALOR[0]=셋째순번;int elemento_CONTAR=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!elemento_CONTAR){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<elemento_CONTAR;순번++){int código_de_carácter=누름값();if(código_de_carácter<128||código_de_carácter>191){pendente_Chave=código_de_carácter;유효함=0;break;}SEGUNDO_VALOR[순번]=código_de_carácter;}
                if(유효함)Anexar_VALOR(SEGUNDO_VALOR,elemento_CONTAR);
            }continue;
        }
        if(앞부분){int datos_cargo=앞부분;앞부분=0;if(datos_cargo=='g'&&셋째순번=='g'){ÍNDICE_VALOR=0;continue;}if(datos_cargo=='Z'&&셋째순번=='Z'){saír_apl_55b3a1cd=Store_VALOR();continue;}if((datos_cargo=='d'&&셋째순번=='d')||(datos_cargo=='y'&&셋째순번=='y')){int 첫째값=Executar_2(ÍNDICE_VALOR),SEGUNDO_VALOR=finalizar_DESPRAZAMENTO(ÍNDICE_VALOR);if(SEGUNDO_VALOR<duración_VALOR)SEGUNDO_VALOR++;copiar_duración=SEGUNDO_VALOR-첫째값;for(int 순번=0;순번<copiar_duración;순번++)복사자료[순번]=Texto[첫째값+순번];if(datos_cargo=='d')바이트지우기(첫째값,SEGUNDO_VALOR);continue;}}
        if(셋째순번=='i'){Inserir=1;continue;}if(셋째순번=='a'){if(ÍNDICE_VALOR<finalizar_DESPRAZAMENTO(ÍNDICE_VALOR))ÍNDICE_VALOR=Seguinte_elemento(ÍNDICE_VALOR);Inserir=1;continue;}
        if(셋째순번=='I'){ÍNDICE_VALOR=Executar_2(ÍNDICE_VALOR);Inserir=1;continue;}if(셋째순번=='A'){ÍNDICE_VALOR=finalizar_DESPRAZAMENTO(ÍNDICE_VALOR);Inserir=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char liña_finalizar='\n';ÍNDICE_VALOR=셋째순번=='o'?finalizar_DESPRAZAMENTO(ÍNDICE_VALOR):Executar_2(ÍNDICE_VALOR);if(Anexar_VALOR(&liña_finalizar,1)){if(셋째순번=='O')ÍNDICE_VALOR--;Inserir=1;}continue;}
        if(셋째순번=='h'){ÍNDICE_VALOR=이전항목(ÍNDICE_VALOR);continue;}if(셋째순번=='l'){ÍNDICE_VALOR=Seguinte_elemento(ÍNDICE_VALOR);continue;}if(셋째순번=='j'){Vertical(1);continue;}if(셋째순번=='k'){Vertical(-1);continue;}
        if(셋째순번=='0'){ÍNDICE_VALOR=Executar_2(ÍNDICE_VALOR);continue;}if(셋째순번=='$'){ÍNDICE_VALOR=finalizar_DESPRAZAMENTO(ÍNDICE_VALOR);continue;}if(셋째순번=='G'){ÍNDICE_VALOR=Executar_2(duración_VALOR);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(ÍNDICE_VALOR<duración_VALOR)바이트지우기(ÍNDICE_VALOR,Seguinte_elemento(ÍNDICE_VALOR));continue;}
        if(셋째순번=='p'&&copiar_duración){ÍNDICE_VALOR=finalizar_DESPRAZAMENTO(ÍNDICE_VALOR);if(ÍNDICE_VALOR<duración_VALOR)ÍNDICE_VALOR++;Anexar_VALOR(복사자료,copiar_duración);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_capacidade;순번++){unsigned char SEGUNDO_VALOR=Texto[순번];Texto[순번]=desfacer_datos[순번];desfacer_datos[순번]=SEGUNDO_VALOR;}int elemento_CONTAR=duración_VALOR;duración_VALOR=desfacer_duración;desfacer_duración=elemento_CONTAR;elemento_CONTAR=ÍNDICE_VALOR;ÍNDICE_VALOR=위쪽;위쪽=elemento_CONTAR;elemento_CONTAR=변경됨;변경됨=desfacer_Modificacións;desfacer_Modificacións=elemento_CONTAR;continue;}
        if(셋째순번==':'||셋째순번=='/'){saír_apl_55b3a1cd=avisar(셋째순번);continue;}if(셋째순번=='n'){Busca_Seguinte();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
