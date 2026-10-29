// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.Memorie_regiune;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB pagina_VALUE 연결과 Scriere 시 복사를 제공한다. */
public final class 쪽관리자 {
    public static final int dimensiune_pagină = 4096;

    private static final class pagina_VALUE {
        private byte[] date = new byte[dimensiune_pagină];
        private int referință_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adresa_SPAȚIU {
        private final Map<Integer, pagina_VALUE> pagina_tabel = new HashMap<Integer, pagina_VALUE>();
    }

    public adresa_SPAȚIU 새주소공간() {
        return new adresa_SPAȚIU();
    }

    public void MAP_pagina(adresa_SPAȚIU adresa_regiune, int adresă_virtuală, boolean 쓰기가능) {
        int INDEX = 쪽번호(adresă_virtuală);
        pagina_VALUE 새쪽 = new pagina_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        adresa_regiune.pagina_tabel.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adresa_SPAȚIU 쓰기시복사복제(adresa_SPAȚIU 원본) {
        adresa_SPAȚIU 복제본 = new adresa_SPAȚIU();
        for (Map.Entry<Integer, pagina_VALUE> intrare_VALUE : 원본.pagina_tabel.entrySet()) {
            pagina_VALUE 공유쪽 = intrare_VALUE.getValue();
            공유쪽.referință_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.pagina_tabel.put(intrare_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(adresa_SPAȚIU adresa_regiune, int adresă_virtuală) {
        pagina_VALUE țintă = FIND_pagina(adresa_regiune, adresă_virtuală);
        return țintă.date[Math.floorMod(adresă_virtuală, dimensiune_pagină)];
    }

    public void scriere_byte_VALUE(adresa_SPAȚIU adresa_regiune, int adresă_virtuală, byte VALUE) {
        int INDEX = 쪽번호(adresă_virtuală);
        pagina_VALUE țintă = FIND_pagina(adresa_regiune, adresă_virtuală);
        if (!țintă.쓰기가능) {
            if (!țintă.쓰기시복사) {
                throw new IllegalStateException("Citire 전용 쪽입니다.");
            }
            țintă = crea_Privat_pagina(adresa_regiune, INDEX, țintă);
        }
        țintă.date[Math.floorMod(adresă_virtuală, dimensiune_pagină)] = VALUE;
    }

    public void Privat_zonă_scriere(adresa_SPAȚIU adresa_regiune, int buta_adresa, int Mărime) {
        if (Mărime < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int termina_un_apel_adresa = Math.addExact(buta_adresa, Mărime);
        for (int adresa = buta_adresa; adresa < termina_un_apel_adresa; adresa = (쪽번호(adresa) + 1) * dimensiune_pagină) {
            int INDEX = 쪽번호(adresa);
            pagina_VALUE țintă = FIND_pagina(adresa_regiune, adresa);
            if (țintă.쓰기시복사) {
                crea_Privat_pagina(adresa_regiune, INDEX, țintă);
            } else {
                țintă.쓰기가능 = true;
            }
        }
    }

    public void zonă_scriere(adresa_SPAȚIU adresa_regiune, int buta_adresa, byte[] date) {
        for (int INDEX = 0; INDEX < date.length; INDEX++) {
            scriere_byte_VALUE(adresa_regiune, buta_adresa + INDEX, date[INDEX]);
        }
    }

    private pagina_VALUE crea_Privat_pagina(adresa_SPAȚIU adresa_regiune, int INDEX, pagina_VALUE 공유쪽) {
        pagina_VALUE Privat_pagina = new pagina_VALUE();
        Privat_pagina.date = Arrays.copyOf(공유쪽.date, 공유쪽.date.length);
        Privat_pagina.쓰기가능 = true;
        Privat_pagina.쓰기시복사 = false;
        공유쪽.referință_COUNT--;
        adresa_regiune.pagina_tabel.put(Integer.valueOf(INDEX), Privat_pagina);
        return Privat_pagina;
    }

    private pagina_VALUE FIND_pagina(adresa_SPAȚIU adresa_regiune, int adresa) {
        pagina_VALUE țintă = adresa_regiune.pagina_tabel.get(Integer.valueOf(쪽번호(adresa)));
        if (țintă == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return țintă;
    }

    private int 쪽번호(int adresa) {
        if (adresa < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return adresa / dimensiune_pagină;
    }
}

