from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add the URL of your frontend application
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

def fetch_all_course_data():
    udemy_data = pd.read_csv('../../Udemy/udemy_course_all_info.csv')
    udemy_data = udemy_data.drop_duplicates(subset=['course_id'])
    coursera_data = pd.read_csv('../../Coursera/coursera_course_all_info.csv')
    coursera_data = coursera_data.drop_duplicates(subset=['course_id'])
    pluralsight_data = pd.read_csv('../../PluralSight/pluralsight_course_all_info.csv')
    pluralsight_data = pluralsight_data.drop_duplicates(subset=['course_id'])
    udemy_data.drop(columns=['Unnamed: 0'], inplace=True)
    coursera_data.drop(columns=['Unnamed: 0'], inplace=True)

    all_courses_data = pd.concat([pluralsight_data, coursera_data, udemy_data], ignore_index=True)
    all_courses_data = all_courses_data[all_courses_data['course_title'].apply(lambda x: all(ord(char) < 128 for char in x))]
    all_courses_data.reset_index(drop=True, inplace=True) 

    return all_courses_data

# Function to recommend courses based on cosine similarity
def recommend_courses(course_title, cosine_sim_matrix, df, top_n=5):
    # Find the index of the course title in the DataFrame
    idx = df.index[df['course_title'] == course_title].tolist()[0]
    
    # Get the cosine similarity scores for the given course
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    
    # Sort the courses based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top n similar courses (excluding itself)
    top_similar_courses = sim_scores[1:top_n+1]
    
    # Get the indices of the top similar courses
    course_indices = [idx for idx, _ in top_similar_courses]
    
    # Get the course names corresponding to the indices
    recommended_courses = df.iloc[course_indices]
    
    return recommended_courses


all_courses_data = fetch_all_course_data()
tf_idf_similarity = pickle.load(open('../../tf_idf_similarity.pkl','rb'))
count_vectorize_similarity = pickle.load(open('../../count_vectorizer_similarity.pkl','rb'))


# API for providing recommendations based on user search
@app.get("/name-recommendations/")
async def get_name_recommendations(query: str = Query(...)):

    try:

        result_df = all_courses_data[all_courses_data['course_title'].str.contains(query, case=False)]
        result_df = result_df[['course_title', 'course_id']]
        result_dict_list = result_df.to_dict('records')
        return result_dict_list
        
    except Exception as e:
        return {}


# API for returning a list of results
@app.get("/results/")
async def get_results(course_title: str = Query(...), id: str = Query(...)):
    # Here you can implement your logic to fetch results based on the category
    # For demonstration, I'll just return some dummy data
    cosine_vector = tf_idf_similarity

    recommended_courses_data = recommend_courses(course_title, cosine_vector, all_courses_data)
    result_df = recommended_courses_data[['course_title', 'course_id', 'course_url', 'course_instructor', 'course_rating', 'course_duration']]
    result_dict_list = result_df.to_dict('records')
    return result_dict_list

# API for returning a list of results
@app.get("/all-courses/")
async def get_all_courses():
    result_df = all_courses_data[['course_title', 'course_id']]
    result_dict_list = result_df.to_dict('records')
    return result_dict_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
