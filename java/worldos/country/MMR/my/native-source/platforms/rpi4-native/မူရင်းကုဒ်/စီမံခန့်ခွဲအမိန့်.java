// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class စီမံခန့်ခွဲအမိန့် {
    static String ပြီးစီးစကားလုံး() { return "ကွန်ရက်ချိန်ညှိ ကွန်ရက်လိပ်စာ တုံ့ပြန်မှုစမ်းသပ် လမ်းကြောင်း ချိတ်ဆက်မှု လုပ်ငန်းစဉ် လုပ်ဆောင်မှု မှတ်ဉာဏ် သိုလှောင်နေရာ အလုပ်လုပ်ချိန် စက်ပိတ် အကူအညီ"; }
    static String စကားလုံးစာသား(int နံပါတ်) {
        if (နံပါတ်==0) return "ကွန်ရက်ချိန်ညှိ";
        if (နံပါတ်==1) return "ကွန်ရက်လိပ်စာ";
        if (နံပါတ်==2) return "တုံ့ပြန်မှုစမ်းသပ်";
        if (နံပါတ်==3) return "လမ်းကြောင်း";
        if (နံပါတ်==4) return "ချိတ်ဆက်မှု";
        if (နံပါတ်==5) return "လုပ်ငန်းစဉ်";
        if (နံပါတ်==6) return "လုပ်ဆောင်မှု";
        if (နံပါတ်==7) return "မှတ်ဉာဏ်";
        if (နံပါတ်==8) return "သိုလှောင်နေရာ";
        if (နံပါတ်==9) return "အလုပ်လုပ်ချိန်";
        if (နံပါတ်==10) return "စက်ပိတ်";
        return "အကူအညီ";
    }
    static String ရှင်းလင်းချက်(int နံပါတ်) {
        if (နံပါတ်==0) return "IPv4 settings: address, netmask, gateway";
        if (နံပါတ်==1) return "IPv4 interface and route tools";
        if (နံပါတ်==2) return "ICMP echo and round-trip time";
        if (နံပါတ်==3) return "Connected network and default route";
        if (နံပါတ်==4) return "TCP/UDP sockets and traffic";
        if (နံပါတ်==5) return "Kernel tasks and user processes";
        if (နံပါတ်==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (နံပါတ်==7) return "Actual kernel pools and user mappings";
        if (နံပါတ်==8) return "RAM filesystem capacity and file slots";
        if (နံပါတ်==9) return "Time since boot";
        if (နံပါတ်==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
