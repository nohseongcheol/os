// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String Amagama_I_SMS(int thola_inkomba) {
        if (thola_inkomba==0) return "ipconfig";
        if (thola_inkomba==1) return "ip";
        if (thola_inkomba==2) return "ping";
        if (thola_inkomba==3) return "route";
        if (thola_inkomba==4) return "netstat";
        if (thola_inkomba==5) return "ps";
        if (thola_inkomba==6) return "top";
        if (thola_inkomba==7) return "free";
        if (thola_inkomba==8) return "df";
        if (thola_inkomba==9) return "uptime";
        if (thola_inkomba==10) return "poweroff";
        return "help";
    }
    static String 설명(int thola_inkomba) {
        if (thola_inkomba==0) return "IPv4 settings: address, netmask, gateway";
        if (thola_inkomba==1) return "IPv4 interface and route tools";
        if (thola_inkomba==2) return "ICMP echo and round-trip time";
        if (thola_inkomba==3) return "Connected network and default route";
        if (thola_inkomba==4) return "TCP/UDP sockets and traffic";
        if (thola_inkomba==5) return "Kernel tasks and user processes";
        if (thola_inkomba==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (thola_inkomba==7) return "Actual kernel pools and user mappings";
        if (thola_inkomba==8) return "RAM filesystem capacity and file slots";
        if (thola_inkomba==9) return "Time since boot";
        if (thola_inkomba==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
