// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** werkelijk_gegevens kernel_WAARDE 상태를 읽는 IPv4·ICMP·작업·Geheugen_WAARDE·RAM opslagplaats_wortel 관리 opdracht. */
public final class Systeem_hulpmiddel {
    static int ADRES_WAARDE;
    static boolean 같음(int INDEX, String Word_sms) { return Opdrachtvertolker.같음(INDEX, Word_sms); }
    static int item_AANTAL() { return Opdrachtvertolker.token_AANTAL; }
    static void fout_WAARDE(String LEESMIJ_eb81d7d9) { Opdrachtvertolker.resultaat=2; 단말.Schrijven(LEESMIJ_eb81d7d9); 단말.문자(10); }
    static void fout(int WAARDE) { Opdrachtvertolker.fout(WAARDE); }
    static void nummer_invoer(String Naam, int WAARDE) { 단말.Schrijven(Naam); 단말.nummer(WAARDE); 단말.문자(10); }
    static int cijfer_WAARDE(int INDEX, int 한도) {
        if (INDEX>=item_AANTAL() || Opdrachtvertolker.tijdsduur_WAARDE[INDEX]==0) return -1;
        int WAARDE=0;
        for (int 순번=0; 순번<Opdrachtvertolker.tijdsduur_WAARDE[INDEX]; 순번++) {
            int teken_WAARDE=Opdrachtvertolker.token_WAARDE[Opdrachtvertolker.시작점[INDEX]+순번]-'0';
            if (teken_WAARDE<0 || teken_WAARDE>9 || WAARDE>(한도-teken_WAARDE)/10) return -1;
            WAARDE=WAARDE*10+teken_WAARDE;
        }
        return WAARDE<=한도?WAARDE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=item_AANTAL()) return false;
        int WAARDE=0, chunk_WAARDE=0, cijfer_AANTAL=0, punt_AANTAL=0;
        for (int 순번=0; 순번<Opdrachtvertolker.tijdsduur_WAARDE[INDEX]; 순번++) {
            int teken_WAARDE=Opdrachtvertolker.token_WAARDE[Opdrachtvertolker.시작점[INDEX]+순번];
            if (teken_WAARDE=='.') { if (cijfer_AANTAL==0 || ++punt_AANTAL>3) return false; WAARDE=(WAARDE<<8)|chunk_WAARDE; chunk_WAARDE=cijfer_AANTAL=0; }
            else { if (teken_WAARDE<'0' || teken_WAARDE>'9' || ++cijfer_AANTAL>3) return false; chunk_WAARDE=chunk_WAARDE*10+teken_WAARDE-'0'; if(chunk_WAARDE>255)return false; }
        }
        if (punt_AANTAL!=3 || cijfer_AANTAL==0) return false;
        ADRES_WAARDE=(WAARDE<<8)|chunk_WAARDE; return true;
    }
    static void schrijven_ADRES(int WAARDE) {
        단말.nummer((WAARDE>>>24)&255); 단말.문자('.'); 단말.nummer((WAARDE>>>16)&255); 단말.문자('.');
        단말.nummer((WAARDE>>>8)&255); 단말.문자('.'); 단말.nummer(WAARDE&255);
    }
    static void weergeven_net_status() {
        단말.Schrijven(Bord.net_status(20,0)!=0?"en0: ":"sl0: "); 단말.Schrijven(Bord.net_status(3,0)!=0?"UP":"DOWN");
        단말.Schrijven(Bord.net_status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Schrijven(Bord.net_status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); schrijven_ADRES(Bord.net_status(0,0));
        단말.Schrijven(" netmask "); schrijven_ADRES(Bord.net_status(1,0)); 단말.Schrijven(" gateway "); schrijven_ADRES(Bord.net_status(2,0)); 단말.문자(10);
        단말.Schrijven("  RX packets "); 단말.nummer(Bord.net_status(4,0)); 단말.Schrijven(" bytes "); 단말.nummer(Bord.net_status(6,0));
        단말.Schrijven(" TX packets "); 단말.nummer(Bord.net_status(5,0)); 단말.Schrijven(" bytes "); 단말.nummer(Bord.net_status(7,0)); 단말.문자(10);
        nummer_invoer("  dropped ",Bord.net_status(8,0));
    }
    static void set_ADRES(int starten) {
        if (item_AANTAL()!=starten+3 || !주소읽기(starten)) { fout_WAARDE("사용법: ipconfig set ADRES 주소가림 gateway_WAARDE"); return; }
        int ADRES=ADRES_WAARDE;
        if(!주소읽기(starten+1)){fout_WAARDE("Invalid IPv4 netmask");return;} int masker_WAARDE=ADRES_WAARDE;
        if(!주소읽기(starten+2)){fout_WAARDE("Invalid IPv4 gateway");return;}
        int resultaat=Bord.net_Instellingen(0,ADRES,masker_WAARDE,ADRES_WAARDE);
        if(resultaat<0) { fout(resultaat); if(resultaat==-16)단말.Schrijven("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Schrijven("IPv4 configuration applied (until reboot)\n"); weergeven_net_status(); }
    }
    static void net_opdracht(boolean IP_adres) {
        if (item_AANTAL()==1 || item_AANTAL()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || item_AANTAL()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { weergeven_net_status();return; }
        if (IP_adres && 같음(1,"route") && (item_AANTAL()==2 || item_AANTAL()==3&&같음(2,"show"))) { weergeven_pad();return; }
        if (같음(1,"set")) { set_ADRES(2);return; }
        if (item_AANTAL()==2 && (같음(1,"up") || 같음(1,"down"))) { Bord.net_Instellingen(같음(1,"up")?1:2,0,0,0);weergeven_net_status();return; }
        if (IP_adres && item_AANTAL()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Bord.net_Instellingen(같음(5,"up")?1:2,0,0,0);weergeven_net_status();return; }
        fout_WAARDE("사용법: ip [addr show|route show|set ADRES 주소가림 gateway_WAARDE|link set dev sl0 up|down]");
    }
    static void weergeven_pad() {
        단말.Schrijven("Destination Netmask Gateway Interface\n");
        schrijven_ADRES(Bord.net_status(0,0)&Bord.net_status(1,0));단말.문자(' ');schrijven_ADRES(Bord.net_status(1,0));단말.Schrijven(Bord.net_status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Bord.net_status(2,0)!=0) {단말.Schrijven("0.0.0.0 0.0.0.0 ");schrijven_ADRES(Bord.net_status(2,0));단말.Schrijven(Bord.net_status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void weergeven_net() {
        단말.Schrijven("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_gebied=Bord.net_status(10,INDEX);if(TYPE_gebied==0)continue;
            단말.Schrijven(TYPE_gebied==1?"TCP ":"UDP ");schrijven_ADRES(Bord.net_status(16,INDEX));단말.문자(':');단말.nummer(Bord.net_status(11,INDEX));단말.문자(' ');
            schrijven_ADRES(Bord.net_status(12,INDEX));단말.문자(':');단말.nummer(Bord.net_status(13,INDEX));단말.문자(' ');
            int Status_WAARDE=Bord.net_status(14,INDEX);단말.Schrijven(TYPE_gebied==2?"DATAGRAM":Status_WAARDE==1?"LISTEN":Status_WAARDE==2?"ESTABLISHED":Status_WAARDE==3?"CLOSE_WAIT":Status_WAARDE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.nummer(Bord.net_status(15,INDEX));단말.문자(10);
        }
        단말.Schrijven("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean wachtstatus(int 밀리초) {
        int starten=Bord.밀리초();
        while(Bord.밀리초()-starten<밀리초) {
            if(셸입출력.informatie_interactief()!=0){int teken_WAARDE=Bord.직렬읽기();if(teken_WAARDE==3 || teken_WAARDE=='q' || teken_WAARDE=='Q' || teken_WAARDE==27 || teken_WAARDE==-4096)return false;}
            Bord.RENDEMENT_CPU();
        }
        return true;
    }
    static void test_reactie() {
        int herhaling_AANTAL=4, 제한=1000, doel=-1;
        for(int plaatsingsindex=1;plaatsingsindex<item_AANTAL();plaatsingsindex++) {
            if(같음(plaatsingsindex,"-c")){herhaling_AANTAL=cijfer_WAARDE(++plaatsingsindex,100);if(herhaling_AANTAL<1){fout_WAARDE("ping: -c 1..100");return;}}
            else if(같음(plaatsingsindex,"-W")){제한=cijfer_WAARDE(++plaatsingsindex,10);if(제한<1){fout_WAARDE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(doel<0)doel=plaatsingsindex;else{fout_WAARDE("사용법: ping [-c herhaling_AANTAL] [-W 초] IPv4");return;}
        }
        if(doel<0 || !주소읽기(doel)){fout_WAARDE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADRES=ADRES_WAARDE, 보낸수=0, OPBRENGST_AANTAL=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Schrijven("PING ");schrijven_ADRES(ADRES);단말.Schrijven(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int order_WAARDE=1;order_WAARDE<=herhaling_AANTAL && 계속;order_WAARDE++) {
            int 처리값=Bord.e_mailen_reactie(ADRES,order_WAARDE);
            if(처리값<0){fout(처리값);break;}보낸수++;
            int starten=Bord.밀리초();
            while(Bord.응답읽기(0)==-11 && Bord.밀리초()-starten<제한)if(!wachtstatus(1)){계속=false;break;}
            if(!계속)break;
            if(Bord.응답읽기(0)==0){
                int TIJD_WAARDE=Bord.응답읽기(1);OPBRENGST_AANTAL++;누적+=TIJD_WAARDE;if(TIJD_WAARDE<최솟값)최솟값=TIJD_WAARDE;if(TIJD_WAARDE>최댓값)최댓값=TIJD_WAARDE;
                단말.Schrijven("32 bytes from ");schrijven_ADRES(ADRES);단말.Schrijven(" seq=");단말.nummer(order_WAARDE);단말.Schrijven(" ttl=");단말.nummer(Bord.응답읽기(2));단말.Schrijven(" time=");단말.nummer(TIJD_WAARDE);단말.Schrijven(" ms\n");
            }else{단말.Schrijven("Request timeout seq=");단말.nummer(order_WAARDE);단말.문자(10);}
            if(order_WAARDE<herhaling_AANTAL)계속=wachtstatus(200);
        }
        단말.nummer(보낸수);단말.Schrijven(" transmitted, ");단말.nummer(OPBRENGST_AANTAL);단말.Schrijven(" received, ");단말.nummer(보낸수==0?100:(보낸수-OPBRENGST_AANTAL)*100/보낸수);단말.Schrijven("% packet loss\n");
        if(OPBRENGST_AANTAL>0){단말.Schrijven("rtt min/avg/max = ");단말.nummer(최솟값);단말.문자('/');단말.nummer(누적/OPBRENGST_AANTAL);단말.문자('/');단말.nummer(최댓값);단말.Schrijven(" ms\n");}
        Opdrachtvertolker.resultaat=계속?(OPBRENGST_AANTAL==0?1:0):130;
    }
    static void weergeven_Activiteit() { 단말.Schrijven("up ");단말.nummer(Bord.밀리초()/1000);단말.Schrijven(" seconds\n"); }
    static void weergeven_Geheugen() {
        nummer_invoer("ARM RAM KiB (firmware): ",Bord.query_Systeem(0,0));
        nummer_invoer("Kernel image+BSS+stack KiB: ",Bord.query_Systeem(1,0));
        int totaal_capaciteit=Bord.query_Systeem(2,0), 사용량=Bord.query_Systeem(3,0);
        단말.Schrijven("AOT heap KiB total/used/free: ");단말.nummer(totaal_capaciteit);단말.문자('/');단말.nummer(사용량);단말.문자('/');단말.nummer(totaal_capaciteit-사용량);단말.문자(10);
        nummer_invoer("Framebuffer KiB: ",Bord.query_Systeem(4,0));
        nummer_invoer("EL0 arena+session reserve KiB: ",Bord.query_Systeem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Bord.query_Systeem(22,INDEX);
        nummer_invoer("EL0 mapped KiB: ",매핑);
        단말.Schrijven("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void weergeven_Tasks() {
        단말.Schrijven("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Schrijven("1 - RUN - - ");단말.nummer(Bord.밀리초());단말.Schrijven(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Bord.taak_Status(INDEX)>0){단말.nummer(INDEX+1);단말.Schrijven(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Status_WAARDE=Bord.query_Systeem(20,INDEX);if(Status_WAARDE==0)continue;
            단말.nummer(Bord.query_Systeem(21,INDEX));단말.문자(' ');단말.nummer(INDEX);단말.Schrijven(Status_WAARDE==1?" RUN ":" SUSPENDED ");
            단말.nummer(Bord.query_Systeem(22,INDEX));단말.문자(' ');단말.nummer(Bord.query_Systeem(24,INDEX));단말.문자(' ');단말.nummer(Bord.query_Systeem(23,INDEX));단말.문자(' ');
            for(int plaatsingsindex=0;plaatsingsindex<288;plaatsingsindex++){int byte_WAARDE=Bord.query_Systeem(25,INDEX+plaatsingsindex*4);if(byte_WAARDE==0)break;Bord.직렬쓰기(byte_WAARDE);}단말.문자(10);
        }
    }
    static void weergeven_Opslag() {
        int sleuf_AANTAL=0, gegevens_AANTAL=0;
        for(int INDEX=0;INDEX<GeheugenBestanden.Bestand_AANTAL;INDEX++)if(GeheugenBestanden.이름길이[INDEX]>0 || GeheugenBestanden.verwijzen_AANTAL[INDEX]>0){sleuf_AANTAL++;gegevens_AANTAL+=GeheugenBestanden.tijdsduur_WAARDE[INDEX];}
        단말.Schrijven("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.nummer(GeheugenBestanden.Bestand_AANTAL*16384);단말.문자(' ');단말.nummer(sleuf_AANTAL*16384);단말.문자(' ');단말.nummer((GeheugenBestanden.Bestand_AANTAL-sleuf_AANTAL)*16384);단말.문자(' ');단말.nummer(gegevens_AANTAL);단말.문자(' ');단말.nummer(sleuf_AANTAL);단말.문자('/');단말.nummer(GeheugenBestanden.Bestand_AANTAL);단말.Schrijven(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void weergeven_status() {
        int herhaling_AANTAL=셸입출력.informatie_interactief()!=0?0:1;
        if(item_AANTAL()>1){if(item_AANTAL()!=3 || !같음(1,"-n") || (herhaling_AANTAL=cijfer_WAARDE(2,1000))<1){fout_WAARDE("사용법: top [-n 1..1000]; q/Ctrl+C로 sluiten_app");return;}}
        for(int REEKS_WAARDE=0;herhaling_AANTAL==0 || REEKS_WAARDE<herhaling_AANTAL;REEKS_WAARDE++){
            if(셸입출력.informatie_interactief()!=0 && herhaling_AANTAL==0)단말.Schrijven("\u001b[2J\u001b[H");
            weergeven_Activiteit();weergeven_Geheugen();weergeven_Tasks();
            if(herhaling_AANTAL!=0 && REEKS_WAARDE+1>=herhaling_AANTAL)break;
            if(!wachtstatus(1000))break;
        }
    }
    static String Standard_Word(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void hulp_tonen() {
        단말.Schrijven("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Schrijven(Standard_Word(INDEX));단말.Schrijven(" / ");단말.Schrijven(관리명령.Word_sms(INDEX));단말.Schrijven(" : ");단말.Schrijven(관리명령.설명(INDEX));단말.문자(10);}
        단말.Schrijven("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Schrijven("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Schrijven("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Uitvoeren_opdracht() {
        int opdracht=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,Standard_Word(INDEX)) || 같음(0,관리명령.Word_sms(INDEX)))opdracht=INDEX;
        if(같음(0,"ifconfig"))opdracht=0;if(같음(0,"ss"))opdracht=4;
        if(opdracht<0)return false;
        if(opdracht==11){if(같음(1,"net") || 같음(1,"system"))hulp_tonen();else if(같음(1,"ko") || 같음(1,"input"))Opdrachtvertolker.한글도움말();else Opdrachtvertolker.hulp_tonen();return true;}
        if(opdracht==0 || opdracht==1)net_opdracht(opdracht==1);
        else if(opdracht==2)test_reactie();
        else if(opdracht==6)weergeven_status();
        else if(item_AANTAL()!=1){fout_WAARDE("This command takes no arguments; help system");}
        else if(opdracht==3)weergeven_pad();else if(opdracht==4)weergeven_net();else if(opdracht==5)weergeven_Tasks();else if(opdracht==7)weergeven_Geheugen();else if(opdracht==8)weergeven_Opslag();else if(opdracht==9)weergeven_Activiteit();
        else if(opdracht==10)Bord.전원끄기();
        return true;
    }
}
