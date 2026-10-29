// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktisk_data kjerne_VERDI 상태를 읽는 IPv4·ICMP·작업·Minne_VERDI·RAM repositorium_rot 관리 Kommando. */
public final class System_verktøy {
    static int e_post_VERDI;
    static boolean 같음(int INDEKS, String ord_SMS) { return 명령해석기.같음(INDEKS, ord_SMS); }
    static int vare_ANTALL() { return 명령해석기.token_ANTALL; }
    static void feil_VERDI(String Viktig_fil_eb81d7d9) { 명령해석기.KR=2; 단말.Skriv(Viktig_fil_eb81d7d9); 단말.문자(10); }
    static void feil(int VERDI) { 명령해석기.feil(VERDI); }
    static void nummer_oppføring(String Navn, int VERDI) { 단말.Skriv(Navn); 단말.nummer(VERDI); 단말.문자(10); }
    static int siffer_VERDI(int INDEKS, int 한도) {
        if (INDEKS>=vare_ANTALL() || 명령해석기.lengde_VERDI[INDEKS]==0) return -1;
        int VERDI=0;
        for (int 순번=0; 순번<명령해석기.lengde_VERDI[INDEKS]; 순번++) {
            int tegn_VERDI=명령해석기.token_VERDI[명령해석기.시작점[INDEKS]+순번]-'0';
            if (tegn_VERDI<0 || tegn_VERDI>9 || VERDI>(한도-tegn_VERDI)/10) return -1;
            VERDI=VERDI*10+tegn_VERDI;
        }
        return VERDI<=한도?VERDI:-1;
    }
    static boolean 주소읽기(int INDEKS) {
        if (INDEKS>=vare_ANTALL()) return false;
        int VERDI=0, 덩이=0, siffer_ANTALL=0, peke_ANTALL=0;
        for (int 순번=0; 순번<명령해석기.lengde_VERDI[INDEKS]; 순번++) {
            int tegn_VERDI=명령해석기.token_VERDI[명령해석기.시작점[INDEKS]+순번];
            if (tegn_VERDI=='.') { if (siffer_ANTALL==0 || ++peke_ANTALL>3) return false; VERDI=(VERDI<<8)|덩이; 덩이=siffer_ANTALL=0; }
            else { if (tegn_VERDI<'0' || tegn_VERDI>'9' || ++siffer_ANTALL>3) return false; 덩이=덩이*10+tegn_VERDI-'0'; if(덩이>255)return false; }
        }
        if (peke_ANTALL!=3 || siffer_ANTALL==0) return false;
        e_post_VERDI=(VERDI<<8)|덩이; return true;
    }
    static void skrive_e_post(int VERDI) {
        단말.nummer((VERDI>>>24)&255); 단말.문자('.'); 단말.nummer((VERDI>>>16)&255); 단말.문자('.');
        단말.nummer((VERDI>>>8)&255); 단말.문자('.'); 단말.nummer(VERDI&255);
    }
    static void vise_nettverk_status() {
        단말.Skriv(Tavle.nettverk_status(20,0)!=0?"en0: ":"sl0: "); 단말.Skriv(Tavle.nettverk_status(3,0)!=0?"UP":"DOWN");
        단말.Skriv(Tavle.nettverk_status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Skriv(Tavle.nettverk_status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); skrive_e_post(Tavle.nettverk_status(0,0));
        단말.Skriv(" netmask "); skrive_e_post(Tavle.nettverk_status(1,0)); 단말.Skriv(" gateway "); skrive_e_post(Tavle.nettverk_status(2,0)); 단말.문자(10);
        단말.Skriv("  RX packets "); 단말.nummer(Tavle.nettverk_status(4,0)); 단말.Skriv(" bytes "); 단말.nummer(Tavle.nettverk_status(6,0));
        단말.Skriv(" TX packets "); 단말.nummer(Tavle.nettverk_status(5,0)); 단말.Skriv(" bytes "); 단말.nummer(Tavle.nettverk_status(7,0)); 단말.문자(10);
        nummer_oppføring("  dropped ",Tavle.nettverk_status(8,0));
    }
    static void sett_e_post(int Kjør_2) {
        if (vare_ANTALL()!=Kjør_2+3 || !주소읽기(Kjør_2)) { feil_VERDI("사용법: ipconfig set e_post 주소가림 gateway_VERDI"); return; }
        int e_post=e_post_VERDI;
        if(!주소읽기(Kjør_2+1)){feil_VERDI("Invalid IPv4 netmask");return;} int maske_VERDI=e_post_VERDI;
        if(!주소읽기(Kjør_2+2)){feil_VERDI("Invalid IPv4 gateway");return;}
        int KR=Tavle.nettverk_Innstillinger(0,e_post,maske_VERDI,e_post_VERDI);
        if(KR<0) { feil(KR); if(KR==-16)단말.Skriv("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Skriv("IPv4 configuration applied (until reboot)\n"); vise_nettverk_status(); }
    }
    static void nettverk_kommando(boolean IP_adresse) {
        if (vare_ANTALL()==1 || vare_ANTALL()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || vare_ANTALL()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { vise_nettverk_status();return; }
        if (IP_adresse && 같음(1,"route") && (vare_ANTALL()==2 || vare_ANTALL()==3&&같음(2,"show"))) { vise_bane();return; }
        if (같음(1,"set")) { sett_e_post(2);return; }
        if (vare_ANTALL()==2 && (같음(1,"up") || 같음(1,"down"))) { Tavle.nettverk_Innstillinger(같음(1,"up")?1:2,0,0,0);vise_nettverk_status();return; }
        if (IP_adresse && vare_ANTALL()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Tavle.nettverk_Innstillinger(같음(5,"up")?1:2,0,0,0);vise_nettverk_status();return; }
        feil_VERDI("사용법: ip [addr show|route show|set e_post 주소가림 gateway_VERDI|link set dev sl0 up|down]");
    }
    static void vise_bane() {
        단말.Skriv("Destination Netmask Gateway Interface\n");
        skrive_e_post(Tavle.nettverk_status(0,0)&Tavle.nettverk_status(1,0));단말.문자(' ');skrive_e_post(Tavle.nettverk_status(1,0));단말.Skriv(Tavle.nettverk_status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Tavle.nettverk_status(2,0)!=0) {단말.Skriv("0.0.0.0 0.0.0.0 ");skrive_e_post(Tavle.nettverk_status(2,0));단말.Skriv(Tavle.nettverk_status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void vise_nettverk() {
        단말.Skriv("Proto Local Remote State Queued\n");
        for(int INDEKS=0;INDEKS<32;INDEKS++) {
            int Type_område=Tavle.nettverk_status(10,INDEKS);if(Type_område==0)continue;
            단말.Skriv(Type_område==1?"TCP ":"UDP ");skrive_e_post(Tavle.nettverk_status(16,INDEKS));단말.문자(':');단말.nummer(Tavle.nettverk_status(11,INDEKS));단말.문자(' ');
            skrive_e_post(Tavle.nettverk_status(12,INDEKS));단말.문자(':');단말.nummer(Tavle.nettverk_status(13,INDEKS));단말.문자(' ');
            int status_VERDI=Tavle.nettverk_status(14,INDEKS);단말.Skriv(Type_område==2?"DATAGRAM":status_VERDI==1?"LISTEN":status_VERDI==2?"ESTABLISHED":status_VERDI==3?"CLOSE_WAIT":status_VERDI==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.nummer(Tavle.nettverk_status(15,INDEKS));단말.문자(10);
        }
        단말.Skriv("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean ventende_tilstand(int 밀리초) {
        int Kjør_2=Tavle.밀리초();
        while(Tavle.밀리초()-Kjør_2<밀리초) {
            if(셸입출력.informasjonssystemer_interaktiv()!=0){int tegn_VERDI=Tavle.직렬읽기();if(tegn_VERDI==3 || tegn_VERDI=='q' || tegn_VERDI=='Q' || tegn_VERDI==27 || tegn_VERDI==-4096)return false;}
            Tavle.AVKAST_CPU();
        }
        return true;
    }
    static void test_svar() {
        int 횟수=4, 제한=1000, mål=-1;
        for(int posisjonsindeks=1;posisjonsindeks<vare_ANTALL();posisjonsindeks++) {
            if(같음(posisjonsindeks,"-c")){횟수=siffer_VERDI(++posisjonsindeks,100);if(횟수<1){feil_VERDI("ping: -c 1..100");return;}}
            else if(같음(posisjonsindeks,"-W")){제한=siffer_VERDI(++posisjonsindeks,10);if(제한<1){feil_VERDI("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(mål<0)mål=posisjonsindeks;else{feil_VERDI("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(mål<0 || !주소읽기(mål)){feil_VERDI("ping: an IPv4 address is required (DNS is not configured)");return;}
        int e_post=e_post_VERDI, 보낸수=0, MOTTATT_AVKAST_ANTALL=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Skriv("PING ");skrive_e_post(e_post);단말.Skriv(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ordre_VERDI=1;ordre_VERDI<=횟수 && 계속;ordre_VERDI++) {
            int 처리값=Tavle.sende_svar(e_post,ordre_VERDI);
            if(처리값<0){feil(처리값);break;}보낸수++;
            int Kjør_2=Tavle.밀리초();
            while(Tavle.응답읽기(0)==-11 && Tavle.밀리초()-Kjør_2<제한)if(!ventende_tilstand(1)){계속=false;break;}
            if(!계속)break;
            if(Tavle.응답읽기(0)==0){
                int TID_VERDI=Tavle.응답읽기(1);MOTTATT_AVKAST_ANTALL++;누적+=TID_VERDI;if(TID_VERDI<최솟값)최솟값=TID_VERDI;if(TID_VERDI>최댓값)최댓값=TID_VERDI;
                단말.Skriv("32 bytes from ");skrive_e_post(e_post);단말.Skriv(" seq=");단말.nummer(ordre_VERDI);단말.Skriv(" ttl=");단말.nummer(Tavle.응답읽기(2));단말.Skriv(" time=");단말.nummer(TID_VERDI);단말.Skriv(" ms\n");
            }else{단말.Skriv("Request timeout seq=");단말.nummer(ordre_VERDI);단말.문자(10);}
            if(ordre_VERDI<횟수)계속=ventende_tilstand(200);
        }
        단말.nummer(보낸수);단말.Skriv(" transmitted, ");단말.nummer(MOTTATT_AVKAST_ANTALL);단말.Skriv(" received, ");단말.nummer(보낸수==0?100:(보낸수-MOTTATT_AVKAST_ANTALL)*100/보낸수);단말.Skriv("% packet loss\n");
        if(MOTTATT_AVKAST_ANTALL>0){단말.Skriv("rtt min/avg/max = ");단말.nummer(최솟값);단말.문자('/');단말.nummer(누적/MOTTATT_AVKAST_ANTALL);단말.문자('/');단말.nummer(최댓값);단말.Skriv(" ms\n");}
        명령해석기.KR=계속?(MOTTATT_AVKAST_ANTALL==0?1:0):130;
    }
    static void vise_Aktivitet() { 단말.Skriv("up ");단말.nummer(Tavle.밀리초()/1000);단말.Skriv(" seconds\n"); }
    static void vise_Minne() {
        nummer_oppføring("ARM RAM KiB (firmware): ",Tavle.spørre_System(0,0));
        nummer_oppføring("Kernel image+BSS+stack KiB: ",Tavle.spørre_System(1,0));
        int total_kapasitet=Tavle.spørre_System(2,0), 사용량=Tavle.spørre_System(3,0);
        단말.Skriv("AOT heap KiB total/used/free: ");단말.nummer(total_kapasitet);단말.문자('/');단말.nummer(사용량);단말.문자('/');단말.nummer(total_kapasitet-사용량);단말.문자(10);
        nummer_oppføring("Framebuffer KiB: ",Tavle.spørre_System(4,0));
        nummer_oppføring("EL0 arena+session reserve KiB: ",Tavle.spørre_System(5,0));
        int 매핑=0;for(int INDEKS=0;INDEKS<4;INDEKS++)매핑+=Tavle.spørre_System(22,INDEKS);
        nummer_oppføring("EL0 mapped KiB: ",매핑);
        단말.Skriv("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void vise_Tasks() {
        단말.Skriv("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Skriv("1 - RUN - - ");단말.nummer(Tavle.밀리초());단말.Skriv(" kernel/shell\n");
        for(int INDEKS=1;INDEKS<3;INDEKS++)if(Tavle.oppgave_status(INDEKS)>0){단말.nummer(INDEKS+1);단말.Skriv(" - READY 64 - - kernel-task\n");}
        for(int INDEKS=0;INDEKS<4;INDEKS++){
            int status_VERDI=Tavle.spørre_System(20,INDEKS);if(status_VERDI==0)continue;
            단말.nummer(Tavle.spørre_System(21,INDEKS));단말.문자(' ');단말.nummer(INDEKS);단말.Skriv(status_VERDI==1?" RUN ":" SUSPENDED ");
            단말.nummer(Tavle.spørre_System(22,INDEKS));단말.문자(' ');단말.nummer(Tavle.spørre_System(24,INDEKS));단말.문자(' ');단말.nummer(Tavle.spørre_System(23,INDEKS));단말.문자(' ');
            for(int posisjonsindeks=0;posisjonsindeks<288;posisjonsindeks++){int byte_VERDI=Tavle.spørre_System(25,INDEKS+posisjonsindeks*4);if(byte_VERDI==0)break;Tavle.직렬쓰기(byte_VERDI);}단말.문자(10);
        }
    }
    static void vise_lager() {
        int åpning_ANTALL=0, data_ANTALL=0;
        for(int INDEKS=0;INDEKS<Minne_Filer.Fil_ANTALL;INDEKS++)if(Minne_Filer.이름길이[INDEKS]>0 || Minne_Filer.referere_ANTALL[INDEKS]>0){åpning_ANTALL++;data_ANTALL+=Minne_Filer.lengde_VERDI[INDEKS];}
        단말.Skriv("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.nummer(Minne_Filer.Fil_ANTALL*16384);단말.문자(' ');단말.nummer(åpning_ANTALL*16384);단말.문자(' ');단말.nummer((Minne_Filer.Fil_ANTALL-åpning_ANTALL)*16384);단말.문자(' ');단말.nummer(data_ANTALL);단말.문자(' ');단말.nummer(åpning_ANTALL);단말.문자('/');단말.nummer(Minne_Filer.Fil_ANTALL);단말.Skriv(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void vise_status_bf9821b5() {
        int 횟수=셸입출력.informasjonssystemer_interaktiv()!=0?0:1;
        if(vare_ANTALL()>1){if(vare_ANTALL()!=3 || !같음(1,"-n") || (횟수=siffer_VERDI(2,1000))<1){feil_VERDI("사용법: top [-n 1..1000]; q/Ctrl+C로 avslutt_app");return;}}
        for(int SEKVENS_VERDI=0;횟수==0 || SEKVENS_VERDI<횟수;SEKVENS_VERDI++){
            if(셸입출력.informasjonssystemer_interaktiv()!=0 && 횟수==0)단말.Skriv("\u001b[2J\u001b[H");
            vise_Aktivitet();vise_Minne();vise_Tasks();
            if(횟수!=0 && SEKVENS_VERDI+1>=횟수)break;
            if(!ventende_tilstand(1000))break;
        }
    }
    static String Standard_ord(int INDEKS) {
        if(INDEKS==0)return "ipconfig";if(INDEKS==1)return "ip";if(INDEKS==2)return "ping";if(INDEKS==3)return "route";if(INDEKS==4)return "netstat";
        if(INDEKS==5)return "ps";if(INDEKS==6)return "top";if(INDEKS==7)return "free";if(INDEKS==8)return "df";if(INDEKS==9)return "uptime";if(INDEKS==10)return "poweroff";return "help";
    }
    static void vise_hjelp() {
        단말.Skriv("--- Network / system commands ---\n");
        for(int INDEKS=0;INDEKS<12;INDEKS++){단말.Skriv(Standard_ord(INDEKS));단말.Skriv(" / ");단말.Skriv(관리명령.ord_SMS(INDEKS));단말.Skriv(" : ");단말.Skriv(관리명령.설명(INDEKS));단말.문자(10);}
        단말.Skriv("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Skriv("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Skriv("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Utfør_kommando() {
        int Kommando=-1;
        for(int INDEKS=0;INDEKS<12;INDEKS++)if(같음(0,Standard_ord(INDEKS)) || 같음(0,관리명령.ord_SMS(INDEKS)))Kommando=INDEKS;
        if(같음(0,"ifconfig"))Kommando=0;if(같음(0,"ss"))Kommando=4;
        if(Kommando<0)return false;
        if(Kommando==11){if(같음(1,"net") || 같음(1,"system"))vise_hjelp();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.vise_hjelp();return true;}
        if(Kommando==0 || Kommando==1)nettverk_kommando(Kommando==1);
        else if(Kommando==2)test_svar();
        else if(Kommando==6)vise_status_bf9821b5();
        else if(vare_ANTALL()!=1){feil_VERDI("This command takes no arguments; help system");}
        else if(Kommando==3)vise_bane();else if(Kommando==4)vise_nettverk();else if(Kommando==5)vise_Tasks();else if(Kommando==7)vise_Minne();else if(Kommando==8)vise_lager();else if(Kommando==9)vise_Aktivitet();
        else if(Kommando==10)Tavle.전원끄기();
        return true;
    }
}
