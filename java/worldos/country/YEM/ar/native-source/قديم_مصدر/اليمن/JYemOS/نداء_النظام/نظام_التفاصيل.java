// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اليمن.JYemOS.نداء_النظام;

public final class نظام_التفاصيل {
    private final String نظام_اسم;
    private final String عقدة_اسم;
    private final String 배포판;
    private final String إصدار_قيمة;
    private final String جهاز;

    public نظام_التفاصيل(String نظام_اسم, String عقدة_اسم, String 배포판, String إصدار_قيمة, String جهاز) {
        this.نظام_اسم = نظام_اسم;
        this.عقدة_اسم = عقدة_اسم;
        this.배포판 = 배포판;
        this.إصدار_قيمة = إصدار_قيمة;
        this.جهاز = جهاز;
    }

    public String نظام_اسم() { return نظام_اسم; }
    public String عقدة_اسم() { return عقدة_اسم; }
    public String 배포판() { return 배포판; }
    public String إصدار_قيمة() { return إصدار_قيمة; }
    public String جهاز() { return جهاز; }
}
