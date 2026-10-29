// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.ໄອອາຄິວ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class 개입중단관리자 {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ວ່າງ;

    public void ລົງທະບຽນ_ເຂົ້າໃນ(int ດັດຊະນີ, 개입중단처리기 처리기) {
        번호확인(ດັດຊະນີ);
        처리기들[ດັດຊະນີ] = 처리기;
    }

    public void ເວີຊັນ_ບ່ອນເກັບຂໍ້ມູນ(int ດັດຊະນີ) {
        번호확인(ດັດຊະນີ);
        처리기들[ດັດຊະນີ] = null;
    }

    public int ແຈກ_ຢາຍ_ຄ່າ(int ດັດຊະນີ, int 저장된쌓임주소) {
        번호확인(ດັດຊະນີ);
        if (!ວ່າງ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ດັດຊະນີ];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.ຂະ_ບວນ_ການ_ຄ່າ_ເຂົ້າໃນ(저장된쌓임주소);
    }

    public void ເປີດ() {
        ວ່າງ = true;
    }

    public void ປິດ_ໃຊ້_ງານ() {
        ວ່າງ = false;
    }

    public boolean ເທັກໂນໂລຢີຂໍ້ມູນຂ່າວສານ_ວ່າງ() {
        return ວ່າງ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ດັດຊະນີ) {
        if (ດັດຊະນີ < 0 || ດັດຊະນີ >= 처리기들.length) {
            throw new IllegalArgumentException("ໄອອາຄິວ 번호가 올바르지 않습니다.");
        }
    }
}

