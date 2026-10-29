// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** taannallarik_titiqqat kernel_atuutilik 상태를 읽는 IPv4·ICMP·작업·puigujjaikkut_atuutilik·RAM 저장소 관리 piqujijjut. */
public final class qarasaujaq_sanajjut {
    static int turaarut_atuutilik;
    static boolean 같음(int nalunaiqsimavik, String 말) { return 명령해석기.같음(nalunaiqsimavik, 말); }
    static int 개수() { return 명령해석기.토큰수; }
    static void itigaqtuq_atuutilik(String README_eb81d7d9) { 명령해석기.결과=2; 단말.titiraq(README_eb81d7d9); 단말.문자(10); }
    static void tammarniq(int atuutilik) { 명령해석기.tammarniq(atuutilik); }
    static void 수항목(String atiq, int atuutilik) { 단말.titiraq(atiq); 단말.수(atuutilik); 단말.문자(10); }
    static int 숫자(int nalunaiqsimavik, int 한도) {
        if (nalunaiqsimavik>=개수() || 명령해석기.takininga_atuutilik[nalunaiqsimavik]==0) return -1;
        int atuutilik=0;
        for (int 순번=0; 순번<명령해석기.takininga_atuutilik[nalunaiqsimavik]; 순번++) {
            int immikkuuqtuq_atuutilik=명령해석기.토큰[명령해석기.시작점[nalunaiqsimavik]+순번]-'0';
            if (immikkuuqtuq_atuutilik<0 || immikkuuqtuq_atuutilik>9 || atuutilik>(한도-immikkuuqtuq_atuutilik)/10) return -1;
            atuutilik=atuutilik*10+immikkuuqtuq_atuutilik;
        }
        return atuutilik<=한도?atuutilik:-1;
    }
    static boolean 주소읽기(int nalunaiqsimavik) {
        if (nalunaiqsimavik>=개수()) return false;
        int atuutilik=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.takininga_atuutilik[nalunaiqsimavik]; 순번++) {
            int immikkuuqtuq_atuutilik=명령해석기.토큰[명령해석기.시작점[nalunaiqsimavik]+순번];
            if (immikkuuqtuq_atuutilik=='.') { if (숫자수==0 || ++점수>3) return false; atuutilik=(atuutilik<<8)|덩이; 덩이=숫자수=0; }
            else { if (immikkuuqtuq_atuutilik<'0' || immikkuuqtuq_atuutilik>'9' || ++숫자수>3) return false; 덩이=덩이*10+immikkuuqtuq_atuutilik-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        turaarut_atuutilik=(atuutilik<<8)|덩이; return true;
    }
    static void titiraq_turaarut(int atuutilik) {
        단말.수((atuutilik>>>24)&255); 단말.문자('.'); 단말.수((atuutilik>>>16)&255); 단말.문자('.');
        단말.수((atuutilik>>>8)&255); 단말.문자('.'); 단말.수(atuutilik&255);
    }
    static void saqqilli_Kasuqatigiitsimajut_qanuilinganiq() {
        단말.titiraq(보드.Kasuqatigiitsimajut_qanuilinganiq(20,0)!=0?"en0: ":"sl0: "); 단말.titiraq(보드.Kasuqatigiitsimajut_qanuilinganiq(3,0)!=0?"UP":"DOWN");
        단말.titiraq(보드.Kasuqatigiitsimajut_qanuilinganiq(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.titiraq(보드.Kasuqatigiitsimajut_qanuilinganiq(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); titiraq_turaarut(보드.Kasuqatigiitsimajut_qanuilinganiq(0,0));
        단말.titiraq(" netmask "); titiraq_turaarut(보드.Kasuqatigiitsimajut_qanuilinganiq(1,0)); 단말.titiraq(" gateway "); titiraq_turaarut(보드.Kasuqatigiitsimajut_qanuilinganiq(2,0)); 단말.문자(10);
        단말.titiraq("  RX packets "); 단말.수(보드.Kasuqatigiitsimajut_qanuilinganiq(4,0)); 단말.titiraq(" bytes "); 단말.수(보드.Kasuqatigiitsimajut_qanuilinganiq(6,0));
        단말.titiraq(" TX packets "); 단말.수(보드.Kasuqatigiitsimajut_qanuilinganiq(5,0)); 단말.titiraq(" bytes "); 단말.수(보드.Kasuqatigiitsimajut_qanuilinganiq(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Kasuqatigiitsimajut_qanuilinganiq(8,0));
    }
    static void attiqsimaniit_turaarut(int 시작) {
        if (개수()!=시작+3 || !주소읽기(시작)) { itigaqtuq_atuutilik("사용법: ipconfig set turaarut 주소가림 aqqusiurut_atuutilik"); return; }
        int turaarut=turaarut_atuutilik;
        if(!주소읽기(시작+1)){itigaqtuq_atuutilik("Invalid IPv4 netmask");return;} int kiinappak_atuutilik=turaarut_atuutilik;
        if(!주소읽기(시작+2)){itigaqtuq_atuutilik("Invalid IPv4 gateway");return;}
        int 결과=보드.망설정(0,turaarut,kiinappak_atuutilik,turaarut_atuutilik);
        if(결과<0) { tammarniq(결과); if(결과==-16)단말.titiraq("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.titiraq("IPv4 configuration applied (until reboot)\n"); saqqilli_Kasuqatigiitsimajut_qanuilinganiq(); }
    }
    static void Kasuqatigiitsimajut_piqujijjut(boolean IP_Turaarut) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { saqqilli_Kasuqatigiitsimajut_qanuilinganiq();return; }
        if (IP_Turaarut && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { saqqilli_aqqut();return; }
        if (같음(1,"set")) { attiqsimaniit_turaarut(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.망설정(같음(1,"up")?1:2,0,0,0);saqqilli_Kasuqatigiitsimajut_qanuilinganiq();return; }
        if (IP_Turaarut && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.망설정(같음(5,"up")?1:2,0,0,0);saqqilli_Kasuqatigiitsimajut_qanuilinganiq();return; }
        itigaqtuq_atuutilik("사용법: ip [addr show|route show|set turaarut 주소가림 aqqusiurut_atuutilik|link set dev sl0 up|down]");
    }
    static void saqqilli_aqqut() {
        단말.titiraq("Destination Netmask Gateway Interface\n");
        titiraq_turaarut(보드.Kasuqatigiitsimajut_qanuilinganiq(0,0)&보드.Kasuqatigiitsimajut_qanuilinganiq(1,0));단말.문자(' ');titiraq_turaarut(보드.Kasuqatigiitsimajut_qanuilinganiq(1,0));단말.titiraq(보드.Kasuqatigiitsimajut_qanuilinganiq(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Kasuqatigiitsimajut_qanuilinganiq(2,0)!=0) {단말.titiraq("0.0.0.0 0.0.0.0 ");titiraq_turaarut(보드.Kasuqatigiitsimajut_qanuilinganiq(2,0));단말.titiraq(보드.Kasuqatigiitsimajut_qanuilinganiq(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void saqqilli_Kasuqatigiitsimajut() {
        단말.titiraq("Proto Local Remote State Queued\n");
        for(int nalunaiqsimavik=0;nalunaiqsimavik<32;nalunaiqsimavik++) {
            int qanuittuuninga_Ataqatigiivvik=보드.Kasuqatigiitsimajut_qanuilinganiq(10,nalunaiqsimavik);if(qanuittuuninga_Ataqatigiivvik==0)continue;
            단말.titiraq(qanuittuuninga_Ataqatigiivvik==1?"TCP ":"UDP ");titiraq_turaarut(보드.Kasuqatigiitsimajut_qanuilinganiq(16,nalunaiqsimavik));단말.문자(':');단말.수(보드.Kasuqatigiitsimajut_qanuilinganiq(11,nalunaiqsimavik));단말.문자(' ');
            titiraq_turaarut(보드.Kasuqatigiitsimajut_qanuilinganiq(12,nalunaiqsimavik));단말.문자(':');단말.수(보드.Kasuqatigiitsimajut_qanuilinganiq(13,nalunaiqsimavik));단말.문자(' ');
            int qanuilinganiq_atuutilik=보드.Kasuqatigiitsimajut_qanuilinganiq(14,nalunaiqsimavik);단말.titiraq(qanuittuuninga_Ataqatigiivvik==2?"DATAGRAM":qanuilinganiq_atuutilik==1?"LISTEN":qanuilinganiq_atuutilik==2?"ESTABLISHED":qanuilinganiq_atuutilik==3?"CLOSE_WAIT":qanuilinganiq_atuutilik==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Kasuqatigiitsimajut_qanuilinganiq(15,nalunaiqsimavik));단말.문자(10);
        }
        단말.titiraq("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int 시작=보드.밀리초();
        while(보드.밀리초()-시작<밀리초) {
            if(셸입출력.대화가능()!=0){int immikkuuqtuq_atuutilik=보드.직렬읽기();if(immikkuuqtuq_atuutilik==3 || immikkuuqtuq_atuutilik=='q' || immikkuuqtuq_atuutilik=='Q' || immikkuuqtuq_atuutilik==27 || immikkuuqtuq_atuutilik==-4096)return false;}
            보드.양보();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, turaagaq=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=숫자(++자리,100);if(횟수<1){itigaqtuq_atuutilik("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=숫자(++자리,10);if(제한<1){itigaqtuq_atuutilik("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(turaagaq<0)turaagaq=자리;else{itigaqtuq_atuutilik("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(turaagaq<0 || !주소읽기(turaagaq)){itigaqtuq_atuutilik("ping: an IPv4 address is required (DNS is not configured)");return;}
        int turaarut=turaarut_atuutilik, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.titiraq("PING ");titiraq_turaarut(turaarut);단말.titiraq(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int agguijjut_atuutilik=1;agguijjut_atuutilik<=횟수 && 계속;agguijjut_atuutilik++) {
            int 처리값=보드.응답보내기(turaarut,agguijjut_atuutilik);
            if(처리값<0){tammarniq(처리값);break;}보낸수++;
            int 시작=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-시작<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.titiraq("32 bytes from ");titiraq_turaarut(turaarut);단말.titiraq(" seq=");단말.수(agguijjut_atuutilik);단말.titiraq(" ttl=");단말.수(보드.응답읽기(2));단말.titiraq(" time=");단말.수(시간);단말.titiraq(" ms\n");
            }else{단말.titiraq("Request timeout seq=");단말.수(agguijjut_atuutilik);단말.문자(10);}
            if(agguijjut_atuutilik<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.titiraq(" transmitted, ");단말.수(받은수);단말.titiraq(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.titiraq("% packet loss\n");
        if(받은수>0){단말.titiraq("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.titiraq(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void saqqilli_suniq() { 단말.titiraq("up ");단말.수(보드.밀리초()/1000);단말.titiraq(" seconds\n"); }
    static void saqqilli_puigujjaikkut() {
        수항목("ARM RAM KiB (firmware): ",보드.kiggusiqarialik_qarasaujaq(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.kiggusiqarialik_qarasaujaq(1,0));
        int 총량=보드.kiggusiqarialik_qarasaujaq(2,0), 사용량=보드.kiggusiqarialik_qarasaujaq(3,0);
        단말.titiraq("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.kiggusiqarialik_qarasaujaq(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.kiggusiqarialik_qarasaujaq(5,0));
        int 매핑=0;for(int nalunaiqsimavik=0;nalunaiqsimavik<4;nalunaiqsimavik++)매핑+=보드.kiggusiqarialik_qarasaujaq(22,nalunaiqsimavik);
        수항목("EL0 mapped KiB: ",매핑);
        단말.titiraq("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.titiraq("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.titiraq("1 - RUN - - ");단말.수(보드.밀리초());단말.titiraq(" kernel/shell\n");
        for(int nalunaiqsimavik=1;nalunaiqsimavik<3;nalunaiqsimavik++)if(보드.sujassaq_qanuilinganiq(nalunaiqsimavik)>0){단말.수(nalunaiqsimavik+1);단말.titiraq(" - READY 64 - - kernel-task\n");}
        for(int nalunaiqsimavik=0;nalunaiqsimavik<4;nalunaiqsimavik++){
            int qanuilinganiq_atuutilik=보드.kiggusiqarialik_qarasaujaq(20,nalunaiqsimavik);if(qanuilinganiq_atuutilik==0)continue;
            단말.수(보드.kiggusiqarialik_qarasaujaq(21,nalunaiqsimavik));단말.문자(' ');단말.수(nalunaiqsimavik);단말.titiraq(qanuilinganiq_atuutilik==1?" RUN ":" SUSPENDED ");
            단말.수(보드.kiggusiqarialik_qarasaujaq(22,nalunaiqsimavik));단말.문자(' ');단말.수(보드.kiggusiqarialik_qarasaujaq(24,nalunaiqsimavik));단말.문자(' ');단말.수(보드.kiggusiqarialik_qarasaujaq(23,nalunaiqsimavik));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int byte_atuutilik=보드.kiggusiqarialik_qarasaujaq(25,nalunaiqsimavik+자리*4);if(byte_atuutilik==0)break;보드.직렬쓰기(byte_atuutilik);}단말.문자(10);
        }
    }
    static void 저장보기() {
        int 칸수=0, 자료수=0;
        for(int nalunaiqsimavik=0;nalunaiqsimavik<기억파일.파일수;nalunaiqsimavik++)if(기억파일.이름길이[nalunaiqsimavik]>0 || 기억파일.참조수[nalunaiqsimavik]>0){칸수++;자료수+=기억파일.takininga_atuutilik[nalunaiqsimavik];}
        단말.titiraq("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(기억파일.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((기억파일.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(기억파일.파일수);단말.titiraq(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void saqqilli_qanuilinganiq_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=숫자(2,1000))<1){itigaqtuq_atuutilik("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int 차례=0;횟수==0 || 차례<횟수;차례++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.titiraq("\u001b[2J\u001b[H");
            saqqilli_suniq();saqqilli_puigujjaikkut();작업보기();
            if(횟수!=0 && 차례+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int nalunaiqsimavik) {
        if(nalunaiqsimavik==0)return "ipconfig";if(nalunaiqsimavik==1)return "ip";if(nalunaiqsimavik==2)return "ping";if(nalunaiqsimavik==3)return "route";if(nalunaiqsimavik==4)return "netstat";
        if(nalunaiqsimavik==5)return "ps";if(nalunaiqsimavik==6)return "top";if(nalunaiqsimavik==7)return "free";if(nalunaiqsimavik==8)return "df";if(nalunaiqsimavik==9)return "uptime";if(nalunaiqsimavik==10)return "poweroff";return "help";
    }
    static void saqqilli_Ikajuqtau() {
        단말.titiraq("--- Network / system commands ---\n");
        for(int nalunaiqsimavik=0;nalunaiqsimavik<12;nalunaiqsimavik++){단말.titiraq(표준말(nalunaiqsimavik));단말.titiraq(" / ");단말.titiraq(관리명령.말(nalunaiqsimavik));단말.titiraq(" : ");단말.titiraq(관리명령.설명(nalunaiqsimavik));단말.문자(10);}
        단말.titiraq("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.titiraq("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.titiraq("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean 실행() {
        int piqujijjut=-1;
        for(int nalunaiqsimavik=0;nalunaiqsimavik<12;nalunaiqsimavik++)if(같음(0,표준말(nalunaiqsimavik)) || 같음(0,관리명령.말(nalunaiqsimavik)))piqujijjut=nalunaiqsimavik;
        if(같음(0,"ifconfig"))piqujijjut=0;if(같음(0,"ss"))piqujijjut=4;
        if(piqujijjut<0)return false;
        if(piqujijjut==11){if(같음(1,"net") || 같음(1,"system"))saqqilli_Ikajuqtau();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.saqqilli_Ikajuqtau();return true;}
        if(piqujijjut==0 || piqujijjut==1)Kasuqatigiitsimajut_piqujijjut(piqujijjut==1);
        else if(piqujijjut==2)응답시험();
        else if(piqujijjut==6)saqqilli_qanuilinganiq_bf9821b5();
        else if(개수()!=1){itigaqtuq_atuutilik("This command takes no arguments; help system");}
        else if(piqujijjut==3)saqqilli_aqqut();else if(piqujijjut==4)saqqilli_Kasuqatigiitsimajut();else if(piqujijjut==5)작업보기();else if(piqujijjut==7)saqqilli_puigujjaikkut();else if(piqujijjut==8)저장보기();else if(piqujijjut==9)saqqilli_suniq();
        else if(piqujijjut==10)보드.전원끄기();
        return true;
    }
}
