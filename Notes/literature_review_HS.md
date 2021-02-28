# [Ethnic disparities in stop and search decompose into officer bias and over-patrolling](https://laravomfell.github.io/publication/ethnic_bias/)

Vomfell and Stewart, Univ. of Warwick (UK), Nature Human Behaviour (2021)

## Summary
- UK "stop and search" (2014-2018)
- Two main factors
	- **Ethnicity of suspects** -> contributed to over-representation of Black
	- Ethnic composition of **the areas the police patrol** -> contributed to over-representation of Asian (this was generally stronger factor though)

## Notes
- **Feedback loop** may exist (people who were searched before are more likely to be searched)
- **Deployment decisions, arrest probabilities, and the accurate recording of crime** are NOT independent of ethnic group.
- **Structures within the police force** perpetuate and broadcast biased beliefs through various hierarchies. (**history**)
- At a police-station-level analysis, **pooling all officers together can be misleading** (creating Simpson's paradox).
- Must-read: [Stop-and-frisk in NYC (Gelman et al.)](http://www.stat.columbia.edu/~gelman/research/published/frisk9.pdf)
- Assumption: **(Police) Force over-searching = Officer over-searching x over-patrolling x aggregation discrepancy**
	- Force over-searching = Force search share / Population share
	- Officer over-searching = Officer search share / Officer patrol share
	- Over-patrolling = Officer patrol share / Population share
	- Aggregation discrepancy = Force search share / Officer search share
- Modeling
	- Multinomial model
	- No model comparison

# [A Multi-Level Bayesian Analysis of Racial Bias in Police Shootings at the County-Level in the United States, 2011–2014](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0141854)

Cody T. Ross, UC Davis, PLOS One (2015)

## Summary
- **U.S. Police-Shooting Database (USPSD)**
	- Grassroots data source (crowdsourced)
	- Only available for 2011-2014 data
- County-specific relative risk outcomes of being shot by police as
	1. whether suspects/civilians were **armed or unarmed**
	2. the **race/ethnicity** of the suspects/civilians
- Results
	-  Significant **bias in the killing of unarmed black Americans relative to unarmed white Americans** (3.49 times)
	- Significant **heterogeneity across counties** in the extent of racial bias in police shootings, with some counties showing relative risk ratios of 20 to 1
	- Racial bias in police shootings is most likely to emerge in police departments in 
		- Larger **metropolitan** counties with 
		- **Low median incomes** and 
		- A sizable portion of **black residents**
		- Especially when there is **high financial inequality in that county**
	- No relationship between county-level racial bias in police shootings and **crime rates** (even race-specific crime rates)

## Notes
- Potential discrepancy between goverment-owned dataset (e.g., FBI's Supplemental Homicide Reports) and grassroots 
- UN Committee Against Torture's criticism on militarization of police departments in the US
- Other useful databases
	- Stolen Lives Project
	- Fatal Encounters Database
	- Killed By Police
	- Mapping Police Violence
	- [Washington Post](https://www.washingtonpost.com/graphics/investigations/police-shootings-database/)
	- Guardian
- Explanations suggested by academics on racial bias in olic shooting
	- Officers' implicit bias
	- Structural biases eastablished by the existing social order
	- Proximate responses by police to areas of high violence and crime
	- Ricla bias in profiling and encountering suspects
	- Blatant racism
	- [Social dominance orientation (SDO)](https://en.wikipedia.org/wiki/Social_dominance_orientation): a personality trait measuring an individual's support for social hierarchy ("people with high SDO score adhere strongly to belief in a 'dog-eat-dog' world.")
	- Others
- Research questions
	1. Shot by Police: Armed vs. Unarmed by Race/Ethnicity
	2. Armed and Shot by Police, Across Race/Ethnicity
	3. Unarmed and Shot by Police: Across Race/Ethnicity
	4. Shot by Police: Race/Ethnicity Across Armed Status
	5. County-Level Racial Bias in Police Shootings as a Function of County-Level Properties
		- Population size, racial/ethnic composition, inequality (Gini), median income, race-specific crime rates, norms about racism (using a proxy of racially-based expletives in Google searches)
- Discussion
	- **Encounter rate** data is not available and thus the data cannot explain the relative risk of being shot by the police on being encountered by police.
	- Data collection with **more empiritical evidence**:
		- Shot in the back?
		- Restrained when shot?
		- Circumstances surrounding the shooting
		- Were police called on report of a serious crime?
		- Was the situation escalated by police prior to shooting?
		- Does the race of a suspect vary by the circumstances surrounding the shooting?
		- **Race of the shooter**
		- Are police more likely to escalate a situation when the suspect is black?
		- Did the injured person who was hospitalized die?
- Data
	- 721 shootings
	- Data was crowdsourced
- Model
	- Bayesian linear model
	- No model comparison
	- More complex priors compared to Vomfell and Stewart (2021)

