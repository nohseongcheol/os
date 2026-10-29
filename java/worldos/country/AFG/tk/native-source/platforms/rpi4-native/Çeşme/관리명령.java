// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String Söz_SMS(int indeks) {
        if (indeks==0) return "ipconfig";
        if (indeks==1) return "ip";
        if (indeks==2) return "ping";
        if (indeks==3) return "route";
        if (indeks==4) return "netstat";
        if (indeks==5) return "ps";
        if (indeks==6) return "top";
        if (indeks==7) return "free";
        if (indeks==8) return "df";
        if (indeks==9) return "uptime";
        if (indeks==10) return "poweroff";
        return "help";
    }
    static String 설명(int indeks) {
        if (indeks==0) return "IPv4 settings: address, netmask, gateway";
        if (indeks==1) return "IPv4 interface and route tools";
        if (indeks==2) return "ICMP echo and round-trip time";
        if (indeks==3) return "Connected network and default route";
        if (indeks==4) return "TCP/UDP sockets and traffic";
        if (indeks==5) return "Kernel tasks and user processes";
        if (indeks==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (indeks==7) return "Actual kernel pools and user mappings";
        if (indeks==8) return "RAM filesystem capacity and file slots";
        if (indeks==9) return "Time since boot";
        if (indeks==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
