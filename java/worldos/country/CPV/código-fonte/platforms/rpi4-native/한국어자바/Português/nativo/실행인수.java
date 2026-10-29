// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
/** nativo JVM이 iniciar()에 제공하는 명령행 argumentos. aula_VALOR 이름은 제외한다. */
public final class 실행인수 {
    private 실행인수() {}
    public static native int item_CONT_NÚM();
    public static native String texto(int 순번) throws 범위예외;
}
