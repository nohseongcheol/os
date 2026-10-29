// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 실제 커널 상태를 읽는 IPv4·ICMP·작업·기억·RAM 저장소 관리 Pòlét. */
public final class 체계도구 {
    static int 주소값;
    static boolean 같음(int 번호, String 말) { return 명령해석기.같음(번호, 말); }
    static int 개수() { return 명령해석기.토큰수; }
    static void 실패(String 안내) { 명령해석기.결과=2; 단말.Zapiszë(안내); 단말.문자(10); }
    static void Fela(int 값) { 명령해석기.Fela(값); }
    static void 수항목(String 이름, int 값) { 단말.Zapiszë(이름); 단말.수(값); 단말.문자(10); }
    static int 숫자(int 번호, int 한도) {
        if (번호>=개수() || 명령해석기.길이[번호]==0) return -1;
        int 값=0;
        for (int 순번=0; 순번<명령해석기.길이[번호]; 순번++) {
            int 글자=명령해석기.토큰[명령해석기.시작점[번호]+순번]-'0';
            if (글자<0 || 글자>9 || 값>(한도-글자)/10) return -1;
            값=값*10+글자;
        }
        return 값<=한도?값:-1;
    }
    static boolean 주소읽기(int 번호) {
        if (번호>=개수()) return false;
        int 값=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.길이[번호]; 순번++) {
            int 글자=명령해석기.토큰[명령해석기.시작점[번호]+순번];
            if (글자=='.') { if (숫자수==0 || ++점수>3) return false; 값=(값<<8)|덩이; 덩이=숫자수=0; }
            else { if (글자<'0' || 글자>'9' || ++숫자수>3) return false; 덩이=덩이*10+글자-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        주소값=(값<<8)|덩이; return true;
    }
    static void 주소쓰기(int 값) {
        단말.수((값>>>24)&255); 단말.문자('.'); 단말.수((값>>>16)&255); 단말.문자('.');
        단말.수((값>>>8)&255); 단말.문자('.'); 단말.수(값&255);
    }
    static void 망보기() {
        단말.Zapiszë(보드.망상태(20,0)!=0?"en0: ":"sl0: "); 단말.Zapiszë(보드.망상태(3,0)!=0?"UP":"DOWN");
        단말.Zapiszë(보드.망상태(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Zapiszë(보드.망상태(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); 주소쓰기(보드.망상태(0,0));
        단말.Zapiszë(" netmask "); 주소쓰기(보드.망상태(1,0)); 단말.Zapiszë(" gateway "); 주소쓰기(보드.망상태(2,0)); 단말.문자(10);
        단말.Zapiszë("  RX packets "); 단말.수(보드.망상태(4,0)); 단말.Zapiszë(" bytes "); 단말.수(보드.망상태(6,0));
        단말.Zapiszë(" TX packets "); 단말.수(보드.망상태(5,0)); 단말.Zapiszë(" bytes "); 단말.수(보드.망상태(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.망상태(8,0));
    }
    static void 주소설정(int 시작) {
        if (개수()!=시작+3 || !주소읽기(시작)) { 실패("사용법: ipconfig set 주소 주소가림 관문"); return; }
        int 주소=주소값;
        if(!주소읽기(시작+1)){실패("Invalid IPv4 netmask");return;} int 가림=주소값;
        if(!주소읽기(시작+2)){실패("Invalid IPv4 gateway");return;}
        int 결과=보드.망설정(0,주소,가림,주소값);
        if(결과<0) { Fela(결과); if(결과==-16)단말.Zapiszë("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Zapiszë("IPv4 configuration applied (until reboot)\n"); 망보기(); }
    }
    static void 망명령(boolean 아이피) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { 망보기();return; }
        if (아이피 && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { 경로보기();return; }
        if (같음(1,"set")) { 주소설정(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.망설정(같음(1,"up")?1:2,0,0,0);망보기();return; }
        if (아이피 && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.망설정(같음(5,"up")?1:2,0,0,0);망보기();return; }
        실패("사용법: ip [addr show|route show|set 주소 주소가림 관문|link set dev sl0 up|down]");
    }
    static void 경로보기() {
        단말.Zapiszë("Destination Netmask Gateway Interface\n");
        주소쓰기(보드.망상태(0,0)&보드.망상태(1,0));단말.문자(' ');주소쓰기(보드.망상태(1,0));단말.Zapiszë(보드.망상태(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.망상태(2,0)!=0) {단말.Zapiszë("0.0.0.0 0.0.0.0 ");주소쓰기(보드.망상태(2,0));단말.Zapiszë(보드.망상태(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void 통신보기() {
        단말.Zapiszë("Proto Local Remote State Queued\n");
        for(int 번호=0;번호<32;번호++) {
            int 유형=보드.망상태(10,번호);if(유형==0)continue;
            단말.Zapiszë(유형==1?"TCP ":"UDP ");주소쓰기(보드.망상태(16,번호));단말.문자(':');단말.수(보드.망상태(11,번호));단말.문자(' ');
            주소쓰기(보드.망상태(12,번호));단말.문자(':');단말.수(보드.망상태(13,번호));단말.문자(' ');
            int 상태=보드.망상태(14,번호);단말.Zapiszë(유형==2?"DATAGRAM":상태==1?"LISTEN":상태==2?"ESTABLISHED":상태==3?"CLOSE_WAIT":상태==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.망상태(15,번호));단말.문자(10);
        }
        단말.Zapiszë("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int 시작=보드.밀리초();
        while(보드.밀리초()-시작<밀리초) {
            if(셸입출력.대화가능()!=0){int 글자=보드.직렬읽기();if(글자==3 || 글자=='q' || 글자=='Q' || 글자==27 || 글자==-4096)return false;}
            보드.양보();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, 대상=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=숫자(++자리,100);if(횟수<1){실패("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=숫자(++자리,10);if(제한<1){실패("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(대상<0)대상=자리;else{실패("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(대상<0 || !주소읽기(대상)){실패("ping: an IPv4 address is required (DNS is not configured)");return;}
        int 주소=주소값, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Zapiszë("PING ");주소쓰기(주소);단말.Zapiszë(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int 순서=1;순서<=횟수 && 계속;순서++) {
            int 처리값=보드.응답보내기(주소,순서);
            if(처리값<0){Fela(처리값);break;}보낸수++;
            int 시작=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-시작<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.Zapiszë("32 bytes from ");주소쓰기(주소);단말.Zapiszë(" seq=");단말.수(순서);단말.Zapiszë(" ttl=");단말.수(보드.응답읽기(2));단말.Zapiszë(" time=");단말.수(시간);단말.Zapiszë(" ms\n");
            }else{단말.Zapiszë("Request timeout seq=");단말.수(순서);단말.문자(10);}
            if(순서<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.Zapiszë(" transmitted, ");단말.수(받은수);단말.Zapiszë(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.Zapiszë("% packet loss\n");
        if(받은수>0){단말.Zapiszë("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.Zapiszë(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void 가동보기() { 단말.Zapiszë("up ");단말.수(보드.밀리초()/1000);단말.Zapiszë(" seconds\n"); }
    static void 기억보기() {
        수항목("ARM RAM KiB (firmware): ",보드.체계조회(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.체계조회(1,0));
        int 총량=보드.체계조회(2,0), 사용량=보드.체계조회(3,0);
        단말.Zapiszë("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.체계조회(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.체계조회(5,0));
        int 매핑=0;for(int 번호=0;번호<4;번호++)매핑+=보드.체계조회(22,번호);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Zapiszë("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.Zapiszë("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Zapiszë("1 - RUN - - ");단말.수(보드.밀리초());단말.Zapiszë(" kernel/shell\n");
        for(int 번호=1;번호<3;번호++)if(보드.작업상태(번호)>0){단말.수(번호+1);단말.Zapiszë(" - READY 64 - - kernel-task\n");}
        for(int 번호=0;번호<4;번호++){
            int 상태=보드.체계조회(20,번호);if(상태==0)continue;
            단말.수(보드.체계조회(21,번호));단말.문자(' ');단말.수(번호);단말.Zapiszë(상태==1?" RUN ":" SUSPENDED ");
            단말.수(보드.체계조회(22,번호));단말.문자(' ');단말.수(보드.체계조회(24,번호));단말.문자(' ');단말.수(보드.체계조회(23,번호));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int 바이트=보드.체계조회(25,번호+자리*4);if(바이트==0)break;보드.직렬쓰기(바이트);}단말.문자(10);
        }
    }
    static void 저장보기() {
        int 칸수=0, 자료수=0;
        for(int 번호=0;번호<기억파일.파일수;번호++)if(기억파일.이름길이[번호]>0 || 기억파일.참조수[번호]>0){칸수++;자료수+=기억파일.길이[번호];}
        단말.Zapiszë("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(기억파일.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((기억파일.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(기억파일.파일수);단말.Zapiszë(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void 현황보기() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=숫자(2,1000))<1){실패("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int 차례=0;횟수==0 || 차례<횟수;차례++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Zapiszë("\u001b[2J\u001b[H");
            가동보기();기억보기();작업보기();
            if(횟수!=0 && 차례+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int 번호) {
        if(번호==0)return "ipconfig";if(번호==1)return "ip";if(번호==2)return "ping";if(번호==3)return "route";if(번호==4)return "netstat";
        if(번호==5)return "ps";if(번호==6)return "top";if(번호==7)return "free";if(번호==8)return "df";if(번호==9)return "uptime";if(번호==10)return "poweroff";return "help";
    }
    static void 도움말() {
        단말.Zapiszë("--- Network / system commands ---\n");
        for(int 번호=0;번호<12;번호++){단말.Zapiszë(표준말(번호));단말.Zapiszë(" / ");단말.Zapiszë(관리명령.말(번호));단말.Zapiszë(" : ");단말.Zapiszë(관리명령.설명(번호));단말.문자(10);}
        단말.Zapiszë("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Zapiszë("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Zapiszë("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean 실행() {
        int Pòlét=-1;
        for(int 번호=0;번호<12;번호++)if(같음(0,표준말(번호)) || 같음(0,관리명령.말(번호)))Pòlét=번호;
        if(같음(0,"ifconfig"))Pòlét=0;if(같음(0,"ss"))Pòlét=4;
        if(Pòlét<0)return false;
        if(Pòlét==11){if(같음(1,"net") || 같음(1,"system"))도움말();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.도움말();return true;}
        if(Pòlét==0 || Pòlét==1)망명령(Pòlét==1);
        else if(Pòlét==2)응답시험();
        else if(Pòlét==6)현황보기();
        else if(개수()!=1){실패("This command takes no arguments; help system");}
        else if(Pòlét==3)경로보기();else if(Pòlét==4)통신보기();else if(Pòlét==5)작업보기();else if(Pòlét==7)기억보기();else if(Pòlét==8)저장보기();else if(Pòlét==9)가동보기();
        else if(Pòlét==10)보드.전원끄기();
        return true;
    }
}
