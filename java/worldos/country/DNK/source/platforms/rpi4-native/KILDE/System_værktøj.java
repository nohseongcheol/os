// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktisk_data kerne_VÆRDI 상태를 읽는 IPv4·ICMP·작업·Hukommelse_VÆRDI·RAM lager_rod 관리 Kommando. */
public final class System_værktøj {
    static int mail_VÆRDI;
    static boolean 같음(int INDEKS, String Ord_sms) { return 명령해석기.같음(INDEKS, Ord_sms); }
    static int vare_TÆL() { return 명령해석기.token_TÆL; }
    static void fejl_VÆRDI(String Vigtigt_eb81d7d9) { 명령해석기.KR=2; 단말.Skrive(Vigtigt_eb81d7d9); 단말.문자(10); }
    static void fejl(int VÆRDI) { 명령해석기.fejl(VÆRDI); }
    static void tal_post(String Navn, int VÆRDI) { 단말.Skrive(Navn); 단말.tal(VÆRDI); 단말.문자(10); }
    static int ciffer_VÆRDI(int INDEKS, int 한도) {
        if (INDEKS>=vare_TÆL() || 명령해석기.varighed_VÆRDI[INDEKS]==0) return -1;
        int VÆRDI=0;
        for (int 순번=0; 순번<명령해석기.varighed_VÆRDI[INDEKS]; 순번++) {
            int tegn_VÆRDI=명령해석기.token_VÆRDI[명령해석기.시작점[INDEKS]+순번]-'0';
            if (tegn_VÆRDI<0 || tegn_VÆRDI>9 || VÆRDI>(한도-tegn_VÆRDI)/10) return -1;
            VÆRDI=VÆRDI*10+tegn_VÆRDI;
        }
        return VÆRDI<=한도?VÆRDI:-1;
    }
    static boolean 주소읽기(int INDEKS) {
        if (INDEKS>=vare_TÆL()) return false;
        int VÆRDI=0, del_VÆRDI=0, ciffer_TÆL=0, pege_TÆL=0;
        for (int 순번=0; 순번<명령해석기.varighed_VÆRDI[INDEKS]; 순번++) {
            int tegn_VÆRDI=명령해석기.token_VÆRDI[명령해석기.시작점[INDEKS]+순번];
            if (tegn_VÆRDI=='.') { if (ciffer_TÆL==0 || ++pege_TÆL>3) return false; VÆRDI=(VÆRDI<<8)|del_VÆRDI; del_VÆRDI=ciffer_TÆL=0; }
            else { if (tegn_VÆRDI<'0' || tegn_VÆRDI>'9' || ++ciffer_TÆL>3) return false; del_VÆRDI=del_VÆRDI*10+tegn_VÆRDI-'0'; if(del_VÆRDI>255)return false; }
        }
        if (pege_TÆL!=3 || ciffer_TÆL==0) return false;
        mail_VÆRDI=(VÆRDI<<8)|del_VÆRDI; return true;
    }
    static void skrive_mail(int VÆRDI) {
        단말.tal((VÆRDI>>>24)&255); 단말.문자('.'); 단말.tal((VÆRDI>>>16)&255); 단말.문자('.');
        단말.tal((VÆRDI>>>8)&255); 단말.문자('.'); 단말.tal(VÆRDI&255);
    }
    static void vise_netværk_status() {
        단말.Skrive(Tavle.netværk_status(20,0)!=0?"en0: ":"sl0: "); 단말.Skrive(Tavle.netværk_status(3,0)!=0?"UP":"DOWN");
        단말.Skrive(Tavle.netværk_status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Skrive(Tavle.netværk_status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); skrive_mail(Tavle.netværk_status(0,0));
        단말.Skrive(" netmask "); skrive_mail(Tavle.netværk_status(1,0)); 단말.Skrive(" gateway "); skrive_mail(Tavle.netværk_status(2,0)); 단말.문자(10);
        단말.Skrive("  RX packets "); 단말.tal(Tavle.netværk_status(4,0)); 단말.Skrive(" bytes "); 단말.tal(Tavle.netværk_status(6,0));
        단말.Skrive(" TX packets "); 단말.tal(Tavle.netværk_status(5,0)); 단말.Skrive(" bytes "); 단말.tal(Tavle.netværk_status(7,0)); 단말.문자(10);
        tal_post("  dropped ",Tavle.netværk_status(8,0));
    }
    static void sæt_mail(int Kør_2) {
        if (vare_TÆL()!=Kør_2+3 || !주소읽기(Kør_2)) { fejl_VÆRDI("사용법: ipconfig set mail 주소가림 gateway_VÆRDI"); return; }
        int mail=mail_VÆRDI;
        if(!주소읽기(Kør_2+1)){fejl_VÆRDI("Invalid IPv4 netmask");return;} int maske_VÆRDI=mail_VÆRDI;
        if(!주소읽기(Kør_2+2)){fejl_VÆRDI("Invalid IPv4 gateway");return;}
        int KR=Tavle.netværk_Indstillinger(0,mail,maske_VÆRDI,mail_VÆRDI);
        if(KR<0) { fejl(KR); if(KR==-16)단말.Skrive("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Skrive("IPv4 configuration applied (until reboot)\n"); vise_netværk_status(); }
    }
    static void netværk_kommando(boolean IP_adresse) {
        if (vare_TÆL()==1 || vare_TÆL()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || vare_TÆL()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { vise_netværk_status();return; }
        if (IP_adresse && 같음(1,"route") && (vare_TÆL()==2 || vare_TÆL()==3&&같음(2,"show"))) { vise_sti();return; }
        if (같음(1,"set")) { sæt_mail(2);return; }
        if (vare_TÆL()==2 && (같음(1,"up") || 같음(1,"down"))) { Tavle.netværk_Indstillinger(같음(1,"up")?1:2,0,0,0);vise_netværk_status();return; }
        if (IP_adresse && vare_TÆL()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Tavle.netværk_Indstillinger(같음(5,"up")?1:2,0,0,0);vise_netværk_status();return; }
        fejl_VÆRDI("사용법: ip [addr show|route show|set mail 주소가림 gateway_VÆRDI|link set dev sl0 up|down]");
    }
    static void vise_sti() {
        단말.Skrive("Destination Netmask Gateway Interface\n");
        skrive_mail(Tavle.netværk_status(0,0)&Tavle.netværk_status(1,0));단말.문자(' ');skrive_mail(Tavle.netværk_status(1,0));단말.Skrive(Tavle.netværk_status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Tavle.netværk_status(2,0)!=0) {단말.Skrive("0.0.0.0 0.0.0.0 ");skrive_mail(Tavle.netværk_status(2,0));단말.Skrive(Tavle.netværk_status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void vise_netværk() {
        단말.Skrive("Proto Local Remote State Queued\n");
        for(int INDEKS=0;INDEKS<32;INDEKS++) {
            int Type_område=Tavle.netværk_status(10,INDEKS);if(Type_område==0)continue;
            단말.Skrive(Type_område==1?"TCP ":"UDP ");skrive_mail(Tavle.netværk_status(16,INDEKS));단말.문자(':');단말.tal(Tavle.netværk_status(11,INDEKS));단말.문자(' ');
            skrive_mail(Tavle.netværk_status(12,INDEKS));단말.문자(':');단말.tal(Tavle.netværk_status(13,INDEKS));단말.문자(' ');
            int status_VÆRDI=Tavle.netværk_status(14,INDEKS);단말.Skrive(Type_område==2?"DATAGRAM":status_VÆRDI==1?"LISTEN":status_VÆRDI==2?"ESTABLISHED":status_VÆRDI==3?"CLOSE_WAIT":status_VÆRDI==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.tal(Tavle.netværk_status(15,INDEKS));단말.문자(10);
        }
        단말.Skrive("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean ventetilstand(int 밀리초) {
        int Kør_2=Tavle.밀리초();
        while(Tavle.밀리초()-Kør_2<밀리초) {
            if(셸입출력.it_interaktiv()!=0){int tegn_VÆRDI=Tavle.직렬읽기();if(tegn_VÆRDI==3 || tegn_VÆRDI=='q' || tegn_VÆRDI=='Q' || tegn_VÆRDI==27 || tegn_VÆRDI==-4096)return false;}
            Tavle.AFKAST_CPU();
        }
        return true;
    }
    static void test_svar() {
        int gentagelse_TÆL=4, 제한=1000, mål=-1;
        for(int positionsindeks=1;positionsindeks<vare_TÆL();positionsindeks++) {
            if(같음(positionsindeks,"-c")){gentagelse_TÆL=ciffer_VÆRDI(++positionsindeks,100);if(gentagelse_TÆL<1){fejl_VÆRDI("ping: -c 1..100");return;}}
            else if(같음(positionsindeks,"-W")){제한=ciffer_VÆRDI(++positionsindeks,10);if(제한<1){fejl_VÆRDI("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(mål<0)mål=positionsindeks;else{fejl_VÆRDI("사용법: ping [-c gentagelse_TÆL] [-W 초] IPv4");return;}
        }
        if(mål<0 || !주소읽기(mål)){fejl_VÆRDI("ping: an IPv4 address is required (DNS is not configured)");return;}
        int mail=mail_VÆRDI, 보낸수=0, MODTAGET_VED_UDLØB_TÆL=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Skrive("PING ");skrive_mail(mail);단말.Skrive(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ordre_VÆRDI=1;ordre_VÆRDI<=gentagelse_TÆL && 계속;ordre_VÆRDI++) {
            int 처리값=Tavle.maile_svar(mail,ordre_VÆRDI);
            if(처리값<0){fejl(처리값);break;}보낸수++;
            int Kør_2=Tavle.밀리초();
            while(Tavle.응답읽기(0)==-11 && Tavle.밀리초()-Kør_2<제한)if(!ventetilstand(1)){계속=false;break;}
            if(!계속)break;
            if(Tavle.응답읽기(0)==0){
                int TID_VÆRDI=Tavle.응답읽기(1);MODTAGET_VED_UDLØB_TÆL++;누적+=TID_VÆRDI;if(TID_VÆRDI<최솟값)최솟값=TID_VÆRDI;if(TID_VÆRDI>최댓값)최댓값=TID_VÆRDI;
                단말.Skrive("32 bytes from ");skrive_mail(mail);단말.Skrive(" seq=");단말.tal(ordre_VÆRDI);단말.Skrive(" ttl=");단말.tal(Tavle.응답읽기(2));단말.Skrive(" time=");단말.tal(TID_VÆRDI);단말.Skrive(" ms\n");
            }else{단말.Skrive("Request timeout seq=");단말.tal(ordre_VÆRDI);단말.문자(10);}
            if(ordre_VÆRDI<gentagelse_TÆL)계속=ventetilstand(200);
        }
        단말.tal(보낸수);단말.Skrive(" transmitted, ");단말.tal(MODTAGET_VED_UDLØB_TÆL);단말.Skrive(" received, ");단말.tal(보낸수==0?100:(보낸수-MODTAGET_VED_UDLØB_TÆL)*100/보낸수);단말.Skrive("% packet loss\n");
        if(MODTAGET_VED_UDLØB_TÆL>0){단말.Skrive("rtt min/avg/max = ");단말.tal(최솟값);단말.문자('/');단말.tal(누적/MODTAGET_VED_UDLØB_TÆL);단말.문자('/');단말.tal(최댓값);단말.Skrive(" ms\n");}
        명령해석기.KR=계속?(MODTAGET_VED_UDLØB_TÆL==0?1:0):130;
    }
    static void vise_Aktivitet() { 단말.Skrive("up ");단말.tal(Tavle.밀리초()/1000);단말.Skrive(" seconds\n"); }
    static void vise_Hukommelse() {
        tal_post("ARM RAM KiB (firmware): ",Tavle.forespørge_System(0,0));
        tal_post("Kernel image+BSS+stack KiB: ",Tavle.forespørge_System(1,0));
        int i_alt_kapacitet=Tavle.forespørge_System(2,0), 사용량=Tavle.forespørge_System(3,0);
        단말.Skrive("AOT heap KiB total/used/free: ");단말.tal(i_alt_kapacitet);단말.문자('/');단말.tal(사용량);단말.문자('/');단말.tal(i_alt_kapacitet-사용량);단말.문자(10);
        tal_post("Framebuffer KiB: ",Tavle.forespørge_System(4,0));
        tal_post("EL0 arena+session reserve KiB: ",Tavle.forespørge_System(5,0));
        int 매핑=0;for(int INDEKS=0;INDEKS<4;INDEKS++)매핑+=Tavle.forespørge_System(22,INDEKS);
        tal_post("EL0 mapped KiB: ",매핑);
        단말.Skrive("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void vise_Tasks() {
        단말.Skrive("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Skrive("1 - RUN - - ");단말.tal(Tavle.밀리초());단말.Skrive(" kernel/shell\n");
        for(int INDEKS=1;INDEKS<3;INDEKS++)if(Tavle.job_status(INDEKS)>0){단말.tal(INDEKS+1);단말.Skrive(" - READY 64 - - kernel-task\n");}
        for(int INDEKS=0;INDEKS<4;INDEKS++){
            int status_VÆRDI=Tavle.forespørge_System(20,INDEKS);if(status_VÆRDI==0)continue;
            단말.tal(Tavle.forespørge_System(21,INDEKS));단말.문자(' ');단말.tal(INDEKS);단말.Skrive(status_VÆRDI==1?" RUN ":" SUSPENDED ");
            단말.tal(Tavle.forespørge_System(22,INDEKS));단말.문자(' ');단말.tal(Tavle.forespørge_System(24,INDEKS));단말.문자(' ');단말.tal(Tavle.forespørge_System(23,INDEKS));단말.문자(' ');
            for(int positionsindeks=0;positionsindeks<288;positionsindeks++){int byte_VÆRDI=Tavle.forespørge_System(25,INDEKS+positionsindeks*4);if(byte_VÆRDI==0)break;Tavle.직렬쓰기(byte_VÆRDI);}단말.문자(10);
        }
    }
    static void vise_Lager() {
        int udvidelsesstik_TÆL=0, data_TÆL=0;
        for(int INDEKS=0;INDEKS<Hukommelse_Filer.fil_TÆL;INDEKS++)if(Hukommelse_Filer.이름길이[INDEKS]>0 || Hukommelse_Filer.referere_TÆL[INDEKS]>0){udvidelsesstik_TÆL++;data_TÆL+=Hukommelse_Filer.varighed_VÆRDI[INDEKS];}
        단말.Skrive("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.tal(Hukommelse_Filer.fil_TÆL*16384);단말.문자(' ');단말.tal(udvidelsesstik_TÆL*16384);단말.문자(' ');단말.tal((Hukommelse_Filer.fil_TÆL-udvidelsesstik_TÆL)*16384);단말.문자(' ');단말.tal(data_TÆL);단말.문자(' ');단말.tal(udvidelsesstik_TÆL);단말.문자('/');단말.tal(Hukommelse_Filer.fil_TÆL);단말.Skrive(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void vise_status_bf9821b5() {
        int gentagelse_TÆL=셸입출력.it_interaktiv()!=0?0:1;
        if(vare_TÆL()>1){if(vare_TÆL()!=3 || !같음(1,"-n") || (gentagelse_TÆL=ciffer_VÆRDI(2,1000))<1){fejl_VÆRDI("사용법: top [-n 1..1000]; q/Ctrl+C로 afslut_app");return;}}
        for(int SEKVENS_VÆRDI=0;gentagelse_TÆL==0 || SEKVENS_VÆRDI<gentagelse_TÆL;SEKVENS_VÆRDI++){
            if(셸입출력.it_interaktiv()!=0 && gentagelse_TÆL==0)단말.Skrive("\u001b[2J\u001b[H");
            vise_Aktivitet();vise_Hukommelse();vise_Tasks();
            if(gentagelse_TÆL!=0 && SEKVENS_VÆRDI+1>=gentagelse_TÆL)break;
            if(!ventetilstand(1000))break;
        }
    }
    static String Standard_Ord(int INDEKS) {
        if(INDEKS==0)return "ipconfig";if(INDEKS==1)return "ip";if(INDEKS==2)return "ping";if(INDEKS==3)return "route";if(INDEKS==4)return "netstat";
        if(INDEKS==5)return "ps";if(INDEKS==6)return "top";if(INDEKS==7)return "free";if(INDEKS==8)return "df";if(INDEKS==9)return "uptime";if(INDEKS==10)return "poweroff";return "help";
    }
    static void vise_hjælp() {
        단말.Skrive("--- Network / system commands ---\n");
        for(int INDEKS=0;INDEKS<12;INDEKS++){단말.Skrive(Standard_Ord(INDEKS));단말.Skrive(" / ");단말.Skrive(관리명령.Ord_sms(INDEKS));단말.Skrive(" : ");단말.Skrive(관리명령.설명(INDEKS));단말.문자(10);}
        단말.Skrive("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Skrive("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Skrive("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Udfør_kommando() {
        int Kommando=-1;
        for(int INDEKS=0;INDEKS<12;INDEKS++)if(같음(0,Standard_Ord(INDEKS)) || 같음(0,관리명령.Ord_sms(INDEKS)))Kommando=INDEKS;
        if(같음(0,"ifconfig"))Kommando=0;if(같음(0,"ss"))Kommando=4;
        if(Kommando<0)return false;
        if(Kommando==11){if(같음(1,"net") || 같음(1,"system"))vise_hjælp();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.vise_hjælp();return true;}
        if(Kommando==0 || Kommando==1)netværk_kommando(Kommando==1);
        else if(Kommando==2)test_svar();
        else if(Kommando==6)vise_status_bf9821b5();
        else if(vare_TÆL()!=1){fejl_VÆRDI("This command takes no arguments; help system");}
        else if(Kommando==3)vise_sti();else if(Kommando==4)vise_netværk();else if(Kommando==5)vise_Tasks();else if(Kommando==7)vise_Hukommelse();else if(Kommando==8)vise_Lager();else if(Kommando==9)vise_Aktivitet();
        else if(Kommando==10)Tavle.전원끄기();
        return true;
    }
}
