// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** werklik_data kern_VALUE 상태를 읽는 IPv4·ICMP·작업·Geheue_VALUE·RAM bewaarplek_wortel 관리 Opdrag. */
public final class stelsel_nutsmiddel {
    static int adres_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int item_COUNT() { return 명령해석기.kenteken_COUNT; }
    static void faling_VALUE(String README_eb81d7d9) { 명령해석기.maatreël=2; 단말.Skryf(README_eb81d7d9); 단말.문자(10); }
    static void Fout(int VALUE) { 명령해석기.Fout(VALUE); }
    static void 수항목(String Naam, int VALUE) { 단말.Skryf(Naam); 단말.수(VALUE); 단말.문자(10); }
    static int syfer_VALUE(int INDEX, int 한도) {
        if (INDEX>=item_COUNT() || 명령해석기.lengte_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.lengte_VALUE[INDEX]; 순번++) {
            int karakter_VALUE=명령해석기.kenteken_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (karakter_VALUE<0 || karakter_VALUE>9 || VALUE>(한도-karakter_VALUE)/10) return -1;
            VALUE=VALUE*10+karakter_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=item_COUNT()) return false;
        int VALUE=0, 덩이=0, syfer_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.lengte_VALUE[INDEX]; 순번++) {
            int karakter_VALUE=명령해석기.kenteken_VALUE[명령해석기.시작점[INDEX]+순번];
            if (karakter_VALUE=='.') { if (syfer_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=syfer_COUNT=0; }
            else { if (karakter_VALUE<'0' || karakter_VALUE>'9' || ++syfer_COUNT>3) return false; 덩이=덩이*10+karakter_VALUE-'0'; if(덩이>255)return false; }
        }
        if (p_COUNT!=3 || syfer_COUNT==0) return false;
        adres_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void skryf_adres(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void wys_Netwerk_stand() {
        단말.Skryf(bord.Netwerk_stand(20,0)!=0?"en0: ":"sl0: "); 단말.Skryf(bord.Netwerk_stand(3,0)!=0?"UP":"DOWN");
        단말.Skryf(bord.Netwerk_stand(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Skryf(bord.Netwerk_stand(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); skryf_adres(bord.Netwerk_stand(0,0));
        단말.Skryf(" netmask "); skryf_adres(bord.Netwerk_stand(1,0)); 단말.Skryf(" gateway "); skryf_adres(bord.Netwerk_stand(2,0)); 단말.문자(10);
        단말.Skryf("  RX packets "); 단말.수(bord.Netwerk_stand(4,0)); 단말.Skryf(" bytes "); 단말.수(bord.Netwerk_stand(6,0));
        단말.Skryf(" TX packets "); 단말.수(bord.Netwerk_stand(5,0)); 단말.Skryf(" bytes "); 단말.수(bord.Netwerk_stand(7,0)); 단말.문자(10);
        수항목("  dropped ",bord.Netwerk_stand(8,0));
    }
    static void stel_adres(int Loop) {
        if (item_COUNT()!=Loop+3 || !주소읽기(Loop)) { faling_VALUE("사용법: ipconfig set adres 주소가림 deurgang_VALUE"); return; }
        int adres=adres_VALUE;
        if(!주소읽기(Loop+1)){faling_VALUE("Invalid IPv4 netmask");return;} int masker_VALUE=adres_VALUE;
        if(!주소읽기(Loop+2)){faling_VALUE("Invalid IPv4 gateway");return;}
        int maatreël=bord.Netwerk_Instellings(0,adres,masker_VALUE,adres_VALUE);
        if(maatreël<0) { Fout(maatreël); if(maatreël==-16)단말.Skryf("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Skryf("IPv4 configuration applied (until reboot)\n"); wys_Netwerk_stand(); }
    }
    static void Netwerk_bevel(boolean IP_adres) {
        if (item_COUNT()==1 || item_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || item_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { wys_Netwerk_stand();return; }
        if (IP_adres && 같음(1,"route") && (item_COUNT()==2 || item_COUNT()==3&&같음(2,"show"))) { wys_pad();return; }
        if (같음(1,"set")) { stel_adres(2);return; }
        if (item_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { bord.Netwerk_Instellings(같음(1,"up")?1:2,0,0,0);wys_Netwerk_stand();return; }
        if (IP_adres && item_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { bord.Netwerk_Instellings(같음(5,"up")?1:2,0,0,0);wys_Netwerk_stand();return; }
        faling_VALUE("사용법: ip [addr show|route show|set adres 주소가림 deurgang_VALUE|link set dev sl0 up|down]");
    }
    static void wys_pad() {
        단말.Skryf("Destination Netmask Gateway Interface\n");
        skryf_adres(bord.Netwerk_stand(0,0)&bord.Netwerk_stand(1,0));단말.문자(' ');skryf_adres(bord.Netwerk_stand(1,0));단말.Skryf(bord.Netwerk_stand(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (bord.Netwerk_stand(2,0)!=0) {단말.Skryf("0.0.0.0 0.0.0.0 ");skryf_adres(bord.Netwerk_stand(2,0));단말.Skryf(bord.Netwerk_stand(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void wys_Netwerk() {
        단말.Skryf("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_kategorie=bord.Netwerk_stand(10,INDEX);if(TYPE_kategorie==0)continue;
            단말.Skryf(TYPE_kategorie==1?"TCP ":"UDP ");skryf_adres(bord.Netwerk_stand(16,INDEX));단말.문자(':');단말.수(bord.Netwerk_stand(11,INDEX));단말.문자(' ');
            skryf_adres(bord.Netwerk_stand(12,INDEX));단말.문자(':');단말.수(bord.Netwerk_stand(13,INDEX));단말.문자(' ');
            int stand_VALUE=bord.Netwerk_stand(14,INDEX);단말.Skryf(TYPE_kategorie==2?"DATAGRAM":stand_VALUE==1?"LISTEN":stand_VALUE==2?"ESTABLISHED":stand_VALUE==3?"CLOSE_WAIT":stand_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(bord.Netwerk_stand(15,INDEX));단말.문자(10);
        }
        단말.Skryf("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean wag_stand(int 밀리초) {
        int Loop=bord.밀리초();
        while(bord.밀리초()-Loop<밀리초) {
            if(셸입출력.대화가능()!=0){int karakter_VALUE=bord.직렬읽기();if(karakter_VALUE==3 || karakter_VALUE=='q' || karakter_VALUE=='Q' || karakter_VALUE==27 || karakter_VALUE==-4096)return false;}
            bord.YIELD_SVE();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, teiken=-1;
        for(int plaas_INDEX=1;plaas_INDEX<item_COUNT();plaas_INDEX++) {
            if(같음(plaas_INDEX,"-c")){횟수=syfer_VALUE(++plaas_INDEX,100);if(횟수<1){faling_VALUE("ping: -c 1..100");return;}}
            else if(같음(plaas_INDEX,"-W")){제한=syfer_VALUE(++plaas_INDEX,10);if(제한<1){faling_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(teiken<0)teiken=plaas_INDEX;else{faling_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(teiken<0 || !주소읽기(teiken)){faling_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int adres=adres_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Skryf("PING ");skryf_adres(adres);단말.Skryf(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int volgorde_VALUE=1;volgorde_VALUE<=횟수 && 계속;volgorde_VALUE++) {
            int 처리값=bord.응답보내기(adres,volgorde_VALUE);
            if(처리값<0){Fout(처리값);break;}보낸수++;
            int Loop=bord.밀리초();
            while(bord.응답읽기(0)==-11 && bord.밀리초()-Loop<제한)if(!wag_stand(1)){계속=false;break;}
            if(!계속)break;
            if(bord.응답읽기(0)==0){
                int tyd_VALUE=bord.응답읽기(1);RECEIVED_COUNT++;누적+=tyd_VALUE;if(tyd_VALUE<최솟값)최솟값=tyd_VALUE;if(tyd_VALUE>최댓값)최댓값=tyd_VALUE;
                단말.Skryf("32 bytes from ");skryf_adres(adres);단말.Skryf(" seq=");단말.수(volgorde_VALUE);단말.Skryf(" ttl=");단말.수(bord.응답읽기(2));단말.Skryf(" time=");단말.수(tyd_VALUE);단말.Skryf(" ms\n");
            }else{단말.Skryf("Request timeout seq=");단말.수(volgorde_VALUE);단말.문자(10);}
            if(volgorde_VALUE<횟수)계속=wag_stand(200);
        }
        단말.수(보낸수);단말.Skryf(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Skryf(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Skryf("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Skryf("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Skryf(" ms\n");}
        명령해석기.maatreël=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void wys_Aktiwiteit() { 단말.Skryf("up ");단말.수(bord.밀리초()/1000);단말.Skryf(" seconds\n"); }
    static void wys_Geheue() {
        수항목("ARM RAM KiB (firmware): ",bord.navraag_stelsel(0,0));
        수항목("Kernel image+BSS+stack KiB: ",bord.navraag_stelsel(1,0));
        int 총량=bord.navraag_stelsel(2,0), 사용량=bord.navraag_stelsel(3,0);
        단말.Skryf("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",bord.navraag_stelsel(4,0));
        수항목("EL0 arena+session reserve KiB: ",bord.navraag_stelsel(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=bord.navraag_stelsel(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Skryf("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void wys_Tasks() {
        단말.Skryf("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Skryf("1 - RUN - - ");단말.수(bord.밀리초());단말.Skryf(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(bord.taak_stand(INDEX)>0){단말.수(INDEX+1);단말.Skryf(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int stand_VALUE=bord.navraag_stelsel(20,INDEX);if(stand_VALUE==0)continue;
            단말.수(bord.navraag_stelsel(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Skryf(stand_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(bord.navraag_stelsel(22,INDEX));단말.문자(' ');단말.수(bord.navraag_stelsel(24,INDEX));단말.문자(' ');단말.수(bord.navraag_stelsel(23,INDEX));단말.문자(' ');
            for(int plaas_INDEX=0;plaas_INDEX<288;plaas_INDEX++){int greep_VALUE=bord.navraag_stelsel(25,INDEX+plaas_INDEX*4);if(greep_VALUE==0)break;bord.직렬쓰기(greep_VALUE);}단말.문자(10);
        }
    }
    static void wys_Berging() {
        int gleuf_COUNT=0, data_COUNT=0;
        for(int INDEX=0;INDEX<Geheue_Lêers.lêer_COUNT;INDEX++)if(Geheue_Lêers.이름길이[INDEX]>0 || Geheue_Lêers.Naslaan_COUNT[INDEX]>0){gleuf_COUNT++;data_COUNT+=Geheue_Lêers.lengte_VALUE[INDEX];}
        단말.Skryf("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Geheue_Lêers.lêer_COUNT*16384);단말.문자(' ');단말.수(gleuf_COUNT*16384);단말.문자(' ');단말.수((Geheue_Lêers.lêer_COUNT-gleuf_COUNT)*16384);단말.문자(' ');단말.수(data_COUNT);단말.문자(' ');단말.수(gleuf_COUNT);단말.문자('/');단말.수(Geheue_Lêers.lêer_COUNT);단말.Skryf(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void wys_stand_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(item_COUNT()>1){if(item_COUNT()!=3 || !같음(1,"-n") || (횟수=syfer_VALUE(2,1000))<1){faling_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 gaan_uit_program");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Skryf("\u001b[2J\u001b[H");
            wys_Aktiwiteit();wys_Geheue();wys_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!wag_stand(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void wys_hulp() {
        단말.Skryf("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Skryf(표준말(INDEX));단말.Skryf(" / ");단말.Skryf(관리명령.Word_SMS(INDEX));단말.Skryf(" : ");단말.Skryf(관리명령.설명(INDEX));단말.문자(10);}
        단말.Skryf("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Skryf("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Skryf("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean uitvoer_bevel() {
        int Opdrag=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Opdrag=INDEX;
        if(같음(0,"ifconfig"))Opdrag=0;if(같음(0,"ss"))Opdrag=4;
        if(Opdrag<0)return false;
        if(Opdrag==11){if(같음(1,"net") || 같음(1,"system"))wys_hulp();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.wys_hulp();return true;}
        if(Opdrag==0 || Opdrag==1)Netwerk_bevel(Opdrag==1);
        else if(Opdrag==2)응답시험();
        else if(Opdrag==6)wys_stand_bf9821b5();
        else if(item_COUNT()!=1){faling_VALUE("This command takes no arguments; help system");}
        else if(Opdrag==3)wys_pad();else if(Opdrag==4)wys_Netwerk();else if(Opdrag==5)wys_Tasks();else if(Opdrag==7)wys_Geheue();else if(Opdrag==8)wys_Berging();else if(Opdrag==9)wys_Aktiwiteit();
        else if(Opdrag==10)bord.전원끄기();
        return true;
    }
}
