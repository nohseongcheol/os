// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** dejanski_podatki jedro_VALUE 상태를 읽는 IPv4·ICMP·작업·pomnilnik_VALUE·RAM shramba_koren 관리 Ukaz. */
public final class sistem_orodje {
    static int naslov_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int element_COUNT() { return 명령해석기.žeton_COUNT; }
    static void napaka_VALUE(String 안내) { 명령해석기.REZULTAT=2; 단말.Pisanje(안내); 단말.문자(10); }
    static void NAPAKA(int VALUE) { 명령해석기.NAPAKA(VALUE); }
    static void 수항목(String Ime, int VALUE) { 단말.Pisanje(Ime); 단말.수(VALUE); 단말.문자(10); }
    static int številka_VALUE(int INDEX, int 한도) {
        if (INDEX>=element_COUNT() || 명령해석기.길이[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.žeton_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (znak_VALUE<0 || znak_VALUE>9 || VALUE>(한도-znak_VALUE)/10) return -1;
            VALUE=VALUE*10+znak_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=element_COUNT()) return false;
        int VALUE=0, košček_VALUE=0, številka_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.žeton_VALUE[명령해석기.시작점[INDEX]+순번];
            if (znak_VALUE=='.') { if (številka_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|košček_VALUE; košček_VALUE=številka_COUNT=0; }
            else { if (znak_VALUE<'0' || znak_VALUE>'9' || ++številka_COUNT>3) return false; košček_VALUE=košček_VALUE*10+znak_VALUE-'0'; if(košček_VALUE>255)return false; }
        }
        if (p_COUNT!=3 || številka_COUNT==0) return false;
        naslov_VALUE=(VALUE<<8)|košček_VALUE; return true;
    }
    static void pisati_naslov(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void oddaja_mreža_stanje() {
        단말.Pisanje(Tabla.mreža_stanje(20,0)!=0?"en0: ":"sl0: "); 단말.Pisanje(Tabla.mreža_stanje(3,0)!=0?"UP":"DOWN");
        단말.Pisanje(Tabla.mreža_stanje(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Pisanje(Tabla.mreža_stanje(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); pisati_naslov(Tabla.mreža_stanje(0,0));
        단말.Pisanje(" netmask "); pisati_naslov(Tabla.mreža_stanje(1,0)); 단말.Pisanje(" gateway "); pisati_naslov(Tabla.mreža_stanje(2,0)); 단말.문자(10);
        단말.Pisanje("  RX packets "); 단말.수(Tabla.mreža_stanje(4,0)); 단말.Pisanje(" bytes "); 단말.수(Tabla.mreža_stanje(6,0));
        단말.Pisanje(" TX packets "); 단말.수(Tabla.mreža_stanje(5,0)); 단말.Pisanje(" bytes "); 단말.수(Tabla.mreža_stanje(7,0)); 단말.문자(10);
        수항목("  dropped ",Tabla.mreža_stanje(8,0));
    }
    static void nabor_naslov(int Zaženi) {
        if (element_COUNT()!=Zaženi+3 || !주소읽기(Zaženi)) { napaka_VALUE("사용법: ipconfig set naslov 주소가림 prehod_VALUE"); return; }
        int naslov=naslov_VALUE;
        if(!주소읽기(Zaženi+1)){napaka_VALUE("Invalid IPv4 netmask");return;} int maska_VALUE=naslov_VALUE;
        if(!주소읽기(Zaženi+2)){napaka_VALUE("Invalid IPv4 gateway");return;}
        int REZULTAT=Tabla.mreža_Nastavitve(0,naslov,maska_VALUE,naslov_VALUE);
        if(REZULTAT<0) { NAPAKA(REZULTAT); if(REZULTAT==-16)단말.Pisanje("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Pisanje("IPv4 configuration applied (until reboot)\n"); oddaja_mreža_stanje(); }
    }
    static void mreža_ukaz(boolean naslov_IP) {
        if (element_COUNT()==1 || element_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || element_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { oddaja_mreža_stanje();return; }
        if (naslov_IP && 같음(1,"route") && (element_COUNT()==2 || element_COUNT()==3&&같음(2,"show"))) { oddaja_pot();return; }
        if (같음(1,"set")) { nabor_naslov(2);return; }
        if (element_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Tabla.mreža_Nastavitve(같음(1,"up")?1:2,0,0,0);oddaja_mreža_stanje();return; }
        if (naslov_IP && element_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Tabla.mreža_Nastavitve(같음(5,"up")?1:2,0,0,0);oddaja_mreža_stanje();return; }
        napaka_VALUE("사용법: ip [addr show|route show|set naslov 주소가림 prehod_VALUE|link set dev sl0 up|down]");
    }
    static void oddaja_pot() {
        단말.Pisanje("Destination Netmask Gateway Interface\n");
        pisati_naslov(Tabla.mreža_stanje(0,0)&Tabla.mreža_stanje(1,0));단말.문자(' ');pisati_naslov(Tabla.mreža_stanje(1,0));단말.Pisanje(Tabla.mreža_stanje(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Tabla.mreža_stanje(2,0)!=0) {단말.Pisanje("0.0.0.0 0.0.0.0 ");pisati_naslov(Tabla.mreža_stanje(2,0));단말.Pisanje(Tabla.mreža_stanje(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void oddaja_mreža() {
        단말.Pisanje("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int Tip_območje=Tabla.mreža_stanje(10,INDEX);if(Tip_območje==0)continue;
            단말.Pisanje(Tip_območje==1?"TCP ":"UDP ");pisati_naslov(Tabla.mreža_stanje(16,INDEX));단말.문자(':');단말.수(Tabla.mreža_stanje(11,INDEX));단말.문자(' ');
            pisati_naslov(Tabla.mreža_stanje(12,INDEX));단말.문자(':');단말.수(Tabla.mreža_stanje(13,INDEX));단말.문자(' ');
            int stanje_VALUE=Tabla.mreža_stanje(14,INDEX);단말.Pisanje(Tip_območje==2?"DATAGRAM":stanje_VALUE==1?"LISTEN":stanje_VALUE==2?"ESTABLISHED":stanje_VALUE==3?"CLOSE_WAIT":stanje_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Tabla.mreža_stanje(15,INDEX));단말.문자(10);
        }
        단말.Pisanje("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean čakalno_stanje(int 밀리초) {
        int Zaženi=Tabla.밀리초();
        while(Tabla.밀리초()-Zaženi<밀리초) {
            if(셸입출력.informacijska_tehnologija_interaktiven()!=0){int znak_VALUE=Tabla.직렬읽기();if(znak_VALUE==3 || znak_VALUE=='q' || znak_VALUE=='Q' || znak_VALUE==27 || znak_VALUE==-4096)return false;}
            Tabla.YIELD_CPE();
        }
        return true;
    }
    static void preskusiti_odziv() {
        int 횟수=4, 제한=1000, tarča=-1;
        for(int kazalec_mesta=1;kazalec_mesta<element_COUNT();kazalec_mesta++) {
            if(같음(kazalec_mesta,"-c")){횟수=številka_VALUE(++kazalec_mesta,100);if(횟수<1){napaka_VALUE("ping: -c 1..100");return;}}
            else if(같음(kazalec_mesta,"-W")){제한=številka_VALUE(++kazalec_mesta,10);if(제한<1){napaka_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(tarča<0)tarča=kazalec_mesta;else{napaka_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(tarča<0 || !주소읽기(tarča)){napaka_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int naslov=naslov_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Pisanje("PING ");pisati_naslov(naslov);단말.Pisanje(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int naročilo_VALUE=1;naročilo_VALUE<=횟수 && 계속;naročilo_VALUE++) {
            int 처리값=Tabla.poslati_odziv(naslov,naročilo_VALUE);
            if(처리값<0){NAPAKA(처리값);break;}보낸수++;
            int Zaženi=Tabla.밀리초();
            while(Tabla.응답읽기(0)==-11 && Tabla.밀리초()-Zaženi<제한)if(!čakalno_stanje(1)){계속=false;break;}
            if(!계속)break;
            if(Tabla.응답읽기(0)==0){
                int čas_VALUE=Tabla.응답읽기(1);RECEIVED_COUNT++;누적+=čas_VALUE;if(čas_VALUE<최솟값)최솟값=čas_VALUE;if(čas_VALUE>최댓값)최댓값=čas_VALUE;
                단말.Pisanje("32 bytes from ");pisati_naslov(naslov);단말.Pisanje(" seq=");단말.수(naročilo_VALUE);단말.Pisanje(" ttl=");단말.수(Tabla.응답읽기(2));단말.Pisanje(" time=");단말.수(čas_VALUE);단말.Pisanje(" ms\n");
            }else{단말.Pisanje("Request timeout seq=");단말.수(naročilo_VALUE);단말.문자(10);}
            if(naročilo_VALUE<횟수)계속=čakalno_stanje(200);
        }
        단말.수(보낸수);단말.Pisanje(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Pisanje(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Pisanje("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Pisanje("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Pisanje(" ms\n");}
        명령해석기.REZULTAT=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void oddaja_Dejavnost() { 단말.Pisanje("up ");단말.수(Tabla.밀리초()/1000);단말.Pisanje(" seconds\n"); }
    static void oddaja_pomnilnik() {
        수항목("ARM RAM KiB (firmware): ",Tabla.poizvedba_sistem(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Tabla.poizvedba_sistem(1,0));
        int skupaj_zmogljivost=Tabla.poizvedba_sistem(2,0), 사용량=Tabla.poizvedba_sistem(3,0);
        단말.Pisanje("AOT heap KiB total/used/free: ");단말.수(skupaj_zmogljivost);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(skupaj_zmogljivost-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Tabla.poizvedba_sistem(4,0));
        수항목("EL0 arena+session reserve KiB: ",Tabla.poizvedba_sistem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Tabla.poizvedba_sistem(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Pisanje("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void oddaja_Tasks() {
        단말.Pisanje("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Pisanje("1 - RUN - - ");단말.수(Tabla.밀리초());단말.Pisanje(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Tabla.opravek_stanje(INDEX)>0){단말.수(INDEX+1);단말.Pisanje(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int stanje_VALUE=Tabla.poizvedba_sistem(20,INDEX);if(stanje_VALUE==0)continue;
            단말.수(Tabla.poizvedba_sistem(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Pisanje(stanje_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(Tabla.poizvedba_sistem(22,INDEX));단말.문자(' ');단말.수(Tabla.poizvedba_sistem(24,INDEX));단말.문자(' ');단말.수(Tabla.poizvedba_sistem(23,INDEX));단말.문자(' ');
            for(int kazalec_mesta=0;kazalec_mesta<288;kazalec_mesta++){int bajt_VALUE=Tabla.poizvedba_sistem(25,INDEX+kazalec_mesta*4);if(bajt_VALUE==0)break;Tabla.직렬쓰기(bajt_VALUE);}단말.문자(10);
        }
    }
    static void oddaja_Senzor_prostora() {
        int 칸수=0, podatki_COUNT=0;
        for(int INDEX=0;INDEX<pomnilnik_Datoteke.Datoteka_COUNT;INDEX++)if(pomnilnik_Datoteke.이름길이[INDEX]>0 || pomnilnik_Datoteke.Gradiva_COUNT[INDEX]>0){칸수++;podatki_COUNT+=pomnilnik_Datoteke.길이[INDEX];}
        단말.Pisanje("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(pomnilnik_Datoteke.Datoteka_COUNT*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((pomnilnik_Datoteke.Datoteka_COUNT-칸수)*16384);단말.문자(' ');단말.수(podatki_COUNT);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(pomnilnik_Datoteke.Datoteka_COUNT);단말.Pisanje(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void oddaja_stanje_bf9821b5() {
        int 횟수=셸입출력.informacijska_tehnologija_interaktiven()!=0?0:1;
        if(element_COUNT()>1){if(element_COUNT()!=3 || !같음(1,"-n") || (횟수=številka_VALUE(2,1000))<1){napaka_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 izhod_aplikacija");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.informacijska_tehnologija_interaktiven()!=0 && 횟수==0)단말.Pisanje("\u001b[2J\u001b[H");
            oddaja_Dejavnost();oddaja_pomnilnik();oddaja_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!čakalno_stanje(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void oddaja_spletna_pomoč() {
        단말.Pisanje("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Pisanje(표준말(INDEX));단말.Pisanje(" / ");단말.Pisanje(관리명령.Word_SMS(INDEX));단말.Pisanje(" : ");단말.Pisanje(관리명령.설명(INDEX));단말.문자(10);}
        단말.Pisanje("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Pisanje("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Pisanje("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Izvedi_ukaz() {
        int Ukaz=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Ukaz=INDEX;
        if(같음(0,"ifconfig"))Ukaz=0;if(같음(0,"ss"))Ukaz=4;
        if(Ukaz<0)return false;
        if(Ukaz==11){if(같음(1,"net") || 같음(1,"system"))oddaja_spletna_pomoč();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.oddaja_spletna_pomoč();return true;}
        if(Ukaz==0 || Ukaz==1)mreža_ukaz(Ukaz==1);
        else if(Ukaz==2)preskusiti_odziv();
        else if(Ukaz==6)oddaja_stanje_bf9821b5();
        else if(element_COUNT()!=1){napaka_VALUE("This command takes no arguments; help system");}
        else if(Ukaz==3)oddaja_pot();else if(Ukaz==4)oddaja_mreža();else if(Ukaz==5)oddaja_Tasks();else if(Ukaz==7)oddaja_pomnilnik();else if(Ukaz==8)oddaja_Senzor_prostora();else if(Ukaz==9)oddaja_Dejavnost();
        else if(Ukaz==10)Tabla.전원끄기();
        return true;
    }
}
