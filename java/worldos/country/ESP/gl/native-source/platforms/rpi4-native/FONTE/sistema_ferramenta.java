// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_datos kernel_VALOR 상태를 읽는 IPv4·ICMP·작업·Memoria_VALOR·RAM repositorio_raíz 관리 Orde. */
public final class sistema_ferramenta {
    static int ENDEREZO_VALOR;
    static boolean 같음(int ÍNDICE, String Word_SMS) { return 명령해석기.같음(ÍNDICE, Word_SMS); }
    static int elemento_CONTAR() { return 명령해석기.ficha_CONTAR; }
    static void erro_VALOR(String Léame_eb81d7d9) { 명령해석기.RESULTANTE=2; 단말.Escritura(Léame_eb81d7d9); 단말.문자(10); }
    static void ERRO(int VALOR) { 명령해석기.ERRO(VALOR); }
    static void 수항목(String Nome, int VALOR) { 단말.Escritura(Nome); 단말.수(VALOR); 단말.문자(10); }
    static int díxito_VALOR(int ÍNDICE, int 한도) {
        if (ÍNDICE>=elemento_CONTAR() || 명령해석기.duración_VALOR[ÍNDICE]==0) return -1;
        int VALOR=0;
        for (int 순번=0; 순번<명령해석기.duración_VALOR[ÍNDICE]; 순번++) {
            int carácter_VALOR=명령해석기.ficha_VALOR[명령해석기.시작점[ÍNDICE]+순번]-'0';
            if (carácter_VALOR<0 || carácter_VALOR>9 || VALOR>(한도-carácter_VALOR)/10) return -1;
            VALOR=VALOR*10+carácter_VALOR;
        }
        return VALOR<=한도?VALOR:-1;
    }
    static boolean 주소읽기(int ÍNDICE) {
        if (ÍNDICE>=elemento_CONTAR()) return false;
        int VALOR=0, 덩이=0, díxito_CONTAR=0, p_CONTAR=0;
        for (int 순번=0; 순번<명령해석기.duración_VALOR[ÍNDICE]; 순번++) {
            int carácter_VALOR=명령해석기.ficha_VALOR[명령해석기.시작점[ÍNDICE]+순번];
            if (carácter_VALOR=='.') { if (díxito_CONTAR==0 || ++p_CONTAR>3) return false; VALOR=(VALOR<<8)|덩이; 덩이=díxito_CONTAR=0; }
            else { if (carácter_VALOR<'0' || carácter_VALOR>'9' || ++díxito_CONTAR>3) return false; 덩이=덩이*10+carácter_VALOR-'0'; if(덩이>255)return false; }
        }
        if (p_CONTAR!=3 || díxito_CONTAR==0) return false;
        ENDEREZO_VALOR=(VALOR<<8)|덩이; return true;
    }
    static void escribir_ENDEREZO(int VALOR) {
        단말.수((VALOR>>>24)&255); 단말.문자('.'); 단말.수((VALOR>>>16)&255); 단말.문자('.');
        단말.수((VALOR>>>8)&255); 단말.문자('.'); 단말.수(VALOR&255);
    }
    static void mostrar_Rede_estado() {
        단말.Escritura(Panel.Rede_estado(20,0)!=0?"en0: ":"sl0: "); 단말.Escritura(Panel.Rede_estado(3,0)!=0?"UP":"DOWN");
        단말.Escritura(Panel.Rede_estado(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Escritura(Panel.Rede_estado(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); escribir_ENDEREZO(Panel.Rede_estado(0,0));
        단말.Escritura(" netmask "); escribir_ENDEREZO(Panel.Rede_estado(1,0)); 단말.Escritura(" gateway "); escribir_ENDEREZO(Panel.Rede_estado(2,0)); 단말.문자(10);
        단말.Escritura("  RX packets "); 단말.수(Panel.Rede_estado(4,0)); 단말.Escritura(" bytes "); 단말.수(Panel.Rede_estado(6,0));
        단말.Escritura(" TX packets "); 단말.수(Panel.Rede_estado(5,0)); 단말.Escritura(" bytes "); 단말.수(Panel.Rede_estado(7,0)); 단말.문자(10);
        수항목("  dropped ",Panel.Rede_estado(8,0));
    }
    static void conxunto_ENDEREZO(int Executar_2) {
        if (elemento_CONTAR()!=Executar_2+3 || !주소읽기(Executar_2)) { erro_VALOR("사용법: ipconfig set ENDEREZO 주소가림 pasarela_VALOR"); return; }
        int ENDEREZO=ENDEREZO_VALOR;
        if(!주소읽기(Executar_2+1)){erro_VALOR("Invalid IPv4 netmask");return;} int máscara_VALOR=ENDEREZO_VALOR;
        if(!주소읽기(Executar_2+2)){erro_VALOR("Invalid IPv4 gateway");return;}
        int RESULTANTE=Panel.Rede_Configuración(0,ENDEREZO,máscara_VALOR,ENDEREZO_VALOR);
        if(RESULTANTE<0) { ERRO(RESULTANTE); if(RESULTANTE==-16)단말.Escritura("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Escritura("IPv4 configuration applied (until reboot)\n"); mostrar_Rede_estado(); }
    }
    static void Rede_comando(boolean enderezo_IP) {
        if (elemento_CONTAR()==1 || elemento_CONTAR()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || elemento_CONTAR()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { mostrar_Rede_estado();return; }
        if (enderezo_IP && 같음(1,"route") && (elemento_CONTAR()==2 || elemento_CONTAR()==3&&같음(2,"show"))) { mostrar_camiño();return; }
        if (같음(1,"set")) { conxunto_ENDEREZO(2);return; }
        if (elemento_CONTAR()==2 && (같음(1,"up") || 같음(1,"down"))) { Panel.Rede_Configuración(같음(1,"up")?1:2,0,0,0);mostrar_Rede_estado();return; }
        if (enderezo_IP && elemento_CONTAR()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Panel.Rede_Configuración(같음(5,"up")?1:2,0,0,0);mostrar_Rede_estado();return; }
        erro_VALOR("사용법: ip [addr show|route show|set ENDEREZO 주소가림 pasarela_VALOR|link set dev sl0 up|down]");
    }
    static void mostrar_camiño() {
        단말.Escritura("Destination Netmask Gateway Interface\n");
        escribir_ENDEREZO(Panel.Rede_estado(0,0)&Panel.Rede_estado(1,0));단말.문자(' ');escribir_ENDEREZO(Panel.Rede_estado(1,0));단말.Escritura(Panel.Rede_estado(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Panel.Rede_estado(2,0)!=0) {단말.Escritura("0.0.0.0 0.0.0.0 ");escribir_ENDEREZO(Panel.Rede_estado(2,0));단말.Escritura(Panel.Rede_estado(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void mostrar_Rede() {
        단말.Escritura("Proto Local Remote State Queued\n");
        for(int ÍNDICE=0;ÍNDICE<32;ÍNDICE++) {
            int TIPO_Categoría=Panel.Rede_estado(10,ÍNDICE);if(TIPO_Categoría==0)continue;
            단말.Escritura(TIPO_Categoría==1?"TCP ":"UDP ");escribir_ENDEREZO(Panel.Rede_estado(16,ÍNDICE));단말.문자(':');단말.수(Panel.Rede_estado(11,ÍNDICE));단말.문자(' ');
            escribir_ENDEREZO(Panel.Rede_estado(12,ÍNDICE));단말.문자(':');단말.수(Panel.Rede_estado(13,ÍNDICE));단말.문자(' ');
            int Estado_VALOR=Panel.Rede_estado(14,ÍNDICE);단말.Escritura(TIPO_Categoría==2?"DATAGRAM":Estado_VALOR==1?"LISTEN":Estado_VALOR==2?"ESTABLISHED":Estado_VALOR==3?"CLOSE_WAIT":Estado_VALOR==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Panel.Rede_estado(15,ÍNDICE));단말.문자(10);
        }
        단말.Escritura("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean agarda_Estado(int 밀리초) {
        int Executar_2=Panel.밀리초();
        while(Panel.밀리초()-Executar_2<밀리초) {
            if(셸입출력.Tecnoloxía_da_información_TI_interactivo()!=0){int carácter_VALOR=Panel.직렬읽기();if(carácter_VALOR==3 || carácter_VALOR=='q' || carácter_VALOR=='Q' || carácter_VALOR==27 || carácter_VALOR==-4096)return false;}
            Panel.suspender_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, obxectivo_VALOR=-1;
        for(int cargo_ÍNDICE=1;cargo_ÍNDICE<elemento_CONTAR();cargo_ÍNDICE++) {
            if(같음(cargo_ÍNDICE,"-c")){횟수=díxito_VALOR(++cargo_ÍNDICE,100);if(횟수<1){erro_VALOR("ping: -c 1..100");return;}}
            else if(같음(cargo_ÍNDICE,"-W")){제한=díxito_VALOR(++cargo_ÍNDICE,10);if(제한<1){erro_VALOR("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(obxectivo_VALOR<0)obxectivo_VALOR=cargo_ÍNDICE;else{erro_VALOR("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(obxectivo_VALOR<0 || !주소읽기(obxectivo_VALOR)){erro_VALOR("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ENDEREZO=ENDEREZO_VALOR, 보낸수=0, RECIBIDO_CONTAR=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Escritura("PING ");escribir_ENDEREZO(ENDEREZO);단말.Escritura(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int orde_VALOR=1;orde_VALOR<=횟수 && 계속;orde_VALOR++) {
            int 처리값=Panel.enviar_resposta(ENDEREZO,orde_VALOR);
            if(처리값<0){ERRO(처리값);break;}보낸수++;
            int Executar_2=Panel.밀리초();
            while(Panel.응답읽기(0)==-11 && Panel.밀리초()-Executar_2<제한)if(!agarda_Estado(1)){계속=false;break;}
            if(!계속)break;
            if(Panel.응답읽기(0)==0){
                int hora_VALOR=Panel.응답읽기(1);RECIBIDO_CONTAR++;누적+=hora_VALOR;if(hora_VALOR<최솟값)최솟값=hora_VALOR;if(hora_VALOR>최댓값)최댓값=hora_VALOR;
                단말.Escritura("32 bytes from ");escribir_ENDEREZO(ENDEREZO);단말.Escritura(" seq=");단말.수(orde_VALOR);단말.Escritura(" ttl=");단말.수(Panel.응답읽기(2));단말.Escritura(" time=");단말.수(hora_VALOR);단말.Escritura(" ms\n");
            }else{단말.Escritura("Request timeout seq=");단말.수(orde_VALOR);단말.문자(10);}
            if(orde_VALOR<횟수)계속=agarda_Estado(200);
        }
        단말.수(보낸수);단말.Escritura(" transmitted, ");단말.수(RECIBIDO_CONTAR);단말.Escritura(" received, ");단말.수(보낸수==0?100:(보낸수-RECIBIDO_CONTAR)*100/보낸수);단말.Escritura("% packet loss\n");
        if(RECIBIDO_CONTAR>0){단말.Escritura("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECIBIDO_CONTAR);단말.문자('/');단말.수(최댓값);단말.Escritura(" ms\n");}
        명령해석기.RESULTANTE=계속?(RECIBIDO_CONTAR==0?1:0):130;
    }
    static void mostrar_Actividade() { 단말.Escritura("up ");단말.수(Panel.밀리초()/1000);단말.Escritura(" seconds\n"); }
    static void mostrar_Memoria() {
        수항목("ARM RAM KiB (firmware): ",Panel.consulta_sistema(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Panel.consulta_sistema(1,0));
        int 총량=Panel.consulta_sistema(2,0), 사용량=Panel.consulta_sistema(3,0);
        단말.Escritura("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Panel.consulta_sistema(4,0));
        수항목("EL0 arena+session reserve KiB: ",Panel.consulta_sistema(5,0));
        int 매핑=0;for(int ÍNDICE=0;ÍNDICE<4;ÍNDICE++)매핑+=Panel.consulta_sistema(22,ÍNDICE);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Escritura("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void mostrar_Tasks() {
        단말.Escritura("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Escritura("1 - RUN - - ");단말.수(Panel.밀리초());단말.Escritura(" kernel/shell\n");
        for(int ÍNDICE=1;ÍNDICE<3;ÍNDICE++)if(Panel.tarefa_Estado(ÍNDICE)>0){단말.수(ÍNDICE+1);단말.Escritura(" - READY 64 - - kernel-task\n");}
        for(int ÍNDICE=0;ÍNDICE<4;ÍNDICE++){
            int Estado_VALOR=Panel.consulta_sistema(20,ÍNDICE);if(Estado_VALOR==0)continue;
            단말.수(Panel.consulta_sistema(21,ÍNDICE));단말.문자(' ');단말.수(ÍNDICE);단말.Escritura(Estado_VALOR==1?" RUN ":" SUSPENDED ");
            단말.수(Panel.consulta_sistema(22,ÍNDICE));단말.문자(' ');단말.수(Panel.consulta_sistema(24,ÍNDICE));단말.문자(' ');단말.수(Panel.consulta_sistema(23,ÍNDICE));단말.문자(' ');
            for(int cargo_ÍNDICE=0;cargo_ÍNDICE<288;cargo_ÍNDICE++){int byte_VALOR=Panel.consulta_sistema(25,ÍNDICE+cargo_ÍNDICE*4);if(byte_VALOR==0)break;Panel.직렬쓰기(byte_VALOR);}단말.문자(10);
        }
    }
    static void mostrar_Almacenamento() {
        int 칸수=0, datos_CONTAR=0;
        for(int ÍNDICE=0;ÍNDICE<Memoria_Ficheiros.Ficheiro_CONTAR;ÍNDICE++)if(Memoria_Ficheiros.이름길이[ÍNDICE]>0 || Memoria_Ficheiros.Material_de_referencia_CONTAR[ÍNDICE]>0){칸수++;datos_CONTAR+=Memoria_Ficheiros.duración_VALOR[ÍNDICE];}
        단말.Escritura("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memoria_Ficheiros.Ficheiro_CONTAR*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((Memoria_Ficheiros.Ficheiro_CONTAR-칸수)*16384);단말.문자(' ');단말.수(datos_CONTAR);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(Memoria_Ficheiros.Ficheiro_CONTAR);단말.Escritura(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void mostrar_estado() {
        int 횟수=셸입출력.Tecnoloxía_da_información_TI_interactivo()!=0?0:1;
        if(elemento_CONTAR()>1){if(elemento_CONTAR()!=3 || !같음(1,"-n") || (횟수=díxito_VALOR(2,1000))<1){erro_VALOR("사용법: top [-n 1..1000]; q/Ctrl+C로 saír_apl_55b3a1cd");return;}}
        for(int SECUENCIA_VALOR=0;횟수==0 || SECUENCIA_VALOR<횟수;SECUENCIA_VALOR++){
            if(셸입출력.Tecnoloxía_da_información_TI_interactivo()!=0 && 횟수==0)단말.Escritura("\u001b[2J\u001b[H");
            mostrar_Actividade();mostrar_Memoria();mostrar_Tasks();
            if(횟수!=0 && SECUENCIA_VALOR+1>=횟수)break;
            if(!agarda_Estado(1000))break;
        }
    }
    static String 표준말(int ÍNDICE) {
        if(ÍNDICE==0)return "ipconfig";if(ÍNDICE==1)return "ip";if(ÍNDICE==2)return "ping";if(ÍNDICE==3)return "route";if(ÍNDICE==4)return "netstat";
        if(ÍNDICE==5)return "ps";if(ÍNDICE==6)return "top";if(ÍNDICE==7)return "free";if(ÍNDICE==8)return "df";if(ÍNDICE==9)return "uptime";if(ÍNDICE==10)return "poweroff";return "help";
    }
    static void mostrar_axuda() {
        단말.Escritura("--- Network / system commands ---\n");
        for(int ÍNDICE=0;ÍNDICE<12;ÍNDICE++){단말.Escritura(표준말(ÍNDICE));단말.Escritura(" / ");단말.Escritura(관리명령.Word_SMS(ÍNDICE));단말.Escritura(" : ");단말.Escritura(관리명령.설명(ÍNDICE));단말.문자(10);}
        단말.Escritura("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Escritura("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Escritura("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean executar_comando() {
        int Orde=-1;
        for(int ÍNDICE=0;ÍNDICE<12;ÍNDICE++)if(같음(0,표준말(ÍNDICE)) || 같음(0,관리명령.Word_SMS(ÍNDICE)))Orde=ÍNDICE;
        if(같음(0,"ifconfig"))Orde=0;if(같음(0,"ss"))Orde=4;
        if(Orde<0)return false;
        if(Orde==11){if(같음(1,"net") || 같음(1,"system"))mostrar_axuda();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.mostrar_axuda();return true;}
        if(Orde==0 || Orde==1)Rede_comando(Orde==1);
        else if(Orde==2)응답시험();
        else if(Orde==6)mostrar_estado();
        else if(elemento_CONTAR()!=1){erro_VALOR("This command takes no arguments; help system");}
        else if(Orde==3)mostrar_camiño();else if(Orde==4)mostrar_Rede();else if(Orde==5)mostrar_Tasks();else if(Orde==7)mostrar_Memoria();else if(Orde==8)mostrar_Almacenamento();else if(Orde==9)mostrar_Actividade();
        else if(Orde==10)Panel.전원끄기();
        return true;
    }
}
