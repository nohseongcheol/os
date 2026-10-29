// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COD.JCodOS.sisitemu_ya_dosiye;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian gukora_ibwiriza 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class igice_agaciro {
        private final int 종류;
        private final int akabendera_agaciro;
        private final int aderesi;
        private final int 파일위치;
        private final int Ingano;

        igice_agaciro(int 종류, int akabendera_agaciro, int aderesi, int 파일위치, int Ingano) {
            this.종류 = 종류;
            this.akabendera_agaciro = akabendera_agaciro;
            this.aderesi = aderesi;
            this.파일위치 = 파일위치;
            this.Ingano = Ingano;
        }

        public int 종류() {
            return 종류;
        }

        public int akabendera_agaciro() {
            return akabendera_agaciro;
        }

        public int aderesi() {
            return aderesi;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Ingano() {
            return Ingano;
        }
    }

    public static final class ishusho {
        private final int Itangira_aderesi;
        private final List<igice_agaciro> 구역들;

        ishusho(int Itangira_aderesi, List<igice_agaciro> 구역들) {
            this.Itangira_aderesi = Itangira_aderesi;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Itangira_aderesi() {
            return Itangira_aderesi;
        }

        public List<igice_agaciro> 구역들() {
            return 구역들;
        }
    }

    public ishusho 검사(byte[] amakurushingiro) {
        if (amakurushingiro == null || amakurushingiro.length < 52
                || amakurushingiro[0] != 0x7f || amakurushingiro[1] != 'E' || amakurushingiro[2] != 'L' || amakurushingiro[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (amakurushingiro[4] != 1 || amakurushingiro[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Itangira_aderesi = gusesengura_umubare_wuzuye(amakurushingiro, 24);
        int 구역표위치 = gusesengura_umubare_wuzuye(amakurushingiro, 32);
        int igice_icyinjizwa_ingano = 짧은정수읽기(amakurushingiro, 46);
        int 구역수 = 짧은정수읽기(amakurushingiro, 48);
        if (igice_icyinjizwa_ingano < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) igice_icyinjizwa_ingano * 구역수 > amakurushingiro.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<igice_agaciro> 구역들 = new ArrayList<igice_agaciro>();
        for (int umugerekashakiro = 0; umugerekashakiro < 구역수; umugerekashakiro++) {
            int 위치 = 구역표위치 + umugerekashakiro * igice_icyinjizwa_ingano;
            int 종류 = gusesengura_umubare_wuzuye(amakurushingiro, 위치 + 4);
            int akabendera_agaciro = gusesengura_umubare_wuzuye(amakurushingiro, 위치 + 8);
            int aderesi = gusesengura_umubare_wuzuye(amakurushingiro, 위치 + 12);
            int 파일위치 = gusesengura_umubare_wuzuye(amakurushingiro, 위치 + 16);
            int Ingano = gusesengura_umubare_wuzuye(amakurushingiro, 위치 + 20);
            if (Ingano < 0 || (종류 != 8 && ((long) 파일위치 + Ingano > amakurushingiro.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF igice_agaciro amakurushingiro 범위가 올바르지 않습니다.");
            }
            구역들.add(new igice_agaciro(종류, akabendera_agaciro, aderesi, 파일위치, Ingano));
        }
        return new ishusho(Itangira_aderesi, 구역들);
    }

    private int gusesengura_umubare_wuzuye(byte[] amakurushingiro, int 위치) {
        if (위치 < 0 || 위치 > amakurushingiro.length - 4) {
            throw new IllegalArgumentException("ELF umubare_wuzuye 범위를 벗어났습니다.");
        }
        return (amakurushingiro[위치] & 0xff)
                | ((amakurushingiro[위치 + 1] & 0xff) << 8)
                | ((amakurushingiro[위치 + 2] & 0xff) << 16)
                | ((amakurushingiro[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] amakurushingiro, int 위치) {
        if (위치 < 0 || 위치 > amakurushingiro.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 umubare_wuzuye 범위를 벗어났습니다.");
        }
        return (amakurushingiro[위치] & 0xff) | ((amakurushingiro[위치 + 1] & 0xff) << 8);
    }
}
