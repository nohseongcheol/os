// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ip-ayarları şəbəkə-ünvanı əks-səda-sınağı marşrutlar bağlantılar proseslər fəaliyyət yaddaş saxlama işləmə-müddəti söndür kömək"; }
    static String Söz_SMS(int INDEX) {
        if (INDEX==0) return "ip-ayarları";
        if (INDEX==1) return "şəbəkə-ünvanı";
        if (INDEX==2) return "əks-səda-sınağı";
        if (INDEX==3) return "marşrutlar";
        if (INDEX==4) return "bağlantılar";
        if (INDEX==5) return "proseslər";
        if (INDEX==6) return "fəaliyyət";
        if (INDEX==7) return "yaddaş";
        if (INDEX==8) return "saxlama";
        if (INDEX==9) return "işləmə-müddəti";
        if (INDEX==10) return "söndür";
        return "kömək";
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
