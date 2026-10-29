// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.Bobolokelo_sedirišwa;

import java.util.Arrays;

/** ATA 28비트 Taelo 계층과 같은 512바이트 논리 karolo_boleng 장치다. */
public final class 고급기술결합장치 {
    public static final int karolo_bogolo = 512;
    private final byte[] data;
    private final boolean balwago_fela_boleng;

    public 고급기술결합장치(int 구역수, boolean balwago_fela_boleng) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("karolo_boleng 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(구역수, karolo_bogolo)];
        this.balwago_fela_boleng = balwago_fela_boleng;
    }

    public int 구역수() {
        return data.length / karolo_bogolo;
    }

    public void Bala(int karolo_lokela, byte[] 받을곳) {
        범위확인(karolo_lokela, 받을곳);
        System.arraycopy(data, karolo_lokela * karolo_bogolo, 받을곳, 0, karolo_bogolo);
    }

    public void Ngwala(int karolo_lokela, byte[] 쓸자료) {
        if (balwago_fela_boleng) {
            throw new IllegalStateException("Bala 전용 장치입니다.");
        }
        범위확인(karolo_lokela, 쓸자료);
        System.arraycopy(쓸자료, 0, data, karolo_lokela * karolo_bogolo, karolo_bogolo);
    }

    public void 지우기() {
        if (balwago_fela_boleng) {
            throw new IllegalStateException("Bala 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void 범위확인(int karolo_lokela, byte[] 임시공간) {
        if (karolo_lokela < 0 || karolo_lokela >= 구역수() || 임시공간.length < karolo_bogolo) {
            throw new IllegalArgumentException("ATA karolo_boleng 범위가 올바르지 않습니다.");
        }
    }
}

