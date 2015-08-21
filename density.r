# getfail = function(x) x %>% mysum %>% .$pfail_raw %>% unlist
# getdelay= function(x) x %>% mysum %>% .$pdelay1hr_raw %>% unlist
# 
# xmax=0.4
# s=d %>% group_by(ORIGIN,DEST,CARRIER) %>% getdelay
# plot(density(s,from=0,to=xmax), ylim=c(0,20))
# 
# s=d %>% group_by(ORIGIN,DEST) %>% getdelay
# lines(density(s,from=0,to=xmax), col='blue')
# 
# s=d %>% group_by(CARRIER) %>% getdelay
# lines(density(s,from=0,to=xmax), col='green')
# 
# s=d %>% group_by(ORIGIN) %>% getdelay
# lines(density(s,from=0,to=xmax), col='red')
# 
# s=d %>% group_by(DEST) %>% getdelay
# lines(density(s,from=0,to=xmax), col='orange')


# Fit the Beta prior on a bunch of MLEs

s1=d %>% group_by(ORIGIN,DEST,CARRIER) %>% mysum %>% filter(n>=1000)
s2=d %>% group_by(ORIGIN) %>% mysum %>% filter(n>=1000)
s3=d %>% group_by(DEST) %>% mysum %>% filter(n>=1000)
s4=d %>% group_by(CARRIER) %>% mysum %>% filter(n>=1000)


fitbeta = function(y) {
    y[y==0]=1e-3
    y[y==1]=1-1e-3
    beta_params = optim(c(1,1), function(p) -sum(dbeta(y, p[1],p[2], log=TRUE)))$par
    beta_params
}


cat("Fail priors\n")
x = do.call(c, lapply(list(s1,s2,s3,s4), function(x) x$pfail_raw))
fitbeta(x) %>% print

cat("Delay priors\n")
x = do.call(c, lapply(list(s1,s2,s3,s4), function(x) x$pdelay1hr_raw))
fitbeta(x) %>% print
