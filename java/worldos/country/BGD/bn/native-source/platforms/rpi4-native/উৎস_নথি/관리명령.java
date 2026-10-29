// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "নেট-বিন্যাস নেট-ঠিকানা প্রতিধ্বনি-পরীক্ষা পথ সংযোগ প্রক্রিয়া কাজের-অবস্থা স্মৃতি সংরক্ষণ চলমান-সময় বন্ধ-করুন সাহায্য"; }
    static String শব্দ_পাঠ(int সূচি) {
        if (সূচি==0) return "নেট-বিন্যাস";
        if (সূচি==1) return "নেট-ঠিকানা";
        if (সূচি==2) return "প্রতিধ্বনি-পরীক্ষা";
        if (সূচি==3) return "পথ";
        if (সূচি==4) return "সংযোগ";
        if (সূচি==5) return "প্রক্রিয়া";
        if (সূচি==6) return "কাজের-অবস্থা";
        if (সূচি==7) return "স্মৃতি";
        if (সূচি==8) return "সংরক্ষণ";
        if (সূচি==9) return "চলমান-সময়";
        if (সূচি==10) return "বন্ধ-করুন";
        return "সাহায্য";
    }
    static String 설명(int সূচি) {
        if (সূচি==0) return "IPv4 settings: address, netmask, gateway";
        if (সূচি==1) return "IPv4 interface and route tools";
        if (সূচি==2) return "ICMP echo and round-trip time";
        if (সূচি==3) return "Connected network and default route";
        if (সূচি==4) return "TCP/UDP sockets and traffic";
        if (সূচি==5) return "Kernel tasks and user processes";
        if (সূচি==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (সূচি==7) return "Actual kernel pools and user mappings";
        if (সূচি==8) return "RAM filesystem capacity and file slots";
        if (সূচি==9) return "Time since boot";
        if (সূচি==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
