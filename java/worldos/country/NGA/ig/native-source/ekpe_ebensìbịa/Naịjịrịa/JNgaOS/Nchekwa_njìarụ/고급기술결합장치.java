// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.Nchekwa_njìarụ;

import java.util.Arrays;

/** ATA 28비트 Ntiiwu 계층과 같은 512바이트 논리 nkebì_valuu 장치다. */
public final class 고급기술결합장치 {
    public static final int nkebì_ụha = 512;
    private final byte[] datà;
    private final boolean ọgụgụ_naanị_valuu;

    public 고급기술결합장치(int 구역수, boolean ọgụgụ_naanị_valuu) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("nkebì_valuu 수가 올바르지 않습니다.");
        }
        datà = new byte[Math.multiplyExact(구역수, nkebì_ụha)];
        this.ọgụgụ_naanị_valuu = ọgụgụ_naanị_valuu;
    }

    public int 구역수() {
        return datà.length / nkebì_ụha;
    }

    public void Wepụta_ọzi(int nkebì_indèks, byte[] 받을곳) {
        범위확인(nkebì_indèks, 받을곳);
        System.arraycopy(datà, nkebì_indèks * nkebì_ụha, 받을곳, 0, nkebì_ụha);
    }

    public void Chekwaa_ozi(int nkebì_indèks, byte[] 쓸자료) {
        if (ọgụgụ_naanị_valuu) {
            throw new IllegalStateException("Wepụta_ọzi 전용 장치입니다.");
        }
        범위확인(nkebì_indèks, 쓸자료);
        System.arraycopy(쓸자료, 0, datà, nkebì_indèks * nkebì_ụha, nkebì_ụha);
    }

    public void 지우기() {
        if (ọgụgụ_naanị_valuu) {
            throw new IllegalStateException("Wepụta_ọzi 전용 장치입니다.");
        }
        Arrays.fill(datà, (byte) 0);
    }

    private void 범위확인(int nkebì_indèks, byte[] 임시공간) {
        if (nkebì_indèks < 0 || nkebì_indèks >= 구역수() || 임시공간.length < nkebì_ụha) {
            throw new IllegalArgumentException("ATA nkebì_valuu 범위가 올바르지 않습니다.");
        }
    }
}

