// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionExécution : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionExécution extends java.lang.RuntimeException {
    public ExceptionExécution() { super(); }
    public ExceptionExécution(String description) { super(description); }
    public String description() { return getMessage(); }
}
