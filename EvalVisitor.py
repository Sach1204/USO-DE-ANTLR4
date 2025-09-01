import math
from labeldExprVisitor import labeldExprVisitor
from labeldExprParser import labeldExprParser

class EvalVisitor(labeldExprVisitor):
    def __init__(self):
        self.memory = {}
        self.use_degrees = True   # por defecto trabajamos en grados

    # --- Salida de resultados ---
    def visitPrintExpr(self, ctx:labeldExprParser.PrintExprContext):
        value = self.visit(ctx.expr())
        print(value)
        return value

    # --- Asignación de variables ---
    def visitAssign(self, ctx:labeldExprParser.AssignContext):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[name] = value
        return value

    def visitId(self, ctx:labeldExprParser.IdContext):
        name = ctx.ID().getText()
        return self.memory.get(name, 0)

    def visitInt(self, ctx:labeldExprParser.IntContext):
        return int(ctx.INT().getText())

    def visitDouble(self, ctx:labeldExprParser.DoubleContext):
        return float(ctx.DOUBLE().getText())

    # --- Operadores básicos ---
    def visitMulDiv(self, ctx:labeldExprParser.MulDivContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.op.type == labeldExprParser.MUL:
            return left * right
        if right == 0:
            raise ZeroDivisionError("Error: intento de división entre cero")
        return left / right

    def visitAddSub(self, ctx:labeldExprParser.AddSubContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.op.type == labeldExprParser.ADD:
            return left + right
        return left - right

    def visitUnaryMinus(self, ctx:labeldExprParser.UnaryMinusContext):
        return -self.visit(ctx.expr())

    def visitParens(self, ctx:labeldExprParser.ParensContext):
        return self.visit(ctx.expr())

    # --- Exponente ---
    def visitPow(self, ctx:labeldExprParser.PowContext):
        base = self.visit(ctx.expr(0))
        exp = self.visit(ctx.expr(1))
        return math.pow(base, exp)

    # --- Factorial ---
    def visitFact(self, ctx:labeldExprParser.FactContext):
        val = self.visit(ctx.expr())
        return math.factorial(int(val))

    # --- Funciones matemáticas ---
    def visitFunction(self, ctx:labeldExprParser.FunctionContext):
        func = ctx.ID().getText()
        arg = self.visit(ctx.expr()) if ctx.expr() else None

        if func == "sin": return math.sin(self._angle(arg))
        if func == "cos": return math.cos(self._angle(arg))
        if func == "tan": return math.tan(self._angle(arg))
        if func == "sqrt": return math.sqrt(arg)
        if func == "ln": return math.log(arg)
        if func == "log": return math.log10(arg)
        if func == "deg":
            self.use_degrees = True
            return 0
        if func == "rad":
            self.use_degrees = False
            return 0
        return 0

    # --- Conversión entre grados y radianes ---
    def _angle(self, value):
        if self.use_degrees:
            return math.radians(value)
        return value
