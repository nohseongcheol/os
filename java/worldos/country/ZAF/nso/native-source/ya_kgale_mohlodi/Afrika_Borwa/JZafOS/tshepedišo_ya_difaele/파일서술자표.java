// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.tshepedišo_ya_difaele;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Faele 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final tshepedišo_ya_difaele.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(tshepedišo_ya_difaele.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final tshepedišo_ya_difaele tshepedišo_ya_difaele;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(tshepedišo_ya_difaele tshepedišo_ya_difaele) {
        this.tshepedišo_ya_difaele = tshepedišo_ya_difaele;
    }

    public int Bula(String Leina) {
        tshepedišo_ya_difaele.열린파일 열린파일 = tshepedišo_ya_difaele.Bula(Leina);
        if (열린파일 == null) {
            return -2;
        }
        int lokela = hloka_selo_lokela(3);
        if (lokela < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(lokela), new 서술자(열린파일));
        return lokela;
    }

    public int Bala(int lokela, byte[] 받을곳, int Bogolo) {
        서술자 go_tsenya_tshedimošo_boleng = 서술자들.get(Integer.valueOf(lokela));
        if (go_tsenya_tshedimošo_boleng == null) {
            return -9;
        }
        if (Bogolo < 0 || Bogolo > 받을곳.length) {
            return -22;
        }
        int 남음 = go_tsenya_tshedimošo_boleng.열린파일.data.length - go_tsenya_tshedimošo_boleng.열린파일.위치;
        int 읽을크기 = Math.min(Bogolo, Math.max(남음, 0));
        System.arraycopy(go_tsenya_tshedimošo_boleng.열린파일.data, go_tsenya_tshedimošo_boleng.열린파일.위치, 받을곳, 0, 읽을크기);
        go_tsenya_tshedimošo_boleng.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int lokela, int 거리, int 기준) {
        서술자 go_tsenya_tshedimošo_boleng = 서술자들.get(Integer.valueOf(lokela));
        if (go_tsenya_tshedimošo_boleng == null) {
            return -9;
        }
        int Bokamorago_boleng;
        if (기준 == 0) {
            Bokamorago_boleng = 0;
        } else if (기준 == 1) {
            Bokamorago_boleng = go_tsenya_tshedimošo_boleng.열린파일.위치;
        } else if (기준 == 2) {
            Bokamorago_boleng = go_tsenya_tshedimošo_boleng.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = Bokamorago_boleng + 거리;
        if (새위치 < 0) {
            return -22;
        }
        go_tsenya_tshedimošo_boleng.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int Tswalela(int lokela) {
        서술자 go_tsenya_tshedimošo_boleng = 서술자들.remove(Integer.valueOf(lokela));
        if (go_tsenya_tshedimošo_boleng == null) {
            return -9;
        }
        go_tsenya_tshedimošo_boleng.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int lokela, int 최소번호) {
        서술자 go_tsenya_tshedimošo_boleng = 서술자들.get(Integer.valueOf(lokela));
        if (go_tsenya_tshedimošo_boleng == null) {
            return -9;
        }
        int 새번호 = hloka_selo_lokela(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        go_tsenya_tshedimošo_boleng.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(go_tsenya_tshedimošo_boleng.열린파일));
        return 새번호;
    }

    public int 지정복제(int lokela, int 새번호) {
        if (lokela == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(lokela)) ? lokela : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(lokela));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Tswalela(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int lokela, boolean boleng) {
        서술자 go_tsenya_tshedimošo_boleng = 서술자들.get(Integer.valueOf(lokela));
        if (go_tsenya_tshedimošo_boleng == null) {
            return -9;
        }
        go_tsenya_tshedimošo_boleng.실행시닫기 = boleng;
        return 0;
    }

    public int 실행시닫기값(int lokela) {
        서술자 go_tsenya_tshedimošo_boleng = 서술자들.get(Integer.valueOf(lokela));
        if (go_tsenya_tshedimošo_boleng == null) {
            return -9;
        }
        return go_tsenya_tshedimošo_boleng.실행시닫기 ? 1 : 0;
    }

    public faele_tshedimošo msinfo32_exe(int lokela) {
        if (lokela >= 0 && lokela <= 2) {
            return new faele_tshedimošo(0, 0020666);
        }
        서술자 go_tsenya_tshedimošo_boleng = 서술자들.get(Integer.valueOf(lokela));
        if (go_tsenya_tshedimošo_boleng == null) {
            return null;
        }
        return new faele_tshedimošo(go_tsenya_tshedimošo_boleng.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer lokela : 번호들) {
            서술자 go_tsenya_tshedimošo_boleng = 서술자들.get(lokela);
            if (go_tsenya_tshedimošo_boleng != null && go_tsenya_tshedimošo_boleng.실행시닫기) {
                Tswalela(lokela.intValue());
            }
        }
    }

    public boolean 열려있음(int lokela) {
        return 서술자들.containsKey(Integer.valueOf(lokela));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(tshepedišo_ya_difaele);
        for (Map.Entry<Integer, 서술자> go_tsenya_tshedimošo_boleng : 서술자들.entrySet()) {
            go_tsenya_tshedimošo_boleng.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(go_tsenya_tshedimošo_boleng.getValue().열린파일);
            새서술자.실행시닫기 = go_tsenya_tshedimošo_boleng.getValue().실행시닫기;
            결과.서술자들.put(go_tsenya_tshedimošo_boleng.getKey(), 새서술자);
        }
        return 결과;
    }

    private int hloka_selo_lokela(int 최소번호) {
        for (int lokela = Math.max(0, 최소번호); lokela < 최대서술자; lokela++) {
            if (!서술자들.containsKey(Integer.valueOf(lokela))) {
                return lokela;
            }
        }
        return -1;
    }
}
