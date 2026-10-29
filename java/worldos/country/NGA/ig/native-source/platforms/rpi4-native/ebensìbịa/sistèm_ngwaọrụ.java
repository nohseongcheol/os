// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ǹdịnezie_datà mkpụrụobī_kọmpùta_valuu 상태를 읽는 IPv4·ICMP·작업·memọrị_valuu·RAM 저장소 관리 Ntiiwu. */
public final class sistèm_ngwaọrụ {
    static int àdreèsì_valuu;
    static boolean 같음(int indèks, String Mkpụrụokwu_SMS) { return 명령해석기.같음(indèks, Mkpụrụokwu_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void ọdịdà_valuu(String GỤ̀ỌM_eb81d7d9) { 명령해석기.결과=2; 단말.Chekwaa_ozi(GỤ̀ỌM_eb81d7d9); 단말.문자(10); }
    static void mmejọ(int valuu) { 명령해석기.mmejọ(valuu); }
    static void 수항목(String Aha, int valuu) { 단말.Chekwaa_ozi(Aha); 단말.수(valuu); 단말.문자(10); }
    static int ọbula_valuu(int indèks, int 한도) {
        if (indèks>=개수() || 명령해석기.ogologo_valuu[indèks]==0) return -1;
        int valuu=0;
        for (int 순번=0; 순번<명령해석기.ogologo_valuu[indèks]; 순번++) {
            int mkpụrụedemede_valuu=명령해석기.akara_valuu_eb540501[명령해석기.시작점[indèks]+순번]-'0';
            if (mkpụrụedemede_valuu<0 || mkpụrụedemede_valuu>9 || valuu>(한도-mkpụrụedemede_valuu)/10) return -1;
            valuu=valuu*10+mkpụrụedemede_valuu;
        }
        return valuu<=한도?valuu:-1;
    }
    static boolean 주소읽기(int indèks) {
        if (indèks>=개수()) return false;
        int valuu=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.ogologo_valuu[indèks]; 순번++) {
            int mkpụrụedemede_valuu=명령해석기.akara_valuu_eb540501[명령해석기.시작점[indèks]+순번];
            if (mkpụrụedemede_valuu=='.') { if (숫자수==0 || ++점수>3) return false; valuu=(valuu<<8)|덩이; 덩이=숫자수=0; }
            else { if (mkpụrụedemede_valuu<'0' || mkpụrụedemede_valuu>'9' || ++숫자수>3) return false; 덩이=덩이*10+mkpụrụedemede_valuu-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        àdreèsì_valuu=(valuu<<8)|덩이; return true;
    }
    static void dee_àdreèsì(int valuu) {
        단말.수((valuu>>>24)&255); 단말.문자('.'); 단말.수((valuu>>>16)&255); 단말.문자('.');
        단말.수((valuu>>>8)&255); 단말.문자('.'); 단말.수(valuu&255);
    }
    static void gòsi_Netwọọkụ_ọnọdụ() {
        단말.Chekwaa_ozi(보드.Netwọọkụ_ọnọdụ(20,0)!=0?"en0: ":"sl0: "); 단말.Chekwaa_ozi(보드.Netwọọkụ_ọnọdụ(3,0)!=0?"UP":"DOWN");
        단말.Chekwaa_ozi(보드.Netwọọkụ_ọnọdụ(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Chekwaa_ozi(보드.Netwọọkụ_ọnọdụ(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); dee_àdreèsì(보드.Netwọọkụ_ọnọdụ(0,0));
        단말.Chekwaa_ozi(" netmask "); dee_àdreèsì(보드.Netwọọkụ_ọnọdụ(1,0)); 단말.Chekwaa_ozi(" gateway "); dee_àdreèsì(보드.Netwọọkụ_ọnọdụ(2,0)); 단말.문자(10);
        단말.Chekwaa_ozi("  RX packets "); 단말.수(보드.Netwọọkụ_ọnọdụ(4,0)); 단말.Chekwaa_ozi(" bytes "); 단말.수(보드.Netwọọkụ_ọnọdụ(6,0));
        단말.Chekwaa_ozi(" TX packets "); 단말.수(보드.Netwọọkụ_ọnọdụ(5,0)); 단말.Chekwaa_ozi(" bytes "); 단말.수(보드.Netwọọkụ_ọnọdụ(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Netwọọkụ_ọnọdụ(8,0));
    }
    static void Seti_àdreèsì(int Bido) {
        if (개수()!=Bido+3 || !주소읽기(Bido)) { ọdịdà_valuu("사용법: ipconfig set àdreèsì 주소가림 ụzọmbànye_valuu"); return; }
        int àdreèsì=àdreèsì_valuu;
        if(!주소읽기(Bido+1)){ọdịdà_valuu("Invalid IPv4 netmask");return;} int mkpù_valuu=àdreèsì_valuu;
        if(!주소읽기(Bido+2)){ọdịdà_valuu("Invalid IPv4 gateway");return;}
        int 결과=보드.Netwọọkụ_Mwube(0,àdreèsì,mkpù_valuu,àdreèsì_valuu);
        if(결과<0) { mmejọ(결과); if(결과==-16)단말.Chekwaa_ozi("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Chekwaa_ozi("IPv4 configuration applied (until reboot)\n"); gòsi_Netwọọkụ_ọnọdụ(); }
    }
    static void Netwọọkụ_nnyemiwu(boolean adreèsì_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { gòsi_Netwọọkụ_ọnọdụ();return; }
        if (adreèsì_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { gòsi_ụzọ_ozi();return; }
        if (같음(1,"set")) { Seti_àdreèsì(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.Netwọọkụ_Mwube(같음(1,"up")?1:2,0,0,0);gòsi_Netwọọkụ_ọnọdụ();return; }
        if (adreèsì_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.Netwọọkụ_Mwube(같음(5,"up")?1:2,0,0,0);gòsi_Netwọọkụ_ọnọdụ();return; }
        ọdịdà_valuu("사용법: ip [addr show|route show|set àdreèsì 주소가림 ụzọmbànye_valuu|link set dev sl0 up|down]");
    }
    static void gòsi_ụzọ_ozi() {
        단말.Chekwaa_ozi("Destination Netmask Gateway Interface\n");
        dee_àdreèsì(보드.Netwọọkụ_ọnọdụ(0,0)&보드.Netwọọkụ_ọnọdụ(1,0));단말.문자(' ');dee_àdreèsì(보드.Netwọọkụ_ọnọdụ(1,0));단말.Chekwaa_ozi(보드.Netwọọkụ_ọnọdụ(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Netwọọkụ_ọnọdụ(2,0)!=0) {단말.Chekwaa_ozi("0.0.0.0 0.0.0.0 ");dee_àdreèsì(보드.Netwọọkụ_ọnọdụ(2,0));단말.Chekwaa_ozi(보드.Netwọọkụ_ọnọdụ(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void gòsi_Netwọọkụ() {
        단말.Chekwaa_ozi("Proto Local Remote State Queued\n");
        for(int indèks=0;indèks<32;indèks++) {
            int pinye_otu=보드.Netwọọkụ_ọnọdụ(10,indèks);if(pinye_otu==0)continue;
            단말.Chekwaa_ozi(pinye_otu==1?"TCP ":"UDP ");dee_àdreèsì(보드.Netwọọkụ_ọnọdụ(16,indèks));단말.문자(':');단말.수(보드.Netwọọkụ_ọnọdụ(11,indèks));단말.문자(' ');
            dee_àdreèsì(보드.Netwọọkụ_ọnọdụ(12,indèks));단말.문자(':');단말.수(보드.Netwọọkụ_ọnọdụ(13,indèks));단말.문자(' ');
            int ọnọdụ_valuu=보드.Netwọọkụ_ọnọdụ(14,indèks);단말.Chekwaa_ozi(pinye_otu==2?"DATAGRAM":ọnọdụ_valuu==1?"LISTEN":ọnọdụ_valuu==2?"ESTABLISHED":ọnọdụ_valuu==3?"CLOSE_WAIT":ọnọdụ_valuu==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Netwọọkụ_ọnọdụ(15,indèks));단말.문자(10);
        }
        단말.Chekwaa_ozi("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int Bido=보드.밀리초();
        while(보드.밀리초()-Bido<밀리초) {
            if(셸입출력.대화가능()!=0){int mkpụrụedemede_valuu=보드.직렬읽기();if(mkpụrụedemede_valuu==3 || mkpụrụedemede_valuu=='q' || mkpụrụedemede_valuu=='Q' || mkpụrụedemede_valuu==27 || mkpụrụedemede_valuu==-4096)return false;}
            보드.kwụsịtụ_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, ebenlereanya=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=ọbula_valuu(++자리,100);if(횟수<1){ọdịdà_valuu("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=ọbula_valuu(++자리,10);if(제한<1){ọdịdà_valuu("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(ebenlereanya<0)ebenlereanya=자리;else{ọdịdà_valuu("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(ebenlereanya<0 || !주소읽기(ebenlereanya)){ọdịdà_valuu("ping: an IPv4 address is required (DNS is not configured)");return;}
        int àdreèsì=àdreèsì_valuu, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Chekwaa_ozi("PING ");dee_àdreèsì(àdreèsì);단말.Chekwaa_ozi(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ùsòrò_valuu=1;ùsòrò_valuu<=횟수 && 계속;ùsòrò_valuu++) {
            int 처리값=보드.응답보내기(àdreèsì,ùsòrò_valuu);
            if(처리값<0){mmejọ(처리값);break;}보낸수++;
            int Bido=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-Bido<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.Chekwaa_ozi("32 bytes from ");dee_àdreèsì(àdreèsì);단말.Chekwaa_ozi(" seq=");단말.수(ùsòrò_valuu);단말.Chekwaa_ozi(" ttl=");단말.수(보드.응답읽기(2));단말.Chekwaa_ozi(" time=");단말.수(시간);단말.Chekwaa_ozi(" ms\n");
            }else{단말.Chekwaa_ozi("Request timeout seq=");단말.수(ùsòrò_valuu);단말.문자(10);}
            if(ùsòrò_valuu<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.Chekwaa_ozi(" transmitted, ");단말.수(받은수);단말.Chekwaa_ozi(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.Chekwaa_ozi("% packet loss\n");
        if(받은수>0){단말.Chekwaa_ozi("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.Chekwaa_ozi(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void gòsi_Mmèmmè() { 단말.Chekwaa_ozi("up ");단말.수(보드.밀리초()/1000);단말.Chekwaa_ozi(" seconds\n"); }
    static void gòsi_memọrị() {
        수항목("ARM RAM KiB (firmware): ",보드.mgbaajụjụ_sistèm(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.mgbaajụjụ_sistèm(1,0));
        int 총량=보드.mgbaajụjụ_sistèm(2,0), 사용량=보드.mgbaajụjụ_sistèm(3,0);
        단말.Chekwaa_ozi("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.mgbaajụjụ_sistèm(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.mgbaajụjụ_sistèm(5,0));
        int 매핑=0;for(int indèks=0;indèks<4;indèks++)매핑+=보드.mgbaajụjụ_sistèm(22,indèks);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Chekwaa_ozi("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.Chekwaa_ozi("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Chekwaa_ozi("1 - RUN - - ");단말.수(보드.밀리초());단말.Chekwaa_ozi(" kernel/shell\n");
        for(int indèks=1;indèks<3;indèks++)if(보드.ọrụ_ọnọdụ(indèks)>0){단말.수(indèks+1);단말.Chekwaa_ozi(" - READY 64 - - kernel-task\n");}
        for(int indèks=0;indèks<4;indèks++){
            int ọnọdụ_valuu=보드.mgbaajụjụ_sistèm(20,indèks);if(ọnọdụ_valuu==0)continue;
            단말.수(보드.mgbaajụjụ_sistèm(21,indèks));단말.문자(' ');단말.수(indèks);단말.Chekwaa_ozi(ọnọdụ_valuu==1?" RUN ":" SUSPENDED ");
            단말.수(보드.mgbaajụjụ_sistèm(22,indèks));단말.문자(' ');단말.수(보드.mgbaajụjụ_sistèm(24,indèks));단말.문자(' ');단말.수(보드.mgbaajụjụ_sistèm(23,indèks));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int baịtị_valuu=보드.mgbaajụjụ_sistèm(25,indèks+자리*4);if(baịtị_valuu==0)break;보드.직렬쓰기(baịtị_valuu);}단말.문자(10);
        }
    }
    static void gòsi_Nchekwa() {
        int 칸수=0, 자료수=0;
        for(int indèks=0;indèks<memọrị_Ndi_ọbọakwụkwọ.파일수;indèks++)if(memọrị_Ndi_ọbọakwụkwọ.이름길이[indèks]>0 || memọrị_Ndi_ọbọakwụkwọ.참조수[indèks]>0){칸수++;자료수+=memọrị_Ndi_ọbọakwụkwọ.ogologo_valuu[indèks];}
        단말.Chekwaa_ozi("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(memọrị_Ndi_ọbọakwụkwọ.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((memọrị_Ndi_ọbọakwụkwọ.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(memọrị_Ndi_ọbọakwụkwọ.파일수);단말.Chekwaa_ozi(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void gòsi_ọnọdụ_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=ọbula_valuu(2,1000))<1){ọdịdà_valuu("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int NSOTANSO_valuu=0;횟수==0 || NSOTANSO_valuu<횟수;NSOTANSO_valuu++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Chekwaa_ozi("\u001b[2J\u001b[H");
            gòsi_Mmèmmè();gòsi_memọrị();작업보기();
            if(횟수!=0 && NSOTANSO_valuu+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int indèks) {
        if(indèks==0)return "ipconfig";if(indèks==1)return "ip";if(indèks==2)return "ping";if(indèks==3)return "route";if(indèks==4)return "netstat";
        if(indèks==5)return "ps";if(indèks==6)return "top";if(indèks==7)return "free";if(indèks==8)return "df";if(indèks==9)return "uptime";if(indèks==10)return "poweroff";return "help";
    }
    static void gòsi_ènyèmaka() {
        단말.Chekwaa_ozi("--- Network / system commands ---\n");
        for(int indèks=0;indèks<12;indèks++){단말.Chekwaa_ozi(표준말(indèks));단말.Chekwaa_ozi(" / ");단말.Chekwaa_ozi(관리명령.Mkpụrụokwu_SMS(indèks));단말.Chekwaa_ozi(" : ");단말.Chekwaa_ozi(관리명령.설명(indèks));단말.문자(10);}
        단말.Chekwaa_ozi("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Chekwaa_ozi("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Chekwaa_ozi("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean mee_nnyemiwu() {
        int Ntiiwu=-1;
        for(int indèks=0;indèks<12;indèks++)if(같음(0,표준말(indèks)) || 같음(0,관리명령.Mkpụrụokwu_SMS(indèks)))Ntiiwu=indèks;
        if(같음(0,"ifconfig"))Ntiiwu=0;if(같음(0,"ss"))Ntiiwu=4;
        if(Ntiiwu<0)return false;
        if(Ntiiwu==11){if(같음(1,"net") || 같음(1,"system"))gòsi_ènyèmaka();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.gòsi_ènyèmaka();return true;}
        if(Ntiiwu==0 || Ntiiwu==1)Netwọọkụ_nnyemiwu(Ntiiwu==1);
        else if(Ntiiwu==2)응답시험();
        else if(Ntiiwu==6)gòsi_ọnọdụ_bf9821b5();
        else if(개수()!=1){ọdịdà_valuu("This command takes no arguments; help system");}
        else if(Ntiiwu==3)gòsi_ụzọ_ozi();else if(Ntiiwu==4)gòsi_Netwọọkụ();else if(Ntiiwu==5)작업보기();else if(Ntiiwu==7)gòsi_memọrị();else if(Ntiiwu==8)gòsi_Nchekwa();else if(Ntiiwu==9)gòsi_Mmèmmè();
        else if(Ntiiwu==10)보드.전원끄기();
        return true;
    }
}
