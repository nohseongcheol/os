// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kgonthe_data khenele_boleng 상태를 읽는 IPv4·ICMP·작업·memori_boleng·RAM 저장소 관리 Taelo. */
public final class lenaneo_tholosi {
    static int atrese_boleng;
    static boolean 같음(int lokela, String Thalokontšu_SMS) { return 명령해석기.같음(lokela, Thalokontšu_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void go_palelwa_boleng(String faele_ya_MPALE_eb81d7d9) { 명령해석기.결과=2; 단말.Ngwala(faele_ya_MPALE_eb81d7d9); 단말.문자(10); }
    static void Phošo(int boleng) { 명령해석기.Phošo(boleng); }
    static void 수항목(String Leina, int boleng) { 단말.Ngwala(Leina); 단말.수(boleng); 단말.문자(10); }
    static int 숫자(int lokela, int 한도) {
        if (lokela>=개수() || 명령해석기.botelele_boleng[lokela]==0) return -1;
        int boleng=0;
        for (int 순번=0; 순번<명령해석기.botelele_boleng[lokela]; 순번++) {
            int tlhaka_boleng=명령해석기.thokene_boleng[명령해석기.시작점[lokela]+순번]-'0';
            if (tlhaka_boleng<0 || tlhaka_boleng>9 || boleng>(한도-tlhaka_boleng)/10) return -1;
            boleng=boleng*10+tlhaka_boleng;
        }
        return boleng<=한도?boleng:-1;
    }
    static boolean 주소읽기(int lokela) {
        if (lokela>=개수()) return false;
        int boleng=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.botelele_boleng[lokela]; 순번++) {
            int tlhaka_boleng=명령해석기.thokene_boleng[명령해석기.시작점[lokela]+순번];
            if (tlhaka_boleng=='.') { if (숫자수==0 || ++점수>3) return false; boleng=(boleng<<8)|덩이; 덩이=숫자수=0; }
            else { if (tlhaka_boleng<'0' || tlhaka_boleng>'9' || ++숫자수>3) return false; 덩이=덩이*10+tlhaka_boleng-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        atrese_boleng=(boleng<<8)|덩이; return true;
    }
    static void ngwala_atrese(int boleng) {
        단말.수((boleng>>>24)&255); 단말.문자('.'); 단말.수((boleng>>>16)&255); 단말.문자('.');
        단말.수((boleng>>>8)&255); 단말.문자('.'); 단말.수(boleng&255);
    }
    static void bontšha_Netweke_boemo() {
        단말.Ngwala(보드.Netweke_boemo(20,0)!=0?"en0: ":"sl0: "); 단말.Ngwala(보드.Netweke_boemo(3,0)!=0?"UP":"DOWN");
        단말.Ngwala(보드.Netweke_boemo(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Ngwala(보드.Netweke_boemo(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); ngwala_atrese(보드.Netweke_boemo(0,0));
        단말.Ngwala(" netmask "); ngwala_atrese(보드.Netweke_boemo(1,0)); 단말.Ngwala(" gateway "); ngwala_atrese(보드.Netweke_boemo(2,0)); 단말.문자(10);
        단말.Ngwala("  RX packets "); 단말.수(보드.Netweke_boemo(4,0)); 단말.Ngwala(" bytes "); 단말.수(보드.Netweke_boemo(6,0));
        단말.Ngwala(" TX packets "); 단말.수(보드.Netweke_boemo(5,0)); 단말.Ngwala(" bytes "); 단말.수(보드.Netweke_boemo(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Netweke_boemo(8,0));
    }
    static void sehlopha_atrese(int Diriša) {
        if (개수()!=Diriša+3 || !주소읽기(Diriša)) { go_palelwa_boleng("사용법: ipconfig set atrese 주소가림 tsela_ya_netweke_boleng"); return; }
        int atrese=atrese_boleng;
        if(!주소읽기(Diriša+1)){go_palelwa_boleng("Invalid IPv4 netmask");return;} int maseke_boleng=atrese_boleng;
        if(!주소읽기(Diriša+2)){go_palelwa_boleng("Invalid IPv4 gateway");return;}
        int 결과=보드.Netweke_Dipeakanyo(0,atrese,maseke_boleng,atrese_boleng);
        if(결과<0) { Phošo(결과); if(결과==-16)단말.Ngwala("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Ngwala("IPv4 configuration applied (until reboot)\n"); bontšha_Netweke_boemo(); }
    }
    static void Netweke_taelo(boolean atrese_ya_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { bontšha_Netweke_boemo();return; }
        if (atrese_ya_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { bontšha_tsela();return; }
        if (같음(1,"set")) { sehlopha_atrese(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.Netweke_Dipeakanyo(같음(1,"up")?1:2,0,0,0);bontšha_Netweke_boemo();return; }
        if (atrese_ya_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.Netweke_Dipeakanyo(같음(5,"up")?1:2,0,0,0);bontšha_Netweke_boemo();return; }
        go_palelwa_boleng("사용법: ip [addr show|route show|set atrese 주소가림 tsela_ya_netweke_boleng|link set dev sl0 up|down]");
    }
    static void bontšha_tsela() {
        단말.Ngwala("Destination Netmask Gateway Interface\n");
        ngwala_atrese(보드.Netweke_boemo(0,0)&보드.Netweke_boemo(1,0));단말.문자(' ');ngwala_atrese(보드.Netweke_boemo(1,0));단말.Ngwala(보드.Netweke_boemo(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Netweke_boemo(2,0)!=0) {단말.Ngwala("0.0.0.0 0.0.0.0 ");ngwala_atrese(보드.Netweke_boemo(2,0));단말.Ngwala(보드.Netweke_boemo(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void bontšha_Netweke() {
        단말.Ngwala("Proto Local Remote State Queued\n");
        for(int lokela=0;lokela<32;lokela++) {
            int thaepa_legoro=보드.Netweke_boemo(10,lokela);if(thaepa_legoro==0)continue;
            단말.Ngwala(thaepa_legoro==1?"TCP ":"UDP ");ngwala_atrese(보드.Netweke_boemo(16,lokela));단말.문자(':');단말.수(보드.Netweke_boemo(11,lokela));단말.문자(' ');
            ngwala_atrese(보드.Netweke_boemo(12,lokela));단말.문자(':');단말.수(보드.Netweke_boemo(13,lokela));단말.문자(' ');
            int boemo_boleng=보드.Netweke_boemo(14,lokela);단말.Ngwala(thaepa_legoro==2?"DATAGRAM":boemo_boleng==1?"LISTEN":boemo_boleng==2?"ESTABLISHED":boemo_boleng==3?"CLOSE_WAIT":boemo_boleng==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Netweke_boemo(15,lokela));단말.문자(10);
        }
        단말.Ngwala("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int Diriša=보드.밀리초();
        while(보드.밀리초()-Diriša<밀리초) {
            if(셸입출력.대화가능()!=0){int tlhaka_boleng=보드.직렬읽기();if(tlhaka_boleng==3 || tlhaka_boleng=='q' || tlhaka_boleng=='Q' || tlhaka_boleng==27 || tlhaka_boleng==-4096)return false;}
            보드.e_thibetšwe_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, nepo=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=숫자(++자리,100);if(횟수<1){go_palelwa_boleng("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=숫자(++자리,10);if(제한<1){go_palelwa_boleng("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(nepo<0)nepo=자리;else{go_palelwa_boleng("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(nepo<0 || !주소읽기(nepo)){go_palelwa_boleng("ping: an IPv4 address is required (DNS is not configured)");return;}
        int atrese=atrese_boleng, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Ngwala("PING ");ngwala_atrese(atrese);단말.Ngwala(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int thulaganyo_boleng=1;thulaganyo_boleng<=횟수 && 계속;thulaganyo_boleng++) {
            int 처리값=보드.응답보내기(atrese,thulaganyo_boleng);
            if(처리값<0){Phošo(처리값);break;}보낸수++;
            int Diriša=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-Diriša<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.Ngwala("32 bytes from ");ngwala_atrese(atrese);단말.Ngwala(" seq=");단말.수(thulaganyo_boleng);단말.Ngwala(" ttl=");단말.수(보드.응답읽기(2));단말.Ngwala(" time=");단말.수(시간);단말.Ngwala(" ms\n");
            }else{단말.Ngwala("Request timeout seq=");단말.수(thulaganyo_boleng);단말.문자(10);}
            if(thulaganyo_boleng<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.Ngwala(" transmitted, ");단말.수(받은수);단말.Ngwala(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.Ngwala("% packet loss\n");
        if(받은수>0){단말.Ngwala("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.Ngwala(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void bontšha_Modiro() { 단말.Ngwala("up ");단말.수(보드.밀리초()/1000);단말.Ngwala(" seconds\n"); }
    static void bontšha_memori() {
        수항목("ARM RAM KiB (firmware): ",보드.kwiri_lenaneo(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.kwiri_lenaneo(1,0));
        int 총량=보드.kwiri_lenaneo(2,0), 사용량=보드.kwiri_lenaneo(3,0);
        단말.Ngwala("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.kwiri_lenaneo(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.kwiri_lenaneo(5,0));
        int 매핑=0;for(int lokela=0;lokela<4;lokela++)매핑+=보드.kwiri_lenaneo(22,lokela);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Ngwala("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.Ngwala("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Ngwala("1 - RUN - - ");단말.수(보드.밀리초());단말.Ngwala(" kernel/shell\n");
        for(int lokela=1;lokela<3;lokela++)if(보드.mošomo_boemo(lokela)>0){단말.수(lokela+1);단말.Ngwala(" - READY 64 - - kernel-task\n");}
        for(int lokela=0;lokela<4;lokela++){
            int boemo_boleng=보드.kwiri_lenaneo(20,lokela);if(boemo_boleng==0)continue;
            단말.수(보드.kwiri_lenaneo(21,lokela));단말.문자(' ');단말.수(lokela);단말.Ngwala(boemo_boleng==1?" RUN ":" SUSPENDED ");
            단말.수(보드.kwiri_lenaneo(22,lokela));단말.문자(' ');단말.수(보드.kwiri_lenaneo(24,lokela));단말.문자(' ');단말.수(보드.kwiri_lenaneo(23,lokela));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int paete_boleng=보드.kwiri_lenaneo(25,lokela+자리*4);if(paete_boleng==0)break;보드.직렬쓰기(paete_boleng);}단말.문자(10);
        }
    }
    static void bontšha_Bobolokelo() {
        int 칸수=0, 자료수=0;
        for(int lokela=0;lokela<memori_Difaele.파일수;lokela++)if(memori_Difaele.이름길이[lokela]>0 || memori_Difaele.참조수[lokela]>0){칸수++;자료수+=memori_Difaele.botelele_boleng[lokela];}
        단말.Ngwala("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(memori_Difaele.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((memori_Difaele.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(memori_Difaele.파일수);단말.Ngwala(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void bontšha_boemo_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=숫자(2,1000))<1){go_palelwa_boleng("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int TATELANO_boleng=0;횟수==0 || TATELANO_boleng<횟수;TATELANO_boleng++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Ngwala("\u001b[2J\u001b[H");
            bontšha_Modiro();bontšha_memori();작업보기();
            if(횟수!=0 && TATELANO_boleng+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int lokela) {
        if(lokela==0)return "ipconfig";if(lokela==1)return "ip";if(lokela==2)return "ping";if(lokela==3)return "route";if(lokela==4)return "netstat";
        if(lokela==5)return "ps";if(lokela==6)return "top";if(lokela==7)return "free";if(lokela==8)return "df";if(lokela==9)return "uptime";if(lokela==10)return "poweroff";return "help";
    }
    static void bontšha_thušo() {
        단말.Ngwala("--- Network / system commands ---\n");
        for(int lokela=0;lokela<12;lokela++){단말.Ngwala(표준말(lokela));단말.Ngwala(" / ");단말.Ngwala(관리명령.Thalokontšu_SMS(lokela));단말.Ngwala(" : ");단말.Ngwala(관리명령.설명(lokela));단말.문자(10);}
        단말.Ngwala("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Ngwala("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Ngwala("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean phethagatša_taelo() {
        int Taelo=-1;
        for(int lokela=0;lokela<12;lokela++)if(같음(0,표준말(lokela)) || 같음(0,관리명령.Thalokontšu_SMS(lokela)))Taelo=lokela;
        if(같음(0,"ifconfig"))Taelo=0;if(같음(0,"ss"))Taelo=4;
        if(Taelo<0)return false;
        if(Taelo==11){if(같음(1,"net") || 같음(1,"system"))bontšha_thušo();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.bontšha_thušo();return true;}
        if(Taelo==0 || Taelo==1)Netweke_taelo(Taelo==1);
        else if(Taelo==2)응답시험();
        else if(Taelo==6)bontšha_boemo_bf9821b5();
        else if(개수()!=1){go_palelwa_boleng("This command takes no arguments; help system");}
        else if(Taelo==3)bontšha_tsela();else if(Taelo==4)bontšha_Netweke();else if(Taelo==5)작업보기();else if(Taelo==7)bontšha_memori();else if(Taelo==8)bontšha_Bobolokelo();else if(Taelo==9)bontšha_Modiro();
        else if(Taelo==10)보드.전원끄기();
        return true;
    }
}
