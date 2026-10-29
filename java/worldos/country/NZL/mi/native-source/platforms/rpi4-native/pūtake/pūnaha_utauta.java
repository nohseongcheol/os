// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tūturu_raraunga kākano_uara_0611a8a8 상태를 읽는 IPv4·ICMP·작업·Pūmahara_uara·RAM 저장소 관리 tono. */
public final class pūnaha_utauta {
    static int ADDRESS_uara;
    static boolean 같음(int INDEX, String Word_TEXT) { return 명령해석기.같음(INDEX, Word_TEXT); }
    static int tuemi_COUNT() { return 명령해석기.tohu_COUNT; }
    static void rahunga_uara(String PĀNUIMAI_eb81d7d9) { 명령해석기.mēhua=2; 단말.Tuhia(PĀNUIMAI_eb81d7d9); 단말.문자(10); }
    static void Pōhēhē(int uara) { 명령해석기.Pōhēhē(uara); }
    static void 수항목(String Ingoa, int uara) { 단말.Tuhia(Ingoa); 단말.수(uara); 단말.문자(10); }
    static int mati_uara(int INDEX, int 한도) {
        if (INDEX>=tuemi_COUNT() || 명령해석기.roa_uara[INDEX]==0) return -1;
        int uara=0;
        for (int 순번=0; 순번<명령해석기.roa_uara[INDEX]; 순번++) {
            int pūāhua_uara=명령해석기.tohu_uara_eb540501[명령해석기.시작점[INDEX]+순번]-'0';
            if (pūāhua_uara<0 || pūāhua_uara>9 || uara>(한도-pūāhua_uara)/10) return -1;
            uara=uara*10+pūāhua_uara;
        }
        return uara<=한도?uara:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=tuemi_COUNT()) return false;
        int uara=0, 덩이=0, mati_COUNT=0, ira_COUNT=0;
        for (int 순번=0; 순번<명령해석기.roa_uara[INDEX]; 순번++) {
            int pūāhua_uara=명령해석기.tohu_uara_eb540501[명령해석기.시작점[INDEX]+순번];
            if (pūāhua_uara=='.') { if (mati_COUNT==0 || ++ira_COUNT>3) return false; uara=(uara<<8)|덩이; 덩이=mati_COUNT=0; }
            else { if (pūāhua_uara<'0' || pūāhua_uara>'9' || ++mati_COUNT>3) return false; 덩이=덩이*10+pūāhua_uara-'0'; if(덩이>255)return false; }
        }
        if (ira_COUNT!=3 || mati_COUNT==0) return false;
        ADDRESS_uara=(uara<<8)|덩이; return true;
    }
    static void tuhi_ADDRESS(int uara) {
        단말.수((uara>>>24)&255); 단말.문자('.'); 단말.수((uara>>>16)&255); 단말.문자('.');
        단말.수((uara>>>8)&255); 단말.문자('.'); 단말.수(uara&255);
    }
    static void whakaatu_whatunga_tūnga() {
        단말.Tuhia(papa.whatunga_tūnga(20,0)!=0?"en0: ":"sl0: "); 단말.Tuhia(papa.whatunga_tūnga(3,0)!=0?"UP":"DOWN");
        단말.Tuhia(papa.whatunga_tūnga(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Tuhia(papa.whatunga_tūnga(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); tuhi_ADDRESS(papa.whatunga_tūnga(0,0));
        단말.Tuhia(" netmask "); tuhi_ADDRESS(papa.whatunga_tūnga(1,0)); 단말.Tuhia(" gateway "); tuhi_ADDRESS(papa.whatunga_tūnga(2,0)); 단말.문자(10);
        단말.Tuhia("  RX packets "); 단말.수(papa.whatunga_tūnga(4,0)); 단말.Tuhia(" bytes "); 단말.수(papa.whatunga_tūnga(6,0));
        단말.Tuhia(" TX packets "); 단말.수(papa.whatunga_tūnga(5,0)); 단말.Tuhia(" bytes "); 단말.수(papa.whatunga_tūnga(7,0)); 단말.문자(10);
        수항목("  dropped ",papa.whatunga_tūnga(8,0));
    }
    static void huinga_ADDRESS(int whakahaere) {
        if (tuemi_COUNT()!=whakahaere+3 || !주소읽기(whakahaere)) { rahunga_uara("사용법: ipconfig set ADDRESS 주소가림 waharoa_uara"); return; }
        int ADDRESS=ADDRESS_uara;
        if(!주소읽기(whakahaere+1)){rahunga_uara("Invalid IPv4 netmask");return;} int hīpoki_uara=ADDRESS_uara;
        if(!주소읽기(whakahaere+2)){rahunga_uara("Invalid IPv4 gateway");return;}
        int mēhua=papa.whatunga_Ngā_Tautuhinga(0,ADDRESS,hīpoki_uara,ADDRESS_uara);
        if(mēhua<0) { Pōhēhē(mēhua); if(mēhua==-16)단말.Tuhia("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Tuhia("IPv4 configuration applied (until reboot)\n"); whakaatu_whatunga_tūnga(); }
    }
    static void whatunga_tono(boolean wāhitau_IP) {
        if (tuemi_COUNT()==1 || tuemi_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || tuemi_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { whakaatu_whatunga_tūnga();return; }
        if (wāhitau_IP && 같음(1,"route") && (tuemi_COUNT()==2 || tuemi_COUNT()==3&&같음(2,"show"))) { whakaatu_ara();return; }
        if (같음(1,"set")) { huinga_ADDRESS(2);return; }
        if (tuemi_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { papa.whatunga_Ngā_Tautuhinga(같음(1,"up")?1:2,0,0,0);whakaatu_whatunga_tūnga();return; }
        if (wāhitau_IP && tuemi_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { papa.whatunga_Ngā_Tautuhinga(같음(5,"up")?1:2,0,0,0);whakaatu_whatunga_tūnga();return; }
        rahunga_uara("사용법: ip [addr show|route show|set ADDRESS 주소가림 waharoa_uara|link set dev sl0 up|down]");
    }
    static void whakaatu_ara() {
        단말.Tuhia("Destination Netmask Gateway Interface\n");
        tuhi_ADDRESS(papa.whatunga_tūnga(0,0)&papa.whatunga_tūnga(1,0));단말.문자(' ');tuhi_ADDRESS(papa.whatunga_tūnga(1,0));단말.Tuhia(papa.whatunga_tūnga(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (papa.whatunga_tūnga(2,0)!=0) {단말.Tuhia("0.0.0.0 0.0.0.0 ");tuhi_ADDRESS(papa.whatunga_tūnga(2,0));단말.Tuhia(papa.whatunga_tūnga(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void whakaatu_whatunga() {
        단말.Tuhia("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_kāwai=papa.whatunga_tūnga(10,INDEX);if(TYPE_kāwai==0)continue;
            단말.Tuhia(TYPE_kāwai==1?"TCP ":"UDP ");tuhi_ADDRESS(papa.whatunga_tūnga(16,INDEX));단말.문자(':');단말.수(papa.whatunga_tūnga(11,INDEX));단말.문자(' ');
            tuhi_ADDRESS(papa.whatunga_tūnga(12,INDEX));단말.문자(':');단말.수(papa.whatunga_tūnga(13,INDEX));단말.문자(' ');
            int tūnga_uara=papa.whatunga_tūnga(14,INDEX);단말.Tuhia(TYPE_kāwai==2?"DATAGRAM":tūnga_uara==1?"LISTEN":tūnga_uara==2?"ESTABLISHED":tūnga_uara==3?"CLOSE_WAIT":tūnga_uara==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(papa.whatunga_tūnga(15,INDEX));단말.문자(10);
        }
        단말.Tuhia("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int whakahaere=papa.밀리초();
        while(papa.밀리초()-whakahaere<밀리초) {
            if(셸입출력.대화가능()!=0){int pūāhua_uara=papa.직렬읽기();if(pūāhua_uara==3 || pūāhua_uara=='q' || pūāhua_uara=='Q' || pūāhua_uara==27 || pūāhua_uara==-4096)return false;}
            papa.YIELD_PTM();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, ūnga=-1;
        for(int tūranga_INDEX=1;tūranga_INDEX<tuemi_COUNT();tūranga_INDEX++) {
            if(같음(tūranga_INDEX,"-c")){횟수=mati_uara(++tūranga_INDEX,100);if(횟수<1){rahunga_uara("ping: -c 1..100");return;}}
            else if(같음(tūranga_INDEX,"-W")){제한=mati_uara(++tūranga_INDEX,10);if(제한<1){rahunga_uara("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(ūnga<0)ūnga=tūranga_INDEX;else{rahunga_uara("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(ūnga<0 || !주소읽기(ūnga)){rahunga_uara("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADDRESS=ADDRESS_uara, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Tuhia("PING ");tuhi_ADDRESS(ADDRESS);단말.Tuhia(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int whakaraupapa_uara=1;whakaraupapa_uara<=횟수 && 계속;whakaraupapa_uara++) {
            int 처리값=papa.응답보내기(ADDRESS,whakaraupapa_uara);
            if(처리값<0){Pōhēhē(처리값);break;}보낸수++;
            int whakahaere=papa.밀리초();
            while(papa.응답읽기(0)==-11 && papa.밀리초()-whakahaere<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(papa.응답읽기(0)==0){
                int TIME_uara=papa.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_uara;if(TIME_uara<최솟값)최솟값=TIME_uara;if(TIME_uara>최댓값)최댓값=TIME_uara;
                단말.Tuhia("32 bytes from ");tuhi_ADDRESS(ADDRESS);단말.Tuhia(" seq=");단말.수(whakaraupapa_uara);단말.Tuhia(" ttl=");단말.수(papa.응답읽기(2));단말.Tuhia(" time=");단말.수(TIME_uara);단말.Tuhia(" ms\n");
            }else{단말.Tuhia("Request timeout seq=");단말.수(whakaraupapa_uara);단말.문자(10);}
            if(whakaraupapa_uara<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.Tuhia(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Tuhia(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Tuhia("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Tuhia("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Tuhia(" ms\n");}
        명령해석기.mēhua=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void whakaatu_Ngohe() { 단말.Tuhia("up ");단말.수(papa.밀리초()/1000);단말.Tuhia(" seconds\n"); }
    static void whakaatu_Pūmahara() {
        수항목("ARM RAM KiB (firmware): ",papa.uiui_pūnaha(0,0));
        수항목("Kernel image+BSS+stack KiB: ",papa.uiui_pūnaha(1,0));
        int 총량=papa.uiui_pūnaha(2,0), 사용량=papa.uiui_pūnaha(3,0);
        단말.Tuhia("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",papa.uiui_pūnaha(4,0));
        수항목("EL0 arena+session reserve KiB: ",papa.uiui_pūnaha(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=papa.uiui_pūnaha(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Tuhia("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void whakaatu_Tasks() {
        단말.Tuhia("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Tuhia("1 - RUN - - ");단말.수(papa.밀리초());단말.Tuhia(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(papa.tūmahi_tūnga(INDEX)>0){단말.수(INDEX+1);단말.Tuhia(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int tūnga_uara=papa.uiui_pūnaha(20,INDEX);if(tūnga_uara==0)continue;
            단말.수(papa.uiui_pūnaha(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Tuhia(tūnga_uara==1?" RUN ":" SUSPENDED ");
            단말.수(papa.uiui_pūnaha(22,INDEX));단말.문자(' ');단말.수(papa.uiui_pūnaha(24,INDEX));단말.문자(' ');단말.수(papa.uiui_pūnaha(23,INDEX));단말.문자(' ');
            for(int tūranga_INDEX=0;tūranga_INDEX<288;tūranga_INDEX++){int paita_uara=papa.uiui_pūnaha(25,INDEX+tūranga_INDEX*4);if(paita_uara==0)break;papa.직렬쓰기(paita_uara);}단말.문자(10);
        }
    }
    static void whakaatu_Rokiroki() {
        int kāniwha_COUNT=0, raraunga_COUNT=0;
        for(int INDEX=0;INDEX<Pūmahara_Ngā_Kōnae.kōnae_COUNT;INDEX++)if(Pūmahara_Ngā_Kōnae.이름길이[INDEX]>0 || Pūmahara_Ngā_Kōnae.Pūranga_kōrero_COUNT[INDEX]>0){kāniwha_COUNT++;raraunga_COUNT+=Pūmahara_Ngā_Kōnae.roa_uara[INDEX];}
        단말.Tuhia("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Pūmahara_Ngā_Kōnae.kōnae_COUNT*16384);단말.문자(' ');단말.수(kāniwha_COUNT*16384);단말.문자(' ');단말.수((Pūmahara_Ngā_Kōnae.kōnae_COUNT-kāniwha_COUNT)*16384);단말.문자(' ');단말.수(raraunga_COUNT);단말.문자(' ');단말.수(kāniwha_COUNT);단말.문자('/');단말.수(Pūmahara_Ngā_Kōnae.kōnae_COUNT);단말.Tuhia(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void whakaatu_tūnga_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(tuemi_COUNT()>1){if(tuemi_COUNT()!=3 || !같음(1,"-n") || (횟수=mati_uara(2,1000))<1){rahunga_uara("사용법: top [-n 1..1000]; q/Ctrl+C로 wehe_kaupapa");return;}}
        for(int SEQUENCE_uara=0;횟수==0 || SEQUENCE_uara<횟수;SEQUENCE_uara++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Tuhia("\u001b[2J\u001b[H");
            whakaatu_Ngohe();whakaatu_Pūmahara();whakaatu_Tasks();
            if(횟수!=0 && SEQUENCE_uara+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void whakaatu_āwhina() {
        단말.Tuhia("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Tuhia(표준말(INDEX));단말.Tuhia(" / ");단말.Tuhia(관리명령.Word_TEXT(INDEX));단말.Tuhia(" : ");단말.Tuhia(관리명령.설명(INDEX));단말.문자(10);}
        단말.Tuhia("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Tuhia("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Tuhia("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean kawe_tono() {
        int tono=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_TEXT(INDEX)))tono=INDEX;
        if(같음(0,"ifconfig"))tono=0;if(같음(0,"ss"))tono=4;
        if(tono<0)return false;
        if(tono==11){if(같음(1,"net") || 같음(1,"system"))whakaatu_āwhina();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.whakaatu_āwhina();return true;}
        if(tono==0 || tono==1)whatunga_tono(tono==1);
        else if(tono==2)응답시험();
        else if(tono==6)whakaatu_tūnga_bf9821b5();
        else if(tuemi_COUNT()!=1){rahunga_uara("This command takes no arguments; help system");}
        else if(tono==3)whakaatu_ara();else if(tono==4)whakaatu_whatunga();else if(tono==5)whakaatu_Tasks();else if(tono==7)whakaatu_Pūmahara();else if(tono==8)whakaatu_Rokiroki();else if(tono==9)whakaatu_Ngohe();
        else if(tono==10)papa.전원끄기();
        return true;
    }
}
