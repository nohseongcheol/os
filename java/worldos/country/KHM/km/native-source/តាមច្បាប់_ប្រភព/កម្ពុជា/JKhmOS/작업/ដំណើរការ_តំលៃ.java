// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.작업;

import កម្ពុជា.JKhmOS.기억공간.ទំព័រ_អ្នកគ្រប់គ្រង;
import កម្ពុជា.JKhmOS.ឯកសារនៃប្រព័ន្ធ.파일서술자표;

public final class ដំណើរការ_តំលៃ {
    private final int អង្គសម្គាល់_តំលៃ;
    private final int 부모식별자;
    private final ទំព័រ_អ្នកគ្រប់គ្រង.អ៊ីម៉ែល_លំហ អ៊ីម៉ែល_លំហ;
    private final 파일서술자표 파일서술자;
    private ដំណើរការ_ភាព ភាព_តំលៃ = ដំណើរការ_ភាព.រៀបចំ;
    private int ចេញ_កូដ;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    ដំណើរការ_តំលៃ(int អង្គសម្គាល់_តំលៃ, int 부모식별자, ទំព័រ_អ្នកគ្រប់គ្រង.អ៊ីម៉ែល_លំហ អ៊ីម៉ែល_លំហ, 파일서술자표 파일서술자) {
        this.អង្គសម្គាល់_តំលៃ = អង្គសម្គាល់_តំលៃ;
        this.부모식별자 = 부모식별자;
        this.អ៊ីម៉ែល_លំហ = អ៊ីម៉ែល_លំហ;
        this.파일서술자 = 파일서술자;
    }

    public int អង្គសម្គាល់_តំលៃ() {
        return អង្គសម្គាល់_តំលៃ;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public ទំព័រ_អ្នកគ្រប់គ្រង.អ៊ីម៉ែល_លំហ អ៊ីម៉ែល_លំហ() {
        return អ៊ីម៉ែល_លំហ;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public ដំណើរការ_ភាព ភាព_តំលៃ() {
        return ភាព_តំលៃ;
    }

    public void កំណត់_ភាព(ដំណើរការ_ភាព 새상태) {
        ភាព_តំលៃ = 새상태;
    }

    public int ចេញ_កូដ() {
        return ចេញ_កូដ;
    }

    public void ចេញ_កម្មវិធី(int តំលៃ) {
        ចេញ_កូដ = តំលៃ & 0xff;
        ភាព_តំលៃ = ដំណើរការ_ភាព.ចេញ_កម្មវិធី;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("កម្មវិធី_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int ផ្តើម_អ៊ីម៉ែល, String[] ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់, String[] 환경) {
        실행시작주소 = ផ្តើម_អ៊ីម៉ែល;
        실행인자 = ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
