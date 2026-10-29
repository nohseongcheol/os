// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.pūnaha_kōnae;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Kōnae 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final pūnaha_kōnae.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(pūnaha_kōnae.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final pūnaha_kōnae pūnaha_kōnae;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(pūnaha_kōnae pūnaha_kōnae) {
        this.pūnaha_kōnae = pūnaha_kōnae;
    }

    public int Huaki(String Ingoa) {
        pūnaha_kōnae.열린파일 열린파일 = pūnaha_kōnae.Huaki(Ingoa);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = putua_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Pānuitia(int INDEX, byte[] 받을곳, int rahi) {
        서술자 tāurunga_uara = 서술자들.get(Integer.valueOf(INDEX));
        if (tāurunga_uara == null) {
            return -9;
        }
        if (rahi < 0 || rahi > 받을곳.length) {
            return -22;
        }
        int 남음 = tāurunga_uara.열린파일.raraunga.length - tāurunga_uara.열린파일.tūranga;
        int 읽을크기 = Math.min(rahi, Math.max(남음, 0));
        System.arraycopy(tāurunga_uara.열린파일.raraunga, tāurunga_uara.열린파일.tūranga, 받을곳, 0, 읽을크기);
        tāurunga_uara.열린파일.tūranga += 읽을크기;
        return 읽을크기;
    }

    public int nuku_tūranga(int INDEX, int 거리, int whakaatu_pūtake) {
        서술자 tāurunga_uara = 서술자들.get(Integer.valueOf(INDEX));
        if (tāurunga_uara == null) {
            return -9;
        }
        int Papamuri_uara;
        if (whakaatu_pūtake == 0) {
            Papamuri_uara = 0;
        } else if (whakaatu_pūtake == 1) {
            Papamuri_uara = tāurunga_uara.열린파일.tūranga;
        } else if (whakaatu_pūtake == 2) {
            Papamuri_uara = tāurunga_uara.열린파일.raraunga.length;
        } else {
            return -22;
        }
        int 새위치 = Papamuri_uara + 거리;
        if (새위치 < 0) {
            return -22;
        }
        tāurunga_uara.열린파일.tūranga = 새위치;
        return 새위치;
    }

    public int Kati(int INDEX) {
        서술자 tāurunga_uara = 서술자들.remove(Integer.valueOf(INDEX));
        if (tāurunga_uara == null) {
            return -9;
        }
        tāurunga_uara.열린파일.Pūranga_kōrero_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 tāurunga_uara = 서술자들.get(Integer.valueOf(INDEX));
        if (tāurunga_uara == null) {
            return -9;
        }
        int 새번호 = putua_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        tāurunga_uara.열린파일.Pūranga_kōrero_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(tāurunga_uara.열린파일));
        return 새번호;
    }

    public int 지정복제(int INDEX, int 새번호) {
        if (INDEX == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Kati(새번호);
        }
        원본.열린파일.Pūranga_kōrero_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean uara) {
        서술자 tāurunga_uara = 서술자들.get(Integer.valueOf(INDEX));
        if (tāurunga_uara == null) {
            return -9;
        }
        tāurunga_uara.실행시닫기 = uara;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 tāurunga_uara = 서술자들.get(Integer.valueOf(INDEX));
        if (tāurunga_uara == null) {
            return -9;
        }
        return tāurunga_uara.실행시닫기 ? 1 : 0;
    }

    public kōnae_mōhiohio msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new kōnae_mōhiohio(0, 0020666);
        }
        서술자 tāurunga_uara = 서술자들.get(Integer.valueOf(INDEX));
        if (tāurunga_uara == null) {
            return null;
        }
        return new kōnae_mōhiohio(tāurunga_uara.열린파일.raraunga.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 tāurunga_uara = 서술자들.get(INDEX);
            if (tāurunga_uara != null && tāurunga_uara.실행시닫기) {
                Kati(INDEX.intValue());
            }
        }
    }

    public boolean 열려있음(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 mēhua = new 파일서술자표(pūnaha_kōnae);
        for (Map.Entry<Integer, 서술자> tāurunga_uara : 서술자들.entrySet()) {
            tāurunga_uara.getValue().열린파일.Pūranga_kōrero_COUNT++;
            서술자 새서술자 = new 서술자(tāurunga_uara.getValue().열린파일);
            새서술자.실행시닫기 = tāurunga_uara.getValue().실행시닫기;
            mēhua.서술자들.put(tāurunga_uara.getKey(), 새서술자);
        }
        return mēhua;
    }

    private int putua_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
