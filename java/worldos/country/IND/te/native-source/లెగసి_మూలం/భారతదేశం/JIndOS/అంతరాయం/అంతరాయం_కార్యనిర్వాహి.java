// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.అంతరాయం;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class అంతరాయం_కార్యనిర్వాహి {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean యాక్టివ్;

    public void నమోదు_చేయి_ప్రవేశం(int సూచీ, 개입중단처리기 처리기) {
        번호확인(సూచీ);
        처리기들[సూచీ] = 처리기;
    }

    public void విడుదల_నిల్వ(int సూచీ) {
        번호확인(సూచీ);
        처리기들[సూచీ] = null;
    }

    public int పంపిణీ_చేయి_మూల్యం(int సూచీ, int 저장된쌓임주소) {
        번호확인(సూచీ);
        if (!యాక్టివ్) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[సూచీ];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.విధానం_మూల్యం_ప్రవేశం(저장된쌓임주소);
    }

    public void ఆన్_చేయి() {
        యాక్టివ్ = true;
    }

    public void నిష్క్రియపరచుట() {
        యాక్టివ్ = false;
    }

    public boolean సమాచార_టెక్నాలజీ_యాక్టివ్() {
        return యాక్టివ్;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int సూచీ) {
        if (సూచీ < 0 || సూచీ >= 처리기들.length) {
            throw new IllegalArgumentException("అంతరాయం 번호가 올바르지 않습니다.");
        }
    }
}

