// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.JMngOS.작업;

import Монгол.JMngOS.기억공간.хуудас_менежер;
import Монгол.JMngOS.файлын_систем.파일서술자표;

public final class үйл_явц_утга {
    private final int танигч_утга;
    private final int 부모식별자;
    private final хуудас_менежер.хаяг_орон_зай хаяг_орон_зай;
    private final 파일서술자표 파일서술자;
    private үйл_явц_төлөв төлөв_утга = үйл_явц_төлөв.Бэлтгэх;
    private int 종료값;
    private int 프로그램끝 = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    үйл_явц_утга(int танигч_утга, int 부모식별자, хуудас_менежер.хаяг_орон_зай хаяг_орон_зай, 파일서술자표 파일서술자) {
        this.танигч_утга = танигч_утга;
        this.부모식별자 = 부모식별자;
        this.хаяг_орон_зай = хаяг_орон_зай;
        this.파일서술자 = 파일서술자;
    }

    public int танигч_утга() {
        return танигч_утга;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public хуудас_менежер.хаяг_орон_зай хаяг_орон_зай() {
        return хаяг_орон_зай;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public үйл_явц_төлөв төлөв_утга() {
        return төлөв_утга;
    }

    public void багц_төлөв(үйл_явц_төлөв 새상태) {
        төлөв_утга = 새상태;
    }

    public int 종료값() {
        return 종료값;
    }

    public void Гарах_програм(int утга) {
        종료값 = утга & 0xff;
        төлөв_утга = үйл_явц_төлөв.Гарах_програм;
    }

    public int 프로그램끝() {
        return 프로그램끝;
    }

    public void 프로그램끝설정(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("програм_f5044b9b 끝 범위를 벗어났습니다.");
        }
        프로그램끝 = 새끝;
    }

    public void 실행문맥설정(int Эхлэл_хаяг, String[] 인자, String[] 환경) {
        실행시작주소 = Эхлэл_хаяг;
        실행인자 = 인자.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
