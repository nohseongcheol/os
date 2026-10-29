// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.ఫైల్_వ్యవస్థ;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 దస్త్రం 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ఫైల్_వ్యవస్థ.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ఫైల్_వ్యవస్థ.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ఫైల్_వ్యవస్థ ఫైల్_వ్యవస్థ;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ఫైల్_వ్యవస్థ ఫైల్_వ్యవస్థ) {
        this.ఫైల్_వ్యవస్థ = ఫైల్_వ్యవస్థ;
    }

    public int తెరువు(String పేరు) {
        ఫైల్_వ్యవస్థ.열린파일 열린파일 = ఫైల్_వ్యవస్థ.తెరువు(పేరు);
        if (열린파일 == null) {
            return -2;
        }
        int సూచీ = ఖాళీ_సూచీ(3);
        if (సూచీ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(సూచీ), new 서술자(열린파일));
        return సూచీ;
    }

    public int చదువు(int సూచీ, byte[] 받을곳, int పరిమాణం) {
        서술자 ప్రవేశం_మూల్యం = 서술자들.get(Integer.valueOf(సూచీ));
        if (ప్రవేశం_మూల్యం == null) {
            return -9;
        }
        if (పరిమాణం < 0 || పరిమాణం > 받을곳.length) {
            return -22;
        }
        int 남음 = ప్రవేశం_మూల్యం.열린파일.డేటా.length - ప్రవేశం_మూల్యం.열린파일.స్థానము;
        int 읽을크기 = Math.min(పరిమాణం, Math.max(남음, 0));
        System.arraycopy(ప్రవేశం_మూల్యం.열린파일.డేటా, ప్రవేశం_మూల్యం.열린파일.స్థానము, 받을곳, 0, 읽을크기);
        ప్రవేశం_మూల్యం.열린파일.స్థానము += 읽을크기;
        return 읽을크기;
    }

    public int తరలించు_స్థాయి(int సూచీ, int 거리, int ప్రొజెక్ట్_మూలం) {
        서술자 ప్రవేశం_మూల్యం = 서술자들.get(Integer.valueOf(సూచీ));
        if (ప్రవేశం_మూల్యం == null) {
            return -9;
        }
        int నేపథ్యం_మూల్యం;
        if (ప్రొజెక్ట్_మూలం == 0) {
            నేపథ్యం_మూల్యం = 0;
        } else if (ప్రొజెక్ట్_మూలం == 1) {
            నేపథ్యం_మూల్యం = ప్రవేశం_మూల్యం.열린파일.స్థానము;
        } else if (ప్రొజెక్ట్_మూలం == 2) {
            నేపథ్యం_మూల్యం = ప్రవేశం_మూల్యం.열린파일.డేటా.length;
        } else {
            return -22;
        }
        int 새위치 = నేపథ్యం_మూల్యం + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ప్రవేశం_మూల్యం.열린파일.స్థానము = 새위치;
        return 새위치;
    }

    public int మూసివేయి(int సూచీ) {
        서술자 ప్రవేశం_మూల్యం = 서술자들.remove(Integer.valueOf(సూచీ));
        if (ప్రవేశం_మూల్యం == null) {
            return -9;
        }
        ప్రవేశం_మూల్యం.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int సూచీ, int 최소번호) {
        서술자 ప్రవేశం_మూల్యం = 서술자들.get(Integer.valueOf(సూచీ));
        if (ప్రవేశం_మూల్యం == null) {
            return -9;
        }
        int 새번호 = ఖాళీ_సూచీ(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ప్రవేశం_మూల్యం.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ప్రవేశం_మూల్యం.열린파일));
        return 새번호;
    }

    public int 지정복제(int సూచీ, int 새번호) {
        if (సూచీ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(సూచీ)) ? సూచీ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(సూచీ));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            మూసివేయి(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int సూచీ, boolean మూల్యం) {
        서술자 ప్రవేశం_మూల్యం = 서술자들.get(Integer.valueOf(సూచీ));
        if (ప్రవేశం_మూల్యం == null) {
            return -9;
        }
        ప్రవేశం_మూల్యం.실행시닫기 = మూల్యం;
        return 0;
    }

    public int 실행시닫기값(int సూచీ) {
        서술자 ప్రవేశం_మూల్యం = 서술자들.get(Integer.valueOf(సూచీ));
        if (ప్రవేశం_మూల్యం == null) {
            return -9;
        }
        return ప్రవేశం_మూల్యం.실행시닫기 ? 1 : 0;
    }

    public ఫైలు_సమాచారం సిస్టమ్_సమాచారం(int సూచీ) {
        if (సూచీ >= 0 && సూచీ <= 2) {
            return new ఫైలు_సమాచారం(0, 0020666);
        }
        서술자 ప్రవేశం_మూల్యం = 서술자들.get(Integer.valueOf(సూచీ));
        if (ప్రవేశం_మూల్యం == null) {
            return null;
        }
        return new ఫైలు_సమాచారం(ప్రవేశం_మూల్యం.열린파일.డేటా.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer సూచీ : 번호들) {
            서술자 ప్రవేశం_మూల్యం = 서술자들.get(సూచీ);
            if (ప్రవేశం_మూల్యం != null && ప్రవేశం_మూల్యం.실행시닫기) {
                మూసివేయి(సూచీ.intValue());
            }
        }
    }

    public boolean సమాచార_టెక్నాలజీ_తెరువు(int సూచీ) {
        return 서술자들.containsKey(Integer.valueOf(సూచీ));
    }

    public 파일서술자표 복제() {
        파일서술자표 ప్రమాణం = new 파일서술자표(ఫైల్_వ్యవస్థ);
        for (Map.Entry<Integer, 서술자> ప్రవేశం_మూల్యం : 서술자들.entrySet()) {
            ప్రవేశం_మూల్యం.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ప్రవేశం_మూల్యం.getValue().열린파일);
            새서술자.실행시닫기 = ప్రవేశం_మూల్యం.getValue().실행시닫기;
            ప్రమాణం.서술자들.put(ప్రవేశం_మూల్యం.getKey(), 새서술자);
        }
        return ప్రమాణం;
    }

    private int ఖాళీ_సూచీ(int 최소번호) {
        for (int సూచీ = Math.max(0, 최소번호); సూచీ < 최대서술자; సూచీ++) {
            if (!서술자들.containsKey(Integer.valueOf(సూచీ))) {
                return సూచీ;
            }
        }
        return -1;
    }
}
