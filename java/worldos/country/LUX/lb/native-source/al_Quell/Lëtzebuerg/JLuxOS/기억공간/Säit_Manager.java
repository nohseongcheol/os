// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB Säit_VALUE 연결과 schreiwen 시 복사를 제공한다. */
public final class Säit_Manager {
    public static final int Säitegréisst = 4096;

    private static final class Säit_VALUE {
        private byte[] Daten = new byte[Säitegréisst];
        private int Referenzen_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class Adress_Plaz {
        private final Map<Integer, Säit_VALUE> Säit_Tabell = new HashMap<Integer, Säit_VALUE>();
    }

    public Adress_Plaz 새주소공간() {
        return new Adress_Plaz();
    }

    public void MAP_Säit(Adress_Plaz 공간, int virtuell_Adress, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtuell_Adress);
        Säit_VALUE 새쪽 = new Säit_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        공간.Säit_Tabell.put(Integer.valueOf(INDEX), 새쪽);
    }

    public Adress_Plaz 쓰기시복사복제(Adress_Plaz 원본) {
        Adress_Plaz 복제본 = new Adress_Plaz();
        for (Map.Entry<Integer, Säit_VALUE> Agab_VALUE : 원본.Säit_Tabell.entrySet()) {
            Säit_VALUE 공유쪽 = Agab_VALUE.getValue();
            공유쪽.Referenzen_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.Säit_Tabell.put(Agab_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(Adress_Plaz 공간, int virtuell_Adress) {
        Säit_VALUE Zil = FIND_Säit(공간, virtuell_Adress);
        return Zil.Daten[Math.floorMod(virtuell_Adress, Säitegréisst)];
    }

    public void schreiwen_Byte_VALUE(Adress_Plaz 공간, int virtuell_Adress, byte VALUE) {
        int INDEX = 쪽번호(virtuell_Adress);
        Säit_VALUE Zil = FIND_Säit(공간, virtuell_Adress);
        if (!Zil.쓰기가능) {
            if (!Zil.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            Zil = Create_privat_Säit(공간, INDEX, Zil);
        }
        Zil.Daten[Math.floorMod(virtuell_Adress, Säitegréisst)] = VALUE;
    }

    public void 범위개인쓰기(Adress_Plaz 공간, int Start_Adress, int d_Gréisst_veränneren) {
        if (d_Gréisst_veränneren < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int bëennegen_Adress = Math.addExact(Start_Adress, d_Gréisst_veränneren);
        for (int Adress = Start_Adress; Adress < bëennegen_Adress; Adress = (쪽번호(Adress) + 1) * Säitegréisst) {
            int INDEX = 쪽번호(Adress);
            Säit_VALUE Zil = FIND_Säit(공간, Adress);
            if (Zil.쓰기시복사) {
                Create_privat_Säit(공간, INDEX, Zil);
            } else {
                Zil.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(Adress_Plaz 공간, int Start_Adress, byte[] Daten) {
        for (int INDEX = 0; INDEX < Daten.length; INDEX++) {
            schreiwen_Byte_VALUE(공간, Start_Adress + INDEX, Daten[INDEX]);
        }
    }

    private Säit_VALUE Create_privat_Säit(Adress_Plaz 공간, int INDEX, Säit_VALUE 공유쪽) {
        Säit_VALUE privat_Säit = new Säit_VALUE();
        privat_Säit.Daten = Arrays.copyOf(공유쪽.Daten, 공유쪽.Daten.length);
        privat_Säit.쓰기가능 = true;
        privat_Säit.쓰기시복사 = false;
        공유쪽.Referenzen_COUNT--;
        공간.Säit_Tabell.put(Integer.valueOf(INDEX), privat_Säit);
        return privat_Säit;
    }

    private Säit_VALUE FIND_Säit(Adress_Plaz 공간, int Adress) {
        Säit_VALUE Zil = 공간.Säit_Tabell.get(Integer.valueOf(쪽번호(Adress)));
        if (Zil == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return Zil;
    }

    private int 쪽번호(int Adress) {
        if (Adress < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return Adress / Säitegréisst;
    }
}

