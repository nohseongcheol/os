// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ரீயூனியன்.JReuOS.கோப்பு_முறைமை;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 கோப்பின்_பெயர் 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final கோப்பு_முறைமை.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(கோப்பு_முறைமை.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final கோப்பு_முறைமை கோப்பு_முறைமை;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(கோப்பு_முறைமை கோப்பு_முறைமை) {
        this.கோப்பு_முறைமை = கோப்பு_முறைமை;
    }

    public int திற(String பெயர்) {
        கோப்பு_முறைமை.열린파일 열린파일 = கோப்பு_முறைமை.திற(பெயர்);
        if (열린파일 == null) {
            return -2;
        }
        int அடைவு = வெறுமை_அடைவு(3);
        if (அடைவு < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(அடைவு), new 서술자(열린파일));
        return அடைவு;
    }

    public int படி(int அடைவு, byte[] 받을곳, int அளவு) {
        서술자 உள்ளீடு_மதிப்பு = 서술자들.get(Integer.valueOf(அடைவு));
        if (உள்ளீடு_மதிப்பு == null) {
            return -9;
        }
        if (அளவு < 0 || அளவு > 받을곳.length) {
            return -22;
        }
        int 남음 = உள்ளீடு_மதிப்பு.열린파일.தரவு.length - உள்ளீடு_மதிப்பு.열린파일.இடம்;
        int 읽을크기 = Math.min(அளவு, Math.max(남음, 0));
        System.arraycopy(உள்ளீடு_மதிப்பு.열린파일.தரவு, உள்ளீடு_மதிப்பு.열린파일.இடம், 받을곳, 0, 읽을크기);
        உள்ளீடு_மதிப்பு.열린파일.இடம் += 읽을크기;
        return 읽을크기;
    }

    public int நகர்த்து_நிலை(int அடைவு, int 거리, int திட்டப்பணி_மூலம்) {
        서술자 உள்ளீடு_மதிப்பு = 서술자들.get(Integer.valueOf(அடைவு));
        if (உள்ளீடு_மதிப்பு == null) {
            return -9;
        }
        int பின்புல_மதிப்பு;
        if (திட்டப்பணி_மூலம் == 0) {
            பின்புல_மதிப்பு = 0;
        } else if (திட்டப்பணி_மூலம் == 1) {
            பின்புல_மதிப்பு = உள்ளீடு_மதிப்பு.열린파일.இடம்;
        } else if (திட்டப்பணி_மூலம் == 2) {
            பின்புல_மதிப்பு = உள்ளீடு_மதிப்பு.열린파일.தரவு.length;
        } else {
            return -22;
        }
        int 새위치 = பின்புல_மதிப்பு + 거리;
        if (새위치 < 0) {
            return -22;
        }
        உள்ளீடு_மதிப்பு.열린파일.இடம் = 새위치;
        return 새위치;
    }

    public int மூடு(int அடைவு) {
        서술자 உள்ளீடு_மதிப்பு = 서술자들.remove(Integer.valueOf(அடைவு));
        if (உள்ளீடு_மதிப்பு == null) {
            return -9;
        }
        உள்ளீடு_மதிப்பு.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int அடைவு, int 최소번호) {
        서술자 உள்ளீடு_மதிப்பு = 서술자들.get(Integer.valueOf(அடைவு));
        if (உள்ளீடு_மதிப்பு == null) {
            return -9;
        }
        int 새번호 = வெறுமை_அடைவு(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        உள்ளீடு_மதிப்பு.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(உள்ளீடு_மதிப்பு.열린파일));
        return 새번호;
    }

    public int 지정복제(int அடைவு, int 새번호) {
        if (அடைவு == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(அடைவு)) ? அடைவு : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(அடைவு));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            மூடு(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int அடைவு, boolean மதிப்பு) {
        서술자 உள்ளீடு_மதிப்பு = 서술자들.get(Integer.valueOf(அடைவு));
        if (உள்ளீடு_மதிப்பு == null) {
            return -9;
        }
        உள்ளீடு_மதிப்பு.실행시닫기 = மதிப்பு;
        return 0;
    }

    public int 실행시닫기값(int அடைவு) {
        서술자 உள்ளீடு_மதிப்பு = 서술자들.get(Integer.valueOf(அடைவு));
        if (உள்ளீடு_மதிப்பு == null) {
            return -9;
        }
        return உள்ளீடு_மதிப்பு.실행시닫기 ? 1 : 0;
    }

    public கோப்பு_தகவல் கணினித்_தகவல்(int அடைவு) {
        if (அடைவு >= 0 && அடைவு <= 2) {
            return new கோப்பு_தகவல்(0, 0020666);
        }
        서술자 உள்ளீடு_மதிப்பு = 서술자들.get(Integer.valueOf(அடைவு));
        if (உள்ளீடு_மதிப்பு == null) {
            return null;
        }
        return new கோப்பு_தகவல்(உள்ளீடு_மதிப்பு.열린파일.தரவு.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer அடைவு : 번호들) {
            서술자 உள்ளீடு_மதிப்பு = 서술자들.get(அடைவு);
            if (உள்ளீடு_மதிப்பு != null && உள்ளீடு_மதிப்பு.실행시닫기) {
                மூடு(அடைவு.intValue());
            }
        }
    }

    public boolean தகவல்_தொழில்நுட்பம்_திற(int அடைவு) {
        return 서술자들.containsKey(Integer.valueOf(அடைவு));
    }

    public 파일서술자표 복제() {
        파일서술자표 அளவிடக்கூடியது = new 파일서술자표(கோப்பு_முறைமை);
        for (Map.Entry<Integer, 서술자> உள்ளீடு_மதிப்பு : 서술자들.entrySet()) {
            உள்ளீடு_மதிப்பு.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(உள்ளீடு_மதிப்பு.getValue().열린파일);
            새서술자.실행시닫기 = உள்ளீடு_மதிப்பு.getValue().실행시닫기;
            அளவிடக்கூடியது.서술자들.put(உள்ளீடு_மதிப்பு.getKey(), 새서술자);
        }
        return அளவிடக்கூடியது;
    }

    private int வெறுமை_அடைவு(int 최소번호) {
        for (int அடைவு = Math.max(0, 최소번호); அடைவு < 최대서술자; அடைவு++) {
            if (!서술자들.containsKey(Integer.valueOf(அடைவு))) {
                return அடைவு;
            }
        }
        return -1;
    }
}
