// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 실제 keetnerü_ajutuu 상태를 읽는 IPv4·ICMP·작업·기억·RAM 저장소 관리 aluwataaya. */
public final class a_yatawaajiraaya_a_yataaya {
    static int ejepüsee_ajutuu;
    static boolean 같음(int ee_iyatialujuna, String 말) { return 명령해석기.같음(ee_iyatialujuna, 말); }
    static int 개수() { return 명령해석기.토큰수; }
    static void ajachitia_ajutuu(String PAASHAJE_ERAN_eb81d7d9) { 명령해석기.결과=2; 단말.ashajaa(PAASHAJE_ERAN_eb81d7d9); 단말.문자(10); }
    static void ajachitia(int ajutuu) { 명령해석기.ajachitia(ajutuu); }
    static void 수항목(String 이름, int ajutuu) { 단말.ashajaa(이름); 단말.수(ajutuu); 단말.문자(10); }
    static int 숫자(int ee_iyatialujuna, int 한도) {
        if (ee_iyatialujuna>=개수() || 명령해석기.akaliaa_ajutuu[ee_iyatialujuna]==0) return -1;
        int ajutuu=0;
        for (int 순번=0; 순번<명령해석기.akaliaa_ajutuu[ee_iyatialujuna]; 순번++) {
            int jeerü_ajutuu=명령해석기.토큰[명령해석기.시작점[ee_iyatialujuna]+순번]-'0';
            if (jeerü_ajutuu<0 || jeerü_ajutuu>9 || ajutuu>(한도-jeerü_ajutuu)/10) return -1;
            ajutuu=ajutuu*10+jeerü_ajutuu;
        }
        return ajutuu<=한도?ajutuu:-1;
    }
    static boolean 주소읽기(int ee_iyatialujuna) {
        if (ee_iyatialujuna>=개수()) return false;
        int ajutuu=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.akaliaa_ajutuu[ee_iyatialujuna]; 순번++) {
            int jeerü_ajutuu=명령해석기.토큰[명령해석기.시작점[ee_iyatialujuna]+순번];
            if (jeerü_ajutuu=='.') { if (숫자수==0 || ++점수>3) return false; ajutuu=(ajutuu<<8)|덩이; 덩이=숫자수=0; }
            else { if (jeerü_ajutuu<'0' || jeerü_ajutuu>'9' || ++숫자수>3) return false; 덩이=덩이*10+jeerü_ajutuu-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        ejepüsee_ajutuu=(ajutuu<<8)|덩이; return true;
    }
    static void ashajaa_ejepüsee(int ajutuu) {
        단말.수((ajutuu>>>24)&255); 단말.문자('.'); 단말.수((ajutuu>>>16)&255); 단말.문자('.');
        단말.수((ajutuu>>>8)&255); 단말.문자('.'); 단말.수(ajutuu&255);
    }
    static void 망보기() {
        단말.ashajaa(보드.kusu_jamakua_iparülein(20,0)!=0?"en0: ":"sl0: "); 단말.ashajaa(보드.kusu_jamakua_iparülein(3,0)!=0?"UP":"DOWN");
        단말.ashajaa(보드.kusu_jamakua_iparülein(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.ashajaa(보드.kusu_jamakua_iparülein(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); ashajaa_ejepüsee(보드.kusu_jamakua_iparülein(0,0));
        단말.ashajaa(" netmask "); ashajaa_ejepüsee(보드.kusu_jamakua_iparülein(1,0)); 단말.ashajaa(" gateway "); ashajaa_ejepüsee(보드.kusu_jamakua_iparülein(2,0)); 단말.문자(10);
        단말.ashajaa("  RX packets "); 단말.수(보드.kusu_jamakua_iparülein(4,0)); 단말.ashajaa(" bytes "); 단말.수(보드.kusu_jamakua_iparülein(6,0));
        단말.ashajaa(" TX packets "); 단말.수(보드.kusu_jamakua_iparülein(5,0)); 단말.ashajaa(" bytes "); 단말.수(보드.kusu_jamakua_iparülein(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.kusu_jamakua_iparülein(8,0));
    }
    static void 주소설정(int 시작) {
        if (개수()!=시작+3 || !주소읽기(시작)) { ajachitia_ajutuu("사용법: ipconfig set ejepüsee 주소가림 miicho_u_a_ttaalee_ajutuu"); return; }
        int ejepüsee=ejepüsee_ajutuu;
        if(!주소읽기(시작+1)){ajachitia_ajutuu("Invalid IPv4 netmask");return;} int o_upünaa_utajana_ajutuu=ejepüsee_ajutuu;
        if(!주소읽기(시작+2)){ajachitia_ajutuu("Invalid IPv4 gateway");return;}
        int 결과=보드.망설정(0,ejepüsee,o_upünaa_utajana_ajutuu,ejepüsee_ajutuu);
        if(결과<0) { ajachitia(결과); if(결과==-16)단말.ashajaa("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.ashajaa("IPv4 configuration applied (until reboot)\n"); 망보기(); }
    }
    static void kusu_aluwataaya(boolean ejepüsee_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { 망보기();return; }
        if (ejepüsee_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { 경로보기();return; }
        if (같음(1,"set")) { 주소설정(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.망설정(같음(1,"up")?1:2,0,0,0);망보기();return; }
        if (ejepüsee_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.망설정(같음(5,"up")?1:2,0,0,0);망보기();return; }
        ajachitia_ajutuu("사용법: ip [addr show|route show|set ejepüsee 주소가림 miicho_u_a_ttaalee_ajutuu|link set dev sl0 up|down]");
    }
    static void 경로보기() {
        단말.ashajaa("Destination Netmask Gateway Interface\n");
        ashajaa_ejepüsee(보드.kusu_jamakua_iparülein(0,0)&보드.kusu_jamakua_iparülein(1,0));단말.문자(' ');ashajaa_ejepüsee(보드.kusu_jamakua_iparülein(1,0));단말.ashajaa(보드.kusu_jamakua_iparülein(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.kusu_jamakua_iparülein(2,0)!=0) {단말.ashajaa("0.0.0.0 0.0.0.0 ");ashajaa_ejepüsee(보드.kusu_jamakua_iparülein(2,0));단말.ashajaa(보드.kusu_jamakua_iparülein(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void 통신보기() {
        단말.ashajaa("Proto Local Remote State Queued\n");
        for(int ee_iyatialujuna=0;ee_iyatialujuna<32;ee_iyatialujuna++) {
            int 유형=보드.kusu_jamakua_iparülein(10,ee_iyatialujuna);if(유형==0)continue;
            단말.ashajaa(유형==1?"TCP ":"UDP ");ashajaa_ejepüsee(보드.kusu_jamakua_iparülein(16,ee_iyatialujuna));단말.문자(':');단말.수(보드.kusu_jamakua_iparülein(11,ee_iyatialujuna));단말.문자(' ');
            ashajaa_ejepüsee(보드.kusu_jamakua_iparülein(12,ee_iyatialujuna));단말.문자(':');단말.수(보드.kusu_jamakua_iparülein(13,ee_iyatialujuna));단말.문자(' ');
            int jamakua_iparülein_ajutuu=보드.kusu_jamakua_iparülein(14,ee_iyatialujuna);단말.ashajaa(유형==2?"DATAGRAM":jamakua_iparülein_ajutuu==1?"LISTEN":jamakua_iparülein_ajutuu==2?"ESTABLISHED":jamakua_iparülein_ajutuu==3?"CLOSE_WAIT":jamakua_iparülein_ajutuu==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.kusu_jamakua_iparülein(15,ee_iyatialujuna));단말.문자(10);
        }
        단말.ashajaa("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int 시작=보드.밀리초();
        while(보드.밀리초()-시작<밀리초) {
            if(셸입출력.대화가능()!=0){int jeerü_ajutuu=보드.직렬읽기();if(jeerü_ajutuu==3 || jeerü_ajutuu=='q' || jeerü_ajutuu=='Q' || jeerü_ajutuu==27 || jeerü_ajutuu==-4096)return false;}
            보드.양보();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, 대상=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=숫자(++자리,100);if(횟수<1){ajachitia_ajutuu("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=숫자(++자리,10);if(제한<1){ajachitia_ajutuu("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(대상<0)대상=자리;else{ajachitia_ajutuu("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(대상<0 || !주소읽기(대상)){ajachitia_ajutuu("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ejepüsee=ejepüsee_ajutuu, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.ashajaa("PING ");ashajaa_ejepüsee(ejepüsee);단말.ashajaa(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int anaajiaakua_ipa_ajutuu=1;anaajiaakua_ipa_ajutuu<=횟수 && 계속;anaajiaakua_ipa_ajutuu++) {
            int 처리값=보드.응답보내기(ejepüsee,anaajiaakua_ipa_ajutuu);
            if(처리값<0){ajachitia(처리값);break;}보낸수++;
            int 시작=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-시작<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.ashajaa("32 bytes from ");ashajaa_ejepüsee(ejepüsee);단말.ashajaa(" seq=");단말.수(anaajiaakua_ipa_ajutuu);단말.ashajaa(" ttl=");단말.수(보드.응답읽기(2));단말.ashajaa(" time=");단말.수(시간);단말.ashajaa(" ms\n");
            }else{단말.ashajaa("Request timeout seq=");단말.수(anaajiaakua_ipa_ajutuu);단말.문자(10);}
            if(anaajiaakua_ipa_ajutuu<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.ashajaa(" transmitted, ");단말.수(받은수);단말.ashajaa(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.ashajaa("% packet loss\n");
        if(받은수>0){단말.ashajaa("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.ashajaa(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void 가동보기() { 단말.ashajaa("up ");단말.수(보드.밀리초()/1000);단말.ashajaa(" seconds\n"); }
    static void 기억보기() {
        수항목("ARM RAM KiB (firmware): ",보드.asakiriaa_a_yatawaajiraaya(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.asakiriaa_a_yatawaajiraaya(1,0));
        int 총량=보드.asakiriaa_a_yatawaajiraaya(2,0), 사용량=보드.asakiriaa_a_yatawaajiraaya(3,0);
        단말.ashajaa("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.asakiriaa_a_yatawaajiraaya(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.asakiriaa_a_yatawaajiraaya(5,0));
        int 매핑=0;for(int ee_iyatialujuna=0;ee_iyatialujuna<4;ee_iyatialujuna++)매핑+=보드.asakiriaa_a_yatawaajiraaya(22,ee_iyatialujuna);
        수항목("EL0 mapped KiB: ",매핑);
        단말.ashajaa("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.ashajaa("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.ashajaa("1 - RUN - - ");단말.수(보드.밀리초());단말.ashajaa(" kernel/shell\n");
        for(int ee_iyatialujuna=1;ee_iyatialujuna<3;ee_iyatialujuna++)if(보드.aa_innajatü_jamakua_iparülein(ee_iyatialujuna)>0){단말.수(ee_iyatialujuna+1);단말.ashajaa(" - READY 64 - - kernel-task\n");}
        for(int ee_iyatialujuna=0;ee_iyatialujuna<4;ee_iyatialujuna++){
            int jamakua_iparülein_ajutuu=보드.asakiriaa_a_yatawaajiraaya(20,ee_iyatialujuna);if(jamakua_iparülein_ajutuu==0)continue;
            단말.수(보드.asakiriaa_a_yatawaajiraaya(21,ee_iyatialujuna));단말.문자(' ');단말.수(ee_iyatialujuna);단말.ashajaa(jamakua_iparülein_ajutuu==1?" RUN ":" SUSPENDED ");
            단말.수(보드.asakiriaa_a_yatawaajiraaya(22,ee_iyatialujuna));단말.문자(' ');단말.수(보드.asakiriaa_a_yatawaajiraaya(24,ee_iyatialujuna));단말.문자(' ');단말.수(보드.asakiriaa_a_yatawaajiraaya(23,ee_iyatialujuna));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int waai_ajutuu=보드.asakiriaa_a_yatawaajiraaya(25,ee_iyatialujuna+자리*4);if(waai_ajutuu==0)break;보드.직렬쓰기(waai_ajutuu);}단말.문자(10);
        }
    }
    static void 저장보기() {
        int 칸수=0, 자료수=0;
        for(int ee_iyatialujuna=0;ee_iyatialujuna<기억파일.파일수;ee_iyatialujuna++)if(기억파일.이름길이[ee_iyatialujuna]>0 || 기억파일.참조수[ee_iyatialujuna]>0){칸수++;자료수+=기억파일.akaliaa_ajutuu[ee_iyatialujuna];}
        단말.ashajaa("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(기억파일.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((기억파일.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(기억파일.파일수);단말.ashajaa(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void 현황보기() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=숫자(2,1000))<1){ajachitia_ajutuu("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int 차례=0;횟수==0 || 차례<횟수;차례++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.ashajaa("\u001b[2J\u001b[H");
            가동보기();기억보기();작업보기();
            if(횟수!=0 && 차례+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int ee_iyatialujuna) {
        if(ee_iyatialujuna==0)return "ipconfig";if(ee_iyatialujuna==1)return "ip";if(ee_iyatialujuna==2)return "ping";if(ee_iyatialujuna==3)return "route";if(ee_iyatialujuna==4)return "netstat";
        if(ee_iyatialujuna==5)return "ps";if(ee_iyatialujuna==6)return "top";if(ee_iyatialujuna==7)return "free";if(ee_iyatialujuna==8)return "df";if(ee_iyatialujuna==9)return "uptime";if(ee_iyatialujuna==10)return "poweroff";return "help";
    }
    static void 도움말() {
        단말.ashajaa("--- Network / system commands ---\n");
        for(int ee_iyatialujuna=0;ee_iyatialujuna<12;ee_iyatialujuna++){단말.ashajaa(표준말(ee_iyatialujuna));단말.ashajaa(" / ");단말.ashajaa(관리명령.말(ee_iyatialujuna));단말.ashajaa(" : ");단말.ashajaa(관리명령.설명(ee_iyatialujuna));단말.문자(10);}
        단말.ashajaa("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.ashajaa("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.ashajaa("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean 실행() {
        int aluwataaya=-1;
        for(int ee_iyatialujuna=0;ee_iyatialujuna<12;ee_iyatialujuna++)if(같음(0,표준말(ee_iyatialujuna)) || 같음(0,관리명령.말(ee_iyatialujuna)))aluwataaya=ee_iyatialujuna;
        if(같음(0,"ifconfig"))aluwataaya=0;if(같음(0,"ss"))aluwataaya=4;
        if(aluwataaya<0)return false;
        if(aluwataaya==11){if(같음(1,"net") || 같음(1,"system"))도움말();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.도움말();return true;}
        if(aluwataaya==0 || aluwataaya==1)kusu_aluwataaya(aluwataaya==1);
        else if(aluwataaya==2)응답시험();
        else if(aluwataaya==6)현황보기();
        else if(개수()!=1){ajachitia_ajutuu("This command takes no arguments; help system");}
        else if(aluwataaya==3)경로보기();else if(aluwataaya==4)통신보기();else if(aluwataaya==5)작업보기();else if(aluwataaya==7)기억보기();else if(aluwataaya==8)저장보기();else if(aluwataaya==9)가동보기();
        else if(aluwataaya==10)보드.전원끄기();
        return true;
    }
}
