#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Martim Ferreira Jośe - Logíca da Computação (Aula 1)

import re


def sanitization(value):
    return re.split('(\W)', value.replace(" ", ""))


def main():
    print("Enter expression: ")
    data = sanitization(input())

    for i in range(len(data)):
        if data[i-1] == "-":
            data[i] = "-" + data[i]

    remove_operator = list(
        map(int, filter(lambda x: x != "+" and x != "-", data)))

    print(sum(remove_operator))


if __name__ == "__main__":
    main()
