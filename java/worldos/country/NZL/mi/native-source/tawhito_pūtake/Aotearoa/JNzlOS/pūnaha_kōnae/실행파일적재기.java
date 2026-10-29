// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.pūnaha_kōnae;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian kawe_tono 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class wāhanga_uara {
        private final int 종류;
        private final int kara_uara;
        private final int ADDRESS;
        private final int kōnae_tūranga;
        private final int rahi;

        wāhanga_uara(int 종류, int kara_uara, int ADDRESS, int kōnae_tūranga, int rahi) {
            this.종류 = 종류;
            this.kara_uara = kara_uara;
            this.ADDRESS = ADDRESS;
            this.kōnae_tūranga = kōnae_tūranga;
            this.rahi = rahi;
        }

        public int 종류() {
            return 종류;
        }

        public int kara_uara() {
            return kara_uara;
        }

        public int ADDRESS() {
            return ADDRESS;
        }

        public int kōnae_tūranga() {
            return kōnae_tūranga;
        }

        public int rahi() {
            return rahi;
        }
    }

    public static final class IMAGE {
        private final int Start_ADDRESS;
        private final List<wāhanga_uara> 구역들;

        IMAGE(int Start_ADDRESS, List<wāhanga_uara> 구역들) {
            this.Start_ADDRESS = Start_ADDRESS;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_ADDRESS() {
            return Start_ADDRESS;
        }

        public List<wāhanga_uara> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] raraunga) {
        if (raraunga == null || raraunga.length < 52
                || raraunga[0] != 0x7f || raraunga[1] != 'E' || raraunga[2] != 'L' || raraunga[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (raraunga[4] != 1 || raraunga[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_ADDRESS = poroporo_tau_tōpū(raraunga, 24);
        int wāhanga_ripanga_tūranga = poroporo_tau_tōpū(raraunga, 32);
        int wāhanga_tāurunga_rahi = 짧은정수읽기(raraunga, 46);
        int wāhanga_COUNT = 짧은정수읽기(raraunga, 48);
        if (wāhanga_tāurunga_rahi < 40 || wāhanga_ripanga_tūranga < 0
                || (long) wāhanga_ripanga_tūranga + (long) wāhanga_tāurunga_rahi * wāhanga_COUNT > raraunga.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<wāhanga_uara> 구역들 = new ArrayList<wāhanga_uara>();
        for (int INDEX = 0; INDEX < wāhanga_COUNT; INDEX++) {
            int tūranga = wāhanga_ripanga_tūranga + INDEX * wāhanga_tāurunga_rahi;
            int 종류 = poroporo_tau_tōpū(raraunga, tūranga + 4);
            int kara_uara = poroporo_tau_tōpū(raraunga, tūranga + 8);
            int ADDRESS = poroporo_tau_tōpū(raraunga, tūranga + 12);
            int kōnae_tūranga = poroporo_tau_tōpū(raraunga, tūranga + 16);
            int rahi = poroporo_tau_tōpū(raraunga, tūranga + 20);
            if (rahi < 0 || (종류 != 8 && ((long) kōnae_tūranga + rahi > raraunga.length || kōnae_tūranga < 0))) {
                throw new IllegalArgumentException("ELF wāhanga_uara raraunga 범위가 올바르지 않습니다.");
            }
            구역들.add(new wāhanga_uara(종류, kara_uara, ADDRESS, kōnae_tūranga, rahi));
        }
        return new IMAGE(Start_ADDRESS, 구역들);
    }

    private int poroporo_tau_tōpū(byte[] raraunga, int tūranga) {
        if (tūranga < 0 || tūranga > raraunga.length - 4) {
            throw new IllegalArgumentException("ELF tau_tōpū 범위를 벗어났습니다.");
        }
        return (raraunga[tūranga] & 0xff)
                | ((raraunga[tūranga + 1] & 0xff) << 8)
                | ((raraunga[tūranga + 2] & 0xff) << 16)
                | ((raraunga[tūranga + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] raraunga, int tūranga) {
        if (tūranga < 0 || tūranga > raraunga.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 tau_tōpū 범위를 벗어났습니다.");
        }
        return (raraunga[tūranga] & 0xff) | ((raraunga[tūranga + 1] & 0xff) << 8);
    }
}
