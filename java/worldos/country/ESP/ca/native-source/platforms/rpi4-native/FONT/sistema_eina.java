// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_dades nucli_VALOR 상태를 읽는 IPv4·ICMP·작업·Memòria_VALOR·RAM dipòsit_rel 관리 Ordre. */
public final class sistema_eina {
    static int ADREÇA_VALOR;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int element_COMPT() { return 명령해석기.testimoni_COMPT; }
    static void error_VALOR(String LLEGIU_ME_eb81d7d9) { 명령해석기.RESULTAT=2; 단말.Escriptura(LLEGIU_ME_eb81d7d9); 단말.문자(10); }
    static void s_ha_produït_un_error(int VALOR) { 명령해석기.s_ha_produït_un_error(VALOR); }
    static void 수항목(String Nom, int VALOR) { 단말.Escriptura(Nom); 단말.수(VALOR); 단말.문자(10); }
    static int dígit_VALOR(int INDEX, int 한도) {
        if (INDEX>=element_COMPT() || 명령해석기.durada_VALOR[INDEX]==0) return -1;
        int VALOR=0;
        for (int 순번=0; 순번<명령해석기.durada_VALOR[INDEX]; 순번++) {
            int caràcter_VALOR=명령해석기.testimoni_VALOR[명령해석기.시작점[INDEX]+순번]-'0';
            if (caràcter_VALOR<0 || caràcter_VALOR>9 || VALOR>(한도-caràcter_VALOR)/10) return -1;
            VALOR=VALOR*10+caràcter_VALOR;
        }
        return VALOR<=한도?VALOR:-1;
    }
    static boolean tancar_ADREÇA(int INDEX) {
        if (INDEX>=element_COMPT()) return false;
        int VALOR=0, 덩이=0, dígit_COMPT=0, p_COMPT=0;
        for (int 순번=0; 순번<명령해석기.durada_VALOR[INDEX]; 순번++) {
            int caràcter_VALOR=명령해석기.testimoni_VALOR[명령해석기.시작점[INDEX]+순번];
            if (caràcter_VALOR=='.') { if (dígit_COMPT==0 || ++p_COMPT>3) return false; VALOR=(VALOR<<8)|덩이; 덩이=dígit_COMPT=0; }
            else { if (caràcter_VALOR<'0' || caràcter_VALOR>'9' || ++dígit_COMPT>3) return false; 덩이=덩이*10+caràcter_VALOR-'0'; if(덩이>255)return false; }
        }
        if (p_COMPT!=3 || dígit_COMPT==0) return false;
        ADREÇA_VALOR=(VALOR<<8)|덩이; return true;
    }
    static void escriure_ADREÇA(int VALOR) {
        단말.수((VALOR>>>24)&255); 단말.문자('.'); 단말.수((VALOR>>>16)&255); 단말.문자('.');
        단말.수((VALOR>>>8)&255); 단말.문자('.'); 단말.수(VALOR&255);
    }
    static void mostrar_xarxa_estat() {
        단말.Escriptura(Tauler.xarxa_estat(20,0)!=0?"en0: ":"sl0: "); 단말.Escriptura(Tauler.xarxa_estat(3,0)!=0?"UP":"DOWN");
        단말.Escriptura(Tauler.xarxa_estat(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Escriptura(Tauler.xarxa_estat(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); escriure_ADREÇA(Tauler.xarxa_estat(0,0));
        단말.Escriptura(" netmask "); escriure_ADREÇA(Tauler.xarxa_estat(1,0)); 단말.Escriptura(" gateway "); escriure_ADREÇA(Tauler.xarxa_estat(2,0)); 단말.문자(10);
        단말.Escriptura("  RX packets "); 단말.수(Tauler.xarxa_estat(4,0)); 단말.Escriptura(" bytes "); 단말.수(Tauler.xarxa_estat(6,0));
        단말.Escriptura(" TX packets "); 단말.수(Tauler.xarxa_estat(5,0)); 단말.Escriptura(" bytes "); 단말.수(Tauler.xarxa_estat(7,0)); 단말.문자(10);
        수항목("  dropped ",Tauler.xarxa_estat(8,0));
    }
    static void conjunt_ADREÇA(int Executa_2) {
        if (element_COMPT()!=Executa_2+3 || !tancar_ADREÇA(Executa_2)) { error_VALOR("사용법: ipconfig set Adreça 주소가림 passarel_la_VALOR"); return; }
        int Adreça=ADREÇA_VALOR;
        if(!tancar_ADREÇA(Executa_2+1)){error_VALOR("Invalid IPv4 netmask");return;} int màscara_VALOR=ADREÇA_VALOR;
        if(!tancar_ADREÇA(Executa_2+2)){error_VALOR("Invalid IPv4 gateway");return;}
        int RESULTAT=Tauler.xarxa_Configuració(0,Adreça,màscara_VALOR,ADREÇA_VALOR);
        if(RESULTAT<0) { s_ha_produït_un_error(RESULTAT); if(RESULTAT==-16)단말.Escriptura("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Escriptura("IPv4 configuration applied (until reboot)\n"); mostrar_xarxa_estat(); }
    }
    static void xarxa_ordre(boolean adreça_IP) {
        if (element_COMPT()==1 || element_COMPT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || element_COMPT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { mostrar_xarxa_estat();return; }
        if (adreça_IP && 같음(1,"route") && (element_COMPT()==2 || element_COMPT()==3&&같음(2,"show"))) { mostrar_camí();return; }
        if (같음(1,"set")) { conjunt_ADREÇA(2);return; }
        if (element_COMPT()==2 && (같음(1,"up") || 같음(1,"down"))) { Tauler.xarxa_Configuració(같음(1,"up")?1:2,0,0,0);mostrar_xarxa_estat();return; }
        if (adreça_IP && element_COMPT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Tauler.xarxa_Configuració(같음(5,"up")?1:2,0,0,0);mostrar_xarxa_estat();return; }
        error_VALOR("사용법: ip [addr show|route show|set Adreça 주소가림 passarel_la_VALOR|link set dev sl0 up|down]");
    }
    static void mostrar_camí() {
        단말.Escriptura("Destination Netmask Gateway Interface\n");
        escriure_ADREÇA(Tauler.xarxa_estat(0,0)&Tauler.xarxa_estat(1,0));단말.문자(' ');escriure_ADREÇA(Tauler.xarxa_estat(1,0));단말.Escriptura(Tauler.xarxa_estat(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Tauler.xarxa_estat(2,0)!=0) {단말.Escriptura("0.0.0.0 0.0.0.0 ");escriure_ADREÇA(Tauler.xarxa_estat(2,0));단말.Escriptura(Tauler.xarxa_estat(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void mostrar_xarxa() {
        단말.Escriptura("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TIPUS_Categoria=Tauler.xarxa_estat(10,INDEX);if(TIPUS_Categoria==0)continue;
            단말.Escriptura(TIPUS_Categoria==1?"TCP ":"UDP ");escriure_ADREÇA(Tauler.xarxa_estat(16,INDEX));단말.문자(':');단말.수(Tauler.xarxa_estat(11,INDEX));단말.문자(' ');
            escriure_ADREÇA(Tauler.xarxa_estat(12,INDEX));단말.문자(':');단말.수(Tauler.xarxa_estat(13,INDEX));단말.문자(' ');
            int Estat_VALOR=Tauler.xarxa_estat(14,INDEX);단말.Escriptura(TIPUS_Categoria==2?"DATAGRAM":Estat_VALOR==1?"LISTEN":Estat_VALOR==2?"ESTABLISHED":Estat_VALOR==3?"CLOSE_WAIT":Estat_VALOR==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Tauler.xarxa_estat(15,INDEX));단말.문자(10);
        }
        단말.Escriptura("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean Espera_Estat(int 밀리초) {
        int Executa_2=Tauler.밀리초();
        while(Tauler.밀리초()-Executa_2<밀리초) {
            if(셸입출력.tecnologies_de_la_informació_interactiu()!=0){int caràcter_VALOR=Tauler.직렬읽기();if(caràcter_VALOR==3 || caràcter_VALOR=='q' || caràcter_VALOR=='Q' || caràcter_VALOR==27 || caràcter_VALOR==-4096)return false;}
            Tauler.RENDTO_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, objectiu=-1;
        for(int càrrec_INDEX=1;càrrec_INDEX<element_COMPT();càrrec_INDEX++) {
            if(같음(càrrec_INDEX,"-c")){횟수=dígit_VALOR(++càrrec_INDEX,100);if(횟수<1){error_VALOR("ping: -c 1..100");return;}}
            else if(같음(càrrec_INDEX,"-W")){제한=dígit_VALOR(++càrrec_INDEX,10);if(제한<1){error_VALOR("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(objectiu<0)objectiu=càrrec_INDEX;else{error_VALOR("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(objectiu<0 || !tancar_ADREÇA(objectiu)){error_VALOR("ping: an IPv4 address is required (DNS is not configured)");return;}
        int Adreça=ADREÇA_VALOR, 보낸수=0, CANTIDAD_RECIBIDA_COMPT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Escriptura("PING ");escriure_ADREÇA(Adreça);단말.Escriptura(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int comanda_VALOR=1;comanda_VALOR<=횟수 && 계속;comanda_VALOR++) {
            int 처리값=Tauler.enviar_resposta(Adreça,comanda_VALOR);
            if(처리값<0){s_ha_produït_un_error(처리값);break;}보낸수++;
            int Executa_2=Tauler.밀리초();
            while(Tauler.tancar_resposta(0)==-11 && Tauler.밀리초()-Executa_2<제한)if(!Espera_Estat(1)){계속=false;break;}
            if(!계속)break;
            if(Tauler.tancar_resposta(0)==0){
                int Hora_VALOR=Tauler.tancar_resposta(1);CANTIDAD_RECIBIDA_COMPT++;누적+=Hora_VALOR;if(Hora_VALOR<최솟값)최솟값=Hora_VALOR;if(Hora_VALOR>최댓값)최댓값=Hora_VALOR;
                단말.Escriptura("32 bytes from ");escriure_ADREÇA(Adreça);단말.Escriptura(" seq=");단말.수(comanda_VALOR);단말.Escriptura(" ttl=");단말.수(Tauler.tancar_resposta(2));단말.Escriptura(" time=");단말.수(Hora_VALOR);단말.Escriptura(" ms\n");
            }else{단말.Escriptura("Request timeout seq=");단말.수(comanda_VALOR);단말.문자(10);}
            if(comanda_VALOR<횟수)계속=Espera_Estat(200);
        }
        단말.수(보낸수);단말.Escriptura(" transmitted, ");단말.수(CANTIDAD_RECIBIDA_COMPT);단말.Escriptura(" received, ");단말.수(보낸수==0?100:(보낸수-CANTIDAD_RECIBIDA_COMPT)*100/보낸수);단말.Escriptura("% packet loss\n");
        if(CANTIDAD_RECIBIDA_COMPT>0){단말.Escriptura("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/CANTIDAD_RECIBIDA_COMPT);단말.문자('/');단말.수(최댓값);단말.Escriptura(" ms\n");}
        명령해석기.RESULTAT=계속?(CANTIDAD_RECIBIDA_COMPT==0?1:0):130;
    }
    static void mostrar_Activitat() { 단말.Escriptura("up ");단말.수(Tauler.밀리초()/1000);단말.Escriptura(" seconds\n"); }
    static void mostrar_Memòria() {
        수항목("ARM RAM KiB (firmware): ",Tauler.cerca_sistema(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Tauler.cerca_sistema(1,0));
        int total_capacitat=Tauler.cerca_sistema(2,0), 사용량=Tauler.cerca_sistema(3,0);
        단말.Escriptura("AOT heap KiB total/used/free: ");단말.수(total_capacitat);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(total_capacitat-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Tauler.cerca_sistema(4,0));
        수항목("EL0 arena+session reserve KiB: ",Tauler.cerca_sistema(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Tauler.cerca_sistema(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Escriptura("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void mostrar_Tasks() {
        단말.Escriptura("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Escriptura("1 - RUN - - ");단말.수(Tauler.밀리초());단말.Escriptura(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Tauler.tasca_Estat(INDEX)>0){단말.수(INDEX+1);단말.Escriptura(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Estat_VALOR=Tauler.cerca_sistema(20,INDEX);if(Estat_VALOR==0)continue;
            단말.수(Tauler.cerca_sistema(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Escriptura(Estat_VALOR==1?" RUN ":" SUSPENDED ");
            단말.수(Tauler.cerca_sistema(22,INDEX));단말.문자(' ');단말.수(Tauler.cerca_sistema(24,INDEX));단말.문자(' ');단말.수(Tauler.cerca_sistema(23,INDEX));단말.문자(' ');
            for(int càrrec_INDEX=0;càrrec_INDEX<288;càrrec_INDEX++){int byte_VALOR=Tauler.cerca_sistema(25,INDEX+càrrec_INDEX*4);if(byte_VALOR==0)break;Tauler.직렬쓰기(byte_VALOR);}단말.문자(10);
        }
    }
    static void mostrar_Emmagatzematge() {
        int 칸수=0, dades_COMPT=0;
        for(int INDEX=0;INDEX<Memòria_Fitxers.arxiu_COMPT;INDEX++)if(Memòria_Fitxers.이름길이[INDEX]>0 || Memòria_Fitxers.Referència_COMPT[INDEX]>0){칸수++;dades_COMPT+=Memòria_Fitxers.durada_VALOR[INDEX];}
        단말.Escriptura("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memòria_Fitxers.arxiu_COMPT*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((Memòria_Fitxers.arxiu_COMPT-칸수)*16384);단말.문자(' ');단말.수(dades_COMPT);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(Memòria_Fitxers.arxiu_COMPT);단말.Escriptura(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void mostrar_estat() {
        int 횟수=셸입출력.tecnologies_de_la_informació_interactiu()!=0?0:1;
        if(element_COMPT()>1){if(element_COMPT()!=3 || !같음(1,"-n") || (횟수=dígit_VALOR(2,1000))<1){error_VALOR("사용법: top [-n 1..1000]; q/Ctrl+C로 sortir_programa");return;}}
        for(int SEQÜÈNCIA_VALOR=0;횟수==0 || SEQÜÈNCIA_VALOR<횟수;SEQÜÈNCIA_VALOR++){
            if(셸입출력.tecnologies_de_la_informació_interactiu()!=0 && 횟수==0)단말.Escriptura("\u001b[2J\u001b[H");
            mostrar_Activitat();mostrar_Memòria();mostrar_Tasks();
            if(횟수!=0 && SEQÜÈNCIA_VALOR+1>=횟수)break;
            if(!Espera_Estat(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void mostrar_ajuda() {
        단말.Escriptura("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Escriptura(표준말(INDEX));단말.Escriptura(" / ");단말.Escriptura(관리명령.Word_SMS(INDEX));단말.Escriptura(" : ");단말.Escriptura(관리명령.설명(INDEX));단말.문자(10);}
        단말.Escriptura("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Escriptura("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Escriptura("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Executa_ordre() {
        int Ordre=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Ordre=INDEX;
        if(같음(0,"ifconfig"))Ordre=0;if(같음(0,"ss"))Ordre=4;
        if(Ordre<0)return false;
        if(Ordre==11){if(같음(1,"net") || 같음(1,"system"))mostrar_ajuda();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.mostrar_ajuda();return true;}
        if(Ordre==0 || Ordre==1)xarxa_ordre(Ordre==1);
        else if(Ordre==2)응답시험();
        else if(Ordre==6)mostrar_estat();
        else if(element_COMPT()!=1){error_VALOR("This command takes no arguments; help system");}
        else if(Ordre==3)mostrar_camí();else if(Ordre==4)mostrar_xarxa();else if(Ordre==5)mostrar_Tasks();else if(Ordre==7)mostrar_Memòria();else if(Ordre==8)mostrar_Emmagatzematge();else if(Ordre==9)mostrar_Activitat();
        else if(Ordre==10)Tauler.전원끄기();
        return true;
    }
}
