// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** laatii_keɓe aaluude_njaru 상태를 읽는 IPv4·ICMP·작업·teskordu_njaru·RAM 저장소 관리 ginol. */
public final class yuɓɓo_kuutorgal {
    static int ñiiɓirde_njaru;
    static boolean 같음(int joopirdu, String 말) { return 명령해석기.같음(joopirdu, 말); }
    static int 개수() { return 명령해석기.토큰수; }
    static void ella_njaru(String TARƊOO_eb81d7d9) { 명령해석기.결과=2; 단말.winndude(TARƊOO_eb81d7d9); 단말.문자(10); }
    static void juumre(int njaru) { 명령해석기.juumre(njaru); }
    static void 수항목(String innde, int njaru) { 단말.winndude(innde); 단말.수(njaru); 단말.문자(10); }
    static int 숫자(int joopirdu, int 한도) {
        if (joopirdu>=개수() || 명령해석기.njuuteendi_njaru[joopirdu]==0) return -1;
        int njaru=0;
        for (int 순번=0; 순번<명령해석기.njuuteendi_njaru[joopirdu]; 순번++) {
            int alkulal_njaru=명령해석기.토큰[명령해석기.시작점[joopirdu]+순번]-'0';
            if (alkulal_njaru<0 || alkulal_njaru>9 || njaru>(한도-alkulal_njaru)/10) return -1;
            njaru=njaru*10+alkulal_njaru;
        }
        return njaru<=한도?njaru:-1;
    }
    static boolean 주소읽기(int joopirdu) {
        if (joopirdu>=개수()) return false;
        int njaru=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.njuuteendi_njaru[joopirdu]; 순번++) {
            int alkulal_njaru=명령해석기.토큰[명령해석기.시작점[joopirdu]+순번];
            if (alkulal_njaru=='.') { if (숫자수==0 || ++점수>3) return false; njaru=(njaru<<8)|덩이; 덩이=숫자수=0; }
            else { if (alkulal_njaru<'0' || alkulal_njaru>'9' || ++숫자수>3) return false; 덩이=덩이*10+alkulal_njaru-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        ñiiɓirde_njaru=(njaru<<8)|덩이; return true;
    }
    static void winndude_ñiiɓirde(int njaru) {
        단말.수((njaru>>>24)&255); 단말.문자('.'); 단말.수((njaru>>>16)&255); 단말.문자('.');
        단말.수((njaru>>>8)&255); 단말.문자('.'); 단말.수(njaru&255);
    }
    static void hollirde_laylaytol_ngonka() {
        단말.winndude(보드.laylaytol_ngonka(20,0)!=0?"en0: ":"sl0: "); 단말.winndude(보드.laylaytol_ngonka(3,0)!=0?"UP":"DOWN");
        단말.winndude(보드.laylaytol_ngonka(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.winndude(보드.laylaytol_ngonka(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); winndude_ñiiɓirde(보드.laylaytol_ngonka(0,0));
        단말.winndude(" netmask "); winndude_ñiiɓirde(보드.laylaytol_ngonka(1,0)); 단말.winndude(" gateway "); winndude_ñiiɓirde(보드.laylaytol_ngonka(2,0)); 단말.문자(10);
        단말.winndude("  RX packets "); 단말.수(보드.laylaytol_ngonka(4,0)); 단말.winndude(" bytes "); 단말.수(보드.laylaytol_ngonka(6,0));
        단말.winndude(" TX packets "); 단말.수(보드.laylaytol_ngonka(5,0)); 단말.winndude(" bytes "); 단말.수(보드.laylaytol_ngonka(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.laylaytol_ngonka(8,0));
    }
    static void 주소설정(int huutoraade) {
        if (개수()!=huutoraade+3 || !주소읽기(huutoraade)) { ella_njaru("사용법: ipconfig set ñiiɓirde 주소가림 관문"); return; }
        int ñiiɓirde=ñiiɓirde_njaru;
        if(!주소읽기(huutoraade+1)){ella_njaru("Invalid IPv4 netmask");return;} int 가림=ñiiɓirde_njaru;
        if(!주소읽기(huutoraade+2)){ella_njaru("Invalid IPv4 gateway");return;}
        int 결과=보드.망설정(0,ñiiɓirde,가림,ñiiɓirde_njaru);
        if(결과<0) { juumre(결과); if(결과==-16)단말.winndude("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.winndude("IPv4 configuration applied (until reboot)\n"); hollirde_laylaytol_ngonka(); }
    }
    static void laylaytol_ginol(boolean ñiiɓirde_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { hollirde_laylaytol_ngonka();return; }
        if (ñiiɓirde_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { hollirde_laawol();return; }
        if (같음(1,"set")) { 주소설정(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.망설정(같음(1,"up")?1:2,0,0,0);hollirde_laylaytol_ngonka();return; }
        if (ñiiɓirde_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.망설정(같음(5,"up")?1:2,0,0,0);hollirde_laylaytol_ngonka();return; }
        ella_njaru("사용법: ip [addr show|route show|set ñiiɓirde 주소가림 관문|link set dev sl0 up|down]");
    }
    static void hollirde_laawol() {
        단말.winndude("Destination Netmask Gateway Interface\n");
        winndude_ñiiɓirde(보드.laylaytol_ngonka(0,0)&보드.laylaytol_ngonka(1,0));단말.문자(' ');winndude_ñiiɓirde(보드.laylaytol_ngonka(1,0));단말.winndude(보드.laylaytol_ngonka(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.laylaytol_ngonka(2,0)!=0) {단말.winndude("0.0.0.0 0.0.0.0 ");winndude_ñiiɓirde(보드.laylaytol_ngonka(2,0));단말.winndude(보드.laylaytol_ngonka(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void hollirde_laylaytol() {
        단말.winndude("Proto Local Remote State Queued\n");
        for(int joopirdu=0;joopirdu<32;joopirdu++) {
            int 유형=보드.laylaytol_ngonka(10,joopirdu);if(유형==0)continue;
            단말.winndude(유형==1?"TCP ":"UDP ");winndude_ñiiɓirde(보드.laylaytol_ngonka(16,joopirdu));단말.문자(':');단말.수(보드.laylaytol_ngonka(11,joopirdu));단말.문자(' ');
            winndude_ñiiɓirde(보드.laylaytol_ngonka(12,joopirdu));단말.문자(':');단말.수(보드.laylaytol_ngonka(13,joopirdu));단말.문자(' ');
            int ngonka_njaru=보드.laylaytol_ngonka(14,joopirdu);단말.winndude(유형==2?"DATAGRAM":ngonka_njaru==1?"LISTEN":ngonka_njaru==2?"ESTABLISHED":ngonka_njaru==3?"CLOSE_WAIT":ngonka_njaru==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.laylaytol_ngonka(15,joopirdu));단말.문자(10);
        }
        단말.winndude("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int huutoraade=보드.밀리초();
        while(보드.밀리초()-huutoraade<밀리초) {
            if(셸입출력.대화가능()!=0){int alkulal_njaru=보드.직렬읽기();if(alkulal_njaru==3 || alkulal_njaru=='q' || alkulal_njaru=='Q' || alkulal_njaru==27 || alkulal_njaru==-4096)return false;}
            보드.양보();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, faandaare=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=숫자(++자리,100);if(횟수<1){ella_njaru("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=숫자(++자리,10);if(제한<1){ella_njaru("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(faandaare<0)faandaare=자리;else{ella_njaru("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(faandaare<0 || !주소읽기(faandaare)){ella_njaru("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ñiiɓirde=ñiiɓirde_njaru, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.winndude("PING ");winndude_ñiiɓirde(ñiiɓirde);단말.winndude(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int deggondiral_njaru=1;deggondiral_njaru<=횟수 && 계속;deggondiral_njaru++) {
            int 처리값=보드.응답보내기(ñiiɓirde,deggondiral_njaru);
            if(처리값<0){juumre(처리값);break;}보낸수++;
            int huutoraade=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-huutoraade<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.winndude("32 bytes from ");winndude_ñiiɓirde(ñiiɓirde);단말.winndude(" seq=");단말.수(deggondiral_njaru);단말.winndude(" ttl=");단말.수(보드.응답읽기(2));단말.winndude(" time=");단말.수(시간);단말.winndude(" ms\n");
            }else{단말.winndude("Request timeout seq=");단말.수(deggondiral_njaru);단말.문자(10);}
            if(deggondiral_njaru<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.winndude(" transmitted, ");단말.수(받은수);단말.winndude(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.winndude("% packet loss\n");
        if(받은수>0){단말.winndude("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.winndude(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void 가동보기() { 단말.winndude("up ");단말.수(보드.밀리초()/1000);단말.winndude(" seconds\n"); }
    static void hollirde_teskordu() {
        수항목("ARM RAM KiB (firmware): ",보드.ɗaɓɓal_yuɓɓo(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.ɗaɓɓal_yuɓɓo(1,0));
        int 총량=보드.ɗaɓɓal_yuɓɓo(2,0), 사용량=보드.ɗaɓɓal_yuɓɓo(3,0);
        단말.winndude("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.ɗaɓɓal_yuɓɓo(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.ɗaɓɓal_yuɓɓo(5,0));
        int 매핑=0;for(int joopirdu=0;joopirdu<4;joopirdu++)매핑+=보드.ɗaɓɓal_yuɓɓo(22,joopirdu);
        수항목("EL0 mapped KiB: ",매핑);
        단말.winndude("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.winndude("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.winndude("1 - RUN - - ");단말.수(보드.밀리초());단말.winndude(" kernel/shell\n");
        for(int joopirdu=1;joopirdu<3;joopirdu++)if(보드.golle_ngonka(joopirdu)>0){단말.수(joopirdu+1);단말.winndude(" - READY 64 - - kernel-task\n");}
        for(int joopirdu=0;joopirdu<4;joopirdu++){
            int ngonka_njaru=보드.ɗaɓɓal_yuɓɓo(20,joopirdu);if(ngonka_njaru==0)continue;
            단말.수(보드.ɗaɓɓal_yuɓɓo(21,joopirdu));단말.문자(' ');단말.수(joopirdu);단말.winndude(ngonka_njaru==1?" RUN ":" SUSPENDED ");
            단말.수(보드.ɗaɓɓal_yuɓɓo(22,joopirdu));단말.문자(' ');단말.수(보드.ɗaɓɓal_yuɓɓo(24,joopirdu));단말.문자(' ');단말.수(보드.ɗaɓɓal_yuɓɓo(23,joopirdu));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int oktee_njaru=보드.ɗaɓɓal_yuɓɓo(25,joopirdu+자리*4);if(oktee_njaru==0)break;보드.직렬쓰기(oktee_njaru);}단말.문자(10);
        }
    }
    static void 저장보기() {
        int 칸수=0, 자료수=0;
        for(int joopirdu=0;joopirdu<기억파일.파일수;joopirdu++)if(기억파일.이름길이[joopirdu]>0 || 기억파일.참조수[joopirdu]>0){칸수++;자료수+=기억파일.njuuteendi_njaru[joopirdu];}
        단말.winndude("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(기억파일.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((기억파일.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(기억파일.파일수);단말.winndude(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void hollirde_ngonka_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=숫자(2,1000))<1){ella_njaru("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int 차례=0;횟수==0 || 차례<횟수;차례++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.winndude("\u001b[2J\u001b[H");
            가동보기();hollirde_teskordu();작업보기();
            if(횟수!=0 && 차례+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int joopirdu) {
        if(joopirdu==0)return "ipconfig";if(joopirdu==1)return "ip";if(joopirdu==2)return "ping";if(joopirdu==3)return "route";if(joopirdu==4)return "netstat";
        if(joopirdu==5)return "ps";if(joopirdu==6)return "top";if(joopirdu==7)return "free";if(joopirdu==8)return "df";if(joopirdu==9)return "uptime";if(joopirdu==10)return "poweroff";return "help";
    }
    static void hollirde_ballal() {
        단말.winndude("--- Network / system commands ---\n");
        for(int joopirdu=0;joopirdu<12;joopirdu++){단말.winndude(표준말(joopirdu));단말.winndude(" / ");단말.winndude(관리명령.말(joopirdu));단말.winndude(" : ");단말.winndude(관리명령.설명(joopirdu));단말.문자(10);}
        단말.winndude("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.winndude("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.winndude("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean 실행() {
        int ginol=-1;
        for(int joopirdu=0;joopirdu<12;joopirdu++)if(같음(0,표준말(joopirdu)) || 같음(0,관리명령.말(joopirdu)))ginol=joopirdu;
        if(같음(0,"ifconfig"))ginol=0;if(같음(0,"ss"))ginol=4;
        if(ginol<0)return false;
        if(ginol==11){if(같음(1,"net") || 같음(1,"system"))hollirde_ballal();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.hollirde_ballal();return true;}
        if(ginol==0 || ginol==1)laylaytol_ginol(ginol==1);
        else if(ginol==2)응답시험();
        else if(ginol==6)hollirde_ngonka_bf9821b5();
        else if(개수()!=1){ella_njaru("This command takes no arguments; help system");}
        else if(ginol==3)hollirde_laawol();else if(ginol==4)hollirde_laylaytol();else if(ginol==5)작업보기();else if(ginol==7)hollirde_teskordu();else if(ginol==8)저장보기();else if(ginol==9)가동보기();
        else if(ginol==10)보드.전원끄기();
        return true;
    }
}
