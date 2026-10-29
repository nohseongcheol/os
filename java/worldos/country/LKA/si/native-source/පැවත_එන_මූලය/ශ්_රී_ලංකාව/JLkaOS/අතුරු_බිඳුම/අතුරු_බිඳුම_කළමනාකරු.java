// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.අතුරු_බිඳුම;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class අතුරු_බිඳුම_කළමනාකරු {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean සක්_රිය;

    public void ලියාපදිංචිය_පිවිසුම(int සූචිය, 개입중단처리기 처리기) {
        번호확인(සූචිය);
        처리기들[සූචිය] = 처리기;
    }

    public void මුදාහැරීම_ගබඩාව(int සූචිය) {
        번호확인(සූචිය);
        처리기들[සූචිය] = null;
    }

    public int බෙදා_හැරීම_අගය(int සූචිය, int 저장된쌓임주소) {
        번호확인(සූචිය);
        if (!සක්_රිය) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[සූචිය];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.ක්_රියාවලිය_අගය_පිවිසුම(저장된쌓임주소);
    }

    public void ඔන්_කරන්න() {
        සක්_රිය = true;
    }

    public void අක්_රියකරණය_කරන්න() {
        සක්_රිය = false;
    }

    public boolean 활성인가() {
        return සක්_රිය;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int සූචිය) {
        if (සූචිය < 0 || සූචිය >= 처리기들.length) {
            throw new IllegalArgumentException("අතුරු_බිඳුම 번호가 올바르지 않습니다.");
        }
    }
}

