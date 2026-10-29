// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COD.JCodOS.Ububiko_igendanwa;

import java.util.Arrays;

/** ATA 28비트 Icyo_wifuza 계층과 같은 512바이트 논리 igice_agaciro 장치다. */
public final class 고급기술결합장치 {
    public static final int igice_ingano = 512;
    private final byte[] amakurushingiro;
    private final boolean soma_gusa_agaciro;

    public 고급기술결합장치(int 구역수, boolean soma_gusa_agaciro) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("igice_agaciro 수가 올바르지 않습니다.");
        }
        amakurushingiro = new byte[Math.multiplyExact(구역수, igice_ingano)];
        this.soma_gusa_agaciro = soma_gusa_agaciro;
    }

    public int 구역수() {
        return amakurushingiro.length / igice_ingano;
    }

    public void 읽기(int igice_umugerekashakiro, byte[] 받을곳) {
        범위확인(igice_umugerekashakiro, 받을곳);
        System.arraycopy(amakurushingiro, igice_umugerekashakiro * igice_ingano, 받을곳, 0, igice_ingano);
    }

    public void kwandika(int igice_umugerekashakiro, byte[] 쓸자료) {
        if (soma_gusa_agaciro) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(igice_umugerekashakiro, 쓸자료);
        System.arraycopy(쓸자료, 0, amakurushingiro, igice_umugerekashakiro * igice_ingano, igice_ingano);
    }

    public void 지우기() {
        if (soma_gusa_agaciro) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(amakurushingiro, (byte) 0);
    }

    private void 범위확인(int igice_umugerekashakiro, byte[] 임시공간) {
        if (igice_umugerekashakiro < 0 || igice_umugerekashakiro >= 구역수() || 임시공간.length < igice_ingano) {
            throw new IllegalArgumentException("ATA igice_agaciro 범위가 올바르지 않습니다.");
        }
    }
}

