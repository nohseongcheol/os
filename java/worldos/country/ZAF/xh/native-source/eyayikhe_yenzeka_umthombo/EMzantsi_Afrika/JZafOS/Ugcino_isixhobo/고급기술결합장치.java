// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.Ugcino_isixhobo;

import java.util.Arrays;

/** ATA 28비트 Umyalelo 계층과 같은 512바이트 논리 icandelo_ixabiso 장치다. */
public final class 고급기술결합장치 {
    public static final int icandelo_isayizi = 512;
    private final byte[] iingcombolo;
    private final boolean efundwayo_kuphela_ixabiso;

    public 고급기술결합장치(int 구역수, boolean efundwayo_kuphela_ixabiso) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("icandelo_ixabiso 수가 올바르지 않습니다.");
        }
        iingcombolo = new byte[Math.multiplyExact(구역수, icandelo_isayizi)];
        this.efundwayo_kuphela_ixabiso = efundwayo_kuphela_ixabiso;
    }

    public int 구역수() {
        return iingcombolo.length / icandelo_isayizi;
    }

    public void Funda(int icandelo_indeksa, byte[] 받을곳) {
        범위확인(icandelo_indeksa, 받을곳);
        System.arraycopy(iingcombolo, icandelo_indeksa * icandelo_isayizi, 받을곳, 0, icandelo_isayizi);
    }

    public void Bhala(int icandelo_indeksa, byte[] 쓸자료) {
        if (efundwayo_kuphela_ixabiso) {
            throw new IllegalStateException("Funda 전용 장치입니다.");
        }
        범위확인(icandelo_indeksa, 쓸자료);
        System.arraycopy(쓸자료, 0, iingcombolo, icandelo_indeksa * icandelo_isayizi, icandelo_isayizi);
    }

    public void 지우기() {
        if (efundwayo_kuphela_ixabiso) {
            throw new IllegalStateException("Funda 전용 장치입니다.");
        }
        Arrays.fill(iingcombolo, (byte) 0);
    }

    private void 범위확인(int icandelo_indeksa, byte[] 임시공간) {
        if (icandelo_indeksa < 0 || icandelo_indeksa >= 구역수() || 임시공간.length < icandelo_isayizi) {
            throw new IllegalArgumentException("ATA icandelo_ixabiso 범위가 올바르지 않습니다.");
        }
    }
}

