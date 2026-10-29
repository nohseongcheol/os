// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Ολοκληρωμένες_λέξη() { return "ρύθμιση-ip διεύθυνση-ip δοκιμή-ηχούς διαδρομές συνδέσεις διεργασίες δραστηριότητα μνήμη αποθήκευση χρόνος-λειτουργίας τερματισμός βοήθεια"; }
    static String λέξη_μήνυμα(int Ευρετήριο) {
        if (Ευρετήριο==0) return "ρύθμιση-ip";
        if (Ευρετήριο==1) return "διεύθυνση-ip";
        if (Ευρετήριο==2) return "δοκιμή-ηχούς";
        if (Ευρετήριο==3) return "διαδρομές";
        if (Ευρετήριο==4) return "συνδέσεις";
        if (Ευρετήριο==5) return "διεργασίες";
        if (Ευρετήριο==6) return "δραστηριότητα";
        if (Ευρετήριο==7) return "μνήμη";
        if (Ευρετήριο==8) return "αποθήκευση";
        if (Ευρετήριο==9) return "χρόνος-λειτουργίας";
        if (Ευρετήριο==10) return "τερματισμός";
        return "βοήθεια";
    }
    static String 설명(int Ευρετήριο) {
        if (Ευρετήριο==0) return "IPv4 settings: address, netmask, gateway";
        if (Ευρετήριο==1) return "IPv4 interface and route tools";
        if (Ευρετήριο==2) return "ICMP echo and round-trip time";
        if (Ευρετήριο==3) return "Connected network and default route";
        if (Ευρετήριο==4) return "TCP/UDP sockets and traffic";
        if (Ευρετήριο==5) return "Kernel tasks and user processes";
        if (Ευρετήριο==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (Ευρετήριο==7) return "Actual kernel pools and user mappings";
        if (Ευρετήριο==8) return "RAM filesystem capacity and file slots";
        if (Ευρετήριο==9) return "Time since boot";
        if (Ευρετήριο==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
