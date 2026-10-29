// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Namibiab.JNamOS.체계호출;

import Namibiab.JNamOS.기억공간.쪽관리자;
import Namibiab.JNamOS.작업.과정;
import Namibiab.JNamOS.작업.배정기;
import Namibiab.JNamOS.파일체계.실행파일적재기;
import Namibiab.JNamOS.파일체계.파일체계;
import Namibiab.JNamOS.파일체계.파일정보;
import Namibiab.JNamOS.핵심.하드웨어;
import Namibiab.JNamOS.입력.입력관리자;
import Namibiab.JNamOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int 읽기만 = 0;
    public static final int 찾기시작 = 0;
    public static final int 찾기현재 = 1;
    public static final int 찾기끝 = 2;

    private final 파일체계 파일체계;
    private final 쪽관리자 쪽관리;
    private final 배정기 배정기;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 장치;
    private final 입력관리자 입력관리;

    public 체계호출(파일체계 파일체계, 쪽관리자 쪽관리, 배정기 배정기, 하드웨어 장치, 입력관리자 입력관리) {
        this.파일체계 = 파일체계;
        this.쪽관리 = 쪽관리;
        this.배정기 = 배정기;
        this.장치 = 장치;
        this.입력관리 = 입력관리;
    }

    public int 과정식별자(과정 현재과정) {
        return 현재과정.식별자();
    }

    public int 부모과정식별자(과정 현재과정) {
        return 현재과정.부모식별자();
    }

    public int 열기(과정 현재과정, String 이름, int 깃발) {
        if (깃발 != 읽기만) {
            return -30;
        }
        return 현재과정.파일서술자().열기(이름);
    }

    public int 읽기(과정 현재과정, int 서술자, byte[] 받을곳, int 크기) {
        if (서술자 == 0) {
            if (크기 <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 사건 = 입력관리.다음사건();
            if (사건 == null || 사건.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) 사건.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, 크기);
    }

    public int 쓰기(과정 현재과정, int 서술자, byte[] 자료, int 크기) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (크기 < 0 || 크기 > 자료.length) {
            return -22;
        }
        장치.직렬출력(new String(자료, 0, 크기, java.nio.charset.StandardCharsets.UTF_8));
        return 크기;
    }

    public int 닫기(과정 현재과정, int 서술자) {
        return 현재과정.파일서술자().닫기(서술자);
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

    public int 접근가능(String 이름, int 방식) {
        파일정보 정보 = 파일체계.정보(이름);
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

    public int 작업목록바꾸기(String 이름) {
        return "/".equals(이름) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int 사용자식별자() { return 0; }
    public int 유효사용자식별자() { return 0; }
    public int 무리식별자() { return 0; }
    public int 유효무리식별자() { return 0; }

    public int 파일동기화(과정 현재과정, int 서술자) {
        return 현재과정.파일서술자().정보(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(과정 현재과정, int 서술자) {
        파일정보 정보 = 현재과정.파일서술자().정보(서술자);
        return 정보 != null && (정보.형태() & 0170000) == 0020000;
    }

    public int 파일제어(과정 현재과정, int 서술자, int 명령, int 인자) {
        if (명령 == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (명령 == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (명령 == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (명령 == 3) {
            return 현재과정.파일서술자().정보(서술자) == null ? -9 : 읽기만;
        }
        if (명령 == 4) {
            return 인자 == 읽기만 ? 0 : -30;
        }
        return -22;
    }

    public int 만들기(String 이름, int 권한) {
        return -30;
    }

    public 파일정보 서술자정보(과정 현재과정, int 서술자) {
        return 현재과정.파일서술자().정보(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JNamOS", "JNamOS", "0.1", "Java managed kernel", "i386");
    }

    public 파일정보 파일정보(String 이름) {
        return 파일체계.정보(이름);
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
            for (int 번호 = 첫쪽; 번호 < 끝쪽; 번호++) {
                int 주소 = 번호 * 쪽관리자.쪽크기;
                try {
                    쪽관리.바이트읽기(현재과정.주소공간(), 주소);
                } catch (IllegalStateException 오류) {
                    쪽관리.쪽연결(현재과정.주소공간(), 주소, true);
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
        실행파일적재기.실행영상 영상;
        try {
            영상 = 적재기.검사(실행파일);
        } catch (IllegalArgumentException 오류) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.구역 구역 : 영상.구역들()) {
            if ((구역.깃발() & 2) == 0 || 구역.크기() == 0) {
                continue;
            }
            int 첫쪽 = 구역.주소() / 쪽관리자.쪽크기;
            int 끝쪽 = (구역.주소() + 구역.크기() + 쪽관리자.쪽크기 - 1) / 쪽관리자.쪽크기;
            for (int 번호 = 첫쪽; 번호 < 끝쪽; 번호++) {
                int 주소 = 번호 * 쪽관리자.쪽크기;
                try {
                    쪽관리.바이트읽기(현재과정.주소공간(), 주소);
                    쪽관리.범위개인쓰기(현재과정.주소공간(), 주소, 쪽관리자.쪽크기);
                } catch (IllegalStateException 오류) {
                    쪽관리.쪽연결(현재과정.주소공간(), 주소, true);
                }
            }
            for (int 번호 = 0; 번호 < 구역.크기(); 번호++) {
                byte 값 = 구역.종류() == 8 ? 0 : 실행파일[구역.파일위치() + 번호];
                쪽관리.바이트쓰기(현재과정.주소공간(), 구역.주소() + 번호, 값);
            }
        }
        현재과정.실행문맥설정(영상.시작주소(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void 끝내기(과정 현재과정, int 상태) {
        현재과정.종료(상태);
    }
}
