// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionBornes : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionBornes extends java.lang.IndexOutOfBoundsException {
    public ExceptionBornes() { super(); }
    public ExceptionBornes(String description) { super(description); }
    public String description() { return getMessage(); }
}
