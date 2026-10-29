// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package لبنان.JLbnOS.작업;

import لبنان.JLbnOS.ذاكرة_منطقة.صفحة_مدير;
import لبنان.JLbnOS.نظام_الملفات.파일서술자표;

public final class عملية_قيمة {
    private final int معرف_قيمة;
    private final int أصل_معرف;
    private final صفحة_مدير.عنوان_مساحة عنوان_مساحة;
    private final 파일서술자표 파일서술자;
    private عملية_حالة حالة_قيمة = عملية_حالة.إعداد;
    private int التعليمة_البرمجية_للخروج;
    private int تطبيق_توقف = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] بيئة_التشغيل_قيمة = new String[0];

    عملية_قيمة(int معرف_قيمة, int أصل_معرف, صفحة_مدير.عنوان_مساحة عنوان_مساحة, 파일서술자표 파일서술자) {
        this.معرف_قيمة = معرف_قيمة;
        this.أصل_معرف = أصل_معرف;
        this.عنوان_مساحة = عنوان_مساحة;
        this.파일서술자 = 파일서술자;
    }

    public int معرف_قيمة() {
        return معرف_قيمة;
    }

    public int أصل_معرف() {
        return أصل_معرف;
    }

    public صفحة_مدير.عنوان_مساحة عنوان_مساحة() {
        return عنوان_مساحة;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public عملية_حالة حالة_قيمة() {
        return حالة_قيمة;
    }

    public void مجموعة_حالة(عملية_حالة 새상태) {
        حالة_قيمة = 새상태;
    }

    public int التعليمة_البرمجية_للخروج() {
        return التعليمة_البرمجية_للخروج;
    }

    public void خروج_تطبيق(int قيمة) {
        التعليمة_البرمجية_للخروج = قيمة & 0xff;
        حالة_قيمة = عملية_حالة.خروج_تطبيق;
    }

    public int تطبيق_توقف() {
        return تطبيق_توقف;
    }

    public void مجموعة_تطبيق_توقف(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("تطبيق_f5044b9b 끝 범위를 벗어났습니다.");
        }
        تطبيق_توقف = 새끝;
    }

    public void 실행문맥설정(int بدء_عنوان, String[] معلمة_وسيطة, String[] بيئة_التشغيل) {
        실행시작주소 = بدء_عنوان;
        실행인자 = معلمة_وسيطة.clone();
        بيئة_التشغيل_قيمة = بيئة_التشغيل.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] بيئة_التشغيل_قيمة() { return بيئة_التشغيل_قيمة.clone(); }
}
