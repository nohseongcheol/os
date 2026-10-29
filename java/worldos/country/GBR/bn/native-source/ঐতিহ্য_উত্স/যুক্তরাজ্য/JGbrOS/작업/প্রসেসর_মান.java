// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package যুক্তরাজ্য.JGbrOS.작업;

import যুক্তরাজ্য.JGbrOS.기억공간.পৃষ্ঠা_ব্যবস্থাপক;
import যুক্তরাজ্য.JGbrOS.ফাইল_পদ্ধতি.파일서술자표;

public final class প্রসেসর_মান {
    private final int সনাক্তকারী_মান;
    private final int 부모식별자;
    private final পৃষ্ঠা_ব্যবস্থাপক.ইমেইল_স্পেস ইমেইল_স্পেস;
    private final 파일서술자표 파일서술자;
    private প্রসেসর_অবস্হা অবস্হা_মান = প্রসেসর_অবস্হা.প্রস্তুত_করুন;
    private int প্রস্থান_কোড;
    private int অ্যাপ_বিরতি = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    প্রসেসর_মান(int সনাক্তকারী_মান, int 부모식별자, পৃষ্ঠা_ব্যবস্থাপক.ইমেইল_স্পেস ইমেইল_স্পেস, 파일서술자표 파일서술자) {
        this.সনাক্তকারী_মান = সনাক্তকারী_মান;
        this.부모식별자 = 부모식별자;
        this.ইমেইল_স্পেস = ইমেইল_স্পেস;
        this.파일서술자 = 파일서술자;
    }

    public int সনাক্তকারী_মান() {
        return সনাক্তকারী_মান;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public পৃষ্ঠা_ব্যবস্থাপক.ইমেইল_স্পেস ইমেইল_স্পেস() {
        return ইমেইল_স্পেস;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public প্রসেসর_অবস্হা অবস্হা_মান() {
        return অবস্হা_মান;
    }

    public void সেট_অবস্হা(প্রসেসর_অবস্হা 새상태) {
        অবস্হা_মান = 새상태;
    }

    public int প্রস্থান_কোড() {
        return প্রস্থান_কোড;
    }

    public void প্রস্থান_অ্যাপ(int মান) {
        প্রস্থান_কোড = মান & 0xff;
        অবস্হা_মান = প্রসেসর_অবস্হা.প্রস্থান_অ্যাপ;
    }

    public int অ্যাপ_বিরতি() {
        return অ্যাপ_বিরতি;
    }

    public void সেট_অ্যাপ_বিরতি(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("অ্যাপ_f5044b9b 끝 범위를 벗어났습니다.");
        }
        অ্যাপ_বিরতি = 새끝;
    }

    public void 실행문맥설정(int শুরু_ইমেইল, String[] প্যারামিটার_যুক্তি, String[] 환경) {
        실행시작주소 = শুরু_ইমেইল;
        실행인자 = প্যারামিটার_যুক্তি.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
