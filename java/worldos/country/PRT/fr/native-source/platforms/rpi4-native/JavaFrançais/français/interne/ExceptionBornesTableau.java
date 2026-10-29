// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionBornesTableau : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionBornesTableau extends ExceptionBornes {
    public ExceptionBornesTableau() { super(); }
    public ExceptionBornesTableau(String description) { super(description); }
    public String description() { return getMessage(); }
}
