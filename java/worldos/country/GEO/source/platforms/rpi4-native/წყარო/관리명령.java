// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ip-გამართვა ქსელის-მისამართი ექოს-შემოწმება მარშრუტები კავშირები პროცესები აქტივობა მეხსიერება საცავი მუშაობის-დრო გამორთვა დახმარება"; }
    static String სიტყვები_ტექსტი(int ინდექსი) {
        if (ინდექსი==0) return "ip-გამართვა";
        if (ინდექსი==1) return "ქსელის-მისამართი";
        if (ინდექსი==2) return "ექოს-შემოწმება";
        if (ინდექსი==3) return "მარშრუტები";
        if (ინდექსი==4) return "კავშირები";
        if (ინდექსი==5) return "პროცესები";
        if (ინდექსი==6) return "აქტივობა";
        if (ინდექსი==7) return "მეხსიერება";
        if (ინდექსი==8) return "საცავი";
        if (ინდექსი==9) return "მუშაობის-დრო";
        if (ინდექსი==10) return "გამორთვა";
        return "დახმარება";
    }
    static String 설명(int ინდექსი) {
        if (ინდექსი==0) return "IPv4 settings: address, netmask, gateway";
        if (ინდექსი==1) return "IPv4 interface and route tools";
        if (ინდექსი==2) return "ICMP echo and round-trip time";
        if (ინდექსი==3) return "Connected network and default route";
        if (ინდექსი==4) return "TCP/UDP sockets and traffic";
        if (ინდექსი==5) return "Kernel tasks and user processes";
        if (ინდექსი==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ინდექსი==7) return "Actual kernel pools and user mappings";
        if (ინდექსი==8) return "RAM filesystem capacity and file slots";
        if (ინდექსი==9) return "Time since boot";
        if (ინდექსი==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
