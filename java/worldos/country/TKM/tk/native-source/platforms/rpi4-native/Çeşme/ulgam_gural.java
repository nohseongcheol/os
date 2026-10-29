// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** hakyky_maglumat ýadro_baha 상태를 읽는 IPv4·ICMP·작업·ýat_baha·RAM 저장소 관리 buýruk. */
public final class ulgam_gural {
    static int salgy_baha;
    static boolean 같음(int indeks, String Söz_SMS) { return 명령해석기.같음(indeks, Söz_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void näsazlyk_baha(String README_eb81d7d9) { 명령해석기.결과=2; 단말.Ýaz(README_eb81d7d9); 단말.문자(10); }
    static void Hata(int baha) { 명령해석기.Hata(baha); }
    static void 수항목(String Ad, int baha) { 단말.Ýaz(Ad); 단말.수(baha); 단말.문자(10); }
    static int san_baha(int indeks, int 한도) {
        if (indeks>=개수() || 명령해석기.dowamlylyk_baha[indeks]==0) return -1;
        int baha=0;
        for (int 순번=0; 순번<명령해석기.dowamlylyk_baha[indeks]; 순번++) {
            int nyşan_baha_068c2631=명령해석기.token_baha[명령해석기.시작점[indeks]+순번]-'0';
            if (nyşan_baha_068c2631<0 || nyşan_baha_068c2631>9 || baha>(한도-nyşan_baha_068c2631)/10) return -1;
            baha=baha*10+nyşan_baha_068c2631;
        }
        return baha<=한도?baha:-1;
    }
    static boolean 주소읽기(int indeks) {
        if (indeks>=개수()) return false;
        int baha=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.dowamlylyk_baha[indeks]; 순번++) {
            int nyşan_baha_068c2631=명령해석기.token_baha[명령해석기.시작점[indeks]+순번];
            if (nyşan_baha_068c2631=='.') { if (숫자수==0 || ++점수>3) return false; baha=(baha<<8)|덩이; 덩이=숫자수=0; }
            else { if (nyşan_baha_068c2631<'0' || nyşan_baha_068c2631>'9' || ++숫자수>3) return false; 덩이=덩이*10+nyşan_baha_068c2631-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        salgy_baha=(baha<<8)|덩이; return true;
    }
    static void ýaz_salgy(int baha) {
        단말.수((baha>>>24)&255); 단말.문자('.'); 단말.수((baha>>>16)&255); 단말.문자('.');
        단말.수((baha>>>8)&255); 단말.문자('.'); 단말.수(baha&255);
    }
    static void görkez_Tor_ýagdaý() {
        단말.Ýaz(보드.Tor_ýagdaý(20,0)!=0?"en0: ":"sl0: "); 단말.Ýaz(보드.Tor_ýagdaý(3,0)!=0?"UP":"DOWN");
        단말.Ýaz(보드.Tor_ýagdaý(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Ýaz(보드.Tor_ýagdaý(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); ýaz_salgy(보드.Tor_ýagdaý(0,0));
        단말.Ýaz(" netmask "); ýaz_salgy(보드.Tor_ýagdaý(1,0)); 단말.Ýaz(" gateway "); ýaz_salgy(보드.Tor_ýagdaý(2,0)); 단말.문자(10);
        단말.Ýaz("  RX packets "); 단말.수(보드.Tor_ýagdaý(4,0)); 단말.Ýaz(" bytes "); 단말.수(보드.Tor_ýagdaý(6,0));
        단말.Ýaz(" TX packets "); 단말.수(보드.Tor_ýagdaý(5,0)); 단말.Ýaz(" bytes "); 단말.수(보드.Tor_ýagdaý(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Tor_ýagdaý(8,0));
    }
    static void köplük_salgy(int Bitir) {
        if (개수()!=Bitir+3 || !주소읽기(Bitir)) { näsazlyk_baha("사용법: ipconfig set salgy 주소가림 şlýuz_baha"); return; }
        int salgy=salgy_baha;
        if(!주소읽기(Bitir+1)){näsazlyk_baha("Invalid IPv4 netmask");return;} int örtük_baha=salgy_baha;
        if(!주소읽기(Bitir+2)){näsazlyk_baha("Invalid IPv4 gateway");return;}
        int 결과=보드.Tor_Sazlamalar(0,salgy,örtük_baha,salgy_baha);
        if(결과<0) { Hata(결과); if(결과==-16)단말.Ýaz("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Ýaz("IPv4 configuration applied (until reboot)\n"); görkez_Tor_ýagdaý(); }
    }
    static void Tor_buýruk(boolean IP_salgy) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { görkez_Tor_ýagdaý();return; }
        if (IP_salgy && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { görkez_ýol();return; }
        if (같음(1,"set")) { köplük_salgy(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.Tor_Sazlamalar(같음(1,"up")?1:2,0,0,0);görkez_Tor_ýagdaý();return; }
        if (IP_salgy && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.Tor_Sazlamalar(같음(5,"up")?1:2,0,0,0);görkez_Tor_ýagdaý();return; }
        näsazlyk_baha("사용법: ip [addr show|route show|set salgy 주소가림 şlýuz_baha|link set dev sl0 up|down]");
    }
    static void görkez_ýol() {
        단말.Ýaz("Destination Netmask Gateway Interface\n");
        ýaz_salgy(보드.Tor_ýagdaý(0,0)&보드.Tor_ýagdaý(1,0));단말.문자(' ');ýaz_salgy(보드.Tor_ýagdaý(1,0));단말.Ýaz(보드.Tor_ýagdaý(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Tor_ýagdaý(2,0)!=0) {단말.Ýaz("0.0.0.0 0.0.0.0 ");ýaz_salgy(보드.Tor_ýagdaý(2,0));단말.Ýaz(보드.Tor_ýagdaý(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void görkez_Tor() {
        단말.Ýaz("Proto Local Remote State Queued\n");
        for(int indeks=0;indeks<32;indeks++) {
            int ýaz_kategoriýa=보드.Tor_ýagdaý(10,indeks);if(ýaz_kategoriýa==0)continue;
            단말.Ýaz(ýaz_kategoriýa==1?"TCP ":"UDP ");ýaz_salgy(보드.Tor_ýagdaý(16,indeks));단말.문자(':');단말.수(보드.Tor_ýagdaý(11,indeks));단말.문자(' ');
            ýaz_salgy(보드.Tor_ýagdaý(12,indeks));단말.문자(':');단말.수(보드.Tor_ýagdaý(13,indeks));단말.문자(' ');
            int ýagdaý_baha=보드.Tor_ýagdaý(14,indeks);단말.Ýaz(ýaz_kategoriýa==2?"DATAGRAM":ýagdaý_baha==1?"LISTEN":ýagdaý_baha==2?"ESTABLISHED":ýagdaý_baha==3?"CLOSE_WAIT":ýagdaý_baha==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Tor_ýagdaý(15,indeks));단말.문자(10);
        }
        단말.Ýaz("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int Bitir=보드.밀리초();
        while(보드.밀리초()-Bitir<밀리초) {
            if(셸입출력.대화가능()!=0){int nyşan_baha_068c2631=보드.직렬읽기();if(nyşan_baha_068c2631==3 || nyşan_baha_068c2631=='q' || nyşan_baha_068c2631=='Q' || nyşan_baha_068c2631==27 || nyşan_baha_068c2631==-4096)return false;}
            보드.togtatmak_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, niýet=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=san_baha(++자리,100);if(횟수<1){näsazlyk_baha("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=san_baha(++자리,10);if(제한<1){näsazlyk_baha("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(niýet<0)niýet=자리;else{näsazlyk_baha("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(niýet<0 || !주소읽기(niýet)){näsazlyk_baha("ping: an IPv4 address is required (DNS is not configured)");return;}
        int salgy=salgy_baha, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Ýaz("PING ");ýaz_salgy(salgy);단말.Ýaz(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int tertip_baha=1;tertip_baha<=횟수 && 계속;tertip_baha++) {
            int 처리값=보드.응답보내기(salgy,tertip_baha);
            if(처리값<0){Hata(처리값);break;}보낸수++;
            int Bitir=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-Bitir<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.Ýaz("32 bytes from ");ýaz_salgy(salgy);단말.Ýaz(" seq=");단말.수(tertip_baha);단말.Ýaz(" ttl=");단말.수(보드.응답읽기(2));단말.Ýaz(" time=");단말.수(시간);단말.Ýaz(" ms\n");
            }else{단말.Ýaz("Request timeout seq=");단말.수(tertip_baha);단말.문자(10);}
            if(tertip_baha<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.Ýaz(" transmitted, ");단말.수(받은수);단말.Ýaz(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.Ýaz("% packet loss\n");
        if(받은수>0){단말.Ýaz("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.Ýaz(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void görkez_Işjeňlik() { 단말.Ýaz("up ");단말.수(보드.밀리초()/1000);단말.Ýaz(" seconds\n"); }
    static void görkez_ýat() {
        수항목("ARM RAM KiB (firmware): ",보드.talap_ulgam(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.talap_ulgam(1,0));
        int 총량=보드.talap_ulgam(2,0), 사용량=보드.talap_ulgam(3,0);
        단말.Ýaz("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.talap_ulgam(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.talap_ulgam(5,0));
        int 매핑=0;for(int indeks=0;indeks<4;indeks++)매핑+=보드.talap_ulgam(22,indeks);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Ýaz("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.Ýaz("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Ýaz("1 - RUN - - ");단말.수(보드.밀리초());단말.Ýaz(" kernel/shell\n");
        for(int indeks=1;indeks<3;indeks++)if(보드.tabşyryk_ýagdaý(indeks)>0){단말.수(indeks+1);단말.Ýaz(" - READY 64 - - kernel-task\n");}
        for(int indeks=0;indeks<4;indeks++){
            int ýagdaý_baha=보드.talap_ulgam(20,indeks);if(ýagdaý_baha==0)continue;
            단말.수(보드.talap_ulgam(21,indeks));단말.문자(' ');단말.수(indeks);단말.Ýaz(ýagdaý_baha==1?" RUN ":" SUSPENDED ");
            단말.수(보드.talap_ulgam(22,indeks));단말.문자(' ');단말.수(보드.talap_ulgam(24,indeks));단말.문자(' ');단말.수(보드.talap_ulgam(23,indeks));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int baýt_baha=보드.talap_ulgam(25,indeks+자리*4);if(baýt_baha==0)break;보드.직렬쓰기(baýt_baha);}단말.문자(10);
        }
    }
    static void görkez_Ammar() {
        int 칸수=0, 자료수=0;
        for(int indeks=0;indeks<ýat_Faýllar.파일수;indeks++)if(ýat_Faýllar.이름길이[indeks]>0 || ýat_Faýllar.참조수[indeks]>0){칸수++;자료수+=ýat_Faýllar.dowamlylyk_baha[indeks];}
        단말.Ýaz("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(ýat_Faýllar.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((ýat_Faýllar.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(ýat_Faýllar.파일수);단말.Ýaz(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void görkez_ýagdaý_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=san_baha(2,1000))<1){näsazlyk_baha("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int SEQUENCE_baha=0;횟수==0 || SEQUENCE_baha<횟수;SEQUENCE_baha++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Ýaz("\u001b[2J\u001b[H");
            görkez_Işjeňlik();görkez_ýat();작업보기();
            if(횟수!=0 && SEQUENCE_baha+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int indeks) {
        if(indeks==0)return "ipconfig";if(indeks==1)return "ip";if(indeks==2)return "ping";if(indeks==3)return "route";if(indeks==4)return "netstat";
        if(indeks==5)return "ps";if(indeks==6)return "top";if(indeks==7)return "free";if(indeks==8)return "df";if(indeks==9)return "uptime";if(indeks==10)return "poweroff";return "help";
    }
    static void görkez_kömek() {
        단말.Ýaz("--- Network / system commands ---\n");
        for(int indeks=0;indeks<12;indeks++){단말.Ýaz(표준말(indeks));단말.Ýaz(" / ");단말.Ýaz(관리명령.Söz_SMS(indeks));단말.Ýaz(" : ");단말.Ýaz(관리명령.설명(indeks));단말.문자(10);}
        단말.Ýaz("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Ýaz("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Ýaz("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean ýerine_ýetir_buýruk() {
        int buýruk=-1;
        for(int indeks=0;indeks<12;indeks++)if(같음(0,표준말(indeks)) || 같음(0,관리명령.Söz_SMS(indeks)))buýruk=indeks;
        if(같음(0,"ifconfig"))buýruk=0;if(같음(0,"ss"))buýruk=4;
        if(buýruk<0)return false;
        if(buýruk==11){if(같음(1,"net") || 같음(1,"system"))görkez_kömek();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.görkez_kömek();return true;}
        if(buýruk==0 || buýruk==1)Tor_buýruk(buýruk==1);
        else if(buýruk==2)응답시험();
        else if(buýruk==6)görkez_ýagdaý_bf9821b5();
        else if(개수()!=1){näsazlyk_baha("This command takes no arguments; help system");}
        else if(buýruk==3)görkez_ýol();else if(buýruk==4)görkez_Tor();else if(buýruk==5)작업보기();else if(buýruk==7)görkez_ýat();else if(buýruk==8)görkez_Ammar();else if(buýruk==9)görkez_Işjeňlik();
        else if(buýruk==10)보드.전원끄기();
        return true;
    }
}
