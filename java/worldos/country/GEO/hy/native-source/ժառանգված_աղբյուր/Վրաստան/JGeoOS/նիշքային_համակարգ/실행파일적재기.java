// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Վրաստան.JGeoOS.նիշքային_համակարգ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian կատարել_հրաման 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class խումբ_արժեք_366e0bfa {
        private final int 종류;
        private final int դրոշ_արժեք;
        private final int հասցե;
        private final int նիշք_դիրք;
        private final int Չափս;

        խումբ_արժեք_366e0bfa(int 종류, int դրոշ_արժեք, int հասցե, int նիշք_դիրք, int Չափս) {
            this.종류 = 종류;
            this.դրոշ_արժեք = դրոշ_արժեք;
            this.հասցե = հասցե;
            this.նիշք_դիրք = նիշք_դիրք;
            this.Չափս = Չափս;
        }

        public int 종류() {
            return 종류;
        }

        public int դրոշ_արժեք() {
            return դրոշ_արժեք;
        }

        public int հասցե() {
            return հասցե;
        }

        public int նիշք_դիրք() {
            return նիշք_դիրք;
        }

        public int Չափս() {
            return Չափս;
        }
    }

    public static final class նկար {
        private final int Մեկնարկ_հասցե;
        private final List<խումբ_արժեք_366e0bfa> 구역들;

        նկար(int Մեկնարկ_հասցե, List<խումբ_արժեք_366e0bfa> 구역들) {
            this.Մեկնարկ_հասցե = Մեկնարկ_հասցե;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Մեկնարկ_հասցե() {
            return Մեկնարկ_հասցե;
        }

        public List<խումբ_արժեք_366e0bfa> 구역들() {
            return 구역들;
        }
    }

    public նկար 검사(byte[] տվյալ) {
        if (տվյալ == null || տվյալ.length < 52
                || տվյալ[0] != 0x7f || տվյալ[1] != 'E' || տվյալ[2] != 'L' || տվյալ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (տվյալ[4] != 1 || տվյալ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Մեկնարկ_հասցե = վերլուծել_ամբողջ_թիվ(տվյալ, 24);
        int խումբ_աղյուսակ_դիրք = վերլուծել_ամբողջ_թիվ(տվյալ, 32);
        int խումբ_մուտքագրում_չափափոխել = 짧은정수읽기(տվյալ, 46);
        int 구역수 = 짧은정수읽기(տվյալ, 48);
        if (խումբ_մուտքագրում_չափափոխել < 40 || խումբ_աղյուսակ_դիրք < 0
                || (long) խումբ_աղյուսակ_դիրք + (long) խումբ_մուտքագրում_չափափոխել * 구역수 > տվյալ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<խումբ_արժեք_366e0bfa> 구역들 = new ArrayList<խումբ_արժեք_366e0bfa>();
        for (int դասիչ = 0; դասիչ < 구역수; դասիչ++) {
            int Դիրք = խումբ_աղյուսակ_դիրք + դասիչ * խումբ_մուտքագրում_չափափոխել;
            int 종류 = վերլուծել_ամբողջ_թիվ(տվյալ, Դիրք + 4);
            int դրոշ_արժեք = վերլուծել_ամբողջ_թիվ(տվյալ, Դիրք + 8);
            int հասցե = վերլուծել_ամբողջ_թիվ(տվյալ, Դիրք + 12);
            int նիշք_դիրք = վերլուծել_ամբողջ_թիվ(տվյալ, Դիրք + 16);
            int Չափս = վերլուծել_ամբողջ_թիվ(տվյալ, Դիրք + 20);
            if (Չափս < 0 || (종류 != 8 && ((long) նիշք_դիրք + Չափս > տվյալ.length || նիշք_դիրք < 0))) {
                throw new IllegalArgumentException("ELF խումբ_արժեք_366e0bfa տվյալ 범위가 올바르지 않습니다.");
            }
            구역들.add(new խումբ_արժեք_366e0bfa(종류, դրոշ_արժեք, հասցե, նիշք_դիրք, Չափս));
        }
        return new նկար(Մեկնարկ_հասցե, 구역들);
    }

    private int վերլուծել_ամբողջ_թիվ(byte[] տվյալ, int Դիրք) {
        if (Դիրք < 0 || Դիրք > տվյալ.length - 4) {
            throw new IllegalArgumentException("ELF ամբողջ_թիվ 범위를 벗어났습니다.");
        }
        return (տվյալ[Դիրք] & 0xff)
                | ((տվյալ[Դիրք + 1] & 0xff) << 8)
                | ((տվյալ[Դիրք + 2] & 0xff) << 16)
                | ((տվյալ[Դիրք + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] տվյալ, int Դիրք) {
        if (Դիրք < 0 || Դիրք > տվյալ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ամբողջ_թիվ 범위를 벗어났습니다.");
        }
        return (տվյալ[Դիրք] & 0xff) | ((տվյալ[Դիրք + 1] & 0xff) << 8);
    }
}
