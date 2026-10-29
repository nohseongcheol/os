// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String 말(int nalunaiqsimavik) {
        if (nalunaiqsimavik==0) return "ipconfig";
        if (nalunaiqsimavik==1) return "ip";
        if (nalunaiqsimavik==2) return "ping";
        if (nalunaiqsimavik==3) return "route";
        if (nalunaiqsimavik==4) return "netstat";
        if (nalunaiqsimavik==5) return "ps";
        if (nalunaiqsimavik==6) return "top";
        if (nalunaiqsimavik==7) return "free";
        if (nalunaiqsimavik==8) return "df";
        if (nalunaiqsimavik==9) return "uptime";
        if (nalunaiqsimavik==10) return "poweroff";
        return "help";
    }
    static String 설명(int nalunaiqsimavik) {
        if (nalunaiqsimavik==0) return "IPv4 settings: address, netmask, gateway";
        if (nalunaiqsimavik==1) return "IPv4 interface and route tools";
        if (nalunaiqsimavik==2) return "ICMP echo and round-trip time";
        if (nalunaiqsimavik==3) return "Connected network and default route";
        if (nalunaiqsimavik==4) return "TCP/UDP sockets and traffic";
        if (nalunaiqsimavik==5) return "Kernel tasks and user processes";
        if (nalunaiqsimavik==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (nalunaiqsimavik==7) return "Actual kernel pools and user mappings";
        if (nalunaiqsimavik==8) return "RAM filesystem capacity and file slots";
        if (nalunaiqsimavik==9) return "Time since boot";
        if (nalunaiqsimavik==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
