// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ip-sazlamalary tor-salgysy ýaň-synagy ugurlar baglanyşyklar prosesler işjeňlik ýat saklaýyş iş-wagty öçürmek kömek"; }
    static String Söz_SMS(int indeks) {
        if (indeks==0) return "ip-sazlamalary";
        if (indeks==1) return "tor-salgysy";
        if (indeks==2) return "ýaň-synagy";
        if (indeks==3) return "ugurlar";
        if (indeks==4) return "baglanyşyklar";
        if (indeks==5) return "prosesler";
        if (indeks==6) return "işjeňlik";
        if (indeks==7) return "ýat";
        if (indeks==8) return "saklaýyş";
        if (indeks==9) return "iş-wagty";
        if (indeks==10) return "öçürmek";
        return "kömek";
    }
    static String 설명(int indeks) {
        if (indeks==0) return "IPv4 settings: address, netmask, gateway";
        if (indeks==1) return "IPv4 interface and route tools";
        if (indeks==2) return "ICMP echo and round-trip time";
        if (indeks==3) return "Connected network and default route";
        if (indeks==4) return "TCP/UDP sockets and traffic";
        if (indeks==5) return "Kernel tasks and user processes";
        if (indeks==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (indeks==7) return "Actual kernel pools and user mappings";
        if (indeks==8) return "RAM filesystem capacity and file slots";
        if (indeks==9) return "Time since boot";
        if (indeks==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
