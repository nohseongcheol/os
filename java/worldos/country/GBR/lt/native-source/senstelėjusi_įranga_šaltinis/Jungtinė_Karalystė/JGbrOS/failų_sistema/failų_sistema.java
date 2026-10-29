// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.failų_sistema;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Skaitymas 계층과 같은 Skaitymas 전용 Failas 저장소의 관리 모델이다. */
public final class failų_sistema {
    static final class 열린파일 {
        final byte[] duomenys;
        int Pozicija;
        int nuoroda_COUNT = 1;

        열린파일(byte[] duomenys) {
            this.duomenys = duomenys;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void sujungti_Failas(String Pavadinimas_2, byte[] duomenys) {
        파일들.put(kanoninis_vardas(Pavadinimas_2), Arrays.copyOf(duomenys, duomenys.length));
    }

    열린파일 Atverti(String Pavadinimas_2) {
        byte[] duomenys = 파일들.get(kanoninis_vardas(Pavadinimas_2));
        if (duomenys == null) {
            return null;
        }
        return new 열린파일(duomenys);
    }

    public boolean 존재함(String Pavadinimas_2) {
        return 파일들.containsKey(kanoninis_vardas(Pavadinimas_2));
    }

    public Failas_informacija msinfo32_exe(String Pavadinimas_2) {
        byte[] duomenys = 파일들.get(kanoninis_vardas(Pavadinimas_2));
        if (duomenys == null) {
            return null;
        }
        return new Failas_informacija(duomenys.length, 0100444);
    }

    private String kanoninis_vardas(String Pavadinimas_2) {
        if (Pavadinimas_2 == null) {
            throw new NullPointerException("Failas 이름이 없습니다.");
        }
        String REZULTATAS = Pavadinimas_2.startsWith("/") ? Pavadinimas_2.substring(1) : Pavadinimas_2;
        return REZULTATAS.toUpperCase(Locale.ROOT);
    }
}
