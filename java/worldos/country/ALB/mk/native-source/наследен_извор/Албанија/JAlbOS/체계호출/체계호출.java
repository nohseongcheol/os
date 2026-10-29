// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Албанија.JAlbOS.체계호출;

import Албанија.JAlbOS.기억공간.страница_управник;
import Албанија.JAlbOS.작업.Процес_VALUE;
import Албанија.JAlbOS.작업.Распоредувач;
import Албанија.JAlbOS.систем_на_датотеки.실행파일적재기;
import Албанија.JAlbOS.систем_на_датотеки.систем_на_датотеки;
import Албанија.JAlbOS.систем_на_датотеки.датотека_информации;
import Албанија.JAlbOS.јадро.하드웨어;
import Албанија.JAlbOS.입력.입력관리자;
import Албанија.JAlbOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int само_за_читање_знаменце = 0;
    public static final int SEARCH_Start = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_внес_крај = 2;

    private final систем_на_датотеки систем_на_датотеки;
    private final страница_управник 쪽관리;
    private final Распоредувач Распоредувач;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 уред_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(систем_на_датотеки систем_на_датотеки, страница_управник 쪽관리, Распоредувач Распоредувач, 하드웨어 уред_VALUE, 입력관리자 입력관리) {
        this.систем_на_датотеки = систем_на_датотеки;
        this.쪽관리 = 쪽관리;
        this.Распоредувач = Распоредувач;
        this.уред_VALUE = уред_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Процес_идентификатор(Процес_VALUE 현재과정) {
        return 현재과정.идентификатор_VALUE();
    }

    public int 부모과정식별자(Процес_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int Отвори(Процес_VALUE 현재과정, String Име, int знаменце_VALUE) {
        if (знаменце_VALUE != само_за_читање_знаменце) {
            return -30;
        }
        return 현재과정.파일서술자().Отвори(Име);
    }

    public int Читај(Процес_VALUE 현재과정, int 서술자, byte[] 받을곳, int Големина) {
        if (서술자 == 0) {
            if (Големина <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 настан = 입력관리.Следно_настан();
            if (настан == null || настан.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) настан.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().Читај(서술자, 받을곳, Големина);
    }

    public int Запиши(Процес_VALUE 현재과정, int 서술자, byte[] податоци, int Големина) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().информатичка_технологија_отвори(서술자) ? -30 : -9;
        }
        if (Големина < 0 || Големина > податоци.length) {
            return -22;
        }
        уред_VALUE.직렬출력(new String(податоци, 0, Големина, java.nio.charset.StandardCharsets.UTF_8));
        return Големина;
    }

    public int Затвори(Процес_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Затвори(서술자);
    }

    public int премести_позиционирање(Процес_VALUE 현재과정, int 서술자, int 거리, int Project_корен) {
        return 현재과정.파일서술자().премести_позиционирање(서술자, 거리, Project_корен);
    }

    public int 서술자복제(Процес_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Процес_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Име, int метод_MODE) {
        датотека_информации msinfo32_exe = систем_на_датотеки.msinfo32_exe(Име);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((метод_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((метод_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_список_со_задачи(String Име) {
        return "/".equals(Име) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int корисник_идентификатор() { return 0; }
    public int ефективен_корисник_идентификатор() { return 0; }
    public int Група_идентификатор() { return 0; }
    public int ефективен_Група_идентификатор() { return 0; }

    public int синхронизирај_датотека(Процес_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 Читај 전용이어서 밀어낼 자료가 없다.
    }

    public boolean информатичка_технологија_Терминал(Процес_VALUE 현재과정, int 서술자) {
        датотека_информации msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int датотека_контрола(Процес_VALUE 현재과정, int 서술자, int Команда, int параметар_аргумент) {
        if (Команда == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, параметар_аргумент);
        }
        if (Команда == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (Команда == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (параметар_аргумент & 1) != 0);
        }
        if (Команда == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : само_за_читање_знаменце;
        }
        if (Команда == 4) {
            return параметар_аргумент == само_за_читање_знаменце ? 0 : -30;
        }
        return -22;
    }

    public int Create_внес(String Име, int дозвола_VALUE) {
        return -30;
    }

    public датотека_информации 서술자정보(Процес_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JAlbOS", "JAlbOS", "0.1", "Java managed kernel", "i386");
    }

    public датотека_информации датотека_информации(String Име) {
        return систем_на_датотеки.msinfo32_exe(Име);
    }

    public Процес_VALUE 과정복제(Процес_VALUE 부모) {
        return Распоредувач.복제(부모);
    }

    public int 자식기다리기(Процес_VALUE 부모, int дете_идентификатор, boolean 기다리지않음) {
        return Распоредувач.자식기다리기(부모, дете_идентификатор, 기다리지않음);
    }

    public int 프로그램끝(Процес_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / страница_управник.големина_на_страницата;
        int 끝쪽 = (새끝 + страница_управник.големина_на_страницата - 1) / страница_управник.големина_на_страницата;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int адреса = INDEX * страница_управник.големина_на_страницата;
                try {
                    쪽관리.바이트읽기(현재과정.адреса_простор(), адреса);
                } catch (IllegalStateException ГРЕШКА) {
                    쪽관리.MAP_страница(현재과정.адреса_простор(), адреса, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Процес_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int мерка = 프로그램끝(현재과정, 이전끝 + 증가량);
        return мерка < 0 ? мерка : 이전끝;
    }

    public int Изврши_наредба(Процес_VALUE 현재과정, byte[] 실행파일) {
        return Изврши_наредба(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int Изврши_наредба(Процес_VALUE 현재과정, byte[] 실행파일, String[] параметар_аргумент, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException ГРЕШКА) {
            return -8;
        }
        if (параметар_аргумент == null || 환경 == null || параметар_аргумент.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.секција_VALUE секција_VALUE : IMAGE_VALUE.구역들()) {
            if ((секција_VALUE.знаменце_VALUE() & 2) == 0 || секција_VALUE.Големина() == 0) {
                continue;
            }
            int 첫쪽 = секција_VALUE.адреса() / страница_управник.големина_на_страницата;
            int 끝쪽 = (секција_VALUE.адреса() + секција_VALUE.Големина() + страница_управник.големина_на_страницата - 1) / страница_управник.големина_на_страницата;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int адреса = INDEX * страница_управник.големина_на_страницата;
                try {
                    쪽관리.바이트읽기(현재과정.адреса_простор(), адреса);
                    쪽관리.범위개인쓰기(현재과정.адреса_простор(), адреса, страница_управник.големина_на_страницата);
                } catch (IllegalStateException ГРЕШКА) {
                    쪽관리.MAP_страница(현재과정.адреса_простор(), адреса, true);
                }
            }
            for (int INDEX = 0; INDEX < секција_VALUE.Големина(); INDEX++) {
                byte VALUE = секција_VALUE.종류() == 8 ? 0 : 실행파일[секција_VALUE.датотека_позиционирање() + INDEX];
                쪽관리.запиши_бајт_VALUE(현재과정.адреса_простор(), секција_VALUE.адреса() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(IMAGE_VALUE.почетна_адреса(), параметар_аргумент, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void излез_програма(Процес_VALUE 현재과정, int статус_VALUE) {
        현재과정.Излез_програма(статус_VALUE);
    }
}
