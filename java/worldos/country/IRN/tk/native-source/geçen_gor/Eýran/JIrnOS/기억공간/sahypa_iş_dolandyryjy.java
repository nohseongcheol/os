// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eýran.JIrnOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB sahypa_baha 연결과 Ýaz 시 복사를 제공한다. */
public final class sahypa_iş_dolandyryjy {
    public static final int sahypanyň_ölçegi = 4096;

    private static final class sahypa_baha {
        private byte[] maglumat = new byte[sahypanyň_ölçegi];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class salgy_ýer {
        private final Map<Integer, sahypa_baha> sahypa_tablisa = new HashMap<Integer, sahypa_baha>();
    }

    public salgy_ýer 새주소공간() {
        return new salgy_ýer();
    }

    public void kartada_görkez_sahypa(salgy_ýer 공간, int hyýaly_salgy, boolean 쓰기가능) {
        int indeks = 쪽번호(hyýaly_salgy);
        sahypa_baha 새쪽 = new sahypa_baha();
        새쪽.쓰기가능 = 쓰기가능;
        공간.sahypa_tablisa.put(Integer.valueOf(indeks), 새쪽);
    }

    public salgy_ýer 쓰기시복사복제(salgy_ýer 원본) {
        salgy_ýer 복제본 = new salgy_ýer();
        for (Map.Entry<Integer, sahypa_baha> girizmeklik_baha : 원본.sahypa_tablisa.entrySet()) {
            sahypa_baha 공유쪽 = girizmeklik_baha.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.sahypa_tablisa.put(girizmeklik_baha.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(salgy_ýer 공간, int hyýaly_salgy) {
        sahypa_baha niýet = tap_sahypa(공간, hyýaly_salgy);
        return niýet.maglumat[Math.floorMod(hyýaly_salgy, sahypanyň_ölçegi)];
    }

    public void ýaz_baýt_baha(salgy_ýer 공간, int hyýaly_salgy, byte baha) {
        int indeks = 쪽번호(hyýaly_salgy);
        sahypa_baha niýet = tap_sahypa(공간, hyýaly_salgy);
        if (!niýet.쓰기가능) {
            if (!niýet.쓰기시복사) {
                throw new IllegalStateException("Oka 전용 쪽입니다.");
            }
            niýet = döretmek_hususy_sahypa(공간, indeks, niýet);
        }
        niýet.maglumat[Math.floorMod(hyýaly_salgy, sahypanyň_ölçegi)] = baha;
    }

    public void 범위개인쓰기(salgy_ýer 공간, int başlat_salgy, int Ululyk) {
        if (Ululyk < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int tamamla_salgy = Math.addExact(başlat_salgy, Ululyk);
        for (int salgy = başlat_salgy; salgy < tamamla_salgy; salgy = (쪽번호(salgy) + 1) * sahypanyň_ölçegi) {
            int indeks = 쪽번호(salgy);
            sahypa_baha niýet = tap_sahypa(공간, salgy);
            if (niýet.쓰기시복사) {
                döretmek_hususy_sahypa(공간, indeks, niýet);
            } else {
                niýet.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(salgy_ýer 공간, int başlat_salgy, byte[] maglumat) {
        for (int indeks = 0; indeks < maglumat.length; indeks++) {
            ýaz_baýt_baha(공간, başlat_salgy + indeks, maglumat[indeks]);
        }
    }

    private sahypa_baha döretmek_hususy_sahypa(salgy_ýer 공간, int indeks, sahypa_baha 공유쪽) {
        sahypa_baha hususy_sahypa = new sahypa_baha();
        hususy_sahypa.maglumat = Arrays.copyOf(공유쪽.maglumat, 공유쪽.maglumat.length);
        hususy_sahypa.쓰기가능 = true;
        hususy_sahypa.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.sahypa_tablisa.put(Integer.valueOf(indeks), hususy_sahypa);
        return hususy_sahypa;
    }

    private sahypa_baha tap_sahypa(salgy_ýer 공간, int salgy) {
        sahypa_baha niýet = 공간.sahypa_tablisa.get(Integer.valueOf(쪽번호(salgy)));
        if (niýet == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return niýet;
    }

    private int 쪽번호(int salgy) {
        if (salgy < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return salgy / sahypanyň_ölçegi;
    }
}

