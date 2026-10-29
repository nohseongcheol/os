// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.i_IRQ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class i_IRQ_umphathi {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean edlamkileyo;

    public void bhalisa_ufako_nkcukacha(int indeksa, 개입중단처리기 처리기) {
        번호확인(indeksa);
        처리기들[indeksa] = 처리기;
    }

    public void vulela_Ugcino(int indeksa) {
        번호확인(indeksa);
        처리기들[indeksa] = null;
    }

    public int sasaza_ixabiso(int indeksa, int 저장된쌓임주소) {
        번호확인(indeksa);
        if (!edlamkileyo) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[indeksa];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Inkqubo_ixabiso_ufako_nkcukacha(저장된쌓임주소);
    }

    public void ukuvula() {
        edlamkileyo = true;
    }

    public void yenza_ingasebenzi() {
        edlamkileyo = false;
    }

    public boolean 활성인가() {
        return edlamkileyo;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int indeksa) {
        if (indeksa < 0 || indeksa >= 처리기들.length) {
            throw new IllegalArgumentException("i_IRQ 번호가 올바르지 않습니다.");
        }
    }
}

