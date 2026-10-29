// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Voltooid_Word() { return "ip-instellen netwerkadres antwoordtest routes verbindingen processen activiteit geheugen opslag bedrijfstijd uitschakelen hulp"; }
    static String Word_sms(int INDEX) {
        if (INDEX==0) return "ip-instellen";
        if (INDEX==1) return "netwerkadres";
        if (INDEX==2) return "antwoordtest";
        if (INDEX==3) return "routes";
        if (INDEX==4) return "verbindingen";
        if (INDEX==5) return "processen";
        if (INDEX==6) return "activiteit";
        if (INDEX==7) return "geheugen";
        if (INDEX==8) return "opslag";
        if (INDEX==9) return "bedrijfstijd";
        if (INDEX==10) return "uitschakelen";
        return "hulp";
    }
    static String 설명(int INDEX) {
        if (INDEX==0) return "IPv4 settings: address, netmask, gateway";
        if (INDEX==1) return "IPv4 interface and route tools";
        if (INDEX==2) return "ICMP echo and round-trip time";
        if (INDEX==3) return "Connected network and default route";
        if (INDEX==4) return "TCP/UDP sockets and traffic";
        if (INDEX==5) return "Kernel tasks and user processes";
        if (INDEX==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (INDEX==7) return "Actual kernel pools and user mappings";
        if (INDEX==8) return "RAM filesystem capacity and file slots";
        if (INDEX==9) return "Time since boot";
        if (INDEX==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
