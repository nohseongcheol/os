// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "सञ्जाल-विन्यास सञ्जाल-ठेगाना प्रतिध्वनि-परीक्षण मार्ग जडान प्रक्रिया कार्य-स्थिति स्मृति भण्डारण चल्ने-अवधि बन्द-गर्नुहोस् सहायता"; }
    static String शब्द_पाठ(int अनुक्रमणिका) {
        if (अनुक्रमणिका==0) return "सञ्जाल-विन्यास";
        if (अनुक्रमणिका==1) return "सञ्जाल-ठेगाना";
        if (अनुक्रमणिका==2) return "प्रतिध्वनि-परीक्षण";
        if (अनुक्रमणिका==3) return "मार्ग";
        if (अनुक्रमणिका==4) return "जडान";
        if (अनुक्रमणिका==5) return "प्रक्रिया";
        if (अनुक्रमणिका==6) return "कार्य-स्थिति";
        if (अनुक्रमणिका==7) return "स्मृति";
        if (अनुक्रमणिका==8) return "भण्डारण";
        if (अनुक्रमणिका==9) return "चल्ने-अवधि";
        if (अनुक्रमणिका==10) return "बन्द-गर्नुहोस्";
        return "सहायता";
    }
    static String 설명(int अनुक्रमणिका) {
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
