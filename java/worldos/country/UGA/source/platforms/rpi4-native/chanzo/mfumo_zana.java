// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** halisi_data kiini_thamani_0611a8a8 상태를 읽는 IPv4·ICMP·작업·kumbukumbu_thamani_603669bd·RAM 저장소 관리 amri. */
public final class mfumo_zana {
    static int anwani_thamani;
    static boolean 같음(int kielezo, String Neno_SMS) { return 명령해석기.같음(kielezo, Neno_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void kushindwa_thamani(String NISOME_eb81d7d9) { 명령해석기.결과=2; 단말.andika(NISOME_eb81d7d9); 단말.문자(10); }
    static void kosa(int thamani) { 명령해석기.kosa(thamani); }
    static void 수항목(String Jina, int thamani) { 단말.andika(Jina); 단말.수(thamani); 단말.문자(10); }
    static int dijiti_thamani(int kielezo, int 한도) {
        if (kielezo>=개수() || 명령해석기.urefu_thamani[kielezo]==0) return -1;
        int thamani=0;
        for (int 순번=0; 순번<명령해석기.urefu_thamani[kielezo]; 순번++) {
            int kibambo_thamani=명령해석기.tuzo_thamani[명령해석기.시작점[kielezo]+순번]-'0';
            if (kibambo_thamani<0 || kibambo_thamani>9 || thamani>(한도-kibambo_thamani)/10) return -1;
            thamani=thamani*10+kibambo_thamani;
        }
        return thamani<=한도?thamani:-1;
    }
    static boolean 주소읽기(int kielezo) {
        if (kielezo>=개수()) return false;
        int thamani=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.urefu_thamani[kielezo]; 순번++) {
            int kibambo_thamani=명령해석기.tuzo_thamani[명령해석기.시작점[kielezo]+순번];
            if (kibambo_thamani=='.') { if (숫자수==0 || ++점수>3) return false; thamani=(thamani<<8)|덩이; 덩이=숫자수=0; }
            else { if (kibambo_thamani<'0' || kibambo_thamani>'9' || ++숫자수>3) return false; 덩이=덩이*10+kibambo_thamani-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        anwani_thamani=(thamani<<8)|덩이; return true;
    }
    static void andika_anwani(int thamani) {
        단말.수((thamani>>>24)&255); 단말.문자('.'); 단말.수((thamani>>>16)&255); 단말.문자('.');
        단말.수((thamani>>>8)&255); 단말.문자('.'); 단말.수(thamani&255);
    }
    static void onyesha_Mtandao_hali() {
        단말.andika(보드.Mtandao_hali(20,0)!=0?"en0: ":"sl0: "); 단말.andika(보드.Mtandao_hali(3,0)!=0?"UP":"DOWN");
        단말.andika(보드.Mtandao_hali(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.andika(보드.Mtandao_hali(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); andika_anwani(보드.Mtandao_hali(0,0));
        단말.andika(" netmask "); andika_anwani(보드.Mtandao_hali(1,0)); 단말.andika(" gateway "); andika_anwani(보드.Mtandao_hali(2,0)); 단말.문자(10);
        단말.andika("  RX packets "); 단말.수(보드.Mtandao_hali(4,0)); 단말.andika(" bytes "); 단말.수(보드.Mtandao_hali(6,0));
        단말.andika(" TX packets "); 단말.수(보드.Mtandao_hali(5,0)); 단말.andika(" bytes "); 단말.수(보드.Mtandao_hali(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Mtandao_hali(8,0));
    }
    static void seti_anwani(int endesha) {
        if (개수()!=endesha+3 || !주소읽기(endesha)) { kushindwa_thamani("사용법: ipconfig set anwani 주소가림 kichanganishi_mtandao_thamani"); return; }
        int anwani=anwani_thamani;
        if(!주소읽기(endesha+1)){kushindwa_thamani("Invalid IPv4 netmask");return;} int barakoa_thamani=anwani_thamani;
        if(!주소읽기(endesha+2)){kushindwa_thamani("Invalid IPv4 gateway");return;}
        int 결과=보드.Mtandao_Mipangilio(0,anwani,barakoa_thamani,anwani_thamani);
        if(결과<0) { kosa(결과); if(결과==-16)단말.andika("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.andika("IPv4 configuration applied (until reboot)\n"); onyesha_Mtandao_hali(); }
    }
    static void Mtandao_amri(boolean anwani_ya_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { onyesha_Mtandao_hali();return; }
        if (anwani_ya_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { onyesha_njia();return; }
        if (같음(1,"set")) { seti_anwani(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.Mtandao_Mipangilio(같음(1,"up")?1:2,0,0,0);onyesha_Mtandao_hali();return; }
        if (anwani_ya_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.Mtandao_Mipangilio(같음(5,"up")?1:2,0,0,0);onyesha_Mtandao_hali();return; }
        kushindwa_thamani("사용법: ip [addr show|route show|set anwani 주소가림 kichanganishi_mtandao_thamani|link set dev sl0 up|down]");
    }
    static void onyesha_njia() {
        단말.andika("Destination Netmask Gateway Interface\n");
        andika_anwani(보드.Mtandao_hali(0,0)&보드.Mtandao_hali(1,0));단말.문자(' ');andika_anwani(보드.Mtandao_hali(1,0));단말.andika(보드.Mtandao_hali(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Mtandao_hali(2,0)!=0) {단말.andika("0.0.0.0 0.0.0.0 ");andika_anwani(보드.Mtandao_hali(2,0));단말.andika(보드.Mtandao_hali(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void onyesha_Mtandao() {
        단말.andika("Proto Local Remote State Queued\n");
        for(int kielezo=0;kielezo<32;kielezo++) {
            int aina_kategoria=보드.Mtandao_hali(10,kielezo);if(aina_kategoria==0)continue;
            단말.andika(aina_kategoria==1?"TCP ":"UDP ");andika_anwani(보드.Mtandao_hali(16,kielezo));단말.문자(':');단말.수(보드.Mtandao_hali(11,kielezo));단말.문자(' ');
            andika_anwani(보드.Mtandao_hali(12,kielezo));단말.문자(':');단말.수(보드.Mtandao_hali(13,kielezo));단말.문자(' ');
            int hali_thamani=보드.Mtandao_hali(14,kielezo);단말.andika(aina_kategoria==2?"DATAGRAM":hali_thamani==1?"LISTEN":hali_thamani==2?"ESTABLISHED":hali_thamani==3?"CLOSE_WAIT":hali_thamani==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Mtandao_hali(15,kielezo));단말.문자(10);
        }
        단말.andika("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean subiri_hali(int 밀리초) {
        int endesha=보드.밀리초();
        while(보드.밀리초()-endesha<밀리초) {
            if(셸입출력.teknolojia_ya_maelezo_ingiliani()!=0){int kibambo_thamani=보드.직렬읽기();if(kibambo_thamani==3 || kibambo_thamani=='q' || kibambo_thamani=='Q' || kibambo_thamani==27 || kibambo_thamani==-4096)return false;}
            보드.ahirisha_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, lengo=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=dijiti_thamani(++자리,100);if(횟수<1){kushindwa_thamani("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=dijiti_thamani(++자리,10);if(제한<1){kushindwa_thamani("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(lengo<0)lengo=자리;else{kushindwa_thamani("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(lengo<0 || !주소읽기(lengo)){kushindwa_thamani("ping: an IPv4 address is required (DNS is not configured)");return;}
        int anwani=anwani_thamani, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.andika("PING ");andika_anwani(anwani);단말.andika(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int mpangilio_thamani=1;mpangilio_thamani<=횟수 && 계속;mpangilio_thamani++) {
            int 처리값=보드.응답보내기(anwani,mpangilio_thamani);
            if(처리값<0){kosa(처리값);break;}보낸수++;
            int endesha=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-endesha<제한)if(!subiri_hali(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int saa_thamani_4692cef5=보드.응답읽기(1);받은수++;누적+=saa_thamani_4692cef5;if(saa_thamani_4692cef5<최솟값)최솟값=saa_thamani_4692cef5;if(saa_thamani_4692cef5>최댓값)최댓값=saa_thamani_4692cef5;
                단말.andika("32 bytes from ");andika_anwani(anwani);단말.andika(" seq=");단말.수(mpangilio_thamani);단말.andika(" ttl=");단말.수(보드.응답읽기(2));단말.andika(" time=");단말.수(saa_thamani_4692cef5);단말.andika(" ms\n");
            }else{단말.andika("Request timeout seq=");단말.수(mpangilio_thamani);단말.문자(10);}
            if(mpangilio_thamani<횟수)계속=subiri_hali(200);
        }
        단말.수(보낸수);단말.andika(" transmitted, ");단말.수(받은수);단말.andika(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.andika("% packet loss\n");
        if(받은수>0){단말.andika("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.andika(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void onyesha_Shughuli() { 단말.andika("up ");단말.수(보드.밀리초()/1000);단말.andika(" seconds\n"); }
    static void onyesha_kumbukumbu() {
        수항목("ARM RAM KiB (firmware): ",보드.uliza_mfumo(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.uliza_mfumo(1,0));
        int 총량=보드.uliza_mfumo(2,0), 사용량=보드.uliza_mfumo(3,0);
        단말.andika("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.uliza_mfumo(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.uliza_mfumo(5,0));
        int 매핑=0;for(int kielezo=0;kielezo<4;kielezo++)매핑+=보드.uliza_mfumo(22,kielezo);
        수항목("EL0 mapped KiB: ",매핑);
        단말.andika("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void onyesha_Kazi() {
        단말.andika("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.andika("1 - RUN - - ");단말.수(보드.밀리초());단말.andika(" kernel/shell\n");
        for(int kielezo=1;kielezo<3;kielezo++)if(보드.kazi_hali(kielezo)>0){단말.수(kielezo+1);단말.andika(" - READY 64 - - kernel-task\n");}
        for(int kielezo=0;kielezo<4;kielezo++){
            int hali_thamani=보드.uliza_mfumo(20,kielezo);if(hali_thamani==0)continue;
            단말.수(보드.uliza_mfumo(21,kielezo));단말.문자(' ');단말.수(kielezo);단말.andika(hali_thamani==1?" RUN ":" SUSPENDED ");
            단말.수(보드.uliza_mfumo(22,kielezo));단말.문자(' ');단말.수(보드.uliza_mfumo(24,kielezo));단말.문자(' ');단말.수(보드.uliza_mfumo(23,kielezo));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int baiti_thamani=보드.uliza_mfumo(25,kielezo+자리*4);if(baiti_thamani==0)break;보드.직렬쓰기(baiti_thamani);}단말.문자(10);
        }
    }
    static void onyesha_Hifadhi() {
        int 칸수=0, 자료수=0;
        for(int kielezo=0;kielezo<kumbukumbu_Faili.파일수;kielezo++)if(kumbukumbu_Faili.이름길이[kielezo]>0 || kumbukumbu_Faili.참조수[kielezo]>0){칸수++;자료수+=kumbukumbu_Faili.urefu_thamani[kielezo];}
        단말.andika("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(kumbukumbu_Faili.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((kumbukumbu_Faili.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(kumbukumbu_Faili.파일수);단말.andika(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void onyesha_hali_bf9821b5() {
        int 횟수=셸입출력.teknolojia_ya_maelezo_ingiliani()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=dijiti_thamani(2,1000))<1){kushindwa_thamani("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int MFUATANO_thamani=0;횟수==0 || MFUATANO_thamani<횟수;MFUATANO_thamani++){
            if(셸입출력.teknolojia_ya_maelezo_ingiliani()!=0 && 횟수==0)단말.andika("\u001b[2J\u001b[H");
            onyesha_Shughuli();onyesha_kumbukumbu();onyesha_Kazi();
            if(횟수!=0 && MFUATANO_thamani+1>=횟수)break;
            if(!subiri_hali(1000))break;
        }
    }
    static String 표준말(int kielezo) {
        if(kielezo==0)return "ipconfig";if(kielezo==1)return "ip";if(kielezo==2)return "ping";if(kielezo==3)return "route";if(kielezo==4)return "netstat";
        if(kielezo==5)return "ps";if(kielezo==6)return "top";if(kielezo==7)return "free";if(kielezo==8)return "df";if(kielezo==9)return "uptime";if(kielezo==10)return "poweroff";return "help";
    }
    static void onyesha_msaada() {
        단말.andika("--- Network / system commands ---\n");
        for(int kielezo=0;kielezo<12;kielezo++){단말.andika(표준말(kielezo));단말.andika(" / ");단말.andika(관리명령.Neno_SMS(kielezo));단말.andika(" : ");단말.andika(관리명령.설명(kielezo));단말.문자(10);}
        단말.andika("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.andika("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.andika("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean tekeleza_amri() {
        int amri=-1;
        for(int kielezo=0;kielezo<12;kielezo++)if(같음(0,표준말(kielezo)) || 같음(0,관리명령.Neno_SMS(kielezo)))amri=kielezo;
        if(같음(0,"ifconfig"))amri=0;if(같음(0,"ss"))amri=4;
        if(amri<0)return false;
        if(amri==11){if(같음(1,"net") || 같음(1,"system"))onyesha_msaada();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.onyesha_msaada();return true;}
        if(amri==0 || amri==1)Mtandao_amri(amri==1);
        else if(amri==2)응답시험();
        else if(amri==6)onyesha_hali_bf9821b5();
        else if(개수()!=1){kushindwa_thamani("This command takes no arguments; help system");}
        else if(amri==3)onyesha_njia();else if(amri==4)onyesha_Mtandao();else if(amri==5)onyesha_Kazi();else if(amri==7)onyesha_kumbukumbu();else if(amri==8)onyesha_Hifadhi();else if(amri==9)onyesha_Shughuli();
        else if(amri==10)보드.전원끄기();
        return true;
    }
}
