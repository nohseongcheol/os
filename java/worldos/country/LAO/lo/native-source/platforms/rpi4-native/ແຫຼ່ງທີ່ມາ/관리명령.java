// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ຕັ້ງຄ່າເຄືອຂ່າຍ ທີ່ຢູ່ ທົດສອບຕອບກັບ ເສັ້ນທາງ ການເຊື່ອມຕໍ່ ຂະບວນການ ກິດຈະກຳ ຄວາມຈຳ ພື້ນທີ່ເກັບ ເວລາເຮັດວຽກ ປິດເຄື່ອງ ຊ່ວຍເຫຼືອ"; }
    static String ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ(int ດັດຊະນີ) {
        if (ດັດຊະນີ==0) return "ຕັ້ງຄ່າເຄືອຂ່າຍ";
        if (ດັດຊະນີ==1) return "ທີ່ຢູ່";
        if (ດັດຊະນີ==2) return "ທົດສອບຕອບກັບ";
        if (ດັດຊະນີ==3) return "ເສັ້ນທາງ";
        if (ດັດຊະນີ==4) return "ການເຊື່ອມຕໍ່";
        if (ດັດຊະນີ==5) return "ຂະບວນການ";
        if (ດັດຊະນີ==6) return "ກິດຈະກຳ";
        if (ດັດຊະນີ==7) return "ຄວາມຈຳ";
        if (ດັດຊະນີ==8) return "ພື້ນທີ່ເກັບ";
        if (ດັດຊະນີ==9) return "ເວລາເຮັດວຽກ";
        if (ດັດຊະນີ==10) return "ປິດເຄື່ອງ";
        return "ຊ່ວຍເຫຼືອ";
    }
    static String 설명(int ດັດຊະນີ) {
        if (ດັດຊະນີ==0) return "IPv4 settings: address, netmask, gateway";
        if (ດັດຊະນີ==1) return "IPv4 interface and route tools";
        if (ດັດຊະນີ==2) return "ICMP echo and round-trip time";
        if (ດັດຊະນີ==3) return "Connected network and default route";
        if (ດັດຊະນີ==4) return "TCP/UDP sockets and traffic";
        if (ດັດຊະນີ==5) return "Kernel tasks and user processes";
        if (ດັດຊະນີ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ດັດຊະນີ==7) return "Actual kernel pools and user mappings";
        if (ດັດຊະນີ==8) return "RAM filesystem capacity and file slots";
        if (ດັດຊະນີ==9) return "Time since boot";
        if (ດັດຊະນີ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
