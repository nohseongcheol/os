// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class LệnhQuảnTrị {
    static String từĐãHoànTất() { return "cấu-hình-ip địa-chỉ-mạng thử-phản-hồi đường-đi kết-nối tiến-trình hoạt-động bộ-nhớ lưu-trữ thời-gian-chạy tắt-máy trợ-giúp"; }
    static String vănBảnTừ(int sốHiệu) {
        if (sốHiệu==0) return "cấu-hình-ip";
        if (sốHiệu==1) return "địa-chỉ-mạng";
        if (sốHiệu==2) return "thử-phản-hồi";
        if (sốHiệu==3) return "đường-đi";
        if (sốHiệu==4) return "kết-nối";
        if (sốHiệu==5) return "tiến-trình";
        if (sốHiệu==6) return "hoạt-động";
        if (sốHiệu==7) return "bộ-nhớ";
        if (sốHiệu==8) return "lưu-trữ";
        if (sốHiệu==9) return "thời-gian-chạy";
        if (sốHiệu==10) return "tắt-máy";
        return "trợ-giúp";
    }
    static String môTả(int sốHiệu) {
        if (sốHiệu==0) return "IPv4 settings: address, netmask, gateway";
        if (sốHiệu==1) return "IPv4 interface and route tools";
        if (sốHiệu==2) return "ICMP echo and round-trip time";
        if (sốHiệu==3) return "Connected network and default route";
        if (sốHiệu==4) return "TCP/UDP sockets and traffic";
        if (sốHiệu==5) return "Kernel tasks and user processes";
        if (sốHiệu==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (sốHiệu==7) return "Actual kernel pools and user mappings";
        if (sốHiệu==8) return "RAM filesystem capacity and file slots";
        if (sốHiệu==9) return "Time since boot";
        if (sốHiệu==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
