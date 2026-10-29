// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iMalawi.JMwiOS.i_IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class i_IRQ_imeneja {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean kuyasebenza;

    public void bhalisa_okufakwayo(int thola_inkomba, 개입중단처리기 처리기) {
        번호확인(thola_inkomba);
        처리기들[thola_inkomba] = 처리기;
    }

    public void khulula_Indawo_yokugcina(int thola_inkomba) {
        번호확인(thola_inkomba);
        처리기들[thola_inkomba] = null;
    }

    public int sabalalisa_inani(int thola_inkomba, int 저장된쌓임주소) {
        번호확인(thola_inkomba);
        if (!kuyasebenza) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[thola_inkomba];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Inqubo_inani_okufakwayo(저장된쌓임주소);
    }

    public void vumela() {
        kuyasebenza = true;
    }

    public void yekisa_ukusebenza() {
        kuyasebenza = false;
    }

    public boolean 활성인가() {
        return kuyasebenza;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int thola_inkomba) {
        if (thola_inkomba < 0 || thola_inkomba >= 처리기들.length) {
            throw new IllegalArgumentException("i_IRQ 번호가 올바르지 않습니다.");
        }
    }
}

