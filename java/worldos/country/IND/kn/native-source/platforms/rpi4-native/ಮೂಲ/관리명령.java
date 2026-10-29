// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String ಪದ_ಪಠ್ಯ(int ಪದಸೂಚಿ) {
        if (ಪದಸೂಚಿ==0) return "ipconfig";
        if (ಪದಸೂಚಿ==1) return "ip";
        if (ಪದಸೂಚಿ==2) return "ping";
        if (ಪದಸೂಚಿ==3) return "route";
        if (ಪದಸೂಚಿ==4) return "netstat";
        if (ಪದಸೂಚಿ==5) return "ps";
        if (ಪದಸೂಚಿ==6) return "top";
        if (ಪದಸೂಚಿ==7) return "free";
        if (ಪದಸೂಚಿ==8) return "df";
        if (ಪದಸೂಚಿ==9) return "uptime";
        if (ಪದಸೂಚಿ==10) return "poweroff";
        return "help";
    }
    static String 설명(int ಪದಸೂಚಿ) {
        if (ಪದಸೂಚಿ==0) return "IPv4 settings: address, netmask, gateway";
        if (ಪದಸೂಚಿ==1) return "IPv4 interface and route tools";
        if (ಪದಸೂಚಿ==2) return "ICMP echo and round-trip time";
        if (ಪದಸೂಚಿ==3) return "Connected network and default route";
        if (ಪದಸೂಚಿ==4) return "TCP/UDP sockets and traffic";
        if (ಪದಸೂಚಿ==5) return "Kernel tasks and user processes";
        if (ಪದಸೂಚಿ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ಪದಸೂಚಿ==7) return "Actual kernel pools and user mappings";
        if (ಪದಸೂಚಿ==8) return "RAM filesystem capacity and file slots";
        if (ಪದಸೂಚಿ==9) return "Time since boot";
        if (ಪದಸೂಚಿ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
