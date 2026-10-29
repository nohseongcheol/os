// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Msumbiji.JMozOS.mfumo_ya_mafaili;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 faili 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final mfumo_ya_mafaili.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(mfumo_ya_mafaili.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final mfumo_ya_mafaili mfumo_ya_mafaili;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(mfumo_ya_mafaili mfumo_ya_mafaili) {
        this.mfumo_ya_mafaili = mfumo_ya_mafaili;
    }

    public int unda(String Jina) {
        mfumo_ya_mafaili.열린파일 열린파일 = mfumo_ya_mafaili.unda(Jina);
        if (열린파일 == null) {
            return -2;
        }
        int kielezo = tupu_kielezo(3);
        if (kielezo < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(kielezo), new 서술자(열린파일));
        return kielezo;
    }

    public int 읽기(int kielezo, byte[] 받을곳, int panga_ukubwa) {
        서술자 ingizo_thamani = 서술자들.get(Integer.valueOf(kielezo));
        if (ingizo_thamani == null) {
            return -9;
        }
        if (panga_ukubwa < 0 || panga_ukubwa > 받을곳.length) {
            return -22;
        }
        int 남음 = ingizo_thamani.열린파일.data.length - ingizo_thamani.열린파일.위치;
        int 읽을크기 = Math.min(panga_ukubwa, Math.max(남음, 0));
        System.arraycopy(ingizo_thamani.열린파일.data, ingizo_thamani.열린파일.위치, 받을곳, 0, 읽을크기);
        ingizo_thamani.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int kielezo, int 거리, int 기준) {
        서술자 ingizo_thamani = 서술자들.get(Integer.valueOf(kielezo));
        if (ingizo_thamani == null) {
            return -9;
        }
        int nyuma_thamani;
        if (기준 == 0) {
            nyuma_thamani = 0;
        } else if (기준 == 1) {
            nyuma_thamani = ingizo_thamani.열린파일.위치;
        } else if (기준 == 2) {
            nyuma_thamani = ingizo_thamani.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = nyuma_thamani + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ingizo_thamani.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int funga(int kielezo) {
        서술자 ingizo_thamani = 서술자들.remove(Integer.valueOf(kielezo));
        if (ingizo_thamani == null) {
            return -9;
        }
        ingizo_thamani.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int kielezo, int 최소번호) {
        서술자 ingizo_thamani = 서술자들.get(Integer.valueOf(kielezo));
        if (ingizo_thamani == null) {
            return -9;
        }
        int 새번호 = tupu_kielezo(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ingizo_thamani.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ingizo_thamani.열린파일));
        return 새번호;
    }

    public int 지정복제(int kielezo, int 새번호) {
        if (kielezo == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(kielezo)) ? kielezo : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(kielezo));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            funga(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int kielezo, boolean thamani) {
        서술자 ingizo_thamani = 서술자들.get(Integer.valueOf(kielezo));
        if (ingizo_thamani == null) {
            return -9;
        }
        ingizo_thamani.실행시닫기 = thamani;
        return 0;
    }

    public int 실행시닫기값(int kielezo) {
        서술자 ingizo_thamani = 서술자들.get(Integer.valueOf(kielezo));
        if (ingizo_thamani == null) {
            return -9;
        }
        return ingizo_thamani.실행시닫기 ? 1 : 0;
    }

    public faili_maelezo msinfo32_exe(int kielezo) {
        if (kielezo >= 0 && kielezo <= 2) {
            return new faili_maelezo(0, 0020666);
        }
        서술자 ingizo_thamani = 서술자들.get(Integer.valueOf(kielezo));
        if (ingizo_thamani == null) {
            return null;
        }
        return new faili_maelezo(ingizo_thamani.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer kielezo : 번호들) {
            서술자 ingizo_thamani = 서술자들.get(kielezo);
            if (ingizo_thamani != null && ingizo_thamani.실행시닫기) {
                funga(kielezo.intValue());
            }
        }
    }

    public boolean teknolojia_ya_maelezo_unda(int kielezo) {
        return 서술자들.containsKey(Integer.valueOf(kielezo));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(mfumo_ya_mafaili);
        for (Map.Entry<Integer, 서술자> ingizo_thamani : 서술자들.entrySet()) {
            ingizo_thamani.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ingizo_thamani.getValue().열린파일);
            새서술자.실행시닫기 = ingizo_thamani.getValue().실행시닫기;
            결과.서술자들.put(ingizo_thamani.getKey(), 새서술자);
        }
        return 결과;
    }

    private int tupu_kielezo(int 최소번호) {
        for (int kielezo = Math.max(0, 최소번호); kielezo < 최대서술자; kielezo++) {
            if (!서술자들.containsKey(Integer.valueOf(kielezo))) {
                return kielezo;
            }
        }
        return -1;
    }
}
