// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.dog;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class dog_doxalkat {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean sawar;

    public void bindu_dugal_xabaar(int àlluwa_tur, 개입중단처리기 처리기) {
        번호확인(àlluwa_tur);
        처리기들[àlluwa_tur] = 처리기;
    }

    public void yewwi_Dencukaay(int àlluwa_tur) {
        번호확인(àlluwa_tur);
        처리기들[àlluwa_tur] = null;
    }

    public int Séddale_xëyma(int àlluwa_tur, int 저장된쌓임주소) {
        번호확인(àlluwa_tur);
        if (!sawar) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[àlluwa_tur];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.yokkute_xëyma_dugal_xabaar(저장된쌓임주소);
    }

    public void dekkal() {
        sawar = true;
    }

    public void dakkal() {
        sawar = false;
    }

    public boolean 활성인가() {
        return sawar;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int àlluwa_tur) {
        if (àlluwa_tur < 0 || àlluwa_tur >= 처리기들.length) {
            throw new IllegalArgumentException("dog 번호가 올바르지 않습니다.");
        }
    }
}

