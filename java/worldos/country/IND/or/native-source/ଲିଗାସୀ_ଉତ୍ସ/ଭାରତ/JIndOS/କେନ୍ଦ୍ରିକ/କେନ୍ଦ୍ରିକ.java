// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.କେନ୍ଦ୍ରିକ;

import ଭାରତ.JIndOS.기억공간.ମୋମରୀ_ପରିଚାଳକ;
import ଭାରତ.JIndOS.기억공간.ପେଜ୍_ପରିଚାଳକ;
import ଭାରତ.JIndOS.입력.입력관리자;
import ଭାରତ.JIndOS.작업.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ;
import ଭାରତ.JIndOS.작업.ସିଡ୍ୟୁଲର୍;
import ଭାରତ.JIndOS.체계호출.체계호출;
import ଭାରତ.JIndOS.ଫାଇଲ୍_ସିଷ୍ଟମ୍.파일서술자표;
import ଭାରତ.JIndOS.ଫାଇଲ୍_ସିଷ୍ଟମ୍.ଫାଇଲ୍_ସିଷ୍ଟମ୍;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class କେନ୍ଦ୍ରିକ {
    private final ହାର୍ଡୱେର୍_ମୂଲ୍ୟ ଡିଭାଇସ_ମୂଲ୍ୟ;
    private final ମୋମରୀ_ପରିଚାଳକ 기억공간 = new ମୋମରୀ_ପରିଚାଳକ(32 * 1024 * 1024);
    private final ପେଜ୍_ପରିଚାଳକ 쪽관리 = new ପେଜ୍_ପରିଚାଳକ();
    private final ଫାଇଲ୍_ସିଷ୍ଟମ୍ ଫାଇଲ୍_ସିଷ୍ଟମ୍ = new ଫାଇଲ୍_ସିଷ୍ଟମ୍();
    private final ସିଡ୍ୟୁଲର୍ ସିଡ୍ୟୁଲର୍ = new ସିଡ୍ୟୁଲର୍(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final ପ୍ରୋସେସ୍_ମୂଲ୍ୟ 첫과정;
    private final 체계호출 체계호출;

    public କେନ୍ଦ୍ରିକ(ହାର୍ଡୱେର୍_ମୂଲ୍ୟ ଡିଭାଇସ_ମୂଲ୍ୟ) {
        this.ଡିଭାଇସ_ମୂଲ୍ୟ = ଡିଭାଇସ_ମୂଲ୍ୟ;
        첫과정 = ସିଡ୍ୟୁଲର୍.첫과정(new 파일서술자표(ଫାଇଲ୍_ସିଷ୍ଟମ୍));
        체계호출 = new 체계호출(ଫାଇଲ୍_ସିଷ୍ଟମ୍, 쪽관리, ସିଡ୍ୟୁଲର୍, ଡିଭାଇସ_ମୂଲ୍ୟ, 입력관리);
    }

    public void ଚଳାନ୍ତୁ() {
        ଡିଭାଇସ_ମୂଲ୍ୟ.직렬출력("=== JIndOS 관리 କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ ===\n");
    }

    public void 한단계실행() {
        ଡିଭାଇସ_ମୂଲ୍ୟ.중앙처리장치멈춤();
    }

    public ମୋମରୀ_ପରିଚାଳକ 기억공간() {
        return 기억공간;
    }

    public ପେଜ୍_ପରିଚାଳକ 쪽관리() {
        return 쪽관리;
    }

    public ଫାଇଲ୍_ସିଷ୍ଟମ୍ ଫାଇଲ୍_ସିଷ୍ଟମ୍() {
        return ଫାଇଲ୍_ସିଷ୍ଟମ୍;
    }

    public ସିଡ୍ୟୁଲର୍ ସିଡ୍ୟୁଲର୍() {
        return ସିଡ୍ୟୁଲର୍;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public ପ୍ରୋସେସ୍_ମୂଲ୍ୟ 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
