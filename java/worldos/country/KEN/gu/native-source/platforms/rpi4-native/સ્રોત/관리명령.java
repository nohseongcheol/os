// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String શબ્દ_પાઠ(int અનુક્રમણિકા) {
        if (અનુક્રમણિકા==0) return "ipconfig";
        if (અનુક્રમણિકા==1) return "ip";
        if (અનુક્રમણિકા==2) return "ping";
        if (અનુક્રમણિકા==3) return "route";
        if (અનુક્રમણિકા==4) return "netstat";
        if (અનુક્રમણિકા==5) return "ps";
        if (અનુક્રમણિકા==6) return "top";
        if (અનુક્રમણિકા==7) return "free";
        if (અનુક્રમણિકા==8) return "df";
        if (અનુક્રમણિકા==9) return "uptime";
        if (અનુક્રમણિકા==10) return "poweroff";
        return "help";
    }
    static String 설명(int અનુક્રમણિકા) {
        if (અનુક્રમણિકા==0) return "IPv4 settings: address, netmask, gateway";
        if (અનુક્રમણિકા==1) return "IPv4 interface and route tools";
        if (અનુક્રમણિકા==2) return "ICMP echo and round-trip time";
        if (અનુક્રમણિકા==3) return "Connected network and default route";
        if (અનુક્રમણિકા==4) return "TCP/UDP sockets and traffic";
        if (અનુક્રમણિકા==5) return "Kernel tasks and user processes";
        if (અનુક્રમણિકા==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (અનુક્રમણિકા==7) return "Actual kernel pools and user mappings";
        if (અનુક્રમણિકા==8) return "RAM filesystem capacity and file slots";
        if (અનુક્રમણિકા==9) return "Time since boot";
        if (અનુક્રમણિકા==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
