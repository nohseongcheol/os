// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ජාලසැකසුම් ජාලලිපිනය ප්‍රතිචාරපරීක්ෂාව මාර්ග සම්බන්ධතා ක්‍රියාවලි ක්‍රියාකාරකම් මතකය ගබඩාව ක්‍රියාකාලය වසාදමන්න උදව්"; }
    static String 말(int සූචිය) {
        if (සූචිය==0) return "ජාලසැකසුම්";
        if (සූචිය==1) return "ජාලලිපිනය";
        if (සූචිය==2) return "ප්‍රතිචාරපරීක්ෂාව";
        if (සූචිය==3) return "මාර්ග";
        if (සූචිය==4) return "සම්බන්ධතා";
        if (සූචිය==5) return "ක්‍රියාවලි";
        if (සූචිය==6) return "ක්‍රියාකාරකම්";
        if (සූචිය==7) return "මතකය";
        if (සූචිය==8) return "ගබඩාව";
        if (සූචිය==9) return "ක්‍රියාකාලය";
        if (සූචිය==10) return "වසාදමන්න";
        return "උදව්";
    }
    static String 설명(int සූචිය) {
        if (සූචිය==0) return "IPv4 settings: address, netmask, gateway";
        if (සූචිය==1) return "IPv4 interface and route tools";
        if (සූචිය==2) return "ICMP echo and round-trip time";
        if (සූචිය==3) return "Connected network and default route";
        if (සූචිය==4) return "TCP/UDP sockets and traffic";
        if (සූචිය==5) return "Kernel tasks and user processes";
        if (සූචිය==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (සූචිය==7) return "Actual kernel pools and user mappings";
        if (සූචිය==8) return "RAM filesystem capacity and file slots";
        if (සූචිය==9) return "Time since boot";
        if (සූචිය==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
