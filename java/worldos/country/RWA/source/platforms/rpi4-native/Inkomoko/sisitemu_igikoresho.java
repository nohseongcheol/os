// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** nyakuri_amakurushingiro intima_agaciro 상태를 읽는 IPv4·ICMP·작업·ububiko_agaciro·RAM 저장소 관리 Icyo_wifuza. */
public final class sisitemu_igikoresho {
    static int aderesi_agaciro;
    static boolean 같음(int umugerekashakiro, String Ijambo_SMS) { return 명령해석기.같음(umugerekashakiro, Ijambo_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void kudakora_agaciro(String NSOMA_eb81d7d9) { 명령해석기.결과=2; 단말.kwandika(NSOMA_eb81d7d9); 단말.문자(10); }
    static void IKOSA(int agaciro) { 명령해석기.IKOSA(agaciro); }
    static void 수항목(String Izina, int agaciro) { 단말.kwandika(Izina); 단말.수(agaciro); 단말.문자(10); }
    static int umubare_agaciro(int umugerekashakiro, int 한도) {
        if (umugerekashakiro>=개수() || 명령해석기.uburebure_agaciro[umugerekashakiro]==0) return -1;
        int agaciro=0;
        for (int 순번=0; 순번<명령해석기.uburebure_agaciro[umugerekashakiro]; 순번++) {
            int inyuguti_agaciro=명령해석기.tike_agaciro[명령해석기.시작점[umugerekashakiro]+순번]-'0';
            if (inyuguti_agaciro<0 || inyuguti_agaciro>9 || agaciro>(한도-inyuguti_agaciro)/10) return -1;
            agaciro=agaciro*10+inyuguti_agaciro;
        }
        return agaciro<=한도?agaciro:-1;
    }
    static boolean 주소읽기(int umugerekashakiro) {
        if (umugerekashakiro>=개수()) return false;
        int agaciro=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.uburebure_agaciro[umugerekashakiro]; 순번++) {
            int inyuguti_agaciro=명령해석기.tike_agaciro[명령해석기.시작점[umugerekashakiro]+순번];
            if (inyuguti_agaciro=='.') { if (숫자수==0 || ++점수>3) return false; agaciro=(agaciro<<8)|덩이; 덩이=숫자수=0; }
            else { if (inyuguti_agaciro<'0' || inyuguti_agaciro>'9' || ++숫자수>3) return false; 덩이=덩이*10+inyuguti_agaciro-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        aderesi_agaciro=(agaciro<<8)|덩이; return true;
    }
    static void kwandika_aderesi(int agaciro) {
        단말.수((agaciro>>>24)&255); 단말.문자('.'); 단말.수((agaciro>>>16)&255); 단말.문자('.');
        단말.수((agaciro>>>8)&255); 단말.문자('.'); 단말.수(agaciro&255);
    }
    static void kugaragaza_Urusobemiyoboro_imimerere() {
        단말.kwandika(보드.Urusobemiyoboro_imimerere(20,0)!=0?"en0: ":"sl0: "); 단말.kwandika(보드.Urusobemiyoboro_imimerere(3,0)!=0?"UP":"DOWN");
        단말.kwandika(보드.Urusobemiyoboro_imimerere(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.kwandika(보드.Urusobemiyoboro_imimerere(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); kwandika_aderesi(보드.Urusobemiyoboro_imimerere(0,0));
        단말.kwandika(" netmask "); kwandika_aderesi(보드.Urusobemiyoboro_imimerere(1,0)); 단말.kwandika(" gateway "); kwandika_aderesi(보드.Urusobemiyoboro_imimerere(2,0)); 단말.문자(10);
        단말.kwandika("  RX packets "); 단말.수(보드.Urusobemiyoboro_imimerere(4,0)); 단말.kwandika(" bytes "); 단말.수(보드.Urusobemiyoboro_imimerere(6,0));
        단말.kwandika(" TX packets "); 단말.수(보드.Urusobemiyoboro_imimerere(5,0)); 단말.kwandika(" bytes "); 단말.수(보드.Urusobemiyoboro_imimerere(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Urusobemiyoboro_imimerere(8,0));
    }
    static void itsinda_aderesi(int ihuriro) {
        if (개수()!=ihuriro+3 || !주소읽기(ihuriro)) { kudakora_agaciro("사용법: ipconfig set aderesi 주소가림 muhuzaporotokore_agaciro"); return; }
        int aderesi=aderesi_agaciro;
        if(!주소읽기(ihuriro+1)){kudakora_agaciro("Invalid IPv4 netmask");return;} int masiki_agaciro=aderesi_agaciro;
        if(!주소읽기(ihuriro+2)){kudakora_agaciro("Invalid IPv4 gateway");return;}
        int 결과=보드.Urusobemiyoboro_Amagenamiterere(0,aderesi,masiki_agaciro,aderesi_agaciro);
        if(결과<0) { IKOSA(결과); if(결과==-16)단말.kwandika("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.kwandika("IPv4 configuration applied (until reboot)\n"); kugaragaza_Urusobemiyoboro_imimerere(); }
    }
    static void Urusobemiyoboro_ibwiriza(boolean Aderesi_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { kugaragaza_Urusobemiyoboro_imimerere();return; }
        if (Aderesi_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { kugaragaza_inzira();return; }
        if (같음(1,"set")) { itsinda_aderesi(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.Urusobemiyoboro_Amagenamiterere(같음(1,"up")?1:2,0,0,0);kugaragaza_Urusobemiyoboro_imimerere();return; }
        if (Aderesi_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.Urusobemiyoboro_Amagenamiterere(같음(5,"up")?1:2,0,0,0);kugaragaza_Urusobemiyoboro_imimerere();return; }
        kudakora_agaciro("사용법: ip [addr show|route show|set aderesi 주소가림 muhuzaporotokore_agaciro|link set dev sl0 up|down]");
    }
    static void kugaragaza_inzira() {
        단말.kwandika("Destination Netmask Gateway Interface\n");
        kwandika_aderesi(보드.Urusobemiyoboro_imimerere(0,0)&보드.Urusobemiyoboro_imimerere(1,0));단말.문자(' ');kwandika_aderesi(보드.Urusobemiyoboro_imimerere(1,0));단말.kwandika(보드.Urusobemiyoboro_imimerere(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Urusobemiyoboro_imimerere(2,0)!=0) {단말.kwandika("0.0.0.0 0.0.0.0 ");kwandika_aderesi(보드.Urusobemiyoboro_imimerere(2,0));단말.kwandika(보드.Urusobemiyoboro_imimerere(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void kugaragaza_Urusobemiyoboro() {
        단말.kwandika("Proto Local Remote State Queued\n");
        for(int umugerekashakiro=0;umugerekashakiro<32;umugerekashakiro++) {
            int 유형=보드.Urusobemiyoboro_imimerere(10,umugerekashakiro);if(유형==0)continue;
            단말.kwandika(유형==1?"TCP ":"UDP ");kwandika_aderesi(보드.Urusobemiyoboro_imimerere(16,umugerekashakiro));단말.문자(':');단말.수(보드.Urusobemiyoboro_imimerere(11,umugerekashakiro));단말.문자(' ');
            kwandika_aderesi(보드.Urusobemiyoboro_imimerere(12,umugerekashakiro));단말.문자(':');단말.수(보드.Urusobemiyoboro_imimerere(13,umugerekashakiro));단말.문자(' ');
            int imimerere_agaciro=보드.Urusobemiyoboro_imimerere(14,umugerekashakiro);단말.kwandika(유형==2?"DATAGRAM":imimerere_agaciro==1?"LISTEN":imimerere_agaciro==2?"ESTABLISHED":imimerere_agaciro==3?"CLOSE_WAIT":imimerere_agaciro==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Urusobemiyoboro_imimerere(15,umugerekashakiro));단말.문자(10);
        }
        단말.kwandika("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int ihuriro=보드.밀리초();
        while(보드.밀리초()-ihuriro<밀리초) {
            if(셸입출력.대화가능()!=0){int inyuguti_agaciro=보드.직렬읽기();if(inyuguti_agaciro==3 || inyuguti_agaciro=='q' || inyuguti_agaciro=='Q' || inyuguti_agaciro==27 || inyuguti_agaciro==-4096)return false;}
            보드.gusubika_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, gusimbuza_igishya=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=umubare_agaciro(++자리,100);if(횟수<1){kudakora_agaciro("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=umubare_agaciro(++자리,10);if(제한<1){kudakora_agaciro("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(gusimbuza_igishya<0)gusimbuza_igishya=자리;else{kudakora_agaciro("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(gusimbuza_igishya<0 || !주소읽기(gusimbuza_igishya)){kudakora_agaciro("ping: an IPv4 address is required (DNS is not configured)");return;}
        int aderesi=aderesi_agaciro, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.kwandika("PING ");kwandika_aderesi(aderesi);단말.kwandika(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int umujyo_agaciro=1;umujyo_agaciro<=횟수 && 계속;umujyo_agaciro++) {
            int 처리값=보드.응답보내기(aderesi,umujyo_agaciro);
            if(처리값<0){IKOSA(처리값);break;}보낸수++;
            int ihuriro=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-ihuriro<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.kwandika("32 bytes from ");kwandika_aderesi(aderesi);단말.kwandika(" seq=");단말.수(umujyo_agaciro);단말.kwandika(" ttl=");단말.수(보드.응답읽기(2));단말.kwandika(" time=");단말.수(시간);단말.kwandika(" ms\n");
            }else{단말.kwandika("Request timeout seq=");단말.수(umujyo_agaciro);단말.문자(10);}
            if(umujyo_agaciro<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.kwandika(" transmitted, ");단말.수(받은수);단말.kwandika(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.kwandika("% packet loss\n");
        if(받은수>0){단말.kwandika("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.kwandika(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void kugaragaza_Igikorwa() { 단말.kwandika("up ");단말.수(보드.밀리초()/1000);단말.kwandika(" seconds\n"); }
    static void kugaragaza_ububiko() {
        수항목("ARM RAM KiB (firmware): ",보드.isaba_sisitemu(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.isaba_sisitemu(1,0));
        int 총량=보드.isaba_sisitemu(2,0), 사용량=보드.isaba_sisitemu(3,0);
        단말.kwandika("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.isaba_sisitemu(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.isaba_sisitemu(5,0));
        int 매핑=0;for(int umugerekashakiro=0;umugerekashakiro<4;umugerekashakiro++)매핑+=보드.isaba_sisitemu(22,umugerekashakiro);
        수항목("EL0 mapped KiB: ",매핑);
        단말.kwandika("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.kwandika("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.kwandika("1 - RUN - - ");단말.수(보드.밀리초());단말.kwandika(" kernel/shell\n");
        for(int umugerekashakiro=1;umugerekashakiro<3;umugerekashakiro++)if(보드.umukoro_imimerere(umugerekashakiro)>0){단말.수(umugerekashakiro+1);단말.kwandika(" - READY 64 - - kernel-task\n");}
        for(int umugerekashakiro=0;umugerekashakiro<4;umugerekashakiro++){
            int imimerere_agaciro=보드.isaba_sisitemu(20,umugerekashakiro);if(imimerere_agaciro==0)continue;
            단말.수(보드.isaba_sisitemu(21,umugerekashakiro));단말.문자(' ');단말.수(umugerekashakiro);단말.kwandika(imimerere_agaciro==1?" RUN ":" SUSPENDED ");
            단말.수(보드.isaba_sisitemu(22,umugerekashakiro));단말.문자(' ');단말.수(보드.isaba_sisitemu(24,umugerekashakiro));단말.문자(' ');단말.수(보드.isaba_sisitemu(23,umugerekashakiro));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int bayiti_agaciro=보드.isaba_sisitemu(25,umugerekashakiro+자리*4);if(bayiti_agaciro==0)break;보드.직렬쓰기(bayiti_agaciro);}단말.문자(10);
        }
    }
    static void kugaragaza_Ububiko() {
        int 칸수=0, 자료수=0;
        for(int umugerekashakiro=0;umugerekashakiro<ububiko_Dosiye.파일수;umugerekashakiro++)if(ububiko_Dosiye.이름길이[umugerekashakiro]>0 || ububiko_Dosiye.참조수[umugerekashakiro]>0){칸수++;자료수+=ububiko_Dosiye.uburebure_agaciro[umugerekashakiro];}
        단말.kwandika("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(ububiko_Dosiye.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((ububiko_Dosiye.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(ububiko_Dosiye.파일수);단말.kwandika(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void kugaragaza_imimerere_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=umubare_agaciro(2,1000))<1){kudakora_agaciro("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int URUKURIKIRANE_agaciro=0;횟수==0 || URUKURIKIRANE_agaciro<횟수;URUKURIKIRANE_agaciro++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.kwandika("\u001b[2J\u001b[H");
            kugaragaza_Igikorwa();kugaragaza_ububiko();작업보기();
            if(횟수!=0 && URUKURIKIRANE_agaciro+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int umugerekashakiro) {
        if(umugerekashakiro==0)return "ipconfig";if(umugerekashakiro==1)return "ip";if(umugerekashakiro==2)return "ping";if(umugerekashakiro==3)return "route";if(umugerekashakiro==4)return "netstat";
        if(umugerekashakiro==5)return "ps";if(umugerekashakiro==6)return "top";if(umugerekashakiro==7)return "free";if(umugerekashakiro==8)return "df";if(umugerekashakiro==9)return "uptime";if(umugerekashakiro==10)return "poweroff";return "help";
    }
    static void kugaragaza_ifashayoboro() {
        단말.kwandika("--- Network / system commands ---\n");
        for(int umugerekashakiro=0;umugerekashakiro<12;umugerekashakiro++){단말.kwandika(표준말(umugerekashakiro));단말.kwandika(" / ");단말.kwandika(관리명령.Ijambo_SMS(umugerekashakiro));단말.kwandika(" : ");단말.kwandika(관리명령.설명(umugerekashakiro));단말.문자(10);}
        단말.kwandika("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.kwandika("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.kwandika("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean gukora_ibwiriza() {
        int Icyo_wifuza=-1;
        for(int umugerekashakiro=0;umugerekashakiro<12;umugerekashakiro++)if(같음(0,표준말(umugerekashakiro)) || 같음(0,관리명령.Ijambo_SMS(umugerekashakiro)))Icyo_wifuza=umugerekashakiro;
        if(같음(0,"ifconfig"))Icyo_wifuza=0;if(같음(0,"ss"))Icyo_wifuza=4;
        if(Icyo_wifuza<0)return false;
        if(Icyo_wifuza==11){if(같음(1,"net") || 같음(1,"system"))kugaragaza_ifashayoboro();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.kugaragaza_ifashayoboro();return true;}
        if(Icyo_wifuza==0 || Icyo_wifuza==1)Urusobemiyoboro_ibwiriza(Icyo_wifuza==1);
        else if(Icyo_wifuza==2)응답시험();
        else if(Icyo_wifuza==6)kugaragaza_imimerere_bf9821b5();
        else if(개수()!=1){kudakora_agaciro("This command takes no arguments; help system");}
        else if(Icyo_wifuza==3)kugaragaza_inzira();else if(Icyo_wifuza==4)kugaragaza_Urusobemiyoboro();else if(Icyo_wifuza==5)작업보기();else if(Icyo_wifuza==7)kugaragaza_ububiko();else if(Icyo_wifuza==8)kugaragaza_Ububiko();else if(Icyo_wifuza==9)kugaragaza_Igikorwa();
        else if(Icyo_wifuza==10)보드.전원끄기();
        return true;
    }
}
