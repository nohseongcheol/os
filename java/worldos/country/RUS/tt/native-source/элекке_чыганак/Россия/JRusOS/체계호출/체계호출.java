// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.체계호출;

import Россия.JRusOS.기억공간.бит_идарәче;
import Россия.JRusOS.작업.Процесс_VALUE;
import Россия.JRusOS.작업.Планлаштыручы;
import Россия.JRusOS.файл_системасы.실행파일적재기;
import Россия.JRusOS.файл_системасы.файл_системасы;
import Россия.JRusOS.файл_системасы.файл_мәгълүмат;
import Россия.JRusOS.төш.하드웨어;
import Россия.JRusOS.입력.입력관리자;
import Россия.JRusOS.입력.입력사건;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int укымалы_гына_тамга_кую = 0;
    public static final int Эзләү_Start = 0;
    public static final int 찾기현재 = 1;
    public static final int FIND_кертү_тәмамлау = 2;

    private final файл_системасы файл_системасы;
    private final бит_идарәче 쪽관리;
    private final Планлаштыручы Планлаштыручы;
    private final 실행파일적재기 적재기 = new 실행파일적재기();
    private final 하드웨어 мобиль_VALUE;
    private final 입력관리자 입력관리;

    public 체계호출(файл_системасы файл_системасы, бит_идарәче 쪽관리, Планлаштыручы Планлаштыручы, 하드웨어 мобиль_VALUE, 입력관리자 입력관리) {
        this.файл_системасы = файл_системасы;
        this.쪽관리 = 쪽관리;
        this.Планлаштыручы = Планлаштыручы;
        this.мобиль_VALUE = мобиль_VALUE;
        this.입력관리 = 입력관리;
    }

    public int Процесс_күрсәткеч(Процесс_VALUE 현재과정) {
        return 현재과정.күрсәткеч_VALUE();
    }

    public int 부모과정식별자(Процесс_VALUE 현재과정) {
        return 현재과정.부모식별자();
    }

    public int ачу(Процесс_VALUE 현재과정, String исем, int тамга_кую_VALUE) {
        if (тамга_кую_VALUE != укымалы_гына_тамга_кую) {
            return -30;
        }
        return 현재과정.파일서술자().ачу(исем);
    }

    public int 읽기(Процесс_VALUE 현재과정, int 서술자, byte[] 받을곳, int үлчәмен_үзгәртү) {
        if (서술자 == 0) {
            if (үлчәмен_үзгәртү <= 0 || 받을곳.length == 0) {
                return 0;
            }
            입력사건 вакыйга = 입력관리.Киләсе_вакыйга();
            if (вакыйга == null || вакыйга.사건종류() != 입력사건.종류.키누름) {
                return -11;
            }
            받을곳[0] = (byte) вакыйга.첫째값();
            return 1;
        }
        return 현재과정.파일서술자().읽기(서술자, 받을곳, үлчәмен_үзгәртү);
    }

    public int язу(Процесс_VALUE 현재과정, int 서술자, byte[] мәгълүмат, int үлчәмен_үзгәртү) {
        if (서술자 != 1 && 서술자 != 2) {
            return 현재과정.파일서술자().열려있음(서술자) ? -30 : -9;
        }
        if (үлчәмен_үзгәртү < 0 || үлчәмен_үзгәртү > мәгълүмат.length) {
            return -22;
        }
        мобиль_VALUE.직렬출력(new String(мәгълүмат, 0, үлчәмен_үзгәртү, java.nio.charset.StandardCharsets.UTF_8));
        return үлчәмен_үзгәртү;
    }

    public int Yap(Процесс_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().Yap(서술자);
    }

    public int күчерү_урнаштыру(Процесс_VALUE 현재과정, int 서술자, int 거리, int экранга_җибәрү_тамыр) {
        return 현재과정.파일서술자().күчерү_урнаштыру(서술자, 거리, экранга_җибәрү_тамыр);
    }

    public int 서술자복제(Процесс_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Процесс_VALUE 현재과정, int 서술자, int 새서술자) {
        return 현재과정.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String исем, int ысул_MODE) {
        файл_мәгълүмат msinfo32_exe = файл_системасы.msinfo32_exe(исем);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((ысул_MODE & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((ысул_MODE & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_мәсьәләләр_исемлеге(String исем) {
        return "/".equals(исем) ? 0 : -20;
    }

    public String 현재작업목록(int 받을크기) {
        return 받을크기 >= 2 ? "/" : null;
    }

    public int кулланучы_күрсәткеч() { return 0; }
    public int эффектив_кулланучы_күрсәткеч() { return 0; }
    public int төркем_күрсәткеч() { return 0; }
    public int эффектив_төркем_күрсәткеч() { return 0; }

    public int синхронлаштыру_файл(Процесс_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // 현재 파일체계는 읽기 전용이어서 밀어낼 자료가 없다.
    }

    public boolean 단말인가(Процесс_VALUE 현재과정, int 서술자) {
        файл_мәгълүмат msinfo32_exe = 현재과정.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int файл_идарә(Процесс_VALUE 현재과정, int 서술자, int команда, int 인자) {
        if (команда == 0) {
            return 현재과정.파일서술자().복제서술자(서술자, 인자);
        }
        if (команда == 1) {
            return 현재과정.파일서술자().실행시닫기값(서술자);
        }
        if (команда == 2) {
            return 현재과정.파일서술자().실행시닫기설정(서술자, (인자 & 1) != 0);
        }
        if (команда == 3) {
            return 현재과정.파일서술자().msinfo32_exe(서술자) == null ? -9 : укымалы_гына_тамга_кую;
        }
        if (команда == 4) {
            return 인자 == укымалы_гына_тамга_кую ? 0 : -30;
        }
        return -22;
    }

    public int Төзү_кертү(String исем, int рөхсәт_VALUE) {
        return -30;
    }

    public файл_мәгълүмат 서술자정보(Процесс_VALUE 현재과정, int 서술자) {
        return 현재과정.파일서술자().msinfo32_exe(서술자);
    }

    public 체계정보 체계정보() {
        return new 체계정보("JRusOS", "JRusOS", "0.1", "Java managed kernel", "i386");
    }

    public файл_мәгълүмат файл_мәгълүмат(String исем) {
        return файл_системасы.msinfo32_exe(исем);
    }

    public Процесс_VALUE 과정복제(Процесс_VALUE 부모) {
        return Планлаштыручы.복제(부모);
    }

    public int 자식기다리기(Процесс_VALUE 부모, int бала_күрсәткеч, boolean 기다리지않음) {
        return Планлаштыручы.자식기다리기(부모, бала_күрсәткеч, 기다리지않음);
    }

    public int 프로그램끝(Процесс_VALUE 현재과정, int 새끝) {
        int 이전끝 = 현재과정.프로그램끝();
        if (새끝 == 0) {
            return 이전끝;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = 이전끝 / бит_идарәче.бит_зурлыгы;
        int 끝쪽 = (새끝 + бит_идарәче.бит_зурлыгы - 1) / бит_идарәче.бит_зурлыгы;
        if (새끝 > 이전끝) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int адрес = INDEX * бит_идарәче.бит_зурлыгы;
                try {
                    쪽관리.바이트읽기(현재과정.адрес_өлкә(), адрес);
                } catch (IllegalStateException Хата) {
                    쪽관리.MAP_бит(현재과정.адрес_өлкә(), адрес, true);
                }
            }
        }
        현재과정.프로그램끝설정(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Процесс_VALUE 현재과정, int 증가량) {
        int 이전끝 = 현재과정.프로그램끝();
        int үлчәм = 프로그램끝(현재과정, 이전끝 + 증가량);
        return үлчәм < 0 ? үлчәм : 이전끝;
    }

    public int үтәргә_команда(Процесс_VALUE 현재과정, byte[] 실행파일) {
        return үтәргә_команда(현재과정, 실행파일, new String[0], new String[0]);
    }

    public int үтәргә_команда(Процесс_VALUE 현재과정, byte[] 실행파일, String[] 인자, String[] 환경) {
        실행파일적재기.IMAGE IMAGE_VALUE;
        try {
            IMAGE_VALUE = 적재기.검사(실행파일);
        } catch (IllegalArgumentException Хата) {
            return -8;
        }
        if (인자 == null || 환경 == null || 인자.length > 16 || 환경.length > 16) {
            return -7;
        }
        for (실행파일적재기.өлеш_VALUE өлеш_VALUE : IMAGE_VALUE.구역들()) {
            if ((өлеш_VALUE.тамга_кую_VALUE() & 2) == 0 || өлеш_VALUE.үлчәмен_үзгәртү() == 0) {
                continue;
            }
            int 첫쪽 = өлеш_VALUE.адрес() / бит_идарәче.бит_зурлыгы;
            int 끝쪽 = (өлеш_VALUE.адрес() + өлеш_VALUE.үлчәмен_үзгәртү() + бит_идарәче.бит_зурлыгы - 1) / бит_идарәче.бит_зурлыгы;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int адрес = INDEX * бит_идарәче.бит_зурлыгы;
                try {
                    쪽관리.바이트읽기(현재과정.адрес_өлкә(), адрес);
                    쪽관리.범위개인쓰기(현재과정.адрес_өлкә(), адрес, бит_идарәче.бит_зурлыгы);
                } catch (IllegalStateException Хата) {
                    쪽관리.MAP_бит(현재과정.адрес_өлкә(), адрес, true);
                }
            }
            for (int INDEX = 0; INDEX < өлеш_VALUE.үлчәмен_үзгәртү(); INDEX++) {
                byte VALUE = өлеш_VALUE.종류() == 8 ? 0 : 실행파일[өлеш_VALUE.файл_урнаштыру() + INDEX];
                쪽관리.язу_байт_VALUE(현재과정.адрес_өлкә(), өлеш_VALUE.адрес() + INDEX, VALUE);
            }
        }
        현재과정.실행문맥설정(IMAGE_VALUE.Start_адрес(), 인자, 환경);
        현재과정.파일서술자().실행시닫기();
        return 0;
    }

    public void чыгу_кушымта(Процесс_VALUE 현재과정, int халәт_VALUE) {
        현재과정.Чыгу_кушымта(халәт_VALUE);
    }
}
