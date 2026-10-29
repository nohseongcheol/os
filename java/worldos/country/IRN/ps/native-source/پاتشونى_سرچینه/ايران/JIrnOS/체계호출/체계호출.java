// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ايران.JIrnOS.체계호출;

import ايران.JIrnOS.기억공간.쪽관리자;
import ايران.JIrnOS.작업.과정;
import ايران.JIrnOS.작업.배정기;
import ايران.JIrnOS.دوتنه_سېسټم.실행파일적재기;
import ايران.JIrnOS.دوتنه_سېسټم.دوتنه_سېسټم;
import ايران.JIrnOS.دوتنه_سېسټم.파일정보;
import ايران.JIrnOS.نوغی.하드웨어;
import ايران.JIrnOS.입력.입력관리자;
import ايران.JIrnOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int 읽기만 = 0;
    public static final int پلټل_پيل = 0;
    public static final int 찾기현재 = 1;
    public static final int 찾기끝 = 2;

    private final دوتنه_سېسټم دوتنه_سېسټم;
    private final 쪽관리자 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 وزله_ارزښت;
    private final 입력관리자 입력관리;

    public 체계호출(دوتنه_سېسټم دوتنه_سېسټم, 쪽관리자 쪽관리, 배정기 배정기, 하드웨어 وزله_ارزښت, 입력관리자 입력관리) {
        this.دوتنه_سېسټم = دوتنه_سېسټم;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.وزله_ارزښت = وزله_ارزښت;
        this.입력관리 = 입력관리;
    }

    public int 과정식별자(과정 현재과정) {
        return 현재과정.식별자();
    }

    public int 부모과정식별자(과정 현재과정) {
        return 현재과정.부모식별자();
    }

    public int پرانيستل(과정 현재과정, String نوم, int رپى_ارزښت) {
        if (رپى_ارزښت != 읽기만) {
            return -30;
        }
        return 현재과정.파일서술자().پرانيستل(نوم);
    }

    public int لوستل(과정 현재과정, int 서술자, byte[] 받을곳, int کچ) {
        if (서술자 == 0) {
            if (کچ <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 پېښه = 입력관리.다음사건();
            if (پېښه == null || پېښه.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) پېښه.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().لوستل(서술자, 받을곳, کچ);
    }

    public int لوستل_2(과정 현재과정, int 서술자, byte[] اومتوک, int کچ) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (کچ < 0 || کچ > اومتوک.length) {
            return -22;
        }
        وزله_ارزښت.직렬출력(new String(اومتوک, 0, کچ, java.nio.charset.StandardCharsets.UTF_8));
        return کچ;
    }

    public int بندول(과정 현재과정, int 서술자) {
        return 현재과정.파일서술자().بندول(서술자);
    }

    public int 위치옮기기(과정 현재과정, int 서술자, int 거리, int 기준) {
        return 현재과정.파일서술자().위치옮기기(서술자, 거리, 기준);
    }

    public int 서술자복제(과정 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(과정 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String نوم, int 방식) {
        파일정보 정보 = دوتنه_سېسټم.정보(نوم);
        if (정보 == null) {
            return -2;
        }
        if ((방식 & 1) != 0 && (정보.형태() & 0111) == 0) {
            return -13;
        }
        if ((방식 & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int 작업목록바꾸기(String نوم) {
        return "/".equals(نوم) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int 사용자식별자() { return 0; }
    public int 유효사용자식별자() { return 0; }
    public int 무리식별자() { return 0; }
    public int 유효무리식별자() { return 0; }

    public int هممهالى_دوتنه(과정 현재과정, int 서술자) {
        return 현재과정.파일서술자().정보(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 لوستل 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(과정 현재과정, int 서술자) {
        파일정보 정보 = 현재과정.파일서술자().정보(서술자);
        return 정보 != null && (정보.형태() & 0170000) == 0020000;
    }

    public int دوتنه_مهار(과정 현재과정, int 서술자, int بولۍ, int 인자) {
        if (بولۍ == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (بولۍ == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (بولۍ == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (بولۍ == 3) {
            return 현재과정.파일서술자().정보(서술자) == null ? -9 : 읽기만;
        }
        if (بولۍ == 4) {
            return 인자 == 읽기만 ? 0 : -30;
        }
        return -22;
    }

    public int 만들기(String نوم, int 권한) {
        return -30;
    }

    public 파일정보 서술자정보(과정 현재과정, int 서술자) {
        return 현재과정.파일서술자().정보(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JIrnOS", "JIrnOS", "0.1", "Java managed kernel", "i386");
    }

    public 파일정보 파일정보(String نوم) {
        return دوتنه_سېسټم.정보(نوم);
    }

    public 과정 과정복제(과정 부모) {
        return 배정기.복제(부모);
    }

    public int 자식기다리기(과정 부모, int 자식식별자, boolean 기다리지않음) {
        return 배정기.자식기다리기(부모, 자식식별자, 기다리지않음);
    }

    public int 프로그램끝(과정 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / 쪽관리자.쪽크기;
        int 끝쪽 = (새끝 + 쪽관리자.쪽크기 - 1) / 쪽관리자.쪽크기;
        if (새끝 > 이전끝) {
            for (int لړیال = 첫쪽; لړیال < 끝쪽; لړیال++) {
                int پته = لړیال * 쪽관리자.쪽크기;
                try {
                    쪽관리.바이트읽기(현재과정.پته_تشې_پټۍ(), پته);
                } catch (IllegalStateException تېروتنه) {
                    쪽관리.쪽연결(현재과정.پته_تشې_پټۍ(), پته, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(과정 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int 결과 = 프로그램끝(현재과정, 이전끝 + 증가량);
        return 결과 < 0 ? 결과 : 이전끝;
    }

    public int 실행(과정 현재과정, byte[] 실행파일) {
        return 실행(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int 실행(과정 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.انځور انځور_ارزښت;
        try {
            انځور_ارزښت = 적재기.검사(실행파일);
        } catch (IllegalArgumentException تېروتنه) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.برخه_ارزښت برخه_ارزښت : انځور_ارزښت.구역들()) {
            if ((برخه_ارزښت.رپى_ارزښت() & 2) == 0 || برخه_ارزښت.کچ() == 0) {
                continue;
            }
            int 첫쪽 = برخه_ارزښت.پته() / 쪽관리자.쪽크기;
            int 끝쪽 = (برخه_ارزښت.پته() + برخه_ارزښت.کچ() + 쪽관리자.쪽크기 - 1) / 쪽관리자.쪽크기;
            for (int لړیال = 첫쪽; لړیال < 끝쪽; لړیال++) {
                int پته = لړیال * 쪽관리자.쪽크기;
                try {
                    쪽관리.바이트읽기(현재과정.پته_تشې_پټۍ(), پته);
                    쪽관리.범위개인쓰기(현재과정.پته_تشې_پټۍ(), پته, 쪽관리자.쪽크기);
                } catch (IllegalStateException تېروتنه) {
                    쪽관리.쪽연결(현재과정.پته_تشې_پټۍ(), پته, true);
                }
            }
            for (int لړیال = 0; لړیال < برخه_ارزښت.کچ(); لړیال++) {
                byte ارزښت = برخه_ارزښت.종류() == 8 ? 0 : 실행파일[برخه_ارزښت.파일위치() + لړیال];
                쪽관리.ليکل_بايټ_ارزښت(현재과정.پته_تشې_پټۍ(), برخه_ارزښت.پته() + لړیال, ارزښت);
            }
        }
        현재과정.실행문맥설정(انځور_ارزښت.پيل_پته(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(과정 현재과정, int انکړ_ارزښت) {
        현재과정.وتون_کاريال(انکړ_ارزښت);
    }
}
