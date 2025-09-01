import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;


public class Calc {
public static void main(String[] args) throws Exception {
java.io.InputStream is = System.in;
ANTLRInputStream input = new ANTLRInputStream(is);
labeldExprLexer lexer = new labeldExprLexer(input);
CommonTokenStream tokens = new CommonTokenStream(lexer);
labeldExprParser parser = new labeldExprParser(tokens);
ParseTree tree = parser.prog();
EvalVisitor eval = new EvalVisitor();
eval.visit(tree);
}
}
