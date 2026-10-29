// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.מערכת_קבצים;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian לבצע_פקודה 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class מקטע_ערך {
        private final int 종류;
        private final int דגל_ערך;
        private final int למען;
        private final int קובץ_עמדה;
        private final int גודל;

        מקטע_ערך(int 종류, int דגל_ערך, int למען, int קובץ_עמדה, int גודל) {
            this.종류 = 종류;
            this.דגל_ערך = דגל_ערך;
            this.למען = למען;
            this.קובץ_עמדה = קובץ_עמדה;
            this.גודל = גודל;
        }

        public int 종류() {
            return 종류;
        }

        public int דגל_ערך() {
            return דגל_ערך;
        }

        public int למען() {
            return למען;
        }

        public int קובץ_עמדה() {
            return קובץ_עמדה;
        }

        public int גודל() {
            return גודל;
        }
    }

    public static final class תמונה {
        private final int התחל_למען;
        private final List<מקטע_ערך> 구역들;

        תמונה(int התחל_למען, List<מקטע_ערך> 구역들) {
            this.התחל_למען = התחל_למען;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int התחל_למען() {
            return התחל_למען;
        }

        public List<מקטע_ערך> 구역들() {
            return 구역들;
        }
    }

    public תמונה 검사(byte[] נתונים) {
        if (נתונים == null || נתונים.length < 52
                || נתונים[0] != 0x7f || נתונים[1] != 'E' || נתונים[2] != 'L' || נתונים[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (נתונים[4] != 1 || נתונים[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int התחל_למען = ניתוח_מבנה_טקסט_מספר_שלם(נתונים, 24);
        int מקטע_טבלה_עמדה = ניתוח_מבנה_טקסט_מספר_שלם(נתונים, 32);
        int מקטע_ערך_גודל = 짧은정수읽기(נתונים, 46);
        int 구역수 = 짧은정수읽기(נתונים, 48);
        if (מקטע_ערך_גודל < 40 || מקטע_טבלה_עמדה < 0
                || (long) מקטע_טבלה_עמדה + (long) מקטע_ערך_גודל * 구역수 > נתונים.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<מקטע_ערך> 구역들 = new ArrayList<מקטע_ערך>();
        for (int מדד = 0; מדד < 구역수; מדד++) {
            int מיקום = מקטע_טבלה_עמדה + מדד * מקטע_ערך_גודל;
            int 종류 = ניתוח_מבנה_טקסט_מספר_שלם(נתונים, מיקום + 4);
            int דגל_ערך = ניתוח_מבנה_טקסט_מספר_שלם(נתונים, מיקום + 8);
            int למען = ניתוח_מבנה_טקסט_מספר_שלם(נתונים, מיקום + 12);
            int קובץ_עמדה = ניתוח_מבנה_טקסט_מספר_שלם(נתונים, מיקום + 16);
            int גודל = ניתוח_מבנה_טקסט_מספר_שלם(נתונים, מיקום + 20);
            if (גודל < 0 || (종류 != 8 && ((long) קובץ_עמדה + גודל > נתונים.length || קובץ_עמדה < 0))) {
                throw new IllegalArgumentException("ELF מקטע_ערך נתונים 범위가 올바르지 않습니다.");
            }
            구역들.add(new מקטע_ערך(종류, דגל_ערך, למען, קובץ_עמדה, גודל));
        }
        return new תמונה(התחל_למען, 구역들);
    }

    private int ניתוח_מבנה_טקסט_מספר_שלם(byte[] נתונים, int מיקום) {
        if (מיקום < 0 || מיקום > נתונים.length - 4) {
            throw new IllegalArgumentException("ELF מספר_שלם 범위를 벗어났습니다.");
        }
        return (נתונים[מיקום] & 0xff)
                | ((נתונים[מיקום + 1] & 0xff) << 8)
                | ((נתונים[מיקום + 2] & 0xff) << 16)
                | ((נתונים[מיקום + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] נתונים, int מיקום) {
        if (מיקום < 0 || מיקום > נתונים.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 מספר_שלם 범위를 벗어났습니다.");
        }
        return (נתונים[מיקום] & 0xff) | ((נתונים[מיקום + 1] & 0xff) << 8);
    }
}
