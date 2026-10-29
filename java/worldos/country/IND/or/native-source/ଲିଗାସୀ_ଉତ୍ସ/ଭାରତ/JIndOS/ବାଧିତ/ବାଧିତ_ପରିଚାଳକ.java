// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ବାଧିତ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ବାଧିତ_ପରିଚାଳକ {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ସକ୍ରିୟ;

    public void ପଞ୍ଜିକରଣ_କରନ୍ତୁ_ଏଣ୍ଟ୍ରି(int ଅନୁକ୍ରମଣିକା, 개입중단처리기 처리기) {
        번호확인(ଅନୁକ୍ରମଣିକା);
        처리기들[ଅନୁକ୍ରମଣିକା] = 처리기;
    }

    public void ରିଲିଜ୍_ଷ୍ଟୋରେଜ୍(int ଅନୁକ୍ରମଣିକା) {
        번호확인(ଅନୁକ୍ରମଣିକା);
        처리기들[ଅନୁକ୍ରମଣିକା] = null;
    }

    public int ବିତରଣ_ମୂଲ୍ୟ(int ଅନୁକ୍ରମଣିକା, int 저장된쌓임주소) {
        번호확인(ଅନୁକ୍ରମଣିକା);
        if (!ସକ୍ରିୟ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ଅନୁକ୍ରମଣିକା];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ_ଏଣ୍ଟ୍ରି(저장된쌓임주소);
    }

    public void ସାମର୍ଥ୍ୟ() {
        ସକ୍ରିୟ = true;
    }

    public void ନିଷ୍କ୍ରିୟ_କରନ୍ତୁ() {
        ସକ୍ରିୟ = false;
    }

    public boolean ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ସକ୍ରିୟ() {
        return ସକ୍ରିୟ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ଅନୁକ୍ରମଣିକା) {
        if (ଅନୁକ୍ରମଣିକା < 0 || ଅନୁକ୍ରମଣିକା >= 처리기들.length) {
            throw new IllegalArgumentException("ବାଧିତ 번호가 올바르지 않습니다.");
        }
    }
}

