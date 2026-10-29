// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Maďarsko.JHunOS.systém_súborov;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Vykonať_príkaz 파일의 머리부와 적재 구역을 검증한다. */
public final class spustiteľný_súbor_zavádzací_program {
    public static final class sekcia_VALUE {
        private final int 종류;
        private final int príznak_VALUE;
        private final int adresa;
        private final int Súbor_pozícia;
        private final int Veľkosť;

        sekcia_VALUE(int 종류, int príznak_VALUE, int adresa, int Súbor_pozícia, int Veľkosť) {
            this.종류 = 종류;
            this.príznak_VALUE = príznak_VALUE;
            this.adresa = adresa;
            this.Súbor_pozícia = Súbor_pozícia;
            this.Veľkosť = Veľkosť;
        }

        public int 종류() {
            return 종류;
        }

        public int príznak_VALUE() {
            return príznak_VALUE;
        }

        public int adresa() {
            return adresa;
        }

        public int Súbor_pozícia() {
            return Súbor_pozícia;
        }

        public int Veľkosť() {
            return Veľkosť;
        }
    }

    public static final class IMAGE {
        private final int START_adresa;
        private final List<sekcia_VALUE> 구역들;

        IMAGE(int START_adresa, List<sekcia_VALUE> 구역들) {
            this.START_adresa = START_adresa;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_adresa() {
            return START_adresa;
        }

        public List<sekcia_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] údaje) {
        if (údaje == null || údaje.length < 52
                || údaje[0] != 0x7f || údaje[1] != 'E' || údaje[2] != 'L' || údaje[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (údaje[4] != 1 || údaje[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_adresa = analyzovať_celé_číslo(údaje, 24);
        int sekcia_tabuľka_pozícia = analyzovať_celé_číslo(údaje, 32);
        int sekcia_položka_zmeniť_veľkosť = 짧은정수읽기(údaje, 46);
        int sekcia_COUNT = 짧은정수읽기(údaje, 48);
        if (sekcia_položka_zmeniť_veľkosť < 40 || sekcia_tabuľka_pozícia < 0
                || (long) sekcia_tabuľka_pozícia + (long) sekcia_položka_zmeniť_veľkosť * sekcia_COUNT > údaje.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sekcia_VALUE> 구역들 = new ArrayList<sekcia_VALUE>();
        for (int INDEX = 0; INDEX < sekcia_COUNT; INDEX++) {
            int Pozícia = sekcia_tabuľka_pozícia + INDEX * sekcia_položka_zmeniť_veľkosť;
            int 종류 = analyzovať_celé_číslo(údaje, Pozícia + 4);
            int príznak_VALUE = analyzovať_celé_číslo(údaje, Pozícia + 8);
            int adresa = analyzovať_celé_číslo(údaje, Pozícia + 12);
            int Súbor_pozícia = analyzovať_celé_číslo(údaje, Pozícia + 16);
            int Veľkosť = analyzovať_celé_číslo(údaje, Pozícia + 20);
            if (Veľkosť < 0 || (종류 != 8 && ((long) Súbor_pozícia + Veľkosť > údaje.length || Súbor_pozícia < 0))) {
                throw new IllegalArgumentException("ELF sekcia_VALUE údaje 범위가 올바르지 않습니다.");
            }
            구역들.add(new sekcia_VALUE(종류, príznak_VALUE, adresa, Súbor_pozícia, Veľkosť));
        }
        return new IMAGE(START_adresa, 구역들);
    }

    private int analyzovať_celé_číslo(byte[] údaje, int Pozícia) {
        if (Pozícia < 0 || Pozícia > údaje.length - 4) {
            throw new IllegalArgumentException("ELF celé_číslo 범위를 벗어났습니다.");
        }
        return (údaje[Pozícia] & 0xff)
                | ((údaje[Pozícia + 1] & 0xff) << 8)
                | ((údaje[Pozícia + 2] & 0xff) << 16)
                | ((údaje[Pozícia + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] údaje, int Pozícia) {
        if (Pozícia < 0 || Pozícia > údaje.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 celé_číslo 범위를 벗어났습니다.");
        }
        return (údaje[Pozícia] & 0xff) | ((údaje[Pozícia + 1] & 0xff) << 8);
    }
}
