// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String Mkpụrụokwu_SMS(int indèks) {
        if (indèks==0) return "ipconfig";
        if (indèks==1) return "ip";
        if (indèks==2) return "ping";
        if (indèks==3) return "route";
        if (indèks==4) return "netstat";
        if (indèks==5) return "ps";
        if (indèks==6) return "top";
        if (indèks==7) return "free";
        if (indèks==8) return "df";
        if (indèks==9) return "uptime";
        if (indèks==10) return "poweroff";
        return "help";
    }
    static String 설명(int indèks) {
        if (indèks==0) return "IPv4 settings: address, netmask, gateway";
        if (indèks==1) return "IPv4 interface and route tools";
        if (indèks==2) return "ICMP echo and round-trip time";
        if (indèks==3) return "Connected network and default route";
        if (indèks==4) return "TCP/UDP sockets and traffic";
        if (indèks==5) return "Kernel tasks and user processes";
        if (indèks==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (indèks==7) return "Actual kernel pools and user mappings";
        if (indèks==8) return "RAM filesystem capacity and file slots";
        if (indèks==9) return "Time since boot";
        if (indèks==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
