# Hemeroteca Oberta

Módul de django per a la creació d'una hemeroteca digital per a revistes i periodisme
de proximitat

## Requeriments

1. python3.10.\*
2. tesseract-ocr
3. tesseract-ocr-{locale}

## Instal·lació

Primer necessitaràs un projecte de django instal·lat. Per crear-lo, podeu se

## Configuració

La configuració es definirà a l'arxiu `settings.py` de la vostre projecte.

1. HEMEROTECA_SEARCH_CONTENT: Variable lògica que indica si l'hemeroteca ha
   de suportar la funcionalitat de cerca dins el contingut. En cas que així
   sigui, el programari tesseract serà imprescindible per poder fer la ingesta
   de dades

2.

## Ingesta

Per poder realitzar la ingesta haureu d'executar la comanda:

```sh
python manage.py ingestion <cataleg> [--flush] [-v {0,1}]
```

El paràmetre **cataleg** haurà de ser la ruta a l'index del vostre catàleg.

## Catàleg

Els formats suportats per a aquest index són CSV i ODF. L'estructura d'aquest arxiu
haura de respectar el següent esquema:

| Arxiu | Número | Data | Secció | Títol | Firma | Pàgina |
| ----- | ------ | ---- | ------ | ----- | ----- | ------ |
| path  | int    | date | str    | str   | str   | int    |

### Camps de l'índex

1. Arxiu: Ruta relativa a l'arxiu PDF del número on apareix l'arxiu
2. Número: Numeració de les publicacions
3. Data: Data de la publicació en format `%m/%Y`
4. Secció: Nom de la secció en que apareix l'article (Opcional)
5. Títol: Títol de l'article
6. Firma: Firma de l'article (Opcional)
7. Pàgina: Pàgina en que apareix l'article (opcional)

Els camps opcionals poden restar buits, però la columna s'haurà de respectar.

## Desplegament
