// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 సమలేఖనం_చెయ్యి_మూల్యం కేటాయించు_నిల్వ, విడుదల_నిల్వ, 병합을 담당한다. */
public final class మెమరీ_కార్యనిర్వాహి {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public మెమరీ_కార్యనిర్వాహి(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int కేటాయించు_నిల్వ(int పరిమాణం) {
        return 정렬할당(పరిమాణం, 1);
    }

    public synchronized int 정렬할당(int పరిమాణం, int సమలేఖనం_చెయ్యి_మూల్యం) {
        if (పరిమాణం <= 0 || సమలేఖనం_చెయ్యి_మూల్యం <= 0 || (సమలేఖనం_చెయ్యి_మూల్యం & (సమలేఖనం_చెయ్యి_మూల్యం - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ప్రవేశం_మూల్యం : 빈영역.entrySet()) {
            int నడుపుము = ప్రవేశం_మూల్యం.getKey().intValue();
            int 영역크기 = ప్రవేశం_మూల్యం.getValue().intValue();
            int 정렬시작 = (నడుపుము + సమలేఖనం_చెయ్యి_మూల్యం - 1) & -సమలేఖనం_చెయ్యి_మూల్యం;
            int ముందు_మూల్యం_పరిమాణం_మార్చు = 정렬시작 - నడుపుము;
            int 끝크기 = 영역크기 - ముందు_మూల్యం_పరిమాణం_మార్చు - పరిమాణం;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(నడుపుము));
            if (ముందు_మూల్యం_పరిమాణం_మార్చు > 0) {
                빈영역.put(Integer.valueOf(నడుపుము), Integer.valueOf(ముందు_మూల్యం_పరిమాణం_మార్చు));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + పరిమాణం), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(పరిమాణం));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + పరిమాణం, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void విడుదల_నిల్వ(int ఇమెయిల్) {
        Integer పరిమాణం_మార్చు_అంశం = 사용영역.remove(Integer.valueOf(ఇమెయిల్));
        if (పరిమాణం_మార్చు_అంశం == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int నడుపుము = ఇమెయిల్;
        int పరిమాణం = పరిమాణం_మార్చు_అంశం.intValue();
        Map.Entry<Integer, Integer> ముందు_మూల్యం = 빈영역.lowerEntry(Integer.valueOf(నడుపుము));
        if (ముందు_మూల్యం != null && ముందు_మూల్యం.getKey().intValue() + ముందు_మూల్యం.getValue().intValue() == నడుపుము) {
            నడుపుము = ముందు_మూల్యం.getKey().intValue();
            పరిమాణం += ముందు_మూల్యం.getValue().intValue();
            빈영역.remove(ముందు_మూల్యం.getKey());
        }
        Map.Entry<Integer, Integer> వెనుకకు_మూల్యం = 빈영역.ceilingEntry(Integer.valueOf(నడుపుము));
        if (వెనుకకు_మూల్యం != null && నడుపుము + పరిమాణం == వెనుకకు_మూల్యం.getKey().intValue()) {
            పరిమాణం += వెనుకకు_మూల్యం.getValue().intValue();
            빈영역.remove(వెనుకకు_మూల్యం.getKey());
        }
        빈영역.put(Integer.valueOf(నడుపుము), Integer.valueOf(పరిమాణం));
    }

    public synchronized byte 바이트읽기(int ఇమెయిల్) {
        범위확인(ఇమెయిల్, 1);
        return 기억공간[ఇమెయిల్];
    }

    public synchronized void వ్రాయి_బైట్_మూల్యం(int ఇమెయిల్, byte మూల్యం) {
        범위확인(ఇమెయిల్, 1);
        기억공간[ఇమెయిల్] = మూల్యం;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer పరిమాణం : 사용영역.values()) {
            합계 += పరిమాణం.intValue();
        }
        return 합계;
    }

    private void 범위확인(int ఇమెయిల్, int పరిమాణం) {
        if (ఇమెయిల్ < 0 || పరిమాణం < 0 || ఇమెయిల్ > 기억공간.length - పరిమాణం) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

