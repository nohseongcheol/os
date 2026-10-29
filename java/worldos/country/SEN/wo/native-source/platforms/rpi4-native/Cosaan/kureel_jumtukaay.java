// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** liteew_mbir xoox_xëyma 상태를 읽는 IPv4·ICMP·작업·fatlekookaay_xëyma·RAM 저장소 관리 ndigel. */
public final class kureel_jumtukaay {
    static int dëkkuwaay_xëyma;
    static boolean 같음(int àlluwa_tur, String Word_SMS) { return 명령해석기.같음(àlluwa_tur, Word_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void foo_xëyma(String JANG_MA_eb81d7d9) { 명령해석기.결과=2; 단말.biir(JANG_MA_eb81d7d9); 단말.문자(10); }
    static void njumte(int xëyma) { 명령해석기.njumte(xëyma); }
    static void 수항목(String tur_253d1510, int xëyma) { 단말.biir(tur_253d1510); 단말.수(xëyma); 단말.문자(10); }
    static int siifar_xëyma(int àlluwa_tur, int 한도) {
        if (àlluwa_tur>=개수() || 명령해석기.diir_xëyma[àlluwa_tur]==0) return -1;
        int xëyma=0;
        for (int 순번=0; 순번<명령해석기.diir_xëyma[àlluwa_tur]; 순번++) {
            int Araf_xëyma=명령해석기.jeton_xëyma[명령해석기.시작점[àlluwa_tur]+순번]-'0';
            if (Araf_xëyma<0 || Araf_xëyma>9 || xëyma>(한도-Araf_xëyma)/10) return -1;
            xëyma=xëyma*10+Araf_xëyma;
        }
        return xëyma<=한도?xëyma:-1;
    }
    static boolean 주소읽기(int àlluwa_tur) {
        if (àlluwa_tur>=개수()) return false;
        int xëyma=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.diir_xëyma[àlluwa_tur]; 순번++) {
            int Araf_xëyma=명령해석기.jeton_xëyma[명령해석기.시작점[àlluwa_tur]+순번];
            if (Araf_xëyma=='.') { if (숫자수==0 || ++점수>3) return false; xëyma=(xëyma<<8)|덩이; 덩이=숫자수=0; }
            else { if (Araf_xëyma<'0' || Araf_xëyma>'9' || ++숫자수>3) return false; 덩이=덩이*10+Araf_xëyma-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        dëkkuwaay_xëyma=(xëyma<<8)|덩이; return true;
    }
    static void biir_dëkkuwaay(int xëyma) {
        단말.수((xëyma>>>24)&255); 단말.문자('.'); 단말.수((xëyma>>>16)&255); 단말.문자('.');
        단말.수((xëyma>>>8)&255); 단말.문자('.'); 단말.수(xëyma&255);
    }
    static void féeñal_mbaal_nekkin() {
        단말.biir(보드.mbaal_nekkin(20,0)!=0?"en0: ":"sl0: "); 단말.biir(보드.mbaal_nekkin(3,0)!=0?"UP":"DOWN");
        단말.biir(보드.mbaal_nekkin(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.biir(보드.mbaal_nekkin(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); biir_dëkkuwaay(보드.mbaal_nekkin(0,0));
        단말.biir(" netmask "); biir_dëkkuwaay(보드.mbaal_nekkin(1,0)); 단말.biir(" gateway "); biir_dëkkuwaay(보드.mbaal_nekkin(2,0)); 단말.문자(10);
        단말.biir("  RX packets "); 단말.수(보드.mbaal_nekkin(4,0)); 단말.biir(" bytes "); 단말.수(보드.mbaal_nekkin(6,0));
        단말.biir(" TX packets "); 단말.수(보드.mbaal_nekkin(5,0)); 단말.biir(" bytes "); 단말.수(보드.mbaal_nekkin(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.mbaal_nekkin(8,0));
    }
    static void Boole_gi_dëkkuwaay(int daw) {
        if (개수()!=daw+3 || !주소읽기(daw)) { foo_xëyma("사용법: ipconfig set dëkkuwaay 주소가림 bunt_xëyma"); return; }
        int dëkkuwaay=dëkkuwaay_xëyma;
        if(!주소읽기(daw+1)){foo_xëyma("Invalid IPv4 netmask");return;} int muuraay_xëyma=dëkkuwaay_xëyma;
        if(!주소읽기(daw+2)){foo_xëyma("Invalid IPv4 gateway");return;}
        int 결과=보드.mbaal_Jekkal_yi(0,dëkkuwaay,muuraay_xëyma,dëkkuwaay_xëyma);
        if(결과<0) { njumte(결과); if(결과==-16)단말.biir("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.biir("IPv4 configuration applied (until reboot)\n"); féeñal_mbaal_nekkin(); }
    }
    static void mbaal_ndigel(boolean dëkkuwaayu_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { féeñal_mbaal_nekkin();return; }
        if (dëkkuwaayu_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { féeñal_Yoonu_jëmale();return; }
        if (같음(1,"set")) { Boole_gi_dëkkuwaay(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.mbaal_Jekkal_yi(같음(1,"up")?1:2,0,0,0);féeñal_mbaal_nekkin();return; }
        if (dëkkuwaayu_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.mbaal_Jekkal_yi(같음(5,"up")?1:2,0,0,0);féeñal_mbaal_nekkin();return; }
        foo_xëyma("사용법: ip [addr show|route show|set dëkkuwaay 주소가림 bunt_xëyma|link set dev sl0 up|down]");
    }
    static void féeñal_Yoonu_jëmale() {
        단말.biir("Destination Netmask Gateway Interface\n");
        biir_dëkkuwaay(보드.mbaal_nekkin(0,0)&보드.mbaal_nekkin(1,0));단말.문자(' ');biir_dëkkuwaay(보드.mbaal_nekkin(1,0));단말.biir(보드.mbaal_nekkin(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.mbaal_nekkin(2,0)!=0) {단말.biir("0.0.0.0 0.0.0.0 ");biir_dëkkuwaay(보드.mbaal_nekkin(2,0));단말.biir(보드.mbaal_nekkin(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void féeñal_mbaal() {
        단말.biir("Proto Local Remote State Queued\n");
        for(int àlluwa_tur=0;àlluwa_tur<32;àlluwa_tur++) {
            int xeet_ngiir=보드.mbaal_nekkin(10,àlluwa_tur);if(xeet_ngiir==0)continue;
            단말.biir(xeet_ngiir==1?"TCP ":"UDP ");biir_dëkkuwaay(보드.mbaal_nekkin(16,àlluwa_tur));단말.문자(':');단말.수(보드.mbaal_nekkin(11,àlluwa_tur));단말.문자(' ');
            biir_dëkkuwaay(보드.mbaal_nekkin(12,àlluwa_tur));단말.문자(':');단말.수(보드.mbaal_nekkin(13,àlluwa_tur));단말.문자(' ');
            int nekkin_xëyma=보드.mbaal_nekkin(14,àlluwa_tur);단말.biir(xeet_ngiir==2?"DATAGRAM":nekkin_xëyma==1?"LISTEN":nekkin_xëyma==2?"ESTABLISHED":nekkin_xëyma==3?"CLOSE_WAIT":nekkin_xëyma==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.mbaal_nekkin(15,àlluwa_tur));단말.문자(10);
        }
        단말.biir("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int daw=보드.밀리초();
        while(보드.밀리초()-daw<밀리초) {
            if(셸입출력.대화가능()!=0){int Araf_xëyma=보드.직렬읽기();if(Araf_xëyma==3 || Araf_xëyma=='q' || Araf_xëyma=='Q' || Araf_xëyma==27 || Araf_xëyma==-4096)return false;}
            보드.dakkal_UC();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, luñu_name=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=siifar_xëyma(++자리,100);if(횟수<1){foo_xëyma("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=siifar_xëyma(++자리,10);if(제한<1){foo_xëyma("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(luñu_name<0)luñu_name=자리;else{foo_xëyma("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(luñu_name<0 || !주소읽기(luñu_name)){foo_xëyma("ping: an IPv4 address is required (DNS is not configured)");return;}
        int dëkkuwaay=dëkkuwaay_xëyma, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.biir("PING ");biir_dëkkuwaay(dëkkuwaay);단말.biir(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int toftale_xëyma=1;toftale_xëyma<=횟수 && 계속;toftale_xëyma++) {
            int 처리값=보드.응답보내기(dëkkuwaay,toftale_xëyma);
            if(처리값<0){njumte(처리값);break;}보낸수++;
            int daw=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-daw<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.biir("32 bytes from ");biir_dëkkuwaay(dëkkuwaay);단말.biir(" seq=");단말.수(toftale_xëyma);단말.biir(" ttl=");단말.수(보드.응답읽기(2));단말.biir(" time=");단말.수(시간);단말.biir(" ms\n");
            }else{단말.biir("Request timeout seq=");단말.수(toftale_xëyma);단말.문자(10);}
            if(toftale_xëyma<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.biir(" transmitted, ");단말.수(받은수);단말.biir(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.biir("% packet loss\n");
        if(받은수>0){단말.biir("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.biir(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void féeñal_Jëf() { 단말.biir("up ");단말.수(보드.밀리초()/1000);단말.biir(" seconds\n"); }
    static void féeñal_fatlekookaay() {
        수항목("ARM RAM KiB (firmware): ",보드.laaj_kureel(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.laaj_kureel(1,0));
        int 총량=보드.laaj_kureel(2,0), 사용량=보드.laaj_kureel(3,0);
        단말.biir("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.laaj_kureel(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.laaj_kureel(5,0));
        int 매핑=0;for(int àlluwa_tur=0;àlluwa_tur<4;àlluwa_tur++)매핑+=보드.laaj_kureel(22,àlluwa_tur);
        수항목("EL0 mapped KiB: ",매핑);
        단말.biir("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.biir("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.biir("1 - RUN - - ");단말.수(보드.밀리초());단말.biir(" kernel/shell\n");
        for(int àlluwa_tur=1;àlluwa_tur<3;àlluwa_tur++)if(보드.ligeey_nekkin(àlluwa_tur)>0){단말.수(àlluwa_tur+1);단말.biir(" - READY 64 - - kernel-task\n");}
        for(int àlluwa_tur=0;àlluwa_tur<4;àlluwa_tur++){
            int nekkin_xëyma=보드.laaj_kureel(20,àlluwa_tur);if(nekkin_xëyma==0)continue;
            단말.수(보드.laaj_kureel(21,àlluwa_tur));단말.문자(' ');단말.수(àlluwa_tur);단말.biir(nekkin_xëyma==1?" RUN ":" SUSPENDED ");
            단말.수(보드.laaj_kureel(22,àlluwa_tur));단말.문자(' ');단말.수(보드.laaj_kureel(24,àlluwa_tur));단말.문자(' ');단말.수(보드.laaj_kureel(23,àlluwa_tur));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int okte_xëyma=보드.laaj_kureel(25,àlluwa_tur+자리*4);if(okte_xëyma==0)break;보드.직렬쓰기(okte_xëyma);}단말.문자(10);
        }
    }
    static void féeñal_Dencukaay() {
        int 칸수=0, 자료수=0;
        for(int àlluwa_tur=0;àlluwa_tur<fatlekookaay_Fisiye_yi.파일수;àlluwa_tur++)if(fatlekookaay_Fisiye_yi.이름길이[àlluwa_tur]>0 || fatlekookaay_Fisiye_yi.참조수[àlluwa_tur]>0){칸수++;자료수+=fatlekookaay_Fisiye_yi.diir_xëyma[àlluwa_tur];}
        단말.biir("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(fatlekookaay_Fisiye_yi.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((fatlekookaay_Fisiye_yi.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(fatlekookaay_Fisiye_yi.파일수);단말.biir(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void féeñal_nekkin_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=siifar_xëyma(2,1000))<1){foo_xëyma("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int SEQUENCE_xëyma=0;횟수==0 || SEQUENCE_xëyma<횟수;SEQUENCE_xëyma++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.biir("\u001b[2J\u001b[H");
            féeñal_Jëf();féeñal_fatlekookaay();작업보기();
            if(횟수!=0 && SEQUENCE_xëyma+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int àlluwa_tur) {
        if(àlluwa_tur==0)return "ipconfig";if(àlluwa_tur==1)return "ip";if(àlluwa_tur==2)return "ping";if(àlluwa_tur==3)return "route";if(àlluwa_tur==4)return "netstat";
        if(àlluwa_tur==5)return "ps";if(àlluwa_tur==6)return "top";if(àlluwa_tur==7)return "free";if(àlluwa_tur==8)return "df";if(àlluwa_tur==9)return "uptime";if(àlluwa_tur==10)return "poweroff";return "help";
    }
    static void féeñal_ndimbal() {
        단말.biir("--- Network / system commands ---\n");
        for(int àlluwa_tur=0;àlluwa_tur<12;àlluwa_tur++){단말.biir(표준말(àlluwa_tur));단말.biir(" / ");단말.biir(관리명령.Word_SMS(àlluwa_tur));단말.biir(" : ");단말.biir(관리명령.설명(àlluwa_tur));단말.문자(10);}
        단말.biir("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.biir("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.biir("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean def_ndigel() {
        int ndigel=-1;
        for(int àlluwa_tur=0;àlluwa_tur<12;àlluwa_tur++)if(같음(0,표준말(àlluwa_tur)) || 같음(0,관리명령.Word_SMS(àlluwa_tur)))ndigel=àlluwa_tur;
        if(같음(0,"ifconfig"))ndigel=0;if(같음(0,"ss"))ndigel=4;
        if(ndigel<0)return false;
        if(ndigel==11){if(같음(1,"net") || 같음(1,"system"))féeñal_ndimbal();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.féeñal_ndimbal();return true;}
        if(ndigel==0 || ndigel==1)mbaal_ndigel(ndigel==1);
        else if(ndigel==2)응답시험();
        else if(ndigel==6)féeñal_nekkin_bf9821b5();
        else if(개수()!=1){foo_xëyma("This command takes no arguments; help system");}
        else if(ndigel==3)féeñal_Yoonu_jëmale();else if(ndigel==4)féeñal_mbaal();else if(ndigel==5)작업보기();else if(ndigel==7)féeñal_fatlekookaay();else if(ndigel==8)féeñal_Dencukaay();else if(ndigel==9)féeñal_Jëf();
        else if(ndigel==10)보드.전원끄기();
        return true;
    }
}
