# STA 220 Project (Winter 2024)
## Exploring Online Learning Landscapes: Insights and Recommendations from Course Data Analysis

## Code Structure

- Within the directories Coursera, Udemy, and PluralSight, you'll find the `.ipynb` files responsible for data scraping or fetching data using APIs from their respective sites. Additionally, each directory contains a file named `<course_platform>_course_all_info.csv`, which comprehensively stores all data pertaining to the columns indicated below.

- The file named `Data Merger.ipynb` houses the code necessary for merging data acquired from all sources. The merged dataset is then saved into a file titled `all_courses_data.csv`.

- Within the `Course Recommendation.ipynb` file, you'll discover code designed to recommend courses based on cosine similarity. This includes preprocessing steps, the recommendation algorithm, and the recommendation function.

- The contents of the `Visualization/Visualization.ipynb` file pertain to data visualization. All resulting `*.html` files are generated as a consequence of these visualizations.


## Table Columns Fetched
1. course_id (ud:udemy, ce:coursera, ps: PluralSight)
2. course_title
3. course_url
4. course_instructor
5. course_rating (out of 5)
6. course_duration (In hrs)
7. course_details (Definition based on the source)
- Udemy(Description+ What you'll learn)
- Courseera(Skills you'll gain + Modules Description)
- PluralSight(What you'll learn)
8. course_level (All: 0, Beginner: 1, Intermediate: 2, Advanced: 3)
9. course_no_of_reviews
10. course_no_of_enrolled


