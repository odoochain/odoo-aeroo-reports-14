# Aeroo Reports

Aeroo Reports for Odoo v11.0

## Installation

 - Install the python library aerolib available at https://github.com/aeroo/aeroolib.git
    - git clone https://github.com/aeroo/aeroolib.git
    - cd aerolib
    - python setup.py install

 - Install the python library Genshi
    - pip install Genshi

 - Install libreoffice
    - apt-get install libreoffice, libreoffice-writer, openjdk-7-jre

## Translations

The main difference between this fork of Aeroo reports and other similar reporting
engines for Odoo is the way it handles translations.

Most engines implement the standard way of Odoo to translate a document.
This implies that the template is writen in english and that all terms in the template
are stored in the database (as model ir.translation).
Every time you change a word in the template, you must update the translations and
test that it is translated correctly. Therefore, it is very inconvenient for someone
non-technical to maintain the report.

The philosophy in this fork of Aeroo is that the person who uses the report
(i.e. the accountant, the office manager, etc.) is the one who maintains the report,
not the developper.

## Different template per language

For each language that the report must support, you may create a template and bind it to the language.

* Go to: Settings -> Technical -> Reports -> Aeroo Reports
* Select your report
* In the field 'Template Source', select 'Different Template per Language'
* In the field 'Templates by Language', add a line that maps your language to a template.

If a template is not available for a language and a user tries to print the report in that language,
the system will raise an exception saying that the report is unavailable for the given language.

The language used for printing the template must be parametrized in the field 'Language Evaluation'
(by default: o.partner_id.lang).

## Numbers and Currencies

Aeroo defines 2 helpers for formatting number field values in the language of the report.

* format_decimal
* format_currency

### Exemple for format_decimal

```python
format_decimal(o.amount_total)
```

If the report is printed in Canada French, the output will look like:

```
1 500,00
```

### Exemple for format_currency

```python
format_currency(o.amount_total, o.currency_id)
```

If the report is printed in Canada French, the output will look like:

```
1 500,00 $US
```

### Force a number format

Both format_decimal and format_currency functions accept an optional `amount_format` parameter.

This parameter accepts a number format using the variables documented on the babel website:

http://babel.pocoo.org/en/latest/numbers.html#pattern-syntax

## Date and Time

Aeroo defines 2 helpers for formatting date and datetime field values in the language of the report.

* format_date
* format_datetime
* today
* now

The variables that you can use in these functions are documented on the babel website:

http://babel.pocoo.org/en/latest/dates.html#date-fields

### Exemple for format_date

```python
format_date(o.date_invoice, 'dd MMMM yyyy')
```

If the report is printed in French, the output will look like:

```
06 avril 2018
```

### Exemple for format_datetime

```python
format_datetime(o.confirmation_date, 'dd MMMM yyyy hh:mm a')
```

If the report is printed in French, the output will look like:

```
6 avril 2018 10:34 AM
```

### Exemple for today

The function today is the same as format_date, but with the current date in the user's timezone.

```python
today('dd MMMM yyyy')
```

Suppose we are on the 6 of April 2018 and the report is printed in French, the output will look like:

```
06 avril 2018
```

### Exemple for now

The function now is the same as format_datetime, but with the current time in the user's timezone.

```python
now('dd MMMM yyyy hh:mm a')
```

Suppose we are on the 6 of April 2018, 10:34 AM and the report is printed in French, the output will look like:

```
06 avril 2018 10:34 AM
```

## Grouping Rows

It is possible to group rows to display in a table.

In the following example, the invoice lines are grouped by per product category:

```xml
<for each="(category, lines) in group_by(o.invoice_line_ids, lambda line: line.product_id.categ_id)">
```

Each tuple contains:

1. the groupment key
2. the records matching this groupment key

### Grouping Rows in a Particular Order

By default, the groupment keys are not sorted in any particular order.

Usually, we will require to sort the grouped records by some criteria.
This can be done using the argument ``sort`` of the ``group_by`` function.

The ``sort`` argument expects a function.
This function takes as argument the groupment key.

In the following example, the groupment keys (the product categories) are sorted by their ``Display Name``.

```xml
<for each="(category, lines) in group_by(o.invoice_line_ids, lambda line: line.product_id.categ_id, sort=lambda category: category.display_name)">
```

Here is a preview on how to organize the for/each statements in your libreoffice template.

![Group By Example](report_aeroo/static/description/libreoffice_writer_group_by.png?raw=true)

## Generate Report From List View

In the form view of your Aeroo report, the checkbox `Generate Report From Record List`
allows to generate a report from a list view.

![Report From List View](report_aeroo/static/description/report_from_list_view.png?raw=true)

In the Libreoffice template, the variable `o` (which contains a single record) is replaced with a new variable `objects`
which contains a record set. This variable can be used in a for loop to iterate over all selected records.

### Language Evaluation For List Reports

When generating a report from a list view, the first item in the selected records is used when evaluating
the language and the company of the report to generate.

The fields `Language Evaluation` and `Company Evaluation` can not use the variable `objects`.
Those fields still use a variable `o` (which contains the first record in the selection).


## Creating a Template

### Spreadsheets

In a spreadsheet, you must insert hyperlinks in order to display data dynamically.

Go to: Insert -> Hyperlink, then in the field URL, write python://your-python-expression

Displaying each element of a list on a seperate row:

|   | A                                        | B                        |
|---|------------------------------------------|--------------------------|
| 1 | Description                              | Unit Price               |
| 2 | python://for each="line in o.order_line" |                          |
| 3 | python://line.name                       | python://line.price_unit |
| 4 | python:///for                            |                          |


## Insert An Image In A Report

In the template, you must insert a frame in order to display an image dynamically.

Go to: Insert -> Frame -> Frame...
In the 'Type' tab:
* For the Width, check Relative To, then choose a width percentage.
* For the Height, check Relative To, uncheck AutoSize, then choose a height percentage.

You can also resize with more precision the image/frame by selecting it and dragging
with the mouse its corner/side.

In the 'Options' tab:
* In the field Name write image:asimage(o.image)

## Insert A Report In An Email Template

The `Aeroo Report` module adds an easy way to attach reports to an email template.

![Email Template Form](report_aeroo/static/description/email_template_form.png?raw=true)

The difference between this feature and a report attachment from `Advanced Settings / Optional report to print and attach` is:

1. You may attach more than one aeroo reports.
2. You do not need to redefine the name of the attachment in the email template.
   The attachment name will be the one defined on the report.

## Attachment Names

The name of a rendered Aeroo report is similar to the name of an attachment in an email template.

The same functions available from your Aeroo template are available for the name of the attachment.

![Filename](report_aeroo/static/description/filename.png?raw=true)

### Invoice Attachment Name Example

Here is a complex example for the attachment name of an invoice.

```
${o.company_id.display_name} - ${'Invoice' if o.type == 'out_invoice' else 'Refund'} - ${format_date(o.date_invoice, 'yyyy-mm-dd')}
```

The result for a given invoice could be the following:

`Your Company - Invoice - 2018-07-12.pdf`

### Different Filename per Language

In order to have a different filename based on the context of the report, you may check `Different Filename per Language`.

Make sure when using this option to add one entry for each active language.

![Filename per Language](report_aeroo/static/description/filename_per_language.png?raw=true)
