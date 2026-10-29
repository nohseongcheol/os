// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Andorra.JAndOS.sistema_d_arxius;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Executa_ordre 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class secció_VALOR {
        private final int 종류;
        private final int marcar_VALOR_58846146;
        private final int Adreça;
        private final int arxiu_càrrec;
        private final int Mida;

        secció_VALOR(int 종류, int marcar_VALOR_58846146, int Adreça, int arxiu_càrrec, int Mida) {
            this.종류 = 종류;
            this.marcar_VALOR_58846146 = marcar_VALOR_58846146;
            this.Adreça = Adreça;
            this.arxiu_càrrec = arxiu_càrrec;
            this.Mida = Mida;
        }

        public int 종류() {
            return 종류;
        }

        public int marcar_VALOR_58846146() {
            return marcar_VALOR_58846146;
        }

        public int Adreça() {
            return Adreça;
        }

        public int arxiu_càrrec() {
            return arxiu_càrrec;
        }

        public int Mida() {
            return Mida;
        }
    }

    public static final class IMATGE {
        private final int Inici_ADREÇA;
        private final List<secció_VALOR> 구역들;

        IMATGE(int Inici_ADREÇA, List<secció_VALOR> 구역들) {
            this.Inici_ADREÇA = Inici_ADREÇA;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Inici_ADREÇA() {
            return Inici_ADREÇA;
        }

        public List<secció_VALOR> 구역들() {
            return 구역들;
        }
    }

    public IMATGE 검사(byte[] dades) {
        if (dades == null || dades.length < 52
                || dades[0] != 0x7f || dades[1] != 'E' || dades[2] != 'L' || dades[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (dades[4] != 1 || dades[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Inici_ADREÇA = 정수읽기(dades, 24);
        int secció_taula_càrrec = 정수읽기(dades, 32);
        int secció_introducció_canviar_la_mida = 짧은정수읽기(dades, 46);
        int secció_COMPT = 짧은정수읽기(dades, 48);
        if (secció_introducció_canviar_la_mida < 40 || secció_taula_càrrec < 0
                || (long) secció_taula_càrrec + (long) secció_introducció_canviar_la_mida * secció_COMPT > dades.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<secció_VALOR> 구역들 = new ArrayList<secció_VALOR>();
        for (int INDEX = 0; INDEX < secció_COMPT; INDEX++) {
            int Posició = secció_taula_càrrec + INDEX * secció_introducció_canviar_la_mida;
            int 종류 = 정수읽기(dades, Posició + 4);
            int marcar_VALOR_58846146 = 정수읽기(dades, Posició + 8);
            int Adreça = 정수읽기(dades, Posició + 12);
            int arxiu_càrrec = 정수읽기(dades, Posició + 16);
            int Mida = 정수읽기(dades, Posició + 20);
            if (Mida < 0 || (종류 != 8 && ((long) arxiu_càrrec + Mida > dades.length || arxiu_càrrec < 0))) {
                throw new IllegalArgumentException("ELF secció_VALOR dades 범위가 올바르지 않습니다.");
            }
            구역들.add(new secció_VALOR(종류, marcar_VALOR_58846146, Adreça, arxiu_càrrec, Mida));
        }
        return new IMATGE(Inici_ADREÇA, 구역들);
    }

    private int 정수읽기(byte[] dades, int Posició) {
        if (Posició < 0 || Posició > dades.length - 4) {
            throw new IllegalArgumentException("ELF 정수 범위를 벗어났습니다.");
        }
        return (dades[Posició] & 0xff)
                | ((dades[Posició + 1] & 0xff) << 8)
                | ((dades[Posició + 2] & 0xff) << 16)
                | ((dades[Posició + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] dades, int Posició) {
        if (Posició < 0 || Posició > dades.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 정수 범위를 벗어났습니다.");
        }
        return (dades[Posició] & 0xff) | ((dades[Posició + 1] & 0xff) << 8);
    }
}
