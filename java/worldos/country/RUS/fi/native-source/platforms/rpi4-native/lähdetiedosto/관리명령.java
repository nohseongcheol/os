// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String valmis_Word() { return "ip-asetukset verkko-osoite kaikutesti reitit yhteydet prosessit toiminta muisti tallennustila käyntiaika sammuta ohje"; }
    static String Word_SMS(int INDEKSI) {
        if (INDEKSI==0) return "ip-asetukset";
        if (INDEKSI==1) return "verkko-osoite";
        if (INDEKSI==2) return "kaikutesti";
        if (INDEKSI==3) return "reitit";
        if (INDEKSI==4) return "yhteydet";
        if (INDEKSI==5) return "prosessit";
        if (INDEKSI==6) return "toiminta";
        if (INDEKSI==7) return "muisti";
        if (INDEKSI==8) return "tallennustila";
        if (INDEKSI==9) return "käyntiaika";
        if (INDEKSI==10) return "sammuta";
        return "ohje";
    }
    static String 설명(int INDEKSI) {
        if (INDEKSI==0) return "IPv4 settings: address, netmask, gateway";
        if (INDEKSI==1) return "IPv4 interface and route tools";
        if (INDEKSI==2) return "ICMP echo and round-trip time";
        if (INDEKSI==3) return "Connected network and default route";
        if (INDEKSI==4) return "TCP/UDP sockets and traffic";
        if (INDEKSI==5) return "Kernel tasks and user processes";
        if (INDEKSI==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (INDEKSI==7) return "Actual kernel pools and user mappings";
        if (INDEKSI==8) return "RAM filesystem capacity and file slots";
        if (INDEKSI==9) return "Time since boot";
        if (INDEKSI==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
