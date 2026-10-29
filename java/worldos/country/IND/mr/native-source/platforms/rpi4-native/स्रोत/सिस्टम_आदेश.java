// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class सिस्टम_आदेश {
    static String पूर्णझालेले_शब्द() { return ""; }
    static String शब्द_मजकूर(int अनुक्रमणिका) {
        if (अनुक्रमणिका==0) return "ipconfig";
        if (अनुक्रमणिका==1) return "ip";
        if (अनुक्रमणिका==2) return "ping";
        if (अनुक्रमणिका==3) return "route";
        if (अनुक्रमणिका==4) return "netstat";
        if (अनुक्रमणिका==5) return "ps";
        if (अनुक्रमणिका==6) return "top";
        if (अनुक्रमणिका==7) return "free";
        if (अनुक्रमणिका==8) return "df";
        if (अनुक्रमणिका==9) return "uptime";
        if (अनुक्रमणिका==10) return "poweroff";
        return "help";
    }
    static String वर्णन(int अनुक्रमणिका) {
        if (अनुक्रमणिका==0) return "IPv4 settings: address, netmask, gateway";
        if (अनुक्रमणिका==1) return "IPv4 interface and route tools";
        if (अनुक्रमणिका==2) return "ICMP echo and round-trip time";
        if (अनुक्रमणिका==3) return "Connected network and default route";
        if (अनुक्रमणिका==4) return "TCP/UDP sockets and traffic";
        if (अनुक्रमणिका==5) return "Kernel tasks and user processes";
        if (अनुक्रमणिका==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (अनुक्रमणिका==7) return "Actual kernel pools and user mappings";
        if (अनुक्रमणिका==8) return "RAM filesystem capacity and file slots";
        if (अनुक्रमणिका==9) return "Time since boot";
        if (अनुक्रमणिका==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
