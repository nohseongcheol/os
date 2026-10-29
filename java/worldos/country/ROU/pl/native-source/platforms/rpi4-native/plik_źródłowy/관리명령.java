// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Wykonane_Word() { return "ustawienia-ip adres-sieci test-echa trasy połączenia procesy aktywność pamięć miejsce czas-pracy wyłącz pomoc"; }
    static String Word_SMS(int INDEKS) {
        if (INDEKS==0) return "ustawienia-ip";
        if (INDEKS==1) return "adres-sieci";
        if (INDEKS==2) return "test-echa";
        if (INDEKS==3) return "trasy";
        if (INDEKS==4) return "połączenia";
        if (INDEKS==5) return "procesy";
        if (INDEKS==6) return "aktywność";
        if (INDEKS==7) return "pamięć";
        if (INDEKS==8) return "miejsce";
        if (INDEKS==9) return "czas-pracy";
        if (INDEKS==10) return "wyłącz";
        return "pomoc";
    }
    static String 설명(int INDEKS) {
        if (INDEKS==0) return "IPv4 settings: address, netmask, gateway";
        if (INDEKS==1) return "IPv4 interface and route tools";
        if (INDEKS==2) return "ICMP echo and round-trip time";
        if (INDEKS==3) return "Connected network and default route";
        if (INDEKS==4) return "TCP/UDP sockets and traffic";
        if (INDEKS==5) return "Kernel tasks and user processes";
        if (INDEKS==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (INDEKS==7) return "Actual kernel pools and user mappings";
        if (INDEKS==8) return "RAM filesystem capacity and file slots";
        if (INDEKS==9) return "Time since boot";
        if (INDEKS==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
