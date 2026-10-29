// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class SystemCommands {
    static String completedWord() { return "address-settings address echo-test routes connections processes activity memory storage running-time shut-down assistance"; }
    static String wordText(int index) {
        if (index==0) return "address-settings";
        if (index==1) return "address";
        if (index==2) return "echo-test";
        if (index==3) return "routes";
        if (index==4) return "connections";
        if (index==5) return "processes";
        if (index==6) return "activity";
        if (index==7) return "memory";
        if (index==8) return "storage";
        if (index==9) return "running-time";
        if (index==10) return "shut-down";
        return "assistance";
    }
    static String description(int index) {
        if (index==0) return "IPv4 settings: address, netmask, gateway";
        if (index==1) return "IPv4 interface and route tools";
        if (index==2) return "ICMP echo and round-trip time";
        if (index==3) return "Connected network and default route";
        if (index==4) return "TCP/UDP sockets and traffic";
        if (index==5) return "Kernel tasks and user processes";
        if (index==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (index==7) return "Actual kernel pools and user mappings";
        if (index==8) return "RAM filesystem capacity and file slots";
        if (index==9) return "Time since boot";
        if (index==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
