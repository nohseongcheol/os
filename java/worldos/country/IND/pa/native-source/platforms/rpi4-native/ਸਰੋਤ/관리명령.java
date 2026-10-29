// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String ਸ਼ਬਦ_ਪਾਠ(int ਅਨੁਕ੍ਰਮਣਿਕਾ) {
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==0) return "ipconfig";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==1) return "ip";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==2) return "ping";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==3) return "route";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==4) return "netstat";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==5) return "ps";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==6) return "top";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==7) return "free";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==8) return "df";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==9) return "uptime";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==10) return "poweroff";
        return "help";
    }
    static String 설명(int ਅਨੁਕ੍ਰਮਣਿਕਾ) {
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==0) return "IPv4 settings: address, netmask, gateway";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==1) return "IPv4 interface and route tools";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==2) return "ICMP echo and round-trip time";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==3) return "Connected network and default route";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==4) return "TCP/UDP sockets and traffic";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==5) return "Kernel tasks and user processes";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==7) return "Actual kernel pools and user mappings";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==8) return "RAM filesystem capacity and file slots";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==9) return "Time since boot";
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
