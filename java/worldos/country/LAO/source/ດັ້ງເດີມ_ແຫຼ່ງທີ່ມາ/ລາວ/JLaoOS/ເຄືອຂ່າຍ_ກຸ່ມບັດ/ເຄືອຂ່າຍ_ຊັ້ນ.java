// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.ເຄືອຂ່າຍ_ກຸ່ມບັດ;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class ເຄືອຂ່າຍ_ຊັ້ນ {
    @FunctionalInterface
    public interface 자료처리기 {
        void ຂະ_ບວນ_ການ_ຄ່າ_ເຂົ້າໃນ(byte[] ຂໍ້ມູນ, int ແລ່ນ, int ຄວາມຍາວ_ຄ່າ);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void ລົງທະບຽນ_ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void ລົງທະບຽນ_ໄອພີ(int ສັນຍາ_ຄ່າ, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ສັນຍາ_ຄ່າ & 0xff), 처리기);
    }

    public void ລົງທະບຽນ_ຜູ້ໃຊ້_ຂໍ້ມູນ_ບົດຮຽນ(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void ລົງທະບຽນ_ການສົ່ງ_ຄວບຄຸມ(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ກອບ_ດັດຊະນີ) {
        if (!ເຄືອຂ່າຍ_ເຄື່ອງມື.ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ການເຊື່ອມຕໍ່ແບບຜ່ານສາຍ_ກອບ(ກອບ_ດັດຊະນີ)) {
            return false;
        }
        int 종류 = ເຄືອຂ່າຍ_ເຄື່ອງມື.이더넷상위규약(ກອບ_ດັດຊະນີ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.ຂະ_ບວນ_ການ_ຄ່າ_ເຂົ້າໃນ(ກອບ_ດັດຊະນີ, 14, ກອບ_ດັດຊະນີ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ກອບ_ດັດຊະນີ, 14);
    }

    private boolean 상호통신망받기(byte[] ຂໍ້ມູນ, int ແລ່ນ) {
        if (!ເຄືອຂ່າຍ_ເຄື່ອງມື.상호통신망규약사판인가(ຂໍ້ມູນ, ແລ່ນ)) {
            return false;
        }
        int ສ່ວນຫົວ_ຄວາມຍາວ = (ຂໍ້ມູນ[ແລ່ນ] & 0x0f) * 4;
        int 전체길이 = ເຄືອຂ່າຍ_ເຄື່ອງມື.큰순서짧은정수(ຂໍ້ມູນ, ແລ່ນ + 2);
        if (전체길이 < ສ່ວນຫົວ_ຄວາມຍາວ || ແລ່ນ + 전체길이 > ຂໍ້ມູນ.length) {
            return false;
        }
        int ສັນຍາ_ຄ່າ = ຂໍ້ມູນ[ແລ່ນ + 9] & 0xff;
        int ເນື້ອໃນ_ເລີ່ມ = ແລ່ນ + ສ່ວນຫົວ_ຄວາມຍາວ;
        int ເນື້ອໃນ_ຄວາມຍາວ = 전체길이 - ສ່ວນຫົວ_ຄວາມຍາວ;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ສັນຍາ_ຄ່າ));
        if (직접처리기 != null) {
            직접처리기.ຂະ_ບວນ_ການ_ຄ່າ_ເຂົ້າໃນ(ຂໍ້ມູນ, ເນື້ອໃນ_ເລີ່ມ, ເນື້ອໃນ_ຄວາມຍາວ);
            return true;
        }
        if (ເນື້ອໃນ_ຄວາມຍາວ < 4) {
            return false;
        }
        int ປາຍທາງ_ຫມາຍເລກພອດ = ເຄືອຂ່າຍ_ເຄື່ອງມື.큰순서짧은정수(ຂໍ້ມູນ, ເນື້ອໃນ_ເລີ່ມ + 2);
        Map<Integer, 자료처리기> ຜອດ_ຕາຕະລາງ = ສັນຍາ_ຄ່າ == 17 ? 사용자자료단위처리기 : ສັນຍາ_ຄ່າ == 6 ? 전송제어처리기 : null;
        if (ຜອດ_ຕາຕະລາງ == null) {
            return false;
        }
        자료처리기 포트처리기 = ຜອດ_ຕາຕະລາງ.get(Integer.valueOf(ປາຍທາງ_ຫມາຍເລກພອດ));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.ຂະ_ບວນ_ການ_ຄ່າ_ເຂົ້າໃນ(ຂໍ້ມູນ, ເນື້ອໃນ_ເລີ່ມ, ເນື້ອໃນ_ຄວາມຍາວ);
        return true;
    }
}

