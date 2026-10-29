// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Faịlụ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sistèm_ọbọakwụkwo.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sistèm_ọbọakwụkwo.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistèm_ọbọakwụkwo sistèm_ọbọakwụkwo;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sistèm_ọbọakwụkwo sistèm_ọbọakwụkwo) {
        this.sistèm_ọbọakwụkwo = sistèm_ọbọakwụkwo;
    }

    public int Mepee(String Aha) {
        sistèm_ọbọakwụkwo.열린파일 열린파일 = sistèm_ọbọakwụkwo.Mepee(Aha);
        if (열린파일 == null) {
            return -2;
        }
        int indèks = oghere_indèks(3);
        if (indèks < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(indèks), new 서술자(열린파일));
        return indèks;
    }

    public int Wepụta_ọzi(int indèks, byte[] 받을곳, int Ụhara) {
        서술자 ndebà_valuu = 서술자들.get(Integer.valueOf(indèks));
        if (ndebà_valuu == null) {
            return -9;
        }
        if (Ụhara < 0 || Ụhara > 받을곳.length) {
            return -22;
        }
        int 남음 = ndebà_valuu.열린파일.datà.length - ndebà_valuu.열린파일.위치;
        int 읽을크기 = Math.min(Ụhara, Math.max(남음, 0));
        System.arraycopy(ndebà_valuu.열린파일.datà, ndebà_valuu.열린파일.위치, 받을곳, 0, 읽을크기);
        ndebà_valuu.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int indèks, int 거리, int 기준) {
        서술자 ndebà_valuu = 서술자들.get(Integer.valueOf(indèks));
        if (ndebà_valuu == null) {
            return -9;
        }
        int Bakgraụnd_valuu;
        if (기준 == 0) {
            Bakgraụnd_valuu = 0;
        } else if (기준 == 1) {
            Bakgraụnd_valuu = ndebà_valuu.열린파일.위치;
        } else if (기준 == 2) {
            Bakgraụnd_valuu = ndebà_valuu.열린파일.datà.length;
        } else {
            return -22;
        }
        int 새위치 = Bakgraụnd_valuu + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ndebà_valuu.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int Mechie(int indèks) {
        서술자 ndebà_valuu = 서술자들.remove(Integer.valueOf(indèks));
        if (ndebà_valuu == null) {
            return -9;
        }
        ndebà_valuu.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int indèks, int 최소번호) {
        서술자 ndebà_valuu = 서술자들.get(Integer.valueOf(indèks));
        if (ndebà_valuu == null) {
            return -9;
        }
        int 새번호 = oghere_indèks(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ndebà_valuu.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ndebà_valuu.열린파일));
        return 새번호;
    }

    public int 지정복제(int indèks, int 새번호) {
        if (indèks == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(indèks)) ? indèks : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(indèks));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Mechie(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int indèks, boolean valuu) {
        서술자 ndebà_valuu = 서술자들.get(Integer.valueOf(indèks));
        if (ndebà_valuu == null) {
            return -9;
        }
        ndebà_valuu.실행시닫기 = valuu;
        return 0;
    }

    public int 실행시닫기값(int indèks) {
        서술자 ndebà_valuu = 서술자들.get(Integer.valueOf(indèks));
        if (ndebà_valuu == null) {
            return -9;
        }
        return ndebà_valuu.실행시닫기 ? 1 : 0;
    }

    public ọbọakwụkwọ_ozi Ozi_Sistèm(int indèks) {
        if (indèks >= 0 && indèks <= 2) {
            return new ọbọakwụkwọ_ozi(0, 0020666);
        }
        서술자 ndebà_valuu = 서술자들.get(Integer.valueOf(indèks));
        if (ndebà_valuu == null) {
            return null;
        }
        return new ọbọakwụkwọ_ozi(ndebà_valuu.열린파일.datà.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer indèks : 번호들) {
            서술자 ndebà_valuu = 서술자들.get(indèks);
            if (ndebà_valuu != null && ndebà_valuu.실행시닫기) {
                Mechie(indèks.intValue());
            }
        }
    }

    public boolean 열려있음(int indèks) {
        return 서술자들.containsKey(Integer.valueOf(indèks));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(sistèm_ọbọakwụkwo);
        for (Map.Entry<Integer, 서술자> ndebà_valuu : 서술자들.entrySet()) {
            ndebà_valuu.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ndebà_valuu.getValue().열린파일);
            새서술자.실행시닫기 = ndebà_valuu.getValue().실행시닫기;
            결과.서술자들.put(ndebà_valuu.getKey(), 새서술자);
        }
        return 결과;
    }

    private int oghere_indèks(int 최소번호) {
        for (int indèks = Math.max(0, 최소번호); indèks < 최대서술자; indèks++) {
            if (!서술자들.containsKey(Integer.valueOf(indèks))) {
                return indèks;
            }
        }
        return -1;
    }
}
