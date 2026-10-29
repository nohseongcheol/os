// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package UGA.JUgaOS.sisitemu_ya_dosiye;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Idosiye 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sisitemu_ya_dosiye.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sisitemu_ya_dosiye.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sisitemu_ya_dosiye sisitemu_ya_dosiye;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sisitemu_ya_dosiye sisitemu_ya_dosiye) {
        this.sisitemu_ya_dosiye = sisitemu_ya_dosiye;
    }

    public int Gufungura(String Izina) {
        sisitemu_ya_dosiye.열린파일 열린파일 = sisitemu_ya_dosiye.Gufungura(Izina);
        if (열린파일 == null) {
            return -2;
        }
        int umugerekashakiro = irimo_ubusa_umugerekashakiro(3);
        if (umugerekashakiro < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(umugerekashakiro), new 서술자(열린파일));
        return umugerekashakiro;
    }

    public int 읽기(int umugerekashakiro, byte[] 받을곳, int Ingano) {
        서술자 icyinjizwa_agaciro = 서술자들.get(Integer.valueOf(umugerekashakiro));
        if (icyinjizwa_agaciro == null) {
            return -9;
        }
        if (Ingano < 0 || Ingano > 받을곳.length) {
            return -22;
        }
        int 남음 = icyinjizwa_agaciro.열린파일.amakurushingiro.length - icyinjizwa_agaciro.열린파일.위치;
        int 읽을크기 = Math.min(Ingano, Math.max(남음, 0));
        System.arraycopy(icyinjizwa_agaciro.열린파일.amakurushingiro, icyinjizwa_agaciro.열린파일.위치, 받을곳, 0, 읽을크기);
        icyinjizwa_agaciro.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int umugerekashakiro, int 거리, int 기준) {
        서술자 icyinjizwa_agaciro = 서술자들.get(Integer.valueOf(umugerekashakiro));
        if (icyinjizwa_agaciro == null) {
            return -9;
        }
        int Imbuganyuma_agaciro;
        if (기준 == 0) {
            Imbuganyuma_agaciro = 0;
        } else if (기준 == 1) {
            Imbuganyuma_agaciro = icyinjizwa_agaciro.열린파일.위치;
        } else if (기준 == 2) {
            Imbuganyuma_agaciro = icyinjizwa_agaciro.열린파일.amakurushingiro.length;
        } else {
            return -22;
        }
        int 새위치 = Imbuganyuma_agaciro + 거리;
        if (새위치 < 0) {
            return -22;
        }
        icyinjizwa_agaciro.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int Gufunga(int umugerekashakiro) {
        서술자 icyinjizwa_agaciro = 서술자들.remove(Integer.valueOf(umugerekashakiro));
        if (icyinjizwa_agaciro == null) {
            return -9;
        }
        icyinjizwa_agaciro.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int umugerekashakiro, int 최소번호) {
        서술자 icyinjizwa_agaciro = 서술자들.get(Integer.valueOf(umugerekashakiro));
        if (icyinjizwa_agaciro == null) {
            return -9;
        }
        int 새번호 = irimo_ubusa_umugerekashakiro(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        icyinjizwa_agaciro.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(icyinjizwa_agaciro.열린파일));
        return 새번호;
    }

    public int 지정복제(int umugerekashakiro, int 새번호) {
        if (umugerekashakiro == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(umugerekashakiro)) ? umugerekashakiro : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(umugerekashakiro));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Gufunga(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int umugerekashakiro, boolean agaciro) {
        서술자 icyinjizwa_agaciro = 서술자들.get(Integer.valueOf(umugerekashakiro));
        if (icyinjizwa_agaciro == null) {
            return -9;
        }
        icyinjizwa_agaciro.실행시닫기 = agaciro;
        return 0;
    }

    public int 실행시닫기값(int umugerekashakiro) {
        서술자 icyinjizwa_agaciro = 서술자들.get(Integer.valueOf(umugerekashakiro));
        if (icyinjizwa_agaciro == null) {
            return -9;
        }
        return icyinjizwa_agaciro.실행시닫기 ? 1 : 0;
    }

    public dosiye_amakuru msinfo32_exe(int umugerekashakiro) {
        if (umugerekashakiro >= 0 && umugerekashakiro <= 2) {
            return new dosiye_amakuru(0, 0020666);
        }
        서술자 icyinjizwa_agaciro = 서술자들.get(Integer.valueOf(umugerekashakiro));
        if (icyinjizwa_agaciro == null) {
            return null;
        }
        return new dosiye_amakuru(icyinjizwa_agaciro.열린파일.amakurushingiro.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer umugerekashakiro : 번호들) {
            서술자 icyinjizwa_agaciro = 서술자들.get(umugerekashakiro);
            if (icyinjizwa_agaciro != null && icyinjizwa_agaciro.실행시닫기) {
                Gufunga(umugerekashakiro.intValue());
            }
        }
    }

    public boolean 열려있음(int umugerekashakiro) {
        return 서술자들.containsKey(Integer.valueOf(umugerekashakiro));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(sisitemu_ya_dosiye);
        for (Map.Entry<Integer, 서술자> icyinjizwa_agaciro : 서술자들.entrySet()) {
            icyinjizwa_agaciro.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(icyinjizwa_agaciro.getValue().열린파일);
            새서술자.실행시닫기 = icyinjizwa_agaciro.getValue().실행시닫기;
            결과.서술자들.put(icyinjizwa_agaciro.getKey(), 새서술자);
        }
        return 결과;
    }

    private int irimo_ubusa_umugerekashakiro(int 최소번호) {
        for (int umugerekashakiro = Math.max(0, 최소번호); umugerekashakiro < 최대서술자; umugerekashakiro++) {
            if (!서술자들.containsKey(Integer.valueOf(umugerekashakiro))) {
                return umugerekashakiro;
            }
        }
        return -1;
    }
}
