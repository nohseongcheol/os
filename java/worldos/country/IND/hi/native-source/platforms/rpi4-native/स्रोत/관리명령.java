// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String पूर्ण_शब्द() { return "जाल-विन्यास जाल-पता प्रतिध्वनि-जाँच मार्ग प्रक्रिया-संपर्क प्रक्रियाएँ कार्य-स्थिति स्मृति भंडारण कार्य-अवधि बंद-करें सहायता"; }
    static String शब्द_पाठ(int इंडेक्स) {
        if (इंडेक्स==0) return "जाल-विन्यास";
        if (इंडेक्स==1) return "जाल-पता";
        if (इंडेक्स==2) return "प्रतिध्वनि-जाँच";
        if (इंडेक्स==3) return "मार्ग";
        if (इंडेक्स==4) return "प्रक्रिया-संपर्क";
        if (इंडेक्स==5) return "प्रक्रियाएँ";
        if (इंडेक्स==6) return "कार्य-स्थिति";
        if (इंडेक्स==7) return "स्मृति";
        if (इंडेक्स==8) return "भंडारण";
        if (इंडेक्स==9) return "कार्य-अवधि";
        if (इंडेक्स==10) return "बंद-करें";
        return "सहायता";
    }
    static String 설명(int इंडेक्स) {
        if (इंडेक्स==0) return "IPv4 settings: address, netmask, gateway";
        if (इंडेक्स==1) return "IPv4 interface and route tools";
        if (इंडेक्स==2) return "ICMP echo and round-trip time";
        if (इंडेक्स==3) return "Connected network and default route";
        if (इंडेक्स==4) return "TCP/UDP sockets and traffic";
        if (इंडेक्स==5) return "Kernel tasks and user processes";
        if (इंडेक्स==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (इंडेक्स==7) return "Actual kernel pools and user mappings";
        if (इंडेक्स==8) return "RAM filesystem capacity and file slots";
        if (इंडेक्स==9) return "Time since boot";
        if (इंडेक्स==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
