// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionÉtatValeurFilExécution : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionÉtatValeurFilExécution extends java.lang.IllegalThreadStateException {
    public ExceptionÉtatValeurFilExécution() { super(); }
    public ExceptionÉtatValeurFilExécution(String description) { super(description); }
    public String description() { return getMessage(); }
}
