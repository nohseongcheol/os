// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ELesotho.JLsoOS.uhlobo_loseto_lwefayile;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 iFayili 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final uhlobo_loseto_lwefayile.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(uhlobo_loseto_lwefayile.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final uhlobo_loseto_lwefayile uhlobo_loseto_lwefayile;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(uhlobo_loseto_lwefayile uhlobo_loseto_lwefayile) {
        this.uhlobo_loseto_lwefayile = uhlobo_loseto_lwefayile;
    }

    public int Vula(String Igama) {
        uhlobo_loseto_lwefayile.열린파일 열린파일 = uhlobo_loseto_lwefayile.Vula(Igama);
        if (열린파일 == null) {
            return -2;
        }
        int indeksa = engenanto_indeksa(3);
        if (indeksa < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(indeksa), new 서술자(열린파일));
        return indeksa;
    }

    public int Funda(int indeksa, byte[] 받을곳, int Ubukhulu) {
        서술자 ufako_nkcukacha_ixabiso = 서술자들.get(Integer.valueOf(indeksa));
        if (ufako_nkcukacha_ixabiso == null) {
            return -9;
        }
        if (Ubukhulu < 0 || Ubukhulu > 받을곳.length) {
            return -22;
        }
        int 남음 = ufako_nkcukacha_ixabiso.열린파일.iingcombolo.length - ufako_nkcukacha_ixabiso.열린파일.위치;
        int 읽을크기 = Math.min(Ubukhulu, Math.max(남음, 0));
        System.arraycopy(ufako_nkcukacha_ixabiso.열린파일.iingcombolo, ufako_nkcukacha_ixabiso.열린파일.위치, 받을곳, 0, 읽을크기);
        ufako_nkcukacha_ixabiso.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int indeksa, int 거리, int 기준) {
        서술자 ufako_nkcukacha_ixabiso = 서술자들.get(Integer.valueOf(indeksa));
        if (ufako_nkcukacha_ixabiso == null) {
            return -9;
        }
        int Ngasemva_ixabiso;
        if (기준 == 0) {
            Ngasemva_ixabiso = 0;
        } else if (기준 == 1) {
            Ngasemva_ixabiso = ufako_nkcukacha_ixabiso.열린파일.위치;
        } else if (기준 == 2) {
            Ngasemva_ixabiso = ufako_nkcukacha_ixabiso.열린파일.iingcombolo.length;
        } else {
            return -22;
        }
        int 새위치 = Ngasemva_ixabiso + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ufako_nkcukacha_ixabiso.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int Vala(int indeksa) {
        서술자 ufako_nkcukacha_ixabiso = 서술자들.remove(Integer.valueOf(indeksa));
        if (ufako_nkcukacha_ixabiso == null) {
            return -9;
        }
        ufako_nkcukacha_ixabiso.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int indeksa, int 최소번호) {
        서술자 ufako_nkcukacha_ixabiso = 서술자들.get(Integer.valueOf(indeksa));
        if (ufako_nkcukacha_ixabiso == null) {
            return -9;
        }
        int 새번호 = engenanto_indeksa(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ufako_nkcukacha_ixabiso.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ufako_nkcukacha_ixabiso.열린파일));
        return 새번호;
    }

    public int 지정복제(int indeksa, int 새번호) {
        if (indeksa == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(indeksa)) ? indeksa : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(indeksa));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Vala(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int indeksa, boolean ixabiso) {
        서술자 ufako_nkcukacha_ixabiso = 서술자들.get(Integer.valueOf(indeksa));
        if (ufako_nkcukacha_ixabiso == null) {
            return -9;
        }
        ufako_nkcukacha_ixabiso.실행시닫기 = ixabiso;
        return 0;
    }

    public int 실행시닫기값(int indeksa) {
        서술자 ufako_nkcukacha_ixabiso = 서술자들.get(Integer.valueOf(indeksa));
        if (ufako_nkcukacha_ixabiso == null) {
            return -9;
        }
        return ufako_nkcukacha_ixabiso.실행시닫기 ? 1 : 0;
    }

    public ifayile_ingcaciso i_msinfo32_exe(int indeksa) {
        if (indeksa >= 0 && indeksa <= 2) {
            return new ifayile_ingcaciso(0, 0020666);
        }
        서술자 ufako_nkcukacha_ixabiso = 서술자들.get(Integer.valueOf(indeksa));
        if (ufako_nkcukacha_ixabiso == null) {
            return null;
        }
        return new ifayile_ingcaciso(ufako_nkcukacha_ixabiso.열린파일.iingcombolo.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer indeksa : 번호들) {
            서술자 ufako_nkcukacha_ixabiso = 서술자들.get(indeksa);
            if (ufako_nkcukacha_ixabiso != null && ufako_nkcukacha_ixabiso.실행시닫기) {
                Vala(indeksa.intValue());
            }
        }
    }

    public boolean 열려있음(int indeksa) {
        return 서술자들.containsKey(Integer.valueOf(indeksa));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(uhlobo_loseto_lwefayile);
        for (Map.Entry<Integer, 서술자> ufako_nkcukacha_ixabiso : 서술자들.entrySet()) {
            ufako_nkcukacha_ixabiso.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ufako_nkcukacha_ixabiso.getValue().열린파일);
            새서술자.실행시닫기 = ufako_nkcukacha_ixabiso.getValue().실행시닫기;
            결과.서술자들.put(ufako_nkcukacha_ixabiso.getKey(), 새서술자);
        }
        return 결과;
    }

    private int engenanto_indeksa(int 최소번호) {
        for (int indeksa = Math.max(0, 최소번호); indeksa < 최대서술자; indeksa++) {
            if (!서술자들.containsKey(Integer.valueOf(indeksa))) {
                return indeksa;
            }
        }
        return -1;
    }
}
