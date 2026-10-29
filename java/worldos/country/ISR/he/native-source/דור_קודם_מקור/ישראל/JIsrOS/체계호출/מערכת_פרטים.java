// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.체계호출;

public final class מערכת_פרטים {
    private final String מערכת_שם;
    private final String צומת_שם;
    private final String מהדורה_ערך;
    private final String גירסה_ערך;
    private final String מחשב;

    public מערכת_פרטים(String מערכת_שם, String צומת_שם, String מהדורה_ערך, String גירסה_ערך, String מחשב) {
        this.מערכת_שם = מערכת_שם;
        this.צומת_שם = צומת_שם;
        this.מהדורה_ערך = מהדורה_ערך;
        this.גירסה_ערך = גירסה_ערך;
        this.מחשב = מחשב;
    }

    public String מערכת_שם() { return מערכת_שם; }
    public String צומת_שם() { return צומת_שם; }
    public String מהדורה_ערך() { return מהדורה_ערך; }
    public String גירסה_ערך() { return גירסה_ערך; }
    public String מחשב() { return מחשב; }
}
