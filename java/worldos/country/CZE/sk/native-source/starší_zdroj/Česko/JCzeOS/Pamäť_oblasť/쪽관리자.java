// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.Pamäť_oblasť;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB strana_VALUE 연결과 Zápis 시 복사를 제공한다. */
public final class 쪽관리자 {
    public static final int veľkosť_stránky = 4096;

    private static final class strana_VALUE {
        private byte[] údaje = new byte[veľkosť_stránky];
        private int zdroj_COUNT = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class adresa_priestor {
        private final Map<Integer, strana_VALUE> strana_tabuľka = new HashMap<Integer, strana_VALUE>();
    }

    public adresa_priestor 새주소공간() {
        return new adresa_priestor();
    }

    public void MAP_strana(adresa_priestor adresa_oblasť, int virtuálna_adresa, boolean 쓰기가능) {
        int INDEX = 쪽번호(virtuálna_adresa);
        strana_VALUE 새쪽 = new strana_VALUE();
        새쪽.쓰기가능 = 쓰기가능;
        adresa_oblasť.strana_tabuľka.put(Integer.valueOf(INDEX), 새쪽);
    }

    public adresa_priestor 쓰기시복사복제(adresa_priestor 원본) {
        adresa_priestor 복제본 = new adresa_priestor();
        for (Map.Entry<Integer, strana_VALUE> položka_VALUE : 원본.strana_tabuľka.entrySet()) {
            strana_VALUE 공유쪽 = položka_VALUE.getValue();
            공유쪽.zdroj_COUNT++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.strana_tabuľka.put(položka_VALUE.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(adresa_priestor adresa_oblasť, int virtuálna_adresa) {
        strana_VALUE cieľová_hodnota = FIND_strana(adresa_oblasť, virtuálna_adresa);
        return cieľová_hodnota.údaje[Math.floorMod(virtuálna_adresa, veľkosť_stránky)];
    }

    public void zapísať_Byte_VALUE(adresa_priestor adresa_oblasť, int virtuálna_adresa, byte VALUE) {
        int INDEX = 쪽번호(virtuálna_adresa);
        strana_VALUE cieľová_hodnota = FIND_strana(adresa_oblasť, virtuálna_adresa);
        if (!cieľová_hodnota.쓰기가능) {
            if (!cieľová_hodnota.쓰기시복사) {
                throw new IllegalStateException("Čítanie 전용 쪽입니다.");
            }
            cieľová_hodnota = Create_súkromné_strana(adresa_oblasť, INDEX, cieľová_hodnota);
        }
        cieľová_hodnota.údaje[Math.floorMod(virtuálna_adresa, veľkosť_stránky)] = VALUE;
    }

    public void súkromné_rozsah_zapísať(adresa_priestor adresa_oblasť, int START_adresa, int Veľkosť) {
        if (Veľkosť < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ukončiť_hovor_adresa = Math.addExact(START_adresa, Veľkosť);
        for (int adresa = START_adresa; adresa < ukončiť_hovor_adresa; adresa = (쪽번호(adresa) + 1) * veľkosť_stránky) {
            int INDEX = 쪽번호(adresa);
            strana_VALUE cieľová_hodnota = FIND_strana(adresa_oblasť, adresa);
            if (cieľová_hodnota.쓰기시복사) {
                Create_súkromné_strana(adresa_oblasť, INDEX, cieľová_hodnota);
            } else {
                cieľová_hodnota.쓰기가능 = true;
            }
        }
    }

    public void rozsah_zapísať(adresa_priestor adresa_oblasť, int START_adresa, byte[] údaje) {
        for (int INDEX = 0; INDEX < údaje.length; INDEX++) {
            zapísať_Byte_VALUE(adresa_oblasť, START_adresa + INDEX, údaje[INDEX]);
        }
    }

    private strana_VALUE Create_súkromné_strana(adresa_priestor adresa_oblasť, int INDEX, strana_VALUE 공유쪽) {
        strana_VALUE súkromné_strana = new strana_VALUE();
        súkromné_strana.údaje = Arrays.copyOf(공유쪽.údaje, 공유쪽.údaje.length);
        súkromné_strana.쓰기가능 = true;
        súkromné_strana.쓰기시복사 = false;
        공유쪽.zdroj_COUNT--;
        adresa_oblasť.strana_tabuľka.put(Integer.valueOf(INDEX), súkromné_strana);
        return súkromné_strana;
    }

    private strana_VALUE FIND_strana(adresa_priestor adresa_oblasť, int adresa) {
        strana_VALUE cieľová_hodnota = adresa_oblasť.strana_tabuľka.get(Integer.valueOf(쪽번호(adresa)));
        if (cieľová_hodnota == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return cieľová_hodnota;
    }

    private int 쪽번호(int adresa) {
        if (adresa < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return adresa / veľkosť_stránky;
    }
}

