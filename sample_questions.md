# Sample Questions

## BEGINNER LEVEL (Simple SELECT queries)

1. **Basic Selection**
   - "Show me all the Olympic sports" FAIL
   - "List all the cities that have hosted Olympics" SUCCESS
   - "What are the different types of medals?" SUCCESS

2. **Simple Filtering**
   - "Show me all Summer Olympic games" SUCCESS
   - "Find all competitors from the United States"
   - "List all events in Swimming"

3. **Basic Counting**
   - "How many Olympic sports are there?"
   - "How many people have competed in the Olympics?"
   - "Count the number of Olympic games held"

---

## INTERMEDIATE LEVEL (JOINs and basic aggregations)

4. **Single JOIN Queries**
   - "Which cities hosted the 2008 Olympics?"
   - "Show me all competitors who won gold medals"
   - "List all events that took place in the 1996 Olympics"

5. **Basic Aggregations with GROUP BY**
   - "How many medals has each country won?"
   - "Count the number of events in each sport"
   - "Show the number of competitors in each Olympic games"

6. **Filtering with JOINs**
   - "Find all gold medalists from Canada"
   - "Show me swimmers who won any medal in 2004"
   - "List all female competitors who won bronze medals"

7. **Date/Year-based Queries**
   - "Who won medals in the 1992 Olympics?"
   - "Show all Winter Olympics held between 1980 and 2000"
   - "Find competitors who participated in Olympics before 1950"

---

## ADVANCED LEVEL (Complex JOINs, subqueries, window functions)

8. **Multiple JOINs**
   - "Show me the names of all gold medalists, their countries, and the cities where they won"
   - "List all swimming events, the winners, and which Olympics they were in"
   - "Find all competitors from Australia who won medals in track and field events"

9. **Aggregation with Complex Filtering**
   - "Which country has won the most gold medals in gymnastics?"
   - "Show the top 10 athletes with the most total medals"
   - "Find countries that have won medals in both Summer and Winter Olympics"

10. **Subqueries and Comparisons**
    - "Who are the tallest athletes who have won gold medals?"
    - "Find athletes who have won more than 5 medals"
    - "Show countries that have never won a gold medal"

11. **Multi-Olympics Analysis**
    - "Which athletes competed in more than 3 different Olympic games?"
    - "Find athletes who won medals in consecutive Olympics"
    - "Show countries whose medal count improved from one Olympics to the next"

---

## EXPERT LEVEL (Complex analytics, window functions, CTEs)

12. **Ranking and Window Functions**
    - "Rank countries by their total medal count and show their percentile"
    - "For each Olympics, show the top 3 countries by gold medal count"
    - "Calculate the running total of medals won by the USA across all Olympics"

13. **Complex Multi-table Analysis**
    - "Find athletes who switched countries between Olympics and won medals for both"
    - "Show the age distribution of medal winners by decade"
    - "Calculate the medal efficiency rate (medals per athlete) for each country"

14. **Advanced Statistical Queries**
    - "What's the average height and weight of gold medalists in different sports?"
    - "Find the correlation between a country's total athletes sent and medals won"
    - "Show the sports where the USA has the highest medal percentage compared to other countries"

15. **Time Series and Trend Analysis**
    - "How has the number of female participants changed over time in Olympics?"
    - "Show the trend of medal distribution (Gold/Silver/Bronze) across decades"
    - "Find countries that had their best Olympic performance (by medal percentage) in recent games"

16. **Complex Business Logic**
    - "Identify 'comeback' athletes who won medals after competing in Olympics without winning"
    - "Find the most 'balanced' countries (similar numbers of Gold, Silver, Bronze medals)"
    - "Calculate the 'dominance factor' - countries winning medals in sports where few countries compete"

---

## EXPERT+ LEVEL (Advanced analytics requiring domain knowledge)

17. **Multi-dimensional Analysis**
    - "Create a medal 'efficiency score' adjusting for population and GDP of countries"
    - "Find Olympic 'dynasties' - families where multiple members won medals"
    - "Analyze home field advantage - do host countries perform better?"

18. **Predictive and Pattern Analysis**
    - "Based on historical data, which countries are most likely to win medals in new sports?"
    - "Find athletes whose performance pattern suggests they might compete in future Olympics"
    - "Identify sports where medal winners have become significantly taller/heavier over time"

19. **Cross-temporal Comparisons**
    - "If we normalize for the number of events available, which era had the most dominant athletes?"
    - "Compare the 'medal concentration' - are medals more or less distributed among countries now vs. historically?"
    - "Find the 'most improved' countries by comparing their recent 20-year performance to their historical average"

20. **Advanced Relationship Analysis**
    - "Find coaches or support staff who have been associated with multiple medal-winning athletes across different Olympics"
    - "Analyze 'training camp effects' - athletes from the same region/facility who won medals in the same Olympics"
    - "Create a 'competitiveness index' for each sport based on how many different countries have won medals"

---

## Natural Language Complexity Variations

Each question type can be asked in various ways to test natural language understanding:

**Formal Style**: "Calculate the total number of gold medals won by American athletes in swimming events"

**Casual Style**: "How many swimming golds did the US win?"

**Conversational Style**: "I'm curious about American swimmers - how many of them took home gold medals?"

**Ambiguous Style**: "Show me the best US swimmers" (requires interpretation of "best")

**Context-dependent**: "Who were their main competitors?" (requires context from previous query)

**Comparative Style**: "Which country is better at swimming, USA or Australia?"

**Temporal Ambiguity**: "Recent Olympic swimming results" (requires defining "recent")

**Colloquial Terms**: "Show me the GOAT swimmers" (Greatest Of All Time)