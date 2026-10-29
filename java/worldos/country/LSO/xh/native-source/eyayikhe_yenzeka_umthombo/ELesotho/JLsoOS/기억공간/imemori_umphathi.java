// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ELesotho.JLsoOS.기억공간;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 lungelelanisa_ixabiso yabela_Ugcino, vulela_Ugcino, 병합을 담당한다. */
public final class imemori_umphathi {
    private final byte[] 기억공간;
    private final TreeMap<Integer, Integer> 빈영역 = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public imemori_umphathi(int 전체크기) {
        if (전체크기 < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        기억공간 = new byte[전체크기];
        빈영역.put(Integer.valueOf(4096), Integer.valueOf(전체크기 - 4096));
    }

    public synchronized int yabela_Ugcino(int Ubukhulu) {
        return 정렬할당(Ubukhulu, 1);
    }

    public synchronized int 정렬할당(int Ubukhulu, int lungelelanisa_ixabiso) {
        if (Ubukhulu <= 0 || lungelelanisa_ixabiso <= 0 || (lungelelanisa_ixabiso & (lungelelanisa_ixabiso - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ufako_nkcukacha_ixabiso : 빈영역.entrySet()) {
            int Phumeza = ufako_nkcukacha_ixabiso.getKey().intValue();
            int 영역크기 = ufako_nkcukacha_ixabiso.getValue().intValue();
            int 정렬시작 = (Phumeza + lungelelanisa_ixabiso - 1) & -lungelelanisa_ixabiso;
            int 앞크기 = 정렬시작 - Phumeza;
            int 끝크기 = 영역크기 - 앞크기 - Ubukhulu;
            if (끝크기 < 0) {
                continue;
            }
            빈영역.remove(Integer.valueOf(Phumeza));
            if (앞크기 > 0) {
                빈영역.put(Integer.valueOf(Phumeza), Integer.valueOf(앞크기));
            }
            if (끝크기 > 0) {
                빈영역.put(Integer.valueOf(정렬시작 + Ubukhulu), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(Ubukhulu));
            Arrays.fill(기억공간, 정렬시작, 정렬시작 + Ubukhulu, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void vulela_Ugcino(int idilesi) {
        Integer isayizi_into = 사용영역.remove(Integer.valueOf(idilesi));
        if (isayizi_into == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int Phumeza = idilesi;
        int Ubukhulu = isayizi_into.intValue();
        Map.Entry<Integer, Integer> 앞 = 빈영역.lowerEntry(Integer.valueOf(Phumeza));
        if (앞 != null && 앞.getKey().intValue() + 앞.getValue().intValue() == Phumeza) {
            Phumeza = 앞.getKey().intValue();
            Ubukhulu += 앞.getValue().intValue();
            빈영역.remove(앞.getKey());
        }
        Map.Entry<Integer, Integer> Emva_ixabiso = 빈영역.ceilingEntry(Integer.valueOf(Phumeza));
        if (Emva_ixabiso != null && Phumeza + Ubukhulu == Emva_ixabiso.getKey().intValue()) {
            Ubukhulu += Emva_ixabiso.getValue().intValue();
            빈영역.remove(Emva_ixabiso.getKey());
        }
        빈영역.put(Integer.valueOf(Phumeza), Integer.valueOf(Ubukhulu));
    }

    public synchronized byte 바이트읽기(int idilesi) {
        범위확인(idilesi, 1);
        return 기억공간[idilesi];
    }

    public synchronized void bhala_ibhayithi_ixabiso(int idilesi, byte ixabiso) {
        범위확인(idilesi, 1);
        기억공간[idilesi] = ixabiso;
    }

    public synchronized int 전체크기() {
        return 기억공간.length;
    }

    public synchronized int 사용크기() {
        int 합계 = 0;
        for (Integer Ubukhulu : 사용영역.values()) {
            합계 += Ubukhulu.intValue();
        }
        return 합계;
    }

    private void 범위확인(int idilesi, int Ubukhulu) {
        if (idilesi < 0 || Ubukhulu < 0 || idilesi > 기억공간.length - Ubukhulu) {
            throw new IndexOutOfBoundsException("기억공간 범위를 벗어났습니다.");
        }
    }
}

