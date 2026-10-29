// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionRéférenceRéférenceNulle : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionRéférenceRéférenceNulle extends java.lang.NullPointerException {
    public ExceptionRéférenceRéférenceNulle() { super(); }
    public ExceptionRéférenceRéférenceNulle(String description) { super(description); }
    public String description() { return getMessage(); }
}
