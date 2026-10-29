// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Azərbaycan.JAzeOS.fayl_sistemi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian icra_etmək_əmr 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class bölmə_VALUE_366e0bfa {
        private final int 종류;
        private final int bayraq_VALUE;
        private final int ünvan;
        private final int fayl_yerinə_qoymaq;
        private final int Böyüklük;

        bölmə_VALUE_366e0bfa(int 종류, int bayraq_VALUE, int ünvan, int fayl_yerinə_qoymaq, int Böyüklük) {
            this.종류 = 종류;
            this.bayraq_VALUE = bayraq_VALUE;
            this.ünvan = ünvan;
            this.fayl_yerinə_qoymaq = fayl_yerinə_qoymaq;
            this.Böyüklük = Böyüklük;
        }

        public int 종류() {
            return 종류;
        }

        public int bayraq_VALUE() {
            return bayraq_VALUE;
        }

        public int ünvan() {
            return ünvan;
        }

        public int fayl_yerinə_qoymaq() {
            return fayl_yerinə_qoymaq;
        }

        public int Böyüklük() {
            return Böyüklük;
        }
    }

    public static final class IMAGE {
        private final int başlama_ünvanı;
        private final List<bölmə_VALUE_366e0bfa> 구역들;

        IMAGE(int başlama_ünvanı, List<bölmə_VALUE_366e0bfa> 구역들) {
            this.başlama_ünvanı = başlama_ünvanı;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int başlama_ünvanı() {
            return başlama_ünvanı;
        }

        public List<bölmə_VALUE_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] verilənlər) {
        if (verilənlər == null || verilənlər.length < 52
                || verilənlər[0] != 0x7f || verilənlər[1] != 'E' || verilənlər[2] != 'L' || verilənlər[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (verilənlər[4] != 1 || verilənlər[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int başlama_ünvanı = parselləmək_tam_ədəd(verilənlər, 24);
        int bölmə_cədvəl_yerinə_qoymaq = parselləmək_tam_ədəd(verilənlər, 32);
        int bölmə_daxiletmə_ölçünü_dəyişmək = 짧은정수읽기(verilənlər, 46);
        int bölmə_COUNT = 짧은정수읽기(verilənlər, 48);
        if (bölmə_daxiletmə_ölçünü_dəyişmək < 40 || bölmə_cədvəl_yerinə_qoymaq < 0
                || (long) bölmə_cədvəl_yerinə_qoymaq + (long) bölmə_daxiletmə_ölçünü_dəyişmək * bölmə_COUNT > verilənlər.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<bölmə_VALUE_366e0bfa> 구역들 = new ArrayList<bölmə_VALUE_366e0bfa>();
        for (int INDEX = 0; INDEX < bölmə_COUNT; INDEX++) {
            int yerinə_qoymaq = bölmə_cədvəl_yerinə_qoymaq + INDEX * bölmə_daxiletmə_ölçünü_dəyişmək;
            int 종류 = parselləmək_tam_ədəd(verilənlər, yerinə_qoymaq + 4);
            int bayraq_VALUE = parselləmək_tam_ədəd(verilənlər, yerinə_qoymaq + 8);
            int ünvan = parselləmək_tam_ədəd(verilənlər, yerinə_qoymaq + 12);
            int fayl_yerinə_qoymaq = parselləmək_tam_ədəd(verilənlər, yerinə_qoymaq + 16);
            int Böyüklük = parselləmək_tam_ədəd(verilənlər, yerinə_qoymaq + 20);
            if (Böyüklük < 0 || (종류 != 8 && ((long) fayl_yerinə_qoymaq + Böyüklük > verilənlər.length || fayl_yerinə_qoymaq < 0))) {
                throw new IllegalArgumentException("ELF bölmə_VALUE_366e0bfa verilənlər 범위가 올바르지 않습니다.");
            }
            구역들.add(new bölmə_VALUE_366e0bfa(종류, bayraq_VALUE, ünvan, fayl_yerinə_qoymaq, Böyüklük));
        }
        return new IMAGE(başlama_ünvanı, 구역들);
    }

    private int parselləmək_tam_ədəd(byte[] verilənlər, int yerinə_qoymaq) {
        if (yerinə_qoymaq < 0 || yerinə_qoymaq > verilənlər.length - 4) {
            throw new IllegalArgumentException("ELF tam_ədəd 범위를 벗어났습니다.");
        }
        return (verilənlər[yerinə_qoymaq] & 0xff)
                | ((verilənlər[yerinə_qoymaq + 1] & 0xff) << 8)
                | ((verilənlər[yerinə_qoymaq + 2] & 0xff) << 16)
                | ((verilənlər[yerinə_qoymaq + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] verilənlər, int yerinə_qoymaq) {
        if (yerinə_qoymaq < 0 || yerinə_qoymaq > verilənlər.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 tam_ədəd 범위를 벗어났습니다.");
        }
        return (verilənlər[yerinə_qoymaq] & 0xff) | ((verilənlər[yerinə_qoymaq + 1] & 0xff) << 8);
    }
}
