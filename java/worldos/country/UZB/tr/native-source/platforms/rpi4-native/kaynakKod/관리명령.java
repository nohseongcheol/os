// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Bitenler_Word() { return "ip-ayarları ağ-adresi yankı-sınaması yollar bağlantılar süreçler etkinlik bellek depolama çalışma-süresi kapat yardım"; }
    static String Word_SMS(int Dizin) {
        if (Dizin==0) return "ip-ayarları";
        if (Dizin==1) return "ağ-adresi";
        if (Dizin==2) return "yankı-sınaması";
        if (Dizin==3) return "yollar";
        if (Dizin==4) return "bağlantılar";
        if (Dizin==5) return "süreçler";
        if (Dizin==6) return "etkinlik";
        if (Dizin==7) return "bellek";
        if (Dizin==8) return "depolama";
        if (Dizin==9) return "çalışma-süresi";
        if (Dizin==10) return "kapat";
        return "yardım";
    }
    static String 설명(int Dizin) {
        if (Dizin==0) return "IPv4 settings: address, netmask, gateway";
        if (Dizin==1) return "IPv4 interface and route tools";
        if (Dizin==2) return "ICMP echo and round-trip time";
        if (Dizin==3) return "Connected network and default route";
        if (Dizin==4) return "TCP/UDP sockets and traffic";
        if (Dizin==5) return "Kernel tasks and user processes";
        if (Dizin==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (Dizin==7) return "Actual kernel pools and user mappings";
        if (Dizin==8) return "RAM filesystem capacity and file slots";
        if (Dizin==9) return "Time since boot";
        if (Dizin==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
