# Run from the ames_proposal folder. Base R only; no package installation needed.
options(stringsAsFactors = FALSE)
dir.create('outputs', showWarnings = FALSE)
raw <- read.delim('data/AmesHousing_original.txt', check.names = FALSE,
                  colClasses = 'character', na.strings = '', strip.white = TRUE)
stopifnot(nrow(raw) == 2930, ncol(raw) == 82)
write.csv(raw, 'data/AmesHousing_original.csv', row.names = FALSE, na = '')
num <- function(name) suppressWarnings(as.numeric(raw[[name]]))
d <- data.frame(PID=raw$PID, SalePrice=num('SalePrice'),
  Living100=num('Gr Liv Area')/100, Building=factor(raw[['Bldg Type']]),
  Lot1000=num('Lot Area')/1000, Quality=num('Overall Qual'),
  Age=num('Yr Sold')-num('Year Built'), Basement100=num('Total Bsmt SF')/100,
  GarageCars=num('Garage Cars'), Neighborhood=factor(raw$Neighborhood),
  SaleYear=factor(raw[['Yr Sold']]), SaleMonth=num('Mo Sold'))
d$Building <- relevel(d$Building, '1Fam')
d$Neighborhood <- relevel(d$Neighborhood, 'NAmes')
vars <- c('SalePrice','Living100','Building','Lot1000','Quality','Age',
          'Basement100','GarageCars','Neighborhood','SaleYear')
missing <- data.frame(Variable=vars, Missing=sapply(d[vars],function(x)sum(is.na(x))))
write.csv(missing,'outputs/missingness.csv',row.names=FALSE)
keep <- complete.cases(d[vars])
write.csv(d[!keep,],'outputs/excluded_missing.csv',row.names=FALSE)
clean <- droplevels(d[keep,])
stopifnot(nrow(clean)>=1000, !anyDuplicated(clean$PID), all(clean$SalePrice>0))
write.csv(clean,'data/AmesHousing_cleaned.csv',row.names=FALSE)
# Centering and unit changes aid interpretation; no log transform or outlier removal.
clean$LivingC <- clean$Living100 - 15
fit <- lm(SalePrice ~ LivingC*Building + Lot1000 + Quality + Age +
          Basement100 + GarageCars + Neighborhood + SaleYear, data=clean)
stopifnot(fit$rank == ncol(model.matrix(fit)))
write.csv(data.frame(n=nobs(fit),sigma=summary(fit)$sigma,
 adjusted_r_squared=summary(fit)$adj.r.squared),'outputs/metrics.csv',row.names=FALSE)
co <- summary(fit)$coefficients
ci <- confint(fit)
write.csv(data.frame(Term=rownames(co),Estimate=co[,1],SE=co[,2],
                    Lower=ci[,1],Upper=ci[,2],P=co[,4]),
          'outputs/coefficients.csv',row.names=FALSE)
numeric_vars <- vars[sapply(clean[vars],is.numeric)]
summ <- do.call(rbind,lapply(numeric_vars,function(v){
 x <- clean[[v]]
 data.frame(Variable=v,N=length(x),Mean=mean(x),SD=sd(x),Min=min(x),
            Q1=unname(quantile(x,.25)),Median=median(x),Q3=unname(quantile(x,.75)),Max=max(x))
}))
write.csv(summ,'outputs/numeric_summary.csv',row.names=FALSE)
cats <- do.call(rbind,lapply(setdiff(vars,numeric_vars),function(v){
 t <- table(clean[[v]])
 data.frame(Variable=v,Level=names(t),N=as.integer(t),Percent=100*as.integer(t)/nrow(clean))
}))
write.csv(cats,'outputs/categorical_summary.csv',row.names=FALSE)
slopes <- do.call(rbind,lapply(levels(clean$Building),function(b){
 L <- setNames(rep(0,length(coef(fit))),names(coef(fit))); L['LivingC'] <- 1
 if(b!='1Fam')L[paste0('LivingC:Building',b)] <- 1
 est <- sum(L*coef(fit)); se <- sqrt(drop(t(L)%*%vcov(fit)%*%L))
 data.frame(Building=b,Estimate=est,SE=se,Lower=est-qt(.975,df.residual(fit))*se,
            Upper=est+qt(.975,df.residual(fit))*se)
}))
write.csv(slopes,'outputs/area_slopes.csv',row.names=FALSE)
reduced <- update(fit,.~.-LivingC:Building)
test <- anova(reduced,fit)
write.csv(test,'outputs/interaction_test.csv')
influence <- data.frame(PID=clean$PID,CooksD=cooks.distance(fit),
 Leverage=hatvalues(fit),Studentized=rstudent(fit))
write.csv(influence[order(-influence$CooksD),],'outputs/influence.csv',row.names=FALSE)
png('outputs/diagnostics.png',width=2100,height=1400,res=180)
par(mfrow=c(2,3),mar=c(4.2,4.2,2.5,1),cex=.8)
plot(fit,which=1,id.n=3)
plot(fit,which=2,id.n=3)
plot(fit,which=3,id.n=3)
plot(fit,which=5,id.n=3)
plot(clean$Age,resid(fit),pch=16,col='#173f5f55',xlab='Age (years)',ylab='Residual (USD)',main='Residuals vs age')
lines(lowess(clean$Age,resid(fit)),col='red',lwd=2); abline(h=0,lty=2)
time <- as.numeric(as.character(clean$SaleYear))+(clean$SaleMonth-1)/12
plot(time,resid(fit),pch=16,col='#173f5f55',xlab='Sale year and month',ylab='Residual (USD)',main='Residuals vs sale time')
lines(lowess(time,resid(fit)),col='red',lwd=2);abline(h=0,lty=2)
dev.off()
png('outputs/interaction.png',width=2100,height=700,res=180)
par(mfrow=c(1,2),mar=c(4.2,4.5,2.4,1),cex=.85)
cols <- c('#176b87','#ba4a00','#6c3483','#229954','#b7950b')
plot(clean$Living100*100,clean$SalePrice,pch=16,col=adjustcolor(cols[clean$Building],alpha.f=.45),
 xlab='Above-ground living area (sq ft)',ylab='Sale price (USD)',main='Observed sales')
legend('topleft',legend=levels(clean$Building),col=cols,pch=16,cex=.7,bty='n')
plot(slopes$Estimate,seq_len(nrow(slopes)),xlim=range(slopes$Lower,slopes$Upper),yaxt='n',
 xlab='Adjusted price difference per 100 sq ft (USD)',ylab='',pch=19,col=cols,main='Type-specific slopes and 95% CIs')
axis(2,at=seq_len(nrow(slopes)),labels=slopes$Building,las=1)
segments(slopes$Lower,seq_len(nrow(slopes)),slopes$Upper,seq_len(nrow(slopes)),col=cols,lwd=2)
dev.off()
capture.output({cat('Original:',nrow(raw),' Complete:',nrow(clean),' Excluded:',sum(!keep),'\n');
 print(summary(fit));print(slopes);print(test);print(summ);
 cat('Largest finite Cook D:',max(influence$CooksD,na.rm=TRUE),'\n');
 cat('Leverage-one cases (undefined standardized diagnostics):',sum(influence$Leverage>1-1e-8),'\n');
 cat('Negative ages:',sum(clean$Age<0),'\n'); print(sessionInfo())},file='outputs/model_log.txt')
saveRDS(fit,'outputs/preliminary_model.rds')
