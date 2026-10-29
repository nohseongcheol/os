// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.a_yatawaajiraaya_anaajaalaairua;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian 실행 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class alüjalee_ajutuu {
        private final int 종류;
        private final int panteera_ajutuu;
        private final int ejepüsee;
        private final int 파일위치;
        private final int 크기;

        alüjalee_ajutuu(int 종류, int panteera_ajutuu, int ejepüsee, int 파일위치, int 크기) {
            this.종류 = 종류;
            this.panteera_ajutuu = panteera_ajutuu;
            this.ejepüsee = ejepüsee;
            this.파일위치 = 파일위치;
            this.크기 = 크기;
        }

        public int 종류() {
            return 종류;
        }

        public int panteera_ajutuu() {
            return panteera_ajutuu;
        }

        public int ejepüsee() {
            return ejepüsee;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int 크기() {
            return 크기;
        }
    }

    public static final class ayaakuaa {
        private final int achuwalaa_ejepüsee;
        private final List<alüjalee_ajutuu> 구역들;

        ayaakuaa(int achuwalaa_ejepüsee, List<alüjalee_ajutuu> 구역들) {
            this.achuwalaa_ejepüsee = achuwalaa_ejepüsee;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int achuwalaa_ejepüsee() {
            return achuwalaa_ejepüsee;
        }

        public List<alüjalee_ajutuu> 구역들() {
            return 구역들;
        }
    }

    public ayaakuaa 검사(byte[] atijaaya) {
        if (atijaaya == null || atijaaya.length < 52
                || atijaaya[0] != 0x7f || atijaaya[1] != 'E' || atijaaya[2] != 'L' || atijaaya[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (atijaaya[4] != 1 || atijaaya[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int achuwalaa_ejepüsee = akatajaa_waneepiasü(atijaaya, 24);
        int 구역표위치 = akatajaa_waneepiasü(atijaaya, 32);
        int 구역항목크기 = 짧은정수읽기(atijaaya, 46);
        int 구역수 = 짧은정수읽기(atijaaya, 48);
        if (구역항목크기 < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) 구역항목크기 * 구역수 > atijaaya.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<alüjalee_ajutuu> 구역들 = new ArrayList<alüjalee_ajutuu>();
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 구역수; ee_iyatialujuna++) {
            int 위치 = 구역표위치 + ee_iyatialujuna * 구역항목크기;
            int 종류 = akatajaa_waneepiasü(atijaaya, 위치 + 4);
            int panteera_ajutuu = akatajaa_waneepiasü(atijaaya, 위치 + 8);
            int ejepüsee = akatajaa_waneepiasü(atijaaya, 위치 + 12);
            int 파일위치 = akatajaa_waneepiasü(atijaaya, 위치 + 16);
            int 크기 = akatajaa_waneepiasü(atijaaya, 위치 + 20);
            if (크기 < 0 || (종류 != 8 && ((long) 파일위치 + 크기 > atijaaya.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF alüjalee_ajutuu atijaaya 범위가 올바르지 않습니다.");
            }
            구역들.add(new alüjalee_ajutuu(종류, panteera_ajutuu, ejepüsee, 파일위치, 크기));
        }
        return new ayaakuaa(achuwalaa_ejepüsee, 구역들);
    }

    private int akatajaa_waneepiasü(byte[] atijaaya, int 위치) {
        if (위치 < 0 || 위치 > atijaaya.length - 4) {
            throw new IllegalArgumentException("ELF waneepiasü 범위를 벗어났습니다.");
        }
        return (atijaaya[위치] & 0xff)
                | ((atijaaya[위치 + 1] & 0xff) << 8)
                | ((atijaaya[위치 + 2] & 0xff) << 16)
                | ((atijaaya[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] atijaaya, int 위치) {
        if (위치 < 0 || 위치 > atijaaya.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 waneepiasü 범위를 벗어났습니다.");
        }
        return (atijaaya[위치] & 0xff) | ((atijaaya[위치 + 1] & 0xff) << 8);
    }
}
