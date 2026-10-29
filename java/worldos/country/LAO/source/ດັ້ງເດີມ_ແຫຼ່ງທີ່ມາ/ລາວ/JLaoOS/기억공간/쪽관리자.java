// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ຫນ້າ_ຄ່າ 연결과 ຂຽນ 시 복사를 제공한다. */
public final class 쪽관리자 {
    public static final int ຂະ_ຫນາດ_ຫນ້າ = 4096;

    private static final class ຫນ້າ_ຄ່າ {
        private byte[] ຂໍ້ມູນ = new byte[ຂະ_ຫນາດ_ຫນ້າ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ອີເມວ_ພື້ນທີ່ {
        private final Map<Integer, ຫນ້າ_ຄ່າ> ຫນ້າ_ຕາຕະລາງ = new HashMap<Integer, ຫນ້າ_ຄ່າ>();
    }

    public ອີເມວ_ພື້ນທີ່ 새주소공간() {
        return new ອີເມວ_ພື້ນທີ່();
    }

    public void ແຜນທີ່_ຫນ້າ(ອີເມວ_ພື້ນທີ່ 공간, int ທີ່ຢູ່ຈໍາລອງ, boolean 쓰기가능) {
        int ດັດຊະນີ = 쪽번호(ທີ່ຢູ່ຈໍາລອງ);
        ຫນ້າ_ຄ່າ 새쪽 = new ຫນ້າ_ຄ່າ();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ຫນ້າ_ຕາຕະລາງ.put(Integer.valueOf(ດັດຊະນີ), 새쪽);
    }

    public ອີເມວ_ພື້ນທີ່ 쓰기시복사복제(ອີເມວ_ພື້ນທີ່ 원본) {
        ອີເມວ_ພື້ນທີ່ 복제본 = new ອີເມວ_ພື້ນທີ່();
        for (Map.Entry<Integer, ຫນ້າ_ຄ່າ> ເຂົ້າໃນ_ຄ່າ : 원본.ຫນ້າ_ຕາຕະລາງ.entrySet()) {
            ຫນ້າ_ຄ່າ 공유쪽 = ເຂົ້າໃນ_ຄ່າ.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ຫນ້າ_ຕາຕະລາງ.put(ເຂົ້າໃນ_ຄ່າ.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ອີເມວ_ພື້ນທີ່ 공간, int ທີ່ຢູ່ຈໍາລອງ) {
        ຫນ້າ_ຄ່າ ເປົ້າ_ຫມາຍ = ຊອກຫາ_ຫນ້າ(공간, ທີ່ຢູ່ຈໍາລອງ);
        return ເປົ້າ_ຫມາຍ.ຂໍ້ມູນ[Math.floorMod(ທີ່ຢູ່ຈໍາລອງ, ຂະ_ຫນາດ_ຫນ້າ)];
    }

    public void ຂຽນ_ໄບ_ຄ່າ(ອີເມວ_ພື້ນທີ່ 공간, int ທີ່ຢູ່ຈໍາລອງ, byte ຄ່າ) {
        int ດັດຊະນີ = 쪽번호(ທີ່ຢູ່ຈໍາລອງ);
        ຫນ້າ_ຄ່າ ເປົ້າ_ຫມາຍ = ຊອກຫາ_ຫນ້າ(공간, ທີ່ຢູ່ຈໍາລອງ);
        if (!ເປົ້າ_ຫມາຍ.쓰기가능) {
            if (!ເປົ້າ_ຫມາຍ.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            ເປົ້າ_ຫມາຍ = ສ້າງ_ສ່ວນຕົວ_ຫນ້າ(공간, ດັດຊະນີ, ເປົ້າ_ຫມາຍ);
        }
        ເປົ້າ_ຫມາຍ.ຂໍ້ມູນ[Math.floorMod(ທີ່ຢູ່ຈໍາລອງ, ຂະ_ຫນາດ_ຫນ້າ)] = ຄ່າ;
    }

    public void 범위개인쓰기(ອີເມວ_ພື້ນທີ່ 공간, int ເລີ່ມ_ອີເມວ, int ຂະ_ຫນາດ) {
        if (ຂະ_ຫນາດ < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ຈົບ_ອີເມວ = Math.addExact(ເລີ່ມ_ອີເມວ, ຂະ_ຫນາດ);
        for (int ອີເມວ = ເລີ່ມ_ອີເມວ; ອີເມວ < ຈົບ_ອີເມວ; ອີເມວ = (쪽번호(ອີເມວ) + 1) * ຂະ_ຫນາດ_ຫນ້າ) {
            int ດັດຊະນີ = 쪽번호(ອີເມວ);
            ຫນ້າ_ຄ່າ ເປົ້າ_ຫມາຍ = ຊອກຫາ_ຫນ້າ(공간, ອີເມວ);
            if (ເປົ້າ_ຫມາຍ.쓰기시복사) {
                ສ້າງ_ສ່ວນຕົວ_ຫນ້າ(공간, ດັດຊະນີ, ເປົ້າ_ຫມາຍ);
            } else {
                ເປົ້າ_ຫມາຍ.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ອີເມວ_ພື້ນທີ່ 공간, int ເລີ່ມ_ອີເມວ, byte[] ຂໍ້ມູນ) {
        for (int ດັດຊະນີ = 0; ດັດຊະນີ < ຂໍ້ມູນ.length; ດັດຊະນີ++) {
            ຂຽນ_ໄບ_ຄ່າ(공간, ເລີ່ມ_ອີເມວ + ດັດຊະນີ, ຂໍ້ມູນ[ດັດຊະນີ]);
        }
    }

    private ຫນ້າ_ຄ່າ ສ້າງ_ສ່ວນຕົວ_ຫນ້າ(ອີເມວ_ພື້ນທີ່ 공간, int ດັດຊະນີ, ຫນ້າ_ຄ່າ 공유쪽) {
        ຫນ້າ_ຄ່າ ສ່ວນຕົວ_ຫນ້າ = new ຫນ້າ_ຄ່າ();
        ສ່ວນຕົວ_ຫນ້າ.ຂໍ້ມູນ = Arrays.copyOf(공유쪽.ຂໍ້ມູນ, 공유쪽.ຂໍ້ມູນ.length);
        ສ່ວນຕົວ_ຫນ້າ.쓰기가능 = true;
        ສ່ວນຕົວ_ຫນ້າ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ຫນ້າ_ຕາຕະລາງ.put(Integer.valueOf(ດັດຊະນີ), ສ່ວນຕົວ_ຫນ້າ);
        return ສ່ວນຕົວ_ຫນ້າ;
    }

    private ຫນ້າ_ຄ່າ ຊອກຫາ_ຫນ້າ(ອີເມວ_ພື້ນທີ່ 공간, int ອີເມວ) {
        ຫນ້າ_ຄ່າ ເປົ້າ_ຫມາຍ = 공간.ຫນ້າ_ຕາຕະລາງ.get(Integer.valueOf(쪽번호(ອີເມວ)));
        if (ເປົ້າ_ຫມາຍ == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ເປົ້າ_ຫມາຍ;
    }

    private int 쪽번호(int ອີເມວ) {
        if (ອີເມວ < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ອີເມວ / ຂະ_ຫນາດ_ຫນ້າ;
    }
}

