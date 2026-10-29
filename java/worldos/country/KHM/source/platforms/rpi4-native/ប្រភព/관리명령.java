// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "កំណត់បណ្ដាញ អាសយដ្ឋាន សាកល្បងចម្លើយ ផ្លូវ ការតភ្ជាប់ ដំណើរការ សកម្មភាព អង្គចងចាំ ទំហំផ្ទុក រយៈពេលដំណើរការ បិទម៉ាស៊ីន ជំនួយ"; }
    static String ពាក្យ_អត្ថបទ(int សន្ទស្សន៏) {
        if (សន្ទស្សន៏==0) return "កំណត់បណ្ដាញ";
        if (សន្ទស្សន៏==1) return "អាសយដ្ឋាន";
        if (សន្ទស្សន៏==2) return "សាកល្បងចម្លើយ";
        if (សន្ទស្សន៏==3) return "ផ្លូវ";
        if (សន្ទស្សន៏==4) return "ការតភ្ជាប់";
        if (សន្ទស្សន៏==5) return "ដំណើរការ";
        if (សន្ទស្សន៏==6) return "សកម្មភាព";
        if (សន្ទស្សន៏==7) return "អង្គចងចាំ";
        if (សន្ទស្សន៏==8) return "ទំហំផ្ទុក";
        if (សន្ទស្សន៏==9) return "រយៈពេលដំណើរការ";
        if (សន្ទស្សន៏==10) return "បិទម៉ាស៊ីន";
        return "ជំនួយ";
    }
    static String 설명(int សន្ទស្សន៏) {
        if (សន្ទស្សន៏==0) return "IPv4 settings: address, netmask, gateway";
        if (សន្ទស្សន៏==1) return "IPv4 interface and route tools";
        if (សន្ទស្សន៏==2) return "ICMP echo and round-trip time";
        if (សន្ទស្សន៏==3) return "Connected network and default route";
        if (សន្ទស្សន៏==4) return "TCP/UDP sockets and traffic";
        if (សន្ទស្សន៏==5) return "Kernel tasks and user processes";
        if (សន្ទស្សន៏==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (សន្ទស្សន៏==7) return "Actual kernel pools and user mappings";
        if (សន្ទស្សន៏==8) return "RAM filesystem capacity and file slots";
        if (សន្ទស្សន៏==9) return "Time since boot";
        if (សន្ទស្សន៏==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
