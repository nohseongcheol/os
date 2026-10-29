// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.tshepedišo_ya_difaele;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian phethagatša_taelo 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class karolo_boleng {
        private final int 종류;
        private final int folaga_boleng;
        private final int atrese;
        private final int 파일위치;
        private final int Bogolo;

        karolo_boleng(int 종류, int folaga_boleng, int atrese, int 파일위치, int Bogolo) {
            this.종류 = 종류;
            this.folaga_boleng = folaga_boleng;
            this.atrese = atrese;
            this.파일위치 = 파일위치;
            this.Bogolo = Bogolo;
        }

        public int 종류() {
            return 종류;
        }

        public int folaga_boleng() {
            return folaga_boleng;
        }

        public int atrese() {
            return atrese;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Bogolo() {
            return Bogolo;
        }
    }

    public static final class seswantšho {
        private final int Thomišo_atrese;
        private final List<karolo_boleng> 구역들;

        seswantšho(int Thomišo_atrese, List<karolo_boleng> 구역들) {
            this.Thomišo_atrese = Thomišo_atrese;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Thomišo_atrese() {
            return Thomišo_atrese;
        }

        public List<karolo_boleng> 구역들() {
            return 구역들;
        }
    }

    public seswantšho 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Thomišo_atrese = ripaganya_palotlalo(data, 24);
        int 구역표위치 = ripaganya_palotlalo(data, 32);
        int karolo_go_tsenya_tshedimošo_bogolo = 짧은정수읽기(data, 46);
        int 구역수 = 짧은정수읽기(data, 48);
        if (karolo_go_tsenya_tshedimošo_bogolo < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) karolo_go_tsenya_tshedimošo_bogolo * 구역수 > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<karolo_boleng> 구역들 = new ArrayList<karolo_boleng>();
        for (int lokela = 0; lokela < 구역수; lokela++) {
            int 위치 = 구역표위치 + lokela * karolo_go_tsenya_tshedimošo_bogolo;
            int 종류 = ripaganya_palotlalo(data, 위치 + 4);
            int folaga_boleng = ripaganya_palotlalo(data, 위치 + 8);
            int atrese = ripaganya_palotlalo(data, 위치 + 12);
            int 파일위치 = ripaganya_palotlalo(data, 위치 + 16);
            int Bogolo = ripaganya_palotlalo(data, 위치 + 20);
            if (Bogolo < 0 || (종류 != 8 && ((long) 파일위치 + Bogolo > data.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF karolo_boleng data 범위가 올바르지 않습니다.");
            }
            구역들.add(new karolo_boleng(종류, folaga_boleng, atrese, 파일위치, Bogolo));
        }
        return new seswantšho(Thomišo_atrese, 구역들);
    }

    private int ripaganya_palotlalo(byte[] data, int 위치) {
        if (위치 < 0 || 위치 > data.length - 4) {
            throw new IllegalArgumentException("ELF palotlalo 범위를 벗어났습니다.");
        }
        return (data[위치] & 0xff)
                | ((data[위치 + 1] & 0xff) << 8)
                | ((data[위치 + 2] & 0xff) << 16)
                | ((data[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int 위치) {
        if (위치 < 0 || 위치 > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 palotlalo 범위를 벗어났습니다.");
        }
        return (data[위치] & 0xff) | ((data[위치 + 1] & 0xff) << 8);
    }
}
