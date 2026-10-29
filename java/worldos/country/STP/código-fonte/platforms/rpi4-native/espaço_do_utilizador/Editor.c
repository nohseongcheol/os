/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "Arquivo_ABI.h"
#define Editor_capacidade 16384
static unsigned char texto[Editor_capacidade],desfazer_dados[Editor_capacidade],복사자료[Editor_capacidade],RC_dados[1024];
static int duração_VALOR,ÍNDICE_VALOR,맨위,왼쪽,변경됨,Inserir,desfazer_duração,위쪽,desfazer_Alterações,되돌림있음,copiar_duração,사용량,COLS=68,LIN_CONT_NÚM=19;
static char Arquivo_entrada_nome[64],comando[128],PROCURAR_entrada[128];
static const char *aviso_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned Pendente_Chave;
static int ajuda_área,Estado_foto,Estado_Fila;
static void liberar(void){if(사용량){사용자호출(1,1,(uintptr_t)RC_dados,사용량,0,0,0);사용량=0;}}
static void byte_dados(unsigned ponto_de_código){if(Estado_foto){if((ponto_de_código&192)!=128){Estado_Fila+=ponto_de_código>=196?2:1;}if(Estado_Fila>=COLS)return;}if(사용량==(int)sizeof(RC_dados))liberar();RC_dados[사용량++]=ponto_de_código;}
static void 글내보내기(const char *cadeia_dados){while(*cadeia_dados)byte_dados((unsigned char)*cadeia_dados++);}
static void 수치(unsigned item_CONT_NÚM){char SEGUNDO_VALOR[12];int 순번=0;do{SEGUNDO_VALOR[순번++]='0'+item_CONT_NÚM%10;item_CONT_NÚM/=10;}while(item_CONT_NÚM);while(순번)byte_dados(SEGUNDO_VALOR[--순번]);}
static void mover_VALOR(int LIN_cargo,int COL_cargo){글내보내기("\033[");수치(LIN_cargo);byte_dados(';');수치(COL_cargo);byte_dados('H');}
static int Anterior(int dados_cargo){if(dados_cargo){dados_cargo--;while(dados_cargo>0&&(texto[dados_cargo]&192)==128)dados_cargo--;}return dados_cargo;}
static int Avançar_item(int dados_cargo){if(dados_cargo<duração_VALOR){dados_cargo++;while(dados_cargo<duração_VALOR&&(texto[dados_cargo]&192)==128)dados_cargo++;}return dados_cargo;}
static int iniciar(int dados_cargo){while(dados_cargo>0&&texto[dados_cargo-1]!='\n')dados_cargo--;return dados_cargo;}
static int encerrar_DESLOC(int dados_cargo){while(dados_cargo<duração_VALOR&&texto[dados_cargo]!='\n')dados_cargo++;return dados_cargo;}
static int 너비(unsigned ponto_de_código){return ponto_de_código>=196?2:1;}
static int COL(int dados_cargo){int ponto_de_código=0;for(int 순번=iniciar(dados_cargo);순번<dados_cargo;순번=Avançar_item(순번))ponto_de_código+=texto[순번]=='\t'?4-ponto_de_código%4:너비(texto[순번]);return ponto_de_código;}
static void ponto_de_verificação(void){for(int 순번=0;순번<duração_VALOR;순번++)desfazer_dados[순번]=texto[순번];desfazer_duração=duração_VALOR;위쪽=ÍNDICE_VALOR;desfazer_Alterações=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){ponto_de_verificação();for(int 순번=도착위치;순번<duração_VALOR;순번++)texto[출발위치+순번-도착위치]=texto[순번];duração_VALOR-=도착위치-출발위치;ÍNDICE_VALOR=출발위치;변경됨=1;}
static int Acrescentar_VALOR(const unsigned char *cadeia_dados,int item_CONT_NÚM){if(item_CONT_NÚM>Editor_capacidade-duração_VALOR){aviso_SMS="File full (16384 bytes)";return 0;}ponto_de_verificação();for(int 순번=duração_VALOR-1;순번>=ÍNDICE_VALOR;순번--)texto[순번+item_CONT_NÚM]=texto[순번];for(int 순번=0;순번<item_CONT_NÚM;순번++)texto[ÍNDICE_VALOR+순번]=cadeia_dados[순번];duração_VALOR+=item_CONT_NÚM;ÍNDICE_VALOR+=item_CONT_NÚM;변경됨=1;return 1;}
static void Vertical(int 차이){int COL_cargo=COL(ÍNDICE_VALOR),dados_cargo=iniciar(ÍNDICE_VALOR);if(차이<0){if(!dados_cargo)return;dados_cargo=iniciar(dados_cargo-1);}else{dados_cargo=encerrar_DESLOC(dados_cargo);if(dados_cargo==duração_VALOR)return;dados_cargo++;}int ponto_de_código=0;while(dados_cargo<duração_VALOR&&texto[dados_cargo]!='\n'&&ponto_de_código<COL_cargo){ponto_de_código+=texto[dados_cargo]=='\t'?4-ponto_de_código%4:너비(texto[dados_cargo]);dados_cargo=Avançar_item(dados_cargo);}ÍNDICE_VALOR=dados_cargo;}
static void emitir_tela(void){
    if(ÍNDICE_VALOR>duração_VALOR)ÍNDICE_VALOR=duração_VALOR;if(맨위>ÍNDICE_VALOR)맨위=iniciar(ÍNDICE_VALOR);맨위=iniciar(맨위);
    int LIN_cargo=0;for(int 순번=맨위;순번<ÍNDICE_VALOR;순번++)if(texto[순번]=='\n')LIN_cargo++;
    while(LIN_cargo>=LIN_CONT_NÚM-1){맨위=encerrar_DESLOC(맨위);if(맨위<duração_VALOR)맨위++;LIN_cargo--;}
    int COL_cargo=COL(ÍNDICE_VALOR);if(COL_cargo<왼쪽)왼쪽=COL_cargo;if(COL_cargo-왼쪽>=COLS-1)왼쪽=COL_cargo-COLS+2;
    글내보내기("\033[?25l");int dados_cargo=맨위;
    for(int 반환값=0;반환값<LIN_CONT_NÚM-1;반환값++){
        mover_VALOR(반환값+1,1);글내보내기("\033[0m\033[2K");int ponto_de_código=0,그려진상태=0;
        if(dados_cargo>=duração_VALOR&&반환값>LIN_cargo){글내보내기("\033[90m~\033[0m");continue;}
        while(dados_cargo<duração_VALOR&&texto[dados_cargo]!='\n'){
            int Avançar_DESLOC=Avançar_item(dados_cargo),너비값=texto[dados_cargo]=='\t'?4-ponto_de_código%4:너비(texto[dados_cargo]);
            if(ponto_de_código>=왼쪽&&ponto_de_código-왼쪽+너비값<COLS){
                if(texto[dados_cargo]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)byte_dados(' ');}else if(texto[dados_cargo]<32||texto[dados_cargo]==127){byte_dados('?');}else for(int 안쪽순번=dados_cargo;안쪽순번<Avançar_DESLOC;안쪽순번++)byte_dados(texto[안쪽순번]);그려진상태+=너비값;
            }ponto_de_código+=너비값;dados_cargo=Avançar_DESLOC;
        }
        (void)그려진상태;if(dados_cargo<duração_VALOR)dados_cargo++;
    }
    mover_VALOR(LIN_CONT_NÚM,1);글내보내기("\033[7m\033[2K");Estado_foto=1;Estado_Fila=0;글내보내기(Inserir?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Arquivo_entrada_nome[이름바이트수]&&이름바이트수<30)byte_dados(Arquivo_entrada_nome[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int linha_de_entrada=1;for(int 순번=0;순번<ÍNDICE_VALOR;순번++)if(texto[순번]=='\n')linha_de_entrada++;수치(linha_de_entrada);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(aviso_SMS){int item_CONT_NÚM=0;글내보내기(" | ");while(aviso_SMS[item_CONT_NÚM]&&item_CONT_NÚM<20)byte_dados(aviso_SMS[item_CONT_NÚM++]);}
    Estado_foto=0;글내보내기("\033[0m");mover_VALOR(LIN_cargo+1,COL_cargo-왼쪽+1);글내보내기("\033[?25h");liberar();
}
static int 누름값(void){
    if(Pendente_Chave){int 셋째순번=Pendente_Chave;Pendente_Chave=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Tamanho=사용자호출(16,3,0,0,0,0,0);
        if(COLS!=(int)(Tamanho&65535)||LIN_CONT_NÚM!=(int)(Tamanho>>16)){
            COLS=Tamanho&65535;LIN_CONT_NÚM=Tamanho>>16;emitir_tela();
            if(ajuda_área){mover_VALOR(LIN_CONT_NÚM,1);글내보내기("\033[0m\033[2K");byte_dados(ajuda_área);글내보내기(comando);liberar();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned em_dia_cargo=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-em_dia_cargo<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){Pendente_Chave=셋째순번;return 27;}
    int item_CONT_NÚM=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){item_CONT_NÚM=item_CONT_NÚM*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return item_CONT_NÚM==3?1007:item_CONT_NÚM==5?1008:item_CONT_NÚM==6?1009:item_CONT_NÚM==1?1005:item_CONT_NÚM==4?1006:27;return 27;}return 27;
}
static int Store_VALOR(void){
    int identificador_de_arquivo=abrir_Arquivo(Arquivo_entrada_nome,de_leitura_gravação|없으면만들기|cortar_Sumário,0600);if(identificador_de_arquivo<0){aviso_SMS="Cannot open for save";return 0;}
    intptr_t item_CONT_NÚM=gravar_Arquivo_dados(identificador_de_arquivo,texto,duração_VALOR);Close_Arquivo(identificador_de_arquivo);if(item_CONT_NÚM!=duração_VALOR){aviso_SMS="Write failed";return 0;}변경됨=0;aviso_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEGUNDO_VALOR){while(*첫째값&&*첫째값==*SEGUNDO_VALOR){첫째값++;SEGUNDO_VALOR++;}return *첫째값==*SEGUNDO_VALOR;}
static void PROCURAR_Avançar(void){int item_CONT_NÚM=0;while(PROCURAR_entrada[item_CONT_NÚM])item_CONT_NÚM++;if(!item_CONT_NÚM){aviso_SMS="No search pattern";return;}for(int 순번=1;순번<=duração_VALOR;순번++){int dados_cargo=(ÍNDICE_VALOR+순번)%(duração_VALOR?duração_VALOR:1),안쪽순번=0;while(안쪽순번<item_CONT_NÚM&&dados_cargo+안쪽순번<duração_VALOR&&texto[dados_cargo+안쪽순번]==(unsigned char)PROCURAR_entrada[안쪽순번])안쪽순번++;if(안쪽순번==item_CONT_NÚM){ÍNDICE_VALOR=dados_cargo;aviso_SMS="Match";return;}}aviso_SMS="Pattern not found";}
static int aviso_1dd14da4(int área_VALOR){
    int item_CONT_NÚM=0;comando[0]=0;
    for(;;){mover_VALOR(LIN_CONT_NÚM,1);글내보내기("\033[0m\033[2K");byte_dados(área_VALOR);글내보내기(comando);liberar();ajuda_área=área_VALOR;int 셋째순번=누름값();ajuda_área=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(item_CONT_NÚM){item_CONT_NÚM--;while(item_CONT_NÚM>0&&((unsigned char)comando[item_CONT_NÚM]&192)==128)item_CONT_NÚM--;comando[item_CONT_NÚM]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&item_CONT_NÚM<120){comando[item_CONT_NÚM++]=셋째순번;comando[item_CONT_NÚM]=0;}
    }
    if(área_VALOR=='/'){for(int 순번=0;순번<=item_CONT_NÚM;순번++)PROCURAR_entrada[순번]=comando[순번];PROCURAR_Avançar();return 0;}
    if(같은지(comando,"q!"))return 1;
    if(같은지(comando,"q")){if(!변경됨)return 1;aviso_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(comando,"wq")||같은지(comando,"x"))return Store_VALOR();
    if(같은지(comando,"w")){Store_VALOR();return 0;}
    if(comando[0]=='w'&&comando[1]==' '){int 순번=2;while(comando[순번]==' ')순번++;int Tamanho=item_CONT_NÚM-순번;if(Tamanho<1||Tamanho>63){aviso_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Tamanho;안쪽순번++)Arquivo_entrada_nome[안쪽순번]=comando[순번+안쪽순번];Arquivo_entrada_nome[Tamanho]=0;Store_VALOR();return 0;}
    int linha_de_entrada=0;for(int 순번=0;순번<item_CONT_NÚM;순번++){if(comando[순번]<'0'||comando[순번]>'9'){linha_de_entrada=0;break;}linha_de_entrada=linha_de_entrada*10+comando[순번]-'0';if(linha_de_entrada>16384){linha_de_entrada=0;break;}}
    if(linha_de_entrada){ÍNDICE_VALOR=0;while(--linha_de_entrada&&ÍNDICE_VALOR<duração_VALOR){ÍNDICE_VALOR=encerrar_DESLOC(ÍNDICE_VALOR);if(ÍNDICE_VALOR<duração_VALOR)ÍNDICE_VALOR++;}return 0;}
    aviso_SMS="Unknown vi command";return 0;
}
int START_usuário_app(int 무시값){
    (void)무시값;if(usuário_argumento_CONT_NÚM()!=1||usuário_argumento(0,Arquivo_entrada_nome,sizeof(Arquivo_entrada_nome))<0){글내보내기("Usage: vi FILE\n");liberar();return 2;}
    int identificador_de_arquivo=abrir_Arquivo(Arquivo_entrada_nome,somente_leitura_VALOR,0);
    if(identificador_de_arquivo>=0){int item_CONT_NÚM=tamanho_do_arquivo(identificador_de_arquivo);if(item_CONT_NÚM<0||item_CONT_NÚM>Editor_capacidade){Close_Arquivo(identificador_de_arquivo);return 1;}duração_VALOR=leitura_Arquivo_dados(identificador_de_arquivo,texto,item_CONT_NÚM);Close_Arquivo(identificador_de_arquivo);if(duração_VALOR!=item_CONT_NÚM)return 1;for(int 순번=0;순번<duração_VALOR;순번++)if(!texto[순번]){글내보내기("vi: NUL byte in text file\n");liberar();return 1;}}
    else if(número_do_erro!=2){글내보내기("vi: cannot read file\n");liberar();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");liberar();return 1;}COLS=흐린색&65535;LIN_CONT_NÚM=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");liberar();
    int entrelinhamento_bloco=0,encerrar_app=0;
    while(!encerrar_app){emitir_tela();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();aviso_SMS=0;
        if(셋째순번==1001){Vertical(-1);continue;}if(셋째순번==1002){Vertical(1);continue;}if(셋째순번==1003){ÍNDICE_VALOR=Avançar_item(ÍNDICE_VALOR);continue;}if(셋째순번==1004){ÍNDICE_VALOR=Anterior(ÍNDICE_VALOR);continue;}
        if(셋째순번==1005){ÍNDICE_VALOR=iniciar(ÍNDICE_VALOR);continue;}if(셋째순번==1006){ÍNDICE_VALOR=encerrar_DESLOC(ÍNDICE_VALOR);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<LIN_CONT_NÚM-2;순번++)Vertical(셋째순번==1008?-1:1);continue;}
        if(Inserir){
            if(셋째순번==27||셋째순번==3){Inserir=0;continue;}
            if(셋째순번==127||셋째순번==8){if(ÍNDICE_VALOR)바이트지우기(Anterior(ÍNDICE_VALOR),ÍNDICE_VALOR);continue;}
            if(셋째순번==1007){if(ÍNDICE_VALOR<duração_VALOR)바이트지우기(ÍNDICE_VALOR,Avançar_item(ÍNDICE_VALOR));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEGUNDO_VALOR[4];SEGUNDO_VALOR[0]=셋째순번;int item_CONT_NÚM=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!item_CONT_NÚM){aviso_SMS="Invalid UTF-8";continue;}int válido=1;for(int 순번=1;순번<item_CONT_NÚM;순번++){int ponto_de_código=누름값();if(ponto_de_código<128||ponto_de_código>191){Pendente_Chave=ponto_de_código;válido=0;break;}SEGUNDO_VALOR[순번]=ponto_de_código;}
                if(válido)Acrescentar_VALOR(SEGUNDO_VALOR,item_CONT_NÚM);
            }continue;
        }
        if(entrelinhamento_bloco){int dados_cargo=entrelinhamento_bloco;entrelinhamento_bloco=0;if(dados_cargo=='g'&&셋째순번=='g'){ÍNDICE_VALOR=0;continue;}if(dados_cargo=='Z'&&셋째순번=='Z'){encerrar_app=Store_VALOR();continue;}if((dados_cargo=='d'&&셋째순번=='d')||(dados_cargo=='y'&&셋째순번=='y')){int 첫째값=iniciar(ÍNDICE_VALOR),SEGUNDO_VALOR=encerrar_DESLOC(ÍNDICE_VALOR);if(SEGUNDO_VALOR<duração_VALOR)SEGUNDO_VALOR++;copiar_duração=SEGUNDO_VALOR-첫째값;for(int 순번=0;순번<copiar_duração;순번++)복사자료[순번]=texto[첫째값+순번];if(dados_cargo=='d')바이트지우기(첫째값,SEGUNDO_VALOR);continue;}}
        if(셋째순번=='i'){Inserir=1;continue;}if(셋째순번=='a'){if(ÍNDICE_VALOR<encerrar_DESLOC(ÍNDICE_VALOR))ÍNDICE_VALOR=Avançar_item(ÍNDICE_VALOR);Inserir=1;continue;}
        if(셋째순번=='I'){ÍNDICE_VALOR=iniciar(ÍNDICE_VALOR);Inserir=1;continue;}if(셋째순번=='A'){ÍNDICE_VALOR=encerrar_DESLOC(ÍNDICE_VALOR);Inserir=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linha_encerrar='\n';ÍNDICE_VALOR=셋째순번=='o'?encerrar_DESLOC(ÍNDICE_VALOR):iniciar(ÍNDICE_VALOR);if(Acrescentar_VALOR(&linha_encerrar,1)){if(셋째순번=='O')ÍNDICE_VALOR--;Inserir=1;}continue;}
        if(셋째순번=='h'){ÍNDICE_VALOR=Anterior(ÍNDICE_VALOR);continue;}if(셋째순번=='l'){ÍNDICE_VALOR=Avançar_item(ÍNDICE_VALOR);continue;}if(셋째순번=='j'){Vertical(1);continue;}if(셋째순번=='k'){Vertical(-1);continue;}
        if(셋째순번=='0'){ÍNDICE_VALOR=iniciar(ÍNDICE_VALOR);continue;}if(셋째순번=='$'){ÍNDICE_VALOR=encerrar_DESLOC(ÍNDICE_VALOR);continue;}if(셋째순번=='G'){ÍNDICE_VALOR=iniciar(duração_VALOR);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){entrelinhamento_bloco=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(ÍNDICE_VALOR<duração_VALOR)바이트지우기(ÍNDICE_VALOR,Avançar_item(ÍNDICE_VALOR));continue;}
        if(셋째순번=='p'&&copiar_duração){ÍNDICE_VALOR=encerrar_DESLOC(ÍNDICE_VALOR);if(ÍNDICE_VALOR<duração_VALOR)ÍNDICE_VALOR++;Acrescentar_VALOR(복사자료,copiar_duração);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Editor_capacidade;순번++){unsigned char SEGUNDO_VALOR=texto[순번];texto[순번]=desfazer_dados[순번];desfazer_dados[순번]=SEGUNDO_VALOR;}int item_CONT_NÚM=duração_VALOR;duração_VALOR=desfazer_duração;desfazer_duração=item_CONT_NÚM;item_CONT_NÚM=ÍNDICE_VALOR;ÍNDICE_VALOR=위쪽;위쪽=item_CONT_NÚM;item_CONT_NÚM=변경됨;변경됨=desfazer_Alterações;desfazer_Alterações=item_CONT_NÚM;continue;}
        if(셋째순번==':'||셋째순번=='/'){encerrar_app=aviso_1dd14da4(셋째순번);continue;}if(셋째순번=='n'){PROCURAR_Avançar();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");liberar();사용자호출(16,2,0,0,0,0,0);return 0;
}
