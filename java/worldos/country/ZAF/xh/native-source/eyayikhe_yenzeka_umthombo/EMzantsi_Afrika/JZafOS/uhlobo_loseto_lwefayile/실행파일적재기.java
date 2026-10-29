// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.uhlobo_loseto_lwefayile;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ukwenza_umyalelo 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class icandelo_ixabiso {
        private final int 종류;
        private final int iflegi_ixabiso;
        private final int idilesi;
        private final int 파일위치;
        private final int Ubukhulu;

        icandelo_ixabiso(int 종류, int iflegi_ixabiso, int idilesi, int 파일위치, int Ubukhulu) {
            this.종류 = 종류;
            this.iflegi_ixabiso = iflegi_ixabiso;
            this.idilesi = idilesi;
            this.파일위치 = 파일위치;
            this.Ubukhulu = Ubukhulu;
        }

        public int 종류() {
            return 종류;
        }

        public int iflegi_ixabiso() {
            return iflegi_ixabiso;
        }

        public int idilesi() {
            return idilesi;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Ubukhulu() {
            return Ubukhulu;
        }
    }

    public static final class umfanekiso {
        private final int qala_idilesi;
        private final List<icandelo_ixabiso> 구역들;

        umfanekiso(int qala_idilesi, List<icandelo_ixabiso> 구역들) {
            this.qala_idilesi = qala_idilesi;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int qala_idilesi() {
            return qala_idilesi;
        }

        public List<icandelo_ixabiso> 구역들() {
            return 구역들;
        }
    }

    public umfanekiso 검사(byte[] iingcombolo) {
        if (iingcombolo == null || iingcombolo.length < 52
                || iingcombolo[0] != 0x7f || iingcombolo[1] != 'E' || iingcombolo[2] != 'L' || iingcombolo[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (iingcombolo[4] != 1 || iingcombolo[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int qala_idilesi = ingcaciso_yegama_inani_elipheleleyo(iingcombolo, 24);
        int 구역표위치 = ingcaciso_yegama_inani_elipheleleyo(iingcombolo, 32);
        int icandelo_ufako_nkcukacha_isayizi = 짧은정수읽기(iingcombolo, 46);
        int 구역수 = 짧은정수읽기(iingcombolo, 48);
        if (icandelo_ufako_nkcukacha_isayizi < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) icandelo_ufako_nkcukacha_isayizi * 구역수 > iingcombolo.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<icandelo_ixabiso> 구역들 = new ArrayList<icandelo_ixabiso>();
        for (int indeksa = 0; indeksa < 구역수; indeksa++) {
            int 위치 = 구역표위치 + indeksa * icandelo_ufako_nkcukacha_isayizi;
            int 종류 = ingcaciso_yegama_inani_elipheleleyo(iingcombolo, 위치 + 4);
            int iflegi_ixabiso = ingcaciso_yegama_inani_elipheleleyo(iingcombolo, 위치 + 8);
            int idilesi = ingcaciso_yegama_inani_elipheleleyo(iingcombolo, 위치 + 12);
            int 파일위치 = ingcaciso_yegama_inani_elipheleleyo(iingcombolo, 위치 + 16);
            int Ubukhulu = ingcaciso_yegama_inani_elipheleleyo(iingcombolo, 위치 + 20);
            if (Ubukhulu < 0 || (종류 != 8 && ((long) 파일위치 + Ubukhulu > iingcombolo.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF icandelo_ixabiso iingcombolo 범위가 올바르지 않습니다.");
            }
            구역들.add(new icandelo_ixabiso(종류, iflegi_ixabiso, idilesi, 파일위치, Ubukhulu));
        }
        return new umfanekiso(qala_idilesi, 구역들);
    }

    private int ingcaciso_yegama_inani_elipheleleyo(byte[] iingcombolo, int 위치) {
        if (위치 < 0 || 위치 > iingcombolo.length - 4) {
            throw new IllegalArgumentException("ELF inani_elipheleleyo 범위를 벗어났습니다.");
        }
        return (iingcombolo[위치] & 0xff)
                | ((iingcombolo[위치 + 1] & 0xff) << 8)
                | ((iingcombolo[위치 + 2] & 0xff) << 16)
                | ((iingcombolo[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] iingcombolo, int 위치) {
        if (위치 < 0 || 위치 > iingcombolo.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 inani_elipheleleyo 범위를 벗어났습니다.");
        }
        return (iingcombolo[위치] & 0xff) | ((iingcombolo[위치 + 1] & 0xff) << 8);
    }
}
