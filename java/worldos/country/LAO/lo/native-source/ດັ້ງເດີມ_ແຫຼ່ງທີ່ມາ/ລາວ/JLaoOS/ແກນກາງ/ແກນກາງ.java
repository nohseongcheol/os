// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.ແກນກາງ;

import ລາວ.JLaoOS.기억공간.기억공간관리자;
import ລາວ.JLaoOS.기억공간.쪽관리자;
import ລາວ.JLaoOS.입력.입력관리자;
import ລາວ.JLaoOS.작업.ຂະ_ບວນ_ການ_ຄ່າ;
import ລາວ.JLaoOS.작업.ຕົວກໍານົດການ;
import ລາວ.JLaoOS.체계호출.체계호출;
import ລາວ.JLaoOS.ລະບົບຟາຍ.파일서술자표;
import ລາວ.JLaoOS.ລະບົບຟາຍ.ລະບົບຟາຍ;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ແກນກາງ {
    private final 하드웨어 ມືຖື_ຄ່າ;
    private final 기억공간관리자 기억공간 = new 기억공간관리자(32 * 1024 * 1024);
    private final 쪽관리자 쪽관리 = new 쪽관리자();
    private final ລະບົບຟາຍ ລະບົບຟາຍ = new ລະບົບຟາຍ();
    private final ຕົວກໍານົດການ ຕົວກໍານົດການ = new ຕົວກໍານົດການ(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final ຂະ_ບວນ_ການ_ຄ່າ 첫과정;
    private final 체계호출 체계호출;

    public ແກນກາງ(하드웨어 ມືຖື_ຄ່າ) {
        this.ມືຖື_ຄ່າ = ມືຖື_ຄ່າ;
        첫과정 = ຕົວກໍານົດການ.첫과정(new 파일서술자표(ລະບົບຟາຍ));
        체계호출 = new 체계호출(ລະບົບຟາຍ, 쪽관리, ຕົວກໍານົດການ, ມືຖື_ຄ່າ, 입력관리);
    }

    public void ແລ່ນ() {
        ມືຖື_ຄ່າ.직렬출력("=== JLaoOS 관리 ແກນກາງ_ຄ່າ ===\n");
    }

    public void 한단계실행() {
        ມືຖື_ຄ່າ.중앙처리장치멈춤();
    }

    public 기억공간관리자 기억공간() {
        return 기억공간;
    }

    public 쪽관리자 쪽관리() {
        return 쪽관리;
    }

    public ລະບົບຟາຍ ລະບົບຟາຍ() {
        return ລະບົບຟາຍ;
    }

    public ຕົວກໍານົດການ ຕົວກໍານົດການ() {
        return ຕົວກໍານົດການ;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public ຂະ_ບວນ_ການ_ຄ່າ 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
