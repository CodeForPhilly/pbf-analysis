# Questions and analysis
List of questions to address.

## 1. Aggregate-level analysis
These analysis will describe the current state of the bail system and address the question "who / what communities are heavily impacted by the bail system?"

- Q1.1 Aggregate information on bail
	* Total amount of bail set (per year?)
	* Total amount of bail posted (per year?)
	* Distribution of time (detained or not) between arrest and case outcome decided
	* Total days spent in jail (per year?) when bail not posted. 
	* Time series analysis of these statistics

- Q1.2 What is the race statistics of people impacted by bail? (wait for court summary to get race information) Related to Q2.2

- Q1.3 What is the financial stability of the neighborhoods highly impacted by bail? 
	* Use median hosuehold income of each zipcode to show that many people live in high poverty areas.

## 2. Relationships between bail type / amount and various factors 
These analysis will address the question "what determines someone's bail type and bail amount?" 

- Q2.1 Relationship between bail type / amount and the following factors: 
	-  age, zipcode, magistrate, whether they were represented by a private lawyer or a public defender, amount of time detained before prelim/bail hearing (Data available in csv).
	- race, geneder, offense type (Data will be available soon from scraped dockets an court summaries).
	- amount of time (detained or not) between arrest and case outcome decided (Data may be available from old dockets)

- Q2.2 Relationship between defendant race and the following factors. 
	* bail type / amount (Duplicate of quesiton Q2.1with race)
	* amount of time detained before prelim/bail hearing
	* whether bail is posted
	* amount of time (detained or not) between arrest and case outcome decided. (Data may be available from old dockets(
	* Race information will be availabe soon from scraped dockets and court summaries)

- Q2.3 What are the strongest factors determining bail type / bail amount? 
	* do a predictive modeling (regression, decision tress, random forest, etc) & feature importance type analysis
	* wait until we get the race, gender, and offense type information.

- Q2.4 Relationship between outcomes (conviction, sentencing) and bail type, bail amount, and whether bail is posted. (Data may be available from old dockets) 

## 3. Other questions
* Does bail actually lead to better presence at trials? (This analysis could be used to support the end of the bail system. Not sure how we'll get the right data for this.) 