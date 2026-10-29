// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ռուսաստան.JRusOS.նիշքային_համակարգ;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Ֆայլ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final նիշքային_համակարգ.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(նիշքային_համակարգ.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final նիշքային_համակարգ նիշքային_համակարգ;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(նիշքային_համակարգ նիշքային_համակարգ) {
        this.նիշքային_համակարգ = նիշքային_համակարգ;
    }

    public int Բաց(String Անուն) {
        նիշքային_համակարգ.열린파일 열린파일 = նիշքային_համակարգ.Բաց(Անուն);
        if (열린파일 == null) {
            return -2;
        }
        int դասիչ = դատարկ_դասիչ(3);
        if (դասիչ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(դասիչ), new 서술자(열린파일));
        return դասիչ;
    }

    public int Ընթերցում(int դասիչ, byte[] 받을곳, int Չափս) {
        서술자 մուտքագրում_արժեք = 서술자들.get(Integer.valueOf(դասիչ));
        if (մուտքագրում_արժեք == null) {
            return -9;
        }
        if (Չափս < 0 || Չափս > 받을곳.length) {
            return -22;
        }
        int 남음 = մուտքագրում_արժեք.열린파일.տվյալ.length - մուտքագրում_արժեք.열린파일.Դիրք;
        int 읽을크기 = Math.min(Չափս, Math.max(남음, 0));
        System.arraycopy(մուտքագրում_արժեք.열린파일.տվյալ, մուտքագրում_արժեք.열린파일.Դիրք, 받을곳, 0, 읽을크기);
        մուտքագրում_արժեք.열린파일.Դիրք += 읽을크기;
        return 읽을크기;
    }

    public int տեղափոխել_դիրք(int դասիչ, int 거리, int արձակել_արմատ) {
        서술자 մուտքագրում_արժեք = 서술자들.get(Integer.valueOf(դասիչ));
        if (մուտքագրում_արժեք == null) {
            return -9;
        }
        int խորք_արժեք;
        if (արձակել_արմատ == 0) {
            խորք_արժեք = 0;
        } else if (արձակել_արմատ == 1) {
            խորք_արժեք = մուտքագրում_արժեք.열린파일.Դիրք;
        } else if (արձակել_արմատ == 2) {
            խորք_արժեք = մուտքագրում_արժեք.열린파일.տվյալ.length;
        } else {
            return -22;
        }
        int 새위치 = խորք_արժեք + 거리;
        if (새위치 < 0) {
            return -22;
        }
        մուտքագրում_արժեք.열린파일.Դիրք = 새위치;
        return 새위치;
    }

    public int Փակ(int դասիչ) {
        서술자 մուտքագրում_արժեք = 서술자들.remove(Integer.valueOf(դասիչ));
        if (մուտքագրում_արժեք == null) {
            return -9;
        }
        մուտքագրում_արժեք.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int դասիչ, int 최소번호) {
        서술자 մուտքագրում_արժեք = 서술자들.get(Integer.valueOf(դասիչ));
        if (մուտքագրում_արժեք == null) {
            return -9;
        }
        int 새번호 = դատարկ_դասիչ(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        մուտքագրում_արժեք.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(մուտքագրում_արժեք.열린파일));
        return 새번호;
    }

    public int 지정복제(int դասիչ, int 새번호) {
        if (դասիչ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(դասիչ)) ? դասիչ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(դասիչ));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Փակ(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int դասիչ, boolean արժեք) {
        서술자 մուտքագրում_արժեք = 서술자들.get(Integer.valueOf(դասիչ));
        if (մուտքագրում_արժեք == null) {
            return -9;
        }
        մուտքագրում_արժեք.실행시닫기 = արժեք;
        return 0;
    }

    public int 실행시닫기값(int դասիչ) {
        서술자 մուտքագրում_արժեք = 서술자들.get(Integer.valueOf(դասիչ));
        if (մուտքագրում_արժեք == null) {
            return -9;
        }
        return մուտքագրում_արժեք.실행시닫기 ? 1 : 0;
    }

    public նիշք_տեղեկություն Համակարգի_տեղեկություն(int դասիչ) {
        if (դասիչ >= 0 && դասիչ <= 2) {
            return new նիշք_տեղեկություն(0, 0020666);
        }
        서술자 մուտքագրում_արժեք = 서술자들.get(Integer.valueOf(դասիչ));
        if (մուտքագրում_արժեք == null) {
            return null;
        }
        return new նիշք_տեղեկություն(մուտքագրում_արժեք.열린파일.տվյալ.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer դասիչ : 번호들) {
            서술자 մուտքագրում_արժեք = 서술자들.get(դասիչ);
            if (մուտքագրում_արժեք != null && մուտքագրում_արժեք.실행시닫기) {
                Փակ(դասիչ.intValue());
            }
        }
    }

    public boolean 열려있음(int դասիչ) {
        return 서술자들.containsKey(Integer.valueOf(դասիչ));
    }

    public 파일서술자표 복제() {
        파일서술자표 չափ = new 파일서술자표(նիշքային_համակարգ);
        for (Map.Entry<Integer, 서술자> մուտքագրում_արժեք : 서술자들.entrySet()) {
            մուտքագրում_արժեք.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(մուտքագրում_արժեք.getValue().열린파일);
            새서술자.실행시닫기 = մուտքագրում_արժեք.getValue().실행시닫기;
            չափ.서술자들.put(մուտքագրում_արժեք.getKey(), 새서술자);
        }
        return չափ;
    }

    private int դատարկ_դասիչ(int 최소번호) {
        for (int դասիչ = Math.max(0, 최소번호); դասիչ < 최대서술자; դասիչ++) {
            if (!서술자들.containsKey(Integer.valueOf(դասիչ))) {
                return դասիչ;
            }
        }
        return -1;
    }
}
