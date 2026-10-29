// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ip-sozlamalari tarmoq-manzili aks-sado-sinovi yo‘nalishlar ulanishlar jarayonlar faoliyat xotira saqlash ishlash-vaqti o‘chirish yordam"; }
    static String Word_SMS(int INDEX) {
        if (INDEX==0) return "ip-sozlamalari";
        if (INDEX==1) return "tarmoq-manzili";
        if (INDEX==2) return "aks-sado-sinovi";
        if (INDEX==3) return "yo‘nalishlar";
        if (INDEX==4) return "ulanishlar";
        if (INDEX==5) return "jarayonlar";
        if (INDEX==6) return "faoliyat";
        if (INDEX==7) return "xotira";
        if (INDEX==8) return "saqlash";
        if (INDEX==9) return "ishlash-vaqti";
        if (INDEX==10) return "o‘chirish";
        return "yordam";
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
