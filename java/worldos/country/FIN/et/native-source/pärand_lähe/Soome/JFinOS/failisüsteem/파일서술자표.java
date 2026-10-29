// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Soome.JFinOS.failisüsteem;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fail 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final failisüsteem.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(failisüsteem.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final failisüsteem failisüsteem;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(failisüsteem failisüsteem) {
        this.failisüsteem = failisüsteem;
    }

    public int Ava(String Nimi_2) {
        failisüsteem.열린파일 열린파일 = failisüsteem.Ava(Nimi_2);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = 빈번호(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Lugemine(int INDEX, byte[] saama_sihtkoht, int Suurus) {
        서술자 kirje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kirje_VALUE == null) {
            return -9;
        }
        if (Suurus < 0 || Suurus > saama_sihtkoht.length) {
            return -22;
        }
        int 남음 = kirje_VALUE.열린파일.andmed.length - kirje_VALUE.열린파일.Asukoht;
        int 읽을크기 = Math.min(Suurus, Math.max(남음, 0));
        System.arraycopy(kirje_VALUE.열린파일.andmed, kirje_VALUE.열린파일.Asukoht, saama_sihtkoht, 0, 읽을크기);
        kirje_VALUE.열린파일.Asukoht += 읽을크기;
        return 읽을크기;
    }

    public int liigutama_ametikoht(int INDEX, int 거리, int Project_juur) {
        서술자 kirje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kirje_VALUE == null) {
            return -9;
        }
        int taust_VALUE;
        if (Project_juur == 0) {
            taust_VALUE = 0;
        } else if (Project_juur == 1) {
            taust_VALUE = kirje_VALUE.열린파일.Asukoht;
        } else if (Project_juur == 2) {
            taust_VALUE = kirje_VALUE.열린파일.andmed.length;
        } else {
            return -22;
        }
        int 새위치 = taust_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        kirje_VALUE.열린파일.Asukoht = 새위치;
        return 새위치;
    }

    public int Suletud(int INDEX) {
        서술자 kirje_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (kirje_VALUE == null) {
            return -9;
        }
        kirje_VALUE.열린파일.viide_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 kirje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kirje_VALUE == null) {
            return -9;
        }
        int Uus_number = 빈번호(최소번호);
        if (Uus_number < 0) {
            return -24;
        }
        kirje_VALUE.열린파일.viide_COUNT++;
        서술자들.put(Integer.valueOf(Uus_number), new 서술자(kirje_VALUE.열린파일));
        return Uus_number;
    }

    public int 지정복제(int INDEX, int Uus_number) {
        if (INDEX == Uus_number) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (Uus_number < 0 || Uus_number >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Uus_number))) {
            Suletud(Uus_number);
        }
        원본.열린파일.viide_COUNT++;
        서술자들.put(Integer.valueOf(Uus_number), new 서술자(원본.열린파일));
        return Uus_number;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 kirje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kirje_VALUE == null) {
            return -9;
        }
        kirje_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 kirje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kirje_VALUE == null) {
            return -9;
        }
        return kirje_VALUE.실행시닫기 ? 1 : 0;
    }

    public Fail_teave msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new Fail_teave(0, 0020666);
        }
        서술자 kirje_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kirje_VALUE == null) {
            return null;
        }
        return new Fail_teave(kirje_VALUE.열린파일.andmed.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] number_Loend = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : number_Loend) {
            서술자 kirje_VALUE = 서술자들.get(INDEX);
            if (kirje_VALUE != null && kirje_VALUE.실행시닫기) {
                Suletud(INDEX.intValue());
            }
        }
    }

    public boolean infotehnoloogia_avama(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 kloon_VALUE() {
        파일서술자표 TULEMUS = new 파일서술자표(failisüsteem);
        for (Map.Entry<Integer, 서술자> kirje_VALUE : 서술자들.entrySet()) {
            kirje_VALUE.getValue().열린파일.viide_COUNT++;
            서술자 새서술자 = new 서술자(kirje_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = kirje_VALUE.getValue().실행시닫기;
            TULEMUS.서술자들.put(kirje_VALUE.getKey(), 새서술자);
        }
        return TULEMUS;
    }

    private int 빈번호(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
