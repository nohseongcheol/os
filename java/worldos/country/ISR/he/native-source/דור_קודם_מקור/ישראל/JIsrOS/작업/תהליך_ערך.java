// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.작업;

import ישראל.JIsrOS.זיכרון_אזור.דף_מנהל;
import ישראל.JIsrOS.מערכת_קבצים.파일서술자표;

public final class תהליך_ערך {
    private final int מזהה_ערך;
    private final int אב_מזהה;
    private final דף_מנהל.למען_חלל למען_חלל;
    private final 파일서술자표 파일서술자;
    private תהליך_מצב_4346e67f מצב_ערך = תהליך_מצב_4346e67f.להכין;
    private int קוד_יציאה;
    private int תוכנית_הפסקה = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] סביבה_ערך = new String[0];

    תהליך_ערך(int מזהה_ערך, int אב_מזהה, דף_מנהל.למען_חלל למען_חלל, 파일서술자표 파일서술자) {
        this.מזהה_ערך = מזהה_ערך;
        this.אב_מזהה = אב_מזהה;
        this.למען_חלל = למען_חלל;
        this.파일서술자 = 파일서술자;
    }

    public int מזהה_ערך() {
        return מזהה_ערך;
    }

    public int אב_מזהה() {
        return אב_מזהה;
    }

    public דף_מנהל.למען_חלל למען_חלל() {
        return למען_חלל;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public תהליך_מצב_4346e67f מצב_ערך() {
        return מצב_ערך;
    }

    public void ערכה_מצב(תהליך_מצב_4346e67f 새상태) {
        מצב_ערך = 새상태;
    }

    public int קוד_יציאה() {
        return קוד_יציאה;
    }

    public void יציאה_תוכנית(int ערך) {
        קוד_יציאה = ערך & 0xff;
        מצב_ערך = תהליך_מצב_4346e67f.יציאה_תוכנית;
    }

    public int תוכנית_הפסקה() {
        return תוכנית_הפסקה;
    }

    public void ערכה_תוכנית_הפסקה(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("תוכנית_f5044b9b 끝 범위를 벗어났습니다.");
        }
        תוכנית_הפסקה = 새끝;
    }

    public void 실행문맥설정(int התחל_למען, String[] פרמטר_ארגומנט, String[] סביבה) {
        실행시작주소 = התחל_למען;
        실행인자 = פרמטר_ארגומנט.clone();
        סביבה_ערך = סביבה.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] סביבה_ערך() { return סביבה_ערך.clone(); }
}
