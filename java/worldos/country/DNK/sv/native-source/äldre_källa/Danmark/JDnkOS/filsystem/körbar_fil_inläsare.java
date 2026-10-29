// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.filsystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian köra_kommando 파일의 머리부와 적재 구역을 검증한다. */
public final class körbar_fil_inläsare {
    public static final class avsnitt_värde {
        private final int variant_värde;
        private final int flagga_värde;
        private final int Adress;
        private final int fil_placera;
        private final int Storlek;

        avsnitt_värde(int variant_värde, int flagga_värde, int Adress, int fil_placera, int Storlek) {
            this.variant_värde = variant_värde;
            this.flagga_värde = flagga_värde;
            this.Adress = Adress;
            this.fil_placera = fil_placera;
            this.Storlek = Storlek;
        }

        public int variant_värde() {
            return variant_värde;
        }

        public int flagga_värde() {
            return flagga_värde;
        }

        public int Adress() {
            return Adress;
        }

        public int fil_placera() {
            return fil_placera;
        }

        public int Storlek() {
            return Storlek;
        }
    }

    public static final class BILD {
        private final int START_ADRESS;
        private final List<avsnitt_värde> 구역들;

        BILD(int START_ADRESS, List<avsnitt_värde> 구역들) {
            this.START_ADRESS = START_ADRESS;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_ADRESS() {
            return START_ADRESS;
        }

        public List<avsnitt_värde> 구역들() {
            return 구역들;
        }
    }

    public BILD 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_ADRESS = parsa_heltal(data, 24);
        int avsnitt_tabell_placera = parsa_heltal(data, 32);
        int avsnitt_post_storlek = 짧은정수읽기(data, 46);
        int avsnitt_ANTAL = 짧은정수읽기(data, 48);
        if (avsnitt_post_storlek < 40 || avsnitt_tabell_placera < 0
                || (long) avsnitt_tabell_placera + (long) avsnitt_post_storlek * avsnitt_ANTAL > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<avsnitt_värde> 구역들 = new ArrayList<avsnitt_värde>();
        for (int INDEX = 0; INDEX < avsnitt_ANTAL; INDEX++) {
            int position = avsnitt_tabell_placera + INDEX * avsnitt_post_storlek;
            int variant_värde = parsa_heltal(data, position + 4);
            int flagga_värde = parsa_heltal(data, position + 8);
            int Adress = parsa_heltal(data, position + 12);
            int fil_placera = parsa_heltal(data, position + 16);
            int Storlek = parsa_heltal(data, position + 20);
            if (Storlek < 0 || (variant_värde != 8 && ((long) fil_placera + Storlek > data.length || fil_placera < 0))) {
                throw new IllegalArgumentException("ELF avsnitt_värde data 범위가 올바르지 않습니다.");
            }
            구역들.add(new avsnitt_värde(variant_värde, flagga_värde, Adress, fil_placera, Storlek));
        }
        return new BILD(START_ADRESS, 구역들);
    }

    private int parsa_heltal(byte[] data, int position) {
        if (position < 0 || position > data.length - 4) {
            throw new IllegalArgumentException("ELF heltal 범위를 벗어났습니다.");
        }
        return (data[position] & 0xff)
                | ((data[position + 1] & 0xff) << 8)
                | ((data[position + 2] & 0xff) << 16)
                | ((data[position + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int position) {
        if (position < 0 || position > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 heltal 범위를 벗어났습니다.");
        }
        return (data[position] & 0xff) | ((data[position + 1] & 0xff) << 8);
    }
}
