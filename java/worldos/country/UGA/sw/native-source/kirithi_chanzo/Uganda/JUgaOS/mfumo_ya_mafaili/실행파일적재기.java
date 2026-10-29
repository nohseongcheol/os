// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Uganda.JUgaOS.mfumo_ya_mafaili;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian tekeleza_amri 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class sehemu_thamani {
        private final int 종류;
        private final int alama_thamani;
        private final int anwani;
        private final int 파일위치;
        private final int panga_ukubwa;

        sehemu_thamani(int 종류, int alama_thamani, int anwani, int 파일위치, int panga_ukubwa) {
            this.종류 = 종류;
            this.alama_thamani = alama_thamani;
            this.anwani = anwani;
            this.파일위치 = 파일위치;
            this.panga_ukubwa = panga_ukubwa;
        }

        public int 종류() {
            return 종류;
        }

        public int alama_thamani() {
            return alama_thamani;
        }

        public int anwani() {
            return anwani;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int panga_ukubwa() {
            return panga_ukubwa;
        }
    }

    public static final class picha {
        private final int Anza_anwani;
        private final List<sehemu_thamani> 구역들;

        picha(int Anza_anwani, List<sehemu_thamani> 구역들) {
            this.Anza_anwani = Anza_anwani;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Anza_anwani() {
            return Anza_anwani;
        }

        public List<sehemu_thamani> 구역들() {
            return 구역들;
        }
    }

    public picha 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Anza_anwani = changanua_namba_kamili(data, 24);
        int 구역표위치 = changanua_namba_kamili(data, 32);
        int sehemu_ingizo_panga_ukubwa = 짧은정수읽기(data, 46);
        int 구역수 = 짧은정수읽기(data, 48);
        if (sehemu_ingizo_panga_ukubwa < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) sehemu_ingizo_panga_ukubwa * 구역수 > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sehemu_thamani> 구역들 = new ArrayList<sehemu_thamani>();
        for (int kielezo = 0; kielezo < 구역수; kielezo++) {
            int 위치 = 구역표위치 + kielezo * sehemu_ingizo_panga_ukubwa;
            int 종류 = changanua_namba_kamili(data, 위치 + 4);
            int alama_thamani = changanua_namba_kamili(data, 위치 + 8);
            int anwani = changanua_namba_kamili(data, 위치 + 12);
            int 파일위치 = changanua_namba_kamili(data, 위치 + 16);
            int panga_ukubwa = changanua_namba_kamili(data, 위치 + 20);
            if (panga_ukubwa < 0 || (종류 != 8 && ((long) 파일위치 + panga_ukubwa > data.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF sehemu_thamani data 범위가 올바르지 않습니다.");
            }
            구역들.add(new sehemu_thamani(종류, alama_thamani, anwani, 파일위치, panga_ukubwa));
        }
        return new picha(Anza_anwani, 구역들);
    }

    private int changanua_namba_kamili(byte[] data, int 위치) {
        if (위치 < 0 || 위치 > data.length - 4) {
            throw new IllegalArgumentException("ELF namba_kamili 범위를 벗어났습니다.");
        }
        return (data[위치] & 0xff)
                | ((data[위치 + 1] & 0xff) << 8)
                | ((data[위치 + 2] & 0xff) << 16)
                | ((data[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int 위치) {
        if (위치 < 0 || 위치 > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 namba_kamili 범위를 벗어났습니다.");
        }
        return (data[위치] & 0xff) | ((data[위치 + 1] & 0xff) << 8);
    }
}
