// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktisk_data kjerne_VALUE 상태를 읽는 IPv4·ICMP·작업·Minne_VALUE·RAM 저장소 관리 Kommando. */
public final class system_verktøy {
    static int ADDRESS_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int vare_COUNT() { return 명령해석기.token_COUNT; }
    static void feil_VALUE(String Viktig_eb81d7d9) { 명령해석기.forretningsmål=2; 단말.Skriv(Viktig_eb81d7d9); 단말.문자(10); }
    static void FEIL(int VALUE) { 명령해석기.FEIL(VALUE); }
    static void 수항목(String Namn, int VALUE) { 단말.Skriv(Namn); 단말.수(VALUE); 단말.문자(10); }
    static int siffer_VALUE(int INDEX, int 한도) {
        if (INDEX>=vare_COUNT() || 명령해석기.lengd_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.lengd_VALUE[INDEX]; 순번++) {
            int teikn_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (teikn_VALUE<0 || teikn_VALUE>9 || VALUE>(한도-teikn_VALUE)/10) return -1;
            VALUE=VALUE*10+teikn_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=vare_COUNT()) return false;
        int VALUE=0, 덩이=0, siffer_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.lengd_VALUE[INDEX]; 순번++) {
            int teikn_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (teikn_VALUE=='.') { if (siffer_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=siffer_COUNT=0; }
            else { if (teikn_VALUE<'0' || teikn_VALUE>'9' || ++siffer_COUNT>3) return false; 덩이=덩이*10+teikn_VALUE-'0'; if(덩이>255)return false; }
        }
        if (p_COUNT!=3 || siffer_COUNT==0) return false;
        ADDRESS_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void skrive_ADDRESS(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void vise_Nettverk_merkje() {
        단말.Skriv(Tavle.Nettverk_merkje(20,0)!=0?"en0: ":"sl0: "); 단말.Skriv(Tavle.Nettverk_merkje(3,0)!=0?"UP":"DOWN");
        단말.Skriv(Tavle.Nettverk_merkje(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Skriv(Tavle.Nettverk_merkje(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); skrive_ADDRESS(Tavle.Nettverk_merkje(0,0));
        단말.Skriv(" netmask "); skrive_ADDRESS(Tavle.Nettverk_merkje(1,0)); 단말.Skriv(" gateway "); skrive_ADDRESS(Tavle.Nettverk_merkje(2,0)); 단말.문자(10);
        단말.Skriv("  RX packets "); 단말.수(Tavle.Nettverk_merkje(4,0)); 단말.Skriv(" bytes "); 단말.수(Tavle.Nettverk_merkje(6,0));
        단말.Skriv(" TX packets "); 단말.수(Tavle.Nettverk_merkje(5,0)); 단말.Skriv(" bytes "); 단말.수(Tavle.Nettverk_merkje(7,0)); 단말.문자(10);
        수항목("  dropped ",Tavle.Nettverk_merkje(8,0));
    }
    static void sett_ADDRESS(int Køyr_2) {
        if (vare_COUNT()!=Køyr_2+3 || !주소읽기(Køyr_2)) { feil_VALUE("사용법: ipconfig set ADDRESS 주소가림 gateway_VALUE"); return; }
        int ADDRESS=ADDRESS_VALUE;
        if(!주소읽기(Køyr_2+1)){feil_VALUE("Invalid IPv4 netmask");return;} int maske_VALUE=ADDRESS_VALUE;
        if(!주소읽기(Køyr_2+2)){feil_VALUE("Invalid IPv4 gateway");return;}
        int forretningsmål=Tavle.Nettverk_Innstillingar(0,ADDRESS,maske_VALUE,ADDRESS_VALUE);
        if(forretningsmål<0) { FEIL(forretningsmål); if(forretningsmål==-16)단말.Skriv("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Skriv("IPv4 configuration applied (until reboot)\n"); vise_Nettverk_merkje(); }
    }
    static void Nettverk_kommando(boolean IP_adresse) {
        if (vare_COUNT()==1 || vare_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || vare_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { vise_Nettverk_merkje();return; }
        if (IP_adresse && 같음(1,"route") && (vare_COUNT()==2 || vare_COUNT()==3&&같음(2,"show"))) { vise_bane();return; }
        if (같음(1,"set")) { sett_ADDRESS(2);return; }
        if (vare_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Tavle.Nettverk_Innstillingar(같음(1,"up")?1:2,0,0,0);vise_Nettverk_merkje();return; }
        if (IP_adresse && vare_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Tavle.Nettverk_Innstillingar(같음(5,"up")?1:2,0,0,0);vise_Nettverk_merkje();return; }
        feil_VALUE("사용법: ip [addr show|route show|set ADDRESS 주소가림 gateway_VALUE|link set dev sl0 up|down]");
    }
    static void vise_bane() {
        단말.Skriv("Destination Netmask Gateway Interface\n");
        skrive_ADDRESS(Tavle.Nettverk_merkje(0,0)&Tavle.Nettverk_merkje(1,0));단말.문자(' ');skrive_ADDRESS(Tavle.Nettverk_merkje(1,0));단말.Skriv(Tavle.Nettverk_merkje(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Tavle.Nettverk_merkje(2,0)!=0) {단말.Skriv("0.0.0.0 0.0.0.0 ");skrive_ADDRESS(Tavle.Nettverk_merkje(2,0));단말.Skriv(Tavle.Nettverk_merkje(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void vise_Nettverk() {
        단말.Skriv("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_kategori=Tavle.Nettverk_merkje(10,INDEX);if(TYPE_kategori==0)continue;
            단말.Skriv(TYPE_kategori==1?"TCP ":"UDP ");skrive_ADDRESS(Tavle.Nettverk_merkje(16,INDEX));단말.문자(':');단말.수(Tavle.Nettverk_merkje(11,INDEX));단말.문자(' ');
            skrive_ADDRESS(Tavle.Nettverk_merkje(12,INDEX));단말.문자(':');단말.수(Tavle.Nettverk_merkje(13,INDEX));단말.문자(' ');
            int status_VALUE=Tavle.Nettverk_merkje(14,INDEX);단말.Skriv(TYPE_kategori==2?"DATAGRAM":status_VALUE==1?"LISTEN":status_VALUE==2?"ESTABLISHED":status_VALUE==3?"CLOSE_WAIT":status_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Tavle.Nettverk_merkje(15,INDEX));단말.문자(10);
        }
        단말.Skriv("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean vent_status(int 밀리초) {
        int Køyr_2=Tavle.밀리초();
        while(Tavle.밀리초()-Køyr_2<밀리초) {
            if(셸입출력.informasjonsteknologi_interaktiv()!=0){int teikn_VALUE=Tavle.직렬읽기();if(teikn_VALUE==3 || teikn_VALUE=='q' || teikn_VALUE=='Q' || teikn_VALUE==27 || teikn_VALUE==-4096)return false;}
            Tavle.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, mål=-1;
        for(int plassere_INDEX=1;plassere_INDEX<vare_COUNT();plassere_INDEX++) {
            if(같음(plassere_INDEX,"-c")){횟수=siffer_VALUE(++plassere_INDEX,100);if(횟수<1){feil_VALUE("ping: -c 1..100");return;}}
            else if(같음(plassere_INDEX,"-W")){제한=siffer_VALUE(++plassere_INDEX,10);if(제한<1){feil_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(mål<0)mål=plassere_INDEX;else{feil_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(mål<0 || !주소읽기(mål)){feil_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADDRESS=ADDRESS_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Skriv("PING ");skrive_ADDRESS(ADDRESS);단말.Skriv(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int rekkjefølgje_VALUE=1;rekkjefølgje_VALUE<=횟수 && 계속;rekkjefølgje_VALUE++) {
            int 처리값=Tavle.응답보내기(ADDRESS,rekkjefølgje_VALUE);
            if(처리값<0){FEIL(처리값);break;}보낸수++;
            int Køyr_2=Tavle.밀리초();
            while(Tavle.응답읽기(0)==-11 && Tavle.밀리초()-Køyr_2<제한)if(!vent_status(1)){계속=false;break;}
            if(!계속)break;
            if(Tavle.응답읽기(0)==0){
                int TIME_VALUE=Tavle.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Skriv("32 bytes from ");skrive_ADDRESS(ADDRESS);단말.Skriv(" seq=");단말.수(rekkjefølgje_VALUE);단말.Skriv(" ttl=");단말.수(Tavle.응답읽기(2));단말.Skriv(" time=");단말.수(TIME_VALUE);단말.Skriv(" ms\n");
            }else{단말.Skriv("Request timeout seq=");단말.수(rekkjefølgje_VALUE);단말.문자(10);}
            if(rekkjefølgje_VALUE<횟수)계속=vent_status(200);
        }
        단말.수(보낸수);단말.Skriv(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Skriv(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Skriv("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Skriv("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Skriv(" ms\n");}
        명령해석기.forretningsmål=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void vise_Aktivitet() { 단말.Skriv("up ");단말.수(Tavle.밀리초()/1000);단말.Skriv(" seconds\n"); }
    static void vise_Minne() {
        수항목("ARM RAM KiB (firmware): ",Tavle.spørjing_system(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Tavle.spørjing_system(1,0));
        int 총량=Tavle.spørjing_system(2,0), 사용량=Tavle.spørjing_system(3,0);
        단말.Skriv("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Tavle.spørjing_system(4,0));
        수항목("EL0 arena+session reserve KiB: ",Tavle.spørjing_system(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Tavle.spørjing_system(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Skriv("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void vise_Tasks() {
        단말.Skriv("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Skriv("1 - RUN - - ");단말.수(Tavle.밀리초());단말.Skriv(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Tavle.oppgåve_status(INDEX)>0){단말.수(INDEX+1);단말.Skriv(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int status_VALUE=Tavle.spørjing_system(20,INDEX);if(status_VALUE==0)continue;
            단말.수(Tavle.spørjing_system(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Skriv(status_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(Tavle.spørjing_system(22,INDEX));단말.문자(' ');단말.수(Tavle.spørjing_system(24,INDEX));단말.문자(' ');단말.수(Tavle.spørjing_system(23,INDEX));단말.문자(' ');
            for(int plassere_INDEX=0;plassere_INDEX<288;plassere_INDEX++){int byte_VALUE=Tavle.spørjing_system(25,INDEX+plassere_INDEX*4);if(byte_VALUE==0)break;Tavle.직렬쓰기(byte_VALUE);}단말.문자(10);
        }
    }
    static void vise_Lagring() {
        int felt_COUNT=0, data_COUNT=0;
        for(int INDEX=0;INDEX<Minne_Filer.fil_COUNT;INDEX++)if(Minne_Filer.이름길이[INDEX]>0 || Minne_Filer.Oppslagsverk_COUNT[INDEX]>0){felt_COUNT++;data_COUNT+=Minne_Filer.lengd_VALUE[INDEX];}
        단말.Skriv("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Minne_Filer.fil_COUNT*16384);단말.문자(' ');단말.수(felt_COUNT*16384);단말.문자(' ');단말.수((Minne_Filer.fil_COUNT-felt_COUNT)*16384);단말.문자(' ');단말.수(data_COUNT);단말.문자(' ');단말.수(felt_COUNT);단말.문자('/');단말.수(Minne_Filer.fil_COUNT);단말.Skriv(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void vise_merkje() {
        int 횟수=셸입출력.informasjonsteknologi_interaktiv()!=0?0:1;
        if(vare_COUNT()>1){if(vare_COUNT()!=3 || !같음(1,"-n") || (횟수=siffer_VALUE(2,1000))<1){feil_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 avslutt_app");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.informasjonsteknologi_interaktiv()!=0 && 횟수==0)단말.Skriv("\u001b[2J\u001b[H");
            vise_Aktivitet();vise_Minne();vise_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!vent_status(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void vise_hjelp() {
        단말.Skriv("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Skriv(표준말(INDEX));단말.Skriv(" / ");단말.Skriv(관리명령.Word_SMS(INDEX));단말.Skriv(" : ");단말.Skriv(관리명령.설명(INDEX));단말.문자(10);}
        단말.Skriv("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Skriv("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Skriv("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Utfør_kommando() {
        int Kommando=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Kommando=INDEX;
        if(같음(0,"ifconfig"))Kommando=0;if(같음(0,"ss"))Kommando=4;
        if(Kommando<0)return false;
        if(Kommando==11){if(같음(1,"net") || 같음(1,"system"))vise_hjelp();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.vise_hjelp();return true;}
        if(Kommando==0 || Kommando==1)Nettverk_kommando(Kommando==1);
        else if(Kommando==2)응답시험();
        else if(Kommando==6)vise_merkje();
        else if(vare_COUNT()!=1){feil_VALUE("This command takes no arguments; help system");}
        else if(Kommando==3)vise_bane();else if(Kommando==4)vise_Nettverk();else if(Kommando==5)vise_Tasks();else if(Kommando==7)vise_Minne();else if(Kommando==8)vise_Lagring();else if(Kommando==9)vise_Aktivitet();
        else if(Kommando==10)Tavle.전원끄기();
        return true;
    }
}
