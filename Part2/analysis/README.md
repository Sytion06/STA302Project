# Guided Ames analysis

`analysis.Rmd` is the authoritative, worksheet-style report. Edit it directly.
It interleaves explanations, short executable chunks, numbered tables, figures
and interpretation. All analytical calculations start from the Part 1 originals;
no saved table or model from Part 2 is required as an input.

## Report structure

The main report has five sections: data; model development; diagnostics, sensitivity
and model selection; final model and results; and conclusions, limitations and
improvements. Candidate models remain candidates until the diagnostic, sensitivity
and complexity comparisons are complete. The final selection balances the question,
residual evidence, parsimony and stability; it is not a claim that assumptions are
fully satisfied or that overfitting has been ruled out.

The same-sample, log-response AIC comparison includes two additional simpler-rating
candidates with type-specific curves. It is exported to
`worksheet_outputs/model_complexity.csv`. All 24 tables and 20 figures are numbered
in reading order. Unresolved assumptions and selection/validation limitations are
collected in the last main section.

## Render

```r
rmarkdown::render("analysis.Rmd")
# Optional HTML:
rmarkdown::render("analysis.Rmd", output_format = "html_document")
```

PDF is the default (XeLaTeX, Pandoc, rmarkdown, knitr and recommended MASS).
Run from this directory or pass the full Rmd path, as VSCode Knit does.
R Markdown uses the document directory for its relative input paths.
The PDF hides all source code while retaining results, tables and figures. HTML shows analytical code. Session setup and file-saving safeguards
are hidden; the latter remain in the Rmd's export appendix.

## Files and maintenance

- `analysis.pdf` and `analysis.html`: rendered directly from this Rmd.
- `worksheet_outputs/`: fresh contrasts, diagnostics, coefficients and model snapshots.
- `audit/worksheet_reference_map.json`: table/figure numbering for this revision.
- `audit/before_worksheet_revamp/`: previous Rmd/PDF and maintenance files.
- `analyze.R`, `tables/`, `figures/`, prose `.md` files: retained legacy analytical
  evidence. They no longer generate or synchronize the current Rmd.
- `build_documents.py`: retired with a fail-fast message to prevent accidental
  overwriting of the revised document. Do not use the old build route.

Tables and figures now appear where discussed. Caption numbers follow document
order; when adding/removing outputs, update the corresponding prose references.
The same R code produces the displayed results, not a screenshot or old CSV.

## Verification

The final Rmd chunk checks the reproduced baseline, primary F statistic,
diagnostic counts and unchanged original input. The revision verification also
compares all contrast estimates and intervals against the preserved prior exports.
Run `python verify_outputs.py` after rendering to check the revised outputs.
Native render logs and checks are saved under `audit/worksheet_*`.

CSV and RDS exporters retain staged writes. A locked model snapshot is saved to a
unique filename and recorded in `worksheet_outputs/model_export_manifest.csv`.
A persistently locked CSV yields an explicit error rather than accepting stale data.

## Scope and provenance

AI-assisted starting draft for team review. Simplifying its code does not change
its provenance or establish permission for assessed use. The course AI-use rule,
Ames eligibility question, missing feedback/Module 10 material and two literature
full-text checks remain documented in the report. No poster, recording, submission
or team contribution record has been created. Original data and Part 1 are preserved.
