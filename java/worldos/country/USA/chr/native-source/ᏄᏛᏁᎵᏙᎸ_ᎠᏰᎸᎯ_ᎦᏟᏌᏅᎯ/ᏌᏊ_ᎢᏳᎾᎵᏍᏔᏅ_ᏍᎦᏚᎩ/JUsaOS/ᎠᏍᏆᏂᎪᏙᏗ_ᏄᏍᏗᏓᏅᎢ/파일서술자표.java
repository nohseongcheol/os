// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ᎠᏍᏆᏂᎪᏙᏗ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ) {
        this.ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ = ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ;
    }

    public int ᎯᏍᏚᎢ(String ᏚᏙᎥᎢ) {
        ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ.열린파일 열린파일 = ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ.ᎯᏍᏚᎢ(ᏚᏙᎥᎢ);
        if (열린파일 == null) {
            return -2;
        }
        int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 빈번호(3);
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ), new 서술자(열린파일));
        return ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ;
    }

    public int 읽기(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, byte[] 받을곳, int ᎢᎩᏓ) {
        서술자 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = 서술자들.get(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ));
        if (Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ == null) {
            return -9;
        }
        if (ᎢᎩᏓ < 0 || ᎢᎩᏓ > 받을곳.length) {
            return -22;
        }
        int 남음 = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.ᎦᏟᏌᏅᎯ.length - Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.위치;
        int 읽을크기 = Math.min(ᎢᎩᏓ, Math.max(남음, 0));
        System.arraycopy(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.ᎦᏟᏌᏅᎯ, Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.위치, 받을곳, 0, 읽을크기);
        Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, int 거리, int 기준) {
        서술자 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = 서술자들.get(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ));
        if (Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ == null) {
            return -9;
        }
        int ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ;
        if (기준 == 0) {
            ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ = 0;
        } else if (기준 == 1) {
            ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.위치;
        } else if (기준 == 2) {
            ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.ᎦᏟᏌᏅᎯ.length;
        } else {
            return -22;
        }
        int 새위치 = ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ + 거리;
        if (새위치 < 0) {
            return -22;
        }
        Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int ᎯᏍᏚᎲᎦ(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        서술자 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = 서술자들.remove(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ));
        if (Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ == null) {
            return -9;
        }
        Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, int 최소번호) {
        서술자 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = 서술자들.get(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ));
        if (Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ == null) {
            return -9;
        }
        int 새번호 = 빈번호(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일));
        return 새번호;
    }

    public int 지정복제(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, int 새번호) {
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ)) ? ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            ᎯᏍᏚᎲᎦ(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, boolean ᏧᎬᏩᎶᏗᏯ) {
        서술자 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = 서술자들.get(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ));
        if (Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ == null) {
            return -9;
        }
        Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.실행시닫기 = ᏧᎬᏩᎶᏗᏯ;
        return 0;
    }

    public int 실행시닫기값(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        서술자 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = 서술자들.get(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ));
        if (Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ == null) {
            return -9;
        }
        return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.실행시닫기 ? 1 : 0;
    }

    public ᎠᏍᏆᏂᎪᏙᏗ_ᎧᏃᎮᏢᎥᏍᎩ msinfo32_exe(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ >= 0 && ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ <= 2) {
            return new ᎠᏍᏆᏂᎪᏙᏗ_ᎧᏃᎮᏢᎥᏍᎩ(0, 0020666);
        }
        서술자 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = 서술자들.get(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ));
        if (Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ == null) {
            return null;
        }
        return new ᎠᏍᏆᏂᎪᏙᏗ_ᎧᏃᎮᏢᎥᏍᎩ(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.열린파일.ᎦᏟᏌᏅᎯ.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ : 번호들) {
            서술자 Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = 서술자들.get(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
            if (Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ != null && Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.실행시닫기) {
                ᎯᏍᏚᎲᎦ(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ.intValue());
            }
        }
    }

    public boolean 열려있음(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        return 서술자들.containsKey(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ);
        for (Map.Entry<Integer, 서술자> Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ : 서술자들.entrySet()) {
            Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.getValue().열린파일);
            새서술자.실행시닫기 = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.getValue().실행시닫기;
            결과.서술자들.put(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.getKey(), 새서술자);
        }
        return 결과;
    }

    private int 빈번호(int 최소번호) {
        for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = Math.max(0, 최소번호); ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 최대서술자; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
            if (!서술자들.containsKey(Integer.valueOf(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ))) {
                return ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ;
            }
        }
        return -1;
    }
}
