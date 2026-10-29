// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.inikkuvik;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ini 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final inikkuvik.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(inikkuvik.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final inikkuvik inikkuvik;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(inikkuvik inikkuvik) {
        this.inikkuvik = inikkuvik;
    }

    public int matuirli(String atiq) {
        inikkuvik.열린파일 열린파일 = inikkuvik.matuirli(atiq);
        if (열린파일 == null) {
            return -2;
        }
        int nalunaiqsimavik = 빈번호(3);
        if (nalunaiqsimavik < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(nalunaiqsimavik), new 서술자(열린파일));
        return nalunaiqsimavik;
    }

    public int 읽기(int nalunaiqsimavik, byte[] 받을곳, int anininga) {
        서술자 Iliniku_atuutilik = 서술자들.get(Integer.valueOf(nalunaiqsimavik));
        if (Iliniku_atuutilik == null) {
            return -9;
        }
        if (anininga < 0 || anininga > 받을곳.length) {
            return -22;
        }
        int 남음 = Iliniku_atuutilik.열린파일.titiqqat.length - Iliniku_atuutilik.열린파일.위치;
        int 읽을크기 = Math.min(anininga, Math.max(남음, 0));
        System.arraycopy(Iliniku_atuutilik.열린파일.titiqqat, Iliniku_atuutilik.열린파일.위치, 받을곳, 0, 읽을크기);
        Iliniku_atuutilik.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int nalunaiqsimavik, int 거리, int 기준) {
        서술자 Iliniku_atuutilik = 서술자들.get(Integer.valueOf(nalunaiqsimavik));
        if (Iliniku_atuutilik == null) {
            return -9;
        }
        int ungataa_atuutilik;
        if (기준 == 0) {
            ungataa_atuutilik = 0;
        } else if (기준 == 1) {
            ungataa_atuutilik = Iliniku_atuutilik.열린파일.위치;
        } else if (기준 == 2) {
            ungataa_atuutilik = Iliniku_atuutilik.열린파일.titiqqat.length;
        } else {
            return -22;
        }
        int 새위치 = ungataa_atuutilik + 거리;
        if (새위치 < 0) {
            return -22;
        }
        Iliniku_atuutilik.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int matuli(int nalunaiqsimavik) {
        서술자 Iliniku_atuutilik = 서술자들.remove(Integer.valueOf(nalunaiqsimavik));
        if (Iliniku_atuutilik == null) {
            return -9;
        }
        Iliniku_atuutilik.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int nalunaiqsimavik, int 최소번호) {
        서술자 Iliniku_atuutilik = 서술자들.get(Integer.valueOf(nalunaiqsimavik));
        if (Iliniku_atuutilik == null) {
            return -9;
        }
        int 새번호 = 빈번호(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        Iliniku_atuutilik.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(Iliniku_atuutilik.열린파일));
        return 새번호;
    }

    public int 지정복제(int nalunaiqsimavik, int 새번호) {
        if (nalunaiqsimavik == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(nalunaiqsimavik)) ? nalunaiqsimavik : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(nalunaiqsimavik));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            matuli(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int nalunaiqsimavik, boolean atuutilik) {
        서술자 Iliniku_atuutilik = 서술자들.get(Integer.valueOf(nalunaiqsimavik));
        if (Iliniku_atuutilik == null) {
            return -9;
        }
        Iliniku_atuutilik.실행시닫기 = atuutilik;
        return 0;
    }

    public int 실행시닫기값(int nalunaiqsimavik) {
        서술자 Iliniku_atuutilik = 서술자들.get(Integer.valueOf(nalunaiqsimavik));
        if (Iliniku_atuutilik == null) {
            return -9;
        }
        return Iliniku_atuutilik.실행시닫기 ? 1 : 0;
    }

    public ini_tukisigiarut msinfo32_exe(int nalunaiqsimavik) {
        if (nalunaiqsimavik >= 0 && nalunaiqsimavik <= 2) {
            return new ini_tukisigiarut(0, 0020666);
        }
        서술자 Iliniku_atuutilik = 서술자들.get(Integer.valueOf(nalunaiqsimavik));
        if (Iliniku_atuutilik == null) {
            return null;
        }
        return new ini_tukisigiarut(Iliniku_atuutilik.열린파일.titiqqat.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer nalunaiqsimavik : 번호들) {
            서술자 Iliniku_atuutilik = 서술자들.get(nalunaiqsimavik);
            if (Iliniku_atuutilik != null && Iliniku_atuutilik.실행시닫기) {
                matuli(nalunaiqsimavik.intValue());
            }
        }
    }

    public boolean 열려있음(int nalunaiqsimavik) {
        return 서술자들.containsKey(Integer.valueOf(nalunaiqsimavik));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(inikkuvik);
        for (Map.Entry<Integer, 서술자> Iliniku_atuutilik : 서술자들.entrySet()) {
            Iliniku_atuutilik.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(Iliniku_atuutilik.getValue().열린파일);
            새서술자.실행시닫기 = Iliniku_atuutilik.getValue().실행시닫기;
            결과.서술자들.put(Iliniku_atuutilik.getKey(), 새서술자);
        }
        return 결과;
    }

    private int 빈번호(int 최소번호) {
        for (int nalunaiqsimavik = Math.max(0, 최소번호); nalunaiqsimavik < 최대서술자; nalunaiqsimavik++) {
            if (!서술자들.containsKey(Integer.valueOf(nalunaiqsimavik))) {
                return nalunaiqsimavik;
            }
        }
        return -1;
    }
}
