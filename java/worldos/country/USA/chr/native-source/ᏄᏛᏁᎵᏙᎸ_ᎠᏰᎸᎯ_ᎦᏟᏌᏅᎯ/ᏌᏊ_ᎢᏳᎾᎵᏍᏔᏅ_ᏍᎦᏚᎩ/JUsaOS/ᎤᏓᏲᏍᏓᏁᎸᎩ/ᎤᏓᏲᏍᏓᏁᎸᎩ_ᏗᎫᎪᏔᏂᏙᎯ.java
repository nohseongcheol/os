// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎤᏓᏲᏍᏓᏁᎸᎩ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ᎤᏓᏲᏍᏓᏁᎸᎩ_ᏗᎫᎪᏔᏂᏙᎯ {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ᎾᏛᏁᎲ;

    public void 등록(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, 개입중단처리기 처리기) {
        번호확인(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
        처리기들[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] = 처리기;
    }

    public void 해제(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        번호확인(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
        처리기들[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ] = null;
    }

    public int 분배(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, int 저장된쌓임주소) {
        번호확인(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
        if (!ᎾᏛᏁᎲ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(저장된쌓임주소);
    }

    public void ᎡᎵᏊ_ᏱᎬᏛᏁᏗ() {
        ᎾᏛᏁᎲ = true;
    }

    public void 비활성화() {
        ᎾᏛᏁᎲ = false;
    }

    public boolean 활성인가() {
        return ᎾᏛᏁᎲ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 0 || ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ >= 처리기들.length) {
            throw new IllegalArgumentException("ᎤᏓᏲᏍᏓᏁᎸᎩ 번호가 올바르지 않습니다.");
        }
    }
}

