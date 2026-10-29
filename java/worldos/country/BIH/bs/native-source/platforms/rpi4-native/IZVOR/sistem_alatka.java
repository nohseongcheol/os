// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** stvaran_podaci jezgro_VALUE 상태를 읽는 IPv4·ICMP·작업·Memorija_VALUE·RAM 저장소 관리 Naredba. */
public final class sistem_alatka {
    static int adresa_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int stavka_COUNT() { return 명령해석기.token_COUNT; }
    static void neuspjeh_VALUE(String Pročitaj_me_eb81d7d9) { 명령해석기.mjera=2; 단말.Piši(Pročitaj_me_eb81d7d9); 단말.문자(10); }
    static void GRESKA(int VALUE) { 명령해석기.GRESKA(VALUE); }
    static void 수항목(String Naziv, int VALUE) { 단말.Piši(Naziv); 단말.수(VALUE); 단말.문자(10); }
    static int cifra_VALUE(int INDEX, int 한도) {
        if (INDEX>=stavka_COUNT() || 명령해석기.dužina_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.dužina_VALUE[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (znak_VALUE<0 || znak_VALUE>9 || VALUE>(한도-znak_VALUE)/10) return -1;
            VALUE=VALUE*10+znak_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=stavka_COUNT()) return false;
        int VALUE=0, 덩이=0, cifra_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.dužina_VALUE[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (znak_VALUE=='.') { if (cifra_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=cifra_COUNT=0; }
            else { if (znak_VALUE<'0' || znak_VALUE>'9' || ++cifra_COUNT>3) return false; 덩이=덩이*10+znak_VALUE-'0'; if(덩이>255)return false; }
        }
        if (p_COUNT!=3 || cifra_COUNT==0) return false;
        adresa_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void pisati_adresa(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void program_Mreža_stanje() {
        단말.Piši(ploča.Mreža_stanje(20,0)!=0?"en0: ":"sl0: "); 단말.Piši(ploča.Mreža_stanje(3,0)!=0?"UP":"DOWN");
        단말.Piši(ploča.Mreža_stanje(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Piši(ploča.Mreža_stanje(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); pisati_adresa(ploča.Mreža_stanje(0,0));
        단말.Piši(" netmask "); pisati_adresa(ploča.Mreža_stanje(1,0)); 단말.Piši(" gateway "); pisati_adresa(ploča.Mreža_stanje(2,0)); 단말.문자(10);
        단말.Piši("  RX packets "); 단말.수(ploča.Mreža_stanje(4,0)); 단말.Piši(" bytes "); 단말.수(ploča.Mreža_stanje(6,0));
        단말.Piši(" TX packets "); 단말.수(ploča.Mreža_stanje(5,0)); 단말.Piši(" bytes "); 단말.수(ploča.Mreža_stanje(7,0)); 단말.문자(10);
        수항목("  dropped ",ploča.Mreža_stanje(8,0));
    }
    static void skup_adresa(int Pokreni) {
        if (stavka_COUNT()!=Pokreni+3 || !주소읽기(Pokreni)) { neuspjeh_VALUE("사용법: ipconfig set adresa 주소가림 pristupni_uređaj_VALUE"); return; }
        int adresa=adresa_VALUE;
        if(!주소읽기(Pokreni+1)){neuspjeh_VALUE("Invalid IPv4 netmask");return;} int maska_VALUE=adresa_VALUE;
        if(!주소읽기(Pokreni+2)){neuspjeh_VALUE("Invalid IPv4 gateway");return;}
        int mjera=ploča.Mreža_Postavke(0,adresa,maska_VALUE,adresa_VALUE);
        if(mjera<0) { GRESKA(mjera); if(mjera==-16)단말.Piši("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Piši("IPv4 configuration applied (until reboot)\n"); program_Mreža_stanje(); }
    }
    static void Mreža_komanda(boolean IP_adresa) {
        if (stavka_COUNT()==1 || stavka_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || stavka_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { program_Mreža_stanje();return; }
        if (IP_adresa && 같음(1,"route") && (stavka_COUNT()==2 || stavka_COUNT()==3&&같음(2,"show"))) { program_put();return; }
        if (같음(1,"set")) { skup_adresa(2);return; }
        if (stavka_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { ploča.Mreža_Postavke(같음(1,"up")?1:2,0,0,0);program_Mreža_stanje();return; }
        if (IP_adresa && stavka_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { ploča.Mreža_Postavke(같음(5,"up")?1:2,0,0,0);program_Mreža_stanje();return; }
        neuspjeh_VALUE("사용법: ip [addr show|route show|set adresa 주소가림 pristupni_uređaj_VALUE|link set dev sl0 up|down]");
    }
    static void program_put() {
        단말.Piši("Destination Netmask Gateway Interface\n");
        pisati_adresa(ploča.Mreža_stanje(0,0)&ploča.Mreža_stanje(1,0));단말.문자(' ');pisati_adresa(ploča.Mreža_stanje(1,0));단말.Piši(ploča.Mreža_stanje(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (ploča.Mreža_stanje(2,0)!=0) {단말.Piši("0.0.0.0 0.0.0.0 ");pisati_adresa(ploča.Mreža_stanje(2,0));단말.Piši(ploča.Mreža_stanje(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void program_Mreža() {
        단말.Piši("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_oblast=ploča.Mreža_stanje(10,INDEX);if(TYPE_oblast==0)continue;
            단말.Piši(TYPE_oblast==1?"TCP ":"UDP ");pisati_adresa(ploča.Mreža_stanje(16,INDEX));단말.문자(':');단말.수(ploča.Mreža_stanje(11,INDEX));단말.문자(' ');
            pisati_adresa(ploča.Mreža_stanje(12,INDEX));단말.문자(':');단말.수(ploča.Mreža_stanje(13,INDEX));단말.문자(' ');
            int stanje_VALUE=ploča.Mreža_stanje(14,INDEX);단말.Piši(TYPE_oblast==2?"DATAGRAM":stanje_VALUE==1?"LISTEN":stanje_VALUE==2?"ESTABLISHED":stanje_VALUE==3?"CLOSE_WAIT":stanje_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(ploča.Mreža_stanje(15,INDEX));단말.문자(10);
        }
        단말.Piši("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean čekaj_stanje(int 밀리초) {
        int Pokreni=ploča.밀리초();
        while(ploča.밀리초()-Pokreni<밀리초) {
            if(셸입출력.odjel_za_informacijske_tehnologije_interaktivno()!=0){int znak_VALUE=ploča.직렬읽기();if(znak_VALUE==3 || znak_VALUE=='q' || znak_VALUE=='Q' || znak_VALUE==27 || znak_VALUE==-4096)return false;}
            ploča.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, cilj=-1;
        for(int položaj_INDEX=1;položaj_INDEX<stavka_COUNT();položaj_INDEX++) {
            if(같음(položaj_INDEX,"-c")){횟수=cifra_VALUE(++položaj_INDEX,100);if(횟수<1){neuspjeh_VALUE("ping: -c 1..100");return;}}
            else if(같음(položaj_INDEX,"-W")){제한=cifra_VALUE(++položaj_INDEX,10);if(제한<1){neuspjeh_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(cilj<0)cilj=položaj_INDEX;else{neuspjeh_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(cilj<0 || !주소읽기(cilj)){neuspjeh_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int adresa=adresa_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Piši("PING ");pisati_adresa(adresa);단말.Piši(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int redoslijed_VALUE=1;redoslijed_VALUE<=횟수 && 계속;redoslijed_VALUE++) {
            int 처리값=ploča.응답보내기(adresa,redoslijed_VALUE);
            if(처리값<0){GRESKA(처리값);break;}보낸수++;
            int Pokreni=ploča.밀리초();
            while(ploča.응답읽기(0)==-11 && ploča.밀리초()-Pokreni<제한)if(!čekaj_stanje(1)){계속=false;break;}
            if(!계속)break;
            if(ploča.응답읽기(0)==0){
                int TIME_VALUE=ploča.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Piši("32 bytes from ");pisati_adresa(adresa);단말.Piši(" seq=");단말.수(redoslijed_VALUE);단말.Piši(" ttl=");단말.수(ploča.응답읽기(2));단말.Piši(" time=");단말.수(TIME_VALUE);단말.Piši(" ms\n");
            }else{단말.Piši("Request timeout seq=");단말.수(redoslijed_VALUE);단말.문자(10);}
            if(redoslijed_VALUE<횟수)계속=čekaj_stanje(200);
        }
        단말.수(보낸수);단말.Piši(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Piši(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Piši("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Piši("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Piši(" ms\n");}
        명령해석기.mjera=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void program_Aktivnost() { 단말.Piši("up ");단말.수(ploča.밀리초()/1000);단말.Piši(" seconds\n"); }
    static void program_Memorija() {
        수항목("ARM RAM KiB (firmware): ",ploča.upit_sistem(0,0));
        수항목("Kernel image+BSS+stack KiB: ",ploča.upit_sistem(1,0));
        int 총량=ploča.upit_sistem(2,0), 사용량=ploča.upit_sistem(3,0);
        단말.Piši("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",ploča.upit_sistem(4,0));
        수항목("EL0 arena+session reserve KiB: ",ploča.upit_sistem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=ploča.upit_sistem(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Piši("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void program_Tasks() {
        단말.Piši("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Piši("1 - RUN - - ");단말.수(ploča.밀리초());단말.Piši(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(ploča.zadatak_stanje(INDEX)>0){단말.수(INDEX+1);단말.Piši(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int stanje_VALUE=ploča.upit_sistem(20,INDEX);if(stanje_VALUE==0)continue;
            단말.수(ploča.upit_sistem(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Piši(stanje_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(ploča.upit_sistem(22,INDEX));단말.문자(' ');단말.수(ploča.upit_sistem(24,INDEX));단말.문자(' ');단말.수(ploča.upit_sistem(23,INDEX));단말.문자(' ');
            for(int položaj_INDEX=0;položaj_INDEX<288;položaj_INDEX++){int bajt_VALUE=ploča.upit_sistem(25,INDEX+položaj_INDEX*4);if(bajt_VALUE==0)break;ploča.직렬쓰기(bajt_VALUE);}단말.문자(10);
        }
    }
    static void program_Pohrana() {
        int prostor_za_unos_COUNT=0, podaci_COUNT=0;
        for(int INDEX=0;INDEX<Memorija_Fajlovi.fajl_COUNT;INDEX++)if(Memorija_Fajlovi.이름길이[INDEX]>0 || Memorija_Fajlovi.Reference_COUNT[INDEX]>0){prostor_za_unos_COUNT++;podaci_COUNT+=Memorija_Fajlovi.dužina_VALUE[INDEX];}
        단말.Piši("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memorija_Fajlovi.fajl_COUNT*16384);단말.문자(' ');단말.수(prostor_za_unos_COUNT*16384);단말.문자(' ');단말.수((Memorija_Fajlovi.fajl_COUNT-prostor_za_unos_COUNT)*16384);단말.문자(' ');단말.수(podaci_COUNT);단말.문자(' ');단말.수(prostor_za_unos_COUNT);단말.문자('/');단말.수(Memorija_Fajlovi.fajl_COUNT);단말.Piši(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void program_stanje_bf9821b5() {
        int 횟수=셸입출력.odjel_za_informacijske_tehnologije_interaktivno()!=0?0:1;
        if(stavka_COUNT()>1){if(stavka_COUNT()!=3 || !같음(1,"-n") || (횟수=cifra_VALUE(2,1000))<1){neuspjeh_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 izađi_program");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.odjel_za_informacijske_tehnologije_interaktivno()!=0 && 횟수==0)단말.Piši("\u001b[2J\u001b[H");
            program_Aktivnost();program_Memorija();program_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!čekaj_stanje(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void program_pomoć() {
        단말.Piši("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Piši(표준말(INDEX));단말.Piši(" / ");단말.Piši(관리명령.Word_SMS(INDEX));단말.Piši(" : ");단말.Piši(관리명령.설명(INDEX));단말.문자(10);}
        단말.Piši("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Piši("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Piši("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Izvrši_komanda() {
        int Naredba=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Naredba=INDEX;
        if(같음(0,"ifconfig"))Naredba=0;if(같음(0,"ss"))Naredba=4;
        if(Naredba<0)return false;
        if(Naredba==11){if(같음(1,"net") || 같음(1,"system"))program_pomoć();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.program_pomoć();return true;}
        if(Naredba==0 || Naredba==1)Mreža_komanda(Naredba==1);
        else if(Naredba==2)응답시험();
        else if(Naredba==6)program_stanje_bf9821b5();
        else if(stavka_COUNT()!=1){neuspjeh_VALUE("This command takes no arguments; help system");}
        else if(Naredba==3)program_put();else if(Naredba==4)program_Mreža();else if(Naredba==5)program_Tasks();else if(Naredba==7)program_Memorija();else if(Naredba==8)program_Pohrana();else if(Naredba==9)program_Aktivnost();
        else if(Naredba==10)ploča.전원끄기();
        return true;
    }
}
