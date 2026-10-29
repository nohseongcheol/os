// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gana.JGhaOS.sauka;

import java.util.HashMap;
import java.util.Map;
import Gana.JGhaOS.Kwara.kayan_haɗi_na_kwamfuta_Daraja;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 kayan_haɗi_na_kwamfuta_Daraja 대역이다. */
public final class sauka_kayan_haɗi_na_kwamfuta implements kayan_haɗi_na_kwamfuta_Daraja {
    private final Map<Integer, Integer> kayan_haɗi_na_kwamfuta_fot_Daraja = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String kunshiya_Daraja) {
        직렬기록.append(kunshiya_Daraja);
        System.out.print(kunshiya_Daraja);
    }

    @Override
    public int 포트바이트읽기(int kayan_haɗi_na_kwamfuta_lambar_kafa) {
        Integer Daraja = kayan_haɗi_na_kwamfuta_fot_Daraja.get(Integer.valueOf(kayan_haɗi_na_kwamfuta_lambar_kafa));
        return Daraja == null ? 0 : Daraja.intValue();
    }

    @Override
    public void Rubuta_fot_bayit(int kayan_haɗi_na_kwamfuta_lambar_kafa, int Daraja) {
        kayan_haɗi_na_kwamfuta_fot_Daraja.put(Integer.valueOf(kayan_haɗi_na_kwamfuta_lambar_kafa), Integer.valueOf(Daraja & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // sauka 시험에서는 다음 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

