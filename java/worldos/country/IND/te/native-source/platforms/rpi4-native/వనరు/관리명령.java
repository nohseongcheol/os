// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String పదం_పాఠం(int సూచీ) {
        if (సూచీ==0) return "ipconfig";
        if (సూచీ==1) return "ip";
        if (సూచీ==2) return "ping";
        if (సూచీ==3) return "route";
        if (సూచీ==4) return "netstat";
        if (సూచీ==5) return "ps";
        if (సూచీ==6) return "top";
        if (సూచీ==7) return "free";
        if (సూచీ==8) return "df";
        if (సూచీ==9) return "uptime";
        if (సూచీ==10) return "poweroff";
        return "help";
    }
    static String 설명(int సూచీ) {
        if (సూచీ==0) return "IPv4 settings: address, netmask, gateway";
        if (సూచీ==1) return "IPv4 interface and route tools";
        if (సూచీ==2) return "ICMP echo and round-trip time";
        if (సూచీ==3) return "Connected network and default route";
        if (సూచీ==4) return "TCP/UDP sockets and traffic";
        if (సూచీ==5) return "Kernel tasks and user processes";
        if (సూచీ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (సూచీ==7) return "Actual kernel pools and user mappings";
        if (సూచీ==8) return "RAM filesystem capacity and file slots";
        if (సూచీ==9) return "Time since boot";
        if (సూచీ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
