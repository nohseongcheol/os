// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String fuldført_Ord() { return "ip-indstillinger netadresse svartest ruter forbindelser processer aktivitet hukommelse lagerplads driftstid sluk hjælp"; }
    static String Ord_sms(int INDEKS) {
        if (INDEKS==0) return "ip-indstillinger";
        if (INDEKS==1) return "netadresse";
        if (INDEKS==2) return "svartest";
        if (INDEKS==3) return "ruter";
        if (INDEKS==4) return "forbindelser";
        if (INDEKS==5) return "processer";
        if (INDEKS==6) return "aktivitet";
        if (INDEKS==7) return "hukommelse";
        if (INDEKS==8) return "lagerplads";
        if (INDEKS==9) return "driftstid";
        if (INDEKS==10) return "sluk";
        return "hjælp";
    }
    static String 설명(int INDEKS) {
        if (INDEKS==0) return "IPv4 settings: address, netmask, gateway";
        if (INDEKS==1) return "IPv4 interface and route tools";
        if (INDEKS==2) return "ICMP echo and round-trip time";
        if (INDEKS==3) return "Connected network and default route";
        if (INDEKS==4) return "TCP/UDP sockets and traffic";
        if (INDEKS==5) return "Kernel tasks and user processes";
        if (INDEKS==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (INDEKS==7) return "Actual kernel pools and user mappings";
        if (INDEKS==8) return "RAM filesystem capacity and file slots";
        if (INDEKS==9) return "Time since boot";
        if (INDEKS==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
