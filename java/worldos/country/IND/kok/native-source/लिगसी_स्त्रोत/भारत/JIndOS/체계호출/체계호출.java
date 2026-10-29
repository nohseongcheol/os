// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.체계호출;

import भारत.JIndOS.기억공간.पान_वेवस्थापक;
import भारत.JIndOS.작업.प्रक्रिया_मोल;
import भारत.JIndOS.작업.नियोजक;
import भारत.JIndOS.फायल_प्रणाली.실행파일적재기;
import भारत.JIndOS.फायल_प्रणाली.फायल_प्रणाली;
import भारत.JIndOS.फायल_प्रणाली.फायल_म्हायती;
import भारत.JIndOS.कर्नेल.हार्डवॅर_मोल;
import भारत.JIndOS.입력.입력관리자;
import भारत.JIndOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int फकत_वाचचें_कुरवो = 0;
    public static final int सोद_Start = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_प्रवेश_सोपोवचें = 2;

    private final फायल_प्रणाली फायल_प्रणाली;
    private final पान_वेवस्थापक 쪽관리;
    private final नियोजक नियोजक;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final हार्डवॅर_मोल मोबायल_मोल;
    private final 입력관리자 입력관리;

    public 체계호출(फायल_प्रणाली फायल_प्रणाली, पान_वेवस्थापक 쪽관리, नियोजक नियोजक, हार्डवॅर_मोल मोबायल_मोल, 입력관리자 입력관리) {
        this.फायल_प्रणाली = फायल_प्रणाली;
        this.쪽관리 = 쪽관리;
        this.नियोजक = नियोजक;
        this.मोबायल_मोल = मोबायल_मोल;
        this.입력관리 = 입력관리;
    }

    public int प्रक्रिया_वळखुपी(प्रक्रिया_मोल 현재과정) {
        return 현재과정.वळखुपी_मोल();
    }

    public int 부모과정식별자(प्रक्रिया_मोल 현재과정) {
        return 현재과정.부모식별자();
    }

    public int उगडचें(प्रक्रिया_मोल 현재과정, String नांव, int कुरवो_मोल) {
        if (कुरवो_मोल != फकत_वाचचें_कुरवो) {
            return -30;
        }
        return 현재과정.파일서술자().उगडचें(नांव);
    }

    public int 읽기(प्रक्रिया_मोल 현재과정, int 서술자, byte[] 받을곳, int आवाठ) {
        if (서술자 == 0) {
            if (आवाठ <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 प्रसंग = 입력관리.फुडलें_प्रसंग();
            if (प्रसंग == null || प्रसंग.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) प्रसंग.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, आवाठ);
    }

    public int बरोवचें(प्रक्रिया_मोल 현재과정, int 서술자, byte[] डेटा, int आवाठ) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (आवाठ < 0 || आवाठ > डेटा.length) {
            return -22;
        }
        मोबायल_मोल.직렬출력(new String(डेटा, 0, आवाठ, java.nio.charset.StandardCharsets.UTF_8));
        return आवाठ;
    }

    public int शेवट(प्रक्रिया_मोल 현재과정, int 서술자) {
        return 현재과정.파일서술자().शेवट(서술자);
    }

    public int हालोवचें_स्थिती(प्रक्रिया_मोल 현재과정, int 서술자, int 거리, int प्रॉजॅक्ट_रूट) {
        return 현재과정.파일서술자().हालोवचें_स्थिती(서술자, 거리, प्रॉजॅक्ट_रूट);
    }

    public int 서술자복제(प्रक्रिया_मोल 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(प्रक्रिया_मोल 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String नांव, int पद्दत_मोड) {
        फायल_म्हायती msinfo32_exe = फायल_प्रणाली.msinfo32_exe(नांव);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((पद्दत_मोड & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((पद्दत_मोड & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int स्विच_कार्य_सुची(String नांव) {
        return "/".equals(नांव) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int उपेगकर्तो_वळखुपी() { return 0; }
    public int परिणामकारक_उपेगकर्तो_वळखुपी() { return 0; }
    public int गट_वळखुपी() { return 0; }
    public int परिणामकारक_गट_वळखुपी() { return 0; }

    public int सिंक्रोनायझ_फायल(प्रक्रिया_मोल 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(प्रक्रिया_मोल 현재과정, int 서술자) {
        फायल_म्हायती msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int फायल_नियंत्रण(प्रक्रिया_मोल 현재과정, int 서술자, int आदेश, int 인자) {
        if (आदेश == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (आदेश == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (आदेश == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (आदेश == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : फकत_वाचचें_कुरवो;
        }
        if (आदेश == 4) {
            return 인자 == फकत_वाचचें_कुरवो ? 0 : -30;
        }
        return -22;
    }

    public int निर्माण_करचें_प्रवेश(String नांव, int अनुमती_मोल) {
        return -30;
    }

    public फायल_म्हायती 서술자정보(प्रक्रिया_मोल 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JIndOS", "JIndOS", "0.1", "Java managed kernel", "i386");
    }

    public फायल_म्हायती फायल_म्हायती(String नांव) {
        return फायल_प्रणाली.msinfo32_exe(नांव);
    }

    public प्रक्रिया_मोल 과정복제(प्रक्रिया_मोल 부모) {
        return नियोजक.복제(부모);
    }

    public int 자식기다리기(प्रक्रिया_मोल 부모, int भुरगें_वळखुपी, boolean 기다리지않음) {
        return नियोजक.자식기다리기(부모, भुरगें_वळखुपी, 기다리지않음);
    }

    public int 프로그램끝(प्रक्रिया_मोल 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / पान_वेवस्थापक.पानाचो_आंवाठ;
        int 끝쪽 = (새끝 + पान_वेवस्थापक.पानाचो_आंवाठ - 1) / पान_वेवस्थापक.पानाचो_आंवाठ;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int नामो = INDEX * पान_वेवस्थापक.पानाचो_आंवाठ;
                try {
                    쪽관리.바이트읽기(현재과정.नामो_SPACE(), नामो);
                } catch (IllegalStateException चूक) {
                    쪽관리.नकसो_पान(현재과정.नामो_SPACE(), नामो, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(प्रक्रिया_मोल 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int मेजप = 프로그램끝(현재과정, 이전끝 + 증가량);
        return मेजप < 0 ? मेजप : 이전끝;
    }

    public int पाळो_दिवचो_आदेश(प्रक्रिया_मोल 현재과정, byte[] 실행파일) {
        return पाळो_दिवचो_आदेश(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int पाळो_दिवचो_आदेश(प्रक्रिया_मोल 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_मोल;
        try {
            IMAGE_मोल = 적재기.검사(실행파일);
        } catch (IllegalArgumentException चूक) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.विभाग_मोल विभाग_मोल : IMAGE_मोल.구역들()) {
            if ((विभाग_मोल.कुरवो_मोल() & 2) == 0 || विभाग_मोल.आवाठ() == 0) {
                continue;
            }
            int 첫쪽 = विभाग_मोल.नामो() / पान_वेवस्थापक.पानाचो_आंवाठ;
            int 끝쪽 = (विभाग_मोल.नामो() + विभाग_मोल.आवाठ() + पान_वेवस्थापक.पानाचो_आंवाठ - 1) / पान_वेवस्थापक.पानाचो_आंवाठ;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int नामो = INDEX * पान_वेवस्थापक.पानाचो_आंवाठ;
                try {
                    쪽관리.바이트읽기(현재과정.नामो_SPACE(), नामो);
                    쪽관리.범위개인쓰기(현재과정.नामो_SPACE(), नामो, पान_वेवस्थापक.पानाचो_आंवाठ);
                } catch (IllegalStateException चूक) {
                    쪽관리.नकसो_पान(현재과정.नामो_SPACE(), नामो, true);
                }
            }
            for (int INDEX = 0; INDEX < विभाग_मोल.आवाठ(); INDEX++) {
                byte मोल = विभाग_मोल.종류() == 8 ? 0 : 실행파일[विभाग_मोल.फायल_स्थिती_2aa21a9a() + INDEX];
                쪽관리.बरोवचें_बायट_मोल(현재과정.नामो_SPACE(), विभाग_मोल.नामो() + INDEX, मोल);
            }
        }
        현재과정.실행문맥설정(IMAGE_मोल.Start_नामो(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void सोडचें_एप्लिकेशन(प्रक्रिया_मोल 현재과정, int स्थिती_मोल_e10195a1) {
        현재과정.प्रस्थान_करचें_एप्लिकेशन(स्थिती_मोल_e10195a1);
    }
}
