// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.ບ່ອນເກັບຂໍ້ມູນ_ມືຖື;

import java.util.Arrays;

/** ATA 28비트 ຄໍາສັ່ງ_1f12b8e2 계층과 같은 512바이트 논리 ຕອນ_ຄ່າ 장치다. */
public final class 고급기술결합장치 {
    public static final int ຕອນ_ຂະ_ຫນາດ = 512;
    private final byte[] ຂໍ້ມູນ;
    private final boolean ອ່ານ_ເທົ່າ_ນັ້ນ_ຄ່າ;

    public 고급기술결합장치(int 구역수, boolean ອ່ານ_ເທົ່າ_ນັ້ນ_ຄ່າ) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ຕອນ_ຄ່າ 수가 올바르지 않습니다.");
        }
        ຂໍ້ມູນ = new byte[Math.multiplyExact(구역수, ຕອນ_ຂະ_ຫນາດ)];
        this.ອ່ານ_ເທົ່າ_ນັ້ນ_ຄ່າ = ອ່ານ_ເທົ່າ_ນັ້ນ_ຄ່າ;
    }

    public int 구역수() {
        return ຂໍ້ມູນ.length / ຕອນ_ຂະ_ຫນາດ;
    }

    public void 읽기(int ຕອນ_ດັດຊະນີ, byte[] 받을곳) {
        범위확인(ຕອນ_ດັດຊະນີ, 받을곳);
        System.arraycopy(ຂໍ້ມູນ, ຕອນ_ດັດຊະນີ * ຕອນ_ຂະ_ຫນາດ, 받을곳, 0, ຕອນ_ຂະ_ຫນາດ);
    }

    public void ຂຽນ(int ຕອນ_ດັດຊະນີ, byte[] 쓸자료) {
        if (ອ່ານ_ເທົ່າ_ນັ້ນ_ຄ່າ) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(ຕອນ_ດັດຊະນີ, 쓸자료);
        System.arraycopy(쓸자료, 0, ຂໍ້ມູນ, ຕອນ_ດັດຊະນີ * ຕອນ_ຂະ_ຫນາດ, ຕອນ_ຂະ_ຫນາດ);
    }

    public void ລຶບ_ເຂົ້າໃນ() {
        if (ອ່ານ_ເທົ່າ_ນັ້ນ_ຄ່າ) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(ຂໍ້ມູນ, (byte) 0);
    }

    private void 범위확인(int ຕອນ_ດັດຊະນີ, byte[] 임시공간) {
        if (ຕອນ_ດັດຊະນີ < 0 || ຕອນ_ດັດຊະນີ >= 구역수() || 임시공간.length < ຕອນ_ຂະ_ຫນາດ) {
            throw new IllegalArgumentException("ATA ຕອນ_ຄ່າ 범위가 올바르지 않습니다.");
        }
    }
}

