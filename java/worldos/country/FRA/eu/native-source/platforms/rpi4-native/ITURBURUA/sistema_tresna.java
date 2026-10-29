// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** benetako_datuak nukleo_balio 상태를 읽는 IPv4·ICMP·작업·Memoria_balio·RAM biltegi_erro 관리 Komandoa. */
public final class sistema_tresna {
    static int helbide_balio;
    static boolean 같음(int INDIZE, String Word_SMS) { return 명령해석기.같음(INDIZE, Word_SMS); }
    static int elementu_ZENBATU() { return 명령해석기.token_ZENBATU; }
    static void hutsegite_balio(String IRAKHAU_eb81d7d9) { 명령해석기.EMAITZA=2; 단말.Idatzi(IRAKHAU_eb81d7d9); 단말.문자(10); }
    static void errorea(int balio) { 명령해석기.errorea(balio); }
    static void 수항목(String Izena, int balio) { 단말.Idatzi(Izena); 단말.수(balio); 단말.문자(10); }
    static int digitu_balio(int INDIZE, int 한도) {
        if (INDIZE>=elementu_ZENBATU() || 명령해석기.luzera_balio[INDIZE]==0) return -1;
        int balio=0;
        for (int 순번=0; 순번<명령해석기.luzera_balio[INDIZE]; 순번++) {
            int karaktere_balio=명령해석기.token_balio[명령해석기.시작점[INDIZE]+순번]-'0';
            if (karaktere_balio<0 || karaktere_balio>9 || balio>(한도-karaktere_balio)/10) return -1;
            balio=balio*10+karaktere_balio;
        }
        return balio<=한도?balio:-1;
    }
    static boolean 주소읽기(int INDIZE) {
        if (INDIZE>=elementu_ZENBATU()) return false;
        int balio=0, 덩이=0, digitu_ZENBATU=0, p_ZENBATU=0;
        for (int 순번=0; 순번<명령해석기.luzera_balio[INDIZE]; 순번++) {
            int karaktere_balio=명령해석기.token_balio[명령해석기.시작점[INDIZE]+순번];
            if (karaktere_balio=='.') { if (digitu_ZENBATU==0 || ++p_ZENBATU>3) return false; balio=(balio<<8)|덩이; 덩이=digitu_ZENBATU=0; }
            else { if (karaktere_balio<'0' || karaktere_balio>'9' || ++digitu_ZENBATU>3) return false; 덩이=덩이*10+karaktere_balio-'0'; if(덩이>255)return false; }
        }
        if (p_ZENBATU!=3 || digitu_ZENBATU==0) return false;
        helbide_balio=(balio<<8)|덩이; return true;
    }
    static void idatzi_helbide(int balio) {
        단말.수((balio>>>24)&255); 단말.문자('.'); 단말.수((balio>>>16)&255); 단말.문자('.');
        단말.수((balio>>>8)&255); 단말.문자('.'); 단말.수(balio&255);
    }
    static void erakutsi_sare_egoera() {
        단말.Idatzi(arbel.sare_egoera(20,0)!=0?"en0: ":"sl0: "); 단말.Idatzi(arbel.sare_egoera(3,0)!=0?"UP":"DOWN");
        단말.Idatzi(arbel.sare_egoera(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Idatzi(arbel.sare_egoera(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); idatzi_helbide(arbel.sare_egoera(0,0));
        단말.Idatzi(" netmask "); idatzi_helbide(arbel.sare_egoera(1,0)); 단말.Idatzi(" gateway "); idatzi_helbide(arbel.sare_egoera(2,0)); 단말.문자(10);
        단말.Idatzi("  RX packets "); 단말.수(arbel.sare_egoera(4,0)); 단말.Idatzi(" bytes "); 단말.수(arbel.sare_egoera(6,0));
        단말.Idatzi(" TX packets "); 단말.수(arbel.sare_egoera(5,0)); 단말.Idatzi(" bytes "); 단말.수(arbel.sare_egoera(7,0)); 단말.문자(10);
        수항목("  dropped ",arbel.sare_egoera(8,0));
    }
    static void sorta_helbide(int Exekutatu_2) {
        if (elementu_ZENBATU()!=Exekutatu_2+3 || !주소읽기(Exekutatu_2)) { hutsegite_balio("사용법: ipconfig set helbide 주소가림 atebide_balio"); return; }
        int helbide=helbide_balio;
        if(!주소읽기(Exekutatu_2+1)){hutsegite_balio("Invalid IPv4 netmask");return;} int maskara_balio=helbide_balio;
        if(!주소읽기(Exekutatu_2+2)){hutsegite_balio("Invalid IPv4 gateway");return;}
        int EMAITZA=arbel.sare_Ezarpenak(0,helbide,maskara_balio,helbide_balio);
        if(EMAITZA<0) { errorea(EMAITZA); if(EMAITZA==-16)단말.Idatzi("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Idatzi("IPv4 configuration applied (until reboot)\n"); erakutsi_sare_egoera(); }
    }
    static void sare_komando(boolean IP_helbide) {
        if (elementu_ZENBATU()==1 || elementu_ZENBATU()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || elementu_ZENBATU()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { erakutsi_sare_egoera();return; }
        if (IP_helbide && 같음(1,"route") && (elementu_ZENBATU()==2 || elementu_ZENBATU()==3&&같음(2,"show"))) { erakutsi_bide_izen();return; }
        if (같음(1,"set")) { sorta_helbide(2);return; }
        if (elementu_ZENBATU()==2 && (같음(1,"up") || 같음(1,"down"))) { arbel.sare_Ezarpenak(같음(1,"up")?1:2,0,0,0);erakutsi_sare_egoera();return; }
        if (IP_helbide && elementu_ZENBATU()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { arbel.sare_Ezarpenak(같음(5,"up")?1:2,0,0,0);erakutsi_sare_egoera();return; }
        hutsegite_balio("사용법: ip [addr show|route show|set helbide 주소가림 atebide_balio|link set dev sl0 up|down]");
    }
    static void erakutsi_bide_izen() {
        단말.Idatzi("Destination Netmask Gateway Interface\n");
        idatzi_helbide(arbel.sare_egoera(0,0)&arbel.sare_egoera(1,0));단말.문자(' ');idatzi_helbide(arbel.sare_egoera(1,0));단말.Idatzi(arbel.sare_egoera(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (arbel.sare_egoera(2,0)!=0) {단말.Idatzi("0.0.0.0 0.0.0.0 ");idatzi_helbide(arbel.sare_egoera(2,0));단말.Idatzi(arbel.sare_egoera(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void erakutsi_sare() {
        단말.Idatzi("Proto Local Remote State Queued\n");
        for(int INDIZE=0;INDIZE<32;INDIZE++) {
            int MOTA_Kategoria=arbel.sare_egoera(10,INDIZE);if(MOTA_Kategoria==0)continue;
            단말.Idatzi(MOTA_Kategoria==1?"TCP ":"UDP ");idatzi_helbide(arbel.sare_egoera(16,INDIZE));단말.문자(':');단말.수(arbel.sare_egoera(11,INDIZE));단말.문자(' ');
            idatzi_helbide(arbel.sare_egoera(12,INDIZE));단말.문자(':');단말.수(arbel.sare_egoera(13,INDIZE));단말.문자(' ');
            int Egoera_balio=arbel.sare_egoera(14,INDIZE);단말.Idatzi(MOTA_Kategoria==2?"DATAGRAM":Egoera_balio==1?"LISTEN":Egoera_balio==2?"ESTABLISHED":Egoera_balio==3?"CLOSE_WAIT":Egoera_balio==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(arbel.sare_egoera(15,INDIZE));단말.문자(10);
        }
        단말.Idatzi("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean itxaron_Egoera(int 밀리초) {
        int Exekutatu_2=arbel.밀리초();
        while(arbel.밀리초()-Exekutatu_2<밀리초) {
            if(셸입출력.informatika_interaktibo()!=0){int karaktere_balio=arbel.직렬읽기();if(karaktere_balio==3 || karaktere_balio=='q' || karaktere_balio=='Q' || karaktere_balio==27 || karaktere_balio==-4096)return false;}
            arbel.YIELD_PUZ();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, helburu_balio=-1;
        for(int kargu_INDIZE=1;kargu_INDIZE<elementu_ZENBATU();kargu_INDIZE++) {
            if(같음(kargu_INDIZE,"-c")){횟수=digitu_balio(++kargu_INDIZE,100);if(횟수<1){hutsegite_balio("ping: -c 1..100");return;}}
            else if(같음(kargu_INDIZE,"-W")){제한=digitu_balio(++kargu_INDIZE,10);if(제한<1){hutsegite_balio("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(helburu_balio<0)helburu_balio=kargu_INDIZE;else{hutsegite_balio("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(helburu_balio<0 || !주소읽기(helburu_balio)){hutsegite_balio("ping: an IPv4 address is required (DNS is not configured)");return;}
        int helbide=helbide_balio, 보낸수=0, RECEIVED_ZENBATU=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Idatzi("PING ");idatzi_helbide(helbide);단말.Idatzi(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ordena_balio=1;ordena_balio<=횟수 && 계속;ordena_balio++) {
            int 처리값=arbel.bidali_erantzun(helbide,ordena_balio);
            if(처리값<0){errorea(처리값);break;}보낸수++;
            int Exekutatu_2=arbel.밀리초();
            while(arbel.응답읽기(0)==-11 && arbel.밀리초()-Exekutatu_2<제한)if(!itxaron_Egoera(1)){계속=false;break;}
            if(!계속)break;
            if(arbel.응답읽기(0)==0){
                int ordua_balio=arbel.응답읽기(1);RECEIVED_ZENBATU++;누적+=ordua_balio;if(ordua_balio<최솟값)최솟값=ordua_balio;if(ordua_balio>최댓값)최댓값=ordua_balio;
                단말.Idatzi("32 bytes from ");idatzi_helbide(helbide);단말.Idatzi(" seq=");단말.수(ordena_balio);단말.Idatzi(" ttl=");단말.수(arbel.응답읽기(2));단말.Idatzi(" time=");단말.수(ordua_balio);단말.Idatzi(" ms\n");
            }else{단말.Idatzi("Request timeout seq=");단말.수(ordena_balio);단말.문자(10);}
            if(ordena_balio<횟수)계속=itxaron_Egoera(200);
        }
        단말.수(보낸수);단말.Idatzi(" transmitted, ");단말.수(RECEIVED_ZENBATU);단말.Idatzi(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_ZENBATU)*100/보낸수);단말.Idatzi("% packet loss\n");
        if(RECEIVED_ZENBATU>0){단말.Idatzi("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_ZENBATU);단말.문자('/');단말.수(최댓값);단말.Idatzi(" ms\n");}
        명령해석기.EMAITZA=계속?(RECEIVED_ZENBATU==0?1:0):130;
    }
    static void erakutsi_jarduera() { 단말.Idatzi("up ");단말.수(arbel.밀리초()/1000);단말.Idatzi(" seconds\n"); }
    static void erakutsi_Memoria() {
        수항목("ARM RAM KiB (firmware): ",arbel.kontsulta_sistema(0,0));
        수항목("Kernel image+BSS+stack KiB: ",arbel.kontsulta_sistema(1,0));
        int 총량=arbel.kontsulta_sistema(2,0), 사용량=arbel.kontsulta_sistema(3,0);
        단말.Idatzi("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",arbel.kontsulta_sistema(4,0));
        수항목("EL0 arena+session reserve KiB: ",arbel.kontsulta_sistema(5,0));
        int 매핑=0;for(int INDIZE=0;INDIZE<4;INDIZE++)매핑+=arbel.kontsulta_sistema(22,INDIZE);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Idatzi("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void erakutsi_Tasks() {
        단말.Idatzi("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Idatzi("1 - RUN - - ");단말.수(arbel.밀리초());단말.Idatzi(" kernel/shell\n");
        for(int INDIZE=1;INDIZE<3;INDIZE++)if(arbel.ataza_Egoera(INDIZE)>0){단말.수(INDIZE+1);단말.Idatzi(" - READY 64 - - kernel-task\n");}
        for(int INDIZE=0;INDIZE<4;INDIZE++){
            int Egoera_balio=arbel.kontsulta_sistema(20,INDIZE);if(Egoera_balio==0)continue;
            단말.수(arbel.kontsulta_sistema(21,INDIZE));단말.문자(' ');단말.수(INDIZE);단말.Idatzi(Egoera_balio==1?" RUN ":" SUSPENDED ");
            단말.수(arbel.kontsulta_sistema(22,INDIZE));단말.문자(' ');단말.수(arbel.kontsulta_sistema(24,INDIZE));단말.문자(' ');단말.수(arbel.kontsulta_sistema(23,INDIZE));단말.문자(' ');
            for(int kargu_INDIZE=0;kargu_INDIZE<288;kargu_INDIZE++){int byte_balio=arbel.kontsulta_sistema(25,INDIZE+kargu_INDIZE*4);if(byte_balio==0)break;arbel.직렬쓰기(byte_balio);}단말.문자(10);
        }
    }
    static void erakutsi_biltegi() {
        int 칸수=0, datuak_ZENBATU=0;
        for(int INDIZE=0;INDIZE<Memoria_Fitxategiak.fitxategi_ZENBATU;INDIZE++)if(Memoria_Fitxategiak.이름길이[INDIZE]>0 || Memoria_Fitxategiak.Erreferentzia_materiala_ZENBATU[INDIZE]>0){칸수++;datuak_ZENBATU+=Memoria_Fitxategiak.luzera_balio[INDIZE];}
        단말.Idatzi("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memoria_Fitxategiak.fitxategi_ZENBATU*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((Memoria_Fitxategiak.fitxategi_ZENBATU-칸수)*16384);단말.문자(' ');단말.수(datuak_ZENBATU);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(Memoria_Fitxategiak.fitxategi_ZENBATU);단말.Idatzi(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void erakutsi_egoera() {
        int 횟수=셸입출력.informatika_interaktibo()!=0?0:1;
        if(elementu_ZENBATU()>1){if(elementu_ZENBATU()!=3 || !같음(1,"-n") || (횟수=digitu_balio(2,1000))<1){hutsegite_balio("사용법: top [-n 1..1000]; q/Ctrl+C로 irten_aplik_55b3a1cd");return;}}
        for(int SEKUENTZIA_balio=0;횟수==0 || SEKUENTZIA_balio<횟수;SEKUENTZIA_balio++){
            if(셸입출력.informatika_interaktibo()!=0 && 횟수==0)단말.Idatzi("\u001b[2J\u001b[H");
            erakutsi_jarduera();erakutsi_Memoria();erakutsi_Tasks();
            if(횟수!=0 && SEKUENTZIA_balio+1>=횟수)break;
            if(!itxaron_Egoera(1000))break;
        }
    }
    static String 표준말(int INDIZE) {
        if(INDIZE==0)return "ipconfig";if(INDIZE==1)return "ip";if(INDIZE==2)return "ping";if(INDIZE==3)return "route";if(INDIZE==4)return "netstat";
        if(INDIZE==5)return "ps";if(INDIZE==6)return "top";if(INDIZE==7)return "free";if(INDIZE==8)return "df";if(INDIZE==9)return "uptime";if(INDIZE==10)return "poweroff";return "help";
    }
    static void erakutsi_laguntza() {
        단말.Idatzi("--- Network / system commands ---\n");
        for(int INDIZE=0;INDIZE<12;INDIZE++){단말.Idatzi(표준말(INDIZE));단말.Idatzi(" / ");단말.Idatzi(관리명령.Word_SMS(INDIZE));단말.Idatzi(" : ");단말.Idatzi(관리명령.설명(INDIZE));단말.문자(10);}
        단말.Idatzi("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Idatzi("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Idatzi("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean exekutatu_komando() {
        int Komandoa=-1;
        for(int INDIZE=0;INDIZE<12;INDIZE++)if(같음(0,표준말(INDIZE)) || 같음(0,관리명령.Word_SMS(INDIZE)))Komandoa=INDIZE;
        if(같음(0,"ifconfig"))Komandoa=0;if(같음(0,"ss"))Komandoa=4;
        if(Komandoa<0)return false;
        if(Komandoa==11){if(같음(1,"net") || 같음(1,"system"))erakutsi_laguntza();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.erakutsi_laguntza();return true;}
        if(Komandoa==0 || Komandoa==1)sare_komando(Komandoa==1);
        else if(Komandoa==2)응답시험();
        else if(Komandoa==6)erakutsi_egoera();
        else if(elementu_ZENBATU()!=1){hutsegite_balio("This command takes no arguments; help system");}
        else if(Komandoa==3)erakutsi_bide_izen();else if(Komandoa==4)erakutsi_sare();else if(Komandoa==5)erakutsi_Tasks();else if(Komandoa==7)erakutsi_Memoria();else if(Komandoa==8)erakutsi_biltegi();else if(Komandoa==9)erakutsi_jarduera();
        else if(Komandoa==10)arbel.전원끄기();
        return true;
    }
}
