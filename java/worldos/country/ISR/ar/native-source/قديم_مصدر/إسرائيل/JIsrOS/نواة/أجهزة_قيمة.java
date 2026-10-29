// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package إسرائيل.JIsrOS.نواة;

/** Java 관리 커널과 CPU 고유 رمز_قيمة_f3cd31ee 사이의 유일한 경계다. */
public interface أجهزة_قيمة {
    void 직렬출력(String محتوى_قيمة);

    int يقرأ_منفذ_بايت(int أجهزة_رقم_المنفذ);

    void كتابة_منفذ_بايت(int أجهزة_رقم_المنفذ, int قيمة);

    void 중앙처리장치멈춤();
}

