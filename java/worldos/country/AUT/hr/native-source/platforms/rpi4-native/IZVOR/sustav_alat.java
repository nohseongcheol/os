// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** stvaran_podaci jezgra_sustava_VALUE 상태를 읽는 IPv4·ICMP·작업·Memorija_VALUE·RAM spremište_korijen 관리 Naredba. */
public final class sustav_alat {
    static int adresa_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int artikl_COUNT() { return 명령해석기.token_COUNT; }
    static void kvar_VALUE(String 안내) { 명령해석기.REZULTAT=2; 단말.Zapisuj(안내); 단말.문자(10); }
    static void GREŠKA(int VALUE) { 명령해석기.GREŠKA(VALUE); }
    static void 수항목(String Ime, int VALUE) { 단말.Zapisuj(Ime); 단말.수(VALUE); 단말.문자(10); }
    static int znamenka_VALUE(int INDEX, int 한도) {
        if (INDEX>=artikl_COUNT() || 명령해석기.길이[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (znak_VALUE<0 || znak_VALUE>9 || VALUE>(한도-znak_VALUE)/10) return -1;
            VALUE=VALUE*10+znak_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=artikl_COUNT()) return false;
        int VALUE=0, blok_VALUE=0, znamenka_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (znak_VALUE=='.') { if (znamenka_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|blok_VALUE; blok_VALUE=znamenka_COUNT=0; }
            else { if (znak_VALUE<'0' || znak_VALUE>'9' || ++znamenka_COUNT>3) return false; blok_VALUE=blok_VALUE*10+znak_VALUE-'0'; if(blok_VALUE>255)return false; }
        }
        if (p_COUNT!=3 || znamenka_COUNT==0) return false;
        adresa_VALUE=(VALUE<<8)|blok_VALUE; return true;
    }
    static void zapisivanje_adresa(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void emisija_mreža_stanje() {
        단말.Zapisuj(pano.mreža_stanje(20,0)!=0?"en0: ":"sl0: "); 단말.Zapisuj(pano.mreža_stanje(3,0)!=0?"UP":"DOWN");
        단말.Zapisuj(pano.mreža_stanje(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Zapisuj(pano.mreža_stanje(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); zapisivanje_adresa(pano.mreža_stanje(0,0));
        단말.Zapisuj(" netmask "); zapisivanje_adresa(pano.mreža_stanje(1,0)); 단말.Zapisuj(" gateway "); zapisivanje_adresa(pano.mreža_stanje(2,0)); 단말.문자(10);
        단말.Zapisuj("  RX packets "); 단말.수(pano.mreža_stanje(4,0)); 단말.Zapisuj(" bytes "); 단말.수(pano.mreža_stanje(6,0));
        단말.Zapisuj(" TX packets "); 단말.수(pano.mreža_stanje(5,0)); 단말.Zapisuj(" bytes "); 단말.수(pano.mreža_stanje(7,0)); 단말.문자(10);
        수항목("  dropped ",pano.mreža_stanje(8,0));
    }
    static void skup_adresa(int Pokreni) {
        if (artikl_COUNT()!=Pokreni+3 || !주소읽기(Pokreni)) { kvar_VALUE("사용법: ipconfig set adresa 주소가림 pristupnik_VALUE"); return; }
        int adresa=adresa_VALUE;
        if(!주소읽기(Pokreni+1)){kvar_VALUE("Invalid IPv4 netmask");return;} int maska_VALUE=adresa_VALUE;
        if(!주소읽기(Pokreni+2)){kvar_VALUE("Invalid IPv4 gateway");return;}
        int REZULTAT=pano.mreža_Postavke(0,adresa,maska_VALUE,adresa_VALUE);
        if(REZULTAT<0) { GREŠKA(REZULTAT); if(REZULTAT==-16)단말.Zapisuj("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Zapisuj("IPv4 configuration applied (until reboot)\n"); emisija_mreža_stanje(); }
    }
    static void mreža_naredba(boolean IP_adresa) {
        if (artikl_COUNT()==1 || artikl_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || artikl_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { emisija_mreža_stanje();return; }
        if (IP_adresa && 같음(1,"route") && (artikl_COUNT()==2 || artikl_COUNT()==3&&같음(2,"show"))) { emisija_put();return; }
        if (같음(1,"set")) { skup_adresa(2);return; }
        if (artikl_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { pano.mreža_Postavke(같음(1,"up")?1:2,0,0,0);emisija_mreža_stanje();return; }
        if (IP_adresa && artikl_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { pano.mreža_Postavke(같음(5,"up")?1:2,0,0,0);emisija_mreža_stanje();return; }
        kvar_VALUE("사용법: ip [addr show|route show|set adresa 주소가림 pristupnik_VALUE|link set dev sl0 up|down]");
    }
    static void emisija_put() {
        단말.Zapisuj("Destination Netmask Gateway Interface\n");
        zapisivanje_adresa(pano.mreža_stanje(0,0)&pano.mreža_stanje(1,0));단말.문자(' ');zapisivanje_adresa(pano.mreža_stanje(1,0));단말.Zapisuj(pano.mreža_stanje(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (pano.mreža_stanje(2,0)!=0) {단말.Zapisuj("0.0.0.0 0.0.0.0 ");zapisivanje_adresa(pano.mreža_stanje(2,0));단말.Zapisuj(pano.mreža_stanje(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void emisija_mreža() {
        단말.Zapisuj("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_područje=pano.mreža_stanje(10,INDEX);if(TYPE_područje==0)continue;
            단말.Zapisuj(TYPE_područje==1?"TCP ":"UDP ");zapisivanje_adresa(pano.mreža_stanje(16,INDEX));단말.문자(':');단말.수(pano.mreža_stanje(11,INDEX));단말.문자(' ');
            zapisivanje_adresa(pano.mreža_stanje(12,INDEX));단말.문자(':');단말.수(pano.mreža_stanje(13,INDEX));단말.문자(' ');
            int Stanje_VALUE=pano.mreža_stanje(14,INDEX);단말.Zapisuj(TYPE_područje==2?"DATAGRAM":Stanje_VALUE==1?"LISTEN":Stanje_VALUE==2?"ESTABLISHED":Stanje_VALUE==3?"CLOSE_WAIT":Stanje_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(pano.mreža_stanje(15,INDEX));단말.문자(10);
        }
        단말.Zapisuj("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean stanje_čekanja(int 밀리초) {
        int Pokreni=pano.밀리초();
        while(pano.밀리초()-Pokreni<밀리초) {
            if(셸입출력.대화가능()!=0){int znak_VALUE=pano.직렬읽기();if(znak_VALUE==3 || znak_VALUE=='q' || znak_VALUE=='Q' || znak_VALUE==27 || znak_VALUE==-4096)return false;}
            pano.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, cilj=-1;
        for(int indeks_položaja=1;indeks_položaja<artikl_COUNT();indeks_položaja++) {
            if(같음(indeks_položaja,"-c")){횟수=znamenka_VALUE(++indeks_položaja,100);if(횟수<1){kvar_VALUE("ping: -c 1..100");return;}}
            else if(같음(indeks_položaja,"-W")){제한=znamenka_VALUE(++indeks_položaja,10);if(제한<1){kvar_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(cilj<0)cilj=indeks_položaja;else{kvar_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(cilj<0 || !주소읽기(cilj)){kvar_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int adresa=adresa_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Zapisuj("PING ");zapisivanje_adresa(adresa);단말.Zapisuj(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int narudžba_VALUE=1;narudžba_VALUE<=횟수 && 계속;narudžba_VALUE++) {
            int 처리값=pano.slati_odgovor(adresa,narudžba_VALUE);
            if(처리값<0){GREŠKA(처리값);break;}보낸수++;
            int Pokreni=pano.밀리초();
            while(pano.응답읽기(0)==-11 && pano.밀리초()-Pokreni<제한)if(!stanje_čekanja(1)){계속=false;break;}
            if(!계속)break;
            if(pano.응답읽기(0)==0){
                int TIME_VALUE=pano.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Zapisuj("32 bytes from ");zapisivanje_adresa(adresa);단말.Zapisuj(" seq=");단말.수(narudžba_VALUE);단말.Zapisuj(" ttl=");단말.수(pano.응답읽기(2));단말.Zapisuj(" time=");단말.수(TIME_VALUE);단말.Zapisuj(" ms\n");
            }else{단말.Zapisuj("Request timeout seq=");단말.수(narudžba_VALUE);단말.문자(10);}
            if(narudžba_VALUE<횟수)계속=stanje_čekanja(200);
        }
        단말.수(보낸수);단말.Zapisuj(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Zapisuj(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Zapisuj("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Zapisuj("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Zapisuj(" ms\n");}
        명령해석기.REZULTAT=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void emisija_Aktivnost() { 단말.Zapisuj("up ");단말.수(pano.밀리초()/1000);단말.Zapisuj(" seconds\n"); }
    static void emisija_Memorija() {
        수항목("ARM RAM KiB (firmware): ",pano.upit_sustav(0,0));
        수항목("Kernel image+BSS+stack KiB: ",pano.upit_sustav(1,0));
        int ukupni_zbroj_kapacitet=pano.upit_sustav(2,0), 사용량=pano.upit_sustav(3,0);
        단말.Zapisuj("AOT heap KiB total/used/free: ");단말.수(ukupni_zbroj_kapacitet);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(ukupni_zbroj_kapacitet-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",pano.upit_sustav(4,0));
        수항목("EL0 arena+session reserve KiB: ",pano.upit_sustav(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=pano.upit_sustav(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Zapisuj("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void emisija_Tasks() {
        단말.Zapisuj("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Zapisuj("1 - RUN - - ");단말.수(pano.밀리초());단말.Zapisuj(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(pano.obaveza_Stanje(INDEX)>0){단말.수(INDEX+1);단말.Zapisuj(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Stanje_VALUE=pano.upit_sustav(20,INDEX);if(Stanje_VALUE==0)continue;
            단말.수(pano.upit_sustav(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Zapisuj(Stanje_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(pano.upit_sustav(22,INDEX));단말.문자(' ');단말.수(pano.upit_sustav(24,INDEX));단말.문자(' ');단말.수(pano.upit_sustav(23,INDEX));단말.문자(' ');
            for(int indeks_položaja=0;indeks_položaja<288;indeks_položaja++){int bajt_VALUE=pano.upit_sustav(25,INDEX+indeks_položaja*4);if(bajt_VALUE==0)break;pano.직렬쓰기(bajt_VALUE);}단말.문자(10);
        }
    }
    static void emisija_Pohrana() {
        int 칸수=0, podaci_COUNT=0;
        for(int INDEX=0;INDEX<Memorija_Datoteke.Datoteka_COUNT;INDEX++)if(Memorija_Datoteke.이름길이[INDEX]>0 || Memorija_Datoteke.Reference_COUNT[INDEX]>0){칸수++;podaci_COUNT+=Memorija_Datoteke.길이[INDEX];}
        단말.Zapisuj("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memorija_Datoteke.Datoteka_COUNT*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((Memorija_Datoteke.Datoteka_COUNT-칸수)*16384);단말.문자(' ');단말.수(podaci_COUNT);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(Memorija_Datoteke.Datoteka_COUNT);단말.Zapisuj(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void emisija_stanje() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(artikl_COUNT()>1){if(artikl_COUNT()!=3 || !같음(1,"-n") || (횟수=znamenka_VALUE(2,1000))<1){kvar_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 izlaz_program");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Zapisuj("\u001b[2J\u001b[H");
            emisija_Aktivnost();emisija_Memorija();emisija_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!stanje_čekanja(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void emisija_pomoć() {
        단말.Zapisuj("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Zapisuj(표준말(INDEX));단말.Zapisuj(" / ");단말.Zapisuj(관리명령.Word_SMS(INDEX));단말.Zapisuj(" : ");단말.Zapisuj(관리명령.설명(INDEX));단말.문자(10);}
        단말.Zapisuj("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Zapisuj("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Zapisuj("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Izvrši_naredba() {
        int Naredba=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Naredba=INDEX;
        if(같음(0,"ifconfig"))Naredba=0;if(같음(0,"ss"))Naredba=4;
        if(Naredba<0)return false;
        if(Naredba==11){if(같음(1,"net") || 같음(1,"system"))emisija_pomoć();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.emisija_pomoć();return true;}
        if(Naredba==0 || Naredba==1)mreža_naredba(Naredba==1);
        else if(Naredba==2)응답시험();
        else if(Naredba==6)emisija_stanje();
        else if(artikl_COUNT()!=1){kvar_VALUE("This command takes no arguments; help system");}
        else if(Naredba==3)emisija_put();else if(Naredba==4)emisija_mreža();else if(Naredba==5)emisija_Tasks();else if(Naredba==7)emisija_Memorija();else if(Naredba==8)emisija_Pohrana();else if(Naredba==9)emisija_Aktivnost();
        else if(Naredba==10)pano.전원끄기();
        return true;
    }
}
