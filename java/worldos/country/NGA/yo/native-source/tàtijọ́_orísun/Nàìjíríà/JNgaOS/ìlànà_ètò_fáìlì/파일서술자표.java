// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nàìjíríà.JNgaOS.ìlànà_ètò_fáìlì;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fáìlì 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ìlànà_ètò_fáìlì.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ìlànà_ètò_fáìlì.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ìlànà_ètò_fáìlì ìlànà_ètò_fáìlì;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ìlànà_ètò_fáìlì ìlànà_ètò_fáìlì) {
        this.ìlànà_ètò_fáìlì = ìlànà_ètò_fáìlì;
    }

    public int Ṣi(String Orúkọ) {
        ìlànà_ètò_fáìlì.열린파일 열린파일 = ìlànà_ètò_fáìlì.Ṣi(Orúkọ);
        if (열린파일 == null) {
            return -2;
        }
        int wá_atọ̀ka_àkóónú = òfìfo_wá_atọ̀ka_àkóónú(3);
        if (wá_atọ̀ka_àkóónú < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(wá_atọ̀ka_àkóónú), new 서술자(열린파일));
        return wá_atọ̀ka_àkóónú;
    }

    public int Kàá(int wá_atọ̀ka_àkóónú, byte[] 받을곳, int Ìwọ̀n) {
        서술자 ìgbéwọlé_iye = 서술자들.get(Integer.valueOf(wá_atọ̀ka_àkóónú));
        if (ìgbéwọlé_iye == null) {
            return -9;
        }
        if (Ìwọ̀n < 0 || Ìwọ̀n > 받을곳.length) {
            return -22;
        }
        int 남음 = ìgbéwọlé_iye.열린파일.détà.length - ìgbéwọlé_iye.열린파일.위치;
        int 읽을크기 = Math.min(Ìwọ̀n, Math.max(남음, 0));
        System.arraycopy(ìgbéwọlé_iye.열린파일.détà, ìgbéwọlé_iye.열린파일.위치, 받을곳, 0, 읽을크기);
        ìgbéwọlé_iye.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int wá_atọ̀ka_àkóónú, int 거리, int 기준) {
        서술자 ìgbéwọlé_iye = 서술자들.get(Integer.valueOf(wá_atọ̀ka_àkóónú));
        if (ìgbéwọlé_iye == null) {
            return -9;
        }
        int Àgbétẹ́lẹ̀_iye;
        if (기준 == 0) {
            Àgbétẹ́lẹ̀_iye = 0;
        } else if (기준 == 1) {
            Àgbétẹ́lẹ̀_iye = ìgbéwọlé_iye.열린파일.위치;
        } else if (기준 == 2) {
            Àgbétẹ́lẹ̀_iye = ìgbéwọlé_iye.열린파일.détà.length;
        } else {
            return -22;
        }
        int 새위치 = Àgbétẹ́lẹ̀_iye + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ìgbéwọlé_iye.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int Ti(int wá_atọ̀ka_àkóónú) {
        서술자 ìgbéwọlé_iye = 서술자들.remove(Integer.valueOf(wá_atọ̀ka_àkóónú));
        if (ìgbéwọlé_iye == null) {
            return -9;
        }
        ìgbéwọlé_iye.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int wá_atọ̀ka_àkóónú, int 최소번호) {
        서술자 ìgbéwọlé_iye = 서술자들.get(Integer.valueOf(wá_atọ̀ka_àkóónú));
        if (ìgbéwọlé_iye == null) {
            return -9;
        }
        int 새번호 = òfìfo_wá_atọ̀ka_àkóónú(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ìgbéwọlé_iye.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ìgbéwọlé_iye.열린파일));
        return 새번호;
    }

    public int 지정복제(int wá_atọ̀ka_àkóónú, int 새번호) {
        if (wá_atọ̀ka_àkóónú == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(wá_atọ̀ka_àkóónú)) ? wá_atọ̀ka_àkóónú : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(wá_atọ̀ka_àkóónú));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Ti(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int wá_atọ̀ka_àkóónú, boolean iye) {
        서술자 ìgbéwọlé_iye = 서술자들.get(Integer.valueOf(wá_atọ̀ka_àkóónú));
        if (ìgbéwọlé_iye == null) {
            return -9;
        }
        ìgbéwọlé_iye.실행시닫기 = iye;
        return 0;
    }

    public int 실행시닫기값(int wá_atọ̀ka_àkóónú) {
        서술자 ìgbéwọlé_iye = 서술자들.get(Integer.valueOf(wá_atọ̀ka_àkóónú));
        if (ìgbéwọlé_iye == null) {
            return -9;
        }
        return ìgbéwọlé_iye.실행시닫기 ? 1 : 0;
    }

    public fáìlì_Ìwífún msinfo32_exe(int wá_atọ̀ka_àkóónú) {
        if (wá_atọ̀ka_àkóónú >= 0 && wá_atọ̀ka_àkóónú <= 2) {
            return new fáìlì_Ìwífún(0, 0020666);
        }
        서술자 ìgbéwọlé_iye = 서술자들.get(Integer.valueOf(wá_atọ̀ka_àkóónú));
        if (ìgbéwọlé_iye == null) {
            return null;
        }
        return new fáìlì_Ìwífún(ìgbéwọlé_iye.열린파일.détà.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer wá_atọ̀ka_àkóónú : 번호들) {
            서술자 ìgbéwọlé_iye = 서술자들.get(wá_atọ̀ka_àkóónú);
            if (ìgbéwọlé_iye != null && ìgbéwọlé_iye.실행시닫기) {
                Ti(wá_atọ̀ka_àkóónú.intValue());
            }
        }
    }

    public boolean 열려있음(int wá_atọ̀ka_àkóónú) {
        return 서술자들.containsKey(Integer.valueOf(wá_atọ̀ka_àkóónú));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(ìlànà_ètò_fáìlì);
        for (Map.Entry<Integer, 서술자> ìgbéwọlé_iye : 서술자들.entrySet()) {
            ìgbéwọlé_iye.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ìgbéwọlé_iye.getValue().열린파일);
            새서술자.실행시닫기 = ìgbéwọlé_iye.getValue().실행시닫기;
            결과.서술자들.put(ìgbéwọlé_iye.getKey(), 새서술자);
        }
        return 결과;
    }

    private int òfìfo_wá_atọ̀ka_àkóónú(int 최소번호) {
        for (int wá_atọ̀ka_àkóónú = Math.max(0, 최소번호); wá_atọ̀ka_àkóónú < 최대서술자; wá_atọ̀ka_àkóónú++) {
            if (!서술자들.containsKey(Integer.valueOf(wá_atọ̀ka_àkóónú))) {
                return wá_atọ̀ka_àkóónú;
            }
        }
        return -1;
    }
}
