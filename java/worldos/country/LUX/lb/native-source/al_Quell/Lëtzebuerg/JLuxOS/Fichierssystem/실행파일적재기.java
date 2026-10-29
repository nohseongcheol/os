// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Fichierssystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ausféieren_Befeel 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class Beräich_VALUE {
        private final int 종류;
        private final int kennzeechnen_VALUE;
        private final int Adress;
        private final int Fichier_positionéieren;
        private final int d_Gréisst_veränneren;

        Beräich_VALUE(int 종류, int kennzeechnen_VALUE, int Adress, int Fichier_positionéieren, int d_Gréisst_veränneren) {
            this.종류 = 종류;
            this.kennzeechnen_VALUE = kennzeechnen_VALUE;
            this.Adress = Adress;
            this.Fichier_positionéieren = Fichier_positionéieren;
            this.d_Gréisst_veränneren = d_Gréisst_veränneren;
        }

        public int 종류() {
            return 종류;
        }

        public int kennzeechnen_VALUE() {
            return kennzeechnen_VALUE;
        }

        public int Adress() {
            return Adress;
        }

        public int Fichier_positionéieren() {
            return Fichier_positionéieren;
        }

        public int d_Gréisst_veränneren() {
            return d_Gréisst_veränneren;
        }
    }

    public static final class Bild {
        private final int Start_Adress;
        private final List<Beräich_VALUE> 구역들;

        Bild(int Start_Adress, List<Beräich_VALUE> 구역들) {
            this.Start_Adress = Start_Adress;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_Adress() {
            return Start_Adress;
        }

        public List<Beräich_VALUE> 구역들() {
            return 구역들;
        }
    }

    public Bild 검사(byte[] Daten) {
        if (Daten == null || Daten.length < 52
                || Daten[0] != 0x7f || Daten[1] != 'E' || Daten[2] != 'L' || Daten[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (Daten[4] != 1 || Daten[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_Adress = analyséieren_Ganzzuel(Daten, 24);
        int Beräich_Tabell_positionéieren = analyséieren_Ganzzuel(Daten, 32);
        int Beräich_Agab_d_Gréisst_veränneren = 짧은정수읽기(Daten, 46);
        int Beräich_COUNT = 짧은정수읽기(Daten, 48);
        if (Beräich_Agab_d_Gréisst_veränneren < 40 || Beräich_Tabell_positionéieren < 0
                || (long) Beräich_Tabell_positionéieren + (long) Beräich_Agab_d_Gréisst_veränneren * Beräich_COUNT > Daten.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<Beräich_VALUE> 구역들 = new ArrayList<Beräich_VALUE>();
        for (int INDEX = 0; INDEX < Beräich_COUNT; INDEX++) {
            int positionéieren = Beräich_Tabell_positionéieren + INDEX * Beräich_Agab_d_Gréisst_veränneren;
            int 종류 = analyséieren_Ganzzuel(Daten, positionéieren + 4);
            int kennzeechnen_VALUE = analyséieren_Ganzzuel(Daten, positionéieren + 8);
            int Adress = analyséieren_Ganzzuel(Daten, positionéieren + 12);
            int Fichier_positionéieren = analyséieren_Ganzzuel(Daten, positionéieren + 16);
            int d_Gréisst_veränneren = analyséieren_Ganzzuel(Daten, positionéieren + 20);
            if (d_Gréisst_veränneren < 0 || (종류 != 8 && ((long) Fichier_positionéieren + d_Gréisst_veränneren > Daten.length || Fichier_positionéieren < 0))) {
                throw new IllegalArgumentException("ELF Beräich_VALUE Daten 범위가 올바르지 않습니다.");
            }
            구역들.add(new Beräich_VALUE(종류, kennzeechnen_VALUE, Adress, Fichier_positionéieren, d_Gréisst_veränneren));
        }
        return new Bild(Start_Adress, 구역들);
    }

    private int analyséieren_Ganzzuel(byte[] Daten, int positionéieren) {
        if (positionéieren < 0 || positionéieren > Daten.length - 4) {
            throw new IllegalArgumentException("ELF Ganzzuel 범위를 벗어났습니다.");
        }
        return (Daten[positionéieren] & 0xff)
                | ((Daten[positionéieren + 1] & 0xff) << 8)
                | ((Daten[positionéieren + 2] & 0xff) << 16)
                | ((Daten[positionéieren + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] Daten, int positionéieren) {
        if (positionéieren < 0 || positionéieren > Daten.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 Ganzzuel 범위를 벗어났습니다.");
        }
        return (Daten[positionéieren] & 0xff) | ((Daten[positionéieren + 1] & 0xff) << 8);
    }
}
