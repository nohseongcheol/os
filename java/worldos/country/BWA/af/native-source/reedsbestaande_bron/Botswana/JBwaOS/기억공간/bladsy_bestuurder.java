// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB bladsy_VALUE 연결과 Skryf 시 복사를 제공한다. */
public final class bladsy_bestuurder {
    public static final int bladsygrootte = 4096;

    private static final class bladsy_VALUE {
        private byte[] data = new byte[bladsygrootte];
        private int Naslaan_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adres_ruimte {
        private final Map<Integer, bladsy_VALUE> bladsy_tabel = new HashMap<Integer, bladsy_VALUE>();
    }

    public adres_ruimte 새주소공간() {
        return new adres_ruimte();
    }

    public void MAP_bladsy(adres_ruimte 공간, int virtuele_adres, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtuele_adres);
        bladsy_VALUE 새쪽 = new bladsy_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.bladsy_tabel.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adres_ruimte 쓰기시복사복제(adres_ruimte 원본) {
        adres_ruimte 복제본 = new adres_ruimte();
        for (Map.Entry<Integer, bladsy_VALUE> inskrywing_VALUE : 원본.bladsy_tabel.entrySet()) {
            bladsy_VALUE 공유쪽 = inskrywing_VALUE.getValue();
            공유쪽.Naslaan_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.bladsy_tabel.put(inskrywing_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(adres_ruimte 공간, int virtuele_adres) {
        bladsy_VALUE teiken = FIND_bladsy(공간, virtuele_adres);
        return teiken.data[Math.floorMod(virtuele_adres, bladsygrootte)];
    }

    public void skryf_greep_VALUE(adres_ruimte 공간, int virtuele_adres, byte VALUE) {
        int INDEX = 쪽번호(virtuele_adres);
        bladsy_VALUE teiken = FIND_bladsy(공간, virtuele_adres);
        if (!teiken.쓰기가능) {
            if (!teiken.쓰기시복사) {
                throw new IllegalStateException("Lees 전용 쪽입니다.");
            }
            teiken = Skep_Privaat_bladsy(공간, INDEX, teiken);
        }
        teiken.data[Math.floorMod(virtuele_adres, bladsygrootte)] = VALUE;
    }

    public void 범위개인쓰기(adres_ruimte 공간, int BEGIN_adres, int Grootte) {
        if (Grootte < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int beëindig_adres = Math.addExact(BEGIN_adres, Grootte);
        for (int adres = BEGIN_adres; adres < beëindig_adres; adres = (쪽번호(adres) + 1) * bladsygrootte) {
            int INDEX = 쪽번호(adres);
            bladsy_VALUE teiken = FIND_bladsy(공간, adres);
            if (teiken.쓰기시복사) {
                Skep_Privaat_bladsy(공간, INDEX, teiken);
            } else {
                teiken.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(adres_ruimte 공간, int BEGIN_adres, byte[] data) {
        for (int INDEX = 0; INDEX < data.length; INDEX++) {
            skryf_greep_VALUE(공간, BEGIN_adres + INDEX, data[INDEX]);
        }
    }

    private bladsy_VALUE Skep_Privaat_bladsy(adres_ruimte 공간, int INDEX, bladsy_VALUE 공유쪽) {
        bladsy_VALUE Privaat_bladsy = new bladsy_VALUE();
        Privaat_bladsy.data = Arrays.copyOf(공유쪽.data, 공유쪽.data.length);
        Privaat_bladsy.쓰기가능 = true;
        Privaat_bladsy.쓰기시복사 = false;
        공유쪽.Naslaan_COUNT--;
        공간.bladsy_tabel.put(Integer.valueOf(INDEX), Privaat_bladsy);
        return Privaat_bladsy;
    }

    private bladsy_VALUE FIND_bladsy(adres_ruimte 공간, int adres) {
        bladsy_VALUE teiken = 공간.bladsy_tabel.get(Integer.valueOf(쪽번호(adres)));
        if (teiken == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return teiken;
    }

    private int 쪽번호(int adres) {
        if (adres < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return adres / bladsygrootte;
    }
}

