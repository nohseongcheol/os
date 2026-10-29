// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class Verwaltungsbefehle {
    static String abgeschlossenMaschinenwort() { return "Adresskonfiguration Netzadresse Antworttest Wegetabelle Netzverbindungen Prozessliste Aktivitätsübersicht Speicherbelegung Dateisystembelegung Laufzeit Ausschalten Hilfe"; }
    static String maschinenwortText(int Nummer) {
        if (Nummer==0) return "Adresskonfiguration";
        if (Nummer==1) return "Netzadresse";
        if (Nummer==2) return "Antworttest";
        if (Nummer==3) return "Wegetabelle";
        if (Nummer==4) return "Netzverbindungen";
        if (Nummer==5) return "Prozessliste";
        if (Nummer==6) return "Aktivitätsübersicht";
        if (Nummer==7) return "Speicherbelegung";
        if (Nummer==8) return "Dateisystembelegung";
        if (Nummer==9) return "Laufzeit";
        if (Nummer==10) return "Ausschalten";
        return "Hilfe";
    }
    static String beschreibung(int Nummer) {
        if (Nummer==0) return "IPv4 settings: address, netmask, gateway";
        if (Nummer==1) return "IPv4 interface and route tools";
        if (Nummer==2) return "ICMP echo and round-trip time";
        if (Nummer==3) return "Connected network and default route";
        if (Nummer==4) return "TCP/UDP sockets and traffic";
        if (Nummer==5) return "Kernel tasks and user processes";
        if (Nummer==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (Nummer==7) return "Actual kernel pools and user mappings";
        if (Nummer==8) return "RAM filesystem capacity and file slots";
        if (Nummer==9) return "Time since boot";
        if (Nummer==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
