// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Verwaltungsbefehle für IPv4, ICMP, Aufgaben, Speicher und RAM-Dateien, die den tatsächlichen Kernelzustand lesen. */
public final class systemWerkzeug {
    static int adresseWert;
    static boolean gleichText(int Nummer, String maschinenwortText) { return Befehlsinterpreter.gleichText(Nummer, maschinenwortText); }
    static int elementeintragAnzahl() { return Befehlsinterpreter.wortzeichenAnzahl; }
    static void fehlschlagWert(String Anleitung) { Befehlsinterpreter.ergebnis=2; TerminalEinAusgabe.schreiben(Anleitung); TerminalEinAusgabe.Zeichen(10); }
    static void fehler(int Wert) { Befehlsinterpreter.fehler(Wert); }
    static void nummerEintrag(String Name, int Wert) { TerminalEinAusgabe.schreiben(Name); TerminalEinAusgabe.Zahl(Wert); TerminalEinAusgabe.Zeichen(10); }
    static int zifferWert(int Nummer, int kapazitätGrenzwert) {
        if (Nummer>=elementeintragAnzahl() || Befehlsinterpreter.Länge[Nummer]==0) return -1;
        int Wert=0;
        for (int ordnungszahlIndex=0; ordnungszahlIndex<Befehlsinterpreter.Länge[Nummer]; ordnungszahlIndex++) {
            int zeichenWert=Befehlsinterpreter.wortzeichenWert[Befehlsinterpreter.beginnendPunkt[Nummer]+ordnungszahlIndex]-'0';
            if (zeichenWert<0 || zeichenWert>9 || Wert>(kapazitätGrenzwert-zeichenWert)/10) return -1;
            Wert=Wert*10+zeichenWert;
        }
        return Wert<=kapazitätGrenzwert?Wert:-1;
    }
    static boolean adresseLesen(int Nummer) {
        if (Nummer>=elementeintragAnzahl()) return false;
        int Wert=0, teilblockWert=0, zifferAnzahl=0, punktAnzahl=0;
        for (int ordnungszahlIndex=0; ordnungszahlIndex<Befehlsinterpreter.Länge[Nummer]; ordnungszahlIndex++) {
            int zeichenWert=Befehlsinterpreter.wortzeichenWert[Befehlsinterpreter.beginnendPunkt[Nummer]+ordnungszahlIndex];
            if (zeichenWert=='.') { if (zifferAnzahl==0 || ++punktAnzahl>3) return false; Wert=(Wert<<8)|teilblockWert; teilblockWert=zifferAnzahl=0; }
            else { if (zeichenWert<'0' || zeichenWert>'9' || ++zifferAnzahl>3) return false; teilblockWert=teilblockWert*10+zeichenWert-'0'; if(teilblockWert>255)return false; }
        }
        if (punktAnzahl!=3 || zifferAnzahl==0) return false;
        adresseWert=(Wert<<8)|teilblockWert; return true;
    }
    static void adresseSchreiben(int Wert) {
        TerminalEinAusgabe.Zahl((Wert>>>24)&255); TerminalEinAusgabe.Zeichen('.'); TerminalEinAusgabe.Zahl((Wert>>>16)&255); TerminalEinAusgabe.Zeichen('.');
        TerminalEinAusgabe.Zahl((Wert>>>8)&255); TerminalEinAusgabe.Zeichen('.'); TerminalEinAusgabe.Zahl(Wert&255);
    }
    static void netzwerkZustandAnzeigen() {
        TerminalEinAusgabe.schreiben(Platine.netzwerkZustand(20,0)!=0?"en0: ":"sl0: "); TerminalEinAusgabe.schreiben(Platine.netzwerkZustand(3,0)!=0?"UP":"DOWN");
        TerminalEinAusgabe.schreiben(Platine.netzwerkZustand(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        TerminalEinAusgabe.schreiben(Platine.netzwerkZustand(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); adresseSchreiben(Platine.netzwerkZustand(0,0));
        TerminalEinAusgabe.schreiben(" netmask "); adresseSchreiben(Platine.netzwerkZustand(1,0)); TerminalEinAusgabe.schreiben(" gateway "); adresseSchreiben(Platine.netzwerkZustand(2,0)); TerminalEinAusgabe.Zeichen(10);
        TerminalEinAusgabe.schreiben("  RX packets "); TerminalEinAusgabe.Zahl(Platine.netzwerkZustand(4,0)); TerminalEinAusgabe.schreiben(" bytes "); TerminalEinAusgabe.Zahl(Platine.netzwerkZustand(6,0));
        TerminalEinAusgabe.schreiben(" TX packets "); TerminalEinAusgabe.Zahl(Platine.netzwerkZustand(5,0)); TerminalEinAusgabe.schreiben(" bytes "); TerminalEinAusgabe.Zahl(Platine.netzwerkZustand(7,0)); TerminalEinAusgabe.Zeichen(10);
        nummerEintrag("  dropped ",Platine.netzwerkZustand(8,0));
    }
    static void adresseSetzen(int ausführenVorgang) {
        if (elementeintragAnzahl()!=ausführenVorgang+3 || !adresseLesen(ausführenVorgang)) { fehlschlagWert("사용법: ipconfig set adresse 주소가림 netzübergangWert"); return; }
        int adresse=adresseWert;
        if(!adresseLesen(ausführenVorgang+1)){fehlschlagWert("Invalid IPv4 netmask");return;} int maskeWert=adresseWert;
        if(!adresseLesen(ausführenVorgang+2)){fehlschlagWert("Invalid IPv4 gateway");return;}
        int ergebnis=Platine.netzwerkEinstellungen(0,adresse,maskeWert,adresseWert);
        if(ergebnis<0) { fehler(ergebnis); if(ergebnis==-16)TerminalEinAusgabe.schreiben("Close sockets and stop ftpd before changing address.\n"); }
        else { TerminalEinAusgabe.schreiben("IPv4 configuration applied (until reboot)\n"); netzwerkZustandAnzeigen(); }
    }
    static void netzwerkBefehl(boolean iPAdresse) {
        if (elementeintragAnzahl()==1 || elementeintragAnzahl()==2 && (gleichText(1,"show") || gleichText(1,"addr") || gleichText(1,"address") || gleichText(1,"sl0") || gleichText(1,"en0")) || elementeintragAnzahl()==3 && (gleichText(1,"addr") || gleichText(1,"address")) && gleichText(2,"show")) { netzwerkZustandAnzeigen();return; }
        if (iPAdresse && gleichText(1,"route") && (elementeintragAnzahl()==2 || elementeintragAnzahl()==3&&gleichText(2,"show"))) { pfadAnzeigen();return; }
        if (gleichText(1,"set")) { adresseSetzen(2);return; }
        if (elementeintragAnzahl()==2 && (gleichText(1,"up") || gleichText(1,"down"))) { Platine.netzwerkEinstellungen(gleichText(1,"up")?1:2,0,0,0);netzwerkZustandAnzeigen();return; }
        if (iPAdresse && elementeintragAnzahl()==6 && gleichText(1,"link") && gleichText(2,"set") && gleichText(3,"dev") && (gleichText(4,"sl0")||gleichText(4,"en0")) && (gleichText(5,"up") || gleichText(5,"down"))) { Platine.netzwerkEinstellungen(gleichText(5,"up")?1:2,0,0,0);netzwerkZustandAnzeigen();return; }
        fehlschlagWert("사용법: ip [addr show|route show|set adresse 주소가림 netzübergangWert|link set dev sl0 up|down]");
    }
    static void pfadAnzeigen() {
        TerminalEinAusgabe.schreiben("Destination Netmask Gateway Interface\n");
        adresseSchreiben(Platine.netzwerkZustand(0,0)&Platine.netzwerkZustand(1,0));TerminalEinAusgabe.Zeichen(' ');adresseSchreiben(Platine.netzwerkZustand(1,0));TerminalEinAusgabe.schreiben(Platine.netzwerkZustand(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Platine.netzwerkZustand(2,0)!=0) {TerminalEinAusgabe.schreiben("0.0.0.0 0.0.0.0 ");adresseSchreiben(Platine.netzwerkZustand(2,0));TerminalEinAusgabe.schreiben(Platine.netzwerkZustand(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void netzwerkAnzeigen() {
        TerminalEinAusgabe.schreiben("Proto Local Remote State Queued\n");
        for(int Nummer=0;Nummer<32;Nummer++) {
            int typKategorie=Platine.netzwerkZustand(10,Nummer);if(typKategorie==0)continue;
            TerminalEinAusgabe.schreiben(typKategorie==1?"TCP ":"UDP ");adresseSchreiben(Platine.netzwerkZustand(16,Nummer));TerminalEinAusgabe.Zeichen(':');TerminalEinAusgabe.Zahl(Platine.netzwerkZustand(11,Nummer));TerminalEinAusgabe.Zeichen(' ');
            adresseSchreiben(Platine.netzwerkZustand(12,Nummer));TerminalEinAusgabe.Zeichen(':');TerminalEinAusgabe.Zahl(Platine.netzwerkZustand(13,Nummer));TerminalEinAusgabe.Zeichen(' ');
            int statuswertWert=Platine.netzwerkZustand(14,Nummer);TerminalEinAusgabe.schreiben(typKategorie==2?"DATAGRAM":statuswertWert==1?"LISTEN":statuswertWert==2?"ESTABLISHED":statuswertWert==3?"CLOSE_WAIT":statuswertWert==4?"ERROR":"UNCONNECTED");
            TerminalEinAusgabe.Zeichen(' ');TerminalEinAusgabe.Zahl(Platine.netzwerkZustand(15,Nummer));TerminalEinAusgabe.Zeichen(10);
        }
        TerminalEinAusgabe.schreiben("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean statuswertWarten(int millisekunden) {
        int ausführenVorgang=Platine.millisekunden();
        while(Platine.millisekunden()-ausführenVorgang<millisekunden) {
            if(BefehlshülleEinAusgabe.istInteraktiv()!=0){int zeichenWert=Platine.seriellLesen();if(zeichenWert==3 || zeichenWert=='q' || zeichenWert=='Q' || zeichenWert==27 || zeichenWert==-4096)return false;}
            Platine.prozessorAbgeben();
        }
        return true;
    }
    static void rückmeldungPrüfung() {
        int wiederholungAnzahl=4, grenzwertWert=1000, zielobjektWert=-1;
        for(int positionIndex=1;positionIndex<elementeintragAnzahl();positionIndex++) {
            if(gleichText(positionIndex,"-c")){wiederholungAnzahl=zifferWert(++positionIndex,100);if(wiederholungAnzahl<1){fehlschlagWert("ping: -c 1..100");return;}}
            else if(gleichText(positionIndex,"-W")){grenzwertWert=zifferWert(++positionIndex,10);if(grenzwertWert<1){fehlschlagWert("ping: -W 1..10 seconds");return;}grenzwertWert*=1000;}
            else if(zielobjektWert<0)zielobjektWert=positionIndex;else{fehlschlagWert("사용법: ping [-c wiederholungAnzahl] [-W sekundenWert] IPv4");return;}
        }
        if(zielobjektWert<0 || !adresseLesen(zielobjektWert)){fehlschlagWert("ping: an IPv4 address is required (DNS is not configured)");return;}
        int adresse=adresseWert, gesendetAnzahl=0, empfangenWertAnzahl=0, angesammeltWert=0, mindestwertGrenzwert=100000, höchstwertGrenzwert=0;
        TerminalEinAusgabe.schreiben("PING ");adresseSchreiben(adresse);TerminalEinAusgabe.schreiben(" 32 ICMP bytes\n");
        boolean fortsetzenVerarbeitung=true;
        for(int reihenfolgeWert=1;reihenfolgeWert<=wiederholungAnzahl && fortsetzenVerarbeitung;reihenfolgeWert++) {
            int verarbeitetWert=Platine.rückmeldungSenden(adresse,reihenfolgeWert);
            if(verarbeitetWert<0){fehler(verarbeitetWert);break;}gesendetAnzahl++;
            int ausführenVorgang=Platine.millisekunden();
            while(Platine.rückmeldungLesen(0)==-11 && Platine.millisekunden()-ausführenVorgang<grenzwertWert)if(!statuswertWarten(1)){fortsetzenVerarbeitung=false;break;}
            if(!fortsetzenVerarbeitung)break;
            if(Platine.rückmeldungLesen(0)==0){
                int zeitWert=Platine.rückmeldungLesen(1);empfangenWertAnzahl++;angesammeltWert+=zeitWert;if(zeitWert<mindestwertGrenzwert)mindestwertGrenzwert=zeitWert;if(zeitWert>höchstwertGrenzwert)höchstwertGrenzwert=zeitWert;
                TerminalEinAusgabe.schreiben("32 bytes from ");adresseSchreiben(adresse);TerminalEinAusgabe.schreiben(" seq=");TerminalEinAusgabe.Zahl(reihenfolgeWert);TerminalEinAusgabe.schreiben(" ttl=");TerminalEinAusgabe.Zahl(Platine.rückmeldungLesen(2));TerminalEinAusgabe.schreiben(" time=");TerminalEinAusgabe.Zahl(zeitWert);TerminalEinAusgabe.schreiben(" ms\n");
            }else{TerminalEinAusgabe.schreiben("Request timeout seq=");TerminalEinAusgabe.Zahl(reihenfolgeWert);TerminalEinAusgabe.Zeichen(10);}
            if(reihenfolgeWert<wiederholungAnzahl)fortsetzenVerarbeitung=statuswertWarten(200);
        }
        TerminalEinAusgabe.Zahl(gesendetAnzahl);TerminalEinAusgabe.schreiben(" transmitted, ");TerminalEinAusgabe.Zahl(empfangenWertAnzahl);TerminalEinAusgabe.schreiben(" received, ");TerminalEinAusgabe.Zahl(gesendetAnzahl==0?100:(gesendetAnzahl-empfangenWertAnzahl)*100/gesendetAnzahl);TerminalEinAusgabe.schreiben("% packet loss\n");
        if(empfangenWertAnzahl>0){TerminalEinAusgabe.schreiben("rtt min/avg/max = ");TerminalEinAusgabe.Zahl(mindestwertGrenzwert);TerminalEinAusgabe.Zeichen('/');TerminalEinAusgabe.Zahl(angesammeltWert/empfangenWertAnzahl);TerminalEinAusgabe.Zeichen('/');TerminalEinAusgabe.Zahl(höchstwertGrenzwert);TerminalEinAusgabe.schreiben(" ms\n");}
        Befehlsinterpreter.ergebnis=fortsetzenVerarbeitung?(empfangenWertAnzahl==0?1:0):130;
    }
    static void aktivitätAnzeigen() { TerminalEinAusgabe.schreiben("up ");TerminalEinAusgabe.Zahl(Platine.millisekunden()/1000);TerminalEinAusgabe.schreiben(" seconds\n"); }
    static void speicherAnzeigen() {
        nummerEintrag("ARM RAM KiB (firmware): ",Platine.abfragenSystem(0,0));
        nummerEintrag("Kernel image+BSS+stack KiB: ",Platine.abfragenSystem(1,0));
        int gesamtwertKapazität=Platine.abfragenSystem(2,0), benutztKapazität=Platine.abfragenSystem(3,0);
        TerminalEinAusgabe.schreiben("AOT heap KiB total/used/free: ");TerminalEinAusgabe.Zahl(gesamtwertKapazität);TerminalEinAusgabe.Zeichen('/');TerminalEinAusgabe.Zahl(benutztKapazität);TerminalEinAusgabe.Zeichen('/');TerminalEinAusgabe.Zahl(gesamtwertKapazität-benutztKapazität);TerminalEinAusgabe.Zeichen(10);
        nummerEintrag("Framebuffer KiB: ",Platine.abfragenSystem(4,0));
        nummerEintrag("EL0 arena+session reserve KiB: ",Platine.abfragenSystem(5,0));
        int zugeordnetWert=0;for(int Nummer=0;Nummer<4;Nummer++)zugeordnetWert+=Platine.abfragenSystem(22,Nummer);
        nummerEintrag("EL0 mapped KiB: ",zugeordnetWert);
        TerminalEinAusgabe.schreiben("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void aufgabenAnzeigen() {
        TerminalEinAusgabe.schreiben("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        TerminalEinAusgabe.schreiben("1 - RUN - - ");TerminalEinAusgabe.Zahl(Platine.millisekunden());TerminalEinAusgabe.schreiben(" kernel/shell\n");
        for(int Nummer=1;Nummer<3;Nummer++)if(Platine.aufgabeStatuswert(Nummer)>0){TerminalEinAusgabe.Zahl(Nummer+1);TerminalEinAusgabe.schreiben(" - READY 64 - - kernel-task\n");}
        for(int Nummer=0;Nummer<4;Nummer++){
            int statuswertWert=Platine.abfragenSystem(20,Nummer);if(statuswertWert==0)continue;
            TerminalEinAusgabe.Zahl(Platine.abfragenSystem(21,Nummer));TerminalEinAusgabe.Zeichen(' ');TerminalEinAusgabe.Zahl(Nummer);TerminalEinAusgabe.schreiben(statuswertWert==1?" RUN ":" SUSPENDED ");
            TerminalEinAusgabe.Zahl(Platine.abfragenSystem(22,Nummer));TerminalEinAusgabe.Zeichen(' ');TerminalEinAusgabe.Zahl(Platine.abfragenSystem(24,Nummer));TerminalEinAusgabe.Zeichen(' ');TerminalEinAusgabe.Zahl(Platine.abfragenSystem(23,Nummer));TerminalEinAusgabe.Zeichen(' ');
            for(int positionIndex=0;positionIndex<288;positionIndex++){int byteWert=Platine.abfragenSystem(25,Nummer+positionIndex*4);if(byteWert==0)break;Platine.seriellSchreiben(byteWert);}TerminalEinAusgabe.Zeichen(10);
        }
    }
    static void speichergerätAnzeigen() {
        int platzAnzahl=0, datenAnzahl=0;
        for(int Nummer=0;Nummer<SpeicherDateien.dateiAnzahl;Nummer++)if(SpeicherDateien.namenlänge[Nummer]>0 || SpeicherDateien.verweisAnzahl[Nummer]>0){platzAnzahl++;datenAnzahl+=SpeicherDateien.Länge[Nummer];}
        TerminalEinAusgabe.schreiben("Filesystem Total Reserved Available Data Files Mount\nramfs ");TerminalEinAusgabe.Zahl(SpeicherDateien.dateiAnzahl*16384);TerminalEinAusgabe.Zeichen(' ');TerminalEinAusgabe.Zahl(platzAnzahl*16384);TerminalEinAusgabe.Zeichen(' ');TerminalEinAusgabe.Zahl((SpeicherDateien.dateiAnzahl-platzAnzahl)*16384);TerminalEinAusgabe.Zeichen(' ');TerminalEinAusgabe.Zahl(datenAnzahl);TerminalEinAusgabe.Zeichen(' ');TerminalEinAusgabe.Zahl(platzAnzahl);TerminalEinAusgabe.Zeichen('/');TerminalEinAusgabe.Zahl(SpeicherDateien.dateiAnzahl);TerminalEinAusgabe.schreiben(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void zustandAnzeigen() {
        int wiederholungAnzahl=BefehlshülleEinAusgabe.istInteraktiv()!=0?0:1;
        if(elementeintragAnzahl()>1){if(elementeintragAnzahl()!=3 || !gleichText(1,"-n") || (wiederholungAnzahl=zifferWert(2,1000))<1){fehlschlagWert("사용법: top [-n 1..1000]; q/Ctrl+C로 aufhörenProgramm");return;}}
        for(int folgeWert=0;wiederholungAnzahl==0 || folgeWert<wiederholungAnzahl;folgeWert++){
            if(BefehlshülleEinAusgabe.istInteraktiv()!=0 && wiederholungAnzahl==0)TerminalEinAusgabe.schreiben("\u001b[2J\u001b[H");
            aktivitätAnzeigen();speicherAnzeigen();aufgabenAnzeigen();
            if(wiederholungAnzahl!=0 && folgeWert+1>=wiederholungAnzahl)break;
            if(!statuswertWarten(1000))break;
        }
    }
    static String standardMaschinenwort(int Nummer) {
        if(Nummer==0)return "ipconfig";if(Nummer==1)return "ip";if(Nummer==2)return "ping";if(Nummer==3)return "route";if(Nummer==4)return "netstat";
        if(Nummer==5)return "ps";if(Nummer==6)return "top";if(Nummer==7)return "free";if(Nummer==8)return "df";if(Nummer==9)return "uptime";if(Nummer==10)return "poweroff";return "help";
    }
    static void hilfeAnzeigen() {
        TerminalEinAusgabe.schreiben("--- Network / system commands ---\n");
        for(int Nummer=0;Nummer<12;Nummer++){TerminalEinAusgabe.schreiben(standardMaschinenwort(Nummer));TerminalEinAusgabe.schreiben(" / ");TerminalEinAusgabe.schreiben(Verwaltungsbefehle.maschinenwortText(Nummer));TerminalEinAusgabe.schreiben(" : ");TerminalEinAusgabe.schreiben(Verwaltungsbefehle.beschreibung(Nummer));TerminalEinAusgabe.Zeichen(10);}
        TerminalEinAusgabe.schreiben("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        TerminalEinAusgabe.schreiben("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        TerminalEinAusgabe.schreiben("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean befehlAusführen() {
        int befehl=-1;
        for(int Nummer=0;Nummer<12;Nummer++)if(gleichText(0,standardMaschinenwort(Nummer)) || gleichText(0,Verwaltungsbefehle.maschinenwortText(Nummer)))befehl=Nummer;
        if(gleichText(0,"ifconfig"))befehl=0;if(gleichText(0,"ss"))befehl=4;
        if(befehl<0)return false;
        if(befehl==11){if(gleichText(1,"net") || gleichText(1,"system"))hilfeAnzeigen();else if(gleichText(1,"ko") || gleichText(1,"input"))Befehlsinterpreter.hangulHilfe();else Befehlsinterpreter.hilfeAnzeigen();return true;}
        if(befehl==0 || befehl==1)netzwerkBefehl(befehl==1);
        else if(befehl==2)rückmeldungPrüfung();
        else if(befehl==6)zustandAnzeigen();
        else if(elementeintragAnzahl()!=1){fehlschlagWert("This command takes no arguments; help system");}
        else if(befehl==3)pfadAnzeigen();else if(befehl==4)netzwerkAnzeigen();else if(befehl==5)aufgabenAnzeigen();else if(befehl==7)speicherAnzeigen();else if(befehl==8)speichergerätAnzeigen();else if(befehl==9)aktivitätAnzeigen();
        else if(befehl==10)Platine.stromversorgungAusgeschaltet();
        return true;
    }
}
