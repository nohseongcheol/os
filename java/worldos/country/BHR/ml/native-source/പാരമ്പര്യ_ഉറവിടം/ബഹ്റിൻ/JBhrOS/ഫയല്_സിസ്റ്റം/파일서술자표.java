// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ബഹ്റിൻ.JBhrOS.ഫയല്_സിസ്റ്റം;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ഫയല് 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ഫയല്_സിസ്റ്റം.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ഫയല്_സിസ്റ്റം.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ഫയല്_സിസ്റ്റം ഫയല്_സിസ്റ്റം;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ഫയല്_സിസ്റ്റം ഫയല്_സിസ്റ്റം) {
        this.ഫയല്_സിസ്റ്റം = ഫയല്_സിസ്റ്റം;
    }

    public int തുറക്കുക(String പേരു്) {
        ഫയല്_സിസ്റ്റം.열린파일 열린파일 = ഫയല്_സിസ്റ്റം.തുറക്കുക(പേരു്);
        if (열린파일 == null) {
            return -2;
        }
        int സൂചിക = ശൂന്യം_സൂചിക(3);
        if (സൂചിക < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(സൂചിക), new 서술자(열린파일));
        return സൂചിക;
    }

    public int വായന(int സൂചിക, byte[] 받을곳, int വലിപ്പം) {
        서술자 എന്_ട്രി_മൂല്യം = 서술자들.get(Integer.valueOf(സൂചിക));
        if (എന്_ട്രി_മൂല്യം == null) {
            return -9;
        }
        if (വലിപ്പം < 0 || വലിപ്പം > 받을곳.length) {
            return -22;
        }
        int 남음 = എന്_ട്രി_മൂല്യം.열린파일.ഡാറ്റാ.length - എന്_ട്രി_മൂല്യം.열린파일.സ്ഥാനം;
        int 읽을크기 = Math.min(വലിപ്പം, Math.max(남음, 0));
        System.arraycopy(എന്_ട്രി_മൂല്യം.열린파일.ഡാറ്റാ, എന്_ട്രി_മൂല്യം.열린파일.സ്ഥാനം, 받을곳, 0, 읽을크기);
        എന്_ട്രി_മൂല്യം.열린파일.സ്ഥാനം += 읽을크기;
        return 읽을크기;
    }

    public int നീക്കുക_പദവി(int സൂചിക, int 거리, int പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം) {
        서술자 എന്_ട്രി_മൂല്യം = 서술자들.get(Integer.valueOf(സൂചിക));
        if (എന്_ട്രി_മൂല്യം == null) {
            return -9;
        }
        int నేపథ్యం_മൂല്യം;
        if (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം == 0) {
            నేపథ్యం_മൂല്യം = 0;
        } else if (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം == 1) {
            నేపథ్యం_മൂല്യം = എന്_ട്രി_മൂല്യം.열린파일.സ്ഥാനം;
        } else if (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം == 2) {
            నేపథ్యం_മൂല്യം = എന്_ട്രി_മൂല്യം.열린파일.ഡാറ്റാ.length;
        } else {
            return -22;
        }
        int 새위치 = నేపథ్యం_മൂല്യം + 거리;
        if (새위치 < 0) {
            return -22;
        }
        എന്_ട്രി_മൂല്യം.열린파일.സ്ഥാനം = 새위치;
        return 새위치;
    }

    public int അടയ്ക്കു(int സൂചിക) {
        서술자 എന്_ട്രി_മൂല്യം = 서술자들.remove(Integer.valueOf(സൂചിക));
        if (എന്_ട്രി_മൂല്യം == null) {
            return -9;
        }
        എന്_ട്രി_മൂല്യം.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int സൂചിക, int 최소번호) {
        서술자 എന്_ട്രി_മൂല്യം = 서술자들.get(Integer.valueOf(സൂചിക));
        if (എന്_ട്രി_മൂല്യം == null) {
            return -9;
        }
        int 새번호 = ശൂന്യം_സൂചിക(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        എന്_ട്രി_മൂല്യം.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(എന്_ട്രി_മൂല്യം.열린파일));
        return 새번호;
    }

    public int 지정복제(int സൂചിക, int 새번호) {
        if (സൂചിക == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(സൂചിക)) ? സൂചിക : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(സൂചിക));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            അടയ്ക്കു(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int സൂചിക, boolean മൂല്യം) {
        서술자 എന്_ട്രി_മൂല്യം = 서술자들.get(Integer.valueOf(സൂചിക));
        if (എന്_ട്രി_മൂല്യം == null) {
            return -9;
        }
        എന്_ട്രി_മൂല്യം.실행시닫기 = മൂല്യം;
        return 0;
    }

    public int 실행시닫기값(int സൂചിക) {
        서술자 എന്_ട്രി_മൂല്യം = 서술자들.get(Integer.valueOf(സൂചിക));
        if (എന്_ട്രി_മൂല്യം == null) {
            return -9;
        }
        return എന്_ട്രി_മൂല്യം.실행시닫기 ? 1 : 0;
    }

    public ഫയല്_വിവരം സിസ്റ്റം_വിവരങ്ങള്(int സൂചിക) {
        if (സൂചിക >= 0 && സൂചിക <= 2) {
            return new ഫയല്_വിവരം(0, 0020666);
        }
        서술자 എന്_ട്രി_മൂല്യം = 서술자들.get(Integer.valueOf(സൂചിക));
        if (എന്_ട്രി_മൂല്യം == null) {
            return null;
        }
        return new ഫയല്_വിവരം(എന്_ട്രി_മൂല്യം.열린파일.ഡാറ്റാ.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer സൂചിക : 번호들) {
            서술자 എന്_ട്രി_മൂല്യം = 서술자들.get(സൂചിക);
            if (എന്_ട്രി_മൂല്യം != null && എന്_ട്രി_മൂല്യം.실행시닫기) {
                അടയ്ക്കു(സൂചിക.intValue());
            }
        }
    }

    public boolean വിവര_സാങ്കേതികവിദ്യ_തുറക്കുക(int സൂചിക) {
        return 서술자들.containsKey(Integer.valueOf(സൂചിക));
    }

    public 파일서술자표 복제() {
        파일서술자표 അളവ് = new 파일서술자표(ഫയല്_സിസ്റ്റം);
        for (Map.Entry<Integer, 서술자> എന്_ട്രി_മൂല്യം : 서술자들.entrySet()) {
            എന്_ട്രി_മൂല്യം.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(എന്_ട്രി_മൂല്യം.getValue().열린파일);
            새서술자.실행시닫기 = എന്_ട്രി_മൂല്യം.getValue().실행시닫기;
            അളവ്.서술자들.put(എന്_ട്രി_മൂല്യം.getKey(), 새서술자);
        }
        return അളവ്;
    }

    private int ശൂന്യം_സൂചിക(int 최소번호) {
        for (int സൂചിക = Math.max(0, 최소번호); സൂചിക < 최대서술자; സൂചിക++) {
            if (!서술자들.containsKey(Integer.valueOf(സൂചിക))) {
                return സൂചിക;
            }
        }
        return -1;
    }
}
