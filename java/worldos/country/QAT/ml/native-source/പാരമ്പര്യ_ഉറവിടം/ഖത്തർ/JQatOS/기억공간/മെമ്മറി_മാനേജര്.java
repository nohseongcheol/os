// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ഖത്തർ.JQatOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 വിന്യസിക്കുക_മൂല്യം അനുവദിക്കുക_സംഭരണം, റിലീസ്_സംഭരണം, 병합을 담당한다. */
public final class മെമ്മറി_മാനേജര് {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public മെമ്മറി_മാനേജര്(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int അനുവദിക്കുക_സംഭരണം(int വലിപ്പം) {
        return 정렬할당(വലിപ്പം, 1);
    }

    public synchronized int 정렬할당(int വലിപ്പം, int വിന്യസിക്കുക_മൂല്യം) {
        if (വലിപ്പം <= 0 || വിന്യസിക്കുക_മൂല്യം <= 0 || (വിന്യസിക്കുക_മൂല്യം & (വിന്യസിക്കുക_മൂല്യം - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> എന്_ട്രി_മൂല്യം : 빈영역.entrySet()) {
            int നടപ്പിലാക്കുക = എന്_ട്രി_മൂല്യം.getKey().intValue();
            int 영역크기 = എന്_ട്രി_മൂല്യം.getValue().intValue();
            int 정렬시작 = (നടപ്പിലാക്കുക + വിന്യസിക്കുക_മൂല്യം - 1) & -വിന്യസിക്കുക_മൂല്യം;
            int മുൻവശം_മൂല്യം_വലുപ്പം_ക്രമീകരിക്കുക = 정렬시작 - നടപ്പിലാക്കുക;
            int 끝크기 = 영역크기 - മുൻവശം_മൂല്യം_വലുപ്പം_ക്രമീകരിക്കുക - വലിപ്പം;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(നടപ്പിലാക്കുക));
            if (മുൻവശം_മൂല്യം_വലുപ്പം_ക്രമീകരിക്കുക > 0) {
                빈영역.put(Integer.valueOf(നടപ്പിലാക്കുക), Integer.valueOf(മുൻവശം_മൂല്യം_വലുപ്പം_ക്രമീകരിക്കുക));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + വലിപ്പം), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(വലിപ്പം));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + വലിപ്പം, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void റിലീസ്_സംഭരണം(int ഇമെയിൽ) {
        Integer വലുപ്പം_ക്രമീകരിക്കുക_ഓബ്ജക്റ്റ് = 사용영역.remove(Integer.valueOf(ഇമെയിൽ));
        if (വലുപ്പം_ക്രമീകരിക്കുക_ഓബ്ജക്റ്റ് == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int നടപ്പിലാക്കുക = ഇമെയിൽ;
        int വലിപ്പം = വലുപ്പം_ക്രമീകരിക്കുക_ഓബ്ജക്റ്റ്.intValue();
        Map.Entry<Integer, Integer> മുൻവശം_മൂല്യം = 빈영역.lowerEntry(Integer.valueOf(നടപ്പിലാക്കുക));
        if (മുൻവശം_മൂല്യം != null && മുൻവശം_മൂല്യം.getKey().intValue() + മുൻവശം_മൂല്യം.getValue().intValue() == നടപ്പിലാക്കുക) {
            നടപ്പിലാക്കുക = മുൻവശം_മൂല്യം.getKey().intValue();
            വലിപ്പം += മുൻവശം_മൂല്യം.getValue().intValue();
            빈영역.remove(മുൻവശം_മൂല്യം.getKey());
        }
        Map.Entry<Integer, Integer> പിന്നിലേക്ക്_മൂല്യം = 빈영역.ceilingEntry(Integer.valueOf(നടപ്പിലാക്കുക));
        if (പിന്നിലേക്ക്_മൂല്യം != null && നടപ്പിലാക്കുക + വലിപ്പം == പിന്നിലേക്ക്_മൂല്യം.getKey().intValue()) {
            വലിപ്പം += പിന്നിലേക്ക്_മൂല്യം.getValue().intValue();
            빈영역.remove(പിന്നിലേക്ക്_മൂല്യം.getKey());
        }
        빈영역.put(Integer.valueOf(നടപ്പിലാക്കുക), Integer.valueOf(വലിപ്പം));
    }

    public synchronized byte 바이트읽기(int ഇമെയിൽ) {
        범위확인(ഇമെയിൽ, 1);
        return 기억공간[ഇമെയിൽ];
    }

    public synchronized void റൈറ്റ്_ചെയ്യുക_బైట్_മൂല്യം(int ഇമെയിൽ, byte മൂല്യം) {
        범위확인(ഇമെയിൽ, 1);
        기억공간[ഇമെയിൽ] = മൂല്യം;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer വലിപ്പം : 사용영역.values()) {
            합계 += വലിപ്പം.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ഇമെയിൽ, int വലിപ്പം) {
        if (ഇമെയിൽ < 0 || വലിപ്പം < 0 || ഇമെയിൽ > 기억공간.length - വലിപ്പം) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

