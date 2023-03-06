# Status dos testes

![git status](http://3.129.230.99/svg/jamessonlps/logi-comp)

## EBNF

```ts
EXPRESSION = TERM, { ("+" | "-"), TERM };
TERM = FACTOR, { ("*" | "/"), FACTOR };
FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;
```
## Diagrama Sintático

<img src="./diagrama.png" alt="Diagrama sintático" />