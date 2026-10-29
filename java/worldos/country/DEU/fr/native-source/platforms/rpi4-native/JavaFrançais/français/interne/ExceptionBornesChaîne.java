// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionBornesChaîne : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionBornesChaîne extends ExceptionBornes {
    public ExceptionBornesChaîne() { super(); }
    public ExceptionBornesChaîne(String description) { super(description); }
    public String description() { return getMessage(); }
}
