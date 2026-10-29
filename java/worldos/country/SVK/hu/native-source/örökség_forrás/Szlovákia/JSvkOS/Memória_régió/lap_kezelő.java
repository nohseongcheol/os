// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szlovákia.JSvkOS.Memória_régió;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB lap_ÉRTÉK 연결과 Írás 시 복사를 제공한다. */
public final class lap_kezelő {
    public static final int oldalméret = 4096;

    private static final class lap_ÉRTÉK {
        private byte[] adat = new byte[oldalméret];
        private int hivatkozik_DARAB = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class címtartomány {
        private final Map<Integer, lap_ÉRTÉK> lap_tábla = new HashMap<Integer, lap_ÉRTÉK>();
    }

    public címtartomány 새주소공간() {
        return new címtartomány();
    }

    public void MAP_lap(címtartomány CÍM_régió, int virtuális_cím, boolean 쓰기가능) {
        int INDEX = lap_szám(virtuális_cím);
        lap_ÉRTÉK 새쪽 = new lap_ÉRTÉK();
        새쪽.쓰기가능 = 쓰기가능;
        CÍM_régió.lap_tábla.put(Integer.valueOf(INDEX), 새쪽);
    }

    public címtartomány 쓰기시복사복제(címtartomány 원본) {
        címtartomány 복제본 = new címtartomány();
        for (Map.Entry<Integer, lap_ÉRTÉK> bejegyzés_ÉRTÉK : 원본.lap_tábla.entrySet()) {
            lap_ÉRTÉK Közös_lap = bejegyzés_ÉRTÉK.getValue();
            Közös_lap.hivatkozik_DARAB++;
            if (Közös_lap.쓰기가능) {
                Közös_lap.쓰기가능 = false;
                Közös_lap.쓰기시복사 = true;
            }
            복제본.lap_tábla.put(bejegyzés_ÉRTÉK.getKey(), Közös_lap);
        }
        return 복제본;
    }

    public byte 바이트읽기(címtartomány CÍM_régió, int virtuális_cím) {
        lap_ÉRTÉK cél = keres_lap(CÍM_régió, virtuális_cím);
        return cél.adat[Math.floorMod(virtuális_cím, oldalméret)];
    }

    public void ír_bájt_ÉRTÉK(címtartomány CÍM_régió, int virtuális_cím, byte ÉRTÉK) {
        int INDEX = lap_szám(virtuális_cím);
        lap_ÉRTÉK cél = keres_lap(CÍM_régió, virtuális_cím);
        if (!cél.쓰기가능) {
            if (!cél.쓰기시복사) {
                throw new IllegalStateException("Olvasás 전용 쪽입니다.");
            }
            cél = készít_privát_lap(CÍM_régió, INDEX, cél);
        }
        cél.adat[Math.floorMod(virtuális_cím, oldalméret)] = ÉRTÉK;
    }

    public void privát_tartomány_ír(címtartomány CÍM_régió, int START_CÍM, int Méret) {
        if (Méret < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int megszüntet_CÍM = Math.addExact(START_CÍM, Méret);
        for (int CÍM = START_CÍM; CÍM < megszüntet_CÍM; CÍM = (lap_szám(CÍM) + 1) * oldalméret) {
            int INDEX = lap_szám(CÍM);
            lap_ÉRTÉK cél = keres_lap(CÍM_régió, CÍM);
            if (cél.쓰기시복사) {
                készít_privát_lap(CÍM_régió, INDEX, cél);
            } else {
                cél.쓰기가능 = true;
            }
        }
    }

    public void tartomány_ír(címtartomány CÍM_régió, int START_CÍM, byte[] adat) {
        for (int INDEX = 0; INDEX < adat.length; INDEX++) {
            ír_bájt_ÉRTÉK(CÍM_régió, START_CÍM + INDEX, adat[INDEX]);
        }
    }

    private lap_ÉRTÉK készít_privát_lap(címtartomány CÍM_régió, int INDEX, lap_ÉRTÉK Közös_lap) {
        lap_ÉRTÉK privát_lap = new lap_ÉRTÉK();
        privát_lap.adat = Arrays.copyOf(Közös_lap.adat, Közös_lap.adat.length);
        privát_lap.쓰기가능 = true;
        privát_lap.쓰기시복사 = false;
        Közös_lap.hivatkozik_DARAB--;
        CÍM_régió.lap_tábla.put(Integer.valueOf(INDEX), privát_lap);
        return privát_lap;
    }

    private lap_ÉRTÉK keres_lap(címtartomány CÍM_régió, int CÍM) {
        lap_ÉRTÉK cél = CÍM_régió.lap_tábla.get(Integer.valueOf(lap_szám(CÍM)));
        if (cél == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return cél;
    }

    private int lap_szám(int CÍM) {
        if (CÍM < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return CÍM / oldalméret;
    }
}

