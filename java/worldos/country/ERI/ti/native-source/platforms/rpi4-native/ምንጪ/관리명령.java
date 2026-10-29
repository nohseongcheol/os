// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ኣድራሻ መንገዲ ዝኽሪ መኽዘን ኣጥፍእ ሓገዝ"; }
    static String ናይ_ቃል_ጸወታ_ጽሑፍ(int መሐበሪ) {
        if (መሐበሪ==0) return "ipconfig";
        if (መሐበሪ==1) return "ኣድራሻ";
        if (መሐበሪ==2) return "ping";
        if (መሐበሪ==3) return "መንገዲ";
        if (መሐበሪ==4) return "netstat";
        if (መሐበሪ==5) return "ps";
        if (መሐበሪ==6) return "top";
        if (መሐበሪ==7) return "ዝኽሪ";
        if (መሐበሪ==8) return "መኽዘን";
        if (መሐበሪ==9) return "uptime";
        if (መሐበሪ==10) return "ኣጥፍእ";
        return "ሓገዝ";
    }
    static String 설명(int መሐበሪ) {
        if (መሐበሪ==0) return "IPv4 settings: address, netmask, gateway";
        if (መሐበሪ==1) return "IPv4 interface and route tools";
        if (መሐበሪ==2) return "ICMP echo and round-trip time";
        if (መሐበሪ==3) return "Connected network and default route";
        if (መሐበሪ==4) return "TCP/UDP sockets and traffic";
        if (መሐበሪ==5) return "Kernel tasks and user processes";
        if (መሐበሪ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (መሐበሪ==7) return "Actual kernel pools and user mappings";
        if (መሐበሪ==8) return "RAM filesystem capacity and file slots";
        if (መሐበሪ==9) return "Time since boot";
        if (መሐበሪ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
