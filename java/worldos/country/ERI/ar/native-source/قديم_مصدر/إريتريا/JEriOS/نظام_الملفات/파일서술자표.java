// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package إريتريا.JEriOS.نظام_الملفات;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ملف 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final نظام_الملفات.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(نظام_الملفات.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final نظام_الملفات نظام_الملفات;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(نظام_الملفات نظام_الملفات) {
        this.نظام_الملفات = نظام_الملفات;
    }

    public int فتح(String اسم) {
        نظام_الملفات.열린파일 열린파일 = نظام_الملفات.فتح(اسم);
        if (열린파일 == null) {
            return -2;
        }
        int فهرس = فارغ_فهرس(3);
        if (فهرس < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(فهرس), new 서술자(열린파일));
        return فهرس;
    }

    public int قراءة(int فهرس, byte[] يستلم_وجهة, int حجم) {
        서술자 إدخال_قيمة_962f286b = 서술자들.get(Integer.valueOf(فهرس));
        if (إدخال_قيمة_962f286b == null) {
            return -9;
        }
        if (حجم < 0 || حجم > يستلم_وجهة.length) {
            return -22;
        }
        int 남음 = إدخال_قيمة_962f286b.열린파일.بيانات.length - إدخال_قيمة_962f286b.열린파일.موضع;
        int يقرأ_يغير_الحجم = Math.min(حجم, Math.max(남음, 0));
        System.arraycopy(إدخال_قيمة_962f286b.열린파일.بيانات, إدخال_قيمة_962f286b.열린파일.موضع, يستلم_وجهة, 0, يقرأ_يغير_الحجم);
        إدخال_قيمة_962f286b.열린파일.موضع += يقرأ_يغير_الحجم;
        return يقرأ_يغير_الحجم;
    }

    public int نقل_منصب(int فهرس, int 거리, int يعرض_جذر) {
        서술자 إدخال_قيمة_962f286b = 서술자들.get(Integer.valueOf(فهرس));
        if (إدخال_قيمة_962f286b == null) {
            return -9;
        }
        int خلفية_قيمة;
        if (يعرض_جذر == 0) {
            خلفية_قيمة = 0;
        } else if (يعرض_جذر == 1) {
            خلفية_قيمة = إدخال_قيمة_962f286b.열린파일.موضع;
        } else if (يعرض_جذر == 2) {
            خلفية_قيمة = إدخال_قيمة_962f286b.열린파일.بيانات.length;
        } else {
            return -22;
        }
        int 새위치 = خلفية_قيمة + 거리;
        if (새위치 < 0) {
            return -22;
        }
        إدخال_قيمة_962f286b.열린파일.موضع = 새위치;
        return 새위치;
    }

    public int إغلاق(int فهرس) {
        서술자 إدخال_قيمة_962f286b = 서술자들.remove(Integer.valueOf(فهرس));
        if (إدخال_قيمة_962f286b == null) {
            return -9;
        }
        إدخال_قيمة_962f286b.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int فهرس, int 최소번호) {
        서술자 إدخال_قيمة_962f286b = 서술자들.get(Integer.valueOf(فهرس));
        if (إدخال_قيمة_962f286b == null) {
            return -9;
        }
        int رقم_جديد = فارغ_فهرس(최소번호);
        if (رقم_جديد < 0) {
            return -24;
        }
        إدخال_قيمة_962f286b.열린파일.참조수++;
        서술자들.put(Integer.valueOf(رقم_جديد), new 서술자(إدخال_قيمة_962f286b.열린파일));
        return رقم_جديد;
    }

    public int 지정복제(int فهرس, int رقم_جديد) {
        if (فهرس == رقم_جديد) {
            return 서술자들.containsKey(Integer.valueOf(فهرس)) ? فهرس : -9;
        }
        if (رقم_جديد < 0 || رقم_جديد >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(فهرس));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(رقم_جديد))) {
            إغلاق(رقم_جديد);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(رقم_جديد), new 서술자(원본.열린파일));
        return رقم_جديد;
    }

    public int 실행시닫기설정(int فهرس, boolean قيمة) {
        서술자 إدخال_قيمة_962f286b = 서술자들.get(Integer.valueOf(فهرس));
        if (إدخال_قيمة_962f286b == null) {
            return -9;
        }
        إدخال_قيمة_962f286b.실행시닫기 = قيمة;
        return 0;
    }

    public int 실행시닫기값(int فهرس) {
        서술자 إدخال_قيمة_962f286b = 서술자들.get(Integer.valueOf(فهرس));
        if (إدخال_قيمة_962f286b == null) {
            return -9;
        }
        return إدخال_قيمة_962f286b.실행시닫기 ? 1 : 0;
    }

    public ملف_معلومات معلومات_النظام(int فهرس) {
        if (فهرس >= 0 && فهرس <= 2) {
            return new ملف_معلومات(0, 0020666);
        }
        서술자 إدخال_قيمة_962f286b = 서술자들.get(Integer.valueOf(فهرس));
        if (إدخال_قيمة_962f286b == null) {
            return null;
        }
        return new ملف_معلومات(إدخال_قيمة_962f286b.열린파일.بيانات.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] رقم_قائمة = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer فهرس : رقم_قائمة) {
            서술자 إدخال_قيمة_962f286b = 서술자들.get(فهرس);
            if (إدخال_قيمة_962f286b != null && إدخال_قيمة_962f286b.실행시닫기) {
                إغلاق(فهرس.intValue());
            }
        }
    }

    public boolean أنظمة_المعلومات_فتح(int فهرس) {
        return 서술자들.containsKey(Integer.valueOf(فهرس));
    }

    public 파일서술자표 نسخة_قيمة() {
        파일서술자표 نتيجة = new 파일서술자표(نظام_الملفات);
        for (Map.Entry<Integer, 서술자> إدخال_قيمة_962f286b : 서술자들.entrySet()) {
            إدخال_قيمة_962f286b.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(إدخال_قيمة_962f286b.getValue().열린파일);
            새서술자.실행시닫기 = إدخال_قيمة_962f286b.getValue().실행시닫기;
            نتيجة.서술자들.put(إدخال_قيمة_962f286b.getKey(), 새서술자);
        }
        return نتيجة;
    }

    private int فارغ_فهرس(int 최소번호) {
        for (int فهرس = Math.max(0, 최소번호); فهرس < 최대서술자; فهرس++) {
            if (!서술자들.containsKey(Integer.valueOf(فهرس))) {
                return فهرس;
            }
        }
        return -1;
    }
}
