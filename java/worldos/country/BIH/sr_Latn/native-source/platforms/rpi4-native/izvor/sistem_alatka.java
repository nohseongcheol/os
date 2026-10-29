// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** stvarni_podaci jezgro_VALUE 상태를 읽는 IPv4·ICMP·작업·Memorija_VALUE·RAM depo_koren 관리 komanda. */
public final class sistem_alatka {
    static int adresa_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int stavka_COUNT() { return 명령해석기.token_COUNT; }
    static void otkazivanje_VALUE(String 안내) { 명령해석기.KR=2; 단말.쓰기(안내); 단말.문자(10); }
    static void greška(int VALUE) { 명령해석기.greška(VALUE); }
    static void 수항목(String ime, int VALUE) { 단말.쓰기(ime); 단말.수(VALUE); 단말.문자(10); }
    static int cifra_VALUE(int INDEX, int 한도) {
        if (INDEX>=stavka_COUNT() || 명령해석기.길이[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (znak_VALUE<0 || znak_VALUE>9 || VALUE>(한도-znak_VALUE)/10) return -1;
            VALUE=VALUE*10+znak_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=stavka_COUNT()) return false;
        int VALUE=0, odlomak_VALUE=0, cifra_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (znak_VALUE=='.') { if (cifra_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|odlomak_VALUE; odlomak_VALUE=cifra_COUNT=0; }
            else { if (znak_VALUE<'0' || znak_VALUE>'9' || ++cifra_COUNT>3) return false; odlomak_VALUE=odlomak_VALUE*10+znak_VALUE-'0'; if(odlomak_VALUE>255)return false; }
        }
        if (p_COUNT!=3 || cifra_COUNT==0) return false;
        adresa_VALUE=(VALUE<<8)|odlomak_VALUE; return true;
    }
    static void 주소쓰기(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void emisija_Mreža_status() {
        단말.쓰기(Tabla.Mreža_status(20,0)!=0?"en0: ":"sl0: "); 단말.쓰기(Tabla.Mreža_status(3,0)!=0?"UP":"DOWN");
        단말.쓰기(Tabla.Mreža_status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.쓰기(Tabla.Mreža_status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); 주소쓰기(Tabla.Mreža_status(0,0));
        단말.쓰기(" netmask "); 주소쓰기(Tabla.Mreža_status(1,0)); 단말.쓰기(" gateway "); 주소쓰기(Tabla.Mreža_status(2,0)); 단말.문자(10);
        단말.쓰기("  RX packets "); 단말.수(Tabla.Mreža_status(4,0)); 단말.쓰기(" bytes "); 단말.수(Tabla.Mreža_status(6,0));
        단말.쓰기(" TX packets "); 단말.수(Tabla.Mreža_status(5,0)); 단말.쓰기(" bytes "); 단말.수(Tabla.Mreža_status(7,0)); 단말.문자(10);
        수항목("  dropped ",Tabla.Mreža_status(8,0));
    }
    static void skup_adresa(int koristiti) {
        if (stavka_COUNT()!=koristiti+3 || !주소읽기(koristiti)) { otkazivanje_VALUE("사용법: ipconfig set adresa 주소가림 mrežni_prolaz_VALUE"); return; }
        int adresa=adresa_VALUE;
        if(!주소읽기(koristiti+1)){otkazivanje_VALUE("Invalid IPv4 netmask");return;} int maska_VALUE=adresa_VALUE;
        if(!주소읽기(koristiti+2)){otkazivanje_VALUE("Invalid IPv4 gateway");return;}
        int KR=Tabla.Mreža_Postavke(0,adresa,maska_VALUE,adresa_VALUE);
        if(KR<0) { greška(KR); if(KR==-16)단말.쓰기("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.쓰기("IPv4 configuration applied (until reboot)\n"); emisija_Mreža_status(); }
    }
    static void Mreža_komanda(boolean IP_adresa) {
        if (stavka_COUNT()==1 || stavka_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || stavka_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { emisija_Mreža_status();return; }
        if (IP_adresa && 같음(1,"route") && (stavka_COUNT()==2 || stavka_COUNT()==3&&같음(2,"show"))) { emisija_putanja();return; }
        if (같음(1,"set")) { skup_adresa(2);return; }
        if (stavka_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Tabla.Mreža_Postavke(같음(1,"up")?1:2,0,0,0);emisija_Mreža_status();return; }
        if (IP_adresa && stavka_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Tabla.Mreža_Postavke(같음(5,"up")?1:2,0,0,0);emisija_Mreža_status();return; }
        otkazivanje_VALUE("사용법: ip [addr show|route show|set adresa 주소가림 mrežni_prolaz_VALUE|link set dev sl0 up|down]");
    }
    static void emisija_putanja() {
        단말.쓰기("Destination Netmask Gateway Interface\n");
        주소쓰기(Tabla.Mreža_status(0,0)&Tabla.Mreža_status(1,0));단말.문자(' ');주소쓰기(Tabla.Mreža_status(1,0));단말.쓰기(Tabla.Mreža_status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Tabla.Mreža_status(2,0)!=0) {단말.쓰기("0.0.0.0 0.0.0.0 ");주소쓰기(Tabla.Mreža_status(2,0));단말.쓰기(Tabla.Mreža_status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void emisija_Mreža() {
        단말.쓰기("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int tip_oblast=Tabla.Mreža_status(10,INDEX);if(tip_oblast==0)continue;
            단말.쓰기(tip_oblast==1?"TCP ":"UDP ");주소쓰기(Tabla.Mreža_status(16,INDEX));단말.문자(':');단말.수(Tabla.Mreža_status(11,INDEX));단말.문자(' ');
            주소쓰기(Tabla.Mreža_status(12,INDEX));단말.문자(':');단말.수(Tabla.Mreža_status(13,INDEX));단말.문자(' ');
            int Status_VALUE=Tabla.Mreža_status(14,INDEX);단말.쓰기(tip_oblast==2?"DATAGRAM":Status_VALUE==1?"LISTEN":Status_VALUE==2?"ESTABLISHED":Status_VALUE==3?"CLOSE_WAIT":Status_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Tabla.Mreža_status(15,INDEX));단말.문자(10);
        }
        단말.쓰기("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean stanje_čekanja(int 밀리초) {
        int koristiti=Tabla.밀리초();
        while(Tabla.밀리초()-koristiti<밀리초) {
            if(셸입출력.대화가능()!=0){int znak_VALUE=Tabla.직렬읽기();if(znak_VALUE==3 || znak_VALUE=='q' || znak_VALUE=='Q' || znak_VALUE==27 || znak_VALUE==-4096)return false;}
            Tabla.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, cilj=-1;
        for(int indeks_pozicije=1;indeks_pozicije<stavka_COUNT();indeks_pozicije++) {
            if(같음(indeks_pozicije,"-c")){횟수=cifra_VALUE(++indeks_pozicije,100);if(횟수<1){otkazivanje_VALUE("ping: -c 1..100");return;}}
            else if(같음(indeks_pozicije,"-W")){제한=cifra_VALUE(++indeks_pozicije,10);if(제한<1){otkazivanje_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(cilj<0)cilj=indeks_pozicije;else{otkazivanje_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(cilj<0 || !주소읽기(cilj)){otkazivanje_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int adresa=adresa_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.쓰기("PING ");주소쓰기(adresa);단말.쓰기(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int poručiti_VALUE=1;poručiti_VALUE<=횟수 && 계속;poručiti_VALUE++) {
            int 처리값=Tabla.poslati_odgovor(adresa,poručiti_VALUE);
            if(처리값<0){greška(처리값);break;}보낸수++;
            int koristiti=Tabla.밀리초();
            while(Tabla.응답읽기(0)==-11 && Tabla.밀리초()-koristiti<제한)if(!stanje_čekanja(1)){계속=false;break;}
            if(!계속)break;
            if(Tabla.응답읽기(0)==0){
                int TIME_VALUE=Tabla.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.쓰기("32 bytes from ");주소쓰기(adresa);단말.쓰기(" seq=");단말.수(poručiti_VALUE);단말.쓰기(" ttl=");단말.수(Tabla.응답읽기(2));단말.쓰기(" time=");단말.수(TIME_VALUE);단말.쓰기(" ms\n");
            }else{단말.쓰기("Request timeout seq=");단말.수(poručiti_VALUE);단말.문자(10);}
            if(poručiti_VALUE<횟수)계속=stanje_čekanja(200);
        }
        단말.수(보낸수);단말.쓰기(" transmitted, ");단말.수(RECEIVED_COUNT);단말.쓰기(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.쓰기("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.쓰기("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.쓰기(" ms\n");}
        명령해석기.KR=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void emisija_Aktivnost() { 단말.쓰기("up ");단말.수(Tabla.밀리초()/1000);단말.쓰기(" seconds\n"); }
    static void emisija_Memorija() {
        수항목("ARM RAM KiB (firmware): ",Tabla.upit_sistem(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Tabla.upit_sistem(1,0));
        int ukupan_kapacitet=Tabla.upit_sistem(2,0), 사용량=Tabla.upit_sistem(3,0);
        단말.쓰기("AOT heap KiB total/used/free: ");단말.수(ukupan_kapacitet);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(ukupan_kapacitet-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Tabla.upit_sistem(4,0));
        수항목("EL0 arena+session reserve KiB: ",Tabla.upit_sistem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Tabla.upit_sistem(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.쓰기("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void emisija_Tasks() {
        단말.쓰기("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.쓰기("1 - RUN - - ");단말.수(Tabla.밀리초());단말.쓰기(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Tabla.obaveza_Status(INDEX)>0){단말.수(INDEX+1);단말.쓰기(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Status_VALUE=Tabla.upit_sistem(20,INDEX);if(Status_VALUE==0)continue;
            단말.수(Tabla.upit_sistem(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.쓰기(Status_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(Tabla.upit_sistem(22,INDEX));단말.문자(' ');단말.수(Tabla.upit_sistem(24,INDEX));단말.문자(' ');단말.수(Tabla.upit_sistem(23,INDEX));단말.문자(' ');
            for(int indeks_pozicije=0;indeks_pozicije<288;indeks_pozicije++){int bajt_VALUE=Tabla.upit_sistem(25,INDEX+indeks_pozicije*4);if(bajt_VALUE==0)break;Tabla.직렬쓰기(bajt_VALUE);}단말.문자(10);
        }
    }
    static void emisija_Skladište() {
        int 칸수=0, podaci_COUNT=0;
        for(int INDEX=0;INDEX<Memorija_Datoteke.Datoteka_COUNT;INDEX++)if(Memorija_Datoteke.이름길이[INDEX]>0 || Memorija_Datoteke.referenca_COUNT[INDEX]>0){칸수++;podaci_COUNT+=Memorija_Datoteke.길이[INDEX];}
        단말.쓰기("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memorija_Datoteke.Datoteka_COUNT*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((Memorija_Datoteke.Datoteka_COUNT-칸수)*16384);단말.문자(' ');단말.수(podaci_COUNT);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(Memorija_Datoteke.Datoteka_COUNT);단말.쓰기(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void emisija_status() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(stavka_COUNT()>1){if(stavka_COUNT()!=3 || !같음(1,"-n") || (횟수=cifra_VALUE(2,1000))<1){otkazivanje_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 Napusti_program");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.쓰기("\u001b[2J\u001b[H");
            emisija_Aktivnost();emisija_Memorija();emisija_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!stanje_čekanja(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void emisija_pomoć_na_mreži() {
        단말.쓰기("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.쓰기(표준말(INDEX));단말.쓰기(" / ");단말.쓰기(관리명령.Word_SMS(INDEX));단말.쓰기(" : ");단말.쓰기(관리명령.설명(INDEX));단말.문자(10);}
        단말.쓰기("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.쓰기("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.쓰기("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Izvrši_komanda() {
        int komanda=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))komanda=INDEX;
        if(같음(0,"ifconfig"))komanda=0;if(같음(0,"ss"))komanda=4;
        if(komanda<0)return false;
        if(komanda==11){if(같음(1,"net") || 같음(1,"system"))emisija_pomoć_na_mreži();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.emisija_pomoć_na_mreži();return true;}
        if(komanda==0 || komanda==1)Mreža_komanda(komanda==1);
        else if(komanda==2)응답시험();
        else if(komanda==6)emisija_status();
        else if(stavka_COUNT()!=1){otkazivanje_VALUE("This command takes no arguments; help system");}
        else if(komanda==3)emisija_putanja();else if(komanda==4)emisija_Mreža();else if(komanda==5)emisija_Tasks();else if(komanda==7)emisija_Memorija();else if(komanda==8)emisija_Skladište();else if(komanda==9)emisija_Aktivnost();
        else if(komanda==10)Tabla.전원끄기();
        return true;
    }
}
