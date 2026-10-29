// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tota_tshedimosetso Khenele_Boleng 상태를 읽는 IPv4·ICMP·작업·memori_Boleng·RAM 저장소 관리 Taelo. */
public final class tsamaiso_sediriswa {
    static int aterese_Boleng;
    static boolean 같음(int tshupane, String Lefoko_SMS) { return 명령해석기.같음(tshupane, Lefoko_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void palelo_Boleng(String MPUISE_eb81d7d9) { 명령해석기.결과=2; 단말.kwala(MPUISE_eb81d7d9); 단말.문자(10); }
    static void phoso(int Boleng) { 명령해석기.phoso(Boleng); }
    static void 수항목(String leina, int Boleng) { 단말.kwala(leina); 단말.수(Boleng); 단말.문자(10); }
    static int dijite_Boleng(int tshupane, int 한도) {
        if (tshupane>=개수() || 명령해석기.boleele_Boleng[tshupane]==0) return -1;
        int Boleng=0;
        for (int 순번=0; 순번<명령해석기.boleele_Boleng[tshupane]; 순번++) {
            int Letshwao_Boleng=명령해석기.papetlana_Boleng[명령해석기.시작점[tshupane]+순번]-'0';
            if (Letshwao_Boleng<0 || Letshwao_Boleng>9 || Boleng>(한도-Letshwao_Boleng)/10) return -1;
            Boleng=Boleng*10+Letshwao_Boleng;
        }
        return Boleng<=한도?Boleng:-1;
    }
    static boolean 주소읽기(int tshupane) {
        if (tshupane>=개수()) return false;
        int Boleng=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.boleele_Boleng[tshupane]; 순번++) {
            int Letshwao_Boleng=명령해석기.papetlana_Boleng[명령해석기.시작점[tshupane]+순번];
            if (Letshwao_Boleng=='.') { if (숫자수==0 || ++점수>3) return false; Boleng=(Boleng<<8)|덩이; 덩이=숫자수=0; }
            else { if (Letshwao_Boleng<'0' || Letshwao_Boleng>'9' || ++숫자수>3) return false; 덩이=덩이*10+Letshwao_Boleng-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        aterese_Boleng=(Boleng<<8)|덩이; return true;
    }
    static void kwala_aterese(int Boleng) {
        단말.수((Boleng>>>24)&255); 단말.문자('.'); 단말.수((Boleng>>>16)&255); 단말.문자('.');
        단말.수((Boleng>>>8)&255); 단말.문자('.'); 단말.수(Boleng&255);
    }
    static void bontsha_Neteweke_kemo() {
        단말.kwala(보드.Neteweke_kemo(20,0)!=0?"en0: ":"sl0: "); 단말.kwala(보드.Neteweke_kemo(3,0)!=0?"UP":"DOWN");
        단말.kwala(보드.Neteweke_kemo(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.kwala(보드.Neteweke_kemo(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); kwala_aterese(보드.Neteweke_kemo(0,0));
        단말.kwala(" netmask "); kwala_aterese(보드.Neteweke_kemo(1,0)); 단말.kwala(" gateway "); kwala_aterese(보드.Neteweke_kemo(2,0)); 단말.문자(10);
        단말.kwala("  RX packets "); 단말.수(보드.Neteweke_kemo(4,0)); 단말.kwala(" bytes "); 단말.수(보드.Neteweke_kemo(6,0));
        단말.kwala(" TX packets "); 단말.수(보드.Neteweke_kemo(5,0)); 단말.kwala(" bytes "); 단말.수(보드.Neteweke_kemo(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Neteweke_kemo(8,0));
    }
    static void sete_aterese(int dirisa) {
        if (개수()!=dirisa+3 || !주소읽기(dirisa)) { palelo_Boleng("사용법: ipconfig set aterese 주소가림 kgorotsamaiso_Boleng"); return; }
        int aterese=aterese_Boleng;
        if(!주소읽기(dirisa+1)){palelo_Boleng("Invalid IPv4 netmask");return;} int mmaseke_Boleng=aterese_Boleng;
        if(!주소읽기(dirisa+2)){palelo_Boleng("Invalid IPv4 gateway");return;}
        int 결과=보드.Neteweke_Diseting(0,aterese,mmaseke_Boleng,aterese_Boleng);
        if(결과<0) { phoso(결과); if(결과==-16)단말.kwala("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.kwala("IPv4 configuration applied (until reboot)\n"); bontsha_Neteweke_kemo(); }
    }
    static void Neteweke_Taelo(boolean IP_aterese) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { bontsha_Neteweke_kemo();return; }
        if (IP_aterese && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { bontsha_tsela();return; }
        if (같음(1,"set")) { sete_aterese(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.Neteweke_Diseting(같음(1,"up")?1:2,0,0,0);bontsha_Neteweke_kemo();return; }
        if (IP_aterese && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.Neteweke_Diseting(같음(5,"up")?1:2,0,0,0);bontsha_Neteweke_kemo();return; }
        palelo_Boleng("사용법: ip [addr show|route show|set aterese 주소가림 kgorotsamaiso_Boleng|link set dev sl0 up|down]");
    }
    static void bontsha_tsela() {
        단말.kwala("Destination Netmask Gateway Interface\n");
        kwala_aterese(보드.Neteweke_kemo(0,0)&보드.Neteweke_kemo(1,0));단말.문자(' ');kwala_aterese(보드.Neteweke_kemo(1,0));단말.kwala(보드.Neteweke_kemo(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Neteweke_kemo(2,0)!=0) {단말.kwala("0.0.0.0 0.0.0.0 ");kwala_aterese(보드.Neteweke_kemo(2,0));단말.kwala(보드.Neteweke_kemo(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void bontsha_Neteweke() {
        단말.kwala("Proto Local Remote State Queued\n");
        for(int tshupane=0;tshupane<32;tshupane++) {
            int tlanya_setlhopha=보드.Neteweke_kemo(10,tshupane);if(tlanya_setlhopha==0)continue;
            단말.kwala(tlanya_setlhopha==1?"TCP ":"UDP ");kwala_aterese(보드.Neteweke_kemo(16,tshupane));단말.문자(':');단말.수(보드.Neteweke_kemo(11,tshupane));단말.문자(' ');
            kwala_aterese(보드.Neteweke_kemo(12,tshupane));단말.문자(':');단말.수(보드.Neteweke_kemo(13,tshupane));단말.문자(' ');
            int kemo_Boleng=보드.Neteweke_kemo(14,tshupane);단말.kwala(tlanya_setlhopha==2?"DATAGRAM":kemo_Boleng==1?"LISTEN":kemo_Boleng==2?"ESTABLISHED":kemo_Boleng==3?"CLOSE_WAIT":kemo_Boleng==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Neteweke_kemo(15,tshupane));단말.문자(10);
        }
        단말.kwala("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int dirisa=보드.밀리초();
        while(보드.밀리초()-dirisa<밀리초) {
            if(셸입출력.대화가능()!=0){int Letshwao_Boleng=보드.직렬읽기();if(Letshwao_Boleng==3 || Letshwao_Boleng=='q' || Letshwao_Boleng=='Q' || Letshwao_Boleng==27 || Letshwao_Boleng==-4096)return false;}
            보드.emisa_ka_nakwana_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, setotwa=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=dijite_Boleng(++자리,100);if(횟수<1){palelo_Boleng("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=dijite_Boleng(++자리,10);if(제한<1){palelo_Boleng("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(setotwa<0)setotwa=자리;else{palelo_Boleng("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(setotwa<0 || !주소읽기(setotwa)){palelo_Boleng("ping: an IPv4 address is required (DNS is not configured)");return;}
        int aterese=aterese_Boleng, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.kwala("PING ");kwala_aterese(aterese);단말.kwala(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int thulaganyo_Boleng=1;thulaganyo_Boleng<=횟수 && 계속;thulaganyo_Boleng++) {
            int 처리값=보드.응답보내기(aterese,thulaganyo_Boleng);
            if(처리값<0){phoso(처리값);break;}보낸수++;
            int dirisa=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-dirisa<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.kwala("32 bytes from ");kwala_aterese(aterese);단말.kwala(" seq=");단말.수(thulaganyo_Boleng);단말.kwala(" ttl=");단말.수(보드.응답읽기(2));단말.kwala(" time=");단말.수(시간);단말.kwala(" ms\n");
            }else{단말.kwala("Request timeout seq=");단말.수(thulaganyo_Boleng);단말.문자(10);}
            if(thulaganyo_Boleng<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.kwala(" transmitted, ");단말.수(받은수);단말.kwala(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.kwala("% packet loss\n");
        if(받은수>0){단말.kwala("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.kwala(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void bontsha_Tiro() { 단말.kwala("up ");단말.수(보드.밀리초()/1000);단말.kwala(" seconds\n"); }
    static void bontsha_memori() {
        수항목("ARM RAM KiB (firmware): ",보드.fenenkolola_tsamaiso(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.fenenkolola_tsamaiso(1,0));
        int 총량=보드.fenenkolola_tsamaiso(2,0), 사용량=보드.fenenkolola_tsamaiso(3,0);
        단말.kwala("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.fenenkolola_tsamaiso(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.fenenkolola_tsamaiso(5,0));
        int 매핑=0;for(int tshupane=0;tshupane<4;tshupane++)매핑+=보드.fenenkolola_tsamaiso(22,tshupane);
        수항목("EL0 mapped KiB: ",매핑);
        단말.kwala("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.kwala("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.kwala("1 - RUN - - ");단말.수(보드.밀리초());단말.kwala(" kernel/shell\n");
        for(int tshupane=1;tshupane<3;tshupane++)if(보드.Tiro_kemo(tshupane)>0){단말.수(tshupane+1);단말.kwala(" - READY 64 - - kernel-task\n");}
        for(int tshupane=0;tshupane<4;tshupane++){
            int kemo_Boleng=보드.fenenkolola_tsamaiso(20,tshupane);if(kemo_Boleng==0)continue;
            단말.수(보드.fenenkolola_tsamaiso(21,tshupane));단말.문자(' ');단말.수(tshupane);단말.kwala(kemo_Boleng==1?" RUN ":" SUSPENDED ");
            단말.수(보드.fenenkolola_tsamaiso(22,tshupane));단말.문자(' ');단말.수(보드.fenenkolola_tsamaiso(24,tshupane));단말.문자(' ');단말.수(보드.fenenkolola_tsamaiso(23,tshupane));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int baete_Boleng=보드.fenenkolola_tsamaiso(25,tshupane+자리*4);if(baete_Boleng==0)break;보드.직렬쓰기(baete_Boleng);}단말.문자(10);
        }
    }
    static void bontsha_Polokelo() {
        int 칸수=0, 자료수=0;
        for(int tshupane=0;tshupane<memori_Difaele.파일수;tshupane++)if(memori_Difaele.이름길이[tshupane]>0 || memori_Difaele.참조수[tshupane]>0){칸수++;자료수+=memori_Difaele.boleele_Boleng[tshupane];}
        단말.kwala("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(memori_Difaele.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((memori_Difaele.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(memori_Difaele.파일수);단말.kwala(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void bontsha_kemo_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=dijite_Boleng(2,1000))<1){palelo_Boleng("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int TATELANO_Boleng=0;횟수==0 || TATELANO_Boleng<횟수;TATELANO_Boleng++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.kwala("\u001b[2J\u001b[H");
            bontsha_Tiro();bontsha_memori();작업보기();
            if(횟수!=0 && TATELANO_Boleng+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int tshupane) {
        if(tshupane==0)return "ipconfig";if(tshupane==1)return "ip";if(tshupane==2)return "ping";if(tshupane==3)return "route";if(tshupane==4)return "netstat";
        if(tshupane==5)return "ps";if(tshupane==6)return "top";if(tshupane==7)return "free";if(tshupane==8)return "df";if(tshupane==9)return "uptime";if(tshupane==10)return "poweroff";return "help";
    }
    static void bontsha_thuso() {
        단말.kwala("--- Network / system commands ---\n");
        for(int tshupane=0;tshupane<12;tshupane++){단말.kwala(표준말(tshupane));단말.kwala(" / ");단말.kwala(관리명령.Lefoko_SMS(tshupane));단말.kwala(" : ");단말.kwala(관리명령.설명(tshupane));단말.문자(10);}
        단말.kwala("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.kwala("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.kwala("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean diragatsa_Taelo() {
        int Taelo=-1;
        for(int tshupane=0;tshupane<12;tshupane++)if(같음(0,표준말(tshupane)) || 같음(0,관리명령.Lefoko_SMS(tshupane)))Taelo=tshupane;
        if(같음(0,"ifconfig"))Taelo=0;if(같음(0,"ss"))Taelo=4;
        if(Taelo<0)return false;
        if(Taelo==11){if(같음(1,"net") || 같음(1,"system"))bontsha_thuso();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.bontsha_thuso();return true;}
        if(Taelo==0 || Taelo==1)Neteweke_Taelo(Taelo==1);
        else if(Taelo==2)응답시험();
        else if(Taelo==6)bontsha_kemo_bf9821b5();
        else if(개수()!=1){palelo_Boleng("This command takes no arguments; help system");}
        else if(Taelo==3)bontsha_tsela();else if(Taelo==4)bontsha_Neteweke();else if(Taelo==5)작업보기();else if(Taelo==7)bontsha_memori();else if(Taelo==8)bontsha_Polokelo();else if(Taelo==9)bontsha_Tiro();
        else if(Taelo==10)보드.전원끄기();
        return true;
    }
}
