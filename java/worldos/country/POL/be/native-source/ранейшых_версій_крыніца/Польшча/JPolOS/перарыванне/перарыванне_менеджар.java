// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польшча.JPolOS.перарыванне;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class перарыванне_менеджар {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Актыўны;

    public void рэгістраваць_увядзенне(int індэкс, 개입중단처리기 처리기) {
        번호확인(індэкс);
        처리기들[індэкс] = 처리기;
    }

    public void выпуск_Сховішча(int індэкс) {
        번호확인(індэкс);
        처리기들[індэкс] = null;
    }

    public int размеркаваць_значэнне(int індэкс, int 저장된쌓임주소) {
        번호확인(індэкс);
        if (!Актыўны) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[індэкс];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Працэс_значэнне_увядзенне(저장된쌓임주소);
    }

    public void уключыць() {
        Актыўны = true;
    }

    public void адключыць() {
        Актыўны = false;
    }

    public boolean аддзел_інфармацыйных_тэхналогій_Актыўны() {
        return Актыўны;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int індэкс) {
        if (індэкс < 0 || індэкс >= 처리기들.length) {
            throw new IllegalArgumentException("перарыванне 번호가 올바르지 않습니다.");
        }
    }
}

