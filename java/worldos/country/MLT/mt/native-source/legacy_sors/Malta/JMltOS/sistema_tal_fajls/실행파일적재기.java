// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.sistema_tal_fajls;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian eżegwixxa_kmand 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class taqsima_VALUE_366e0bfa {
        private final int 종류;
        private final int mmarka_VALUE;
        private final int ADDRESS;
        private final int fajl_pożizzjoni;
        private final int daqqas;

        taqsima_VALUE_366e0bfa(int 종류, int mmarka_VALUE, int ADDRESS, int fajl_pożizzjoni, int daqqas) {
            this.종류 = 종류;
            this.mmarka_VALUE = mmarka_VALUE;
            this.ADDRESS = ADDRESS;
            this.fajl_pożizzjoni = fajl_pożizzjoni;
            this.daqqas = daqqas;
        }

        public int 종류() {
            return 종류;
        }

        public int mmarka_VALUE() {
            return mmarka_VALUE;
        }

        public int ADDRESS() {
            return ADDRESS;
        }

        public int fajl_pożizzjoni() {
            return fajl_pożizzjoni;
        }

        public int daqqas() {
            return daqqas;
        }
    }

    public static final class IMAGE {
        private final int Bidu_ADDRESS;
        private final List<taqsima_VALUE_366e0bfa> 구역들;

        IMAGE(int Bidu_ADDRESS, List<taqsima_VALUE_366e0bfa> 구역들) {
            this.Bidu_ADDRESS = Bidu_ADDRESS;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Bidu_ADDRESS() {
            return Bidu_ADDRESS;
        }

        public List<taqsima_VALUE_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Bidu_ADDRESS = analizza_numru_sħiħ(data, 24);
        int taqsima_tabella_pożizzjoni = analizza_numru_sħiħ(data, 32);
        int taqsima_entrata_daqqas = 짧은정수읽기(data, 46);
        int taqsima_COUNT = 짧은정수읽기(data, 48);
        if (taqsima_entrata_daqqas < 40 || taqsima_tabella_pożizzjoni < 0
                || (long) taqsima_tabella_pożizzjoni + (long) taqsima_entrata_daqqas * taqsima_COUNT > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<taqsima_VALUE_366e0bfa> 구역들 = new ArrayList<taqsima_VALUE_366e0bfa>();
        for (int INDEX = 0; INDEX < taqsima_COUNT; INDEX++) {
            int pożizzjoni = taqsima_tabella_pożizzjoni + INDEX * taqsima_entrata_daqqas;
            int 종류 = analizza_numru_sħiħ(data, pożizzjoni + 4);
            int mmarka_VALUE = analizza_numru_sħiħ(data, pożizzjoni + 8);
            int ADDRESS = analizza_numru_sħiħ(data, pożizzjoni + 12);
            int fajl_pożizzjoni = analizza_numru_sħiħ(data, pożizzjoni + 16);
            int daqqas = analizza_numru_sħiħ(data, pożizzjoni + 20);
            if (daqqas < 0 || (종류 != 8 && ((long) fajl_pożizzjoni + daqqas > data.length || fajl_pożizzjoni < 0))) {
                throw new IllegalArgumentException("ELF taqsima_VALUE_366e0bfa data 범위가 올바르지 않습니다.");
            }
            구역들.add(new taqsima_VALUE_366e0bfa(종류, mmarka_VALUE, ADDRESS, fajl_pożizzjoni, daqqas));
        }
        return new IMAGE(Bidu_ADDRESS, 구역들);
    }

    private int analizza_numru_sħiħ(byte[] data, int pożizzjoni) {
        if (pożizzjoni < 0 || pożizzjoni > data.length - 4) {
            throw new IllegalArgumentException("ELF numru_sħiħ 범위를 벗어났습니다.");
        }
        return (data[pożizzjoni] & 0xff)
                | ((data[pożizzjoni + 1] & 0xff) << 8)
                | ((data[pożizzjoni + 2] & 0xff) << 16)
                | ((data[pożizzjoni + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int pożizzjoni) {
        if (pożizzjoni < 0 || pożizzjoni > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 numru_sħiħ 범위를 벗어났습니다.");
        }
        return (data[pożizzjoni] & 0xff) | ((data[pożizzjoni + 1] & 0xff) << 8);
    }
}
