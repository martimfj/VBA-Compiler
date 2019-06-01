Function Soma(x as Integer, y as Integer) as Integer
    Dim a as Integer
    print c
    a = x + y
    Print a
    Soma = a
End Function

Sub Main()
    Dim a as Integer
    Dim b as Integer
    Dim c as Integer
    c = 10
    a = 3
    b = Soma(a, 4)
    Print a
    Print b
End Sub