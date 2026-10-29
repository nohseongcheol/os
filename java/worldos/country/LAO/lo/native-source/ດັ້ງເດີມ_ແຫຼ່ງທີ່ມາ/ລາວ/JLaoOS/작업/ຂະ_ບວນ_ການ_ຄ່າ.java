// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.작업;

import ລາວ.JLaoOS.기억공간.쪽관리자;
import ລາວ.JLaoOS.ລະບົບຟາຍ.파일서술자표;

public final class ຂະ_ບວນ_ການ_ຄ່າ {
    private final int ຕົວ_ກໍາ_ນົດ_ຄ່າ;
    private final int 부모식별자;
    private final 쪽관리자.ອີເມວ_ພື້ນທີ່ ອີເມວ_ພື້ນທີ່;
    private final 파일서술자표 파일서술자;
    private ຂະ_ບວນ_ການ_ສະຖານະ ສະຖານະ_ຄ່າ = ຂະ_ບວນ_ການ_ສະຖານະ.ກະ_ກຽມ;
    private int ອອກ_ລະຫັດ;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    ຂະ_ບວນ_ການ_ຄ່າ(int ຕົວ_ກໍາ_ນົດ_ຄ່າ, int 부모식별자, 쪽관리자.ອີເມວ_ພື້ນທີ່ ອີເມວ_ພື້ນທີ່, 파일서술자표 파일서술자) {
        this.ຕົວ_ກໍາ_ນົດ_ຄ່າ = ຕົວ_ກໍາ_ນົດ_ຄ່າ;
        this.부모식별자 = 부모식별자;
        this.ອີເມວ_ພື້ນທີ່ = ອີເມວ_ພື້ນທີ່;
        this.파일서술자 = 파일서술자;
    }

    public int ຕົວ_ກໍາ_ນົດ_ຄ່າ() {
        return ຕົວ_ກໍາ_ນົດ_ຄ່າ;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public 쪽관리자.ອີເມວ_ພື້ນທີ່ ອີເມວ_ພື້ນທີ່() {
        return ອີເມວ_ພື້ນທີ່;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public ຂະ_ບວນ_ການ_ສະຖານະ ສະຖານະ_ຄ່າ() {
        return ສະຖານະ_ຄ່າ;
    }

    public void ຊຸດ_ສະຖານະ(ຂະ_ບວນ_ການ_ສະຖານະ 새상태) {
        ສະຖານະ_ຄ່າ = 새상태;
    }

    public int ອອກ_ລະຫັດ() {
        return ອອກ_ລະຫັດ;
    }

    public void ອອກ_ແອັບ(int ຄ່າ) {
        ອອກ_ລະຫັດ = ຄ່າ & 0xff;
        ສະຖານະ_ຄ່າ = ຂະ_ບວນ_ການ_ສະຖານະ.ອອກ_ແອັບ;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("ແອັບ_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int ເລີ່ມ_ອີເມວ, String[] ພາຣາມິເຕີ_ຂໍ້ພິສູດ, String[] 환경) {
        실행시작주소 = ເລີ່ມ_ອີເມວ;
        실행인자 = ພາຣາມິເຕີ_ຂໍ້ພິສູດ.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
