// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class CommandesAdministration {
    static String motAchevé() { return "configurer-ip adresse-ip tester-écho routes connexions processus activité mémoire stockage durée-active éteindre aide"; }
    static String texteMot(int numéro) {
        if (numéro==0) return "configurer-ip";
        if (numéro==1) return "adresse-ip";
        if (numéro==2) return "tester-écho";
        if (numéro==3) return "routes";
        if (numéro==4) return "connexions";
        if (numéro==5) return "processus";
        if (numéro==6) return "activité";
        if (numéro==7) return "mémoire";
        if (numéro==8) return "stockage";
        if (numéro==9) return "durée-active";
        if (numéro==10) return "éteindre";
        return "aide";
    }
    static String description(int numéro) {
        if (numéro==0) return "IPv4 settings: address, netmask, gateway";
        if (numéro==1) return "IPv4 interface and route tools";
        if (numéro==2) return "ICMP echo and round-trip time";
        if (numéro==3) return "Connected network and default route";
        if (numéro==4) return "TCP/UDP sockets and traffic";
        if (numéro==5) return "Kernel tasks and user processes";
        if (numéro==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (numéro==7) return "Actual kernel pools and user mappings";
        if (numéro==8) return "RAM filesystem capacity and file slots";
        if (numéro==9) return "Time since boot";
        if (numéro==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
