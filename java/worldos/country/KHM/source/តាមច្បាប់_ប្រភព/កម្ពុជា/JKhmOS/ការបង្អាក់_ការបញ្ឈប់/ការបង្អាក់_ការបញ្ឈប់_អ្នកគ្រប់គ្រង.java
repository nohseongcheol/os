// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ការបង្អាក់_ការបញ្ឈប់;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ការបង្អាក់_ការបញ្ឈប់_អ្នកគ្រប់គ្រង {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ទំនេរ;

    public void ចុះឈ្មោះ_ការបញ្ចូល(int សន្ទស្សន៏, 개입중단처리기 처리기) {
        번호확인(សន្ទស្សន៏);
        처리기들[សន្ទស្សន៏] = 처리기;
    }

    public void លែង_ការផ្ទុក(int សន្ទស្សន៏) {
        번호확인(សន្ទស្សន៏);
        처리기들[សន្ទស្សន៏] = null;
    }

    public int ចែកចាយ_តំលៃ(int សន្ទស្សន៏, int 저장된쌓임주소) {
        번호확인(សន្ទស្សន៏);
        if (!ទំនេរ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[សន្ទស្សន៏];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.ដំណើរការ_តំលៃ_ការបញ្ចូល(저장된쌓임주소);
    }

    public void បើក_0b9ce0d7() {
        ទំនេរ = true;
    }

    public void បិទដំណើរការ() {
        ទំនេរ = false;
    }

    public boolean បច្ចេកវិទ្យាព័ត៌មាន_ទំនេរ() {
        return ទំនេរ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int សន្ទស្សន៏) {
        if (សន្ទស្សន៏ < 0 || សន្ទស្សន៏ >= 처리기들.length) {
            throw new IllegalArgumentException("ការបង្អាក់_ការបញ្ឈប់ 번호가 올바르지 않습니다.");
        }
    }
}

