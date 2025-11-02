from streamlit_option_menu import option_menu
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from streamlit_lottie import st_lottie
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import json
import time
from utils import *

df = pd.read_csv("da_internship_task_dataset.csv")

st.set_page_config(page_title="Analytics for ML features", layout="wide")
st.title('Analytics for ML features')
st.sidebar.title("Visualise data")
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation bar",
        options=["Overview", "Relation Exploration", "Trends over time", "User Behaviour Analysis", "Summary"],
        styles = {"nav-link-selected":{"background-color": "#810f7c"} }
    )

def load(message = "All ready!"):
    """

    :param message: message to be displayed after loading
    :return: animation from https://app.lottiefiles.com    """

    with open("Loader_cat.json", "r") as f:
        lottie_tea = json.load(f)
    placeholder = st.empty()

    with st.spinner("your data is purring..."):
        with placeholder.container():
            left, center, right = st.columns([1, 2, 1])
            with center:
                st_lottie(lottie_tea, height=400, width=400)
        time.sleep(7)

    placeholder.empty()
    st.success(message)

if selected == "Overview":
    st.subheader("Project Overview")
    load("Visualisation loaded")

    table1(df)
    st.markdown("""
    The heatmap shows that user activity is concentrated around Models C and D, particularly for high-demand features such as Feature_1 and Feature_4.
This suggests that these models are likely perceived as the most efficient or accurate for the platform’s core tasks.
In contrast, Models A and B display consistently lower engagement, indicating limited or specialized usage.
Overall, the system shows strong model–feature alignment, where user preferences reveal which combinations deliver the most value.
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot17(df), use_container_width=True)
    with col2:
        st.plotly_chart(plot18(df), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        * Feature_1 is by far the most frequently used, followed by Feature_2 and Feature_3.
        * Feature_4 and Feature_5 have significantly fewer counts, suggesting they are more specialized or less frequently needed.
        * It suggests that users rely heavily on a limited set of key features while others remain underutilized.
        """)
    with col2:
        st.markdown("""
        * The Basic and Standard license types dominate the user base, with the highest activity counts.
        * Premium and Enterprise licenses appear smaller in volume, suggesting a smaller but possibly higher-value user segment.
        """)

if selected == "Relation Exploration":
    st.subheader("Relation Exploration")
    load()
    st.write("Exploring relationships between models, licenses, and features with key metrics like requests_cnt and spent_amount.")
    plot1(df)

    st.markdown("""
        * **Premium** and **Enterprise** licenses generally show higher median request counts, indicating heavier or more consistent usage.
        * **Basic** and **Standard users** tend to have lower medians and wider variability, suggesting irregular or lower-intensity usage.
        * Models such as Model_D and Model_C exhibit broader distributions across license types, reflecting a diverse range of user behaviors.
        * Model_A and Model_B have comparatively narrower spreads for most licenses, implying more uniform request patterns.
        """)
    st.write("**This suggests that usage patterns scale predictably with license tier, reflecting clear segmentation of user engagement levels.**")
    plot2(df)
    st.write(" While usage frequency (requests) varies among models, the volume or size of processed units is more stable across different models.")
    st.markdown("""
        * Premium and Enterprise licenses consistently show higher medians and wider ranges, indicating greater engagement and workload capacity.
        * Basic and Standard licenses cluster at lower values, reflecting lighter or less consistent activity — a pattern consistent across both requests and units.
        """)
    st.write("Both charts suggest that Premium and Enterprise users generate both higher frequency and higher usage, confirming their higher system utilization.")
    plot3(df)
    st.markdown("""
    * Model_C and Model_D dominate overall spending particularly in feature 4
    * Across all models, Feature_4 consistently records above-average spending, peaking at 22.8 for Model_C.
    * Model_B displays generally lower average spending across all features, with a notably low value (4.4) for Feature_4.
    * Model_E maintains consistent mid-range values across features (7.9–13.5), suggesting a stable, balanced approach to feature cost allocation. It might be general-purpose model.
    """)
    plot4(df)
    st.markdown("""
    * requests_mean:  
     
     We can observe the highest mean request usage for model C and D and the lowest for model A and B.
    * spend mean
    
    It is around the same for all the models which means that amount of units (credits) spent within the day per model is equal.
    * requests std
    
    It is similarly to mean, the highest for model C and D but differently lowest for E and A.
    * spend std
    
    It is the highest for model C with the value of 51 and the lowest for model E with 12.
    """)
    st.write("Models C and D demonstrate the highest mean request usage and largest variability, indicating that they are the most actively and diversely used models across the user base. In contrast, Models A and B record the lowest request means, suggesting limited adoption or more specialized use. Interestingly, the average spending per model remains relatively consistent, which implies a balanced credit consumption rate — users spend roughly the same amount per day regardless of the model they use. However, variability in spending (standard deviation) differs: Model C shows the highest fluctuation in spending (std = 51), likely reflecting diverse usage intensities or premium feature use, while Model E maintains the most stable and lowest spending variance (std = 12), indicating predictable or limited usage patterns.")
    plot5(df)
    st.markdown("""
    A strong positive correlation (r = 0.94) reveals that spending grows almost linearly with user activity, it indicates a clear usage-based pricing model. 
    Users who submit more requests consistently spend more which we would expect to happen. The imperfections around the line might have been caused by different licenses and features.
    * Above the line -> users relying on premium or higher-cost models.
    * Below the line -> users utilizing lower-cost or limited features.
    """)
    plot6(df)
    st.markdown("""
    Now let's see it broken down by license! Each color represents a different license, with its own regression line showing how spending scales with request volume within that membership.
    * Premium users maintain the highest overall spending and extend furthest along the request axis, indicating heavy and consistent engagement.
    * Enterprise users show a steeper slope, suggesting that each request costs more on average — likely due to advanced or higher-value features.
    * Basic and Standard users cluster near the origin, reflecting limited usage and minimal spending.
    """)
    plot8(df)
    st.write("We can see that Models C and D consistently have the highest spending values, especially for Feature 4 and Feature 1, indicating these combinations drive the most usage or cost. In contrast, Models A and B show much lower averages across all features, suggesting they are less resource-intensive or less frequently used.")

if selected == "Trends over time":
    plot7(df)
    st.markdown("""
    The correlation remains consistently high (≈0.9–1.0), indicating a stable and predictable relationship between activity and spending.
    Possible causes of flactuations are:
    * Users might shift temporarily toward cheaper models or features - Activity (requests) goes up, but spending doesn’t rise as fast so we observe lower correlation.
    * Around weekends, holidays, or updates, users might test or interact differently — producing non-representative activity spikes.
    """)
    plot9(df)
    st.markdown("""
    The clear peaks and troughs suggest a repeating weekly cycle. Spending raises for several consecutive days, then drops almost to zero before rising again.
    This likely reflects weekly usage behavior, such as:
    * Higher activity during workdays (when models are used for production, analysis, or operations),
    * Lower or no usage on weekends (when users are inactive or systems are paused).
""")
    plot10(df)
    st.markdown("""
    * After a sharp increase early in the observed period (around late February–early March), values stabilize with small fluctuations.
    * Spending and requests move in sync — when request volume rises, spending follows.
    """)
    plot11(df)
    st.markdown("""
    * Across all license types, total requests increase steadily month over month, indicating growing engagement.
    * Premium users consistently record the highest request counts, followed by Enterprise and Standard, while Basic users remain the least active but still show significant growth.
    """)
    plot20(df)
    st.markdown("""
            * Dominant segment:
        > The “High activity, low spend (free users)” group consistently forms the largest portion of active users, suggesting that most engagement comes from non-paying users.
        * Stable core users:
        > The “High both (core users)” segment remains stable throughout the period, showing a loyal, consistent base of active and paying users.
        * Limited power buyers:
        > The “High spend, low activity” group stays small and steady, indicating few high-value but low-engagement customers.
        * Low engagement segment persistence:
        > The “Low activity, low spend” area is minor but continuous, reflecting users who occasionally return but don’t contribute significantly to overall activity.
        * Growth trend:
        > Toward late May, total user volume slightly increases, mainly driven by free and core users, hinting at growing engagement.
            """)

if selected == "User Behaviour Analysis":
    plot12(df)
    st.markdown("""There are three engagement stages:
* Used app – 1866 users
 > Total number of users who have been active at least once.
* Used multiple features – 1802 users
 > Most users (≈97%) explored more than one functionality.
* Spent > 100 credits – 1452 users
 > Around 78% of users transitioned into meaningful spending behavior.
    """)
    plot13(df)
    st.markdown("""
    * The retention distribution suggests that while some users drop off quickly, the majority are staying active for more than a month.
    * Premium and Enterprise users make up a huge portion of long-term active users, implying that higher-tier licenses correlate with stronger retention.
    * Basic and Standard licenses dominate the early days but taper off, indicating that casual or trial users stop usage earlier.
    
    We can see a bimodal-like pattern:
    * A smaller group of users who were active for only a few days (low retention).
    * A dominant peak around 40–50 days active, where most users concentrated — showing consistent engagement over time.
    """)
    plot19(df)
    st.markdown("""
    We can observe another plot in favour of statement that higher-tier licenses correlate with stronger retention as the median of premium and enterprise users is much higher than that of standard and basic tier. 
    """)

    col1, col2 = st.columns(2)
    with col1:
        plot14(df)
    with col2:
        plot15(df)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        * The average spend per request is nearly identical across all license types — Basic, Standard, Premium, and Enterprise.
        
        * This suggests that the cost structure is consistent regardless of user tier; all licenses likely share the same pricing per request or resource usage rate.
        
        * Therefore, total spending differences between licenses are mainly driven by volume of requests, not per-request pricing.
        """)
    with col2:
        st.markdown("""
        A clear variation is visible here:
        * Model A and Model B have the highest per-request spending, around 0.33–0.35 units.
        
        * Models C, D, and E cluster lower, around 0.18–0.19 units.
        
        * This implies that different models have different cost or resource demands, possibly reflecting computational complexity.
        """)
    plot16(df)
    st.markdown("""
    * The Premium and Enterprise licenses dominate the top spenders, suggesting that higher-tier licenses correlate with heavier usage and greater spending power.
    * The leading Premium user (user_935) stands out significantly, spending over 50k units, well above others — a potential super-user or enterprise-level account.
    * The long tail of smaller spenders confirms a power-law distribution, where a small minority of users account for the majority of total spending.""")

if selected =="Summary":
    summary_kpis(df)
    summary(df)
