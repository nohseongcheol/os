// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ulwazi_ngokwenzekile_imininingwane ikhenela_inani 상태를 읽는 IPv4·ICMP·작업·inkumbulo_inani·RAM 저장소 관리 Umlayelo. */
public final class isistimu_ithuluzi {
    static int ikheli_inani;
    static boolean 같음(int thola_inkomba, String Amagama_I_SMS) { return 명령해석기.같음(thola_inkomba, Amagama_I_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void ukwehluleka_inani(String NGIFUNDE_eb81d7d9) { 명령해석기.결과=2; 단말.Bhala(NGIFUNDE_eb81d7d9); 단말.문자(10); }
    static void Iphutha(int inani) { 명령해석기.Iphutha(inani); }
    static void 수항목(String Igama, int inani) { 단말.Bhala(Igama); 단말.수(inani); 단말.문자(10); }
    static int idijithi_inani(int thola_inkomba, int 한도) {
        if (thola_inkomba>=개수() || 명령해석기.ubude_inani[thola_inkomba]==0) return -1;
        int inani=0;
        for (int 순번=0; 순번<명령해석기.ubude_inani[thola_inkomba]; 순번++) {
            int uhlamvusimo_inani=명령해석기.ithokhini_inani[명령해석기.시작점[thola_inkomba]+순번]-'0';
            if (uhlamvusimo_inani<0 || uhlamvusimo_inani>9 || inani>(한도-uhlamvusimo_inani)/10) return -1;
            inani=inani*10+uhlamvusimo_inani;
        }
        return inani<=한도?inani:-1;
    }
    static boolean 주소읽기(int thola_inkomba) {
        if (thola_inkomba>=개수()) return false;
        int inani=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.ubude_inani[thola_inkomba]; 순번++) {
            int uhlamvusimo_inani=명령해석기.ithokhini_inani[명령해석기.시작점[thola_inkomba]+순번];
            if (uhlamvusimo_inani=='.') { if (숫자수==0 || ++점수>3) return false; inani=(inani<<8)|덩이; 덩이=숫자수=0; }
            else { if (uhlamvusimo_inani<'0' || uhlamvusimo_inani>'9' || ++숫자수>3) return false; 덩이=덩이*10+uhlamvusimo_inani-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        ikheli_inani=(inani<<8)|덩이; return true;
    }
    static void bhala_ikheli(int inani) {
        단말.수((inani>>>24)&255); 단말.문자('.'); 단말.수((inani>>>16)&255); 단말.문자('.');
        단말.수((inani>>>8)&255); 단말.문자('.'); 단말.수(inani&255);
    }
    static void khombisa_iNethiwekhi_isimo() {
        단말.Bhala(보드.iNethiwekhi_isimo(20,0)!=0?"en0: ":"sl0: "); 단말.Bhala(보드.iNethiwekhi_isimo(3,0)!=0?"UP":"DOWN");
        단말.Bhala(보드.iNethiwekhi_isimo(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Bhala(보드.iNethiwekhi_isimo(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); bhala_ikheli(보드.iNethiwekhi_isimo(0,0));
        단말.Bhala(" netmask "); bhala_ikheli(보드.iNethiwekhi_isimo(1,0)); 단말.Bhala(" gateway "); bhala_ikheli(보드.iNethiwekhi_isimo(2,0)); 단말.문자(10);
        단말.Bhala("  RX packets "); 단말.수(보드.iNethiwekhi_isimo(4,0)); 단말.Bhala(" bytes "); 단말.수(보드.iNethiwekhi_isimo(6,0));
        단말.Bhala(" TX packets "); 단말.수(보드.iNethiwekhi_isimo(5,0)); 단말.Bhala(" bytes "); 단말.수(보드.iNethiwekhi_isimo(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.iNethiwekhi_isimo(8,0));
    }
    static void isethi_ikheli(int Sebenzisa) {
        if (개수()!=Sebenzisa+3 || !주소읽기(Sebenzisa)) { ukwehluleka_inani("사용법: ipconfig set ikheli 주소가림 isango_inani"); return; }
        int ikheli=ikheli_inani;
        if(!주소읽기(Sebenzisa+1)){ukwehluleka_inani("Invalid IPv4 netmask");return;} int insitha_inani=ikheli_inani;
        if(!주소읽기(Sebenzisa+2)){ukwehluleka_inani("Invalid IPv4 gateway");return;}
        int 결과=보드.iNethiwekhi_Amasethingi(0,ikheli,insitha_inani,ikheli_inani);
        if(결과<0) { Iphutha(결과); if(결과==-16)단말.Bhala("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Bhala("IPv4 configuration applied (until reboot)\n"); khombisa_iNethiwekhi_isimo(); }
    }
    static void iNethiwekhi_umyalo(boolean ikheli_le_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { khombisa_iNethiwekhi_isimo();return; }
        if (ikheli_le_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { khombisa_umzila();return; }
        if (같음(1,"set")) { isethi_ikheli(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.iNethiwekhi_Amasethingi(같음(1,"up")?1:2,0,0,0);khombisa_iNethiwekhi_isimo();return; }
        if (ikheli_le_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.iNethiwekhi_Amasethingi(같음(5,"up")?1:2,0,0,0);khombisa_iNethiwekhi_isimo();return; }
        ukwehluleka_inani("사용법: ip [addr show|route show|set ikheli 주소가림 isango_inani|link set dev sl0 up|down]");
    }
    static void khombisa_umzila() {
        단말.Bhala("Destination Netmask Gateway Interface\n");
        bhala_ikheli(보드.iNethiwekhi_isimo(0,0)&보드.iNethiwekhi_isimo(1,0));단말.문자(' ');bhala_ikheli(보드.iNethiwekhi_isimo(1,0));단말.Bhala(보드.iNethiwekhi_isimo(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.iNethiwekhi_isimo(2,0)!=0) {단말.Bhala("0.0.0.0 0.0.0.0 ");bhala_ikheli(보드.iNethiwekhi_isimo(2,0));단말.Bhala(보드.iNethiwekhi_isimo(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void khombisa_iNethiwekhi() {
        단말.Bhala("Proto Local Remote State Queued\n");
        for(int thola_inkomba=0;thola_inkomba<32;thola_inkomba++) {
            int thayipha_umunxa=보드.iNethiwekhi_isimo(10,thola_inkomba);if(thayipha_umunxa==0)continue;
            단말.Bhala(thayipha_umunxa==1?"TCP ":"UDP ");bhala_ikheli(보드.iNethiwekhi_isimo(16,thola_inkomba));단말.문자(':');단말.수(보드.iNethiwekhi_isimo(11,thola_inkomba));단말.문자(' ');
            bhala_ikheli(보드.iNethiwekhi_isimo(12,thola_inkomba));단말.문자(':');단말.수(보드.iNethiwekhi_isimo(13,thola_inkomba));단말.문자(' ');
            int isimo_inani=보드.iNethiwekhi_isimo(14,thola_inkomba);단말.Bhala(thayipha_umunxa==2?"DATAGRAM":isimo_inani==1?"LISTEN":isimo_inani==2?"ESTABLISHED":isimo_inani==3?"CLOSE_WAIT":isimo_inani==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.iNethiwekhi_isimo(15,thola_inkomba));단말.문자(10);
        }
        단말.Bhala("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int Sebenzisa=보드.밀리초();
        while(보드.밀리초()-Sebenzisa<밀리초) {
            if(셸입출력.대화가능()!=0){int uhlamvusimo_inani=보드.직렬읽기();if(uhlamvusimo_inani==3 || uhlamvusimo_inani=='q' || uhlamvusimo_inani=='Q' || uhlamvusimo_inani==27 || uhlamvusimo_inani==-4096)return false;}
            보드.misa_okwesikhashana_i_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, impokophelo=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=idijithi_inani(++자리,100);if(횟수<1){ukwehluleka_inani("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=idijithi_inani(++자리,10);if(제한<1){ukwehluleka_inani("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(impokophelo<0)impokophelo=자리;else{ukwehluleka_inani("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(impokophelo<0 || !주소읽기(impokophelo)){ukwehluleka_inani("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ikheli=ikheli_inani, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Bhala("PING ");bhala_ikheli(ikheli);단말.Bhala(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ukuhleleka_inani=1;ukuhleleka_inani<=횟수 && 계속;ukuhleleka_inani++) {
            int 처리값=보드.응답보내기(ikheli,ukuhleleka_inani);
            if(처리값<0){Iphutha(처리값);break;}보낸수++;
            int Sebenzisa=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-Sebenzisa<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.Bhala("32 bytes from ");bhala_ikheli(ikheli);단말.Bhala(" seq=");단말.수(ukuhleleka_inani);단말.Bhala(" ttl=");단말.수(보드.응답읽기(2));단말.Bhala(" time=");단말.수(시간);단말.Bhala(" ms\n");
            }else{단말.Bhala("Request timeout seq=");단말.수(ukuhleleka_inani);단말.문자(10);}
            if(ukuhleleka_inani<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.Bhala(" transmitted, ");단말.수(받은수);단말.Bhala(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.Bhala("% packet loss\n");
        if(받은수>0){단말.Bhala("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.Bhala(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void khombisa_isenzo() { 단말.Bhala("up ");단말.수(보드.밀리초()/1000);단말.Bhala(" seconds\n"); }
    static void khombisa_inkumbulo() {
        수항목("ARM RAM KiB (firmware): ",보드.umbuzo_isistimu(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.umbuzo_isistimu(1,0));
        int 총량=보드.umbuzo_isistimu(2,0), 사용량=보드.umbuzo_isistimu(3,0);
        단말.Bhala("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.umbuzo_isistimu(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.umbuzo_isistimu(5,0));
        int 매핑=0;for(int thola_inkomba=0;thola_inkomba<4;thola_inkomba++)매핑+=보드.umbuzo_isistimu(22,thola_inkomba);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Bhala("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.Bhala("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Bhala("1 - RUN - - ");단말.수(보드.밀리초());단말.Bhala(" kernel/shell\n");
        for(int thola_inkomba=1;thola_inkomba<3;thola_inkomba++)if(보드.umsebenzi_isimo(thola_inkomba)>0){단말.수(thola_inkomba+1);단말.Bhala(" - READY 64 - - kernel-task\n");}
        for(int thola_inkomba=0;thola_inkomba<4;thola_inkomba++){
            int isimo_inani=보드.umbuzo_isistimu(20,thola_inkomba);if(isimo_inani==0)continue;
            단말.수(보드.umbuzo_isistimu(21,thola_inkomba));단말.문자(' ');단말.수(thola_inkomba);단말.Bhala(isimo_inani==1?" RUN ":" SUSPENDED ");
            단말.수(보드.umbuzo_isistimu(22,thola_inkomba));단말.문자(' ');단말.수(보드.umbuzo_isistimu(24,thola_inkomba));단말.문자(' ');단말.수(보드.umbuzo_isistimu(23,thola_inkomba));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int ibhayithi_inani=보드.umbuzo_isistimu(25,thola_inkomba+자리*4);if(ibhayithi_inani==0)break;보드.직렬쓰기(ibhayithi_inani);}단말.문자(10);
        }
    }
    static void khombisa_Indawo_yokugcina() {
        int 칸수=0, 자료수=0;
        for(int thola_inkomba=0;thola_inkomba<inkumbulo_Amafayela.파일수;thola_inkomba++)if(inkumbulo_Amafayela.이름길이[thola_inkomba]>0 || inkumbulo_Amafayela.참조수[thola_inkomba]>0){칸수++;자료수+=inkumbulo_Amafayela.ubude_inani[thola_inkomba];}
        단말.Bhala("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(inkumbulo_Amafayela.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((inkumbulo_Amafayela.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(inkumbulo_Amafayela.파일수);단말.Bhala(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void khombisa_isimo_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=idijithi_inani(2,1000))<1){ukwehluleka_inani("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int UKULANDELANA_inani=0;횟수==0 || UKULANDELANA_inani<횟수;UKULANDELANA_inani++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Bhala("\u001b[2J\u001b[H");
            khombisa_isenzo();khombisa_inkumbulo();작업보기();
            if(횟수!=0 && UKULANDELANA_inani+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int thola_inkomba) {
        if(thola_inkomba==0)return "ipconfig";if(thola_inkomba==1)return "ip";if(thola_inkomba==2)return "ping";if(thola_inkomba==3)return "route";if(thola_inkomba==4)return "netstat";
        if(thola_inkomba==5)return "ps";if(thola_inkomba==6)return "top";if(thola_inkomba==7)return "free";if(thola_inkomba==8)return "df";if(thola_inkomba==9)return "uptime";if(thola_inkomba==10)return "poweroff";return "help";
    }
    static void khombisa_usizo() {
        단말.Bhala("--- Network / system commands ---\n");
        for(int thola_inkomba=0;thola_inkomba<12;thola_inkomba++){단말.Bhala(표준말(thola_inkomba));단말.Bhala(" / ");단말.Bhala(관리명령.Amagama_I_SMS(thola_inkomba));단말.Bhala(" : ");단말.Bhala(관리명령.설명(thola_inkomba));단말.문자(10);}
        단말.Bhala("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Bhala("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Bhala("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean yenza_umyalo() {
        int Umlayelo=-1;
        for(int thola_inkomba=0;thola_inkomba<12;thola_inkomba++)if(같음(0,표준말(thola_inkomba)) || 같음(0,관리명령.Amagama_I_SMS(thola_inkomba)))Umlayelo=thola_inkomba;
        if(같음(0,"ifconfig"))Umlayelo=0;if(같음(0,"ss"))Umlayelo=4;
        if(Umlayelo<0)return false;
        if(Umlayelo==11){if(같음(1,"net") || 같음(1,"system"))khombisa_usizo();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.khombisa_usizo();return true;}
        if(Umlayelo==0 || Umlayelo==1)iNethiwekhi_umyalo(Umlayelo==1);
        else if(Umlayelo==2)응답시험();
        else if(Umlayelo==6)khombisa_isimo_bf9821b5();
        else if(개수()!=1){ukwehluleka_inani("This command takes no arguments; help system");}
        else if(Umlayelo==3)khombisa_umzila();else if(Umlayelo==4)khombisa_iNethiwekhi();else if(Umlayelo==5)작업보기();else if(Umlayelo==7)khombisa_inkumbulo();else if(Umlayelo==8)khombisa_Indawo_yokugcina();else if(Umlayelo==9)khombisa_isenzo();
        else if(Umlayelo==10)보드.전원끄기();
        return true;
    }
}
