// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String سۆز_تېكست(int ئىندېكس) {
        if (ئىندېكس==0) return "ipconfig";
        if (ئىندېكس==1) return "ip";
        if (ئىندېكس==2) return "ping";
        if (ئىندېكس==3) return "route";
        if (ئىندېكس==4) return "netstat";
        if (ئىندېكس==5) return "ps";
        if (ئىندېكس==6) return "top";
        if (ئىندېكس==7) return "free";
        if (ئىندېكس==8) return "df";
        if (ئىندېكس==9) return "uptime";
        if (ئىندېكس==10) return "poweroff";
        return "help";
    }
    static String 설명(int ئىندېكس) {
        if (ئىندېكس==0) return "IPv4 settings: address, netmask, gateway";
        if (ئىندېكس==1) return "IPv4 interface and route tools";
        if (ئىندېكس==2) return "ICMP echo and round-trip time";
        if (ئىندېكس==3) return "Connected network and default route";
        if (ئىندېكس==4) return "TCP/UDP sockets and traffic";
        if (ئىندېكس==5) return "Kernel tasks and user processes";
        if (ئىندېكس==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ئىندېكس==7) return "Actual kernel pools and user mappings";
        if (ئىندېكس==8) return "RAM filesystem capacity and file slots";
        if (ئىندېكس==9) return "Time since boot";
        if (ئىندېكس==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
