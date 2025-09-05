import pandas as pd
import numpy as np
import streamlit as st
from data import secure_data
import mysql.connector as db


connection = db.connect( 
    host = "localhost", 
    user = "SQLPY",
    password = "Sqlpy@123!@#", 
    database = "db1")

query = "select * from secure_check;"

data = pd.read_sql(query, connection)

q = st.sidebar.radio("Secure_check", ("Select", "🏡Home", "🧾Data_Table", "❓Queries", "🔍Prediction"))

if q == "🏡Home":
    st.title(" 🚦 SecureCheck: Police Post Logs")
    
    st.write("")
    st.write("")
    st.write("")
    
    st.image("C:\\Users\\Dell\\Downloads\\Police secure check.jpg",  use_container_width=True)
    
elif q == "🧾Data_Table":
    st.title(" 🚦 SecureCheck: A Python-SQL Digital Ledger for Police Post Logs")

    st.write("")

    st.write("")


    st.dataframe(data)  
    
elif q == "❓Queries":
    query_groups = {
        "Medium": {
            "🚌 Vehicle based": {
                "1.What are the top 10 vehicle_Number involved in drug-related stops?": """
                    SELECT vehicle_number, COUNT(*) AS drug_stops
                    FROM secure_check
                    WHERE drugs_related_stop = 1
                    GROUP BY vehicle_number
                    ORDER BY drug_stops DESC
                    LIMIT 10;
                """,
                "2.Which vehicles were most frequently searched?": """
                    SELECT VEHICLE_NUMBER, COUNT(*) AS SEARCH_COUNT
                    FROM SECURE_CHECK
                    WHERE SEARCH_CONDUCTED = 1
                    GROUP BY VEHICLE_NUMBER
                    ORDER BY SEARCH_COUNT DESC
                    LIMIT 5;
                """
            },
            "🧍 Demographic-Based": {
                "1.Which driver age group had the highest arrest rate?": """
                    SELECT
                        CASE
                            WHEN DRIVER_AGE <20 THEN '15-19'
                            WHEN DRIVER_AGE BETWEEN 20 AND 29 THEN '20-29'
                            WHEN DRIVER_AGE BETWEEN 30 AND 39 THEN '30-39'
                            WHEN DRIVER_AGE BETWEEN 40 AND 49 THEN '40-49'
                            WHEN DRIVER_AGE BETWEEN 50 AND 59 THEN '50-59'
                            WHEN DRIVER_AGE BETWEEN 60 AND 69 THEN '60-69'
                            WHEN DRIVER_AGE BETWEEN 70 AND 80 THEN '70-80'
                            ELSE '80+'
                        END AS AGE_GROUP,
                        COUNT(*) AS TOTAL_DRIVERS,
                        SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) AS TOTAL_ARREST,
                        ROUND(100 * SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END)/COUNT(*), 2) AS ARREST_RATE
                    FROM DB1.SECURE_CHECK
                    GROUP BY AGE_GROUP
                    ORDER BY ARREST_RATE DESC;
                """,
                "2.What is the gender distribution of drivers stopped in each country?": """
                    SELECT COUNTRY_NAME, DRIVER_GENDER, COUNT(*) AS GENDER_DISTRIBUTION
                    FROM DB1.SECURE_CHECK
                    GROUP BY COUNTRY_NAME, DRIVER_GENDER
                    ORDER BY COUNTRY_NAME, DRIVER_GENDER DESC;
                """,
                "3.Which race and gender combination has the highest search rate?": """
                    SELECT 
                        DRIVER_RACE,
                        DRIVER_GENDER,
                        COUNT(*) AS TOTAL_STOPS,
                        SUM(CASE WHEN SEARCH_CONDUCTED = 1 THEN 1 ELSE 0 END) AS TOTAL_SEARCHES,
                        ROUND(100 * SUM(CASE WHEN SEARCH_CONDUCTED = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS SEARCH_RATE
                    FROM DB1.SECURE_CHECK
                    GROUP BY DRIVER_RACE, DRIVER_GENDER
                    ORDER BY SEARCH_RATE DESC
                    LIMIT 1;
                """
            },
            "🕒 Time & Duration Based": {
                "1.What time of day sees the most traffic stops?": """
                    SELECT
                        CASE
                            WHEN HOUR(STOP_TIME) BETWEEN 0 AND 11 THEN 'MORNING'
                            WHEN HOUR(STOP_TIME) BETWEEN 12 AND 15 THEN 'AFTERNOON'
                            WHEN HOUR(STOP_TIME) BETWEEN 16 AND 19 THEN 'EVENING'
                            ELSE 'NIGHT'
                        END AS TIME_OF_DAY,
                        COUNT(*) AS TOTAL_STOPS
                    FROM DB1.SECURE_CHECK
                    GROUP BY TIME_OF_DAY
                    ORDER BY TOTAL_STOPS DESC
                    LIMIT 1;
                """,
                "2.What is the average stop duration for different violations?": """
                    SELECT VIOLATION_RAW, ROUND(AVG(STOP_DURATION), 2) AS AVERAGE_DURATION
                    FROM DB1.SECURE_CHECK
                    GROUP BY VIOLATION_RAW
                    ORDER BY AVERAGE_DURATION DESC;
                """,
                "3.Are stops during the night more likely to lead to arrests?": """
                    SELECT
                        CASE
                            WHEN HOUR(STOP_TIME) BETWEEN 0 AND 4 THEN 'Night'
                            WHEN HOUR(STOP_TIME) BETWEEN 5 AND 11 THEN 'Morning'
                            WHEN HOUR(STOP_TIME) BETWEEN 12 AND 16 THEN 'Afternoon'
                            WHEN HOUR(STOP_TIME) BETWEEN 17 AND 20 THEN 'Evening'
                            ELSE 'Night'
                        END AS TIME_OF_DAY,
                        COUNT(*) AS TOTAL_STOPS,
                        SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) AS TOTAL_ARRESTS,
                        ROUND(100 * SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END)/COUNT(*), 2) AS ARREST_RATE
                    FROM DB1.SECURE_CHECK
                    GROUP BY TIME_OF_DAY
                    ORDER BY ARREST_RATE DESC;
                """
            },
            "⚖️ Violation-Based": {
                "1.Which violations are most associated with searches or arrests?": """
                    SELECT 
                        VIOLATION_RAW,
                        COUNT(*) AS TOTAL_STOPS,
                        SUM(CASE WHEN SEARCH_TYPE IN ('VEHICLE_SEARCH', 'FRISK') THEN 1 ELSE 0 END) AS SEARCH_COUNT,
                        SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) AS ARREST_COUNT,
                        ROUND(SUM(CASE WHEN SEARCH_TYPE IN ('VEHICLE_SEARCH', 'FRISK') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS SEARCH_RATE,
                        ROUND(SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS ARREST_RATE
                    FROM DB1.SECURE_CHECK
                    GROUP BY VIOLATION_RAW
                    ORDER BY SEARCH_RATE DESC, ARREST_RATE DESC;
                """,
                "2.Which violations are most common among younger drivers (<25)": """
                    SELECT VIOLATION_RAW, COUNT(*) AS TOTAL_STOPS_BY_UNDER25
                    FROM DB1.SECURE_CHECK
                    WHERE DRIVER_AGE <25
                    GROUP BY VIOLATION_RAW
                    ORDER BY TOTAL_STOPS_BY_UNDER25 DESC;
                """,
                "3.Is there a violation that rarely results in search or arrest?": """
                    SELECT 
                        VIOLATION_RAW,
                        COUNT(*) AS TOTAL_STOPS,
                        SUM(CASE WHEN SEARCH_TYPE IN ('VEHICLE_SEARCH', 'FRISK') THEN 1 ELSE 0 END) AS SEARCH_COUNT,
                        SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) AS ARREST_COUNT,
                        ROUND(SUM(CASE WHEN SEARCH_TYPE IN ('VEHICLE_SEARCH', 'FRISK') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS SEARCH_RATE,
                        ROUND(SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS ARREST_RATE
                    FROM DB1.SECURE_CHECK
                    GROUP BY VIOLATION_RAW
                    ORDER BY SEARCH_RATE ASC, ARREST_RATE ASC;
                """
            },
            "🌍 Location-Based": {
                "1.Which countries report the highest rate of drug-related stops?": """
                    SELECT COUNTRY_NAME, COUNT(*) AS TOTAL_STOP_COUNT,
                        SUM(CASE WHEN DRUGS_RELATED_STOP = TRUE THEN 1 ELSE 0 END) AS DRUG_RELATED_STOPS,
                        ROUND(100*SUM(CASE WHEN DRUGS_RELATED_STOP = TRUE THEN 1 ELSE 0 END)/COUNT(*), 2) AS RATE_OF_DRUG_RELATED_STOPS
                    FROM DB1.SECURE_CHECK
                    GROUP BY COUNTRY_NAME
                    ORDER BY RATE_OF_DRUG_RELATED_STOPS DESC;
                """,
                "2.What is the arrest rate by country and violation?": """
                    SELECT COUNTRY_NAME, VIOLATION_RAW, COUNT(*) AS TOTAL_STOP_COUNT,
                        SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) AS ARREST_COUNT,
                        ROUND(100*SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END)/COUNT(*), 2) AS ARREST_RATE
                    FROM DB1.SECURE_CHECK
                    GROUP BY COUNTRY_NAME, VIOLATION_RAW
                    ORDER BY ARREST_RATE DESC;
                """,
                "3.Which country has the most stops with search conducted?": """
                    SELECT COUNTRY_NAME, COUNT(*) AS STOP_COUNT
                    FROM DB1.SECURE_CHECK
                    WHERE SEARCH_CONDUCTED = TRUE
                    GROUP BY COUNTRY_NAME
                    ORDER BY STOP_COUNT DESC;
                """
            }
        },
        "Complex": {"➡️1.":{
            "1.Yearly Breakdown of Stops and Arrests by Country": """
                SELECT 
                    COUNTRY_NAME,
                    STOP_YEAR,
                    TOTAL_STOPS,
                    ARRESTS,
                    ROUND(ARRESTS * 100.0 / TOTAL_STOPS, 2) AS ARREST_RATE,
                    RANK() OVER (PARTITION BY STOP_YEAR ORDER BY (ARRESTS * 1.0/ TOTAL_STOPS) DESC) AS RANK_BY_YEAR
                FROM (
                    SELECT 
                        COUNTRY_NAME,
                        YEAR(STR_TO_DATE(STOP_DATE, '%Y-%m-%d')) AS STOP_YEAR,
                        COUNT(*) AS TOTAL_STOPS,
                        SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) AS ARRESTS
                    FROM DB1.SECURE_CHECK
                    GROUP BY COUNTRY_NAME, YEAR(STR_TO_DATE(STOP_DATE, '%Y-%m-%d'))
                ) AS YEARLY_STATUS
                ORDER BY STOP_YEAR, COUNTRY_NAME;
            """},
            "➡️2.":{"2.Driver Violation Trends Based on Age and Race": """
                SELECT 
                    AGE_GROUP,
                    DRIVER_RACE,
                    VIOLATION_RAW,
                    COUNT(*) AS TOTAL_VIOLATIONS,
                    RANK() OVER (
                        PARTITION BY AGE_GROUP, DRIVER_RACE
                        ORDER BY COUNT(*) DESC
                    ) AS RANK_BY_GROUP
                FROM (
                    SELECT 
                        VIOLATION_RAW,
                        DRIVER_RACE,
                        CASE 
                            WHEN DRIVER_AGE < 25 THEN 'Under 25'
                            WHEN DRIVER_AGE BETWEEN 25 AND 40 THEN '25-40'
                            WHEN DRIVER_AGE BETWEEN 41 AND 60 THEN '41-60'
                            ELSE '60+'
                        END AS AGE_GROUP
                    FROM DB1.SECURE_CHECK
                ) AS AGE_VIOLATIONS
                GROUP BY AGE_GROUP, DRIVER_RACE, VIOLATION_RAW
                ORDER BY AGE_GROUP, DRIVER_RACE, TOTAL_VIOLATIONS DESC;
            """},
            "➡️3.":{"3.Time Period Analysis of Stops": """
                SELECT 
                    YEAR(STR_TO_DATE(STOP_DATE, '%Y-%m-%d')) AS STOP_YEAR,
                    MONTHNAME(STR_TO_DATE(STOP_DATE, '%Y-%m-%d')) AS STOP_MONTH,
                    HOUR(STOP_TIME) AS STOP_HOUR,
                    COUNT(*) AS TOTAL_STOPS
                FROM DB1.SECURE_CHECK
                GROUP BY 
                    YEAR(STR_TO_DATE(STOP_DATE, '%Y-%m-%d')),
                    MONTH(STR_TO_DATE(STOP_DATE, '%Y-%m-%d')),
                    MONTHNAME(STR_TO_DATE(STOP_DATE, '%Y-%m-%d')),
                    HOUR(STOP_TIME)
                ORDER BY STOP_YEAR, MONTH(STR_TO_DATE(STOP_DATE, '%Y-%m-%d')), STOP_HOUR
                LIMIT 100;
            """},
            "➡️4.":{"4.Violations with High Search and Arrest Rates": """
                SELECT 
                    VIOLATION_RAW,
                    TOTAL_STOPS,
                    SEARCHES,
                    ARRESTS,
                    ROUND(SEARCHES * 100.0 / TOTAL_STOPS, 2) AS SEARCH_RATE,
                    ROUND(ARRESTS * 100.0 / TOTAL_STOPS, 2) AS ARREST_RATE,
                    RANK() OVER (ORDER BY (SEARCHES * 1.0 / TOTAL_STOPS) DESC) AS RANK_BY_SEARCH,
                    RANK() OVER (ORDER BY (ARRESTS * 1.0 / TOTAL_STOPS) DESC) AS RANK_BY_ARREST
                FROM (
                    SELECT 
                        VIOLATION_RAW,
                        COUNT(*) AS TOTAL_STOPS,
                        SUM(CASE WHEN STOP_OUTCOME = 'SEARCH' THEN 1 ELSE 0 END) AS SEARCHES,
                        SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) AS ARRESTS
                    FROM DB1.SECURE_CHECK
                    GROUP BY VIOLATION_RAW
                ) AS VIOLATION_STATS
                ORDER BY ARREST_RATE DESC, SEARCH_RATE DESC;
            """},
            "➡️5.":{"5.Driver Demographics by Country": """
                SELECT 
                    COUNTRY_NAME,
                    DRIVER_GENDER,
                    DRIVER_RACE,
                    DRIVER_AGE,
                    COUNT(*) AS TOTAL_DRIVERS,
                    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY COUNTRY_NAME), 2) AS PERCENTAGE_WITHIN_COUNTRY
                FROM DB1.SECURE_CHECK
                GROUP BY COUNTRY_NAME, DRIVER_GENDER, DRIVER_RACE, DRIVER_AGE
                ORDER BY COUNTRY_NAME, DRIVER_GENDER, DRIVER_RACE, DRIVER_AGE
                LIMIT 100;
            """},
            "➡️6.":{"6.Top 5 Violations with Highest Arrest Rates": """
                SELECT 
                    VIOLATION_RAW,
                    COUNT(*) AS TOTAL_STOPS,
                    SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) AS ARRESTS,
                    ROUND(SUM(CASE WHEN STOP_OUTCOME = 'ARREST' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS ARREST_RATE
                FROM DB1.SECURE_CHECK
                GROUP BY VIOLATION_RAW
                ORDER BY ARREST_RATE DESC
                LIMIT 5;
            """}
        }
    }

    query_type = st.sidebar.radio("Select Query Type", list(query_groups.keys()))


    category = st.sidebar.radio(
        "Choose Category",
        ["Select category"] + list(query_groups[query_type].keys())
    )
    
    
    if category != "Select category":
        Query = st.selectbox(
            "Choose Query",
            ["Select Query"] + list(query_groups[query_type][category].keys())
        )
    else:
        Query = "Select Query"
    
    
    if Query != "Select Query":
        Qus = query_groups[query_type][category][Query]
        data = pd.read_sql(Qus, connection)
        st.write(f"### {Query}")
        st.dataframe(data, use_container_width=True)
                    
elif q == "🔍Prediction":
    st.title("🚦 SecureCheck Prediction 🔍")
 


    DRIVER_AGE = st.number_input("Driver Age", min_value = 18, max_value=80, value=20)
    DRIVER_GENDER = st.selectbox("Gender", data["driver_gender"].unique())
    COUNTRY_NAME = st.selectbox("Country", data["country_name"].unique())
    DRIVER_RACE = st.selectbox("Race", data["driver_race"].unique())
    VIOLATION = st.selectbox("violation", data["violation_raw"].unique())
    STOP_DATE = st.date_input("Stop_Date")
    STOP_TIME = st.time_input("Stop Time")
    SEARCH_CONDUCTED = st.selectbox("Search Conducted?", ["No", "Yes"])
    DRUGS_RELATED_STOP = st.selectbox("Drug Related?", ["No", "Yes"])
    STOP_DURATION = st.selectbox("Stop Duration", ["0-5 min", "6-15 min", "16-30 min", "30+ min"])
    STOP_OUTCOME = st.selectbox("Outcome", ["Ticket", "Warning", "Arrest"])
    VEHICLE_NUMBER = st.selectbox("vehicle_number", data["vehicle_number"].unique())
    
    Predict_outcome = st.button("Predict")
    
    if Predict_outcome:
        filtered = data[
            (data["driver_gender"] == DRIVER_GENDER ) &
            (data["driver_age"] == DRIVER_AGE) &
            (data["search_conducted"] == SEARCH_CONDUCTED) &
            (data["stop_duration"] == STOP_DURATION ) &
            (data["drugs_related_stop"] == DRUGS_RELATED_STOP)&
            (data["vehicle_number"] == VEHICLE_NUMBER)
        ]
    
        predicted_outcome = (
        filtered["stop_outcome"].mode()[0] if not filtered.empty else data["stop_outcome"].mode()[0]
        )
        
        predicted_violation = (
        filtered["violation_raw"].mode()[0] if not filtered.empty else data["violation_raw"].mode()[0]
        )
    
        
        search_text = "a search was conducted" if "Yes " else "no search was conducted"
        drug_text = "was drug-related" if "Yes" else "was not drug-related"
    
        st.markdown(f"""
    🚗 **{DRIVER_AGE}-year-old {DRIVER_GENDER} driver** driving **vehicle {VEHICLE_NUMBER}**  
    was stopped for **{predicted_violation} violation**.  
    
    ⏰ The stop lasted **{STOP_DURATION}**, during which {search_text} and it {drug_text}.  
    
    📄 **Predicted Outcome:** **{predicted_outcome}**
    """)
    



        

    
 
        

    


                  
               
                
         
            
                

                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                             
                                         
        






    




