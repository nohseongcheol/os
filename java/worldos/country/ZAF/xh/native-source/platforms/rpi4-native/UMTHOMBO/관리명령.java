// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String Igama_I_SMS(int indeksa) {
        if (indeksa==0) return "ipconfig";
        if (indeksa==1) return "ip";
        if (indeksa==2) return "ping";
        if (indeksa==3) return "route";
        if (indeksa==4) return "netstat";
        if (indeksa==5) return "ps";
        if (indeksa==6) return "top";
        if (indeksa==7) return "free";
        if (indeksa==8) return "df";
        if (indeksa==9) return "uptime";
        if (indeksa==10) return "poweroff";
        return "help";
    }
    static String 설명(int indeksa) {
        if (indeksa==0) return "IPv4 settings: address, netmask, gateway";
        if (indeksa==1) return "IPv4 interface and route tools";
        if (indeksa==2) return "ICMP echo and round-trip time";
        if (indeksa==3) return "Connected network and default route";
        if (indeksa==4) return "TCP/UDP sockets and traffic";
        if (indeksa==5) return "Kernel tasks and user processes";
        if (indeksa==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (indeksa==7) return "Actual kernel pools and user mappings";
        if (indeksa==8) return "RAM filesystem capacity and file slots";
        if (indeksa==9) return "Time since boot";
        if (indeksa==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
