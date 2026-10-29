// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_dados kernel_VALOR 상태를 읽는 IPv4·ICMP·작업·Memória_VALOR·RAM repositório_raiz 관리 comando. */
public final class Sistema_ferramenta {
    static int email_VALOR;
    static boolean 같음(int ÍNDICE, String Word_SMS) { return InterpretadorComandos.같음(ÍNDICE, Word_SMS); }
    static int item_CONT_NÚM() { return InterpretadorComandos.token_CONT_NÚM; }
    static void falha_VALOR(String LEIAME_eb81d7d9) { InterpretadorComandos.resultado=2; 단말.Escrita(LEIAME_eb81d7d9); 단말.문자(10); }
    static void erro(int VALOR) { InterpretadorComandos.erro(VALOR); }
    static void número_entrada(String Nome, int VALOR) { 단말.Escrita(Nome); 단말.número(VALOR); 단말.문자(10); }
    static int dígito_VALOR(int ÍNDICE, int 한도) {
        if (ÍNDICE>=item_CONT_NÚM() || InterpretadorComandos.duração_VALOR[ÍNDICE]==0) return -1;
        int VALOR=0;
        for (int 순번=0; 순번<InterpretadorComandos.duração_VALOR[ÍNDICE]; 순번++) {
            int caractere_VALOR=InterpretadorComandos.token_VALOR[InterpretadorComandos.시작점[ÍNDICE]+순번]-'0';
            if (caractere_VALOR<0 || caractere_VALOR>9 || VALOR>(한도-caractere_VALOR)/10) return -1;
            VALOR=VALOR*10+caractere_VALOR;
        }
        return VALOR<=한도?VALOR:-1;
    }
    static boolean leitura_email(int ÍNDICE) {
        if (ÍNDICE>=item_CONT_NÚM()) return false;
        int VALOR=0, parte_VALOR=0, dígito_CONT_NÚM=0, ponto_CONT_NÚM=0;
        for (int 순번=0; 순번<InterpretadorComandos.duração_VALOR[ÍNDICE]; 순번++) {
            int caractere_VALOR=InterpretadorComandos.token_VALOR[InterpretadorComandos.시작점[ÍNDICE]+순번];
            if (caractere_VALOR=='.') { if (dígito_CONT_NÚM==0 || ++ponto_CONT_NÚM>3) return false; VALOR=(VALOR<<8)|parte_VALOR; parte_VALOR=dígito_CONT_NÚM=0; }
            else { if (caractere_VALOR<'0' || caractere_VALOR>'9' || ++dígito_CONT_NÚM>3) return false; parte_VALOR=parte_VALOR*10+caractere_VALOR-'0'; if(parte_VALOR>255)return false; }
        }
        if (ponto_CONT_NÚM!=3 || dígito_CONT_NÚM==0) return false;
        email_VALOR=(VALOR<<8)|parte_VALOR; return true;
    }
    static void gravar_email(int VALOR) {
        단말.número((VALOR>>>24)&255); 단말.문자('.'); 단말.número((VALOR>>>16)&255); 단말.문자('.');
        단말.número((VALOR>>>8)&255); 단말.문자('.'); 단말.número(VALOR&255);
    }
    static void mostrar_rede_Status() {
        단말.Escrita(Quadro.rede_Status(20,0)!=0?"en0: ":"sl0: "); 단말.Escrita(Quadro.rede_Status(3,0)!=0?"UP":"DOWN");
        단말.Escrita(Quadro.rede_Status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Escrita(Quadro.rede_Status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); gravar_email(Quadro.rede_Status(0,0));
        단말.Escrita(" netmask "); gravar_email(Quadro.rede_Status(1,0)); 단말.Escrita(" gateway "); gravar_email(Quadro.rede_Status(2,0)); 단말.문자(10);
        단말.Escrita("  RX packets "); 단말.número(Quadro.rede_Status(4,0)); 단말.Escrita(" bytes "); 단말.número(Quadro.rede_Status(6,0));
        단말.Escrita(" TX packets "); 단말.número(Quadro.rede_Status(5,0)); 단말.Escrita(" bytes "); 단말.número(Quadro.rede_Status(7,0)); 단말.문자(10);
        número_entrada("  dropped ",Quadro.rede_Status(8,0));
    }
    static void set_email(int iniciar) {
        if (item_CONT_NÚM()!=iniciar+3 || !leitura_email(iniciar)) { falha_VALOR("사용법: ipconfig set Endereço 주소가림 gateway_VALOR"); return; }
        int Endereço=email_VALOR;
        if(!leitura_email(iniciar+1)){falha_VALOR("Invalid IPv4 netmask");return;} int máscara_VALOR=email_VALOR;
        if(!leitura_email(iniciar+2)){falha_VALOR("Invalid IPv4 gateway");return;}
        int resultado=Quadro.rede_Configurações(0,Endereço,máscara_VALOR,email_VALOR);
        if(resultado<0) { erro(resultado); if(resultado==-16)단말.Escrita("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Escrita("IPv4 configuration applied (until reboot)\n"); mostrar_rede_Status(); }
    }
    static void rede_comando(boolean endereço_IP) {
        if (item_CONT_NÚM()==1 || item_CONT_NÚM()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || item_CONT_NÚM()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { mostrar_rede_Status();return; }
        if (endereço_IP && 같음(1,"route") && (item_CONT_NÚM()==2 || item_CONT_NÚM()==3&&같음(2,"show"))) { mostrar_caminho();return; }
        if (같음(1,"set")) { set_email(2);return; }
        if (item_CONT_NÚM()==2 && (같음(1,"up") || 같음(1,"down"))) { Quadro.rede_Configurações(같음(1,"up")?1:2,0,0,0);mostrar_rede_Status();return; }
        if (endereço_IP && item_CONT_NÚM()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Quadro.rede_Configurações(같음(5,"up")?1:2,0,0,0);mostrar_rede_Status();return; }
        falha_VALOR("사용법: ip [addr show|route show|set Endereço 주소가림 gateway_VALOR|link set dev sl0 up|down]");
    }
    static void mostrar_caminho() {
        단말.Escrita("Destination Netmask Gateway Interface\n");
        gravar_email(Quadro.rede_Status(0,0)&Quadro.rede_Status(1,0));단말.문자(' ');gravar_email(Quadro.rede_Status(1,0));단말.Escrita(Quadro.rede_Status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Quadro.rede_Status(2,0)!=0) {단말.Escrita("0.0.0.0 0.0.0.0 ");gravar_email(Quadro.rede_Status(2,0));단말.Escrita(Quadro.rede_Status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void mostrar_rede() {
        단말.Escrita("Proto Local Remote State Queued\n");
        for(int ÍNDICE=0;ÍNDICE<32;ÍNDICE++) {
            int TIPO_área=Quadro.rede_Status(10,ÍNDICE);if(TIPO_área==0)continue;
            단말.Escrita(TIPO_área==1?"TCP ":"UDP ");gravar_email(Quadro.rede_Status(16,ÍNDICE));단말.문자(':');단말.número(Quadro.rede_Status(11,ÍNDICE));단말.문자(' ');
            gravar_email(Quadro.rede_Status(12,ÍNDICE));단말.문자(':');단말.número(Quadro.rede_Status(13,ÍNDICE));단말.문자(' ');
            int Estado_VALOR=Quadro.rede_Status(14,ÍNDICE);단말.Escrita(TIPO_área==2?"DATAGRAM":Estado_VALOR==1?"LISTEN":Estado_VALOR==2?"ESTABLISHED":Estado_VALOR==3?"CLOSE_WAIT":Estado_VALOR==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.número(Quadro.rede_Status(15,ÍNDICE));단말.문자(10);
        }
        단말.Escrita("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean estado_de_espera(int 밀리초) {
        int iniciar=Quadro.밀리초();
        while(Quadro.밀리초()-iniciar<밀리초) {
            if(셸입출력.TI_interativo()!=0){int caractere_VALOR=Quadro.직렬읽기();if(caractere_VALOR==3 || caractere_VALOR=='q' || caractere_VALOR=='Q' || caractere_VALOR==27 || caractere_VALOR==-4096)return false;}
            Quadro.LUCRO_CPU();
        }
        return true;
    }
    static void teste_réplica() {
        int repetição_CONT_NÚM=4, 제한=1000, meta=-1;
        for(int cargo_ÍNDICE=1;cargo_ÍNDICE<item_CONT_NÚM();cargo_ÍNDICE++) {
            if(같음(cargo_ÍNDICE,"-c")){repetição_CONT_NÚM=dígito_VALOR(++cargo_ÍNDICE,100);if(repetição_CONT_NÚM<1){falha_VALOR("ping: -c 1..100");return;}}
            else if(같음(cargo_ÍNDICE,"-W")){제한=dígito_VALOR(++cargo_ÍNDICE,10);if(제한<1){falha_VALOR("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(meta<0)meta=cargo_ÍNDICE;else{falha_VALOR("사용법: ping [-c repetição_CONT_NÚM] [-W 초] IPv4");return;}
        }
        if(meta<0 || !leitura_email(meta)){falha_VALOR("ping: an IPv4 address is required (DNS is not configured)");return;}
        int Endereço=email_VALOR, 보낸수=0, RECEBER_CONT_NÚM=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Escrita("PING ");gravar_email(Endereço);단말.Escrita(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ordem_VALOR=1;ordem_VALOR<=repetição_CONT_NÚM && 계속;ordem_VALOR++) {
            int 처리값=Quadro.enviar_réplica(Endereço,ordem_VALOR);
            if(처리값<0){erro(처리값);break;}보낸수++;
            int iniciar=Quadro.밀리초();
            while(Quadro.leitura_réplica(0)==-11 && Quadro.밀리초()-iniciar<제한)if(!estado_de_espera(1)){계속=false;break;}
            if(!계속)break;
            if(Quadro.leitura_réplica(0)==0){
                int valor_temporal=Quadro.leitura_réplica(1);RECEBER_CONT_NÚM++;누적+=valor_temporal;if(valor_temporal<최솟값)최솟값=valor_temporal;if(valor_temporal>최댓값)최댓값=valor_temporal;
                단말.Escrita("32 bytes from ");gravar_email(Endereço);단말.Escrita(" seq=");단말.número(ordem_VALOR);단말.Escrita(" ttl=");단말.número(Quadro.leitura_réplica(2));단말.Escrita(" time=");단말.número(valor_temporal);단말.Escrita(" ms\n");
            }else{단말.Escrita("Request timeout seq=");단말.número(ordem_VALOR);단말.문자(10);}
            if(ordem_VALOR<repetição_CONT_NÚM)계속=estado_de_espera(200);
        }
        단말.número(보낸수);단말.Escrita(" transmitted, ");단말.número(RECEBER_CONT_NÚM);단말.Escrita(" received, ");단말.número(보낸수==0?100:(보낸수-RECEBER_CONT_NÚM)*100/보낸수);단말.Escrita("% packet loss\n");
        if(RECEBER_CONT_NÚM>0){단말.Escrita("rtt min/avg/max = ");단말.número(최솟값);단말.문자('/');단말.número(누적/RECEBER_CONT_NÚM);단말.문자('/');단말.número(최댓값);단말.Escrita(" ms\n");}
        InterpretadorComandos.resultado=계속?(RECEBER_CONT_NÚM==0?1:0):130;
    }
    static void mostrar_Atividade() { 단말.Escrita("up ");단말.número(Quadro.밀리초()/1000);단말.Escrita(" seconds\n"); }
    static void mostrar_Memória() {
        número_entrada("ARM RAM KiB (firmware): ",Quadro.consulta_Sistema(0,0));
        número_entrada("Kernel image+BSS+stack KiB: ",Quadro.consulta_Sistema(1,0));
        int total_capacidade=Quadro.consulta_Sistema(2,0), 사용량=Quadro.consulta_Sistema(3,0);
        단말.Escrita("AOT heap KiB total/used/free: ");단말.número(total_capacidade);단말.문자('/');단말.número(사용량);단말.문자('/');단말.número(total_capacidade-사용량);단말.문자(10);
        número_entrada("Framebuffer KiB: ",Quadro.consulta_Sistema(4,0));
        número_entrada("EL0 arena+session reserve KiB: ",Quadro.consulta_Sistema(5,0));
        int 매핑=0;for(int ÍNDICE=0;ÍNDICE<4;ÍNDICE++)매핑+=Quadro.consulta_Sistema(22,ÍNDICE);
        número_entrada("EL0 mapped KiB: ",매핑);
        단말.Escrita("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void mostrar_Tasks() {
        단말.Escrita("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Escrita("1 - RUN - - ");단말.número(Quadro.밀리초());단말.Escrita(" kernel/shell\n");
        for(int ÍNDICE=1;ÍNDICE<3;ÍNDICE++)if(Quadro.Tarefa_Estado(ÍNDICE)>0){단말.número(ÍNDICE+1);단말.Escrita(" - READY 64 - - kernel-task\n");}
        for(int ÍNDICE=0;ÍNDICE<4;ÍNDICE++){
            int Estado_VALOR=Quadro.consulta_Sistema(20,ÍNDICE);if(Estado_VALOR==0)continue;
            단말.número(Quadro.consulta_Sistema(21,ÍNDICE));단말.문자(' ');단말.número(ÍNDICE);단말.Escrita(Estado_VALOR==1?" RUN ":" SUSPENDED ");
            단말.número(Quadro.consulta_Sistema(22,ÍNDICE));단말.문자(' ');단말.número(Quadro.consulta_Sistema(24,ÍNDICE));단말.문자(' ');단말.número(Quadro.consulta_Sistema(23,ÍNDICE));단말.문자(' ');
            for(int cargo_ÍNDICE=0;cargo_ÍNDICE<288;cargo_ÍNDICE++){int byte_VALOR=Quadro.consulta_Sistema(25,ÍNDICE+cargo_ÍNDICE*4);if(byte_VALOR==0)break;Quadro.직렬쓰기(byte_VALOR);}단말.문자(10);
        }
    }
    static void mostrar_Armazenamento() {
        int slot_CONT_NÚM=0, dados_CONT_NÚM=0;
        for(int ÍNDICE=0;ÍNDICE<FicheirosMemória.Arquivo_CONT_NÚM;ÍNDICE++)if(FicheirosMemória.이름길이[ÍNDICE]>0 || FicheirosMemória.Referência_CONT_NÚM[ÍNDICE]>0){slot_CONT_NÚM++;dados_CONT_NÚM+=FicheirosMemória.duração_VALOR[ÍNDICE];}
        단말.Escrita("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.número(FicheirosMemória.Arquivo_CONT_NÚM*16384);단말.문자(' ');단말.número(slot_CONT_NÚM*16384);단말.문자(' ');단말.número((FicheirosMemória.Arquivo_CONT_NÚM-slot_CONT_NÚM)*16384);단말.문자(' ');단말.número(dados_CONT_NÚM);단말.문자(' ');단말.número(slot_CONT_NÚM);단말.문자('/');단말.número(FicheirosMemória.Arquivo_CONT_NÚM);단말.Escrita(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void mostrar_Status() {
        int repetição_CONT_NÚM=셸입출력.TI_interativo()!=0?0:1;
        if(item_CONT_NÚM()>1){if(item_CONT_NÚM()!=3 || !같음(1,"-n") || (repetição_CONT_NÚM=dígito_VALOR(2,1000))<1){falha_VALOR("사용법: top [-n 1..1000]; q/Ctrl+C로 encerrar_app");return;}}
        for(int SEQUÊNCIA_VALOR=0;repetição_CONT_NÚM==0 || SEQUÊNCIA_VALOR<repetição_CONT_NÚM;SEQUÊNCIA_VALOR++){
            if(셸입출력.TI_interativo()!=0 && repetição_CONT_NÚM==0)단말.Escrita("\u001b[2J\u001b[H");
            mostrar_Atividade();mostrar_Memória();mostrar_Tasks();
            if(repetição_CONT_NÚM!=0 && SEQUÊNCIA_VALOR+1>=repetição_CONT_NÚM)break;
            if(!estado_de_espera(1000))break;
        }
    }
    static String padrão_Word(int ÍNDICE) {
        if(ÍNDICE==0)return "ipconfig";if(ÍNDICE==1)return "ip";if(ÍNDICE==2)return "ping";if(ÍNDICE==3)return "route";if(ÍNDICE==4)return "netstat";
        if(ÍNDICE==5)return "ps";if(ÍNDICE==6)return "top";if(ÍNDICE==7)return "free";if(ÍNDICE==8)return "df";if(ÍNDICE==9)return "uptime";if(ÍNDICE==10)return "poweroff";return "help";
    }
    static void mostrar_ajuda() {
        단말.Escrita("--- Network / system commands ---\n");
        for(int ÍNDICE=0;ÍNDICE<12;ÍNDICE++){단말.Escrita(padrão_Word(ÍNDICE));단말.Escrita(" / ");단말.Escrita(관리명령.Word_SMS(ÍNDICE));단말.Escrita(" : ");단말.Escrita(관리명령.설명(ÍNDICE));단말.문자(10);}
        단말.Escrita("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Escrita("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Escrita("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Executar_comando() {
        int comando=-1;
        for(int ÍNDICE=0;ÍNDICE<12;ÍNDICE++)if(같음(0,padrão_Word(ÍNDICE)) || 같음(0,관리명령.Word_SMS(ÍNDICE)))comando=ÍNDICE;
        if(같음(0,"ifconfig"))comando=0;if(같음(0,"ss"))comando=4;
        if(comando<0)return false;
        if(comando==11){if(같음(1,"net") || 같음(1,"system"))mostrar_ajuda();else if(같음(1,"ko") || 같음(1,"input"))InterpretadorComandos.한글도움말();else InterpretadorComandos.mostrar_ajuda();return true;}
        if(comando==0 || comando==1)rede_comando(comando==1);
        else if(comando==2)teste_réplica();
        else if(comando==6)mostrar_Status();
        else if(item_CONT_NÚM()!=1){falha_VALOR("This command takes no arguments; help system");}
        else if(comando==3)mostrar_caminho();else if(comando==4)mostrar_rede();else if(comando==5)mostrar_Tasks();else if(comando==7)mostrar_Memória();else if(comando==8)mostrar_Armazenamento();else if(comando==9)mostrar_Atividade();
        else if(comando==10)Quadro.전원끄기();
        return true;
    }
}
