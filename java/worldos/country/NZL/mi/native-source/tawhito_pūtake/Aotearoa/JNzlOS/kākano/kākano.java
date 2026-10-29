// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.kākano;

import Aotearoa.JNzlOS.기억공간.Pūmahara_pouwhakahaere;
import Aotearoa.JNzlOS.기억공간.whārangi_pouwhakahaere;
import Aotearoa.JNzlOS.입력.입력관리자;
import Aotearoa.JNzlOS.작업.Hātepe_uara;
import Aotearoa.JNzlOS.작업.Pūwhakahōtaka;
import Aotearoa.JNzlOS.체계호출.체계호출;
import Aotearoa.JNzlOS.pūnaha_kōnae.파일서술자표;
import Aotearoa.JNzlOS.pūnaha_kōnae.pūnaha_kōnae;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kākano {
    private final 하드웨어 pūkoro_uara;
    private final Pūmahara_pouwhakahaere 기억공간 = new Pūmahara_pouwhakahaere(32 * 1024 * 1024);
    private final whārangi_pouwhakahaere 쪽관리 = new whārangi_pouwhakahaere();
    private final pūnaha_kōnae pūnaha_kōnae = new pūnaha_kōnae();
    private final Pūwhakahōtaka Pūwhakahōtaka = new Pūwhakahōtaka(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Hātepe_uara 첫과정;
    private final 체계호출 체계호출;

    public kākano(하드웨어 pūkoro_uara) {
        this.pūkoro_uara = pūkoro_uara;
        첫과정 = Pūwhakahōtaka.첫과정(new 파일서술자표(pūnaha_kōnae));
        체계호출 = new 체계호출(pūnaha_kōnae, 쪽관리, Pūwhakahōtaka, pūkoro_uara, 입력관리);
    }

    public void whakahaere() {
        pūkoro_uara.직렬출력("=== JNzlOS 관리 kākano_uara_0611a8a8 ===\n");
    }

    public void 한단계실행() {
        pūkoro_uara.중앙처리장치멈춤();
    }

    public Pūmahara_pouwhakahaere 기억공간() {
        return 기억공간;
    }

    public whārangi_pouwhakahaere 쪽관리() {
        return 쪽관리;
    }

    public pūnaha_kōnae pūnaha_kōnae() {
        return pūnaha_kōnae;
    }

    public Pūwhakahōtaka Pūwhakahōtaka() {
        return Pūwhakahōtaka;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Hātepe_uara 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
