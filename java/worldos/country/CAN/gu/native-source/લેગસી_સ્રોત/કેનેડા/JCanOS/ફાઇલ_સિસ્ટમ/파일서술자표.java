// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેનેડા.JCanOS.ફાઇલ_સિસ્ટમ;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ફાઈલ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ફાઇલ_સિસ્ટમ.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ફાઇલ_સિસ્ટમ.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ફાઇલ_સિસ્ટમ ફાઇલ_સિસ્ટમ;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ફાઇલ_સિસ્ટમ ફાઇલ_સિસ્ટમ) {
        this.ફાઇલ_સિસ્ટમ = ફાઇલ_સિસ્ટમ;
    }

    public int ખોલો(String નામ) {
        ફાઇલ_સિસ્ટમ.열린파일 열린파일 = ફાઇલ_સિસ્ટમ.ખોલો(નામ);
        if (열린파일 == null) {
            return -2;
        }
        int અનુક્રમણિકા = ખાલી_અનુક્રમણિકા(3);
        if (અનુક્રમણિકા < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(અનુક્રમણિકા), new 서술자(열린파일));
        return અનુક્રમણિકા;
    }

    public int વાંચો(int અનુક્રમણિકા, byte[] 받을곳, int માપ) {
        서술자 પ્રવેશ_મૂલ્ય = 서술자들.get(Integer.valueOf(અનુક્રમણિકા));
        if (પ્રવેશ_મૂલ્ય == null) {
            return -9;
        }
        if (માપ < 0 || માપ > 받을곳.length) {
            return -22;
        }
        int 남음 = પ્રવેશ_મૂલ્ય.열린파일.ડેટા.length - પ્રવેશ_મૂલ્ય.열린파일.સ્થાન;
        int 읽을크기 = Math.min(માપ, Math.max(남음, 0));
        System.arraycopy(પ્રવેશ_મૂલ્ય.열린파일.ડેટા, પ્રવેશ_મૂલ્ય.열린파일.સ્થાન, 받을곳, 0, 읽을크기);
        પ્રવેશ_મૂલ્ય.열린파일.સ્થાન += 읽을크기;
        return 읽을크기;
    }

    public int ખસેડવું_સ્થિતિ(int અનુક્રમણિકા, int 거리, int પ્રોજેક્ટ_રૂટ) {
        서술자 પ્રવેશ_મૂલ્ય = 서술자들.get(Integer.valueOf(અનુક્રમણિકા));
        if (પ્રવેશ_મૂલ્ય == null) {
            return -9;
        }
        int વૉલપેપર_મૂલ્ય;
        if (પ્રોજેક્ટ_રૂટ == 0) {
            વૉલપેપર_મૂલ્ય = 0;
        } else if (પ્રોજેક્ટ_રૂટ == 1) {
            વૉલપેપર_મૂલ્ય = પ્રવેશ_મૂલ્ય.열린파일.સ્થાન;
        } else if (પ્રોજેક્ટ_રૂટ == 2) {
            વૉલપેપર_મૂલ્ય = પ્રવેશ_મૂલ્ય.열린파일.ડેટા.length;
        } else {
            return -22;
        }
        int 새위치 = વૉલપેપર_મૂલ્ય + 거리;
        if (새위치 < 0) {
            return -22;
        }
        પ્રવેશ_મૂલ્ય.열린파일.સ્થાન = 새위치;
        return 새위치;
    }

    public int બંધ_કરો(int અનુક્રમણિકા) {
        서술자 પ્રવેશ_મૂલ્ય = 서술자들.remove(Integer.valueOf(અનુક્રમણિકા));
        if (પ્રવેશ_મૂલ્ય == null) {
            return -9;
        }
        પ્રવેશ_મૂલ્ય.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int અનુક્રમણિકા, int 최소번호) {
        서술자 પ્રવેશ_મૂલ્ય = 서술자들.get(Integer.valueOf(અનુક્રમણિકા));
        if (પ્રવેશ_મૂલ્ય == null) {
            return -9;
        }
        int 새번호 = ખાલી_અનુક્રમણિકા(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        પ્રવેશ_મૂલ્ય.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(પ્રવેશ_મૂલ્ય.열린파일));
        return 새번호;
    }

    public int 지정복제(int અનુક્રમણિકા, int 새번호) {
        if (અનુક્રમણિકા == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(અનુક્રમણિકા)) ? અનુક્રમણિકા : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(અનુક્રમણિકા));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            બંધ_કરો(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int અનુક્રમણિકા, boolean મૂલ્ય) {
        서술자 પ્રવેશ_મૂલ્ય = 서술자들.get(Integer.valueOf(અનુક્રમણિકા));
        if (પ્રવેશ_મૂલ્ય == null) {
            return -9;
        }
        પ્રવેશ_મૂલ્ય.실행시닫기 = મૂલ્ય;
        return 0;
    }

    public int 실행시닫기값(int અનુક્રમણિકા) {
        서술자 પ્રવેશ_મૂલ્ય = 서술자들.get(Integer.valueOf(અનુક્રમણિકા));
        if (પ્રવેશ_મૂલ્ય == null) {
            return -9;
        }
        return પ્રવેશ_મૂલ્ય.실행시닫기 ? 1 : 0;
    }

    public ફાઇલ_માહિતી સિસ્ટમ_માહિતી(int અનુક્રમણિકા) {
        if (અનુક્રમણિકા >= 0 && અનુક્રમણિકા <= 2) {
            return new ફાઇલ_માહિતી(0, 0020666);
        }
        서술자 પ્રવેશ_મૂલ્ય = 서술자들.get(Integer.valueOf(અનુક્રમણિકા));
        if (પ્રવેશ_મૂલ્ય == null) {
            return null;
        }
        return new ફાઇલ_માહિતી(પ્રવેશ_મૂલ્ય.열린파일.ડેટા.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer અનુક્રમણિકા : 번호들) {
            서술자 પ્રવેશ_મૂલ્ય = 서술자들.get(અનુક્રમણિકા);
            if (પ્રવેશ_મૂલ્ય != null && પ્રવેશ_મૂલ્ય.실행시닫기) {
                બંધ_કરો(અનુક્રમણિકા.intValue());
            }
        }
    }

    public boolean ઇન્ટરમિટેંટ_બનાવો(int અનુક્રમણિકા) {
        return 서술자들.containsKey(Integer.valueOf(અનુક્રમણિકા));
    }

    public 파일서술자표 복제() {
        파일서술자표 પરિમાણ = new 파일서술자표(ફાઇલ_સિસ્ટમ);
        for (Map.Entry<Integer, 서술자> પ્રવેશ_મૂલ્ય : 서술자들.entrySet()) {
            પ્રવેશ_મૂલ્ય.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(પ્રવેશ_મૂલ્ય.getValue().열린파일);
            새서술자.실행시닫기 = પ્રવેશ_મૂલ્ય.getValue().실행시닫기;
            પરિમાણ.서술자들.put(પ્રવેશ_મૂલ્ય.getKey(), 새서술자);
        }
        return પરિમાણ;
    }

    private int ખાલી_અનુક્રમણિકા(int 최소번호) {
        for (int અનુક્રમણિકા = Math.max(0, 최소번호); અનુક્રમણિકા < 최대서술자; અનુક્રમણિકા++) {
            if (!서술자들.containsKey(Integer.valueOf(અનુક્રમણિકા))) {
                return અનુક્રમણિકા;
            }
        }
        return -1;
    }
}
