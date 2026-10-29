// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 ຈັດແຖວ_ຄ່າ ຈັດສັນ_ບ່ອນເກັບຂໍ້ມູນ, ເວີຊັນ_ບ່ອນເກັບຂໍ້ມູນ, 병합을 담당한다. */
public final class 기억공간관리자 {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public 기억공간관리자(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int ຈັດສັນ_ບ່ອນເກັບຂໍ້ມູນ(int ຂະ_ຫນາດ) {
        return 정렬할당(ຂະ_ຫນາດ, 1);
    }

    public synchronized int 정렬할당(int ຂະ_ຫນາດ, int ຈັດແຖວ_ຄ່າ) {
        if (ຂະ_ຫນາດ <= 0 || ຈັດແຖວ_ຄ່າ <= 0 || (ຈັດແຖວ_ຄ່າ & (ຈັດແຖວ_ຄ່າ - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ເຂົ້າໃນ_ຄ່າ : 빈영역.entrySet()) {
            int ແລ່ນ = ເຂົ້າໃນ_ຄ່າ.getKey().intValue();
            int 영역크기 = ເຂົ້າໃນ_ຄ່າ.getValue().intValue();
            int 정렬시작 = (ແລ່ນ + ຈັດແຖວ_ຄ່າ - 1) & -ຈັດແຖວ_ຄ່າ;
            int ດ້ານຫນ້າ_ຄ່າ_ຂະ_ຫນາດ = 정렬시작 - ແລ່ນ;
            int 끝크기 = 영역크기 - ດ້ານຫນ້າ_ຄ່າ_ຂະ_ຫນາດ - ຂະ_ຫນາດ;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(ແລ່ນ));
            if (ດ້ານຫນ້າ_ຄ່າ_ຂະ_ຫນາດ > 0) {
                빈영역.put(Integer.valueOf(ແລ່ນ), Integer.valueOf(ດ້ານຫນ້າ_ຄ່າ_ຂະ_ຫນາດ));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + ຂະ_ຫນາດ), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(ຂະ_ຫນາດ));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + ຂະ_ຫນາດ, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void ເວີຊັນ_ບ່ອນເກັບຂໍ້ມູນ(int ອີເມວ) {
        Integer ຂະ_ຫນາດ_ວັດ_ຖຸ = 사용영역.remove(Integer.valueOf(ອີເມວ));
        if (ຂະ_ຫນາດ_ວັດ_ຖຸ == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int ແລ່ນ = ອີເມວ;
        int ຂະ_ຫນາດ = ຂະ_ຫນາດ_ວັດ_ຖຸ.intValue();
        Map.Entry<Integer, Integer> ດ້ານຫນ້າ_ຄ່າ = 빈영역.lowerEntry(Integer.valueOf(ແລ່ນ));
        if (ດ້ານຫນ້າ_ຄ່າ != null && ດ້ານຫນ້າ_ຄ່າ.getKey().intValue() + ດ້ານຫນ້າ_ຄ່າ.getValue().intValue() == ແລ່ນ) {
            ແລ່ນ = ດ້ານຫນ້າ_ຄ່າ.getKey().intValue();
            ຂະ_ຫນາດ += ດ້ານຫນ້າ_ຄ່າ.getValue().intValue();
            빈영역.remove(ດ້ານຫນ້າ_ຄ່າ.getKey());
        }
        Map.Entry<Integer, Integer> ກັບ_ຄືນ_ຄ່າ = 빈영역.ceilingEntry(Integer.valueOf(ແລ່ນ));
        if (ກັບ_ຄືນ_ຄ່າ != null && ແລ່ນ + ຂະ_ຫນາດ == ກັບ_ຄືນ_ຄ່າ.getKey().intValue()) {
            ຂະ_ຫນາດ += ກັບ_ຄືນ_ຄ່າ.getValue().intValue();
            빈영역.remove(ກັບ_ຄືນ_ຄ່າ.getKey());
        }
        빈영역.put(Integer.valueOf(ແລ່ນ), Integer.valueOf(ຂະ_ຫນາດ));
    }

    public synchronized byte 바이트읽기(int ອີເມວ) {
        범위확인(ອີເມວ, 1);
        return 기억공간[ອີເມວ];
    }

    public synchronized void ຂຽນ_ໄບ_ຄ່າ(int ອີເມວ, byte ຄ່າ) {
        범위확인(ອີເມວ, 1);
        기억공간[ອີເມວ] = ຄ່າ;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer ຂະ_ຫນາດ : 사용영역.values()) {
            합계 += ຂະ_ຫນາດ.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ອີເມວ, int ຂະ_ຫນາດ) {
        if (ອີເມວ < 0 || ຂະ_ຫນາດ < 0 || ອີເມວ > 기억공간.length - ຂະ_ຫນາດ) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

