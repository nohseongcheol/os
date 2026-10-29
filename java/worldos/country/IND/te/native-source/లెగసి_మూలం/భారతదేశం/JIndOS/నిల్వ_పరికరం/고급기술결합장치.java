// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.నిల్వ_పరికరం;

import java.util.Arrays;

/** ATA 28비트 ఆదేశము 계층과 같은 512바이트 논리 విభాగం_మూల్యం 장치다. */
public final class 고급기술결합장치 {
    public static final int విభాగం_పరిమాణం_మార్చు = 512;
    private final byte[] డేటా;
    private final boolean చదవడానికి_మాత్రమే_మూల్యం;

    public 고급기술결합장치(int 구역수, boolean చదవడానికి_మాత్రమే_మూల్యం) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("విభాగం_మూల్యం 수가 올바르지 않습니다.");
        }
        డేటా = new byte[Math.multiplyExact(구역수, విభాగం_పరిమాణం_మార్చు)];
        this.చదవడానికి_మాత్రమే_మూల్యం = చదవడానికి_మాత్రమే_మూల్యం;
    }

    public int 구역수() {
        return డేటా.length / విభాగం_పరిమాణం_మార్చు;
    }

    public void చదువు(int విభాగం_సూచీ, byte[] 받을곳) {
        범위확인(విభాగం_సూచీ, 받을곳);
        System.arraycopy(డేటా, విభాగం_సూచీ * విభాగం_పరిమాణం_మార్చు, 받을곳, 0, విభాగం_పరిమాణం_మార్చు);
    }

    public void వ్రాయుము(int విభాగం_సూచీ, byte[] 쓸자료) {
        if (చదవడానికి_మాత్రమే_మూల్యం) {
            throw new IllegalStateException("చదువు 전용 장치입니다.");
        }
        범위확인(విభాగం_సూచీ, 쓸자료);
        System.arraycopy(쓸자료, 0, డేటా, విభాగం_సూచీ * విభాగం_పరిమాణం_మార్చు, విభాగం_పరిమాణం_మార్చు);
    }

    public void తుడిచివేయి_ప్రవేశం() {
        if (చదవడానికి_మాత్రమే_మూల్యం) {
            throw new IllegalStateException("చదువు 전용 장치입니다.");
        }
        Arrays.fill(డేటా, (byte) 0);
    }

    private void 범위확인(int విభాగం_సూచీ, byte[] 임시공간) {
        if (విభాగం_సూచీ < 0 || విభాగం_సూచీ >= 구역수() || 임시공간.length < విభాగం_పరిమాణం_మార్చు) {
            throw new IllegalArgumentException("ATA విభాగం_మూల్యం 범위가 올바르지 않습니다.");
        }
    }
}

