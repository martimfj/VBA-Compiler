sub main()

dim savings as integer
dim price1 as integer
dim price2 as integer
dim quantity as integer
dim flag as boolean

price1 = 154
price2 = 352
quantity = 6
flag = true

if price1 > price2 then
    savings = price1-price2
    print savings
else
    savings = price2-price1
    print savings
end if

while flag
    if quantity > 0 then
        print savings * quantity
        quantity = quantity - 1
    else
        flag = false
    end if
wend

end sub
