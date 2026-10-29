// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਭਾਰਤ.JIndOS.ਰੋਕ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ਰੋਕ_ਪ੍ਰਬੰਧਕ {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ਕ੍ਰਿਆਸ਼ੀਲ;

    public void ਰਜਿਸਟਰ_ਕਰੋ_ਦਾਖਲਾ(int ਅਨੁਕ੍ਰਮਣਿਕਾ, 개입중단처리기 처리기) {
        번호확인(ਅਨੁਕ੍ਰਮਣਿਕਾ);
        처리기들[ਅਨੁਕ੍ਰਮਣਿਕਾ] = 처리기;
    }

    public void ਰਿਲੀਜ_ਸਟੋਰੇਜ(int ਅਨੁਕ੍ਰਮਣਿਕਾ) {
        번호확인(ਅਨੁਕ੍ਰਮਣਿਕਾ);
        처리기들[ਅਨੁਕ੍ਰਮਣਿਕਾ] = null;
    }

    public int ਵੰਡਣਾ_ਕੀਮਤ(int ਅਨੁਕ੍ਰਮਣਿਕਾ, int 저장된쌓임주소) {
        번호확인(ਅਨੁਕ੍ਰਮਣਿਕਾ);
        if (!ਕ੍ਰਿਆਸ਼ੀਲ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ਅਨੁਕ੍ਰਮਣਿਕਾ];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.ਕਾਰਵਾਈ_ਕੀਮਤ_ਦਾਖਲਾ(저장된쌓임주소);
    }

    public void ਚਾਲੂ_ਕਰੋ() {
        ਕ੍ਰਿਆਸ਼ੀਲ = true;
    }

    public void ਅਕਿਰਿਆਸ਼ੀਲ() {
        ਕ੍ਰਿਆਸ਼ੀਲ = false;
    }

    public boolean 활성인가() {
        return ਕ੍ਰਿਆਸ਼ੀਲ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ਅਨੁਕ੍ਰਮਣਿਕਾ) {
        if (ਅਨੁਕ੍ਰਮਣਿਕਾ < 0 || ਅਨੁਕ੍ਰਮਣਿਕਾ >= 처리기들.length) {
            throw new IllegalArgumentException("ਰੋਕ 번호가 올바르지 않습니다.");
        }
    }
}

