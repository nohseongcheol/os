// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** gangan_détà kánẹ́ẹ̀lì_iye 상태를 읽는 IPv4·ICMP·작업·ibi_ìpamọ́_iye·RAM 저장소 관리 Àṣẹ. */
public final class ètò_irinṣẹ́ {
    static int àdírẹ́ẹ̀sì_iye;
    static boolean 같음(int wá_atọ̀ka_àkóónú, String Ọ̀rọ̀_SMS) { return 명령해석기.같음(wá_atọ̀ka_àkóónú, Ọ̀rọ̀_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void ìkùnà_iye(String KÀ_MÍ_eb81d7d9) { 명령해석기.결과=2; 단말.Kọ(KÀ_MÍ_eb81d7d9); 단말.문자(10); }
    static void àṣìṣe(int iye) { 명령해석기.àṣìṣe(iye); }
    static void 수항목(String Orúkọ, int iye) { 단말.Kọ(Orúkọ); 단말.수(iye); 단말.문자(10); }
    static int díjììtì_iye(int wá_atọ̀ka_àkóónú, int 한도) {
        if (wá_atọ̀ka_àkóónú>=개수() || 명령해석기.gígùn_iye[wá_atọ̀ka_àkóónú]==0) return -1;
        int iye=0;
        for (int 순번=0; 순번<명령해석기.gígùn_iye[wá_atọ̀ka_àkóónú]; 순번++) {
            int ẹyọ_ọ̀rọ̀_iye=명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[명령해석기.시작점[wá_atọ̀ka_àkóónú]+순번]-'0';
            if (ẹyọ_ọ̀rọ̀_iye<0 || ẹyọ_ọ̀rọ̀_iye>9 || iye>(한도-ẹyọ_ọ̀rọ̀_iye)/10) return -1;
            iye=iye*10+ẹyọ_ọ̀rọ̀_iye;
        }
        return iye<=한도?iye:-1;
    }
    static boolean 주소읽기(int wá_atọ̀ka_àkóónú) {
        if (wá_atọ̀ka_àkóónú>=개수()) return false;
        int iye=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.gígùn_iye[wá_atọ̀ka_àkóónú]; 순번++) {
            int ẹyọ_ọ̀rọ̀_iye=명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[명령해석기.시작점[wá_atọ̀ka_àkóónú]+순번];
            if (ẹyọ_ọ̀rọ̀_iye=='.') { if (숫자수==0 || ++점수>3) return false; iye=(iye<<8)|덩이; 덩이=숫자수=0; }
            else { if (ẹyọ_ọ̀rọ̀_iye<'0' || ẹyọ_ọ̀rọ̀_iye>'9' || ++숫자수>3) return false; 덩이=덩이*10+ẹyọ_ọ̀rọ̀_iye-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        àdírẹ́ẹ̀sì_iye=(iye<<8)|덩이; return true;
    }
    static void kọ_àdírẹ́ẹ̀sì(int iye) {
        단말.수((iye>>>24)&255); 단말.문자('.'); 단말.수((iye>>>16)&255); 단말.문자('.');
        단말.수((iye>>>8)&255); 단말.문자('.'); 단말.수(iye&255);
    }
    static void ṣàfihàn_Alásopọ̀_ipò() {
        단말.Kọ(보드.Alásopọ̀_ipò(20,0)!=0?"en0: ":"sl0: "); 단말.Kọ(보드.Alásopọ̀_ipò(3,0)!=0?"UP":"DOWN");
        단말.Kọ(보드.Alásopọ̀_ipò(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Kọ(보드.Alásopọ̀_ipò(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); kọ_àdírẹ́ẹ̀sì(보드.Alásopọ̀_ipò(0,0));
        단말.Kọ(" netmask "); kọ_àdírẹ́ẹ̀sì(보드.Alásopọ̀_ipò(1,0)); 단말.Kọ(" gateway "); kọ_àdírẹ́ẹ̀sì(보드.Alásopọ̀_ipò(2,0)); 단말.문자(10);
        단말.Kọ("  RX packets "); 단말.수(보드.Alásopọ̀_ipò(4,0)); 단말.Kọ(" bytes "); 단말.수(보드.Alásopọ̀_ipò(6,0));
        단말.Kọ(" TX packets "); 단말.수(보드.Alásopọ̀_ipò(5,0)); 단말.Kọ(" bytes "); 단말.수(보드.Alásopọ̀_ipò(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Alásopọ̀_ipò(8,0));
    }
    static void ọ̀wọ̀_àdírẹ́ẹ̀sì(int Rọ́ọ̀nù) {
        if (개수()!=Rọ́ọ̀nù+3 || !주소읽기(Rọ́ọ̀nù)) { ìkùnà_iye("사용법: ipconfig set àdírẹ́ẹ̀sì 주소가림 ẹnu_odi_iye"); return; }
        int àdírẹ́ẹ̀sì=àdírẹ́ẹ̀sì_iye;
        if(!주소읽기(Rọ́ọ̀nù+1)){ìkùnà_iye("Invalid IPv4 netmask");return;} int asẹ́_iye_iye=àdírẹ́ẹ̀sì_iye;
        if(!주소읽기(Rọ́ọ̀nù+2)){ìkùnà_iye("Invalid IPv4 gateway");return;}
        int 결과=보드.Alásopọ̀_Àwọn_ààtò(0,àdírẹ́ẹ̀sì,asẹ́_iye_iye,àdírẹ́ẹ̀sì_iye);
        if(결과<0) { àṣìṣe(결과); if(결과==-16)단말.Kọ("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Kọ("IPv4 configuration applied (until reboot)\n"); ṣàfihàn_Alásopọ̀_ipò(); }
    }
    static void Alásopọ̀_àṣẹ(boolean àdírẹ́ẹ̀sì_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { ṣàfihàn_Alásopọ̀_ipò();return; }
        if (àdírẹ́ẹ̀sì_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { ṣàfihàn_ọ̀nà();return; }
        if (같음(1,"set")) { ọ̀wọ̀_àdírẹ́ẹ̀sì(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.Alásopọ̀_Àwọn_ààtò(같음(1,"up")?1:2,0,0,0);ṣàfihàn_Alásopọ̀_ipò();return; }
        if (àdírẹ́ẹ̀sì_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.Alásopọ̀_Àwọn_ààtò(같음(5,"up")?1:2,0,0,0);ṣàfihàn_Alásopọ̀_ipò();return; }
        ìkùnà_iye("사용법: ip [addr show|route show|set àdírẹ́ẹ̀sì 주소가림 ẹnu_odi_iye|link set dev sl0 up|down]");
    }
    static void ṣàfihàn_ọ̀nà() {
        단말.Kọ("Destination Netmask Gateway Interface\n");
        kọ_àdírẹ́ẹ̀sì(보드.Alásopọ̀_ipò(0,0)&보드.Alásopọ̀_ipò(1,0));단말.문자(' ');kọ_àdírẹ́ẹ̀sì(보드.Alásopọ̀_ipò(1,0));단말.Kọ(보드.Alásopọ̀_ipò(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Alásopọ̀_ipò(2,0)!=0) {단말.Kọ("0.0.0.0 0.0.0.0 ");kọ_àdírẹ́ẹ̀sì(보드.Alásopọ̀_ipò(2,0));단말.Kọ(보드.Alásopọ̀_ipò(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void ṣàfihàn_Alásopọ̀() {
        단말.Kọ("Proto Local Remote State Queued\n");
        for(int wá_atọ̀ka_àkóónú=0;wá_atọ̀ka_àkóónú<32;wá_atọ̀ka_àkóónú++) {
            int irú_ìsọ̀rí=보드.Alásopọ̀_ipò(10,wá_atọ̀ka_àkóónú);if(irú_ìsọ̀rí==0)continue;
            단말.Kọ(irú_ìsọ̀rí==1?"TCP ":"UDP ");kọ_àdírẹ́ẹ̀sì(보드.Alásopọ̀_ipò(16,wá_atọ̀ka_àkóónú));단말.문자(':');단말.수(보드.Alásopọ̀_ipò(11,wá_atọ̀ka_àkóónú));단말.문자(' ');
            kọ_àdírẹ́ẹ̀sì(보드.Alásopọ̀_ipò(12,wá_atọ̀ka_àkóónú));단말.문자(':');단말.수(보드.Alásopọ̀_ipò(13,wá_atọ̀ka_àkóónú));단말.문자(' ');
            int ipò_iye=보드.Alásopọ̀_ipò(14,wá_atọ̀ka_àkóónú);단말.Kọ(irú_ìsọ̀rí==2?"DATAGRAM":ipò_iye==1?"LISTEN":ipò_iye==2?"ESTABLISHED":ipò_iye==3?"CLOSE_WAIT":ipò_iye==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Alásopọ̀_ipò(15,wá_atọ̀ka_àkóónú));단말.문자(10);
        }
        단말.Kọ("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int Rọ́ọ̀nù=보드.밀리초();
        while(보드.밀리초()-Rọ́ọ̀nù<밀리초) {
            if(셸입출력.대화가능()!=0){int ẹyọ_ọ̀rọ̀_iye=보드.직렬읽기();if(ẹyọ_ọ̀rọ̀_iye==3 || ẹyọ_ọ̀rọ̀_iye=='q' || ẹyọ_ọ̀rọ̀_iye=='Q' || ẹyọ_ọ̀rọ̀_iye==27 || ẹyọ_ọ̀rọ̀_iye==-4096)return false;}
            보드.ti_dádúró_díẹ̀_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, àfojúsùn=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=díjììtì_iye(++자리,100);if(횟수<1){ìkùnà_iye("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=díjììtì_iye(++자리,10);if(제한<1){ìkùnà_iye("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(àfojúsùn<0)àfojúsùn=자리;else{ìkùnà_iye("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(àfojúsùn<0 || !주소읽기(àfojúsùn)){ìkùnà_iye("ping: an IPv4 address is required (DNS is not configured)");return;}
        int àdírẹ́ẹ̀sì=àdírẹ́ẹ̀sì_iye, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Kọ("PING ");kọ_àdírẹ́ẹ̀sì(àdírẹ́ẹ̀sì);단말.Kọ(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ìtodátà_iye=1;ìtodátà_iye<=횟수 && 계속;ìtodátà_iye++) {
            int 처리값=보드.응답보내기(àdírẹ́ẹ̀sì,ìtodátà_iye);
            if(처리값<0){àṣìṣe(처리값);break;}보낸수++;
            int Rọ́ọ̀nù=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-Rọ́ọ̀nù<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.Kọ("32 bytes from ");kọ_àdírẹ́ẹ̀sì(àdírẹ́ẹ̀sì);단말.Kọ(" seq=");단말.수(ìtodátà_iye);단말.Kọ(" ttl=");단말.수(보드.응답읽기(2));단말.Kọ(" time=");단말.수(시간);단말.Kọ(" ms\n");
            }else{단말.Kọ("Request timeout seq=");단말.수(ìtodátà_iye);단말.문자(10);}
            if(ìtodátà_iye<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.Kọ(" transmitted, ");단말.수(받은수);단말.Kọ(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.Kọ("% packet loss\n");
        if(받은수>0){단말.Kọ("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.Kọ(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void ṣàfihàn_Iṣẹ́_ṣiṣe() { 단말.Kọ("up ");단말.수(보드.밀리초()/1000);단말.Kọ(" seconds\n"); }
    static void ṣàfihàn_ibi_ìpamọ́() {
        수항목("ARM RAM KiB (firmware): ",보드.aṣèbéèré_ètò(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.aṣèbéèré_ètò(1,0));
        int 총량=보드.aṣèbéèré_ètò(2,0), 사용량=보드.aṣèbéèré_ètò(3,0);
        단말.Kọ("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.aṣèbéèré_ètò(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.aṣèbéèré_ètò(5,0));
        int 매핑=0;for(int wá_atọ̀ka_àkóónú=0;wá_atọ̀ka_àkóónú<4;wá_atọ̀ka_àkóónú++)매핑+=보드.aṣèbéèré_ètò(22,wá_atọ̀ka_àkóónú);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Kọ("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.Kọ("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Kọ("1 - RUN - - ");단말.수(보드.밀리초());단말.Kọ(" kernel/shell\n");
        for(int wá_atọ̀ka_àkóónú=1;wá_atọ̀ka_àkóónú<3;wá_atọ̀ka_àkóónú++)if(보드.iṣẹ́_ipò(wá_atọ̀ka_àkóónú)>0){단말.수(wá_atọ̀ka_àkóónú+1);단말.Kọ(" - READY 64 - - kernel-task\n");}
        for(int wá_atọ̀ka_àkóónú=0;wá_atọ̀ka_àkóónú<4;wá_atọ̀ka_àkóónú++){
            int ipò_iye=보드.aṣèbéèré_ètò(20,wá_atọ̀ka_àkóónú);if(ipò_iye==0)continue;
            단말.수(보드.aṣèbéèré_ètò(21,wá_atọ̀ka_àkóónú));단말.문자(' ');단말.수(wá_atọ̀ka_àkóónú);단말.Kọ(ipò_iye==1?" RUN ":" SUSPENDED ");
            단말.수(보드.aṣèbéèré_ètò(22,wá_atọ̀ka_àkóónú));단말.문자(' ');단말.수(보드.aṣèbéèré_ètò(24,wá_atọ̀ka_àkóónú));단말.문자(' ');단말.수(보드.aṣèbéèré_ètò(23,wá_atọ̀ka_àkóónú));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int báìtì_iye=보드.aṣèbéèré_ètò(25,wá_atọ̀ka_àkóónú+자리*4);if(báìtì_iye==0)break;보드.직렬쓰기(báìtì_iye);}단말.문자(10);
        }
    }
    static void ṣàfihàn_Ibi_ìpamọ́() {
        int 칸수=0, 자료수=0;
        for(int wá_atọ̀ka_àkóónú=0;wá_atọ̀ka_àkóónú<ibi_ìpamọ́_Àwọn_fáìlì.파일수;wá_atọ̀ka_àkóónú++)if(ibi_ìpamọ́_Àwọn_fáìlì.이름길이[wá_atọ̀ka_àkóónú]>0 || ibi_ìpamọ́_Àwọn_fáìlì.참조수[wá_atọ̀ka_àkóónú]>0){칸수++;자료수+=ibi_ìpamọ́_Àwọn_fáìlì.gígùn_iye[wá_atọ̀ka_àkóónú];}
        단말.Kọ("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(ibi_ìpamọ́_Àwọn_fáìlì.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((ibi_ìpamọ́_Àwọn_fáìlì.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(ibi_ìpamọ́_Àwọn_fáìlì.파일수);단말.Kọ(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void ṣàfihàn_ipò_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=díjììtì_iye(2,1000))<1){ìkùnà_iye("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int ÀTẸ̀LÉRA_iye=0;횟수==0 || ÀTẸ̀LÉRA_iye<횟수;ÀTẸ̀LÉRA_iye++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Kọ("\u001b[2J\u001b[H");
            ṣàfihàn_Iṣẹ́_ṣiṣe();ṣàfihàn_ibi_ìpamọ́();작업보기();
            if(횟수!=0 && ÀTẸ̀LÉRA_iye+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int wá_atọ̀ka_àkóónú) {
        if(wá_atọ̀ka_àkóónú==0)return "ipconfig";if(wá_atọ̀ka_àkóónú==1)return "ip";if(wá_atọ̀ka_àkóónú==2)return "ping";if(wá_atọ̀ka_àkóónú==3)return "route";if(wá_atọ̀ka_àkóónú==4)return "netstat";
        if(wá_atọ̀ka_àkóónú==5)return "ps";if(wá_atọ̀ka_àkóónú==6)return "top";if(wá_atọ̀ka_àkóónú==7)return "free";if(wá_atọ̀ka_àkóónú==8)return "df";if(wá_atọ̀ka_àkóónú==9)return "uptime";if(wá_atọ̀ka_àkóónú==10)return "poweroff";return "help";
    }
    static void ṣàfihàn_ìrànwọ́() {
        단말.Kọ("--- Network / system commands ---\n");
        for(int wá_atọ̀ka_àkóónú=0;wá_atọ̀ka_àkóónú<12;wá_atọ̀ka_àkóónú++){단말.Kọ(표준말(wá_atọ̀ka_àkóónú));단말.Kọ(" / ");단말.Kọ(관리명령.Ọ̀rọ̀_SMS(wá_atọ̀ka_àkóónú));단말.Kọ(" : ");단말.Kọ(관리명령.설명(wá_atọ̀ka_àkóónú));단말.문자(10);}
        단말.Kọ("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Kọ("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Kọ("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean ṣiṣẹ́_àṣẹ() {
        int Àṣẹ=-1;
        for(int wá_atọ̀ka_àkóónú=0;wá_atọ̀ka_àkóónú<12;wá_atọ̀ka_àkóónú++)if(같음(0,표준말(wá_atọ̀ka_àkóónú)) || 같음(0,관리명령.Ọ̀rọ̀_SMS(wá_atọ̀ka_àkóónú)))Àṣẹ=wá_atọ̀ka_àkóónú;
        if(같음(0,"ifconfig"))Àṣẹ=0;if(같음(0,"ss"))Àṣẹ=4;
        if(Àṣẹ<0)return false;
        if(Àṣẹ==11){if(같음(1,"net") || 같음(1,"system"))ṣàfihàn_ìrànwọ́();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.ṣàfihàn_ìrànwọ́();return true;}
        if(Àṣẹ==0 || Àṣẹ==1)Alásopọ̀_àṣẹ(Àṣẹ==1);
        else if(Àṣẹ==2)응답시험();
        else if(Àṣẹ==6)ṣàfihàn_ipò_bf9821b5();
        else if(개수()!=1){ìkùnà_iye("This command takes no arguments; help system");}
        else if(Àṣẹ==3)ṣàfihàn_ọ̀nà();else if(Àṣẹ==4)ṣàfihàn_Alásopọ̀();else if(Àṣẹ==5)작업보기();else if(Àṣẹ==7)ṣàfihàn_ibi_ìpamọ́();else if(Àṣẹ==8)ṣàfihàn_Ibi_ìpamọ́();else if(Àṣẹ==9)ṣàfihàn_Iṣẹ́_ṣiṣe();
        else if(Àṣẹ==10)보드.전원끄기();
        return true;
    }
}
