// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tényleges_adat kernel_ÉRTÉK 상태를 읽는 IPv4·ICMP·작업·Memória_ÉRTÉK·RAM adattár_gyök 관리 Parancs. */
public final class Rendszer_eszköz {
    static int CÍM_ÉRTÉK;
    static boolean 같음(int INDEX, String szó_SMS) { return 명령해석기.같음(INDEX, szó_SMS); }
    static int cikk_DARAB() { return 명령해석기.kód_DARAB; }
    static void hiba_ÉRTÉK(String fontos_fájl_eb81d7d9) { 명령해석기.KR=2; 단말.Írás(fontos_fájl_eb81d7d9); 단말.문자(10); }
    static void HIBA(int ÉRTÉK) { 명령해석기.HIBA(ÉRTÉK); }
    static void szám_bejegyzés(String Név, int ÉRTÉK) { 단말.Írás(Név); 단말.szám(ÉRTÉK); 단말.문자(10); }
    static int számjegy_ÉRTÉK(int INDEX, int 한도) {
        if (INDEX>=cikk_DARAB() || 명령해석기.hossz_ÉRTÉK[INDEX]==0) return -1;
        int ÉRTÉK=0;
        for (int 순번=0; 순번<명령해석기.hossz_ÉRTÉK[INDEX]; 순번++) {
            int karakter_ÉRTÉK=명령해석기.kód_ÉRTÉK[명령해석기.시작점[INDEX]+순번]-'0';
            if (karakter_ÉRTÉK<0 || karakter_ÉRTÉK>9 || ÉRTÉK>(한도-karakter_ÉRTÉK)/10) return -1;
            ÉRTÉK=ÉRTÉK*10+karakter_ÉRTÉK;
        }
        return ÉRTÉK<=한도?ÉRTÉK:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=cikk_DARAB()) return false;
        int ÉRTÉK=0, adatrészlet_ÉRTÉK=0, számjegy_DARAB=0, pont_DARAB=0;
        for (int 순번=0; 순번<명령해석기.hossz_ÉRTÉK[INDEX]; 순번++) {
            int karakter_ÉRTÉK=명령해석기.kód_ÉRTÉK[명령해석기.시작점[INDEX]+순번];
            if (karakter_ÉRTÉK=='.') { if (számjegy_DARAB==0 || ++pont_DARAB>3) return false; ÉRTÉK=(ÉRTÉK<<8)|adatrészlet_ÉRTÉK; adatrészlet_ÉRTÉK=számjegy_DARAB=0; }
            else { if (karakter_ÉRTÉK<'0' || karakter_ÉRTÉK>'9' || ++számjegy_DARAB>3) return false; adatrészlet_ÉRTÉK=adatrészlet_ÉRTÉK*10+karakter_ÉRTÉK-'0'; if(adatrészlet_ÉRTÉK>255)return false; }
        }
        if (pont_DARAB!=3 || számjegy_DARAB==0) return false;
        CÍM_ÉRTÉK=(ÉRTÉK<<8)|adatrészlet_ÉRTÉK; return true;
    }
    static void ír_CÍM(int ÉRTÉK) {
        단말.szám((ÉRTÉK>>>24)&255); 단말.문자('.'); 단말.szám((ÉRTÉK>>>16)&255); 단말.문자('.');
        단말.szám((ÉRTÉK>>>8)&255); 단말.문자('.'); 단말.szám(ÉRTÉK&255);
    }
    static void bemutató_hálózat_állapot() {
        단말.Írás(fal.hálózat_állapot(20,0)!=0?"en0: ":"sl0: "); 단말.Írás(fal.hálózat_állapot(3,0)!=0?"UP":"DOWN");
        단말.Írás(fal.hálózat_állapot(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Írás(fal.hálózat_állapot(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); ír_CÍM(fal.hálózat_állapot(0,0));
        단말.Írás(" netmask "); ír_CÍM(fal.hálózat_állapot(1,0)); 단말.Írás(" gateway "); ír_CÍM(fal.hálózat_állapot(2,0)); 단말.문자(10);
        단말.Írás("  RX packets "); 단말.szám(fal.hálózat_állapot(4,0)); 단말.Írás(" bytes "); 단말.szám(fal.hálózat_állapot(6,0));
        단말.Írás(" TX packets "); 단말.szám(fal.hálózat_állapot(5,0)); 단말.Írás(" bytes "); 단말.szám(fal.hálózat_állapot(7,0)); 단말.문자(10);
        szám_bejegyzés("  dropped ",fal.hálózat_állapot(8,0));
    }
    static void halmaz_CÍM(int Futtatás) {
        if (cikk_DARAB()!=Futtatás+3 || !주소읽기(Futtatás)) { hiba_ÉRTÉK("사용법: ipconfig set CÍM 주소가림 átjáró_ÉRTÉK"); return; }
        int CÍM=CÍM_ÉRTÉK;
        if(!주소읽기(Futtatás+1)){hiba_ÉRTÉK("Invalid IPv4 netmask");return;} int maszk_ÉRTÉK=CÍM_ÉRTÉK;
        if(!주소읽기(Futtatás+2)){hiba_ÉRTÉK("Invalid IPv4 gateway");return;}
        int KR=fal.hálózat_Gépház(0,CÍM,maszk_ÉRTÉK,CÍM_ÉRTÉK);
        if(KR<0) { HIBA(KR); if(KR==-16)단말.Írás("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Írás("IPv4 configuration applied (until reboot)\n"); bemutató_hálózat_állapot(); }
    }
    static void hálózat_parancs(boolean IP_cím) {
        if (cikk_DARAB()==1 || cikk_DARAB()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || cikk_DARAB()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { bemutató_hálózat_állapot();return; }
        if (IP_cím && 같음(1,"route") && (cikk_DARAB()==2 || cikk_DARAB()==3&&같음(2,"show"))) { bemutató_útvonal();return; }
        if (같음(1,"set")) { halmaz_CÍM(2);return; }
        if (cikk_DARAB()==2 && (같음(1,"up") || 같음(1,"down"))) { fal.hálózat_Gépház(같음(1,"up")?1:2,0,0,0);bemutató_hálózat_állapot();return; }
        if (IP_cím && cikk_DARAB()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { fal.hálózat_Gépház(같음(5,"up")?1:2,0,0,0);bemutató_hálózat_állapot();return; }
        hiba_ÉRTÉK("사용법: ip [addr show|route show|set CÍM 주소가림 átjáró_ÉRTÉK|link set dev sl0 up|down]");
    }
    static void bemutató_útvonal() {
        단말.Írás("Destination Netmask Gateway Interface\n");
        ír_CÍM(fal.hálózat_állapot(0,0)&fal.hálózat_állapot(1,0));단말.문자(' ');ír_CÍM(fal.hálózat_állapot(1,0));단말.Írás(fal.hálózat_állapot(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (fal.hálózat_állapot(2,0)!=0) {단말.Írás("0.0.0.0 0.0.0.0 ");ír_CÍM(fal.hálózat_állapot(2,0));단말.Írás(fal.hálózat_állapot(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void bemutató_hálózat() {
        단말.Írás("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int beír_terület=fal.hálózat_állapot(10,INDEX);if(beír_terület==0)continue;
            단말.Írás(beír_terület==1?"TCP ":"UDP ");ír_CÍM(fal.hálózat_állapot(16,INDEX));단말.문자(':');단말.szám(fal.hálózat_állapot(11,INDEX));단말.문자(' ');
            ír_CÍM(fal.hálózat_állapot(12,INDEX));단말.문자(':');단말.szám(fal.hálózat_állapot(13,INDEX));단말.문자(' ');
            int Állapot_ÉRTÉK=fal.hálózat_állapot(14,INDEX);단말.Írás(beír_terület==2?"DATAGRAM":Állapot_ÉRTÉK==1?"LISTEN":Állapot_ÉRTÉK==2?"ESTABLISHED":Állapot_ÉRTÉK==3?"CLOSE_WAIT":Állapot_ÉRTÉK==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.szám(fal.hálózat_állapot(15,INDEX));단말.문자(10);
        }
        단말.Írás("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean várakozóállapot(int 밀리초) {
        int Futtatás=fal.밀리초();
        while(fal.밀리초()-Futtatás<밀리초) {
            if(셸입출력.informatikai_részleg_interaktív()!=0){int karakter_ÉRTÉK=fal.직렬읽기();if(karakter_ÉRTÉK==3 || karakter_ÉRTÉK=='q' || karakter_ÉRTÉK=='Q' || karakter_ÉRTÉK==27 || karakter_ÉRTÉK==-4096)return false;}
            fal.HOZAM_CPU();
        }
        return true;
    }
    static void teszt_válasz() {
        int 횟수=4, 제한=1000, cél=-1;
        for(int helyzetindex=1;helyzetindex<cikk_DARAB();helyzetindex++) {
            if(같음(helyzetindex,"-c")){횟수=számjegy_ÉRTÉK(++helyzetindex,100);if(횟수<1){hiba_ÉRTÉK("ping: -c 1..100");return;}}
            else if(같음(helyzetindex,"-W")){제한=számjegy_ÉRTÉK(++helyzetindex,10);if(제한<1){hiba_ÉRTÉK("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(cél<0)cél=helyzetindex;else{hiba_ÉRTÉK("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(cél<0 || !주소읽기(cél)){hiba_ÉRTÉK("ping: an IPv4 address is required (DNS is not configured)");return;}
        int CÍM=CÍM_ÉRTÉK, 보낸수=0, KAPOTT_DARAB=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Írás("PING ");ír_CÍM(CÍM);단말.Írás(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int rendel_ÉRTÉK=1;rendel_ÉRTÉK<=횟수 && 계속;rendel_ÉRTÉK++) {
            int 처리값=fal.küld_válasz(CÍM,rendel_ÉRTÉK);
            if(처리값<0){HIBA(처리값);break;}보낸수++;
            int Futtatás=fal.밀리초();
            while(fal.응답읽기(0)==-11 && fal.밀리초()-Futtatás<제한)if(!várakozóállapot(1)){계속=false;break;}
            if(!계속)break;
            if(fal.응답읽기(0)==0){
                int IDŐ_ÉRTÉK=fal.응답읽기(1);KAPOTT_DARAB++;누적+=IDŐ_ÉRTÉK;if(IDŐ_ÉRTÉK<최솟값)최솟값=IDŐ_ÉRTÉK;if(IDŐ_ÉRTÉK>최댓값)최댓값=IDŐ_ÉRTÉK;
                단말.Írás("32 bytes from ");ír_CÍM(CÍM);단말.Írás(" seq=");단말.szám(rendel_ÉRTÉK);단말.Írás(" ttl=");단말.szám(fal.응답읽기(2));단말.Írás(" time=");단말.szám(IDŐ_ÉRTÉK);단말.Írás(" ms\n");
            }else{단말.Írás("Request timeout seq=");단말.szám(rendel_ÉRTÉK);단말.문자(10);}
            if(rendel_ÉRTÉK<횟수)계속=várakozóállapot(200);
        }
        단말.szám(보낸수);단말.Írás(" transmitted, ");단말.szám(KAPOTT_DARAB);단말.Írás(" received, ");단말.szám(보낸수==0?100:(보낸수-KAPOTT_DARAB)*100/보낸수);단말.Írás("% packet loss\n");
        if(KAPOTT_DARAB>0){단말.Írás("rtt min/avg/max = ");단말.szám(최솟값);단말.문자('/');단말.szám(누적/KAPOTT_DARAB);단말.문자('/');단말.szám(최댓값);단말.Írás(" ms\n");}
        명령해석기.KR=계속?(KAPOTT_DARAB==0?1:0):130;
    }
    static void bemutató_Tevékenység() { 단말.Írás("up ");단말.szám(fal.밀리초()/1000);단말.Írás(" seconds\n"); }
    static void bemutató_Memória() {
        szám_bejegyzés("ARM RAM KiB (firmware): ",fal.lekérdez_Rendszer(0,0));
        szám_bejegyzés("Kernel image+BSS+stack KiB: ",fal.lekérdez_Rendszer(1,0));
        int összesen_kapacitás=fal.lekérdez_Rendszer(2,0), 사용량=fal.lekérdez_Rendszer(3,0);
        단말.Írás("AOT heap KiB total/used/free: ");단말.szám(összesen_kapacitás);단말.문자('/');단말.szám(사용량);단말.문자('/');단말.szám(összesen_kapacitás-사용량);단말.문자(10);
        szám_bejegyzés("Framebuffer KiB: ",fal.lekérdez_Rendszer(4,0));
        szám_bejegyzés("EL0 arena+session reserve KiB: ",fal.lekérdez_Rendszer(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=fal.lekérdez_Rendszer(22,INDEX);
        szám_bejegyzés("EL0 mapped KiB: ",매핑);
        단말.Írás("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void bemutató_Tasks() {
        단말.Írás("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Írás("1 - RUN - - ");단말.szám(fal.밀리초());단말.Írás(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(fal.teendő_Állapot(INDEX)>0){단말.szám(INDEX+1);단말.Írás(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Állapot_ÉRTÉK=fal.lekérdez_Rendszer(20,INDEX);if(Állapot_ÉRTÉK==0)continue;
            단말.szám(fal.lekérdez_Rendszer(21,INDEX));단말.문자(' ');단말.szám(INDEX);단말.Írás(Állapot_ÉRTÉK==1?" RUN ":" SUSPENDED ");
            단말.szám(fal.lekérdez_Rendszer(22,INDEX));단말.문자(' ');단말.szám(fal.lekérdez_Rendszer(24,INDEX));단말.문자(' ');단말.szám(fal.lekérdez_Rendszer(23,INDEX));단말.문자(' ');
            for(int helyzetindex=0;helyzetindex<288;helyzetindex++){int bájt_ÉRTÉK=fal.lekérdez_Rendszer(25,INDEX+helyzetindex*4);if(bájt_ÉRTÉK==0)break;fal.직렬쓰기(bájt_ÉRTÉK);}단말.문자(10);
        }
    }
    static void bemutató_tár() {
        int tárolóhely_DARAB=0, adat_DARAB=0;
        for(int INDEX=0;INDEX<Memória_Files.Fájl_DARAB;INDEX++)if(Memória_Files.이름길이[INDEX]>0 || Memória_Files.hivatkozik_DARAB[INDEX]>0){tárolóhely_DARAB++;adat_DARAB+=Memória_Files.hossz_ÉRTÉK[INDEX];}
        단말.Írás("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.szám(Memória_Files.Fájl_DARAB*16384);단말.문자(' ');단말.szám(tárolóhely_DARAB*16384);단말.문자(' ');단말.szám((Memória_Files.Fájl_DARAB-tárolóhely_DARAB)*16384);단말.문자(' ');단말.szám(adat_DARAB);단말.문자(' ');단말.szám(tárolóhely_DARAB);단말.문자('/');단말.szám(Memória_Files.Fájl_DARAB);단말.Írás(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void bemutató_állapot() {
        int 횟수=셸입출력.informatikai_részleg_interaktív()!=0?0:1;
        if(cikk_DARAB()>1){if(cikk_DARAB()!=3 || !같음(1,"-n") || (횟수=számjegy_ÉRTÉK(2,1000))<1){hiba_ÉRTÉK("사용법: top [-n 1..1000]; q/Ctrl+C로 kilépés_app");return;}}
        for(int szekvencia_ÉRTÉK=0;횟수==0 || szekvencia_ÉRTÉK<횟수;szekvencia_ÉRTÉK++){
            if(셸입출력.informatikai_részleg_interaktív()!=0 && 횟수==0)단말.Írás("\u001b[2J\u001b[H");
            bemutató_Tevékenység();bemutató_Memória();bemutató_Tasks();
            if(횟수!=0 && szekvencia_ÉRTÉK+1>=횟수)break;
            if(!várakozóállapot(1000))break;
        }
    }
    static String Standard_szó(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void bemutató_súgó() {
        단말.Írás("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Írás(Standard_szó(INDEX));단말.Írás(" / ");단말.Írás(관리명령.szó_SMS(INDEX));단말.Írás(" : ");단말.Írás(관리명령.설명(INDEX));단말.문자(10);}
        단말.Írás("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Írás("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Írás("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean végrehajt_parancs() {
        int Parancs=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,Standard_szó(INDEX)) || 같음(0,관리명령.szó_SMS(INDEX)))Parancs=INDEX;
        if(같음(0,"ifconfig"))Parancs=0;if(같음(0,"ss"))Parancs=4;
        if(Parancs<0)return false;
        if(Parancs==11){if(같음(1,"net") || 같음(1,"system"))bemutató_súgó();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.bemutató_súgó();return true;}
        if(Parancs==0 || Parancs==1)hálózat_parancs(Parancs==1);
        else if(Parancs==2)teszt_válasz();
        else if(Parancs==6)bemutató_állapot();
        else if(cikk_DARAB()!=1){hiba_ÉRTÉK("This command takes no arguments; help system");}
        else if(Parancs==3)bemutató_útvonal();else if(Parancs==4)bemutató_hálózat();else if(Parancs==5)bemutató_Tasks();else if(Parancs==7)bemutató_Memória();else if(Parancs==8)bemutató_tár();else if(Parancs==9)bemutató_Tevékenység();
        else if(Parancs==10)fal.전원끄기();
        return true;
    }
}
