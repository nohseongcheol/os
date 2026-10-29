// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Dovršeno_Word() { return "ip-postavke mrežna-adresa provera-odziva putanje veze procesi aktivnost memorija skladište vreme-rada isključi pomoć"; }
    static String Word_SMS(int INDEX) {
        if (INDEX==0) return "ip-postavke";
        if (INDEX==1) return "mrežna-adresa";
        if (INDEX==2) return "provera-odziva";
        if (INDEX==3) return "putanje";
        if (INDEX==4) return "veze";
        if (INDEX==5) return "procesi";
        if (INDEX==6) return "aktivnost";
        if (INDEX==7) return "memorija";
        if (INDEX==8) return "skladište";
        if (INDEX==9) return "vreme-rada";
        if (INDEX==10) return "isključi";
        return "pomoć";
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
