// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Completate_Word() { return "configura-ip indirizzo-ip prova-eco percorsi connessioni processi attività memoria archiviazione tempo-attivo spegni aiuto"; }
    static String Word_SMS(int INDICE) {
        if (INDICE==0) return "configura-ip";
        if (INDICE==1) return "indirizzo-ip";
        if (INDICE==2) return "prova-eco";
        if (INDICE==3) return "percorsi";
        if (INDICE==4) return "connessioni";
        if (INDICE==5) return "processi";
        if (INDICE==6) return "attività";
        if (INDICE==7) return "memoria";
        if (INDICE==8) return "archiviazione";
        if (INDICE==9) return "tempo-attivo";
        if (INDICE==10) return "spegni";
        return "aiuto";
    }
    static String 설명(int INDICE) {
        if (INDICE==0) return "IPv4 settings: address, netmask, gateway";
        if (INDICE==1) return "IPv4 interface and route tools";
        if (INDICE==2) return "ICMP echo and round-trip time";
        if (INDICE==3) return "Connected network and default route";
        if (INDICE==4) return "TCP/UDP sockets and traffic";
        if (INDICE==5) return "Kernel tasks and user processes";
        if (INDICE==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (INDICE==7) return "Actual kernel pools and user mappings";
        if (INDICE==8) return "RAM filesystem capacity and file slots";
        if (INDICE==9) return "Time since boot";
        if (INDICE==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
