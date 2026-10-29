from pathlib import Path
import csv, re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
def rows(name):
    with (OUT/name).open(newline='') as f: return list(csv.DictReader(f))

intro='''Among residential properties sold in Ames, Iowa, during 2006-2010, does the association between above-ground living area and sale price differ by dwelling type after adjustment for lot area, construction quality, age, basement area, garage capacity, neighborhood, and sale year? Sale price is the recorded transaction amount in nominal US dollars. Our target is the adjusted dollar difference associated with 100 additional square feet within each dwelling type, rather than the causal return from enlarging a home.

Housing attributes need to be considered jointly. Mathur (2019), studying King County, Washington, found that construction quality and maintenance were associated with higher prices; a medium-quality home sold for approximately 25% more than a low-quality home. This supports adjustment for quality, while its maintenance findings motivate considering condition in subsequent models. Goodman and Thibodeau (1995), analyzing nearly 8,500 Dallas single-family transactions, found nonlinear depreciation and age-related heteroskedasticity. Their findings motivate including age and checking both functional form and residual variance. Fik et al. (2003), studying the Tucson housing market, found that location and housing attributes jointly influenced prices in ways that simple location indicators did not fully capture. This motivates neighborhood adjustment and cautions that such adjustment may leave spatial dependence.

Together, these studies support an adjusted analysis while warning against a universal price-per-square-foot rule. Our extension asks whether the living-area slope varies across five recorded dwelling types in Ames. We hypothesize that differences in layout and shared structures make a common slope too restrictive. This is a proposed local extension, not a claim that dwelling-type interactions have never been studied.

Multiple linear regression estimates conditional mean-price differences while adjusting for several characteristics simultaneously. A correlation or comparison of group means cannot isolate the adjusted area association or test whether slopes differ. Type-specific slopes, confidence intervals, and a joint partial F-test of the four interaction coefficients answer the question. The outcome is sufficiently continuous for this approach, subject to diagnostic assessment. Historical housing researchers and appraisers studying comparable-property adjustments could benefit; the estimates are not current valuations and should not be transferred directly to Toronto or contemporary Ames.'''

data='''We downloaded the original tab-delimited data and codebook from the Journal of Statistics Education archive (De Cock, 2011). The Ames City Assessor's Office originally recorded property characteristics and sales for valuation and assessment. De Cock obtained a records-system extract, removed specialized assessment variables and nonresidential records, and retained the latest transaction for repeatedly sold properties. His public release contains 2,930 properties and 82 fields and was curated for regression teaching.

The analysis uses 2,928 complete records, excluding one missing basement area and one missing garage capacity. Sale price has mean $180,841, median $160,000, standard deviation $79,890, and range $12,789-$755,000. Its many possible values support a continuous response; right skew does not itself invalidate regression, whose assumptions concern conditional errors. Unique parcel identifiers reduce repeated-property dependence, but neighboring homes and common market conditions can still produce dependent errors.

Nine predictors enter the model: living area, dwelling type, lot area, overall quality, age at sale, basement area, garage capacity, neighborhood, and sale year. Dwelling type and neighborhood are nominal; sale year is a factor. Quality is provisionally treated as a numerical 1-10 score, imposing equal increments. Living area is measured per 100 square feet and centered at 1,500 square feet; lot area is per 1,000 square feet and basement area per 100 square feet. These unit changes do not repair model assumptions.

The living-area-by-dwelling-type interaction allows different slopes for detached homes, converted two-family homes, duplexes, and interior/end-unit townhouses. These are existing categories, so no arbitrary numerical cutoffs are needed. Figure 2 displays the adjusted slopes; differing layouts provide the substantive motivation.'''

ethics='''Administrative provenance, a published codebook, and a reproducible cleaning record support traceability and measurement transparency. Trustworthiness nevertheless depends on fitness for purpose: assessor quality ratings are subjective, one computed age is negative, and the released sample contains only sold properties from one city and period. Public availability alone does not establish accuracy or representativeness.

The curator obtained the records from the Assessor's Office and publicly released a research dataset. We have not verified individual homeowner consent, so we should not claim that every owner consented to this secondary use. Parcel identifiers can link records to addresses and owners; we retain them only for reproducibility and duplicate checks, do not perform identity linkage, and report aggregate findings. Restrict course-data sharing to the required UofT audience.

Neighborhood coefficients may reflect historical inequalities and omitted amenities. They must not be interpreted as intrinsic community quality or used to justify discriminatory lending or pricing. We will describe associations and uncertainty, avoid causal renovation advice, and acknowledge limited geographic and temporal generalizability. [Replace or connect these concepts to the exact Module 3 terminology before submission.]'''

results='''The untransformed preliminary model uses nine predictors and the four living-area interaction coefficients (46 coefficients including the intercept). Adjusted R-squared is 0.8388 and residual standard error is $32,074. Table 2 reports every coefficient with its conventional OLS standard error and 95% confidence interval.

For detached homes, 100 additional square feet is associated with $4,860 higher mean price (95% CI $4,507-$5,212), holding the other predictors fixed. Corresponding slopes are $2,419 for converted two-family homes, $1,900 for duplexes, $1,832 for interior townhouses, and $6,042 for end-unit townhouses. The interaction block has F(4,2882)=9.20, p=2.22e-7. These are provisional model-based comparisons; the diagnostics undermine conventional inferential calibration.

Figure 1 shows curved residual means and increasing spread at high fitted prices, suggesting imperfect linearity and unequal variance. The scale-location trend reinforces the latter. Strong Q-Q tail departures contradict normal errors, with several extreme negative residuals. Cook's distance reaches 0.530. Landmrk has one property and leverage one; its standardized residual and Cook's distance are undefined and omitted from relevant diagnostic panels. The design matrix is full rank, but this does not imply stable estimates or negligible collinearity. Sale-time residuals show no strong smooth trend; they cannot establish independence, especially with possible neighborhood dependence.

The positive quality coefficient ($15,672 per rating point) is directionally consistent with Mathur (2019), although scales and populations differ. Age has a negative linear coefficient ($404 per year), while the residual-age plot shows especially large spread among newer properties. This does not reproduce a simple increasing-variance-with-age pattern from Dallas and reinforces the need for local diagnostics. Neighborhood adjustment follows Fik et al. (2003), but cannot establish absence of spatial effects. No transformations, rare-level pooling, or influential-case deletions have been applied.'''

plan='''Retain living area, dwelling type, and their interaction because they define the question; retain neighborhood and sale year as contextual controls. Preserve all main effects whenever an interaction is included. Compare scientifically justified nested specifications using partial F-tests once assumptions are reasonably supported, and use adjusted R-squared as supporting rather than decisive evidence. Avoid automatic elimination of individual factor levels or selection solely by p-values. Consider adding overall condition and remodeling information, motivated by maintenance research, while checking redundancy among structural measures.

Recheck residual-versus-fitted, Q-Q, scale-location, leverage, and residual-age/time plots after every substantive revision. The fan-shaped spread suggests considering log sale price; curvature suggests quadratic age or living-area terms. Compare diagnostic improvement and interpretability rather than assuming a log transform fixes everything. Investigate the negative age and unusual large-property transactions against the codebook before any correction or exclusion. Assess rare-neighborhood instability, possible collinearity, and neighborhood dependence; discuss methods beyond course scope with the TA. Document sensitivity analyses rather than removing observations to achieve significance.

Proposed schedule (the final submission is at the end of November; confirm the exact date): October 30-31, [Member A] and [Member B] verify sources and data. November 1-3, [Member C] checks code and [Member D] checks interpretation. November 4, all members review; November 5, [Submitter] submits the proposal. November 9-15, [Members A/C] investigate diagnostics and compare revisions. November 16-20, [Members B/D] finalize interpretation and create the poster. November 21-25, all members rehearse and record the presentation. November 26-28, all members audit reproducibility and submission files, leaving a buffer before the confirmed deadline. Combine roles if the team has fewer than four members.'''

refs=[
"De Cock, D. (2011). Ames, Iowa: Alternative to the Boston housing data as an end of semester regression project. Journal of Statistics Education, 19(3). https://doi.org/10.1080/10691898.2011.11889627",
"Fik, T. J., Ling, D. C., & Mulligan, G. F. (2003). Modeling spatial variation in housing prices: A variable interaction approach. Real Estate Economics, 31(4), 623-646. https://doi.org/10.1046/j.1080-8620.2003.00079.x",
"Goodman, A. C., & Thibodeau, T. G. (1995). Age-related heteroskedasticity in hedonic house price equations. Journal of Housing Research, 6(1), 25-42. https://www.jstor.org/stable/24825889",
"Mathur, S. (2019). House price impacts of construction quality and level of maintenance on a regional housing market: Evidence from King County, Washington. Housing and Society, 46(2), 57-80. https://doi.org/10.1080/08882746.2019.1601928"
]
captions={
'summary':'Table 1. Complete-case summaries. Prices and areas have long upper tails. Original missing counts: basement area 1, garage capacity 1; all other selected variables 0. One age equals -1; retain for investigation. Dwelling types are imbalanced; Landmrk has one observation.',
'diagnostics':'Figure 1. Preliminary model diagnostics. Curvature, unequal spread, heavy tails, and influential observations warrant investigation. Labels identify original row numbers; the leverage-one case is omitted from standardized panels.',
'coefficients':'Table 2. Full preliminary model, USD. References: detached home, North Ames (NAmes), 2006. Dwelling-type contrasts are at 1,500 square feet. Interactions are slope differences per 100 square feet. Conventional intervals assume the model conditions hold.',
'interaction':'Figure 2. Observed prices and adjusted living-area slopes by dwelling type. Intervals are conventional 95% OLS intervals; assumption violations limit inference.'}

# Correct the residual standard error from the stored R fit log rather than rounded display.
# R log prints four significant figures; recover exact value via a compact CSV from R.
metrics=rows('metrics.csv')[0]
results=results.replace('$32,074',f"${float(metrics['sigma']):,.0f}")
sections={'Introduction':intro,'Data description':data,'Ethics discussion':ethics,'Preliminary results':results,'Plan':plan}
wordcounts={k:len(v.split()) for k,v in sections.items()}
wordcounts['Preliminary results including captions']=len((results+' '+captions['diagnostics']+' '+captions['coefficients']+' '+captions['interaction']).split())
(OUT/'word_counts.txt').write_text('\n'.join(f'{k}: {v}' for k,v in wordcounts.items()),encoding='utf-8')
assert wordcounts['Introduction']<=400 and wordcounts['Data description']<=300
assert wordcounts['Ethics discussion']<=200 and wordcounts['Plan']<=300
assert wordcounts['Preliminary results including captions']<=400

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyCustom',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallCustom',fontName='Helvetica',fontSize=8,leading=10,spaceAfter=6))
styles.add(ParagraphStyle(name='CellCustom',fontName='Helvetica',fontSize=7.8,leading=9.8))
styles.add(ParagraphStyle(name='CoefCell',fontName='Helvetica',fontSize=7.2,leading=8.5))
styles['Title'].textColor=colors.HexColor('#173f5f')
styles['Heading1'].textColor=colors.HexColor('#173f5f')
story=[]
def para(s,style='BodyCustom'): return Paragraph(html.escape(s),styles[style])
def prose(s):
    for p in s.split('\n\n'): story.append(para(p))
def heading(s): story.append(Paragraph(s,styles['Heading1']))
def table(data,widths,small=True):
    t=Table([[para(str(x),'CellCustom' if small else 'CoefCell') for x in r] for r in data],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#173f5f')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f7f9')]),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    if not small:t.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
    story.append(t)

story.append(Paragraph('Does the value of living space vary by dwelling type?',styles['Title']))
story.append(para('STA302 Part 1 | Ames Housing | Working proposal | Due November 5, 2026','SmallCustom'))
story.append(para('Team review required: fill contribution placeholders, align ethics language with Module 3, and confirm Ames eligibility because the assignment both recommends it and discourages educational datasets.','SmallCustom'))
heading('Contributions')
prose('[Member A]: [actual contribution]. [Member B]: [actual contribution]. [Member C]: [actual contribution]. [Member D]: [actual contribution]. Record completed work, not merely assigned roles.')
heading('Introduction');prose(intro)
story.append(PageBreak());heading('Data description');prose(data)
heading('Ethics discussion');prose(ethics)
story.append(PageBreak());heading('Variable summaries')
story.append(para(captions['summary'],'SmallCustom'))
labels={'SalePrice':'Sale price (USD)','Living100':'Living area (100 sq ft)','Lot1000':'Lot area (1,000 sq ft)','Quality':'Quality (1-10)','Age':'Age (years)','Basement100':'Basement (100 sq ft)','GarageCars':'Garage capacity (cars)'}
numeric=[['Variable','Mean (SD)','Median [Q1, Q3]','Min - Max']]
for r in rows('numeric_summary.csv'):
    f=lambda k:f"{float(r[k]):,.2f}"
    numeric.append([labels[r['Variable']],f"{f('Mean')} ({f('SD')})",f"{f('Median')} [{f('Q1')}, {f('Q3')}]",f"{f('Min')} - {f('Max')}"])
table(numeric,[130,115,155,104]);story.append(Spacer(1,10))
catrows=rows('categorical_summary.csv')
cats=[['Categorical variable','Level: n (%)']]
for variable in ['Building','Neighborhood','SaleYear']:
    entries=[f"{r['Level']}: {r['N']} ({float(r['Percent']):.2f}%)" for r in catrows if r['Variable']==variable]
    # Keep neighborhood blocks readable within one composite Table 1.
    for start in range(0,len(entries),7):cats.append([variable if start==0 else variable+' (continued)','; '.join(entries[start:start+7])])
table(cats,[130,374])
story.append(Spacer(1,10))
story.append(para('Building codes: 1Fam = detached single-family; 2fmCon = two-family conversion; Duplex = duplex; Twnhs = interior townhouse; TwnhsE = end-unit townhouse. Neighborhood codes follow the supplied codebook. All summaries use n = 2,928.','SmallCustom'))

story.append(PageBreak());heading('Preliminary results');prose(results)
story.append(Image(str(OUT/'interaction.png'),width=504,height=168))
story.append(para(captions['interaction'],'SmallCustom'))
story.append(PageBreak());heading('Residual diagnostics')
story.append(Image(str(OUT/'diagnostics.png'),width=504,height=336))
story.append(para(captions['diagnostics'],'SmallCustom'))
story.append(PageBreak());heading('Plan');prose(plan)

story.append(PageBreak());heading('Preliminary model estimates')
story.append(para(captions['coefficients'],'SmallCustom'))
coefrows=[['Term','Estimate','SE','95% CI']]
for r in rows('coefficients.csv'):
    term=r['Term'].replace('Neighborhood','Neighborhood: ').replace('SaleYear','Sale year: ').replace('Building','Type: ')
    coefrows.append([term,f"{float(r['Estimate']):,.1f}",f"{float(r['SE']):,.1f}",f"[{float(r['Lower']):,.1f}, {float(r['Upper']):,.1f}]"])
table(coefrows,[220,76,65,143],small=False)
story.append(PageBreak());heading('Bibliography')
for ref in refs:prose(ref)
heading('Data access and reproducibility')
prose('Original data: https://jse.amstat.org/v19n3/decock/AmesHousing.txt\n\nCodebook: https://jse.amstat.org/v19n3/decock/DataDocumentation.txt\n\nAccessed October 29, 2026. The original CSV is a lossless tabular conversion of the downloaded text file, preserving identifiers and literal NA category codes. The cleaned CSV records derived variables and complete-case exclusions. The R Markdown contains the complete analysis; analyze.R is an independently runnable base-R version. No data download is needed to rerun the supplied analysis.')
heading('Before submission - remove this working-draft checklist')
prose('Confirm dataset eligibility and read the three substantive papers in full through the library. Fill actual contributions and review all wording as a team. Replace the Module 3 ethics placeholder. Confirm the exact late-November deadline. Submit the proposal PDF, RMD code, and teamwork-agreement PDF; upload original and cleaned CSVs to UofT OneDrive, select anyone in UofT with the link, and include that link in the Quercus submission comment. Only one member submits. No upload or submission has been performed here.')

def footer(canvas,doc):
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#5b6770'))
    canvas.drawString(54,30,'STA302 | Working proposal | Team review required')
    canvas.drawRightString(558,30,str(doc.page))
pdf=ROOT/'proposal_draft.pdf'
SimpleDocTemplate(str(pdf),pagesize=(612,792),rightMargin=54,leftMargin=54,topMargin=42,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)

# A self-contained Rmd: analysis code is embedded rather than sourcing analyze.R.
analysis=(ROOT/'analyze.R').read_text(encoding='utf-8')
md=['---','title: "Does the value of living space vary by dwelling type?"','author: "[Team member names]"','date: "STA302 Part 1 - due November 5, 2026"','output:','  pdf_document:','    latex_engine: xelatex','geometry: margin=0.75in','fontsize: 10pt','---','',
'```{r setup, include=FALSE}',"knitr::opts_chunk$set(echo=FALSE, message=FALSE, warning=FALSE)",analysis,'```','',
'**Working draft:** confirm Ames eligibility; replace team and Module 3 placeholders.','',
'## Contributions','[Member A]: [actual contribution]. [Member B]: [actual contribution]. [Member C]: [actual contribution]. [Member D]: [actual contribution].','',
'## Introduction',intro,'','## Data description',data,'',captions['summary'],'',
'```{r summary-tables, results="asis"}',
"knitr::kable(read.csv('outputs/numeric_summary.csv'), digits=2, row.names=FALSE)",
"knitr::kable(read.csv('outputs/categorical_summary.csv'), digits=2, row.names=FALSE)",
"knitr::kable(read.csv('outputs/missingness.csv'), row.names=FALSE)",'```','',
'## Ethics discussion',ethics,'','## Preliminary results',results,'',
'```{r diagnostics, out.width="100%", fig.cap="'+captions['diagnostics']+'"}',
"knitr::include_graphics('outputs/diagnostics.png')",'```','',
'```{r interaction, out.width="100%", fig.cap="'+captions['interaction']+'"}',
"knitr::include_graphics('outputs/interaction.png')",'```','',captions['coefficients'],'',
'```{r coefficients, results="asis"}',
"knitr::kable(read.csv('outputs/coefficients.csv')[1:5], digits=2, row.names=FALSE, longtable=TRUE)",'```','',
'## Plan',plan,'','## Bibliography','\n\n'.join(refs),'',
'Data and codebook: <https://jse.amstat.org/v19n3/decock/AmesHousing.txt> and <https://jse.amstat.org/v19n3/decock/DataDocumentation.txt>. Accessed October 29, 2026.']
(ROOT/'proposal.Rmd').write_text('\n'.join(md),encoding='utf-8')
print('Created',pdf)
print(wordcounts)
