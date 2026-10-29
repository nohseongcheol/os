// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** effettivo_dati kernel_VALORE 상태를 읽는 IPv4·ICMP·작업·Memoria_VALORE·RAM radice_del_repository 관리 comando. */
public final class Sistema_strumento {
    static int e_mail_VALORE;
    static boolean 같음(int INDICE, String Word_SMS) { return InterpreteComandi.같음(INDICE, Word_SMS); }
    static int articolo_CONTA_NUMERI() { return InterpreteComandi.token_CONTA_NUMERI; }
    static void errore_VALORE(String README_eb81d7d9) { InterpreteComandi.risultato=2; 단말.Scrittura(README_eb81d7d9); 단말.문자(10); }
    static void errore(int VALORE) { InterpreteComandi.errore(VALORE); }
    static void numero_voce(String Nome, int VALORE) { 단말.Scrittura(Nome); 단말.numero(VALORE); 단말.문자(10); }
    static int cifra_VALORE(int INDICE, int 한도) {
        if (INDICE>=articolo_CONTA_NUMERI() || InterpreteComandi.durata_VALORE[INDICE]==0) return -1;
        int VALORE=0;
        for (int 순번=0; 순번<InterpreteComandi.durata_VALORE[INDICE]; 순번++) {
            int carattere_VALORE=InterpreteComandi.token_VALORE[InterpreteComandi.시작점[INDICE]+순번]-'0';
            if (carattere_VALORE<0 || carattere_VALORE>9 || VALORE>(한도-carattere_VALORE)/10) return -1;
            VALORE=VALORE*10+carattere_VALORE;
        }
        return VALORE<=한도?VALORE:-1;
    }
    static boolean 주소읽기(int INDICE) {
        if (INDICE>=articolo_CONTA_NUMERI()) return false;
        int VALORE=0, blocco_VALORE=0, cifra_CONTA_NUMERI=0, p_CONTA_NUMERI=0;
        for (int 순번=0; 순번<InterpreteComandi.durata_VALORE[INDICE]; 순번++) {
            int carattere_VALORE=InterpreteComandi.token_VALORE[InterpreteComandi.시작점[INDICE]+순번];
            if (carattere_VALORE=='.') { if (cifra_CONTA_NUMERI==0 || ++p_CONTA_NUMERI>3) return false; VALORE=(VALORE<<8)|blocco_VALORE; blocco_VALORE=cifra_CONTA_NUMERI=0; }
            else { if (carattere_VALORE<'0' || carattere_VALORE>'9' || ++cifra_CONTA_NUMERI>3) return false; blocco_VALORE=blocco_VALORE*10+carattere_VALORE-'0'; if(blocco_VALORE>255)return false; }
        }
        if (p_CONTA_NUMERI!=3 || cifra_CONTA_NUMERI==0) return false;
        e_mail_VALORE=(VALORE<<8)|blocco_VALORE; return true;
    }
    static void scrivere_e_mail(int VALORE) {
        단말.numero((VALORE>>>24)&255); 단말.문자('.'); 단말.numero((VALORE>>>16)&255); 단말.문자('.');
        단말.numero((VALORE>>>8)&255); 단말.문자('.'); 단말.numero(VALORE&255);
    }
    static void mostrare_rete_stato() {
        단말.Scrittura(scheda.rete_stato(20,0)!=0?"en0: ":"sl0: "); 단말.Scrittura(scheda.rete_stato(3,0)!=0?"UP":"DOWN");
        단말.Scrittura(scheda.rete_stato(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Scrittura(scheda.rete_stato(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); scrivere_e_mail(scheda.rete_stato(0,0));
        단말.Scrittura(" netmask "); scrivere_e_mail(scheda.rete_stato(1,0)); 단말.Scrittura(" gateway "); scrivere_e_mail(scheda.rete_stato(2,0)); 단말.문자(10);
        단말.Scrittura("  RX packets "); 단말.numero(scheda.rete_stato(4,0)); 단말.Scrittura(" bytes "); 단말.numero(scheda.rete_stato(6,0));
        단말.Scrittura(" TX packets "); 단말.numero(scheda.rete_stato(5,0)); 단말.Scrittura(" bytes "); 단말.numero(scheda.rete_stato(7,0)); 단말.문자(10);
        numero_voce("  dropped ",scheda.rete_stato(8,0));
    }
    static void set_e_mail(int avvia) {
        if (articolo_CONTA_NUMERI()!=avvia+3 || !주소읽기(avvia)) { errore_VALORE("사용법: ipconfig set e_mail 주소가림 gateway_VALORE"); return; }
        int e_mail=e_mail_VALORE;
        if(!주소읽기(avvia+1)){errore_VALORE("Invalid IPv4 netmask");return;} int maschera_VALORE=e_mail_VALORE;
        if(!주소읽기(avvia+2)){errore_VALORE("Invalid IPv4 gateway");return;}
        int risultato=scheda.rete_Impostazioni(0,e_mail,maschera_VALORE,e_mail_VALORE);
        if(risultato<0) { errore(risultato); if(risultato==-16)단말.Scrittura("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Scrittura("IPv4 configuration applied (until reboot)\n"); mostrare_rete_stato(); }
    }
    static void rete_comando(boolean indirizzo_IP) {
        if (articolo_CONTA_NUMERI()==1 || articolo_CONTA_NUMERI()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || articolo_CONTA_NUMERI()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { mostrare_rete_stato();return; }
        if (indirizzo_IP && 같음(1,"route") && (articolo_CONTA_NUMERI()==2 || articolo_CONTA_NUMERI()==3&&같음(2,"show"))) { mostrare_percorso();return; }
        if (같음(1,"set")) { set_e_mail(2);return; }
        if (articolo_CONTA_NUMERI()==2 && (같음(1,"up") || 같음(1,"down"))) { scheda.rete_Impostazioni(같음(1,"up")?1:2,0,0,0);mostrare_rete_stato();return; }
        if (indirizzo_IP && articolo_CONTA_NUMERI()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { scheda.rete_Impostazioni(같음(5,"up")?1:2,0,0,0);mostrare_rete_stato();return; }
        errore_VALORE("사용법: ip [addr show|route show|set e_mail 주소가림 gateway_VALORE|link set dev sl0 up|down]");
    }
    static void mostrare_percorso() {
        단말.Scrittura("Destination Netmask Gateway Interface\n");
        scrivere_e_mail(scheda.rete_stato(0,0)&scheda.rete_stato(1,0));단말.문자(' ');scrivere_e_mail(scheda.rete_stato(1,0));단말.Scrittura(scheda.rete_stato(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (scheda.rete_stato(2,0)!=0) {단말.Scrittura("0.0.0.0 0.0.0.0 ");scrivere_e_mail(scheda.rete_stato(2,0));단말.Scrittura(scheda.rete_stato(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void mostrare_rete() {
        단말.Scrittura("Proto Local Remote State Queued\n");
        for(int INDICE=0;INDICE<32;INDICE++) {
            int TIPO_area=scheda.rete_stato(10,INDICE);if(TIPO_area==0)continue;
            단말.Scrittura(TIPO_area==1?"TCP ":"UDP ");scrivere_e_mail(scheda.rete_stato(16,INDICE));단말.문자(':');단말.numero(scheda.rete_stato(11,INDICE));단말.문자(' ');
            scrivere_e_mail(scheda.rete_stato(12,INDICE));단말.문자(':');단말.numero(scheda.rete_stato(13,INDICE));단말.문자(' ');
            int Stato_VALORE=scheda.rete_stato(14,INDICE);단말.Scrittura(TIPO_area==2?"DATAGRAM":Stato_VALORE==1?"LISTEN":Stato_VALORE==2?"ESTABLISHED":Stato_VALORE==3?"CLOSE_WAIT":Stato_VALORE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.numero(scheda.rete_stato(15,INDICE));단말.문자(10);
        }
        단말.Scrittura("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean stato_di_attesa(int 밀리초) {
        int avvia=scheda.밀리초();
        while(scheda.밀리초()-avvia<밀리초) {
            if(셸입출력.reparto_IT_interattivo()!=0){int carattere_VALORE=scheda.직렬읽기();if(carattere_VALORE==3 || carattere_VALORE=='q' || carattere_VALORE=='Q' || carattere_VALORE==27 || carattere_VALORE==-4096)return false;}
            scheda.REND_CPU();
        }
        return true;
    }
    static void test_risposta() {
        int ripetizione_CONTA_NUMERI=4, 제한=1000, target=-1;
        for(int funzione_INDICE=1;funzione_INDICE<articolo_CONTA_NUMERI();funzione_INDICE++) {
            if(같음(funzione_INDICE,"-c")){ripetizione_CONTA_NUMERI=cifra_VALORE(++funzione_INDICE,100);if(ripetizione_CONTA_NUMERI<1){errore_VALORE("ping: -c 1..100");return;}}
            else if(같음(funzione_INDICE,"-W")){제한=cifra_VALORE(++funzione_INDICE,10);if(제한<1){errore_VALORE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(target<0)target=funzione_INDICE;else{errore_VALORE("사용법: ping [-c ripetizione_CONTA_NUMERI] [-W 초] IPv4");return;}
        }
        if(target<0 || !주소읽기(target)){errore_VALORE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int e_mail=e_mail_VALORE, 보낸수=0, RICEV_SCAD_CONTA_NUMERI=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Scrittura("PING ");scrivere_e_mail(e_mail);단말.Scrittura(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ordine_VALORE=1;ordine_VALORE<=ripetizione_CONTA_NUMERI && 계속;ordine_VALORE++) {
            int 처리값=scheda.inviare_risposta(e_mail,ordine_VALORE);
            if(처리값<0){errore(처리값);break;}보낸수++;
            int avvia=scheda.밀리초();
            while(scheda.응답읽기(0)==-11 && scheda.밀리초()-avvia<제한)if(!stato_di_attesa(1)){계속=false;break;}
            if(!계속)break;
            if(scheda.응답읽기(0)==0){
                int valore=scheda.응답읽기(1);RICEV_SCAD_CONTA_NUMERI++;누적+=valore;if(valore<최솟값)최솟값=valore;if(valore>최댓값)최댓값=valore;
                단말.Scrittura("32 bytes from ");scrivere_e_mail(e_mail);단말.Scrittura(" seq=");단말.numero(ordine_VALORE);단말.Scrittura(" ttl=");단말.numero(scheda.응답읽기(2));단말.Scrittura(" time=");단말.numero(valore);단말.Scrittura(" ms\n");
            }else{단말.Scrittura("Request timeout seq=");단말.numero(ordine_VALORE);단말.문자(10);}
            if(ordine_VALORE<ripetizione_CONTA_NUMERI)계속=stato_di_attesa(200);
        }
        단말.numero(보낸수);단말.Scrittura(" transmitted, ");단말.numero(RICEV_SCAD_CONTA_NUMERI);단말.Scrittura(" received, ");단말.numero(보낸수==0?100:(보낸수-RICEV_SCAD_CONTA_NUMERI)*100/보낸수);단말.Scrittura("% packet loss\n");
        if(RICEV_SCAD_CONTA_NUMERI>0){단말.Scrittura("rtt min/avg/max = ");단말.numero(최솟값);단말.문자('/');단말.numero(누적/RICEV_SCAD_CONTA_NUMERI);단말.문자('/');단말.numero(최댓값);단말.Scrittura(" ms\n");}
        InterpreteComandi.risultato=계속?(RICEV_SCAD_CONTA_NUMERI==0?1:0):130;
    }
    static void mostrare_Azioni() { 단말.Scrittura("up ");단말.numero(scheda.밀리초()/1000);단말.Scrittura(" seconds\n"); }
    static void mostrare_Memoria() {
        numero_voce("ARM RAM KiB (firmware): ",scheda.query_Sistema(0,0));
        numero_voce("Kernel image+BSS+stack KiB: ",scheda.query_Sistema(1,0));
        int totale_capacità=scheda.query_Sistema(2,0), 사용량=scheda.query_Sistema(3,0);
        단말.Scrittura("AOT heap KiB total/used/free: ");단말.numero(totale_capacità);단말.문자('/');단말.numero(사용량);단말.문자('/');단말.numero(totale_capacità-사용량);단말.문자(10);
        numero_voce("Framebuffer KiB: ",scheda.query_Sistema(4,0));
        numero_voce("EL0 arena+session reserve KiB: ",scheda.query_Sistema(5,0));
        int 매핑=0;for(int INDICE=0;INDICE<4;INDICE++)매핑+=scheda.query_Sistema(22,INDICE);
        numero_voce("EL0 mapped KiB: ",매핑);
        단말.Scrittura("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void mostrare_Tasks() {
        단말.Scrittura("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Scrittura("1 - RUN - - ");단말.numero(scheda.밀리초());단말.Scrittura(" kernel/shell\n");
        for(int INDICE=1;INDICE<3;INDICE++)if(scheda.task_Stato(INDICE)>0){단말.numero(INDICE+1);단말.Scrittura(" - READY 64 - - kernel-task\n");}
        for(int INDICE=0;INDICE<4;INDICE++){
            int Stato_VALORE=scheda.query_Sistema(20,INDICE);if(Stato_VALORE==0)continue;
            단말.numero(scheda.query_Sistema(21,INDICE));단말.문자(' ');단말.numero(INDICE);단말.Scrittura(Stato_VALORE==1?" RUN ":" SUSPENDED ");
            단말.numero(scheda.query_Sistema(22,INDICE));단말.문자(' ');단말.numero(scheda.query_Sistema(24,INDICE));단말.문자(' ');단말.numero(scheda.query_Sistema(23,INDICE));단말.문자(' ');
            for(int funzione_INDICE=0;funzione_INDICE<288;funzione_INDICE++){int byte_VALORE=scheda.query_Sistema(25,INDICE+funzione_INDICE*4);if(byte_VALORE==0)break;scheda.scrivere_seriale(byte_VALORE);}단말.문자(10);
        }
    }
    static void mostrare_Memoria_deafe149() {
        int slot_CONTA_NUMERI=0, dati_CONTA_NUMERI=0;
        for(int INDICE=0;INDICE<FileMemoria.File_CONTA_NUMERI;INDICE++)if(FileMemoria.이름길이[INDICE]>0 || FileMemoria.fonti_CONTA_NUMERI[INDICE]>0){slot_CONTA_NUMERI++;dati_CONTA_NUMERI+=FileMemoria.durata_VALORE[INDICE];}
        단말.Scrittura("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.numero(FileMemoria.File_CONTA_NUMERI*16384);단말.문자(' ');단말.numero(slot_CONTA_NUMERI*16384);단말.문자(' ');단말.numero((FileMemoria.File_CONTA_NUMERI-slot_CONTA_NUMERI)*16384);단말.문자(' ');단말.numero(dati_CONTA_NUMERI);단말.문자(' ');단말.numero(slot_CONTA_NUMERI);단말.문자('/');단말.numero(FileMemoria.File_CONTA_NUMERI);단말.Scrittura(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void mostrare_stato() {
        int ripetizione_CONTA_NUMERI=셸입출력.reparto_IT_interattivo()!=0?0:1;
        if(articolo_CONTA_NUMERI()>1){if(articolo_CONTA_NUMERI()!=3 || !같음(1,"-n") || (ripetizione_CONTA_NUMERI=cifra_VALORE(2,1000))<1){errore_VALORE("사용법: top [-n 1..1000]; q/Ctrl+C로 esci_app");return;}}
        for(int SEQUENZA_VALORE=0;ripetizione_CONTA_NUMERI==0 || SEQUENZA_VALORE<ripetizione_CONTA_NUMERI;SEQUENZA_VALORE++){
            if(셸입출력.reparto_IT_interattivo()!=0 && ripetizione_CONTA_NUMERI==0)단말.Scrittura("\u001b[2J\u001b[H");
            mostrare_Azioni();mostrare_Memoria();mostrare_Tasks();
            if(ripetizione_CONTA_NUMERI!=0 && SEQUENZA_VALORE+1>=ripetizione_CONTA_NUMERI)break;
            if(!stato_di_attesa(1000))break;
        }
    }
    static String Standard_Word(int INDICE) {
        if(INDICE==0)return "ipconfig";if(INDICE==1)return "ip";if(INDICE==2)return "ping";if(INDICE==3)return "route";if(INDICE==4)return "netstat";
        if(INDICE==5)return "ps";if(INDICE==6)return "top";if(INDICE==7)return "free";if(INDICE==8)return "df";if(INDICE==9)return "uptime";if(INDICE==10)return "poweroff";return "help";
    }
    static void mostra_aiuto() {
        단말.Scrittura("--- Network / system commands ---\n");
        for(int INDICE=0;INDICE<12;INDICE++){단말.Scrittura(Standard_Word(INDICE));단말.Scrittura(" / ");단말.Scrittura(관리명령.Word_SMS(INDICE));단말.Scrittura(" : ");단말.Scrittura(관리명령.설명(INDICE));단말.문자(10);}
        단말.Scrittura("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Scrittura("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Scrittura("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Esegui_comando() {
        int comando=-1;
        for(int INDICE=0;INDICE<12;INDICE++)if(같음(0,Standard_Word(INDICE)) || 같음(0,관리명령.Word_SMS(INDICE)))comando=INDICE;
        if(같음(0,"ifconfig"))comando=0;if(같음(0,"ss"))comando=4;
        if(comando<0)return false;
        if(comando==11){if(같음(1,"net") || 같음(1,"system"))mostra_aiuto();else if(같음(1,"ko") || 같음(1,"input"))InterpreteComandi.한글도움말();else InterpreteComandi.mostra_aiuto();return true;}
        if(comando==0 || comando==1)rete_comando(comando==1);
        else if(comando==2)test_risposta();
        else if(comando==6)mostrare_stato();
        else if(articolo_CONTA_NUMERI()!=1){errore_VALORE("This command takes no arguments; help system");}
        else if(comando==3)mostrare_percorso();else if(comando==4)mostrare_rete();else if(comando==5)mostrare_Tasks();else if(comando==7)mostrare_Memoria();else if(comando==8)mostrare_Memoria_deafe149();else if(comando==9)mostrare_Azioni();
        else if(comando==10)scheda.전원끄기();
        return true;
    }
}
