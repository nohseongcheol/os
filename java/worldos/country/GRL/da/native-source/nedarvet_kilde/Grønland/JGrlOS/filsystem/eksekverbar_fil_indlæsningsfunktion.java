// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Grønland.JGrlOS.filsystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Udfør_kommando 파일의 머리부와 적재 구역을 검증한다. */
public final class eksekverbar_fil_indlæsningsfunktion {
    public static final class sektion_VÆRDI {
        private final int 종류;
        private final int flag_VÆRDI;
        private final int mail;
        private final int fil_placere;
        private final int Størrelse;

        sektion_VÆRDI(int 종류, int flag_VÆRDI, int mail, int fil_placere, int Størrelse) {
            this.종류 = 종류;
            this.flag_VÆRDI = flag_VÆRDI;
            this.mail = mail;
            this.fil_placere = fil_placere;
            this.Størrelse = Størrelse;
        }

        public int 종류() {
            return 종류;
        }

        public int flag_VÆRDI() {
            return flag_VÆRDI;
        }

        public int mail() {
            return mail;
        }

        public int fil_placere() {
            return fil_placere;
        }

        public int Størrelse() {
            return Størrelse;
        }
    }

    public static final class Image {
        private final int START_mail;
        private final List<sektion_VÆRDI> 구역들;

        Image(int START_mail, List<sektion_VÆRDI> 구역들) {
            this.START_mail = START_mail;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_mail() {
            return START_mail;
        }

        public List<sektion_VÆRDI> 구역들() {
            return 구역들;
        }
    }

    public Image 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_mail = opdele_tekst_heltal(data, 24);
        int sektion_tabel_placere = opdele_tekst_heltal(data, 32);
        int sektion_post_tilpasse_størrelse = 짧은정수읽기(data, 46);
        int sektion_TÆL = 짧은정수읽기(data, 48);
        if (sektion_post_tilpasse_størrelse < 40 || sektion_tabel_placere < 0
                || (long) sektion_tabel_placere + (long) sektion_post_tilpasse_størrelse * sektion_TÆL > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sektion_VÆRDI> 구역들 = new ArrayList<sektion_VÆRDI>();
        for (int INDEKS = 0; INDEKS < sektion_TÆL; INDEKS++) {
            int Placering = sektion_tabel_placere + INDEKS * sektion_post_tilpasse_størrelse;
            int 종류 = opdele_tekst_heltal(data, Placering + 4);
            int flag_VÆRDI = opdele_tekst_heltal(data, Placering + 8);
            int mail = opdele_tekst_heltal(data, Placering + 12);
            int fil_placere = opdele_tekst_heltal(data, Placering + 16);
            int Størrelse = opdele_tekst_heltal(data, Placering + 20);
            if (Størrelse < 0 || (종류 != 8 && ((long) fil_placere + Størrelse > data.length || fil_placere < 0))) {
                throw new IllegalArgumentException("ELF sektion_VÆRDI data 범위가 올바르지 않습니다.");
            }
            구역들.add(new sektion_VÆRDI(종류, flag_VÆRDI, mail, fil_placere, Størrelse));
        }
        return new Image(START_mail, 구역들);
    }

    private int opdele_tekst_heltal(byte[] data, int Placering) {
        if (Placering < 0 || Placering > data.length - 4) {
            throw new IllegalArgumentException("ELF heltal 범위를 벗어났습니다.");
        }
        return (data[Placering] & 0xff)
                | ((data[Placering + 1] & 0xff) << 8)
                | ((data[Placering + 2] & 0xff) << 16)
                | ((data[Placering + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int Placering) {
        if (Placering < 0 || Placering > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 heltal 범위를 벗어났습니다.");
        }
        return (data[Placering] & 0xff) | ((data[Placering + 1] & 0xff) << 8);
    }
}
