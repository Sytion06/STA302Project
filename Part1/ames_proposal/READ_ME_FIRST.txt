STA302 PART 1: DATASET DECISION AND PROPOSAL PACKAGE
Prepared October 29, 2026

RECOMMENDATION
Choose Ames Housing for the most manageable, well-documented regression project.
The original downloaded data have 2,930 rows and 82 fields. The proposed model has
nine distinct predictors, including natural categories, plus an interaction. It
retains 2,928 complete observations. The question targets differences in adjusted
living-area slopes across dwelling types, rather than generic price prediction.

There is an assignment ambiguity: page 3 discourages educational datasets, but
page 6 explicitly recommends Ames. Ames really was curated for teaching, although
its underlying records are municipal administrative data. Do not disguise this.
Confirm that the explicit recommendation permits its use before final submission.
The recommendation here is based on that explicit listing; work need not wait.

COMPARISON OF THE FIVE PROVIDED OPTIONS
1. AMES HOUSING - strongest overall fit for this course and deadline.
   Clear continuous response, ample observations, interpretable predictors,
   natural categorical interaction, documented collection, and relevant literature.
   Actual files inspected and preliminary model run. Pitfalls: unusual sales,
   sparse neighborhoods, spatial dependence, and the eligibility ambiguity above.
   Source: https://cran.r-project.org/web/packages/AmesHousing/AmesHousing.pdf
   Original paper: https://jse.amstat.org/v19n3/decock.pdf

2. NHANES - strong alternative if the group prefers public health and is willing
   to handle survey methodology. The linked package documents 75 shared variables,
   20,293 raw records and a 10,000-row resampled teaching version. Complex sampling,
   weights, subgroup restrictions and missingness complicate ordinary regression.
   Resampled rows must not be assumed to be 10,000 distinct independent people.
   Native CDC files would give stronger provenance, but require additional work.
   Documentation reviewed; individual records were not downloaded here.
   https://www.stat.ethz.ch/CRAN/web/packages/NHANES/refman/NHANES.html

3. AIRBNB - potentially a good price-response project, but currently less certain.
   The exact data.world link was inaccessible to the web tool and the assignment
   says it requires a free account. Its row count, variables and collection details
   could not be verified. Inspect those before selecting it. Typical issues to check
   include asking versus realized prices, multiple listings per host, missing
   reviews, location and repeated snapshots. These are screening concerns, not
   verified defects in this particular file. Do not quietly substitute another city.
   https://data.world/cannata/gaairbnb

4. NBA PLAYER DATA - interesting if the team is invested in basketball, but the
   exact Kaggle page returned no readable data documentation. Row count and field
   availability remain unverified. Check repeated player-seasons and team clustering;
   1,000 rows do not automatically mean 1,000 independent players. Avoid predicting
   points using variables that algebraically reconstruct points. These are risks
   to investigate, not findings from downloaded records.
   https://www.kaggle.com/datasets/davra98/nba-players-20162019

5. MILLION SONG - least practical for this deadline. Official documentation offers
   one million tracks and a 10,000-track subset, but the full download is about
   280 GB and even the subset is 1.8 GB compressed. Features/metadata, not audio,
   are provided. Extraction and a defensible continuous outcome need more setup;
   repeated artists can complicate independence. Documentation reviewed, not records.
   https://millionsongdataset.com/

This is a ranking of project suitability and implementation risk, not an empirical
data-quality ranking of five downloaded datasets. Only Ames was analyzed row by row.

WHAT IS INCLUDED
- proposal_draft.pdf: reviewable draft with real R results and all coefficient CIs.
- proposal.Rmd: editable proposal and embedded, self-contained analysis code.
- analyze.R: base-R analytical script, already executed successfully.
- build_proposal.py: builds the supplied PDF and Rmd using the saved R outputs.
- data/AmesHousing_original.txt: original journal download, unchanged.
- data/AmesHousing_original.csv: all original rows/columns, tabular CSV conversion.
- data/AmesHousing_cleaned.csv: model variables plus audit identifiers and sale month.
- data/DataDocumentation.txt: original codebook.
- data/ames_raw.rda: unused fallback download from the linked package's repository.
- outputs/: numeric and categorical summaries, missingness, full coefficients,
  derived slopes, interaction test, influence values, plots, model object, log,
  metrics, and section word counts.

HOW TO RUN
Open an R session with this folder as its working directory and run:
  source('analyze.R')
No non-base R packages or network access are required for this analysis.
To knit proposal.Rmd, use RStudio with knitr, rmarkdown, Pandoc and a working XeLaTeX
installation. The Rmd embeds the same analysis instead of depending on analyze.R.
Keep the data subfolder beside it. The supplied PDF was rendered using ReportLab;
the Rmd has not been knitted here because knitr/rmarkdown are not installed in the
detected R library. All analytical code was executed using R 4.6.1.

INTERPRETING THE PRELIMINARY MODEL
The main area coefficient is the slope for detached single-family houses. Each
interaction is another type's slope difference relative to detached houses. Sum
the main slope and interaction to obtain that type's slope. Standard errors for
these sums use the full coefficient covariance matrix, not the sum of the two SEs.
Building main effects compare types at 1,500 square feet because area is centered.
The intercept uses age, quality, basement, garage and lot values of zero; it is not
a realistic house valuation. Year is categorical, not a forced linear time trend.
The ordinal quality score is provisionally numeric; review that assumption later.

The residual plots show assumption problems, so conventional CIs and the partial
F-test are provisional. The singleton neighborhood has leverage one and undefined
standardized diagnostics; the R warnings are expected and disclosed in the report.
An age of -1 is flagged, not silently recoded. No outliers were deleted and no
variance/linearity corrections were applied, in accordance with Part 1 instructions.

BEFORE SUBMISSION
Use actual names and honest descriptions of completed contributions. Confirm the
Ames exception with the TA. The literature summary draws on accessible article
abstracts/text and bibliographic records; read all three substantive papers in full
through UofT before adopting the interpretations. The spatial paper supports
location adjustment, not direct proof of a dwelling-type interaction. Novelty is
a proposed focused extension; an exhaustive novelty search has not been performed.
Match ethics terminology to Module 3. Confirm the exact end-of-November deadline.
Review or remove the working-draft notes/checklist and re-export the final PDF.

Proposal deadline: November 5, 2026, 11:59 p.m. Toronto time.
The assignment also provides an NQA extension to November 8, 11:59 p.m. using a
separate dropbox, and says not to submit before the original deadline if using it.
The team's working schedule targets the ordinary November 5 deadline.

Required submission: teamwork-agreement PDF, proposal PDF, RMD code; original and
cleaned CSVs in UofT OneDrive with 'anyone in UofT with the link' access, and the link
in the Quercus submission comment. Only one teammate submits. No external upload,
message or course submission has been made by this work.
