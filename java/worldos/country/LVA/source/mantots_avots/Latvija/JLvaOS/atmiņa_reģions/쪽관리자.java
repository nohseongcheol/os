// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.atmiņa_reģions;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB lapa_VALUE 연결과 Rakstīt 시 복사를 제공한다. */
public final class 쪽관리자 {
    public static final int lappuses_izmēri = 4096;

    private static final class lapa_VALUE {
        private byte[] dati = new byte[lappuses_izmēri];
        private int Uzziņas_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adrese_telpa {
        private final Map<Integer, lapa_VALUE> lapa_tabula = new HashMap<Integer, lapa_VALUE>();
    }

    public adrese_telpa 새주소공간() {
        return new adrese_telpa();
    }

    public void MAP_lapa(adrese_telpa adrese_reģions, int virtuālā_adrese, boolean 쓰기가능) {
        int INDEX = lapa_numurs(virtuālā_adrese);
        lapa_VALUE 새쪽 = new lapa_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        adrese_reģions.lapa_tabula.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adrese_telpa 쓰기시복사복제(adrese_telpa 원본) {
        adrese_telpa 복제본 = new adrese_telpa();
        for (Map.Entry<Integer, lapa_VALUE> ievade_VALUE : 원본.lapa_tabula.entrySet()) {
            lapa_VALUE 공유쪽 = ievade_VALUE.getValue();
            공유쪽.Uzziņas_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.lapa_tabula.put(ievade_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(adrese_telpa adrese_reģions, int virtuālā_adrese) {
        lapa_VALUE mērķis = FIND_lapa(adrese_reģions, virtuālā_adrese);
        return mērķis.dati[Math.floorMod(virtuālā_adrese, lappuses_izmēri)];
    }

    public void rakstīšana_byte_VALUE(adrese_telpa adrese_reģions, int virtuālā_adrese, byte VALUE) {
        int INDEX = lapa_numurs(virtuālā_adrese);
        lapa_VALUE mērķis = FIND_lapa(adrese_reģions, virtuālā_adrese);
        if (!mērķis.쓰기가능) {
            if (!mērķis.쓰기시복사) {
                throw new IllegalStateException("Lasīt 전용 쪽입니다.");
            }
            mērķis = atvērt_Privāts_lapa(adrese_reģions, INDEX, mērķis);
        }
        mērķis.dati[Math.floorMod(virtuālā_adrese, lappuses_izmēri)] = VALUE;
    }

    public void Privāts_diapazons_rakstīšana(adrese_telpa adrese_reģions, int Sākt_adrese, int Izmērs) {
        if (Izmērs < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int beigt_zvanu_adrese = Math.addExact(Sākt_adrese, Izmērs);
        for (int adrese = Sākt_adrese; adrese < beigt_zvanu_adrese; adrese = (lapa_numurs(adrese) + 1) * lappuses_izmēri) {
            int INDEX = lapa_numurs(adrese);
            lapa_VALUE mērķis = FIND_lapa(adrese_reģions, adrese);
            if (mērķis.쓰기시복사) {
                atvērt_Privāts_lapa(adrese_reģions, INDEX, mērķis);
            } else {
                mērķis.쓰기가능 = true;
            }
        }
    }

    public void diapazons_rakstīšana(adrese_telpa adrese_reģions, int Sākt_adrese, byte[] dati) {
        for (int INDEX = 0; INDEX < dati.length; INDEX++) {
            rakstīšana_byte_VALUE(adrese_reģions, Sākt_adrese + INDEX, dati[INDEX]);
        }
    }

    private lapa_VALUE atvērt_Privāts_lapa(adrese_telpa adrese_reģions, int INDEX, lapa_VALUE 공유쪽) {
        lapa_VALUE Privāts_lapa = new lapa_VALUE();
        Privāts_lapa.dati = Arrays.copyOf(공유쪽.dati, 공유쪽.dati.length);
        Privāts_lapa.쓰기가능 = true;
        Privāts_lapa.쓰기시복사 = false;
        공유쪽.Uzziņas_COUNT--;
        adrese_reģions.lapa_tabula.put(Integer.valueOf(INDEX), Privāts_lapa);
        return Privāts_lapa;
    }

    private lapa_VALUE FIND_lapa(adrese_telpa adrese_reģions, int adrese) {
        lapa_VALUE mērķis = adrese_reģions.lapa_tabula.get(Integer.valueOf(lapa_numurs(adrese)));
        if (mērķis == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return mērķis;
    }

    private int lapa_numurs(int adrese) {
        if (adrese < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return adrese / lappuses_izmēri;
    }
}

