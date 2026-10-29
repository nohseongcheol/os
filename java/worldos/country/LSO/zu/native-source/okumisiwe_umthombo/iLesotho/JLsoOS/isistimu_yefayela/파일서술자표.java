// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iLesotho.JLsoOS.isistimu_yefayela;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Ihele 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final isistimu_yefayela.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(isistimu_yefayela.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final isistimu_yefayela isistimu_yefayela;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(isistimu_yefayela isistimu_yefayela) {
        this.isistimu_yefayela = isistimu_yefayela;
    }

    public int Vula(String Igama) {
        isistimu_yefayela.열린파일 열린파일 = isistimu_yefayela.Vula(Igama);
        if (열린파일 == null) {
            return -2;
        }
        int thola_inkomba = okungasho_lutho_thola_inkomba(3);
        if (thola_inkomba < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(thola_inkomba), new 서술자(열린파일));
        return thola_inkomba;
    }

    public int Funda(int thola_inkomba, byte[] 받을곳, int Ubungako) {
        서술자 okufakwayo_inani = 서술자들.get(Integer.valueOf(thola_inkomba));
        if (okufakwayo_inani == null) {
            return -9;
        }
        if (Ubungako < 0 || Ubungako > 받을곳.length) {
            return -22;
        }
        int 남음 = okufakwayo_inani.열린파일.imininingwane.length - okufakwayo_inani.열린파일.위치;
        int 읽을크기 = Math.min(Ubungako, Math.max(남음, 0));
        System.arraycopy(okufakwayo_inani.열린파일.imininingwane, okufakwayo_inani.열린파일.위치, 받을곳, 0, 읽을크기);
        okufakwayo_inani.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int thola_inkomba, int 거리, int 기준) {
        서술자 okufakwayo_inani = 서술자들.get(Integer.valueOf(thola_inkomba));
        if (okufakwayo_inani == null) {
            return -9;
        }
        int ngemuva_inani;
        if (기준 == 0) {
            ngemuva_inani = 0;
        } else if (기준 == 1) {
            ngemuva_inani = okufakwayo_inani.열린파일.위치;
        } else if (기준 == 2) {
            ngemuva_inani = okufakwayo_inani.열린파일.imininingwane.length;
        } else {
            return -22;
        }
        int 새위치 = ngemuva_inani + 거리;
        if (새위치 < 0) {
            return -22;
        }
        okufakwayo_inani.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int Vala(int thola_inkomba) {
        서술자 okufakwayo_inani = 서술자들.remove(Integer.valueOf(thola_inkomba));
        if (okufakwayo_inani == null) {
            return -9;
        }
        okufakwayo_inani.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int thola_inkomba, int 최소번호) {
        서술자 okufakwayo_inani = 서술자들.get(Integer.valueOf(thola_inkomba));
        if (okufakwayo_inani == null) {
            return -9;
        }
        int 새번호 = okungasho_lutho_thola_inkomba(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        okufakwayo_inani.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(okufakwayo_inani.열린파일));
        return 새번호;
    }

    public int 지정복제(int thola_inkomba, int 새번호) {
        if (thola_inkomba == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(thola_inkomba)) ? thola_inkomba : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(thola_inkomba));
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

    public int 실행시닫기설정(int thola_inkomba, boolean inani) {
        서술자 okufakwayo_inani = 서술자들.get(Integer.valueOf(thola_inkomba));
        if (okufakwayo_inani == null) {
            return -9;
        }
        okufakwayo_inani.실행시닫기 = inani;
        return 0;
    }

    public int 실행시닫기값(int thola_inkomba) {
        서술자 okufakwayo_inani = 서술자들.get(Integer.valueOf(thola_inkomba));
        if (okufakwayo_inani == null) {
            return -9;
        }
        return okufakwayo_inani.실행시닫기 ? 1 : 0;
    }

    public ifayela_ulwazi I_msinfo32_exe(int thola_inkomba) {
        if (thola_inkomba >= 0 && thola_inkomba <= 2) {
            return new ifayela_ulwazi(0, 0020666);
        }
        서술자 okufakwayo_inani = 서술자들.get(Integer.valueOf(thola_inkomba));
        if (okufakwayo_inani == null) {
            return null;
        }
        return new ifayela_ulwazi(okufakwayo_inani.열린파일.imininingwane.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer thola_inkomba : 번호들) {
            서술자 okufakwayo_inani = 서술자들.get(thola_inkomba);
            if (okufakwayo_inani != null && okufakwayo_inani.실행시닫기) {
                Vala(thola_inkomba.intValue());
            }
        }
    }

    public boolean 열려있음(int thola_inkomba) {
        return 서술자들.containsKey(Integer.valueOf(thola_inkomba));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(isistimu_yefayela);
        for (Map.Entry<Integer, 서술자> okufakwayo_inani : 서술자들.entrySet()) {
            okufakwayo_inani.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(okufakwayo_inani.getValue().열린파일);
            새서술자.실행시닫기 = okufakwayo_inani.getValue().실행시닫기;
            결과.서술자들.put(okufakwayo_inani.getKey(), 새서술자);
        }
        return 결과;
    }

    private int okungasho_lutho_thola_inkomba(int 최소번호) {
        for (int thola_inkomba = Math.max(0, 최소번호); thola_inkomba < 최대서술자; thola_inkomba++) {
            if (!서술자들.containsKey(Integer.valueOf(thola_inkomba))) {
                return thola_inkomba;
            }
        }
        return -1;
    }
}
