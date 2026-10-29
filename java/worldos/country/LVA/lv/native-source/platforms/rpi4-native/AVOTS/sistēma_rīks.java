// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktisks_dati kodols_VALUE 상태를 읽는 IPv4·ICMP·작업·atmiņa_VALUE·RAM repozitorijs_sakne 관리 Komanda. */
public final class sistēma_rīks {
    static int adrese_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int krājums_COUNT() { return 명령해석기.daļiņa_COUNT; }
    static void kļūme_VALUE(String fails_Lasi_mani_eb81d7d9) { 명령해석기.mērs=2; 단말.Rakstīt(fails_Lasi_mani_eb81d7d9); 단말.문자(10); }
    static void Kļūda(int VALUE) { 명령해석기.Kļūda(VALUE); }
    static void numurs_ievade(String Nosaukums, int VALUE) { 단말.Rakstīt(Nosaukums); 단말.numurs(VALUE); 단말.문자(10); }
    static int cipars_VALUE(int INDEX, int 한도) {
        if (INDEX>=krājums_COUNT() || 명령해석기.길이[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int rakstzīme_VALUE=명령해석기.daļiņa_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (rakstzīme_VALUE<0 || rakstzīme_VALUE>9 || VALUE>(한도-rakstzīme_VALUE)/10) return -1;
            VALUE=VALUE*10+rakstzīme_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=krājums_COUNT()) return false;
        int VALUE=0, porcija_VALUE=0, cipars_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int rakstzīme_VALUE=명령해석기.daļiņa_VALUE[명령해석기.시작점[INDEX]+순번];
            if (rakstzīme_VALUE=='.') { if (cipars_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|porcija_VALUE; porcija_VALUE=cipars_COUNT=0; }
            else { if (rakstzīme_VALUE<'0' || rakstzīme_VALUE>'9' || ++cipars_COUNT>3) return false; porcija_VALUE=porcija_VALUE*10+rakstzīme_VALUE-'0'; if(porcija_VALUE>255)return false; }
        }
        if (p_COUNT!=3 || cipars_COUNT==0) return false;
        adrese_VALUE=(VALUE<<8)|porcija_VALUE; return true;
    }
    static void rakstīšana_adrese(int VALUE) {
        단말.numurs((VALUE>>>24)&255); 단말.문자('.'); 단말.numurs((VALUE>>>16)&255); 단말.문자('.');
        단말.numurs((VALUE>>>8)&255); 단말.문자('.'); 단말.numurs(VALUE&255);
    }
    static void rādīt_tīkls_statuss() {
        단말.Rakstīt(Panelis.tīkls_statuss(20,0)!=0?"en0: ":"sl0: "); 단말.Rakstīt(Panelis.tīkls_statuss(3,0)!=0?"UP":"DOWN");
        단말.Rakstīt(Panelis.tīkls_statuss(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Rakstīt(Panelis.tīkls_statuss(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); rakstīšana_adrese(Panelis.tīkls_statuss(0,0));
        단말.Rakstīt(" netmask "); rakstīšana_adrese(Panelis.tīkls_statuss(1,0)); 단말.Rakstīt(" gateway "); rakstīšana_adrese(Panelis.tīkls_statuss(2,0)); 단말.문자(10);
        단말.Rakstīt("  RX packets "); 단말.numurs(Panelis.tīkls_statuss(4,0)); 단말.Rakstīt(" bytes "); 단말.numurs(Panelis.tīkls_statuss(6,0));
        단말.Rakstīt(" TX packets "); 단말.numurs(Panelis.tīkls_statuss(5,0)); 단말.Rakstīt(" bytes "); 단말.numurs(Panelis.tīkls_statuss(7,0)); 단말.문자(10);
        numurs_ievade("  dropped ",Panelis.tīkls_statuss(8,0));
    }
    static void kopa_adrese(int Palaist) {
        if (krājums_COUNT()!=Palaist+3 || !주소읽기(Palaist)) { kļūme_VALUE("사용법: ipconfig set adrese 주소가림 vārteja_VALUE"); return; }
        int adrese=adrese_VALUE;
        if(!주소읽기(Palaist+1)){kļūme_VALUE("Invalid IPv4 netmask");return;} int maska_VALUE=adrese_VALUE;
        if(!주소읽기(Palaist+2)){kļūme_VALUE("Invalid IPv4 gateway");return;}
        int mērs=Panelis.tīkls_Iestatījumi(0,adrese,maska_VALUE,adrese_VALUE);
        if(mērs<0) { Kļūda(mērs); if(mērs==-16)단말.Rakstīt("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Rakstīt("IPv4 configuration applied (until reboot)\n"); rādīt_tīkls_statuss(); }
    }
    static void tīkls_komanda(boolean IP_adrese) {
        if (krājums_COUNT()==1 || krājums_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || krājums_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { rādīt_tīkls_statuss();return; }
        if (IP_adrese && 같음(1,"route") && (krājums_COUNT()==2 || krājums_COUNT()==3&&같음(2,"show"))) { rādīt_ceļš();return; }
        if (같음(1,"set")) { kopa_adrese(2);return; }
        if (krājums_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Panelis.tīkls_Iestatījumi(같음(1,"up")?1:2,0,0,0);rādīt_tīkls_statuss();return; }
        if (IP_adrese && krājums_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Panelis.tīkls_Iestatījumi(같음(5,"up")?1:2,0,0,0);rādīt_tīkls_statuss();return; }
        kļūme_VALUE("사용법: ip [addr show|route show|set adrese 주소가림 vārteja_VALUE|link set dev sl0 up|down]");
    }
    static void rādīt_ceļš() {
        단말.Rakstīt("Destination Netmask Gateway Interface\n");
        rakstīšana_adrese(Panelis.tīkls_statuss(0,0)&Panelis.tīkls_statuss(1,0));단말.문자(' ');rakstīšana_adrese(Panelis.tīkls_statuss(1,0));단말.Rakstīt(Panelis.tīkls_statuss(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Panelis.tīkls_statuss(2,0)!=0) {단말.Rakstīt("0.0.0.0 0.0.0.0 ");rakstīšana_adrese(Panelis.tīkls_statuss(2,0));단말.Rakstīt(Panelis.tīkls_statuss(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void rādīt_tīkls() {
        단말.Rakstīt("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_joma=Panelis.tīkls_statuss(10,INDEX);if(TYPE_joma==0)continue;
            단말.Rakstīt(TYPE_joma==1?"TCP ":"UDP ");rakstīšana_adrese(Panelis.tīkls_statuss(16,INDEX));단말.문자(':');단말.numurs(Panelis.tīkls_statuss(11,INDEX));단말.문자(' ');
            rakstīšana_adrese(Panelis.tīkls_statuss(12,INDEX));단말.문자(':');단말.numurs(Panelis.tīkls_statuss(13,INDEX));단말.문자(' ');
            int Statuss_VALUE=Panelis.tīkls_statuss(14,INDEX);단말.Rakstīt(TYPE_joma==2?"DATAGRAM":Statuss_VALUE==1?"LISTEN":Statuss_VALUE==2?"ESTABLISHED":Statuss_VALUE==3?"CLOSE_WAIT":Statuss_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.numurs(Panelis.tīkls_statuss(15,INDEX));단말.문자(10);
        }
        단말.Rakstīt("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean nogaides_stāvoklis(int 밀리초) {
        int Palaist=Panelis.밀리초();
        while(Panelis.밀리초()-Palaist<밀리초) {
            if(셸입출력.대화가능()!=0){int rakstzīme_VALUE=Panelis.직렬읽기();if(rakstzīme_VALUE==3 || rakstzīme_VALUE=='q' || rakstzīme_VALUE=='Q' || rakstzīme_VALUE==27 || rakstzīme_VALUE==-4096)return false;}
            Panelis.YIELD_apstrādātājs();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, mērķis=-1;
        for(int pozīcijas_indekss=1;pozīcijas_indekss<krājums_COUNT();pozīcijas_indekss++) {
            if(같음(pozīcijas_indekss,"-c")){횟수=cipars_VALUE(++pozīcijas_indekss,100);if(횟수<1){kļūme_VALUE("ping: -c 1..100");return;}}
            else if(같음(pozīcijas_indekss,"-W")){제한=cipars_VALUE(++pozīcijas_indekss,10);if(제한<1){kļūme_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(mērķis<0)mērķis=pozīcijas_indekss;else{kļūme_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(mērķis<0 || !주소읽기(mērķis)){kļūme_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int adrese=adrese_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Rakstīt("PING ");rakstīšana_adrese(adrese);단말.Rakstīt(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int secība_VALUE=1;secība_VALUE<=횟수 && 계속;secība_VALUE++) {
            int 처리값=Panelis.sūtīt_atbilde(adrese,secība_VALUE);
            if(처리값<0){Kļūda(처리값);break;}보낸수++;
            int Palaist=Panelis.밀리초();
            while(Panelis.응답읽기(0)==-11 && Panelis.밀리초()-Palaist<제한)if(!nogaides_stāvoklis(1)){계속=false;break;}
            if(!계속)break;
            if(Panelis.응답읽기(0)==0){
                int TIME_VALUE=Panelis.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Rakstīt("32 bytes from ");rakstīšana_adrese(adrese);단말.Rakstīt(" seq=");단말.numurs(secība_VALUE);단말.Rakstīt(" ttl=");단말.numurs(Panelis.응답읽기(2));단말.Rakstīt(" time=");단말.numurs(TIME_VALUE);단말.Rakstīt(" ms\n");
            }else{단말.Rakstīt("Request timeout seq=");단말.numurs(secība_VALUE);단말.문자(10);}
            if(secība_VALUE<횟수)계속=nogaides_stāvoklis(200);
        }
        단말.numurs(보낸수);단말.Rakstīt(" transmitted, ");단말.numurs(RECEIVED_COUNT);단말.Rakstīt(" received, ");단말.numurs(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Rakstīt("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Rakstīt("rtt min/avg/max = ");단말.numurs(최솟값);단말.문자('/');단말.numurs(누적/RECEIVED_COUNT);단말.문자('/');단말.numurs(최댓값);단말.Rakstīt(" ms\n");}
        명령해석기.mērs=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void rādīt_darbība() { 단말.Rakstīt("up ");단말.numurs(Panelis.밀리초()/1000);단말.Rakstīt(" seconds\n"); }
    static void rādīt_atmiņa() {
        numurs_ievade("ARM RAM KiB (firmware): ",Panelis.vaicāt_sistēma(0,0));
        numurs_ievade("Kernel image+BSS+stack KiB: ",Panelis.vaicāt_sistēma(1,0));
        int kopsumma_noslodze=Panelis.vaicāt_sistēma(2,0), 사용량=Panelis.vaicāt_sistēma(3,0);
        단말.Rakstīt("AOT heap KiB total/used/free: ");단말.numurs(kopsumma_noslodze);단말.문자('/');단말.numurs(사용량);단말.문자('/');단말.numurs(kopsumma_noslodze-사용량);단말.문자(10);
        numurs_ievade("Framebuffer KiB: ",Panelis.vaicāt_sistēma(4,0));
        numurs_ievade("EL0 arena+session reserve KiB: ",Panelis.vaicāt_sistēma(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Panelis.vaicāt_sistēma(22,INDEX);
        numurs_ievade("EL0 mapped KiB: ",매핑);
        단말.Rakstīt("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void rādīt_Tasks() {
        단말.Rakstīt("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Rakstīt("1 - RUN - - ");단말.numurs(Panelis.밀리초());단말.Rakstīt(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Panelis.uzdevums_Statuss(INDEX)>0){단말.numurs(INDEX+1);단말.Rakstīt(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Statuss_VALUE=Panelis.vaicāt_sistēma(20,INDEX);if(Statuss_VALUE==0)continue;
            단말.numurs(Panelis.vaicāt_sistēma(21,INDEX));단말.문자(' ');단말.numurs(INDEX);단말.Rakstīt(Statuss_VALUE==1?" RUN ":" SUSPENDED ");
            단말.numurs(Panelis.vaicāt_sistēma(22,INDEX));단말.문자(' ');단말.numurs(Panelis.vaicāt_sistēma(24,INDEX));단말.문자(' ');단말.numurs(Panelis.vaicāt_sistēma(23,INDEX));단말.문자(' ');
            for(int pozīcijas_indekss=0;pozīcijas_indekss<288;pozīcijas_indekss++){int byte_VALUE=Panelis.vaicāt_sistēma(25,INDEX+pozīcijas_indekss*4);if(byte_VALUE==0)break;Panelis.직렬쓰기(byte_VALUE);}단말.문자(10);
        }
    }
    static void rādīt_Krātuve() {
        int 칸수=0, dati_COUNT=0;
        for(int INDEX=0;INDEX<atmiņa_Faili.Fails_COUNT;INDEX++)if(atmiņa_Faili.이름길이[INDEX]>0 || atmiņa_Faili.Uzziņas_COUNT[INDEX]>0){칸수++;dati_COUNT+=atmiņa_Faili.길이[INDEX];}
        단말.Rakstīt("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.numurs(atmiņa_Faili.Fails_COUNT*16384);단말.문자(' ');단말.numurs(칸수*16384);단말.문자(' ');단말.numurs((atmiņa_Faili.Fails_COUNT-칸수)*16384);단말.문자(' ');단말.numurs(dati_COUNT);단말.문자(' ');단말.numurs(칸수);단말.문자('/');단말.numurs(atmiņa_Faili.Fails_COUNT);단말.Rakstīt(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void rādīt_statuss() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(krājums_COUNT()>1){if(krājums_COUNT()!=3 || !같음(1,"-n") || (횟수=cipars_VALUE(2,1000))<1){kļūme_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 iziet_programma");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Rakstīt("\u001b[2J\u001b[H");
            rādīt_darbība();rādīt_atmiņa();rādīt_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!nogaides_stāvoklis(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void rādīt_palīdzība() {
        단말.Rakstīt("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Rakstīt(표준말(INDEX));단말.Rakstīt(" / ");단말.Rakstīt(관리명령.Word_SMS(INDEX));단말.Rakstīt(" : ");단말.Rakstīt(관리명령.설명(INDEX));단말.문자(10);}
        단말.Rakstīt("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Rakstīt("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Rakstīt("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Izpildīt_komanda() {
        int Komanda=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Komanda=INDEX;
        if(같음(0,"ifconfig"))Komanda=0;if(같음(0,"ss"))Komanda=4;
        if(Komanda<0)return false;
        if(Komanda==11){if(같음(1,"net") || 같음(1,"system"))rādīt_palīdzība();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.rādīt_palīdzība();return true;}
        if(Komanda==0 || Komanda==1)tīkls_komanda(Komanda==1);
        else if(Komanda==2)응답시험();
        else if(Komanda==6)rādīt_statuss();
        else if(krājums_COUNT()!=1){kļūme_VALUE("This command takes no arguments; help system");}
        else if(Komanda==3)rādīt_ceļš();else if(Komanda==4)rādīt_tīkls();else if(Komanda==5)rādīt_Tasks();else if(Komanda==7)rādīt_atmiņa();else if(Komanda==8)rādīt_Krātuve();else if(Komanda==9)rādīt_darbība();
        else if(Komanda==10)Panelis.전원끄기();
        return true;
    }
}
