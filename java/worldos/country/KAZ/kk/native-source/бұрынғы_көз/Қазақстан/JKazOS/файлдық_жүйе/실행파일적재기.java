// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.файлдық_жүйе;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian орындау_пәрмен 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class бөлім_мән_366e0bfa {
        private final int 종류;
        private final int жалауша_мән;
        private final int мекенжай;
        private final int файл_лауазым;
        private final int Өлшемі;

        бөлім_мән_366e0bfa(int 종류, int жалауша_мән, int мекенжай, int файл_лауазым, int Өлшемі) {
            this.종류 = 종류;
            this.жалауша_мән = жалауша_мән;
            this.мекенжай = мекенжай;
            this.файл_лауазым = файл_лауазым;
            this.Өлшемі = Өлшемі;
        }

        public int 종류() {
            return 종류;
        }

        public int жалауша_мән() {
            return жалауша_мән;
        }

        public int мекенжай() {
            return мекенжай;
        }

        public int файл_лауазым() {
            return файл_лауазым;
        }

        public int Өлшемі() {
            return Өлшемі;
        }
    }

    public static final class сурет {
        private final int басы_мекенжай;
        private final List<бөлім_мән_366e0bfa> 구역들;

        сурет(int басы_мекенжай, List<бөлім_мән_366e0bfa> 구역들) {
            this.басы_мекенжай = басы_мекенжай;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int басы_мекенжай() {
            return басы_мекенжай;
        }

        public List<бөлім_мән_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public сурет 검사(byte[] деректер) {
        if (деректер == null || деректер.length < 52
                || деректер[0] != 0x7f || деректер[1] != 'E' || деректер[2] != 'L' || деректер[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (деректер[4] != 1 || деректер[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int басы_мекенжай = талдау_бүтін_сан(деректер, 24);
        int бөлім_кесте_лауазым = талдау_бүтін_сан(деректер, 32);
        int бөлім_енгізу_өлшемді_өзгерту = 짧은정수읽기(деректер, 46);
        int 구역수 = 짧은정수읽기(деректер, 48);
        if (бөлім_енгізу_өлшемді_өзгерту < 40 || бөлім_кесте_лауазым < 0
                || (long) бөлім_кесте_лауазым + (long) бөлім_енгізу_өлшемді_өзгерту * 구역수 > деректер.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<бөлім_мән_366e0bfa> 구역들 = new ArrayList<бөлім_мән_366e0bfa>();
        for (int индекс = 0; индекс < 구역수; индекс++) {
            int Орны = бөлім_кесте_лауазым + индекс * бөлім_енгізу_өлшемді_өзгерту;
            int 종류 = талдау_бүтін_сан(деректер, Орны + 4);
            int жалауша_мән = талдау_бүтін_сан(деректер, Орны + 8);
            int мекенжай = талдау_бүтін_сан(деректер, Орны + 12);
            int файл_лауазым = талдау_бүтін_сан(деректер, Орны + 16);
            int Өлшемі = талдау_бүтін_сан(деректер, Орны + 20);
            if (Өлшемі < 0 || (종류 != 8 && ((long) файл_лауазым + Өлшемі > деректер.length || файл_лауазым < 0))) {
                throw new IllegalArgumentException("ELF бөлім_мән_366e0bfa деректер 범위가 올바르지 않습니다.");
            }
            구역들.add(new бөлім_мән_366e0bfa(종류, жалауша_мән, мекенжай, файл_лауазым, Өлшемі));
        }
        return new сурет(басы_мекенжай, 구역들);
    }

    private int талдау_бүтін_сан(byte[] деректер, int Орны) {
        if (Орны < 0 || Орны > деректер.length - 4) {
            throw new IllegalArgumentException("ELF бүтін_сан 범위를 벗어났습니다.");
        }
        return (деректер[Орны] & 0xff)
                | ((деректер[Орны + 1] & 0xff) << 8)
                | ((деректер[Орны + 2] & 0xff) << 16)
                | ((деректер[Орны + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] деректер, int Орны) {
        if (Орны < 0 || Орны > деректер.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 бүтін_сан 범위를 벗어났습니다.");
        }
        return (деректер[Орны] & 0xff) | ((деректер[Орны + 1] & 0xff) << 8);
    }
}
