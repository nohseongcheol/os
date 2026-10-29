// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.זיכרון_אזור;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** 물리 기억공간의 ליישר_ערך הקצה_אחסון, לשחרר_אחסון, 병합을 담당한다. */
public final class זיכרון_מנהל {
    private final byte[] זיכרון_אזור;
    private final TreeMap<Integer, Integer> ריק_אזור = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> 사용영역 = new TreeMap<Integer, Integer>();

    public זיכרון_מנהל(int סך_הכל_גודל) {
        if (סך_הכל_גודל < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        זיכרון_אזור = new byte[סך_הכל_גודל];
        ריק_אזור.put(Integer.valueOf(4096), Integer.valueOf(סך_הכל_גודל - 4096));
    }

    public synchronized int הקצה_אחסון(int גודל) {
        return 정렬할당(גודל, 1);
    }

    public synchronized int 정렬할당(int גודל, int ליישר_ערך) {
        if (גודל <= 0 || ליישר_ערך <= 0 || (ליישר_ערך & (ליישר_ערך - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> ערך_ערך : ריק_אזור.entrySet()) {
            int הפעלה = ערך_ערך.getKey().intValue();
            int אזור_גודל = ערך_ערך.getValue().intValue();
            int 정렬시작 = (הפעלה + ליישר_ערך - 1) & -ליישר_ערך;
            int מצלמה_קדמית_ערך_גודל = 정렬시작 - הפעלה;
            int 끝크기 = אזור_גודל - מצלמה_קדמית_ערך_גודל - גודל;
            if (끝크기 < 0) {
                continue;
            }
            ריק_אזור.remove(Integer.valueOf(הפעלה));
            if (מצלמה_קדמית_ערך_גודל > 0) {
                ריק_אזור.put(Integer.valueOf(הפעלה), Integer.valueOf(מצלמה_קדמית_ערך_גודל));
            }
            if (끝크기 > 0) {
                ריק_אזור.put(Integer.valueOf(정렬시작 + גודל), Integer.valueOf(끝크기));
            }
            사용영역.put(Integer.valueOf(정렬시작), Integer.valueOf(גודל));
            Arrays.fill(זיכרון_אזור, 정렬시작, 정렬시작 + גודל, (byte) 0);
            return 정렬시작;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void לשחרר_אחסון(int למען) {
        Integer גודל_אובייקט = 사용영역.remove(Integer.valueOf(למען));
        if (גודל_אובייקט == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int הפעלה = למען;
        int גודל = גודל_אובייקט.intValue();
        Map.Entry<Integer, Integer> מצלמה_קדמית_ערך_ec1a6b96 = ריק_אזור.lowerEntry(Integer.valueOf(הפעלה));
        if (מצלמה_קדמית_ערך_ec1a6b96 != null && מצלמה_קדמית_ערך_ec1a6b96.getKey().intValue() + מצלמה_קדמית_ערך_ec1a6b96.getValue().intValue() == הפעלה) {
            הפעלה = מצלמה_קדמית_ערך_ec1a6b96.getKey().intValue();
            גודל += מצלמה_קדמית_ערך_ec1a6b96.getValue().intValue();
            ריק_אזור.remove(מצלמה_קדמית_ערך_ec1a6b96.getKey());
        }
        Map.Entry<Integer, Integer> הקודם_ערך = ריק_אזור.ceilingEntry(Integer.valueOf(הפעלה));
        if (הקודם_ערך != null && הפעלה + גודל == הקודם_ערך.getKey().intValue()) {
            גודל += הקודם_ערך.getValue().intValue();
            ריק_אזור.remove(הקודם_ערך.getKey());
        }
        ריק_אזור.put(Integer.valueOf(הפעלה), Integer.valueOf(גודל));
    }

    public synchronized byte 바이트읽기(int למען) {
        שיק_טווח(למען, 1);
        return זיכרון_אזור[למען];
    }

    public synchronized void כתיבה_בית_ערך(int למען, byte ערך) {
        שיק_טווח(למען, 1);
        זיכרון_אזור[למען] = ערך;
    }

    public synchronized int סך_הכל_גודל() {
        return זיכרון_אזור.length;
    }

    public synchronized int 사용크기() {
        int סך_הכל_ערך = 0;
        for (Integer גודל : 사용영역.values()) {
            סך_הכל_ערך += גודל.intValue();
        }
        return סך_הכל_ערך;
    }

    private void שיק_טווח(int למען, int גודל) {
        if (למען < 0 || גודל < 0 || למען > זיכרון_אזור.length - גודל) {
            throw new IndexOutOfBoundsException("זיכרון_אזור 범위를 벗어났습니다.");
        }
    }
}

