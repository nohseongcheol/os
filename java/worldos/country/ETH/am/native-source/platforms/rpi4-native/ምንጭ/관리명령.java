// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "አይፒ-ቅንብር የመረብ-አድራሻ የምላሽ-ሙከራ መንገዶች ግንኙነቶች ሂደቶች እንቅስቃሴ ማህደረ-ትውስታ ማከማቻ የሥራ-ጊዜ አጥፋ እገዛ"; }
    static String ቃል_ጽሁፍ(int መረጃ_ጠቆመ) {
        if (መረጃ_ጠቆመ==0) return "አይፒ-ቅንብር";
        if (መረጃ_ጠቆመ==1) return "የመረብ-አድራሻ";
        if (መረጃ_ጠቆመ==2) return "የምላሽ-ሙከራ";
        if (መረጃ_ጠቆመ==3) return "መንገዶች";
        if (መረጃ_ጠቆመ==4) return "ግንኙነቶች";
        if (መረጃ_ጠቆመ==5) return "ሂደቶች";
        if (መረጃ_ጠቆመ==6) return "እንቅስቃሴ";
        if (መረጃ_ጠቆመ==7) return "ማህደረ-ትውስታ";
        if (መረጃ_ጠቆመ==8) return "ማከማቻ";
        if (መረጃ_ጠቆመ==9) return "የሥራ-ጊዜ";
        if (መረጃ_ጠቆመ==10) return "አጥፋ";
        return "እገዛ";
    }
    static String 설명(int መረጃ_ጠቆመ) {
        if (መረጃ_ጠቆመ==0) return "IPv4 settings: address, netmask, gateway";
        if (መረጃ_ጠቆመ==1) return "IPv4 interface and route tools";
        if (መረጃ_ጠቆመ==2) return "ICMP echo and round-trip time";
        if (መረጃ_ጠቆመ==3) return "Connected network and default route";
        if (መረጃ_ጠቆመ==4) return "TCP/UDP sockets and traffic";
        if (መረጃ_ጠቆመ==5) return "Kernel tasks and user processes";
        if (መረጃ_ጠቆመ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (መረጃ_ጠቆመ==7) return "Actual kernel pools and user mappings";
        if (መረጃ_ጠቆመ==8) return "RAM filesystem capacity and file slots";
        if (መረጃ_ጠቆመ==9) return "Time since boot";
        if (መረጃ_ጠቆመ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
