// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** aktual_të_dhëna bërthamë_VALUE 상태를 읽는 IPv4·ICMP·작업·Memorie_VALUE·RAM depo_rrënjë 관리 Komanda. */
public final class sistem_vegël {
    static int email_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int njësi_COUNT() { return 명령해석기.kodi_COUNT; }
    static void dështim_VALUE(String LEXOMË_eb81d7d9) { 명령해석기.llogaritje=2; 단말.Shkrimi(LEXOMË_eb81d7d9); 단말.문자(10); }
    static void GABIM(int VALUE) { 명령해석기.GABIM(VALUE); }
    static void 수항목(String Emër, int VALUE) { 단말.Shkrimi(Emër); 단말.수(VALUE); 단말.문자(10); }
    static int shifër_VALUE(int INDEX, int 한도) {
        if (INDEX>=njësi_COUNT() || 명령해석기.gjatësi_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.gjatësi_VALUE[INDEX]; 순번++) {
            int karakter_VALUE=명령해석기.kodi_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (karakter_VALUE<0 || karakter_VALUE>9 || VALUE>(한도-karakter_VALUE)/10) return -1;
            VALUE=VALUE*10+karakter_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=njësi_COUNT()) return false;
        int VALUE=0, 덩이=0, shifër_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.gjatësi_VALUE[INDEX]; 순번++) {
            int karakter_VALUE=명령해석기.kodi_VALUE[명령해석기.시작점[INDEX]+순번];
            if (karakter_VALUE=='.') { if (shifër_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=shifër_COUNT=0; }
            else { if (karakter_VALUE<'0' || karakter_VALUE>'9' || ++shifër_COUNT>3) return false; 덩이=덩이*10+karakter_VALUE-'0'; if(덩이>255)return false; }
        }
        if (p_COUNT!=3 || shifër_COUNT==0) return false;
        email_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void shkruaj_email(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void shfaq_rrjet_status() {
        단말.Shkrimi(panel.rrjet_status(20,0)!=0?"en0: ":"sl0: "); 단말.Shkrimi(panel.rrjet_status(3,0)!=0?"UP":"DOWN");
        단말.Shkrimi(panel.rrjet_status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Shkrimi(panel.rrjet_status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); shkruaj_email(panel.rrjet_status(0,0));
        단말.Shkrimi(" netmask "); shkruaj_email(panel.rrjet_status(1,0)); 단말.Shkrimi(" gateway "); shkruaj_email(panel.rrjet_status(2,0)); 단말.문자(10);
        단말.Shkrimi("  RX packets "); 단말.수(panel.rrjet_status(4,0)); 단말.Shkrimi(" bytes "); 단말.수(panel.rrjet_status(6,0));
        단말.Shkrimi(" TX packets "); 단말.수(panel.rrjet_status(5,0)); 단말.Shkrimi(" bytes "); 단말.수(panel.rrjet_status(7,0)); 단말.문자(10);
        수항목("  dropped ",panel.rrjet_status(8,0));
    }
    static void bashkësi_email(int Ekzekuto) {
        if (njësi_COUNT()!=Ekzekuto+3 || !주소읽기(Ekzekuto)) { dështim_VALUE("사용법: ipconfig set email 주소가림 portëkalimi_VALUE"); return; }
        int email=email_VALUE;
        if(!주소읽기(Ekzekuto+1)){dështim_VALUE("Invalid IPv4 netmask");return;} int maskë_VALUE=email_VALUE;
        if(!주소읽기(Ekzekuto+2)){dështim_VALUE("Invalid IPv4 gateway");return;}
        int llogaritje=panel.rrjet_cilësimet(0,email,maskë_VALUE,email_VALUE);
        if(llogaritje<0) { GABIM(llogaritje); if(llogaritje==-16)단말.Shkrimi("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Shkrimi("IPv4 configuration applied (until reboot)\n"); shfaq_rrjet_status(); }
    }
    static void rrjet_komandë(boolean Adresa_e_IP_së) {
        if (njësi_COUNT()==1 || njësi_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || njësi_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { shfaq_rrjet_status();return; }
        if (Adresa_e_IP_së && 같음(1,"route") && (njësi_COUNT()==2 || njësi_COUNT()==3&&같음(2,"show"))) { shfaq_shteg();return; }
        if (같음(1,"set")) { bashkësi_email(2);return; }
        if (njësi_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { panel.rrjet_cilësimet(같음(1,"up")?1:2,0,0,0);shfaq_rrjet_status();return; }
        if (Adresa_e_IP_së && njësi_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { panel.rrjet_cilësimet(같음(5,"up")?1:2,0,0,0);shfaq_rrjet_status();return; }
        dështim_VALUE("사용법: ip [addr show|route show|set email 주소가림 portëkalimi_VALUE|link set dev sl0 up|down]");
    }
    static void shfaq_shteg() {
        단말.Shkrimi("Destination Netmask Gateway Interface\n");
        shkruaj_email(panel.rrjet_status(0,0)&panel.rrjet_status(1,0));단말.문자(' ');shkruaj_email(panel.rrjet_status(1,0));단말.Shkrimi(panel.rrjet_status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (panel.rrjet_status(2,0)!=0) {단말.Shkrimi("0.0.0.0 0.0.0.0 ");shkruaj_email(panel.rrjet_status(2,0));단말.Shkrimi(panel.rrjet_status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void shfaq_rrjet() {
        단말.Shkrimi("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_kategori=panel.rrjet_status(10,INDEX);if(TYPE_kategori==0)continue;
            단말.Shkrimi(TYPE_kategori==1?"TCP ":"UDP ");shkruaj_email(panel.rrjet_status(16,INDEX));단말.문자(':');단말.수(panel.rrjet_status(11,INDEX));단말.문자(' ');
            shkruaj_email(panel.rrjet_status(12,INDEX));단말.문자(':');단말.수(panel.rrjet_status(13,INDEX));단말.문자(' ');
            int status_VALUE=panel.rrjet_status(14,INDEX);단말.Shkrimi(TYPE_kategori==2?"DATAGRAM":status_VALUE==1?"LISTEN":status_VALUE==2?"ESTABLISHED":status_VALUE==3?"CLOSE_WAIT":status_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(panel.rrjet_status(15,INDEX));단말.문자(10);
        }
        단말.Shkrimi("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean Prit_status(int 밀리초) {
        int Ekzekuto=panel.밀리초();
        while(panel.밀리초()-Ekzekuto<밀리초) {
            if(셸입출력.teknologjia_e_informacionit_ndërvepruese()!=0){int karakter_VALUE=panel.직렬읽기();if(karakter_VALUE==3 || karakter_VALUE=='q' || karakter_VALUE=='Q' || karakter_VALUE==27 || karakter_VALUE==-4096)return false;}
            panel.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, objektiv=-1;
        for(int pozicioni_INDEX=1;pozicioni_INDEX<njësi_COUNT();pozicioni_INDEX++) {
            if(같음(pozicioni_INDEX,"-c")){횟수=shifër_VALUE(++pozicioni_INDEX,100);if(횟수<1){dështim_VALUE("ping: -c 1..100");return;}}
            else if(같음(pozicioni_INDEX,"-W")){제한=shifër_VALUE(++pozicioni_INDEX,10);if(제한<1){dështim_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(objektiv<0)objektiv=pozicioni_INDEX;else{dështim_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(objektiv<0 || !주소읽기(objektiv)){dështim_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int email=email_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Shkrimi("PING ");shkruaj_email(email);단말.Shkrimi(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int renditja_VALUE=1;renditja_VALUE<=횟수 && 계속;renditja_VALUE++) {
            int 처리값=panel.dërgoj_përgjigje(email,renditja_VALUE);
            if(처리값<0){GABIM(처리값);break;}보낸수++;
            int Ekzekuto=panel.밀리초();
            while(panel.응답읽기(0)==-11 && panel.밀리초()-Ekzekuto<제한)if(!Prit_status(1)){계속=false;break;}
            if(!계속)break;
            if(panel.응답읽기(0)==0){
                int Ora_VALUE_4692cef5=panel.응답읽기(1);RECEIVED_COUNT++;누적+=Ora_VALUE_4692cef5;if(Ora_VALUE_4692cef5<최솟값)최솟값=Ora_VALUE_4692cef5;if(Ora_VALUE_4692cef5>최댓값)최댓값=Ora_VALUE_4692cef5;
                단말.Shkrimi("32 bytes from ");shkruaj_email(email);단말.Shkrimi(" seq=");단말.수(renditja_VALUE);단말.Shkrimi(" ttl=");단말.수(panel.응답읽기(2));단말.Shkrimi(" time=");단말.수(Ora_VALUE_4692cef5);단말.Shkrimi(" ms\n");
            }else{단말.Shkrimi("Request timeout seq=");단말.수(renditja_VALUE);단말.문자(10);}
            if(renditja_VALUE<횟수)계속=Prit_status(200);
        }
        단말.수(보낸수);단말.Shkrimi(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Shkrimi(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Shkrimi("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Shkrimi("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Shkrimi(" ms\n");}
        명령해석기.llogaritje=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void shfaq_Aktivitet() { 단말.Shkrimi("up ");단말.수(panel.밀리초()/1000);단말.Shkrimi(" seconds\n"); }
    static void shfaq_Memorie() {
        수항목("ARM RAM KiB (firmware): ",panel.pyetja_sistem(0,0));
        수항목("Kernel image+BSS+stack KiB: ",panel.pyetja_sistem(1,0));
        int 총량=panel.pyetja_sistem(2,0), 사용량=panel.pyetja_sistem(3,0);
        단말.Shkrimi("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",panel.pyetja_sistem(4,0));
        수항목("EL0 arena+session reserve KiB: ",panel.pyetja_sistem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=panel.pyetja_sistem(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Shkrimi("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void shfaq_Tasks() {
        단말.Shkrimi("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Shkrimi("1 - RUN - - ");단말.수(panel.밀리초());단말.Shkrimi(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(panel.detyrë_status(INDEX)>0){단말.수(INDEX+1);단말.Shkrimi(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int status_VALUE=panel.pyetja_sistem(20,INDEX);if(status_VALUE==0)continue;
            단말.수(panel.pyetja_sistem(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Shkrimi(status_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(panel.pyetja_sistem(22,INDEX));단말.문자(' ');단말.수(panel.pyetja_sistem(24,INDEX));단말.문자(' ');단말.수(panel.pyetja_sistem(23,INDEX));단말.문자(' ');
            for(int pozicioni_INDEX=0;pozicioni_INDEX<288;pozicioni_INDEX++){int bajt_VALUE=panel.pyetja_sistem(25,INDEX+pozicioni_INDEX*4);if(bajt_VALUE==0)break;panel.직렬쓰기(bajt_VALUE);}단말.문자(10);
        }
    }
    static void shfaq_hapësira_ruajtëse() {
        int hapësirë_për_tekst_COUNT=0, të_dhëna_COUNT=0;
        for(int INDEX=0;INDEX<Memorie_Skedarët.skedar_COUNT;INDEX++)if(Memorie_Skedarët.이름길이[INDEX]>0 || Memorie_Skedarët.Referencë_COUNT[INDEX]>0){hapësirë_për_tekst_COUNT++;të_dhëna_COUNT+=Memorie_Skedarët.gjatësi_VALUE[INDEX];}
        단말.Shkrimi("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memorie_Skedarët.skedar_COUNT*16384);단말.문자(' ');단말.수(hapësirë_për_tekst_COUNT*16384);단말.문자(' ');단말.수((Memorie_Skedarët.skedar_COUNT-hapësirë_për_tekst_COUNT)*16384);단말.문자(' ');단말.수(të_dhëna_COUNT);단말.문자(' ');단말.수(hapësirë_për_tekst_COUNT);단말.문자('/');단말.수(Memorie_Skedarët.skedar_COUNT);단말.Shkrimi(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void shfaq_status_bf9821b5() {
        int 횟수=셸입출력.teknologjia_e_informacionit_ndërvepruese()!=0?0:1;
        if(njësi_COUNT()>1){if(njësi_COUNT()!=3 || !같음(1,"-n") || (횟수=shifër_VALUE(2,1000))<1){dështim_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 mbyll_program");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.teknologjia_e_informacionit_ndërvepruese()!=0 && 횟수==0)단말.Shkrimi("\u001b[2J\u001b[H");
            shfaq_Aktivitet();shfaq_Memorie();shfaq_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!Prit_status(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void shfaq_ndihmë() {
        단말.Shkrimi("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Shkrimi(표준말(INDEX));단말.Shkrimi(" / ");단말.Shkrimi(관리명령.Word_SMS(INDEX));단말.Shkrimi(" : ");단말.Shkrimi(관리명령.설명(INDEX));단말.문자(10);}
        단말.Shkrimi("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Shkrimi("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Shkrimi("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean zbatoj_komandë() {
        int Komanda=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Komanda=INDEX;
        if(같음(0,"ifconfig"))Komanda=0;if(같음(0,"ss"))Komanda=4;
        if(Komanda<0)return false;
        if(Komanda==11){if(같음(1,"net") || 같음(1,"system"))shfaq_ndihmë();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.shfaq_ndihmë();return true;}
        if(Komanda==0 || Komanda==1)rrjet_komandë(Komanda==1);
        else if(Komanda==2)응답시험();
        else if(Komanda==6)shfaq_status_bf9821b5();
        else if(njësi_COUNT()!=1){dështim_VALUE("This command takes no arguments; help system");}
        else if(Komanda==3)shfaq_shteg();else if(Komanda==4)shfaq_rrjet();else if(Komanda==5)shfaq_Tasks();else if(Komanda==7)shfaq_Memorie();else if(Komanda==8)shfaq_hapësira_ruajtëse();else if(Komanda==9)shfaq_Aktivitet();
        else if(Komanda==10)panel.전원끄기();
        return true;
    }
}
