library(readr)
library(dplyr)

files = sort(Sys.glob("data/*.csv"))
# files = rev(Sys.glob("data/*.csv"))[1:3]

d = rbind_all(lapply(files, function(f) {
cat(sprintf("Reading file %s\n", f))
read_csv(f) %>% select(FL_DATE, CARRIER, ORIGIN, DEST, ARR_DELAY, CANCELLED, DIVERTED)
}))

print(d)
gc() %>% print

d$CANCELLED=as.logical(d$CANCELLED)
d$DIVERTED=as.logical(d$DIVERTED)
d$month = factor(d$FL_DATE %>% gsub("^[0-9]*-","", .) %>% gsub("-[0-9]*$","",.))
d$suc = with(d, !CANCELLED & !DIVERTED)
gc() %>% print

# sanity checks.
# arrival delay is NA iff the flight did not succeed
stopifnot(all(!is.na(d$ARR_DELAY[d$suc])))
stopifnot(all(is.na(d$ARR_DELAY[!d$suc])))

whitelist=d %>% group_by(a=ORIGIN) %>% summarise(nout=n()) %>% left_join(d %>% group_by(a=DEST) %>% summarise(nin=n())) %>% mutate(tot=nout+nin) %>% arrange(-nin) %>% head(100) %>% select(a) %>% unlist

d = filter(d, ORIGIN %in% whitelist & DEST %in% whitelist)
gc() %>% print

ac_hi = function(p,n, z=2) {
# high side of the agresti-coull CI (give negative z for low side)
# default z=2 is top of a two-sided 95.4% CI  (= 1-(1-pnorm(2))*2),
# or a one-sided 97.7% CI from 0 to 97.7%ile (= pnorm(2))
    k = n*p
    p2 = (k+0.5*z^2)/(n+z^2)
    se = sqrt(p2*(1-p2)/(n+z^2))
    pmax(0,pmin(1, p2+z*se))
}

mysum = function(x) summarise(x, n=n(),
        pfail_raw=mean(!suc), 
        pdelay1hr_raw=mean(!suc | ARR_DELAY>60)) %>%
    mutate(pfail=ac_hi(pfail_raw,n), pdelay1hr=ac_hi(pdelay1hr_raw,n))

mywrite = function(data,filename) write.csv(sprintf(data,
                            sprintf("summary_data/%s",filename), row.names=FALSE)

src = d %>% group_by(ORIGIN) %>% mysum
src %>% arrange(ORIGIN) %>% mywrite("rank_origin.csv")
dst = d %>% group_by(DEST) %>% mysum
dst %>% arrange(DEST) %>% mywrite("rank_dest.csv")
inner_join(src,dst, by=c("ORIGIN"="DEST")) %>% mywrite("rank_airports.csv")
d %>% group_by(CARRIER) %>% mysum %>% arrange(CARRIER) %>% mywrite("rank_carrier.csv")
d %>% group_by(month) %>% mysum %>% arrange(month) %>% mywrite("rank_month.csv")
d %>% group_by(ORIGIN,DEST) %>% mysum %>% filter(n>=100) %>% arrange(ORIGIN,DEST) %>% mywrite("rank_pair.csv")
d %>% group_by(ORIGIN,DEST,CARRIER) %>% mysum %>% arrange(pdelay1hr) %>% mywrite("rank_pair_carrier.csv")

