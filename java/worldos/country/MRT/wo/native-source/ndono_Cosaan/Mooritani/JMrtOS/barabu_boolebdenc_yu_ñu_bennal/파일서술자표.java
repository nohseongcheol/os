// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mooritani.JMrtOS.barabu_boolebdenc_yu_ñu_bennal;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 bara_denc 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final barabu_boolebdenc_yu_ñu_bennal.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(barabu_boolebdenc_yu_ñu_bennal.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final barabu_boolebdenc_yu_ñu_bennal barabu_boolebdenc_yu_ñu_bennal;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(barabu_boolebdenc_yu_ñu_bennal barabu_boolebdenc_yu_ñu_bennal) {
        this.barabu_boolebdenc_yu_ñu_bennal = barabu_boolebdenc_yu_ñu_bennal;
    }

    public int sos(String tur_253d1510) {
        barabu_boolebdenc_yu_ñu_bennal.열린파일 열린파일 = barabu_boolebdenc_yu_ñu_bennal.sos(tur_253d1510);
        if (열린파일 == null) {
            return -2;
        }
        int àlluwa_tur = neen_àlluwa_tur(3);
        if (àlluwa_tur < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(àlluwa_tur), new 서술자(열린파일));
        return àlluwa_tur;
    }

    public int 읽기(int àlluwa_tur, byte[] 받을곳, int tolluwaay) {
        서술자 dugal_xabaar_xëyma = 서술자들.get(Integer.valueOf(àlluwa_tur));
        if (dugal_xabaar_xëyma == null) {
            return -9;
        }
        if (tolluwaay < 0 || tolluwaay > 받을곳.length) {
            return -22;
        }
        int 남음 = dugal_xabaar_xëyma.열린파일.mbir.length - dugal_xabaar_xëyma.열린파일.위치;
        int 읽을크기 = Math.min(tolluwaay, Math.max(남음, 0));
        System.arraycopy(dugal_xabaar_xëyma.열린파일.mbir, dugal_xabaar_xëyma.열린파일.위치, 받을곳, 0, 읽을크기);
        dugal_xabaar_xëyma.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int àlluwa_tur, int 거리, int 기준) {
        서술자 dugal_xabaar_xëyma = 서술자들.get(Integer.valueOf(àlluwa_tur));
        if (dugal_xabaar_xëyma == null) {
            return -9;
        }
        int Njiitlay_xëyma;
        if (기준 == 0) {
            Njiitlay_xëyma = 0;
        } else if (기준 == 1) {
            Njiitlay_xëyma = dugal_xabaar_xëyma.열린파일.위치;
        } else if (기준 == 2) {
            Njiitlay_xëyma = dugal_xabaar_xëyma.열린파일.mbir.length;
        } else {
            return -22;
        }
        int 새위치 = Njiitlay_xëyma + 거리;
        if (새위치 < 0) {
            return -22;
        }
        dugal_xabaar_xëyma.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int Tej(int àlluwa_tur) {
        서술자 dugal_xabaar_xëyma = 서술자들.remove(Integer.valueOf(àlluwa_tur));
        if (dugal_xabaar_xëyma == null) {
            return -9;
        }
        dugal_xabaar_xëyma.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int àlluwa_tur, int 최소번호) {
        서술자 dugal_xabaar_xëyma = 서술자들.get(Integer.valueOf(àlluwa_tur));
        if (dugal_xabaar_xëyma == null) {
            return -9;
        }
        int 새번호 = neen_àlluwa_tur(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        dugal_xabaar_xëyma.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(dugal_xabaar_xëyma.열린파일));
        return 새번호;
    }

    public int 지정복제(int àlluwa_tur, int 새번호) {
        if (àlluwa_tur == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(àlluwa_tur)) ? àlluwa_tur : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(àlluwa_tur));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Tej(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int àlluwa_tur, boolean xëyma) {
        서술자 dugal_xabaar_xëyma = 서술자들.get(Integer.valueOf(àlluwa_tur));
        if (dugal_xabaar_xëyma == null) {
            return -9;
        }
        dugal_xabaar_xëyma.실행시닫기 = xëyma;
        return 0;
    }

    public int 실행시닫기값(int àlluwa_tur) {
        서술자 dugal_xabaar_xëyma = 서술자들.get(Integer.valueOf(àlluwa_tur));
        if (dugal_xabaar_xëyma == null) {
            return -9;
        }
        return dugal_xabaar_xëyma.실행시닫기 ? 1 : 0;
    }

    public bara_denc_yëglë msinfo32_exe(int àlluwa_tur) {
        if (àlluwa_tur >= 0 && àlluwa_tur <= 2) {
            return new bara_denc_yëglë(0, 0020666);
        }
        서술자 dugal_xabaar_xëyma = 서술자들.get(Integer.valueOf(àlluwa_tur));
        if (dugal_xabaar_xëyma == null) {
            return null;
        }
        return new bara_denc_yëglë(dugal_xabaar_xëyma.열린파일.mbir.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer àlluwa_tur : 번호들) {
            서술자 dugal_xabaar_xëyma = 서술자들.get(àlluwa_tur);
            if (dugal_xabaar_xëyma != null && dugal_xabaar_xëyma.실행시닫기) {
                Tej(àlluwa_tur.intValue());
            }
        }
    }

    public boolean 열려있음(int àlluwa_tur) {
        return 서술자들.containsKey(Integer.valueOf(àlluwa_tur));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(barabu_boolebdenc_yu_ñu_bennal);
        for (Map.Entry<Integer, 서술자> dugal_xabaar_xëyma : 서술자들.entrySet()) {
            dugal_xabaar_xëyma.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(dugal_xabaar_xëyma.getValue().열린파일);
            새서술자.실행시닫기 = dugal_xabaar_xëyma.getValue().실행시닫기;
            결과.서술자들.put(dugal_xabaar_xëyma.getKey(), 새서술자);
        }
        return 결과;
    }

    private int neen_àlluwa_tur(int 최소번호) {
        for (int àlluwa_tur = Math.max(0, 최소번호); àlluwa_tur < 최대서술자; àlluwa_tur++) {
            if (!서술자들.containsKey(Integer.valueOf(àlluwa_tur))) {
                return àlluwa_tur;
            }
        }
        return -1;
    }
}
