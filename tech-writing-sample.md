# AWS Region Consolidation Strategy

Short answer: if us-east-1 goes down, it takes all of Tatari with it.

We are in the process of consolidating all of our data eggs in one basket from us-west-2 (Oregon) -> us-east-1 (Virginia).

The fact that we were even in two regions dates back before my time (5yrs+) at least.

From my discussions with people from that time, Henry Z mostly, the decision to be in us-west-2 was so that West Coast Tatarians could have better latency on dev/staging data connections.

Not a good reason and certainly not addressing BCDR (Business Continuity, Disaster Recovery).

DP has observed multiple issues regarding data replication across this boundary and it has cost us money to maintain as well. Therefore they proposed and we are finally moving on consolidating all of our data in us-east-1 where Prod has always lived.

Once complete we will be entirely inside one region and on purpose.

The cost and maintenance to have essentially two copies of our data (Petabytes at last count, but probably is much less if we got good at getting rid of stuff we don't need) is too cost prohibitive and not really realistic for a company our size and the nature of the business we are doing.

That said, SRE mostly, but some DP efforts are aimed at making the ability for us to spin up a new account, new eks, new s3, new whatever in the same region or another region, is something we are constantly working towards. The idea being that, we could make it relatively painless for us to set up shop in another region in the event of a large outage. But unless that outage goes into the months+, it is probably better for us just wait (with the rest of the world, everyone is in us-east-1) for it to come back online.

Important to note that in this scenario. The data is gone, but we would aim to set up ingestion and what not, to start over with a new copy. Measurement teams would play a role at knowing how much and at what cutoff points we should employ to rebuild up our data. But there definitely would be disruption.

Part of the calculus here, is that if us-east-1 goes down, the entire internet is going to be having a real bad day, such that even if we were immediately able to move to us-east-2 (Ohio) many of our partners and data providers would not. So what are we talking about?
