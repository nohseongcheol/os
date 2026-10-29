// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Kész_szó() { return "ip-beállítás hálózati-cím visszhangpróba útvonalak kapcsolatok folyamatok tevékenység memória tárhely üzemidő kikapcsolás súgó"; }
    static String szó_SMS(int INDEX) {
        if (INDEX==0) return "ip-beállítás";
        if (INDEX==1) return "hálózati-cím";
        if (INDEX==2) return "visszhangpróba";
        if (INDEX==3) return "útvonalak";
        if (INDEX==4) return "kapcsolatok";
        if (INDEX==5) return "folyamatok";
        if (INDEX==6) return "tevékenység";
        if (INDEX==7) return "memória";
        if (INDEX==8) return "tárhely";
        if (INDEX==9) return "üzemidő";
        if (INDEX==10) return "kikapcsolás";
        return "súgó";
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
